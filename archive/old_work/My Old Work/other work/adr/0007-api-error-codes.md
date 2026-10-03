# ADR 0007 — API error codes

- **Status:** Accepted (Phase 1 finalisation)
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Supersedes:** the "PROVISIONAL" code block introduced in Phase 1 (removed).
- **Spec:** 6182 s03 (idempotency conflicts and retry decision table), s04 W01, s06.2, s19.3

## Context

Every error response is `application/problem+json` with a required, stable `code` (contract schema
`Problem`, spec s06.2: "stable code"). The specification was searched in full for named codes.

**Fact established:** `6182.docx` names exactly seven error codes:

| Code | Status | Where |
|---|---|---|
| `IDEMPOTENCY_MISMATCH` | 409 | s03 decision table |
| `REQUEST_IN_PROGRESS` | 409 (+ `Retry-After`) | s03 decision table |
| `VERSION_CONFLICT` | 412 | s03 decision table, s19.3 |
| `PRECONDITION_REQUIRED` | 428 | s03 decision table |
| `HOME_REGION_MISMATCH` | 409 | s04 W01 |
| `INTERNAL_ERROR` | 500 | s06.2 |
| `DEPENDENCY_UNAVAILABLE` | 503 | s06.2 |

For the other error statuses the specification fixes the status but **names no code**: 400 (unknown
query parameter), 401 (missing authentication), 403 (missing permission, suspended member), 404
(wrong-tenant resource), 410 (expired map session), 422 (validation), and, by the router and the size
cap, 405 and 413, plus 429 (throttling). The OpenAPI document that the specification says it was
generated from is not part of the deliverable, so no other source names them.

## Decision

The names chosen in Phase 1 **are** the contract's values. They are not placeholders. They follow the
style of the seven specified names (upper snake case, naming the condition):

| Code | Status | Defined by |
|---|---|---|
| `BAD_REQUEST` | 400 | contract |
| `UNAUTHENTICATED` | 401 | contract |
| `FORBIDDEN` | 403 | contract |
| `NOT_FOUND` | 404 (also: a resource of another tenant) | contract |
| `METHOD_NOT_ALLOWED` | 405 (router level) | contract |
| `MAP_SESSION_EXPIRED` | 410 | contract |
| `PAYLOAD_TOO_LARGE` | 413 | contract |
| `VALIDATION_FAILED` | 422 | contract |
| `RATE_LIMITED` | 429 | contract |

`MAP_SESSION_EXPIRED` is new in this ADR: the contract already documented a 410 response for the tile
endpoint (spec W10: "Expired session →401/410") but it had no code.

The catalogue is published in the contract as the root extension `x-error-codes` (code -> status and
`defined_by`: a 6182 section, or `contract`), each component response lists the codes it can carry, and
`Problem.code` describes the catalogue.

## Enforcement

- `internal/platform/http` holds the same catalogue (`Statuses`); `New` panics on a code/status pair
  outside it, so an undocumented error cannot be produced.
- `TestErrorCatalogueMatchesTheContract` fails if Go and the contract differ in any code or status.
- `contracts/error_codes_test.go` fails if a code named by the specification is missing or not cited to
  6182, if a contract-defined code claims a specification source, if a documented response carries the
  wrong status for its codes, if a code is unreachable, or if a body-taking operation omits 413.
- The frozen-contract lock (`contracts/openapi.lock`) fails on any change without a deliberate update.

## Consequences

- Clients can switch on `code` for every error the API returns.
- Renaming or re-statusing any code, or adding one, is a contract change: P1 review and a new lock.
- If 6182 is later revised to name codes for any of the nine, the specification wins: update the
  catalogue, `specNamedCodes` in `contracts/error_codes_test.go` and this ADR together.
