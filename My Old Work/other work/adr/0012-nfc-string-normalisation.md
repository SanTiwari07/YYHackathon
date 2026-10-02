# ADR 0012 — NFC string normalisation: promote `golang.org/x/text` to a direct dependency

- **Status:** Accepted (P1, 2026-09-20). AGENTS.md rule 6: "No new third-party dependency without an ADR."
- **Owner:** P1 (platform)
- **Spec:** 6182 §06.2 — "Strings normalized UTF-8 NFC and trimmed except tokens/cursors."

## Context

Every API string the specification defines must be stored NFC-normalised and trimmed. Without it, a name typed on
two devices (a precomposed and a decomposed accent) is two different strings: uniqueness constraints such as "active
field names within a farm" and idempotent request hashing would treat visually identical input as different. The Go
standard library has no normalisation; `golang.org/x/text/unicode/norm` is the maintained implementation and is
already in `go.mod` (indirectly, through the Google and Firebase clients) at `v0.41.0`.

## Decision

Depend directly on `golang.org/x/text` for the single package `unicode/norm`, wrapped once in
`internal/platform/text` (`Clean`). Domain code calls `text.Clean`, never `norm` itself, so the choice is replaceable in
one place.

## Consequences

- `go.mod` moves the module from `// indirect` to a direct requirement; the version and checksum do not change, so
  the supply-chain surface is unchanged.
- `Clean` applies to values, never to tokens (`Idempotency-Key`, cursors, ETags, `If-Match`), which the specification
  excludes.
- Invalid UTF-8 is rejected by the caller before `Clean`: `Clean` reports it instead of repairing it.
