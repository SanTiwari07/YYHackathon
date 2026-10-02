# ADR 0014 — Team management: authority, owner controls, invitation acceptance

- **Status:** Accepted (P1, Sprint 5). Implements task 1.20 of [the Phase 2–3 plan](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/docs/platform/PHASE2_3_PLAN.md) (section 4.4); builds on ADR 0013.
- **Owner:** P1 (platform)
- **Spec:** 6182 §04 W03, §09.2 (permission matrix and the notes under it), §09.3, §09.7, §14 (`Membership`, `MembershipPatch`, `Invitation`,
  `InvitationCreate`), §17-§18 (`memberships`, `membership_field_grants`, `authorization_revisions`, `invitations`).

The specification states the rules of W03 in one line ("role cannot exceed inviter authority; last owner protection; seven-day expiry, single
use; revoked/expired → 409; invitee must authenticate verified matching address") and leaves the rest to the implementer. This ADR records
every place where implementing it meant choosing something the text does not spell out. Nothing here changes the contract's shapes.

## Decisions

### 1. Authority is a rank, and only owner and admin manage the team

`owner` (3) > `admin` (2) > every other role (1). The permission matrix (`member:manage`: owner/admin only) is the first gate; the domain
(`internal/domain/tenancy/team.go`) re-checks it, so a later matrix edit cannot widen the rules below. The rules:

- an actor never assigns a role, or touches a membership, above their own rank;
- an actor never hands out **field scope they do not hold**: a field list must be a subset of the actor's own grants, and tenant-wide access
  (`all_fields`) needs an actor who is admin-or-above **and** holds tenant-wide scope themselves. (The spec says "only owner/admin may assign"; an
  admin invited without tenant-wide scope must not be able to mint it.) This is our reading of "role cannot exceed inviter authority".

### 2. Owner controls are outside `MembershipPatch`

Spec §09.2: "Last-owner removal, owner role assignment and tenant-region changes are privileged workflows outside ordinary MembershipPatch."
So through this API the owner role cannot be assigned, an owner membership cannot be changed, and therefore the last owner cannot be removed.
The single ordinary change on an owner is **their own display locale**. Ownership transfer is the support-controlled procedure of the contract
(`Invitation.role` description); it is not built here and is not exposed on `/v1` (plan E7). An attempt answers **403 `FORBIDDEN`**.

### 3. Nobody changes their own role, status or field scope

`ErrSelfChange` (403). A self-service path to a wider role or scope is exactly the "owner/self invitation abuse" of §09.7. Locale is exempt.
Self-invitation (an invitee address equal to the actor's own) is a **422** on `/email` with code `SELF_INVITATION`.

### 4. Suspension is revocation, and revocation removes grants

Approved decision A9 made revocation a suspension "(+ grant removal)". Implemented literally: moving a membership to `suspended` deletes every grant
and clears `all_fields`; asking for grants on a suspended membership is a 422. Reactivation restores the **role** and never the old access; the
owner or admin grants scope again. Every status, role, `all_fields` and grant change bumps `auth_revision` through the trigger of migration 00006, so
every cursor the member holds stops working (spec §06.2 "A revocation invalidates cursor"), and the next request is refused (T02).

`membership_field_grants` is the authority; `memberships.field_ids` is a projection written in the same transaction. Responses are built from the
authority table. `PATCH … field_ids` **replaces** the list.

### 4b. Field existence is a port, and it fails closed

`membership_field_grants.field_id` still has no foreign key: the `fields` table is P3's and does not exist yet. Grants are validated through
`tenancy.FieldValidator`. Until P3 supplies the real one the default is `NoFields`: **no field exists, so no field id can be granted or invited**;
`all_fields` is unaffected. Removal of a grant is never validated (a deleted field can always be un-granted). The invitation is re-validated at
acceptance and the acceptance fails with 409 if a granted field has since vanished.

### 5. Invitations

- **One pending invitation per address per tenant** (log item from E3), checked with the lookup under every held key and serialised by a
  transaction-scoped advisory lock keyed by the (tenant-bound, one-way) lookup, so concurrent requests cannot both pass. An *expired* pending
  invitation does not block a new one.
- **Expiry is the clock.** A pending invitation whose `expires_at` has passed *is* `expired` (`Invitation.EffectiveStatus`); no sweep is needed for
  it to take effect. A retention job may persist the status later.
- **Acceptance** (`invitation:accept`) needs the identity provider's **verified** address (`email_verified`), normalised, matched to the
  invitation by the keyed lookup. There is no role check: an existing membership authorises nothing, and an existing membership (any status) is a
  409 `CONFLICT`, never a second membership. A non-matching caller, an unknown id and a foreign tenant are all **404**; only a matching caller is
  told the invitation is used, revoked or expired (409). Suspended members are not re-invited; the owner reactivates them.
- **Revoke** is safe to repeat (an already revoked invitation answers 200 with its version); an accepted or expired one is 409.
- **The inviter is not re-checked at acceptance.** The specification's `invitations` table has no inviter column, so a suspended inviter's
  still-pending invitations remain acceptable until an owner revokes them. Recorded as **B13**.

### 6. The accept gate: strangers do no work in the tenant

`accept` is a tenant-scoped write whose caller is by definition not (yet) a member, so the role matrix cannot protect it, and the path tenant is
attacker-chosen. `apikit.Kit.MutateAsInvitee` therefore takes a **gate** that runs inside the tenant transaction *before* the idempotency
reservation and before the invitation row is locked: it answers 404 unless the caller already has a membership (a retry after a lost response finds
its own record) or the invitation was made for their verified address. Honest scope of this control: a failed request rolls back its reservation
(B5), so a stranger could never have *persisted* an idempotency row; what the gate prevents is a stranger taking the invitee's row lock and a
reservation slot, i.e. work and contention inside someone else's tenant. Over HTTP a refusal by the gate and one by `Accept` look identical (404),
so the gate has its own test (`TestAcceptGate`).

### 7. The address never enters an idempotency record

`POST /invitations` returns the invitee address (the contract requires it) and the idempotency record persists the response for 24 hours. Storing it
would contradict "encrypted at rest". The handler therefore returns the **sealed** value in its result, the record keeps that, and
`MutateSpec.Reveal` opens it on the way out — for the first response and every replay alike, so both are the same document. The invitation
list opens the sealed values for the owners and admins who may list them. The address is in no audit record, no outbox event (which is a thin
reference), no log, and no job.

### 8. Events and audit

Creating an invitation writes `notification.requested` (the contract has no invitation event; notification delivery is P4's, S9). Accepting or
changing a membership writes `membership.changed`. Audit records carry action, resource and changed field **names** only.

### 9. A new error code: `CONFLICT` (409)

The specification fixes **409** for a revoked, expired or used invitation but names no code, and the catalogue had only idempotency and region 409s.
`CONFLICT` is added to `x-error-codes` (defined_by `contract`) and to the shared `Conflict` response. This is **change request CR-01 for
`contract-v1.0.0-rc2`** (plan E6); the lock was re-hashed now because the Go catalogue and the contract must be identical (a test enforces it). The
version string stays `1.0.0-rc1` until the rc2 batch is cut at the end of S6.

### 10. In-flight jobs re-check the requester

`worker.Job.Authorize` reloads the requester's *current* membership and grants (spec §09.4 "Workers load the original principal scope and current
grant before side effects") and answers `ErrRequesterRevoked` when the membership is suspended or gone. It is **opt-in** per handler: jobs that
legitimately outlive their requester (a privacy erasure requested by a subject who then leaves; system retention) must not be stopped by it.

## Consequences

- No migration was needed: migrations 00003-00006 and 00018 already provide the tables, triggers and columns.
- The contract's `Membership`/`Invitation` shapes are served unchanged; the only contract edit is the additive `CONFLICT` code.
- Follow-ups: the real `FieldValidator` and the FK (P3); the support-controlled ownership transfer (operator procedure, S7); the inviter re-check
  needs an inviter column, which would be a spec change (B13).
