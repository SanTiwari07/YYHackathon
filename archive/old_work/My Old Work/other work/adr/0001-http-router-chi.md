# ADR 0001 — HTTP router for the new platform: chi

- **Status:** Accepted (Phase 0 / Sprint 1, plan task 1.2)
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Supersedes / superseded by:** none
- **Spec:** 6182 §06.1 ("Choose one HTTP router and one migration tool at bootstrap; do not mix frameworks per module")

## Context

The new platform (`cmd/api`, later `cmd/worker` and `cmd/tile`) needs one HTTP
router for a tenant-scoped, versioned API of roughly 80 operations under
`/v1/tenants/{tenant_id}/…`. The legacy server uses Gin and stays that way until
Phase 4; nothing in this ADR changes it.

Requirements that drive the choice:

- Cross-cutting behaviour (problem+json, request ID, body cap, ETag / If-Match,
  idempotency, cursors) must live in `internal/platform/http` as plain
  middleware so that other binaries can reuse it without a framework.
- Handlers must be ordinary `http.Handler`s so the platform packages stay
  testable with `httptest` and independent of a framework context type.
- Path parameters (`{tenant_id}`, `{id}`) and route groups per resource.

## Options considered

| Option | For | Against |
|---|---|---|
| Gin (already in the repo) | Team familiarity | Framework-shaped handlers (`*gin.Context`) leak into platform code; harder to share middleware with non-HTTP-framework binaries |
| **chi v5** | `net/http`-native, zero third-party dependencies, route groups and sub-routers, `chi.URLParam` | One more (small) dependency |
| stdlib `http.ServeMux` (Go 1.22 patterns) | No dependency | No route groups or per-group middleware; the platform would re-implement them |

## Decision

Use **`github.com/go-chi/chi/v5`** (pinned at v5.3.2 in `go.mod`, checksums in
`go.sum`) for `cmd/api`. Handlers and middleware are standard
`func(http.Handler) http.Handler` / `http.HandlerFunc`.

## Consequences

- `internal/platform/http` exposes plain `net/http` middleware; chi is used only
  where routes are assembled (`cmd/api`).
- Two routers coexist in the repository until Phase 4 (Gin in legacy, chi in the
  new stack). `internal/archtest` forbids either stack importing the other.
- No OpenAPI-driven server generation is adopted here; the contract is checked
  by a Go test and `redocly lint` (see `contracts/`).
