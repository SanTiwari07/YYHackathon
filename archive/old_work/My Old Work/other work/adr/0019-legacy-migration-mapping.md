# ADR 0019 — Legacy → new data mapping for `tools/migrate-legacy`

- **Status:** Proposed. Decisions 1–3 below are final (product-approved); the document as a whole awaits the P1
  approval that plan task 3.1 requires ("Mapping doc approved by P1"). The four open questions of the first draft
  (OQ-1–OQ-4) were resolved on 2026-09-27 (§9). Applying them surfaced three narrower questions (OQ-5–OQ-7, at the
  end), each with a provisional deterministic behaviour so that no part of task 3.16 is blocked.
- **Date:** 2026-09-27 (amended 2026-09-27: OQ-1–OQ-4 resolved, Decision 3 windows superseded; amended again
  2026-09-27: OQ-5–OQ-7 resolved, placeholder permanence recorded as risk B7)
- **Owner:** P3 (fields and farm data; owns `tools/migrate-legacy`)
- **Supersedes / superseded by:** none
- **Closes:** plan task 3.1 (legacy → spec table map), which was marked done but never produced. Feeds task 3.16.
- **Spec:** 6182 §01.4 (season labels), §04.3, §07.2 (area computed, client area rejected), §09.3 (provider subject →
  internal UUID), §12.2 (acceptance scenario T10), §14 (parameter dictionary: `FieldCreate`, `Season`, `CropCycle`,
  `Observation`), §17 (physical dictionary). Related: ADR 0004 (legacy scripts frozen), `docs/platform/STATUS.md` B6.

## Context

The legacy application (`cmd/server`, database `agri_platform`, schema frozen in `scripts/db/legacy/schema.sql` per
ADR 0004) holds real farmer data in eight farmer-centric tables: `farmers`, `farmer_locations`, `farms`, `crops`,
`irrigation`, `soil_info`, `consents`, `vi_reports`. The new platform's tables are designed from the specification,
not derived from the legacy ones (ADR 0004, decision 4). They are tenant-scoped with forced row-level security, and
they carry invariants the legacy data never had to satisfy:

- `app.fields.geom` is a required `geometry(Polygon, 4326)` that must pass the field boundary rules. These are
  `fields.ParsePolygonAndHash` (rings, positions, vertex limit, antimeridian) plus the PostGIS topology and area check
  (0.01–20,000 ha).
- `app.seasons` needs `start_date`/`end_date` with `end_date - start_date < 730`.
- `app.crop_cycles` needs a season the field belongs to (FK onto `app.season_fields`). Non-failed cycles on one field
  may not overlap (`crop_cycles_no_overlap`), and `irrigation_method` is NOT NULL.
- `app.observations` needs a `processing_version` and a `job_id`.

Plan task 3.16 migrates "farmers → users/memberships, farms → farms/fields, crops → crop cycles" with a dry-run report
and an idempotent run. That tool must be built against a reviewed mapping, and this ADR is that mapping. New-schema
column names were confirmed against `migrations/00002`, `00003`, `00006`, `00023`, `00028`, `00029`, `00035`, `00036`
and `00039` at the date above.

## Decision

### 1. Unit of work and fixed values

- **One tenant per legacy farmer.** Each legacy `farmers` row becomes one new tenant, and that farmer becomes the
  tenant's sole `owner` membership. No tenant is shared between farmers.
- **One transaction per farmer.** Everything created for one farmer is written in one tenant transaction: the tenant,
  membership, authorization revision, farms, fields, seasons, season fields, crop cycles, consent, their audit/outbox
  rows and the id-map rows (§7). It runs with `app.tenant_id` set to the new tenant. An unexpected error rolls back that
  farmer only; the report counts it as `failed` and the next run retries it. Row-level skips (§5, and the skip
  reasons in §8) are not errors and do not roll back the farmer.
- **Writes go through the domain code, not raw SQL**, so every invariant surfaces as a typed domain error:
  - tenancy's store (`InsertTenant`, and `InsertOwner` for the membership plus authorization revision 1). The
    `tenancy.Service` owned-tenant quota does not apply: each farmer gets exactly one tenant.
  - `farms.Service.Create`
  - `fields.Service.Create`
  - `seasons.Service.CreateSeason` / `UpdateSeason` / `CreateCropCycle`
  - `consent.Service.SetConsent`
- **Audit.** Every created resource gets the audit record its normal write path writes, with
  `ActorID = audit.SystemActor`, `RequestID = run_id` and `ReasonCode = "legacy_migration"`. The same outbox events
  are emitted (`field.created`, `membership.changed`), so downstream projections see migrated data exactly as they see
  new data.
- **Timestamps.** `created_at`/`updated_at` of every new row are the migration run time: they mean "initial
  persistence time" of the new record. The legacy `created_at` / `consented_at` is kept only in the id map
  (`legacy_created_at`, §7) for traceability.
- **Fixed values (engineering defaults, disclosed).** All legacy data is India-only. The legacy schema has no
  per-record IANA timezone, and `farmer_locations.state`/`district` do not map to an IANA zone.

| Target | Value |
|---|---|
| `tenants.countries` | `["IN"]` |
| `tenants.timezone`, `farms.timezone`, `fields.timezone` | `Asia/Kolkata` |
| `farms.country`, `fields.country` | `IN` |
| `tenants.currency` | `INR` |
| `tenants.home_region` | the deployment cell (`HOME_REGION`), as `tenancy.Service.Create` requires |
| `tenants.status` | `active` |
| `tenants.support_access_enabled` | `false` |
| locale (`tenants.default_locale`, `memberships.locale`) | `english`→`en`, `hindi`→`hi`, `marathi`→`mr`, `others`→`en` |
| `irrigation_type` → `crop_cycles.irrigation_method` | `rainfed`→`rainfed`, `drip_irrigation`→`drip`, `sprinkler`→`sprinkler`, `borewell`→`other`, `canal`→`other`; a farm with no `irrigation` row → `unknown` |

