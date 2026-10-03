# Contract change record (`contracts/openapi.json`)

The contract is frozen at each release candidate (AGENTS.md rule 2). A change needs P1 sign-off, a new lock (`contracts/openapi.lock`) and a
note here. Plan decision **E6**: rc1 stays frozen; change requests are collected and land as a batch (rc2 at the end of S6, rc3 candidate at the end
of S9, final at S10).

| Version | Cut | Lock (sha256 of the LF-normalised file) | Content |
|---|---|---|---|
| `1.0.0-rc1` | end of Sprint 2 | `cd94a007...d965f` | 82 operations, 95 schemas, 16 error codes. The git tag `contract-v1.0.0-rc1` was never created (Phase 1 was uncommitted at the time). |
| `1.0.0-rc2` | end of Sprint 6 | see `openapi.lock` | rc1 + **CR-01**. Tag `contract-v1.0.0-rc2`. |

## rc1 -> rc2

| # | Change | Where | Why |
|---|---|---|---|
| **CR-01** | New error code `CONFLICT` (409, `defined_by: contract`) in `x-error-codes` and in `components.responses.Conflict.x-error-codes`. The description now says "ten defined by this contract" (was nine). | root `x-error-codes`, `Conflict` response, `info.description`, `info.version` | The specification fixes **409** for a revoked, expired or already used invitation (W03) and for an invitation to an address that already has one, but names no code; the catalogue had only idempotency and region 409s. Served since S5 (ADR 0014, section 9). |

No operation, schema, property, enum, parameter or `x-permission` changed. Every operation that already documented `409` (the shared `Conflict`
response) now lists `CONFLICT` among its possible codes. A client generated from rc1 keeps working: an unknown `code` value is a string it did not
enumerate.

### How the contract was reviewed for rc2 (S6)

- **Served == contract.** `TestServedRoutesMatchTheFrozenContract` compares every served route (19 operations at S6) with the contract's method, path,
  operationId, `x-permission` and Idempotency-Key rule; `TestEveryContractPermissionIsAccountedFor` fails on a permission that is neither in the role
  matrix, pending, nor special. Response bodies of every served operation are validated against their component schema by the API tests.
- **Error catalogue.** `contracts` and `internal/platform/http` tests require the Go catalogue and `x-error-codes` to be identical (codes and statuses).
- **Status codes actually produced** by the S4/S5 handlers were compared with each operation's documented responses; none was undocumented.
- **Change requests from P2-P6:** none were filed in the repository by S6. The register below is therefore P1's own.

### Change-request register

| # | Item | Status | Decision |
|---|---|---|---|
| CR-01 | `CONFLICT` 409 code | **Landed in rc2** | above |
| CR-02 (B10) | `audit_reason` (<= 2000 characters) has no column; validated, not stored | Open | Needs a product decision (a column, or a restricted sink); **not** a contract change |
| CR-03 (B12) | `POST /uploads` and `POST /assets/{id}/download` return a bearer URL that is persisted in the idempotency record and replayed for 24 h; a replay after the URL expired returns an expired URL | Open, **rc3 candidate** | Options: mark those two operations as "re-issue on replay" (contract note, no schema change) or drop the idempotency requirement for the two read-like commands. Needs your call before S11 |
| CR-04 (B11) | `HOME_REGION` allowlist is a plain string compared with the cell's | Open | Deployment setting, not contract |
| CR-05 (B13) | `Invitation` has no inviter, so acceptance cannot re-check the inviter | Open, spec gap | Would add a property (spec change); recorded, not proposed |

## rc2 -> rc3 candidates (end of S9)

Collected during S7-S9; open items are tracked in [STATUS.md](STATUS.md).

### Status at the end of S9 (2026-09-21): **rc3 is NOT cut; the candidate list is below**

`contracts/openapi.json` is unchanged since rc2 (`1.0.0-rc2`, lock in `openapi.lock`). S7, S8 and S9 needed **no contract change**: the audit and privacy operations
were already in rc2; the S9 limiter answers `429 RATE_LIMITED` with `Retry-After`, which **all 82 operations already document** (`TooManyRequests`, checked
by script at S9); the S9 readiness change (`{"status":"degraded","degraded":["redis"]}` with 200) is on the operational `/readyz`, which is outside the
contract.

| # | Candidate | Status | Notes |
|---|---|---|---|
| CR-03 (B12) | Signed-URL operations replay a persisted bearer URL | Open, **rc3 candidate** | Unchanged from S6. Needs your decision between "re-issue on replay" (contract note) and dropping the idempotency requirement for the two read-like commands; must be decided before S11 |
| CR-02 (B10) | `audit_reason` has no column | Open, not a contract change | Needs a storage decision (sealed column or restricted sink) |
| CR-04 (B11), CR-05 (B13) | Region allowlist; inviter not on `Invitation` | Open | As recorded at S6 |
| CR-06 | `Retry-After` on `429 RATE_LIMITED` produced by the per-user limiter is documented on `TooManyRequests`; no change needed | **Closed, no change** | Recorded so nobody re-opens it |
| CR-07 | The privacy request `reason` is validated but **never stored** | Open, same root as B10 | The `PrivacyRequest` schema in the spec has no `reason` column; the contract accepts it (<= 1000 chars). Product decision: keep accepting-and-discarding, or drop it from the request body |
| CR-08 | A viewer or billing member cannot cancel their own pending privacy request (`job:cancel` excludes them) | Open, matrix question | Either add `job:cancel` on `privacy_*` jobs for the requester, or accept the limitation (documented in ADR 0017) |

Nothing else was proposed by P2-P6 in the repository (their code is absent from this branch).

## After rc2: CR-09 (task 3.15, approved)

| # | Change | Where | Why |
|---|---|---|---|
| **CR-09** | Two operations: `GET /v1/tenants/{tenant_id}/consents` (`listConsent`, `read`, `limit`/`cursor` like every list) and `POST /v1/tenants/{tenant_id}/consents` (`setConsent`, `consent:self`, Idempotency-Key; 201 on the first submission for a purpose, 200 when it updates the record). Schemas `Consent`, `ConsentSet` (closed; `purpose` enum `satellite_monitoring`, `data_sharing`; `granted` boolean; both required) and `ConsentList`. Tag `consents`. | `paths`, `components.schemas`, `tags`, `info.description`; `openapi.lock` | Farmer onboarding (3.15) replaces the legacy `/consent` step, and the spec defines no consent operation or schema (s14, s15), so this is a product decision, not a spec rule: approved as proposed in the 3.15 Part 0 report. Each member reads and sets only their own consent; withdrawing `satellite_monitoring` turns monitoring off on the fields the member may write, in the same transaction (3.14). |

Additive only: no existing operation, schema, property, enum, parameter or `x-permission` changed, so a client generated from rc2 keeps working.
The matrix row `consent:self` (Domain for every role; the handler allows only the caller's own record) is live in
`internal/platform/apikit/permissions.go`. `info.version` stays `1.0.0-rc2` and the lock was regenerated; cutting the next release candidate
(and its tag) with CR-09 is a separate P1 release step.
