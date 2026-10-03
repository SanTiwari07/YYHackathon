# ADR 0011 — Job dedupe uniqueness and manual retry (closes open item A7)

- **Status:** Accepted (E1, approved 2026-09-20)
- **Owner:** P1 (platform)
- **Spec:** 6182 §06.3 ("Async job dedupe additionally uses normalized field/boundary/date/index/profile/input hash. It survives HTTP idempotency expiry. Authorized `force=true` adds the original Idempotency-Key to the semantic identity"), §03 "Jobs" ("Failed jobs are immutable; manual retry creates a linked job"), §07.2 ("SQL uniqueness enforces … semantic job key").

## Decision

1. `dedupe_key` is unique per `(tenant_id, kind)` **among jobs whose status is not `failed` or `cancelled`**. Enforced by a partial unique index (migration 00013), not by application code.
   - A queued, running, waiting, retrying or cancel-requested job blocks an identical request: the second request is answered with the existing job.
   - A `succeeded` or `partial` job blocks an identical request too: recomputing an identical result is what `force=true` is for.
   - A `failed` or `cancelled` job never blocks: it is immutable, and the request that would retry it creates a **new** job.
2. **Manual retry** creates a new job whose `input_snapshot` carries the id of the failed job it retries (`retry_of`). No new column: the spec's `jobs` table has none, and `input_snapshot` is the immutable command record.
3. `force=true` folds the caller's original `Idempotency-Key` into the semantic identity, so an intentional recomputation gets a different `dedupe_key`; retries of that same request with the same key stay deduplicated.
4. `dedupe_key` is server-derived (`internal/platform/jobs.DedupeKey`): SHA-256 over a length-prefixed canonical tuple, hex-encoded (64 characters, within the 1..128 check). Callers never supply it.

## Consequences

- Admission code inserts the job and treats a unique violation on `jobs_dedupe_active` as "return the existing job" (`jobs.ErrDuplicate` carries its id).
- A job that later fails releases its key automatically, because the index excludes `failed`.
- A terminal `succeeded` job keeps its key until its row is removed by retention; retention of `jobs` is out of scope for S4.