- **Text normalisation.** Every migrated string passes `text.Clean` (NFC, trimmed, valid UTF-8; ADR 0012) and is
  truncated rune-safely to the contract limit. Each truncation increments the `truncated` warning (§8):
  - tenant, farm and field names: 120
  - `crop_code`: 80
  - `variety`: 120

### 2. Mapping tables

"Not migrated — see B6-equivalent note" means the value has no destination in the new schema: the same conclusion as
`docs/platform/STATUS.md` B6 for the onboarding flow. It is left behind in the frozen legacy database, and no schema is
invented to hold it.

#### 2.1 `farmers` → `app.tenants`, `app.memberships`, `app.authorization_revisions`

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| farmers | id | `legacy_migration.id_map` (`legacy_key`) | Idempotency key for the tenant and the membership (§7). New ids are fresh UUIDs; the legacy id is never reused as a new id | One legacy farmer id yields two map rows (`farmer_tenant`, `farmer_membership`) |
| farmers | firebase_uid | `app.memberships.user_id`, `app.memberships.status` | Identity confirmed (§9.1) → `user_id = auth.DerivedResolver.Resolve("https://securetoken.google.com/" + FIREBASE_PROJECT_ID, firebase_uid)` (UUIDv5, §09.3) and `status active`. Otherwise → placeholder `user_id` and `status suspended` (data-only migration, §9.1). The subject is not stored anywhere | Unconfirmed farmers are still migrated in full and reported `identity_pending` (§8) |
| farmers | mobile_number | — | Not migrated — see B6-equivalent note | Identity is the identity provider's (Firebase phone sign-in); the new schema stores no phone number. Never written to logs or the report |
| farmers | password_hash | — | Not migrated | Password sign-in is retired; credentials are the identity provider's. Never read into logs or the report |
| farmers | name | `app.tenants.name` | `text.Clean`, truncate to 120. Blank or NULL → the first migrated farm's name; none → `Migrated farm` | The tenant is the farmer's own organization. No user profile column exists; the display name belongs to the identity provider |
| farmers | age | — | Not migrated — see B6-equivalent note | |
| farmers | gender | — | Not migrated — see B6-equivalent note | |
| farmers | preferred_language | `app.tenants.default_locale`, `app.memberships.locale` | Locale map in §1 | `others` → `en` because no language is known |
| farmers | created_at | `legacy_migration.id_map.legacy_created_at` | Copied for traceability; new rows use run time (§1) | |
| farmers | updated_at | — | Not migrated | No meaning for the new records |
| (derived) | — | `app.tenants.*` | `id = tenant_id` = new UUID; `version 1`; fixed values in §1 | |
| (derived) | — | `app.memberships.*` | `role owner`, `all_fields true`, `field_ids []`, `version 1`; `user_id` and `status` as above | Written by `InsertOwner` (active). For `identity_pending` farmers the tool then sets `status suspended` through the team store's `UpdateMember` in the same transaction: the store, not the `tenancy.Team` rules, because those rules exist to stop a live tenant losing its last active owner, and here that is the intent (§9.1) |
| (derived) | — | `app.authorization_revisions.*` | `auth_revision 1` for the owner membership | Written by `InsertOwner` |

#### 2.2 `farmer_locations` → nothing

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| farmer_locations | id | — | Not migrated — see B6-equivalent note | Row counted in the report (`not_migrated.farmer_locations`) |
| farmer_locations | farmer_id | — | Not migrated — see B6-equivalent note | |
| farmer_locations | pin_code | — | Not migrated — see B6-equivalent note | |
| farmer_locations | state | — | Not migrated — see B6-equivalent note | Not usable as a timezone either (§1) |
| farmer_locations | district | — | Not migrated — see B6-equivalent note | |
| farmer_locations | taluka | — | Not migrated — see B6-equivalent note | |
| farmer_locations | village_name | — | Not migrated — see B6-equivalent note | |
| farmer_locations | full_address | — | Not migrated — see B6-equivalent note | |

#### 2.3 `farms` → `app.farms` and `app.fields` (+ `app.field_boundaries`)

Each legacy farm becomes exactly one `app.farms` row, and at most one `app.fields` row (Decision 2, §5).

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| farms | id | `legacy_migration.id_map` (`legacy_key`) | Idempotency key for the farm (`farm`) and its field (`farm_field`) (§7) | |
| farms | farmer_id | `app.farms.tenant_id`, `app.farms.owner_user_id`, `app.fields.tenant_id` | Resolves to the farmer's new tenant and owner `user_id` | |
| farms | farm_name | `app.farms.name`, `app.fields.name` | `text.Clean`, truncate to 120. Blank → `Unnamed farm` | Field names are unique per active farm; each farm has one field, so no collision |
| farms | total_area | — | Not migrated — see B6-equivalent note | §07.2: area is computed by PostGIS from the geometry; client-supplied area is rejected. Used only for the `declared_area_mismatch` warning (§8) |
| farms | area_unit | — | Not migrated — see B6-equivalent note | Used only to convert `total_area` to hectares for that warning: acres × 0.40468564224 |
| farms | land_ownership | — | Not migrated — see B6-equivalent note | §01: field ownership is "an access responsibility, not a claim of legal land title" |
| farms | latitude | — | Not migrated — see B6-equivalent note | The field boundary supersedes a farm point; the new schema has no farm point |
| farms | longitude | — | Not migrated — see B6-equivalent note | As above |
| farms | boundary_geom | `app.fields.geom`, `app.field_boundaries` (version 1) | `ST_AsGeoJSON(boundary_geom)` → `fields.Service.Create`, which canonicalises (7 decimals, orientation) and hashes the geometry, and PostGIS judges topology and area. `source = 'import'`, `created_by` = the farmer's `user_id`. `app.fields.area_ha` is computed by PostGIS | NULL → field skipped, reason `boundary_missing` (Decision 2). A geometry `fields.Service.Create` rejects → field skipped with the `fields.Reason*` code as the reason (§5) |
| farms | location_photo_url | — | Not migrated — see B6-equivalent note | No farm-photo asset purpose exists; the URL is not fetched |
| farms | created_at | `legacy_migration.id_map.legacy_created_at` | Copied for traceability (on the `farm` map row) | |
| (derived) | — | `app.farms.*` | `country IN`, `timezone Asia/Kolkata`, `archived false`, `version 1` | Created even when the field is skipped: a farm has no geometry requirement |
| (derived) | — | `app.fields.*` | `farm_id` = the new farm, `country IN`, `timezone Asia/Kolkata`, `archived false`, `group_ids []`, `monitoring_enabled` per §2.7 | |

