# Platform status (P1)

**Last updated:** 2026-09-24 · **Owner:** P1 (tech lead / platform backend) · **Contract:** `1.0.0-rc2`

Where P1's share of the P0 plan (`docs/references/TEAM_WORK_DIVISION.md`, tasks 1.1–1.26) stands,
what is still open, and where the reasoning lives. Design decisions are in [`docs/adr/`](../adr/);
this page does not repeat them.

## Plan tasks

| Task | What | Status | Record |
|---|---|---|---|
| 1.1–1.4 | Layout (`cmd/{api,worker,tile,maintenance}`, `internal/{platform,domain,adapters,apiv1}`), chi/goose/sqlc, local stack, `AGENTS.md` | Done | ADR 0001–0003, 0006, [LOCAL_STACK.md](LOCAL_STACK.md) |
| 1.5, 1.12 | OpenAPI contract (82 P0 operations), frozen | Done — `1.0.0-rc2` | [CONTRACT_CHANGES.md](CONTRACT_CHANGES.md), `contracts/openapi.lock` |
| 1.6 | Fate of the legacy SQL scripts | Done — frozen in `scripts/db/legacy/` until 1.24 | ADR 0004 |
| 1.7–1.8 | Migrations with RLS `ENABLE`+`FORCE`, runtime role without `BYPASSRLS` | Done — T01 | ADR 0002, `migrations/` |
| 1.9 | Token verifier, principal resolution | Done — T02 | `internal/platform/auth` |
| 1.10–1.11 | Tenant transaction helper; problem+json, request id, body cap | Done | ADR 0007 |
| 1.13–1.15 | Idempotency, ETag/If-Match, HMAC-signed cursors | Done — T03, T04 | `internal/platform/{idempotency,http,pagination}` |
| 1.16–1.17 | Audit + outbox in one transaction; jobs with leases and fence tokens | Done — T06 | ADR 0011 |
| 1.18–1.19 | Queue dispatcher + reaper; object store with quarantine/ready | Done — T07, T17 groundwork | ADR 0008, 0009, 0010 |
| 1.20 | Memberships, invitations, field grants API | Done — W02, W03 | ADR 0013, 0014 |
| 1.21 | Security review of S1–S5 | Done — findings below | ADR 0015 |
| — | Audit read API, signed audit export, support access (S7) | Done | ADR 0016 |
| 1.22 | Privacy job framework | Done — domain erasers are P2/P3/P4's to register | ADR 0017 |
| 1.23 | Retention jobs, cursor hardening, Redis adapter | Done — T25 (P1 part), verified 2026-09-24 | ADR 0018 |
| 1.24 | Remove legacy routes, `internal/httpapi`, `cmd/server` | **Blocked** — `apps/web` does not exist yet, so `frontend/` is still the only UI | ADR 0004 |
| 1.25 | Swap adapters to Cloud SQL / Tasks / Pub/Sub / GCS / Identity Platform | Not started — Phase 5 ("cloud last") | [ADAPTER_SWAP_INVENTORY.md](ADAPTER_SWAP_INVENTORY.md) |
| 1.26 | Production readiness review | Not started — Phase 5 | — |

## Verification

- **CI** (`.github/workflows/ci.yml`) is the authoritative gate: `go vet`, staticcheck, `go test -race`
  against PostGIS 16 and the Firebase Auth emulator, `make migrate-verify`, sqlc drift, Redocly,
  govulncheck, frontend build, Docker image. Green on `main`.
