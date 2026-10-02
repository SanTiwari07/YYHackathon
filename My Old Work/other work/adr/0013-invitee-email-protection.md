# ADR 0013 — Invitee e-mail: sealed at rest, matched by a keyed, tenant-bound lookup hash

- **Status:** Accepted (P1, 2026-09-20). Decision **E3** in [the Phase 2–3 plan](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE2_3_PLAN.md); closes open item **A4**; supersedes the
  "deliberately no lookup column" note of migration 00004 (Phase 1 decision D6).
- **Owner:** P1 (platform)
- **Spec:** 6182 §14 `InvitationCreate.email` ("encrypted at rest, excluded from logs"); §04 W03 ("invitee must authenticate verified matching address").

## Context

The specification asks for two things that pull against each other. The invitee's address must be unreadable in the database. But at acceptance the
caller's *verified* address (from the identity token) has to be matched to an invitation, and ciphertext cannot be searched. Options considered:

| Option | Rejected because |
|---|---|
| Store plaintext, rely on disk encryption | Contradicts "encrypted at rest": a dump or SQL injection reads every invitee. |
| Encrypt only; decrypt every pending invitation in the tenant and compare | O(n) decryptions per acceptance, key needed on the hot path for every row, and it still needs the tenant scan to be cheap. |
| Deterministic encryption as the lookup | Anyone with the key can also decrypt, the ciphertext is the lookup (no separation of duties), and equality of ciphertext across tenants reveals that one person belongs to both. |
| **Sealed value + separate keyed hash** | Chosen. |

## Decision

Two values are derived by the application from the **same normalised address**, stored side by side on `app.invitations`:

| Column | Content |
|---|---|
| `email` | The address sealed with **AES-256-GCM**: `v1.<key id>.<base64url(nonce ‖ ciphertext ‖ tag)>`. The authenticated data is `pragya/invitation-email/v1 ‖ tenant id ‖ invitation id`, so a sealed value cannot be moved to another invitation or tenant. |
| `email_lookup` | **HMAC-SHA-256** (hex) over `pragya/invitation-email-lookup/v1 ‖ tenant id ‖ address`, under a key **different from** the encryption key. |
| `email_lookup_key_id` | The id of the lookup key that produced `email_lookup`. |

Acceptance normalises the caller's verified address, computes the lookup under **every lookup key the process holds** (active first), and runs one
indexed query: `tenant_id = $1 AND status = 'pending' AND expires_at > $now AND email_lookup_key_id = ANY(..) AND email_lookup = ANY(..)`. The adapter then
keeps only rows whose *(key id, hash)* pair is exactly one it computed. No decryption, no plaintext and no scan.

### Guarantees (each has a test; see the implementation log)

1. **A plaintext address cannot be inserted.** `invitations_email_sealed` accepts only the sealed format, which contains no `@`. This holds for any
   code path, including a future bug.
2. **A dump alone yields nothing usable**: the hash is keyed, and the key is not in the database, so it cannot be dictionary-attacked offline.
3. **Tenant isolation.** The tenant id is inside the HMAC input, so the same person invited by two organisations has two unrelated hashes: the database
   cannot show that one person belongs to both. The query is also filtered by tenant and runs under RLS.
4. **Matching is by normalised address**: NFC, trimmed, lower-case, exactly one address (no display name, no comments), ≤ 254 bytes, no control
   characters. Plus-tags and dots in the local part stay significant.
5. **Only pending, unexpired invitations match.** The index is partial (`WHERE status = 'pending'`).
6. **Nothing prints an address.** `emailkey.Address` and `emailkey.Lookup` redact themselves under every `fmt` verb and to `slog`; `Reveal()` is the one
   deliberate exit (sealing, and the notification adapter that sends the invitation in S5/S10).

### Two extra columns: a deviation from the specification's column list (approved)

`email_lookup` and `email_lookup_key_id` are not in the specification's column list. They are the approved E3 addition; the schema-conformance test
(`migrations/migrations_test.go`), which otherwise forbids extra columns, carries an explicit allow-list entry for each.

## Key management and rotation

- **Config** (this repository's names; the spec's parameter table has none): `INVITE_LOOKUP_KEYS`, `INVITE_LOOKUP_ACTIVE_KEY_ID`,
  `INVITE_ENCRYPTION_KEYS`, `INVITE_ENCRYPTION_ACTIVE_KEY_ID`. Key lists are `id:base64` entries; lookup keys ≥ 32 bytes, encryption keys exactly 32.
  Format is validated at startup; **absence** is reported only by `Config.RequireInvitations()`, which the invitation endpoints call when they are added
  (S5), so the API still starts without them, as before. A key may not appear in both sets.
- **Rotation, no re-processing.** Every row carries the id of the key that made it. To rotate: add the new key, make it active, keep the old one.
  New invitations use the new key; acceptance already searches every held lookup key. Invitations live 7 days, so **retire the old key at least 7 days
  after it stopped being active** (a shorter wait would strand still-pending invitations). Sealed values are opened by the id embedded in them.
- **Compromise.** Rotate as above and, if the lookup key leaked, treat existing hashes as recoverable by dictionary attack until the 7-day window has
  passed and the old key is retired; a leaked encryption key exposes only invitations created under it.
- **Phase 5 replaces the key source only** (Secret Manager / Cloud KMS envelope). Formats, derivation and the `emailkey.Index` interface stay.

## Migration 00018

Adds the two columns, three CHECK constraints (sealed format, 64-hex lookup, key-id format) and the partial index. It **refuses to run if `invitations`
is not empty**: nothing has written an invitation before Sprint 5, so no deployed database can hold one, and existing rows could not be backfilled anyway
(their address is not recoverable). The guard turns that into a clear error instead of a `NOT NULL` failure. A `Down` migration is provided.

## Known limits

- **Internationalised domain names** are compared as normalised Unicode, not converted to punycode: that needs a new dependency (AGENTS.md rule 6). Both
  sides pass through the same function, so equal input matches equal input; a user whose token carries the punycode form of an address invited in Unicode
  form (or the reverse) would not match. Revisit if the pilot markets need it.
- The HMAC lookup is deterministic per (tenant, address, key): within one tenant, two invitations to the same address have the same hash. That is
  intended (it is how they are found) and is visible only to someone who can already read that tenant's rows.

## Consequences

- S5 builds invitation creation, acceptance and revocation on `emailkey.Keyring` and `postgres.InvitationIndex`; it does not change the schema again.
- The notification adapter (S10) is the only consumer of `Address.Reveal()` outside sealing, and it receives the address from the request that created
  the invitation, not from the database.
- **Rule for S5:** `audit` records and outbox events must never contain the address or the hash; an invitation's audit row references its id only. Nothing
  writes invitation audit rows yet, so this is a requirement on S5, not something E3 has tested.
