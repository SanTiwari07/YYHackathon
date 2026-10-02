# ADR 0004 — Fate of `schema.sql` and `mindstrix_setup.sql`

- **Status:** Accepted (Phase 0 / Sprint 1, plan task 1.6)
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Supersedes / superseded by:** none
- **Closes:** AUDIT M4 (together with ADR 0002)

## Context

Three SQL files at the repository root bootstrap the **legacy** database:

- `schema.sql` — 8 farmer-centric tables (`farmers`, `farmer_locations`, `farms`,
  `crops`, `irrigation`, `soil_info`, `consents`, `vi_reports`).
- `mindstrix_setup.sql` — the same tables plus `organizations`, `users`,
  `farmer_profiles`, `api_keys`, `api_request_logs`, `webhooks`.
- `migrate_add_password.sql` — one ad-hoc `ALTER`.

They disagree about which tables exist, and neither is versioned. The new
platform's schema (spec §17–§18: ~43 tables, tenant-scoped, RLS forced) shares
almost nothing with them: identity is memberships in tenants rather than phone
OTP farmers, and every row carries `tenant_id`.

(**Update 2026-09-24:** the files now live in `scripts/db/legacy/`. The original note follows.)

(The plan places these files under `scripts/db/`. In this checkout they are
still at the repository root; the "pre-Sprint-1 cleanup" described in the plan
has not been applied. See the implementation log. The decision below does not
depend on the location.)

## Decision

1. The legacy scripts are **superseded, not reconciled.** The new schema lives
   entirely in `migrations/`, applied by goose (ADR 0002) to an empty database.
2. Until legacy removal (Phase 4 / Sprint 10, plan task 1.24) the three files are
   **frozen documentation** of the old schema: they are not edited, and the
   legacy server keeps working against a database created from them.
3. They are deleted together with `internal/httpapi`, `internal/repo`,
   `internal/service` and `cmd/server`, only after P3's legacy-data migration
   (`tools/migrate-legacy`, two rehearsals on a copy) and P6's regression are
   signed off.
4. The legacy → new table map (P3's Sprint 1 deliverable) feeds the data
   migration script, not the schema: the new tables are designed from the
   specification, not derived from the old ones.

## Consequences

- No attempt is made to make `schema.sql` and `mindstrix_setup.sql` agree.
- Developers of the new stack never point `cmd/api` at a legacy database; the
  local stack (`docker compose`) creates a separate database.
