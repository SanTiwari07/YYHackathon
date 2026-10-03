# ADR 0006 — Where adapter interfaces (ports) live

- **Status:** Accepted, deviates from one snippet in the plan (§5) — **needs human confirmation**
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Spec:** 6182 §06.1 (`internal/adapters/…`, `internal/platform/{auth,config,http,logging,telemetry,queue}`)

## Context

The plan states two things that cannot both hold literally:

- §5 shows the interfaces (`cache.Store`, `storage.Bucket`, `queue.Dispatcher`)
  declared in packages under `internal/adapters/…`;
- §5 and §6 also state the rule "`internal/domain/**` never imports
  `internal/adapters/**`; it depends on the interface, which lives next to the
  domain package or in `internal/platform`", and the §6 layout labels
  `internal/adapters/{redis,storage,queue}` as the *implementations*.

If the interface lived inside the adapter package, domain code would have to
import an adapter package to name the type, breaking the rule the Phase 5 GCP
swap depends on.

## Decision

- **Ports** (interfaces) live in `internal/platform/<name>`: `cache`, `storage`,
  `queue`, `auth`. This also matches the specification's own layout, which lists
  `internal/platform/queue`.
- **Adapters** (implementations) live in `internal/adapters/<impl>`: `postgres`,
  `redis`, `storage`, `queue`.
- Concrete adapters are constructed only in `cmd/*/main.go` and passed to domain
  code as interfaces.
- The rule is enforced mechanically by `internal/archtest` (part of
  `go test ./internal/...`), not by review alone.

## Consequences

- The plan's snippet paths (`internal/adapters/cache`, …) are not used.
- Interfaces that would contradict the specification are deferred rather than
  declared early: `queue.Dispatcher` and `storage.Bucket` are designed in
  Sprint 4 against the real `jobs`/`job_execution` schema and the upload/
  quarantine rules; `auth.Verifier` in Sprint 2 with the membership model.
  Only `cache.Store`, which has no conflict, is declared in Phase 0.
