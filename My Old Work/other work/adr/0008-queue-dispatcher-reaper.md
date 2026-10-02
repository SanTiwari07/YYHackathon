# ADR 0008 — Queue, dispatcher, reaper and worker runtime (local shape of spec §02.5)

- **Status:** Accepted (E5, approved 2026-09-20)
- **Owner:** P1 (platform)
- **Spec:** 6182 §02.5 (async execution and failure atomicity), §03 "Jobs", §06.1, §18 `job_execution`, `outbox`, `inbox`.

## Decision

Two ports in `internal/platform/queue`, so Phase 5 maps them to Pub/Sub and Cloud Tasks without touching domain code:

| Port | Meaning | Local adapter | Phase 5 |
|---|---|---|---|
| `Publisher` | at-least-once publication of a committed `DomainEvent` | in-process fan-out to registered subscriptions (inside `cmd/maintenance`) | Pub/Sub |
| `Dispatcher` | create a **named** task that wakes a worker for one dispatch; a second create with the same name returns `ErrAlreadyExists` | HTTP push to the worker's private task endpoint | Cloud Tasks (HTTP target) |

No new table. **`job_execution.dispatch_id` is the task name**: it is written in the same transaction that admits or re-schedules the job (spec 02.5: "the dispatcher records desired task name before creation"), so a failed or lost task creation is simply retried with the same name, and `ErrAlreadyExists` is reconciled as success. A restart loses nothing because the queue is derived from `jobs` + `job_execution`.

### Components (all in the maintenance/worker binaries, none in `cmd/api`)

1. **Outbox publisher** (`cmd/maintenance`): claims pending outbox rows (`lease_until`, `attempts`), publishes to `Publisher`, sets `published_at`. Crash-safe: an unpublished row is republished; consumers are idempotent by `(consumer, event_id)` in `inbox`.
2. **Dispatch scan** (`cmd/maintenance`): finds `queued` jobs that are due and `waiting_provider` jobs whose poll is due, and calls `Dispatcher.Create` with the row's `dispatch_id`. Repeated scans are harmless: the task name is idempotent, and `Claim` rejects a stale dispatch.
3. **Reaper** (`cmd/maintenance`):
   - `running` with an expired lease → `retry_wait` (`attempt` is already counted at claim) with backoff, then `queued` with a **new** `dispatch_id` when `next_attempt_at` is due;
   - a job past `deadline_at` → `failed` with a stable code, never replayed;
   - a `waiting_provider` job past its deadline → `failed` through `running` (the spec routes outcomes through `running`);
   - a job that has a provider operation is **reconciled with the provider before any replay** (spec 02.5). S4 provides the reconciliation hook (`Reconciler`); P2 supplies the Earth Engine one. Without a reconciler the reaper does not replay a job whose `submission_state` is `submitting` or `uncertain`: it leaves it and reports it.
4. **Worker runtime** (`cmd/worker`): private HTTP task endpoint (bearer secret `WORKER_TASK_TOKEN`; in Cloud Run this becomes IAM/OIDC), bounded concurrency (`WORKER_CONCURRENCY`, spec default 4), handler registry keyed by `jobs.Kind`, `Claim` → heartbeat loop → `Publish` with fence, graceful shutdown that stops accepting tasks and lets leases expire. A saturated worker answers 429/503 so the dispatcher retries later; it never queues unbounded work in memory.

### Resuming from `waiting_provider` (spec defect fixed in S4)

The spec's own chain is `queued → running → waiting_provider → running → succeeded|partial|failed`, so the edge `waiting_provider → running` is required. Decisions the spec leaves open, chosen conservatively:

- Entering `waiting_provider` **releases the lease**: the wait is the persisted provider operation, not a held worker (spec: "not an in-memory wait").
- A later **polling task** calls `Manager.Resume`, which acquires a lease with a new fence, moves the job to `running`, and **does not increment `attempt`** (a poll is not a retry).
- Each poll gets a **new `dispatch_id`** written by the scan in its own transaction, so poll tasks have distinct names and stale polls are rejected by the same rule as stale dispatches.
- `waiting_provider → failed` stays absent (via `running`, as the spec routes it).

## Failure model proven by tests

- **T07 (dispatch):** fault injection between "dispatch_id recorded" and "task created" → the scan retries; the job runs exactly once.
- **T07 (worker crash):** kill the worker mid-job → lease expires → reaper re-dispatches exactly once; the dead worker's late `Publish` fails with `ErrFenceLost`.
- **Duplicate/out-of-order events** never regress a resource version (T06, with P4, Sprint 6).

## Consequences

- The dispatcher is at-least-once by design; only fenced, idempotent effects are allowed downstream.
- Adding Cloud Tasks and Pub/Sub in Phase 5 means two new adapters and wiring, plus `ErrAlreadyExists` mapping from Cloud Tasks' `ALREADY_EXISTS`.
