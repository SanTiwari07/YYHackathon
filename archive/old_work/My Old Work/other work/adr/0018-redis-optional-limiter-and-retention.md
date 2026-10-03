# ADR 0018 — Redis is optional to correctness; the per-user limiter; retention with floors in the database

- **Status:** Accepted (P1, Sprint 9). Implements task 1.23 of [the Phase 2–3 plan](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE2_3_PLAN.md). Migration **00021**.
- **Owner:** P1 (platform)
- **Spec:** 6182 §07.5 ("Redis does not store the only job, permission, refresh token, event, audit or budget record. Loss triggers bounded DB fallback
  and shedding; expensive job admission remains SQL-transactional"), §07.7 (retention defaults, "Retention windows are config, not code"), §15-§16
  (`USER_READ_RPM`, `USER_WRITE_RPM`, `REDIS_*`, `*_RETENTION_*`), §10 acceptance scenario **T25**, decision E9 (cursors).

## Decision in one paragraph

Redis holds only things that may be lost: cached projections and one-minute abuse counters, every key with a TTL. It is reached through a small RESP2
adapter (no client library) with hard deadlines and a circuit breaker; every failure becomes "a miss" or "a local decision", never an error to an
authorised caller. The per-user limiter (`USER_READ_RPM` / `USER_WRITE_RPM`) is an *abuse* control that runs after authentication and degrades to a
conservative, bounded, in-process counter; the durable budgets and quotas stay in PostgreSQL and are untouched by it. Retention is **a function, not a
privilege**: `cmd/maintenance` may only call `app.retention_purge()`, a `SECURITY DEFINER` function owned by a constrained role, and the floors below live in
that function, so no configuration or code mistake can lower them.

## 1. The Redis adapter (`internal/adapters/redis`)

- RESP2 over TCP, TLS optional (`REDIS_TLS_ENABLED`, on by default outside dev and refused off there), `AUTH` from `REDIS_AUTH_SECRET` (a `config.Secret`,
  never in an error or a log). Five commands: `PING`, `GET`, `SET … PX`, `DEL`, and one atomic `EVAL` (increment, set the expiry only when the key is
  new: a fixed window that can never live forever). No new dependency (AGENTS.md rule 6).
- **Deadlines:** every call is bounded by `REDIS_OPERATION_TIMEOUT_MS` (20..1000, default 100) and by the caller's context. Socket deadlines use the wall
  clock; only the breaker takes an injected clock.
- **Circuit breaker:** after 3 consecutive connection failures the breaker opens; calls fail immediately (no dial) for a 2 s cool-down; then exactly one
  probe is admitted. A *server error reply* is not a failure (Redis answered).
- **Errors:** always wrap `ErrUnavailable` with a class only (`timeout`, `closed`, `open`…), never the address, a key or a value.
- **Replies are untrusted:** bulk strings are capped at 1 MiB, arrays at 1024 entries and 4 levels; a fuzz target proves the parser never panics or
  allocates the length the peer claims.
- **Every value expires:** `Set` refuses a non-positive TTL, `Incr` a non-positive window; a test asserts every key on the server has a TTL.
- **`redistest`** is an in-process RESP2 server with failure injection (kill, restart on the same address, freeze, garbage, password). It is *not* Redis;
  real Redis is the reference: `conformance_test.go` and `TestT25AgainstARealRedis` run against it when `REDIS_TEST_ADDR` is set (S9 ran them against Redis 7.2.6).

## 2. The cache port (`internal/platform/cache`)

`Key{Env, Cell, Tenant, ScopeRev, Kind, Version, Filter}` renders the specification's `env:cell:tenant:scope_rev:kind:vN:filterhash`; every part is mandatory
and validated (a colon, wildcard or newline is refused), the filter is canonicalised and hashed, and the **scope revision is in the name**, so bumping it
makes every older entry unreachable without a scan, and a failed `Del` cannot serve stale scoped data. `Guarded` wraps any store: an error is a miss on
read and best-effort on write, counted in aggregate stats. **No endpoint reads through the cache yet** (P1 has no cacheable projection; P2/P3 add theirs
against this port), so the cache is delivered and tested, not consumed.

## 3. The limiter (`internal/platform/ratelimit`)

Fixed one-minute windows per (user, class) — `GET`/`HEAD` are reads, everything else writes — counted in Redis under `rl:<env>:<cell>:<user>:<r|w>:<window>`.
Denied requests are `429 RATE_LIMITED` with `Retry-After` (all 82 operations already document 429 in the contract: **no contract change**). Keyed by the
authenticated user only, after authentication (a request with no identity is passed to its handler, which answers 401).

**Failure policy (T25):** if the counter is nil, errors or times out, the decision is local: per-instance in-memory windows with `LocalShare` (default 0.5)
of the configured limit — *conservative*, because N instances each allow that share — and a table capped at 50 000 users (users beyond it share one
overflow bucket, so memory and admissions are bounded). It neither fails open nor locks everyone out. Counters are aggregate (allowed, denied, degraded);
no user, tenant or key is a label. Readiness reports Redis as **degraded, still 200** (`ReadyCheck.Optional`): a cache outage must not take every instance
out of rotation. `REDIS_ENDPOINT` is a required selection outside dev (the deployed API is configured with it) but the API runs without it.

**What the limiter is not:** the tenant-creation cap, idempotency, job admission and the privacy request rules are SQL. T25 kills, freezes and rebuilds
Redis mid-run and proves those still hold, including under concurrency.

## 4. Retention (`app.retention_purge`, `maintenance.Retention`)

| Rule | What | Window (config) | Floor in the database |
|---|---|---|---|
| `idempotency`, `inbox` | rows past their own `expires_at` | applied at write time (`IDEMPOTENCY_RETENTION_H` 24..168, `INBOX_RETENTION_DAYS` 7..90) | never an unexpired row, whatever cutoff |
| `uploads_incomplete` | pending/expired/rejected/quarantined assets and their **quarantine** objects | `RAW_UPLOAD_RETENTION_DAYS` 1..30 (7) | nothing younger than 1 day |
| `reports` | ready assets of purpose `report` and their **ready** objects | `REPORT_RETENTION_DAYS` 1..365 (30) | nothing younger than 1 day |
| `audit` | audit records, **only** as far as the signed export verifies | `AUDIT_RETENTION_DAYS` 90..2555 (365) | nothing younger than 90 days |
| `erasure_ledger` | ledger entries | `BACKUP_RETENTION_DAYS` (30) + 30 days | nothing younger than 30 days |
| `orphan_objects` | objects no asset row references, older than the safety window | `ORPHAN_SAFETY_H` (24) | the duty; a key must be a platform key |

- The specification's defaults are used; every window is marked "product policy pending approval" in the startup log. **Offline ledger (90 days) and the P4
  report tables are P4's**: report *objects* are covered (assets of purpose `report`); a P4 table needs its own rule when it exists. `OPERATIONAL_LOG_DAYS`
  is validated and logged, but log retention is applied by the log sink (infrastructure), not by this binary.
- **Deletion goes through one function.** `app_maintenance` holds no `DELETE`; `app.retention_purge(rule, cutoff, batch, dry, ids)` is `SECURITY DEFINER`,
  owned by NOLOGIN `app_retention` (no BYPASSRLS, `search_path` pinned), whose `DELETE` is confined by policies to five tables. Batches are 1..10000; a **dry
  run** counts and deletes nothing (and applies the same floors).
- **Objects before rows, one zone per rule.** The duty deletes the object first (so no row ever disappears leaving an object behind), leaves a row whose
  object could not be deleted for the next pass, skips any key that does not belong to its row's tenant, and never touches the ready zone except for
  reports. The database re-checks each id's status and age at delete time and never deletes an asset a job result points at.
- **Audit is different.** The database cannot know whether a day was exported, so the *duty* asks `auditexport.SafeBoundary` first: every day from the first
  exported day up to the boundary must have a manifest that verifies (signature, chain, files), and no audit record may predate the first export. A missing,
  broken, tampered or partial export means nothing is purged (tested for each). Every purge leaves an `audit.retention_purge` record in each affected
  tenant. Audit retention does not exist unless the export does. **This is honestly a duty-level guarantee**, not a database one.
- **Orphan sweeper:** lists both zones under `tenant/`; a prefix that returns a full listing is split by the next hex digit (bounded listings per pass);
  an object is deleted only if it is older than the safety window, no row (any status, any tenant) references its key, and it parses as a platform key.
- **Privacy reconciliation** (the S8 open item): a request that is verified, cooling off or running with no live job gets a fresh job (the persisted plan
  resumes where it stopped); after `MaxJobs` = 5 the request is failed with `PRIVACY_JOBS_EXHAUSTED` and audited. Held requests are left alone.

## 5. Cursor hardening (E9)

A fuzz target and 21 forgery shapes now guard the decoder; it found one real defect: the standard base64 decoder **skips CR/LF**, so a token had several
valid spellings ("exactly one valid spelling" was the documented property). The decoder now refuses any character outside the base64url alphabet. Every
paginated route binds its resource into the filter hash (a cross-route reuse test covers every pair). Status mapping stays 400 (E9). The audit time range
is capped at 366 days (S7); the key rotation procedure is in `docs/runbooks/retention-and-cursor-keys.md`.

## Consequences and open items

- **Found and fixed in S9 (not Redis-related):** the tenant-creation quota was a race — N parallel `POST /v1/tenants` from one user all saw "below the quota"
  (6 created against a cap of 3). `SerializeCreation` takes a transaction-scoped advisory lock per caller before the count.
- **Found and fixed in S9 (same class as the cursor defect):** the dev capability-proxy token signature was malleable: the last base64 character of a 32-byte
  signature carries padding bits, so ~7% of last-character changes decoded to the same bytes and a tampered token was accepted. The signature is now compared as
  the exact issued string. The proxy is dev-only (refused outside `ENVIRONMENT=dev`); the S4 test that should have caught it overwrote two characters with `xx`,
  which only failed when the token happened to end in `xx` (once in a full run, 1 in 4096).
- The offline ledger, P4 reports table, and any P3 retention are hooks for their owners; the platform provides the function pattern and the duty.
- `retention_purge` floors are constants in SQL: raising them is a migration, lowering them is deliberately impossible from configuration.
- The local Redis fallback share (0.5) is a starting value to be tuned with the load test (plan S10/S11), as are the breaker constants.
- Real Redis 7.2.6 (built from source in WSL, because Docker was unavailable) ran the conformance test and T25; **not** verified: the compose `redis:7-alpine` image, TLS + AUTH against Memorystore, and a failover drill (see `ADAPTER_SWAP_INVENTORY.md`).