#### 2.4 `crops` → `app.crop_cycles` (+ `app.seasons`, `app.season_fields`)

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| crops | id | `legacy_migration.id_map` (`legacy_key`) | Idempotency key for the crop cycle (`crop`) (§7), and for the season it anchors (`season`) | |
| crops | farm_id | `app.crop_cycles.field_id` | The field created from that farm. Per field, only the crop with the latest `sowing_date` migrates; every earlier crop is skipped `superseded_by_later_cycle`, naming the superseding crop (§9.2) | Farm's field skipped → crop skipped, reason `field_not_migrated` |
| crops | crop_name | `app.crop_cycles.crop_code` | `text.Clean`, truncate to 80 | Free text, no catalog table exists (only `char_length 1..80`). Blank → crop skipped, reason `crop_name_empty` |
| crops | crop_variety | `app.crop_cycles.variety` | `text.Clean`, truncate to 120; blank → NULL | |
| crops | sowing_date | `app.crop_cycles.sowing_date` | Copied | Also selects the crop that migrates per field (§9.2) and derives the season window (§4) |
| crops | season | `app.seasons.name` (label), via `app.crop_cycles.season_id` | The crop's season is synthesized from its `sowing_date` (§4); the enum value is only the season's label, e.g. `Kharif 2024`. The field is added to `app.season_fields` once | The enum no longer determines dates (Decision 3 windows superseded, §4) |
| crops | expected_harvest_month | — | Not migrated — see B6-equivalent note | A month name, not a date; `harvest_date` stays NULL and is never derived (§9.2) |
| crops | created_at | `legacy_migration.id_map.legacy_created_at` | Copied for traceability | |
| (derived) | — | `app.crop_cycles.irrigation_method` | From the farm's selected `irrigation` row via the §1 map; no row → `unknown` | Several rows → one is selected deterministically (§9.4) |
| (derived) | — | `app.crop_cycles.status` | Created `planned` by `CreateCropCycle`. If `sowing_date` ≤ the run date, moved `planned`→`growing` by `UpdateCropCycle` in the same transaction (§9.2) | Never `harvested`: no harvest date exists and none is fabricated |
| (derived) | — | `app.crop_cycles.harvest_date`, `target_yield_t_ha`, `actual_yield_t_ha`, `growth_stage_code` | NULL | No legacy source |

#### 2.5 `irrigation` → `app.crop_cycles.irrigation_method`

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| irrigation | id | — (selection only) | With several rows per farm, the row with the lexically greatest `id` is selected (§9.4) | The value lands on crop cycles; the row itself has no counterpart |
| irrigation | farm_id | (join) | Selects the crop cycle of that farm's field | The legacy table has no UNIQUE on `farm_id`; several rows per farm are resolved by §9.4 |
| irrigation | irrigation_type | `app.crop_cycles.irrigation_method` | §1 map; `borewell` and `canal` → `other` | The new enum describes the application method; borewell and canal are water sources |
| irrigation | water_source | — | Not migrated — see B6-equivalent note | Non-null values counted (`not_migrated.irrigation_water_source`) |

#### 2.6 `soil_info` → nothing

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| soil_info | id | — | Not migrated — see B6-equivalent note | Row counted (`not_migrated.soil_info`) |
| soil_info | farm_id | — | Not migrated — see B6-equivalent note | |
| soil_info | soil_type | — | Not migrated — see B6-equivalent note | A self-declared category. `app.soil_tests` is a measurement that requires `depth_cm` and `method` (§14 `SoilTestCreate`); inventing those would fabricate a lab result |

#### 2.7 `consents` → `app.consents` (+ `app.fields.monitoring_enabled`)

| Legacy table | Legacy column | New table.column | Transform rule | Notes |
|---|---|---|---|---|
| consents | id | `legacy_migration.id_map` (`legacy_key`) | Idempotency key for the consent (`consent`) (§7) | |
| consents | farmer_id | `app.consents.tenant_id`, `app.consents.user_id` | The farmer's new tenant and `user_id` | One consent per farmer in legacy (UNIQUE `farmer_id`), one per (tenant, user, purpose) in the new schema |
| consents | satellite_monitoring | `app.consents.granted` with `purpose = 'satellite_monitoring'` | Copied, written with `consent.Service.SetConsent` after the farmer's fields exist | `satellite_monitoring` is the purpose the legacy step recorded, and the purpose task 3.14 defined for it (`internal/domain/consent/model.go`) |
| consents | consented_at | `legacy_migration.id_map.legacy_created_at` | Copied for traceability; `app.consents.created_at` is run time | No `consented_at` column in the new schema |
| (derived) | — | `app.fields.monitoring_enabled` | `true` only if the farmer has a consent row with `satellite_monitoring = true`; otherwise `false`, set at field creation | Preserves legacy behaviour: the legacy VI trigger ran only in the consent step (`internal/service/onboarding.go`, `SubmitConsent`). A farmer without a consent row was never monitored, and a refusal blocks monitoring (3.14). Re-granting later does not re-enable monitoring (3.14) |

### 3. What is created without a legacy row

