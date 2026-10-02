# ADR 0017 — The privacy job framework: requests, the persisted plan, database-enforced erasure, the ledger

- **Status:** Accepted (P1, Sprint 8). Implements task 1.22 of [the Phase 2–3 plan](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE2_3_PLAN.md). Migration **00020**.
- **Owner:** P1 (platform)
- **Spec:** 6182 §04 W24 ("Verify authority, enumerate lineage, apply hold policy, export or staged erasure, invalidate access, write minimal completion
  audit"; "Tenant deletion has 7-day cancellation window; emergency security suspension immediate. Backups expire on schedule and replay deletion ledger
  after restore; no claim of instant erasure from immutable backups"), §07.6-§07.7, §09.2, §09.3, §14 (`PrivacyRequest`, `Accepted`), §17-§18
  (`privacy_requests`, `artifact_lineage`), §16 (`TENANT_DELETE_GRACE_DAYS`).

## Decision in one paragraph

A privacy request is a row (`privacy_requests`) plus a **persisted plan** (`privacy_steps`) plus a **job** (`privacy_export` / `privacy_delete`) on the
existing job platform: one engine (`internal/domain/privacy`) executes it in bounded batches, each in its own transaction that first proves the job's
lease; the state machine and the cooling-off are enforced by **database triggers**; deletion of platform data is possible only through **one
SECURITY DEFINER function owned by a constrained role (`app_eraser`)** that runs only for a *running* request and only for a step *in its plan*; a
**minimal ledger** outlives the tenant and is **replayed after a restore**.

## 1. Authority (checked before anything is written)

| Request | Who | Why |
|---|---|---|
| `subject_export`, `subject_delete` | the subject, and only the subject (`subject_id` = the caller) — for **every** role, owner included | spec: "tenant owner cannot arbitrarily impersonate another subject"; §09.2 "subject request only" |
| `tenant_export`, `tenant_delete` | the organization **owner** only | §09.2 "Tenant erasure: Owner only". Applying the same rule to `tenant_export` is our reading (the matrix is silent on it) — the conservative one |

A legitimate *representation* flow (a guardian, an authorised delegate) is not in the specification and is not built; until it is, an owner cannot
act for another person. `reason` (1-1000 characters, 1000 multi-byte characters accepted) is validated and **never stored or logged** (audit gets the
code `reason_provided`): the same open item as B10, and the specification asks for "no unnecessary personal data". Recent-authentication and MFA for
privacy operations (§09.3) need an `auth_time` claim and a re-authentication flow the identity layer does not have: **not built, recorded as a gap**.

## 2. The request lifecycle

`requested -> verified -> cooling_off | running -> completed`, plus `held`, `cancelled`, `failed`. Creation verifies authority and inserts the request as
`verified` (or `cooling_off` for `tenant_delete`, `not_before = now + TENANT_DELETE_GRACE_DAYS`, default 7, 1-30), inserts the plan, admits the job, writes
`privacy.request` audit and a `privacy.requested` outbox event: **all in the request's transaction**, so a job exists iff the request committed. The API
answers `202 Accepted` with the job (`job_id`, `status: queued`, `poll_after_seconds: 5`).

- **Cooling-off is a scheduled retry**, not a poll: the handler answers `RetryAfter(not_before, PRIVACY_COOLING_OFF)`; the job sits in `retry_wait`, visible
  with its `next_attempt_at`, and the reaper requeues it when due. **Access stays open during the window** (the owner may still work); it closes the moment
  the request becomes due.
- **Cancellation** is the job cancel endpoint: cancelling the job of a request that has not started cancels the request (same transaction); a **running**
  request answers `409 CONFLICT` (`ErrIrreversible`): erasure that has begun is never half-undone. Limitation: the matrix gives `job:cancel` to neither
  `viewer` nor `billing`, so those roles cannot cancel their own pending request; owner and admin can.
- **Duplicates:** a partial unique index allows one *active* request per (tenant, kind, subject): a second is `409 CONFLICT`, a cancelled, failed or
  completed one does not block the next.
- **Holds** are an operator procedure (`Service.PlaceHold` / `Release`) with a bounded policy reference (`^[A-Za-z0-9._:-]{1,100}$`, no prose, enforced by a
  CHECK). A held request executes nothing, at the start or between any two batches; its job ends `failed` with `PRIVACY_HELD`, and **`Release` creates a new
  job** that resumes from the persisted progress (a request that had started returns to `running`, not to another wait).
- **Invalidate access when due:** starting a `subject_delete` suspends and strips the subject's memberships; starting a `tenant_delete` sets the tenant
  `deleting`, closed to everyone by ADR 0015 — in the same transaction that flips the request to `running`.

## 3. The database is the authority (migration 00020)

- **State machine + cooling-off in a trigger**: only the listed transitions; terminal requests are final; identity, kind, requester and subject are immutable;
  `not_before` can only move *later*; `running` is refused before `not_before` by the **database clock** (10 s of skew allowed). No application bug or
  injected UPDATE can skip the window.
- **Plan first**: `privacy_steps` can be inserted only while the request is `verified` or `cooling_off`; steps are immutable and progress only moves forward.
- **Deletion is not a runtime privilege.** `app_runtime` still holds no `DELETE` except on field grants (test). `app.privacy_erase(request, step, ids, limit)` is
  `SECURITY DEFINER`, **owned by `app_eraser`** (NOLOGIN, NOSUPERUSER, **NOBYPASSRLS**): `DELETE`/`SELECT` only on the platform tables it erases, plus two
  narrow anonymising `UPDATE`s, each behind a policy limited to the *current tenant*. The function refuses unless the request is `running` and the step is an
  open step of its persisted plan (`42501`), is delete-where (idempotent) and bounded (`limit` <= 10000). It is not a superuser function.
- **Ledger** (`erasure_ledger`): request id, kind, subject id, completion time, step counts — no personal data; **no FK to `tenants`** (it outlives the
  tenant's rows); insert-only for the runtime; readable across tenants (read-only) by maintenance for the replay. Retention of ledger rows (until every
  backup that could resurrect the data has expired) is an S9 duty.
- **Lineage** (`artifact_lineage`, spec s18): typed, versioned, immutable edges; `Lineage.Descendants` traverses them (cycle-safe, one entry per artifact, a graph
  beyond `MaxNodes` is `ErrLineageTooLarge` — erasure refuses to guess rather than leave derived data behind). Erasers receive `Scope.Lineage`.

## 4. Execution: one engine, batches, fences, resumability

`Engine.Run` (handler for both job kinds): wait out the cooling-off; **start** (lock, re-check, revoke access, `running`, audit); for each open step run bounded
batches, each `Runner.Tx` = a tenant transaction that begins with **`Manager.Heartbeat`** (a stale fence or an expired lease aborts the batch: a fenced-out worker
commits nothing), locks the request, honours a hold, calls the eraser, and records progress; **complete** in one transaction: scrub the tenant tombstone,
write the ledger entry, the `privacy.complete` audit, the terminal status, **and publish the job's outcome**. Every batch is delete-where, so a kill at *any* point
resumes without double deletion or omission (tested by crashing after every possible number of committed transactions). Failures are explicit: an unknown
step fails the request (`PRIVACY_STEP_UNKNOWN`, a plan is never silently shortened), a step that makes no progress fails it (`PRIVACY_NO_PROGRESS`), a transient
error is returned for the runtime to retry and the request stays `running`.

## 5. What is erased, and what deliberately is not

Domains register an `Eraser`/`Exporter` per step (the contract of an eraser — scoped, resumable, orphan-safe, no side channels — is on the interface). The
platform's own:

- **Subject**: idempotency records (rows removed), the subject's jobs (`requested_by` anonymised to a tombstone id: the work record stays, the person does not),
  membership + revision + grants (removed).
- **Tenant**: assets (**objects first**, both zones, then rows; a key outside the tenant's own prefix stops the step — an asset row can never make erasure delete
  another tenant's object), jobs and job executions (all but the job running this request), outbox and inbox, idempotency records, team (grants, revisions,
  memberships, invitations), lineage, then the tenant row is scrubbed to a **tombstone** (`[erased organization]`, status `deleting`, no support access).
- **Audit records are NOT erased** by a privacy request: they are append-only (no role can UPDATE or DELETE them), they identify a person only by a pseudonymous
  internal id and changed-field *names*, and they live under the audit retention policy (`AUDIT_RETENTION_DAYS`, after the signed export, S9). The tenant row stays
  because audit records and the ledger reference it. This is a product/legal position, recorded here; it is **not** a claim of instant or total erasure.

## 6. Export and the ledger replay

Exporters write parts through an `ExportSink` port (directory or memory now) with a per-step manifest of hashes and counts; a subject export contains only that
person's records (memberships, jobs, own audit actions), a tenant export the organization's; **no address, lookup, sealed value or object key is exported**
(tested). **Not built:** an asset-backed sink, so the requester can download the export through the existing signed-download path — it needs a server-side create
on the `Bucket` port, which today refuses to write the ready zone except through validated promotion (T17); `manifest_asset_id` stays null. Recorded as a gap.

`Engine.ReplayLedger` (T27 scaffolding): after a restore, every ledger entry is re-applied as a *fresh, system-made, due-now* request through the same engine
(every registered eraser runs, no new ledger entry), before traffic opens; an entry for a tenant that is not in this database is skipped.

## Consequences and open items

- Two deviations to record: `privacy_steps` and `erasure_ledger` are tables the specification does not list (the plan and the ledger it requires; approved in plan
  S8); `privacy_requests` and `artifact_lineage` are column-for-column the specification's.
- A request whose job the **reaper** fails (deadline) leaves the request non-terminal: a reconciliation duty joins the retention duties in S9 (maintenance already
  has the read-only discovery policy on `privacy_requests`).
- Not built (need decisions, not code): representation of another subject; recent-authentication/MFA gate; the asset-backed export delivery.
