# ADR 0003 — SQL access layer: sqlc over pgx

- **Status:** Accepted (Phase 0 / Sprint 1, plan task 1.2)
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Supersedes / superseded by:** none
- **Spec:** 6182 §06.1 ("pgx with sqlc or explicit reviewed SQL … No ORM-generated schema changes at runtime")

## Context

The legacy code base hand-writes SQL over `pgx` (`internal/repo`) and that stays
the house style: PostGIS functions, `DISTINCT ON`, `ON CONFLICT … RETURNING` and
`= ANY($1::uuid[])` must keep working. The new schema is about 43 tables instead
of 8, and hand-written scan code at that size is where bugs hide.

## Options considered

| Option | For | Against |
|---|---|---|
| Raw `pgx` everywhere | Zero tooling | Hand-written row scanning across ~43 tables |
| `sqlx` | Less scanning code | Still untyped queries |
| ORM | — | Ruled out by spec §06.1 |
| **sqlc** | SQL stays hand-written and reviewable; Go types and scan code are generated and compile-checked against the migrations | Code generation step; PostGIS types need overrides |

## Decision

Use **sqlc v1.31.1** with the `postgresql` engine and the `pgx/v5` driver,
pinned as a `tool` in `build/tools/go.mod` alongside goose. The schema input is
the `migrations/` directory; queries live next to the adapter in
`internal/adapters/postgres/queries/`. Generated code is committed and CI checks
that regeneration produces no diff.

sqlc is a build-time tool only; it is not a runtime dependency. It is run with
`CGO_ENABLED=0` (its Postgres parser is WASM-based; verified on Windows without a
64-bit C toolchain).

## Consequences

- **AGENTS.md rule 3 (no unscoped `GetByID`).** sqlc's generated `Queries` accepts
  any `DBTX`, which would include a bare pool. The `internal/adapters/postgres`
  package therefore exposes queries only through constructors that take the
  `pgx.Tx` produced by `internal/platform/db.WithTenant`; the generated
  `New(db DBTX)` stays unexported. A test in Sprint 2 proves a bare pool cannot
  reach a generated query from outside the package.
- PostGIS `geometry` columns need explicit type overrides in `sqlc.yaml`; decided
  when the first geometry table lands (P3, Sprint 2–3).
- `sqlc.yaml` and the first queries are added in Sprint 2 with the first
  migrations; Phase 0 pins the tool only.