`app.authorization_revisions` (with each membership) and `app.field_boundaries` version 1 (with each field) are
written by the domain write paths above. So are `app.season_fields` (§4), `app.audit_records` and `app.outbox` (§1).
Nothing else is created. In particular, no `app.observations`, `app.jobs`, `app.soil_tests`, `app.field_groups` or
`app.assets` rows are created.

### 4. Season synthesis — Decision 3 (final, product-approved; windows amended 2026-09-27 by the OQ-3 resolution)

The legacy `crops.season` is an enum (`kharif`/`rabi`/`zaid`) with no year, only a `sowing_date`. `app.seasons` needs
`start_date`/`end_date` (NOT NULL, `end_date >= start_date`, span < 730 days per `seasons_date_window_check`).
`seasons.Service.CreateCropCycle` also requires the cycle's `sowing_date` to lie inside its season's window
(`ErrOutsideSeason`).

#### Superseded: the original fixed calendar windows (struck out 2026-09-27)

The first draft synthesized one season per (tenant, enum value, calendar year Y of `sowing_date`) with these windows.
**They are wrong and no longer apply:**

| Enum | `start_date` | `end_date` | `name` |
|---|---|---|---|
| ~~kharif~~ | ~~1 June Y~~ | ~~31 October Y~~ | ~~`Kharif Y`~~ |
| ~~rabi~~ | ~~1 November Y~~ | ~~31 March Y+1~~ | ~~`Rabi Y-(Y+1)`, e.g. `Rabi 2024-25`~~ |
| ~~zaid~~ | ~~1 March Y~~ | ~~30 June Y~~ | ~~`Zaid Y`~~ |

Why they were struck out: a fixed calendar table cannot guarantee that a crop's `sowing_date` falls inside its own
season window, which season membership (`ErrOutsideSeason`) requires. Real legacy crops fail containment:

- a `rabi` crop sown January–March lands in a window that starts on 1 November of the same year, after it was sown;
- a `kharif` crop sown before 1 June;
- a `zaid` crop sown before 1 March or after 30 June.

(This was OQ-3 in the first draft.)

#### Current rule: the window is derived from each crop's own `sowing_date`

For every crop that migrates (one per field, §9.2):

- `start_date` = `sowing_date` − 30 days
- `end_date` = `sowing_date` + 210 days

The `sowing_date` therefore lies inside `[start_date, end_date]` **by construction**. The span is 240 days, well under
the `seasons_date_window_check` cap of 730.

**Rationale.** A window read off the crop's own dates assumes no calendar convention, country or hemisphere. That is
closer to the specification than any fixed table, since a season is a "Season label; user-defined, not fixed to
hemisphere" (§14, `Season.name`), and the architecture "does not assume India, INR, a northern-hemisphere season"
(§01.4). The product-approved Indian convention of Decision 3 now survives only as the season's label.

- **Label.** The enum value is kept, as a label only: `name` = the enum capitalised + the calendar year of the
  anchoring `sowing_date`, e.g. `Kharif 2024`, `Rabi 2025`, `Zaid 2025`. Rabi no longer gets a two-year label
  (`Rabi 2024-25`): that label described the struck-out November–March window, which the season no longer follows.
- **Sharing.** Each migrating crop's derived window is its own season candidate. It merges into an existing season
  only when that season (same tenant, same enum label) already covers the same field and its window contains the new
  `sowing_date`.
  - **Consequence:** because only one crop per field migrates (§9.2), that condition never holds today. Every migrated
    crop cycle gets its own season, covering exactly its one field. Seasons are **not** shared across fields: two fields'
    derived windows are generally different, and joining one field to another field's window would bend one of them.
  - The rule that a season is inserted into `app.season_fields` **once per distinct field it actually covers** is
    unchanged; here that is one row per season.
  - The first draft's (tenant, enum, year) sharing belonged to the struck-out windows and no longer applies.
- **Processing order.** For determinism (§7), a farmer's crops are processed in `sowing_date` ascending, then `crops.id`
  ascending.
- **Creation order.** The season is created with `CreateSeason` (initial status `planned`) with its field as
  `field_ids`. Then its crop cycle is created (§9.2). Then the season is moved by `UpdateSeason` to the status its
  window implies on the run date:
  - `planned` if the window starts after the run date;
  - `planned`→`active` if the run date is inside the window;
  - `planned`→`active`→`closed` if the window ended before the run date.

  Transitioning after the cycle exists keeps cycle creation independent of season status. Each transition is audited
  like any other.

### 5. Missing or invalid boundary — Decision 2 (final)

§14 makes `Field.geometry` mandatory and non-nullable with no default (`FieldCreate.geometry`: required). The legacy
`farms.boundary_geom` has no NOT NULL constraint, so some legacy farms may have none. Such a farm cannot become a valid
Field. The rule is a **row-level skip, not a farmer-level failure**:

- Skip creating that Field. Record the farm as a skipped row in the id map and the report with reason
  `boundary_missing`.
- Still migrate the farmer's identity (tenant, membership), the `app.farms` row, and every other farm and field that
  has valid geometry.
- The crops of a farm whose field was skipped are skipped with reason `field_not_migrated`.
- The same rule applies to a present geometry that the field boundary rules reject. It cannot become a valid Field
  either, so it is skipped with the precise `fields.Reason*` code as its reason: `geometry_malformed`,
  `geometry_ring_too_short`, `geometry_ring_not_closed`, `geometry_position_invalid`, `geometry_too_many_vertices`,
  `geometry_crosses_antimeridian`, `geometry_invalid_topology`, `geometry_area_too_small` or `geometry_area_too_large`.
- A skipped row is re-evaluated on the next run (§7), so correcting the legacy geometry and re-running migrates it.

### 6. `vi_reports` — Decision 1 (final): NOT MIGRATED

**`vi_reports` rows are not migrated.** Its columns are `id`, `farm_id`, `cvi_mean`, `cvi_median`, `cvi_std_dev`,
`ndvi`, `evi`, `savi`, `ndmi`, `ndwi`, `gndvi`, `confidence_score`, `scenes_used`, `period_start`, `period_end` and
`created_at`. None of them has a destination.