- **Locally**, run the same suite with every dependency required; see
  [LOCAL_STACK.md](LOCAL_STACK.md#db-backed-tests-without-docker). The race detector cannot run on
  the Windows development machine; CI covers it.

## Open items

Security findings (S6 review):

| Id | Finding | State |
|---|---|---|
| S6-04 | `POST /uploads` and `POST /assets/{id}/download` persist a bearer URL in the idempotency record; a replay after expiry returns an expired URL | Open — decision CR-03, **needed before S11** |
| S6-05 | `audit_reason` is validated but has no column, so it is not stored (applies to fields, seasons reopen, crop cycles fail) | Open — decision CR-02 |
| S6-06 | The inviter is not re-checked at acceptance (no inviter column in the spec) | Open — spec gap (CR-05) |
| S6-07 | Field grants must name a real field | **Partly closed**: `postgres.FieldExistence` validates every grant (tenant-scoped, archive-aware). The database FK `membership_field_grants.field_id → fields` is not added yet: fixtures in `internal/platform/{auth,db,worker}`, `internal/domain/privacy` and `internal/apiv1/assets_test.go` insert grants with fabricated field ids and must seed real fields first |

Contract and product decisions (details in [CONTRACT_CHANGES.md](CONTRACT_CHANGES.md)):
CR-02 / CR-07 (free-text audit and privacy reasons are accepted but not stored), CR-03 (signed-URL
replay), CR-04 (home-region allowlist), CR-05 (inviter on `Invitation`), CR-08 (viewer and billing
members cannot cancel their own privacy request).

Other follow-ups:

- **Dependabot and Go 1.26.** Decision E11 called for ignore rules while Go is pinned to 1.25; they
  were never added. Bumps that require Go 1.26 (`golang.org/x/text` 0.42, `validator` 10.30.5)
  arrive as failing PRs and are closed by hand until the toolchain moves.
- **Directory service (D10):** multi-cell routing stays out of P0; `/v1/me` answers for the local cell.
- **Race coverage** of the DB-backed packages comes from CI only (see Verification).
- **Boundary import manifest (P3, tasks 3.10-3.12).** Spec s03 makes the row manifest a private JSON asset
  linked from the job result, but `storage.Bucket` has no server-side write, so row outcomes live in
  `app.import_row_results` (migration 00037) for both dry runs and commits, and no endpoint reads them yet
  (the contract has none). Decisions for P1: a Bucket write port for generated assets (the column
  `job_execution.result_manifest_asset_id` already exists), the manifest read route, and paging beyond
  10,000 rows (imports above that are refused with `IMPORT_TOO_MANY_FEATURES`).
- **Import authorization admission check (B3, P3).** `field:write` is "granted farm scope" for a
  farmer (s09.2) but there are no farm grants; an import is allowed only for a farmer whose grant covers
  every field. Authorization is checked once at job admission before the first row commits; if a farmer's
  grant or membership is revoked mid-import, rows already queued continue to commit, with revocation taking
  effect on the next import request. **Status: accepted risk for P0** (mid-job re-authorization deferred to Phase 5).
- **Import crop metadata dropped on commit (B4, P3).** Crop metadata columns (`crop_code`, sowing/harvest
  dates, `yield_t_ha`) are validated in dry-run but not persisted by the boundary commit because a crop
  cycle requires an active season that imports do not create. The row is marked created with no warning
  that crop data was dropped. **Status: scheduled for fix in Task 3.13+** (surface a warning/reason code on
  `app.import_row_results.code`; deferred from 3.12).
- **Concurrent geometry dedup across write paths (B1, P3).** `ImportStore.FieldByGeometryHash` as well as
  `FieldStore.InsertField` and `FieldStore.UpdateField` acquire a transaction-scoped advisory lock on
  `(farm_id, geometry_hash)` to serialize concurrent imports and direct field writes on the same farm,
  guaranteeing racing operations cannot create duplicate fields and returning clean typed errors
  (`duplicate_geometry` row code in imports, `fields.ErrDuplicateGeometry` in domain writes).
- **Farm archive does not cascade (B5, P3).** `PATCH /farms/{id}` with `archived: true` changes only the farm:
  its fields stay active and keep `monitoring_enabled`, so an archived farm can still hold monitored fields
  and appear to have live work under it. **Status: accepted risk for P0** (revisit if pilot data shows this
  causing real confusion).
- **Legacy onboarding data not carried to /v1 (B6, P3, task 3.15).** The legacy flow captures data the /v1 model has
  no place for, and 3.15 deliberately leaves it behind: farmer age, gender and display-name customization; location
  (PIN code, village, address, state/district/taluka); declared farm area, land ownership and farm photo; expected
  harvest month; irrigation water source and the borewell/canal distinction; self-declared soil type. The spec's
  data model does not include them and this task does not invent schema to hold them. **Status: not planned**
  (product decision required to reconsider).
- **Legacy placeholder identities are permanent (B7, P3, task 3.16, ADR 0019).** A legacy farmer migrated without a
  confirmable identity gets a suspended membership whose `user_id` is a deterministic placeholder, also written to
  `farms.owner_user_id`, `field_boundaries.created_by` and `consents.user_id`. No mechanism anywhere in the platform
  can repoint that placeholder to the farmer's real `user_id` (it is not an updatable field on these rows), so the
  farmer can never sign in to the migrated tenant. **Status: accepted risk, permanent absent a future manual repair
  migration.**

## Historical records

Removed from the tree on 2026-09-24 and kept in git history. The ADRs cite decision ids
(A*, B*, D*, E*) and audit finding ids (M4, H7, L3, M9) from these files:

- [Implementation log (Phases 0–3, S1–S9)](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/IMPLEMENTATION_LOG.md)
- [Phase 1 migration design](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE1_MIGRATION_DESIGN.md)
- [Phase 2–3 plan (decisions E1–E11)](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE2_3_PLAN.md)
- [Codebase audit (AUDIT.md, finding ids)](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/AUDIT.md)
- [Python → Go migration plan](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/PLAN.md) and [report](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/REPORT.md)
