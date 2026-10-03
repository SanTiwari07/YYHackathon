# Runbook — retention duties, Redis degradation, cursor key rotation

Owner: P1. Design: [ADR 0018](../adr/0018-redis-optional-limiter-and-retention.md). Binary: `cmd/maintenance` (retention, privacy reconcile),
`cmd/api` (limiter, cursors).

## 1. Retention

**What runs:** every `RETENTION_INTERVAL_S` (default 3600) the `retention` duty runs the rules of ADR 0018 §4 in a fixed order; each rule is bounded per
pass (`RETENTION_BATCH` rows per database call, at most 20 calls per rule), so a large backlog is worked off over several passes.

**Look at what it is about to do — dry run first.** Set `RETENTION_DRY_RUN=1` on the maintenance service and restart it. The duty then only counts; the
log line `retention` carries `candidates` per rule with `dry_run=true`. Nothing is deleted, no object is touched, and the database floors still apply.
Turn it off (`unset`) only after the counts look right. A new environment should always start in dry-run.

**Reading the log line** (`msg="retention"`, one per rule that had work): `rule`, `dry_run`, `candidates`, `deleted`, `objects` (delete calls to the
object store), `skipped`, `error`. There is no tenant, user or object key in it. `skipped > 0` means an item was left on purpose (its object could not be
deleted this pass — retried next pass — or a key did not belong to its row's tenant, which needs a human).

| Symptom | Meaning | Action |
|---|---|---|
| `rule=audit error=export_not_verified` | The signed export does not cover the days to purge, or does not verify (missing day, bad signature, broken chain, altered file) or audit records predate the first export | **Nothing is purged, by design.** Verify the export (`auditexport.Verify`; see `audit-and-support-access.md`), repair the export first, then let the duty continue. Never lower the window to get around it |
| `rule=erasure_ledger error=failed` (database message "younger than 30 days") | `BACKUP_RETENTION_DAYS` + margin is below the 30-day floor | Fix the configuration; the floor cannot be lowered without a migration |
| `rule=audit error=failed` ("younger than 90 days") | `AUDIT_RETENTION_DAYS` below 90 | Fix the configuration (config validation also refuses it) |
| `skipped` grows every pass on `uploads_incomplete` / `reports` | The object store is refusing deletes | Check the store and the maintenance identity's IAM on the quarantine/ready buckets; rows are kept until the object is gone |
| `orphan_objects` `skipped` > 0 | An object under `tenant/` whose key is not the platform layout | Investigate manually; the sweeper never deletes it |

**Windows are proposals.** Every window is "product policy pending approval" (spec §07.7) and appears in the startup log line
`retention policy (product policy pending approval)`. Changing one is a configuration change (`IDEMPOTENCY_RETENTION_H`, `INBOX_RETENTION_DAYS`,
`RAW_UPLOAD_RETENTION_DAYS`, `REPORT_RETENTION_DAYS`, `AUDIT_RETENTION_DAYS`, `BACKUP_RETENTION_DAYS`, `ORPHAN_SAFETY_H`); the ranges are validated at
startup. **Shortening** a window deletes data at the next pass — run a dry run first. `IDEMPOTENCY_RETENTION_H` and `INBOX_RETENTION_DAYS` apply when a row
is *written* (each row carries its own expiry), so changing them affects new rows only. Log retention (`OPERATIONAL_LOG_DAYS`) is applied by the log
sink, not by this binary.

**Audit retention needs the export.** Without `AUDIT_EXPORT_DIR` the duty logs `audit retention disabled` and never purges audit records. Each audit
purge leaves an `audit.retention_purge` record (reason `retention_purged_<n>`) in every tenant it touched.

**Privacy reconciliation** (`privacy-reconcile`, every 5 minutes): a verified / cooling-off / running privacy request with no live job gets a new job; after
5 jobs it is failed with `PRIVACY_JOBS_EXHAUSTED` (audited) — investigate why its jobs die. Held requests are never touched.

## 2. Redis degradation

Redis is optional to correctness. When it is unreachable: `GET`s are answered from PostgreSQL as usual; the limiter falls back to a per-instance counter
at half the configured limit (`USER_READ_RPM` / `USER_WRITE_RPM`); `/readyz` stays **200** with `{"status":"degraded","degraded":["redis"]}`; nothing durable
is affected (idempotency, quotas, jobs, audit are SQL). Expect somewhat more `429 RATE_LIMITED` for heavy users during the outage (bounded by the local
share) and no other visible change. Nothing needs to be restarted for recovery: the client's circuit breaker re-probes every 2 seconds. A rebuilt (empty)
Redis is fine — it is not a recovery source.

Redis settings: `REDIS_ENDPOINT` (required outside dev), `REDIS_AUTH_SECRET` (injected from the secret manager), `REDIS_TLS_ENABLED` (must be true outside
dev), `REDIS_OPERATION_TIMEOUT_MS` (20..1000, default 100). Memory policy for the server: cache-only, e.g. `maxmemory-policy allkeys-lru`, no persistence.

## 3. Cursor key rotation

Cursors are HMAC-signed with a keyring (`CURSOR_KEYS` = `id:base64,…`, `CURSOR_ACTIVE_KEY_ID`); the key id is part of what is signed. A cursor lives at
most 15 minutes, which bounds every rotation step.

1. **Add** the new key to `CURSOR_KEYS` (keep the old one) but leave `CURSOR_ACTIVE_KEY_ID` on the old id. Deploy to **every** instance. (Old instances
   that do not yet know the new key would reject cursors signed with it in the next step, so all instances must have it first.)
2. **Activate:** set `CURSOR_ACTIVE_KEY_ID` to the new id. New cursors are signed with it; in-flight cursors signed with the old key still verify.
3. **Wait at least 15 minutes** (the cursor lifetime; add a margin).
4. **Retire** the old key: remove it from `CURSOR_KEYS`. Any cursor still signed with it is rejected (`400`), which clients handle by starting the list again.

**Rollback:** while both keys are present, set the active id back. After step 4, re-adding the old key restores verification of cursors signed with it, but
those cursors have expired by then anyway. A suspected key leak: do steps 1–4 with a shortened wait, then treat every cursor issued under the leaked key as
void (it is: step 4 rejects them) — a cursor grants nothing beyond a page position, and every page re-authorises the caller against the primary database.

Key requirements: at least 32 random bytes, id up to 32 characters without `.`, spaces or control characters, distinct from every other key in the system.
An unusable cursor is always `400 BAD_REQUEST` (decision E9), never a 401/403/500.