Rationale (spec-mandated):

- **Observations need real provenance.** The new `app.observations` schema requires a non-null `processing_version`,
  "Immutable pipeline build and parameter-set identifier" (§14 `Observation.processing_version`, §17; migration 00031),
  tied to a real analysis job (`job_id` NOT NULL).
- **The legacy methodology was already unreliable.** Legacy `vi_reports` used a different composite-index (CVI)
  methodology that is internally inconsistent in its own schema file:
  - The table's header comment gives the CVI weights as NDVI 0.35, EVI 0.25, SAVI 0.15, NDMI 0.15, GNDVI 0.10.
  - The inline column comments give NDVI 0.70, EVI 0.10, SAVI 0.05, NDMI 0.10, GNDVI 0.05.
  - The seed row stores `confidence_score` 87.4 against a column comment of "0–1 scale".

  (Precision on the evidence: the weight disagreement is between the header comment and the column comments; the seed
  data contradicts the confidence scale.) This is direct evidence the old provenance was already unreliable.
- **Fabrication is forbidden.** Fabricating a `processing_version`/`job_id` to satisfy the new constraints would
  present legacy CVI-composite scores as if they came from the new Sentinel-2/Cloud Score+ pipeline. The specification
  forbids this class of fabrication:
  - When there is no usable observation, the platform states that it is unavailable rather than filling a value in:
    §12.2 acceptance scenario T10, "All-cloud scene yields unavailable/insufficient, never NDVI0". A missing or
    untraceable observation is reported as absent, never substituted.
  - A substitute method must never pass for the primary one: §04.3, "never silently masquerade as the primary method".
  - (Amended 2026-09-27: the first draft also quoted a "§03 W09" line that is not in the specification text
    (`docs/references/6182.md` contains no "W09"). That attribution is removed; the rationale rests on §12.2 T10 and
    §04.3, both verified.)

Legacy `vi_reports` rows stay in the frozen legacy database (`scripts/db/legacy/`, ADR 0004) as historical reference
only. Migrated farms and fields start their /v1 observation history empty. The report counts the rows found (§8) so
operators can see they exist and were excluded on purpose.

### 7. Idempotency key

A second run must be a no-op for everything already migrated. The mechanism is a **persisted id map keyed by the
legacy primary key**. Legacy UUIDs are stable primary keys, so a re-run is a lookup, not a content comparison.

**Where it lives.** It goes in a dedicated schema `legacy_migration`, **not** `app`. Every table in `app` must be
tenant-scoped with forced RLS and primary key `(tenant_id, id)` (`TestEveryTableIsTenantScoped`), and must appear in the
T01 isolation suite. This table is operator bookkeeping, not farmer data. The table is created by a goose migration in
task 3.16:

```sql
CREATE SCHEMA legacy_migration;

CREATE TABLE legacy_migration.id_map (
    source            text        NOT NULL,  -- see the key list below
    legacy_key        text        NOT NULL,  -- legacy UUID as text, or the season key
    tenant_id         uuid        NOT NULL,  -- the farmer's new tenant
    new_table         text,                  -- e.g. 'app.fields'; NULL when outcome = 'skipped'
    new_id            uuid,                  -- NULL when outcome = 'skipped'
    outcome           text        NOT NULL,  -- 'migrated' | 'skipped'
    reason            text,                  -- skip reason code (section 8); on a migrated row only 'identity_pending'
    legacy_created_at timestamptz,           -- legacy created_at / consented_at, for traceability
    run_id            uuid        NOT NULL,  -- the run that last wrote this row
    updated_at        timestamptz NOT NULL,
    CONSTRAINT id_map_pkey PRIMARY KEY (source, legacy_key),
    CONSTRAINT id_map_source_check CHECK (source IN ('farmer_tenant', 'farmer_membership', 'farm', 'farm_field',
                                                     'season', 'season_field', 'crop', 'consent')),
    CONSTRAINT id_map_outcome_check CHECK (outcome IN ('migrated', 'skipped')),
    CONSTRAINT id_map_migrated_has_target CHECK (outcome <> 'migrated' OR (new_table IS NOT NULL AND new_id IS NOT NULL)),
    CONSTRAINT id_map_skipped_has_reason CHECK (outcome <> 'skipped' OR reason IS NOT NULL)
);
```

**Keys.** One map row per new resource:

| `source` | `legacy_key` | New row |
|---|---|---|
| `farmer_tenant` | `farmers.id` | `app.tenants` |
| `farmer_membership` | `farmers.id` | `app.memberships` |
| `farm` | `farms.id` | `app.farms` |
| `farm_field` | `farms.id` | `app.fields` (or `skipped`) |
| `season` | `crops.id` of the crop that anchors the season (§4) | `app.seasons` |
| `season_field` | anchoring `crops.id` + `:` + `farms.id` | `app.season_fields` |
| `crop` | `crops.id` | `app.crop_cycles` (or `skipped`, e.g. `superseded_by_later_cycle`) |

