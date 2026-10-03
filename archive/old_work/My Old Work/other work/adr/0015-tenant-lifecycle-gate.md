# ADR 0015 — A tenant that is not active is closed to everyone

- **Status:** Accepted (P1, Sprint 6 security review, finding S6-01).
- **Owner:** P1 (platform)
- **Spec:** 6182 §04 (tenant `status`: provisioning / active / suspended / deleting), §07.7 ("Erasure revokes access immediately when due"), §09.3
  ("Check membership status on each request"), §09.6 (incident response: "Disable affected endpoint/export; revoke grants/keys as needed").

## Context

`tenants.status` has four values and, before S6, nothing read it. A tenant marked `suspended` (a security suspension) or `deleting` (the cooling-off
of a tenant erasure, S8) stayed fully usable by every member: the membership check looked only at the member's own status. Plan S8 requires access
"revoked immediately when due"; a security suspension is meaningless if members keep reading and writing. This was found while writing the S6
IDOR/role matrix (which exercises every served route) and reading what each request actually loads.

## Decision

The status of the tenant is loaded **with the membership**, in the same query, on every request, and only `active` lets a request through:

- `auth.Membership.TenantStatus` comes from `app.tenants` joined in `GetMembershipForUser`; `auth.LoadPrincipal` answers `ErrTenantInactive` for any
  other value, **including an empty or unknown one** (default deny).
- `ErrTenantInactive` maps to **403 `FORBIDDEN`**, like a suspended membership. It is checked after the membership itself, so a stranger still sees
  404 and existence is not disclosed.
- One mechanism covers everything that authorises through `LoadPrincipal`: the composed write and read paths (`apikit`), and `worker.Job.Authorize`
  for in-flight jobs (a tenant that is suspended or being erased stops user-scoped work the same way a revoked member does).
- Invitation acceptance is not a `LoadPrincipal` path (the caller is not a member), so `Team.MayAttemptAccept` and `Team.Accept` check
  `TeamStore.TenantActive` themselves and answer 404, as for a tenant that does not exist. `Accept` does not rely on the gate having run.
- `POST /v1/tenants` (the tenant does not exist yet) and `GET /v1/me` (lists the caller's own memberships) are unaffected; `/v1/me` therefore still
  lists a suspended tenant, which is how a client learns it exists.

## Consequences

- The tenant's own `GET` is refused too. There is no read-only "suspended" mode; a client shows the state from `/v1/me` and the 403. If product wants
  owners to read a suspended tenant, that is a deliberate carve-out to add with its own test.
- **Jobs that must run while a tenant is `deleting`** (the S8 privacy erasure, S9 retention) must not call `Job.Authorize`; they run under the
  maintenance identity and system actor (ADR 0010), which is how they are specified anyway.
- One extra join per request on a primary-key lookup; no extra round trip.
- Setting a tenant's status is not exposed on `/v1` (`TenantPatch` has no `status`); suspension is an operator procedure (plan E7) and the privacy
  framework (S8) moves a tenant to `deleting`.
- Tested: `TestInactiveTenantIsClosedToEveryone` (every tenant route as owner and manager, for suspended, deleting and provisioning; invitees cannot
  join; reactivation restores service), `TestAuthorizeReloadsTheRequestersCurrentMembership`, `TestAcceptGate`. Mutation-checked (four guards).
