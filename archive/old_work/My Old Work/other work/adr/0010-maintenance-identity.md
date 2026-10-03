# ADR 0010 — Maintenance identity and `cmd/maintenance` (closes open item A6)

- **Status:** Accepted (E2, approved 2026-09-20)
- **Owner:** P1 (platform)
- **Spec:** 6182 §02.2 ("Maintenance jobs … separate narrowly scoped identities; audited"), §06.1 (`cmd/maintenance/  Outbox, reaper, retention, projection jobs`), §07.3 ("Support admin is not a permanent database superuser"), §09.4 ("scheduled organization jobs use named service policies, not unbounded admin shortcuts").

## Problem

Three duties must find work **across tenants**: the outbox publisher, the job reaper/dispatch scan, and (Sprint 9) retention. `app_runtime` policies are all tenant-scoped, so none of them can run as the API or worker identity.

## Decision

- A new NOLOGIN group role `app_maintenance` (NOSUPERUSER, NOBYPASSRLS, owns nothing) is a **member of `app_runtime`**. Members inherit every tenant-scoped policy, so maintenance work on one tenant is done exactly like API work: a `db.Pool.WithTenant` transaction with the tenant and a system actor set.
- On top of that, `app_maintenance` alone gets **read-only cross-tenant discovery policies** on the four tables the S4 duties scan: `outbox` (pending rows), `jobs` and `job_execution` (queued, due, expired-lease and waiting rows), and `assets` (quarantined uploads awaiting validation; migration 00017). Nothing else. `idempotency_records` and `inbox` discovery is added in Sprint 9 with the retention jobs.
- Discovery returns only identifiers and timestamps; **every mutation** still runs in a tenant-scoped transaction. So a maintenance bug cannot write across tenants, and RLS still holds on every write.
- The one extra write privilege is `UPDATE (published_at, attempts, lease_until, updated_at) ON outbox` — column-limited, tenant-scoped — because the publisher must mark rows published and `app_runtime` may only insert and select outbox rows (migration 00008).
- `cmd/maintenance` is a separate binary with its own login (`DB_MAINTENANCE_USER`), pool and connection cap (spec §10.2: maintenance allowance 20). `cmd/worker` never receives the cross-tenant credential.
- Audit: every maintenance mutation that changes a job's state writes an audit record with the well-known system actor `audit.SystemActor` (`00000000-0000-4000-8000-00000000a001`, an id that is never a user) and `reason_code` naming the duty (`reaper.lease_expired`, `reaper.deadline`, …).
- The migrations create **no login** (approved decision A14). The local compose stack creates a development login for the group in `docker/postgres-init/20-runtime-role.sh`, exactly as for the runtime login; production uses IAM authentication (Phase 5).

## Alternatives rejected

- `BYPASSRLS` on the maintenance role: unbounded, and it would also hide RLS mistakes in maintenance code.
- `SECURITY DEFINER` scan functions: moves logic into SQL that is harder to review and test than three narrow policies.
- Folding the duties into `cmd/worker`: the worker would then hold the cross-tenant credential.

## Consequences

- `VerifyRuntimeRole` also runs for the maintenance login (not superuser, no BYPASSRLS, owns nothing).
- The RLS-coverage guard learns that `app_maintenance` may hold extra policies on exactly the three tables above and no others (a test enumerates them).
