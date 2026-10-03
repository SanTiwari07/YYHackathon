# ADR 0016 — Audit access, the signed daily export, and support access as an operator procedure

- **Status:** Accepted (P1, Sprint 7). Plan decisions **E2** (maintenance identity) and **E7** (what "admin endpoints" means).
- **Owner:** P1 (platform)
- **Spec:** 6182 §09.2 (permission matrix, "Audit access"), §09.6 (audit, privacy and incident access), §07.3 and §07.4 (append-only, indexes), §14/§15
  (`AuditRecord`, `AuditRecordList`, `GET /audit`, `GET /audit/{id}`).

## 1. Audit access is two gates

`audit:read` is the role matrix (viewer: no; every other role: yes or "own actions"). The second gate is **visibility**, applied by the handler:

| Role | `GET /audit`, `GET /audit/{id}` |
|---|---|
| owner, admin | every record of the tenant |
| manager, agronomist, scout, farmer, billing | only records where `actor_id` is the caller ("own actions"; for billing, "billing actions" is read as the same rule) |
| viewer | 403 |

Someone else's record answers **404**, the same as a record that does not exist. The cursor is bound to the tenant, the actor, the caller's
`auth_revision`, and a filter hash that includes **the visibility and the time range**, so a cursor cannot be moved to another range or to a wider
audience. `from` is inclusive, `to` exclusive, both or neither, at most 366 days, filtered on `occurred_at`; the page order is
`(created_at DESC, id DESC)` on the existing page index and a snapshot upper bound keeps later pages stable. Reading audit is not itself audited
(the specification does not ask for it); nothing in a read writes.

The response carries the stored fields only: changed-field **names**, a non-sensitive `reason_code`, no payloads, values, addresses or lookups.

## 2. The daily export: cross-tenant read, tamper evidence, create-only sink

The export (`internal/platform/auditexport`, run by `cmd/maintenance` every five minutes) writes each closed, settled UTC day to a restricted sink.

- **Read path.** Migration 00019 gives `app_maintenance` a **read-only** cross-tenant policy on `audit_records` (the same discovery pattern as outbox, jobs,
  job_execution and assets): no BYPASSRLS, no new role, no write. The table stays append-only for every role (tested: UPDATE, DELETE and TRUNCATE are
  42501 for the maintenance identity too, and an INSERT for another tenant is refused by the append policy). An index `(created_at, tenant_id, id)`
  serves the one-day query; the justification is a test that reads its plan (spec §07.4).
- **Objects.** `audit/<day>/<tenant>.ndjson` (one file per tenant and day, records in `(created_at, id)` order, the API's fields) and
  `audit/manifests/<day>.json`. Serialisation is deterministic, so re-running a day gives the same bytes.
- **Manifest.** Per tenant file: object name, record count, SHA-256; the day's total; the **SHA-256 of the previous day's manifest**; the id of the
  signing key; and an **HMAC-SHA-256** signature over the manifest. Empty days get a manifest too, so the chain has no holes. A manifest is written
  **after** all of its day's files, so a manifest means "this day is complete".
- **What it proves.** Alteration or removal of a file, addition of a file to a closed day, editing or re-signing a manifest, removal of a day and
  cutting off old history are all detected by `Verify` (each has a test). It does **not** stop someone who holds the sink and the signing key from
  rewriting history: this is tamper *evidence*, as §09.6 says ("do not call ordinary rows tamper-proof"). Phase 5 puts the sink in a bucket with a
  retention lock and the key in KMS.
- **Sink port is create-only:** `Get`, `PutOnce`, `List`. No overwrite, no delete: an exporter bug cannot rewrite history. A repeated `PutOnce` with the
  same bytes is accepted (resuming a run that died between files and manifest); with **different** bytes it is a hard error, and nothing is overwritten.
  The local adapter writes to a temporary file and hard-links it into place (atomic and exclusive; 12 concurrent writers create exactly one object).
- **Settle window.** A day is exported only `AUDIT_EXPORT_SETTLE_S` (default 600 s, 60-3600) after midnight UTC, far above the request timeout, so a request
  that started before midnight can still commit. A row that appears in an already exported day anyway is not merged silently (see above).
- **Keys.** `AUDIT_MANIFEST_KEYS` / `AUDIT_MANIFEST_ACTIVE_KEY_ID` (32+ bytes, versioned, rotate by adding a key and switching the active id; every
  retained key verifies). They must differ from the invitee and cursor keys (checked at startup). Local development uses a directory (a `tmpfs` in
  compose: the export is deterministic, an empty sink is rebuilt from the database).
- **Scaling limit, recorded.** One run loads one day's records into memory. Right for the pilot's volumes; a streaming read is a Phase 5 change (the
  `Source` port already returns per-day results, so the change is inside the adapter).

## 3. Support access is an operator procedure, designed and audited, not exposed

Plan E7 and §09.6: "No hidden permanent support role in tenant APIs". `internal/domain/support` implements the procedure and no `/v1` route exists for it
(a test fails if a route, operation, permission or role names support or break-glass, or the contract exposes such a path).

| Requirement (§09.6) | Enforcement |
|---|---|
| customer-scoped ticket | `ABC-123`-shaped reference; it is the reason of record, stored in the audit `reason_code` |
| named operator | a user id; the grant is bound to that person (someone holding the token is refused) |
| specific fields / actions | 1-10 action codes and at most 100 field ids; nothing implicit, no wildcard |
| approval | approver != operator (two-person rule) |
| expiry <= 1 hour | checked at issue and at every use, for break-glass too |
| complete audit | issue, every use, and every refusal (including refused issue and denied use) are audit records **in the customer's tenant**; if the audit record cannot be written the use fails (no audit, no access) |
| alerts on use | ordinary grants raise a `notice`; break-glass **pages** on issue and on every use, allowed or denied; alerts carry ids and codes only |
| no standing access | a grant is an HMAC-signed, self-expiring token, not a database role or a membership; the tenant must have opted in (`support_access_enabled`) and be `active` |
| emergency break-glass | same token without an approver; flagged in the audit action name (`support.break_glass*`) and paged; the after-action review is a procedure step (runbook) |

Not built, on purpose: the operator tooling and a durable grant register. A signed token can be presented until it expires and cannot be revoked
early (the audit trail shows every use); with a ceiling of one hour this is the accepted trade-off. Early revocation would need a table, which is a
spec change.

## 4. What did not change

`PATCH /tenants/{id}`, `GET/…/jobs`, `POST …/jobs/{id}/cancel`, the membership and invitation views: the "admin endpoints" of E7 already existed after
S4/S5 and are covered by the role matrix and the IDOR matrix. There is no new `/v1` operation in S7 other than the two audit reads, and no contract change.
