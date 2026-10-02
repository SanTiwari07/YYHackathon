# ADR 0002 — Database migrations: goose

- **Status:** Accepted (Phase 0 / Sprint 1, plan task 1.2). One point needs human confirmation — see "Open point".
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Supersedes / superseded by:** none
- **Closes:** AUDIT M4 ("no migration tooling")
- **Spec:** 6182 §06.1, §07.7

## Context

The legacy schema is one full dump plus one ad-hoc `ALTER` (`schema.sql`,
`migrate_add_password.sql`), unversioned and unordered (AUDIT M4). The new
platform has 43 tenant-scoped tables (spec §17–§18), row-level-security
policies, grants and indexes. Spec §07.7 requires that migrations are
versioned, tested from an empty database and from a previous snapshot, that RLS
policies, grants and indexes are part of schema review and are never
hand-created in production, and that migration credentials are separate from
the runtime role.

## Options considered

| Option | For | Against |
|---|---|---|
| Hand-rolled runner | No dependency | Re-implements ordering, locking and checksums; AUDIT M4 says adopting a runner "is a project, not a patch" |
| Atlas | Declarative diffing | Different mental model; heavier; licensing/edition questions |
| **goose** | Plain SQL and Go migrations, sequential versions, `up`/`down`, embeddable | Down migrations are easy to misuse in production |

## Decision

Use **goose v3.28.0**, pinned as a `tool` in a separate module,
`build/tools/go.mod`, so the root `go.mod` (and the tidy check in CI) does not
inherit goose's driver dependency tree. Invoke through `make` targets that run
`go tool` from `build/tools`.

Conventions:

- Files in `migrations/`, sequential names `00001_<snake_case>.sql`, one logical
  change per file.
- Migrations run with a privileged owner credential that is never available to
  API or worker instances. The runtime role is created by a migration and has
  no `BYPASSRLS` (plan task 1.8).
- RLS `ENABLE` **and** `FORCE`, policies, grants and indexes live in migrations.

## Open point — forward-only vs. up/down

The specification says migrations are **forward-only** (§07.7: "Migrations are
forward-only, versioned and tested from empty and previous production
snapshots"; destructive changes follow expand/migrate/contract). The plan
(task 1.7) requires **up/down** from an empty database in CI.

Proposed reconciliation, pending approval: every migration carries both `Up` and
`Down`; `Down` exists so CI and developers can prove a migration reverses
cleanly on an empty database, and **is never run against a staging or
production database**. Production rollout is forward-only.

## Consequences

- `make migrate-*` targets and a CI job (owned by P6) exercise up/down from an
  empty PostGIS container.
- Adding a second migration tool later requires superseding this ADR.
