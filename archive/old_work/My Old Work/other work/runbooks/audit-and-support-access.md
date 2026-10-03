# Runbook: audit export, verification, and support access

Owner: P1 / security. Design: ADR 0016. Everything here runs as the **maintenance identity** (`app_maintenance`, no BYPASSRLS); nothing on this page is
available through the tenant API.

## 1. Daily audit export

`cmd/maintenance` runs the `audit-export` duty every five minutes when `AUDIT_EXPORT_DIR` is set. It exports every closed, settled UTC day that has no
manifest, oldest first (at most 31 days per run), and logs `audit export days=… files=… records=…`.

| Situation | What you see | Action |
|---|---|---|
| Normal | one manifest per day under `audit/manifests/` | none |
| The duty logs `… already exists with different content: refusing to overwrite` | an exported day no longer matches the database | **Security incident.** Do not delete or edit sink objects. Either a record was committed to an already-closed day (check the settle window and clock skew) or the table or the sink was altered. Preserve both, run `Verify`, escalate. |
| The duty logs `the previous day's manifest is missing` | a manifest was removed | Treat as tampering until proven otherwise; restore the object from the bucket's versions/backup, then run `Verify`. |
| No sink configured | startup warning `audit export not configured` | Set `AUDIT_EXPORT_DIR` and the manifest keys. Records are still written to the database. |
| After an outage | the next runs catch up, 31 days per run | none |

**Verify a range** (until the operator CLI exists, from a Go test or a small program): `auditexport.Verify(ctx, sink, keys, from, to)` returns the first
inconsistency: missing manifest, bad signature, key not retained, broken chain, altered or missing file, unlisted file. Run it after every restore, key
rotation and sink migration, and periodically (daily is cheap).

**Rotate the signing key:** add the new key to `AUDIT_MANIFEST_KEYS`, set `AUDIT_MANIFEST_ACTIVE_KEY_ID` to it, restart maintenance. Keep every old
key for as long as any manifest signed by it must verify (at least the audit retention, 365 days by default). Dropping a key makes `Verify` say
`not retained` for the days it signed.

## 2. Support access (approved) and break-glass (emergency)

Preconditions: the customer's organization has `support_access_enabled = true` and is active; a customer-scoped ticket exists (`ABC-123`).

**Ordinary support access**
1. The operator files a request: tenant, **named** operator, ticket, the 1-10 action codes and (optionally) field ids needed, duration <= 1 hour.
2. A **different** person approves (two-person rule). The tool calls `support.Service.Issue`. The customer's audit trail now shows `support.grant`
   (outcome `succeeded`, or `denied` with the refusal) with the ticket as the reason.
3. Every action is preceded by `support.Service.Use(operator, token, action, field)`; the action proceeds only if it returns nil. Each use, allowed or
   denied, is in the customer's audit trail and raises a notice.
4. The grant expires by itself. There is no early revoke; keep the duration as short as the work.

**Emergency break-glass** (security-controlled): no approver. Same tool, `BreakGlass: true`. It **pages** on issue and on every use.
After-action review is mandatory within one business day: the security lead reads the customer's `support.break_glass*` audit records, confirms the
ticket and the scope were justified, and records the outcome on the ticket. The customer can read the same records through `GET /v1/tenants/{id}/audit`
(owner/admin).

**Never**: create a database role or a membership for support; widen `app_maintenance`; reuse a grant token for another person or action; store a
token in a ticket. If the audit trail cannot be written, stop: no audit record, no access.