(Amended 2026-09-27: the first draft keyed seasons by `farmers.id:enum:year`, which belonged to the struck-out
calendar windows. Seasons are now anchored by one crop, so the crop's stable legacy id is the key.)

The `farmer_membership` map row of an `identity_pending` farmer (§9.1) has `outcome = 'migrated'` and
`reason = 'identity_pending'`. The existing CHECK constraints allow a reason on a migrated row.
| `consent` | `consents.id` | `app.consents` |

**Run algorithm.**

1. Map rows are written in the **same transaction** as the domain rows they describe (§1: one transaction per
   farmer), so a crash can never leave a created row unmapped or a mapped row uncreated.
2. For each legacy row, look up (`source`, `legacy_key`):
   - `outcome = 'migrated'` → reuse `new_id` and write nothing. For example, the tenant of a migrated farmer is looked
     up to attach newly migratable farms.
   - absent, or `outcome = 'skipped'` → evaluate the row again. On success, write the domain row and set the map row to
     `migrated`. On a skip, insert or update the map row as `skipped` with the current reason.
3. A run in which nothing changed in the legacy data writes no domain row, no audit row and no event. It rewrites no
   map row either: an unchanged `skipped` row is left as it is.
4. A legacy row that disappears after being migrated is never deleted from the new platform. The report lists it as
   `orphaned` (count only).
5. A migrated row is never modified by a later run. In particular:
   - A field's migrated crop cycle stays, even if a newer legacy crop appears later for that farm. The newer crop is
     then open-ended against an existing open-ended cycle, so `CreateCropCycle` refuses it (`ErrOverlap`); it is
     skipped as `overlaps_existing_cycle` and re-evaluated on each run.
   - An `identity_pending` membership is not rebound, even if the farmer's identity becomes confirmable. Such farmers
     are counted as `identity_now_available`; there is no binding mechanism (OQ-7 resolved, risk B7).
6. Every selection is a total order over stable legacy columns, so the same legacy data always produces the same new
   rows on every run:
   - the crop per field (§9.2, ties by OQ-6 as resolved);
   - the irrigation row per farm (§9.4);
   - the processing order (§4).

**Access control.**

- The table holds no farmer PII: no names, phone numbers or geometry. It holds legacy and new ids, reason codes and
  timestamps.
- It is still not readable by the API or worker. `app_runtime` gets **no** `USAGE` on schema `legacy_migration`.
- The tool connects with a dedicated login `app_legacy_migrator`, created by the same migration:
  - member of `app_runtime`, so domain writes run under the same grants and forced RLS as the API;
  - `NOBYPASSRLS`;
  - `USAGE` on `legacy_migration`, plus `SELECT, INSERT, UPDATE` on `legacy_migration.id_map`.
- It is never given to `cmd/api` or `cmd/worker`.
- The legacy database is read with a read-only credential.
- The schema is dropped in the Phase 4 cleanup (plan task 1.24), after the migration is signed off and the legacy
  database is retired.

### 8. Dry-run report shape

`--dry-run` (the default) runs **exactly** the commit code path, per farmer, and rolls back each farmer's transaction
instead of committing. This exercises every constraint, including PostGIS topology and the crop-cycle overlap
exclusion. The commit run produces the same report with "would be" replaced by "was".

The report goes to stdout as a human summary and to `--report <path>` as JSON with this shape. It never contains
names, phone numbers, addresses, coordinates or geometry, only ids, counts and reason codes (§09 logging rules).

```json
{
  "run_id": "uuid",
  "mode": "dry_run | commit",
  "started_at": "RFC 3339", "finished_at": "RFC 3339",
  "legacy_source": { "host": "…", "database": "agri_platform" },
  "farmers":   { "found": 0, "migrated": 0, "already_migrated": 0, "failed": 0,
                 "failed_by_error": { "<error class>": 0 } },
  "identity":  { "confirmed": 0, "identity_pending": 0, "identity_pending_by_cause": {
                   "firebase_uid_missing": 0, "legacy_project_unconfirmed": 0 },
                 "identity_now_available": 0 },
  "tenants":   { "created": 0, "already_present": 0 },
  "memberships": { "created": 0, "already_present": 0 },
  "farms":     { "found": 0, "created": 0, "already_present": 0 },
  "fields":    { "created": 0, "already_present": 0, "skipped": 0,
                 "skipped_by_reason": { "boundary_missing": 0, "geometry_malformed": 0, "geometry_ring_too_short": 0,
                                        "geometry_ring_not_closed": 0, "geometry_position_invalid": 0,
                                        "geometry_too_many_vertices": 0, "geometry_crosses_antimeridian": 0,
                                        "geometry_invalid_topology": 0, "geometry_area_too_small": 0,
                                        "geometry_area_too_large": 0 },
                 "monitoring_enabled": 0, "monitoring_disabled": 0 },
  "seasons":   { "synthesized": 0, "reused": 0,
                 "by_enum": { "kharif": { "synthesized": 0, "reused": 0 }, "rabi": { "…": 0 }, "zaid": { "…": 0 } },
                 "final_status": { "planned": 0, "active": 0, "closed": 0 } },
  "season_fields": { "created": 0, "already_present": 0 },
  "crops":     { "found": 0, "created": 0, "already_present": 0, "skipped": 0,
                 "created_by_status": { "planned": 0, "growing": 0 },
                 "skipped_by_reason": { "field_not_migrated": 0, "crop_name_empty": 0,
                                        "superseded_by_later_cycle": 0, "overlaps_existing_cycle": 0 },
                 "same_sowing_date_ties": 0 },
  "irrigation": { "rows_found": 0, "mapped": { "rainfed": 0, "drip": 0, "sprinkler": 0, "other": 0 },
                  "farms_without_row": 0, "farms_with_multiple_rows": 0 },
  "consents":  { "found": 0, "migrated_granted": 0, "migrated_refused": 0, "already_present": 0,
                 "farmers_without_consent": 0 },
  "not_migrated": { "vi_reports": 0, "farmer_locations": 0, "soil_info": 0, "irrigation_water_source": 0,
                    "farms_with_photo_url": 0, "crops_with_expected_harvest_month": 0,
                    "farmers_with_age_or_gender": 0 },
  "warnings":  { "truncated": 0, "declared_area_mismatch": 0 },
  "orphaned":  { "farmers": 0, "farms": 0, "crops": 0, "consents": 0 },
  "skipped_rows": [ { "source": "farm_field", "legacy_key": "uuid", "reason": "boundary_missing" },
                    { "source": "crop", "legacy_key": "uuid", "reason": "superseded_by_later_cycle",
                      "superseded_by": "uuid of the crop that migrated for that field" } ],
  "flagged_rows": [ { "source": "farmer_membership", "legacy_key": "uuid", "reason": "identity_pending",
                      "cause": "firebase_uid_missing | legacy_project_unconfirmed" } ]
}
```

- **`skipped_rows`** lists every skipped row by `source`, `legacy_key` and `reason`, so an operator can fix the legacy
  data and re-run.
- **`declared_area_mismatch`** counts fields whose PostGIS area differs from the legacy declared area (converted to
  hectares) by more than 25 %. It is informational, never a skip. The 25 % threshold is an engineering choice, fixed
  here.
- **`flagged_rows`** lists migrated rows that need attention but are not skips. Today that is only
  `identity_pending`: the farmer's data was migrated, but nobody can sign in to it yet (§9.1).
  `identity.identity_pending` is its count, kept separate from every skip reason because it needs visibility before
  pilot go-live (see Consequences).
- **`superseded_by_later_cycle`** entries always name the crop that superseded them (`superseded_by`), so no earlier
  crop disappears silently (§9.2).
- **`overlaps_existing_cycle`** can occur only on a re-run, for a legacy crop added after its field's cycle was
  migrated (§7, run algorithm step 5).
- **`outside_season`** (first draft) is gone: derived windows contain their sowing date by construction (§4).
- **`same_sowing_date_ties`** counts fields where two or more crops share the latest sowing date (resolved by OQ-6).
- **Exit code:** 0 when `farmers.failed == 0`; 1 otherwise. Skips and `identity_pending` never change the exit code.

### 9. Resolutions of the first draft's open questions (2026-09-27)

The first draft ended with four open questions. All four are resolved; the rules are applied in the sections cited.

#### 9.1 OQ-1 resolved — farmers without a confirmable identity are migrated data-only

- **Problem (was OQ-1).** `memberships.user_id` must equal what `auth.DerivedResolver` computes from the identity
  provider's issuer and subject (§09.3). Legacy `farmers.firebase_uid` is nullable, and even where present it is not
  established that it belongs to the Firebase project the new platform uses.
- **When identity counts as confirmed.** Only when both hold:
  - `firebase_uid` is not NULL;
  - the operator runs the tool with `--legacy-firebase-project=<id>`, and `<id>` equals the platform's
    `FIREBASE_PROJECT_ID`. This asserts that the legacy UIDs were issued by the same project.

  Without the flag, no farmer is confirmed. A flag value that differs from `FIREBASE_PROJECT_ID` is a configuration
  error: the tool exits before any write, because such UIDs can never match a sign-in.
- **Confirmed farmers:** `user_id` = `DerivedResolver(issuer, firebase_uid)`, membership `status active`, as in §2.1.
- **All other farmers: migrated data-only.**
  - The tenant, membership, farms, fields, seasons, crop cycles and consent are created exactly as for any other
    farmer.
  - The membership is created with `status suspended`.
  - `user_id` is a deterministic placeholder: UUIDv5 over `"farmer:" + farmers.id` in the tool's own fixed namespace
    UUID. That constant is defined once in the tool and never changed, and it differs from `DerivedResolver`'s
    namespace. A placeholder therefore can never equal a real user's derived id, and a re-run recomputes the same
    placeholder (§7).
  - Every row that records a user (`farms.owner_user_id`, `field_boundaries.created_by`, `consents.user_id`) carries the
    same placeholder.
- **Why `suspended`, and no new status.** The membership status enum has exactly two values: `status IN ('active',
  'suspended')` (migration 00003, constraint `memberships_status_enum`; approved decision A9: "revoked" means
  suspended). `auth.LoadPrincipal` refuses every status other than `active` with `ErrSuspended` (403), on every
  request. `suspended` is therefore precisely "the record exists but cannot act", and no new value is needed. What
  distinguishes a pending identity from a revoked one is the id-map reason `identity_pending`, not the status.
- **Reporting.** The farmer counts under `identity.identity_pending` (with its cause) and appears in `flagged_rows`
  with reason `identity_pending` (§8). It is **not** a skip: all its data is migrated.
- **Rationale.** Skipping these farmers would leave their data behind. Pre-creating identity-provider accounts would be
  an account-creation and privacy decision this task cannot make. Data-only migration loses nothing and grants access
  to nobody who has not proved an identity.
- **Permanence (OQ-7 resolved).** This path is confirmed and accepted, and the placeholder is permanent: nothing in the
  platform can later repoint it to a real `user_id`. That is an accepted risk, recorded as **B7** in
  `docs/platform/STATUS.md`; see there for the failure mode.

#### 9.2 OQ-2 resolved — one open cycle per field; earlier crops are superseded, never given invented dates

- **Problem (was OQ-2).** Legacy crops have no status and no harvest date. Open-ended cycles on one field always
  violate `crop_cycles_no_overlap`.
- **Rule.**
  - Per (tenant, field), only the crop with the **latest `sowing_date`** migrates as a crop cycle.
  - Every earlier crop on that field is skipped with reason `superseded_by_later_cycle`. Its id-map row and its
    `skipped_rows` entry name the superseding crop (`superseded_by`), so it is reported, not silently dropped.
  - Ties on the latest `sowing_date`: the tied crop with the latest `crops.created_at` wins, then the lexically greatest
    `crops.id` (OQ-6, resolved).
- **No fabricated certainty.** No `harvest_date` is derived: not from `expected_harvest_month`, not from the season end.
  No cycle is given `harvested`. Inventing an end the source data does not have is the same fabrication pattern
  Decision 1 forbids for observations.
- **Status: `planned`, then `growing` when already sown.**
  - `seasons.Service.CreateCropCycle` accepts only one initial status. Its code: "if c.Status != CyclePlanned { return
    invalid(\"/status\", \"invalid_initial_status\", \"A crop cycle is created as planned.\") }". So every migrated
    cycle is created `planned`.
  - When `sowing_date` ≤ the run date, the crop is in the ground, so the tool moves it `planned`→`growing` with
    `UpdateCropCycle` in the same transaction, audited like any transition. `cycleTransition` allows exactly that edge:
    `from == CyclePlanned && (to == CycleGrowing || to == CycleFailed)`.
  - `validateCycle` requires a harvest date only for `harvested` (`c.Status == CycleHarvested && c.HarvestDate == nil`
    is rejected), so neither `planned` nor `growing` needs one.
  - A cycle whose `sowing_date` is after the run date stays `planned`.
- **Rationale.** One open-ended cycle per field satisfies the overlap exclusion without inventing dates. The most
  recent crop is the one that matters for monitoring now. Earlier crops remain in the frozen legacy database, and every
  one of them is listed by id in the report.

#### 9.3 OQ-3 resolved — season windows are derived from the sowing date

The fixed calendar windows of Decision 3 are struck out and replaced (§4). Each window is
`[sowing_date − 30 days, sowing_date + 210 days]`, so it contains its sowing date by construction. The enum survives as
the season label. The rationale (§14 `Season.name`, "user-defined, not fixed to hemisphere") is in §4.

#### 9.4 OQ-4 resolved — several irrigation rows per farm: deterministic selection

- **Problem (was OQ-4).** The legacy `irrigation` table has no UNIQUE on `farm_id`, so a farm may have several rows.
- **Rule: the greatest `id` wins.** For every farm with more than one `irrigation` row, the row with the lexically
  greatest `id` is selected. The comparison is on the canonical lower-case UUID text; it equals PostgreSQL's `uuid`
  ordering, so `ORDER BY id DESC` selects the same row.
- **Correction (OQ-5 resolved, 2026-09-27).** The first wording of this rule, "most recent row by `created_at`, ties
  broken by the greatest `id`", was misleading. The legacy `irrigation` table has **no `created_at` column at all**
  (its columns are `id`, `farm_id`, `irrigation_type`, `water_source`). Every row ties on the absent timestamp, so in
  practice the rule is simply "greatest `id` wins". Legacy ids come from `gen_random_uuid()`, so the choice is
  deterministic but carries no notion of recency.
- **Why determinism is required.** The acceptance criterion of task 3.16 is an idempotent run. A selection that could
  differ between runs would give the same field a different `irrigation_method` depending on read order.
- **Reporting.** Farms with more than one row count under `irrigation.farms_with_multiple_rows` (§8).

## Consequences

- **What the tool builds against.** Task 3.16 implements `tools/migrate-legacy` against this table set. Every open
  question of this ADR is resolved (§9 and the resolved list at the end).
- **`identity_pending` needs a decision before pilot go-live.** Every `identity_pending` farmer has their data in the
  new platform, but nobody can sign in to it, and the placeholder identity is permanent absent a manual repair
  migration (B7). The `identity.identity_pending` count (with its cause breakdown) must be reviewed before pilot
  go-live, so product and support can decide whether and how to contact those farmers.
- **Crop history.** Only one crop cycle per field is migrated. Earlier legacy crops stay in the frozen legacy database
  and are listed by id in the report (`superseded_by_later_cycle`).
- **Observation history.** Migrated tenants start with an empty observation history. The first real analysis job
  (task 2.9) produces their first observations.
- **Crop codes.** `crop_code` values are the legacy free-text crop names. The contract describes `crop_code` as a
  "Versioned crop catalog code"; when a catalog exists, migrated values will need mapping onto it, which is a
  follow-up for that task, not this one.
- **Data left behind.** Everything marked "Not migrated" stays readable only in the frozen legacy database until its
  retirement (ADR 0004). After that it is gone, as B6 records for onboarding.
- **Legacy consent.** The legacy application keeps writing its own `consents` table while it runs. A consent change
  in legacy after a farmer is migrated is not synchronised; the migrated `app.consents` row is authoritative from
  migration onward.

## Open questions — all resolved (2026-09-27)

OQ-1–OQ-4 of the first draft are resolved in §9. OQ-5–OQ-7 surfaced while applying those resolutions and are resolved
below. No open question remains in this ADR.

- **OQ-5 — Resolved (factual correction).** The "most recent `created_at`" framing of the irrigation rule was
  misleading: the legacy `irrigation` table has no `created_at` column, so every row ties and the rule is, in practice,
  "greatest `id` wins" for every farm with more than one row. §9.4 now states the rule that way. Farms concerned are
  counted in `irrigation.farms_with_multiple_rows`.
- **OQ-6 — Resolved as proposed.** When two or more crops share the latest `sowing_date` on one field, the tied crop
  with the latest `crops.created_at` migrates; a remaining tie goes to the lexically greatest `crops.id`. The others
  are skipped `superseded_by_later_cycle`, naming it, and the field counts in `crops.same_sowing_date_ties`.
- **OQ-7 — Resolved: the placeholder identity is permanent.**
  - **Accepted, not deferred.** The data-only migration path of §9.1 (membership `status suspended`, deterministic
    placeholder `user_id`) is confirmed and accepted. This is not "identity resolution deferred".
  - **Where the placeholder lands.** Once written, it sits in `memberships.user_id`, `farms.owner_user_id`,
    `field_boundaries.created_by` and `consents.user_id`. (`app.fields` has no `created_by` column; a field's creator
    is recorded on its boundary.)
  - **No way to repoint it.** There is **no mechanism anywhere in the current platform** to repoint the placeholder to
    a real `user_id`. `user_id` is not an updatable field on these rows: `tenancy.Team.UpdateMember` and the team
    store's `UpdateMember` do not write it, and `memberships_user_unique` binds the row to it.
  - **Permanence.** It is **permanent unless a future one-off manual data-repair migration is written and run against
    these specific rows.**
  - **Re-runs.** A re-run never modifies an existing `identity_pending` membership (§7, step 5); farmers whose identity
    became confirmable are only counted (`identity_now_available`).
  - **Tracked as:** accepted risk **B7** in `docs/platform/STATUS.md`.
