# Team Work Division — Global Farmer Platform P0

| | |
|---|---|
| Source spec | `6182.docx` — *Global Farmer Platform, Complete Product and Development Specification* v1.0.0 (16 Sep 2026) |
| Baseline audited | `main` @ `000d2da`, 17 Sep 2026 |
| Team | 6 engineers, full time |
| Cadence | 2-week sprints, 12 sprints (~24 weeks) to a 20-farm pilot |
| Scope | **P0 only**: PR-01 – PR-12, PR-25 – PR-27 |
| Cloud | **Last.** Everything runs on the local stack until Phase 5 |

Spec references in this document use the spec's own IDs: chapters (`§04`), requirements (`PR-05`), workflows (`W09`) and acceptance scenarios (`T10`).

---

## Contents

1. [Where we are: codebase audit](#1-where-we-are-codebase-audit)
2. [Ground rules](#2-ground-rules)
3. [Local stack (replaces the cloud until Phase 5)](#3-local-stack-replaces-the-cloud-until-phase-5)
4. [Team and ownership](#4-team-and-ownership)
5. [Phase plan](#5-phase-plan)
6. [Sprint board](#6-sprint-board)
7. [Detailed work by person](#7-detailed-work-by-person)
8. [Handoffs between people](#8-handoffs-between-people)
9. [Acceptance scenarios by owner](#9-acceptance-scenarios-by-owner)
10. [Definition of done](#10-definition-of-done)
11. [Working agreements](#11-working-agreements)
12. [Risks](#12-risks)
13. [After the pilot](#13-after-the-pilot)

---

## 1. Where we are: codebase audit

All 11 tested Go packages pass. The code is a well-built prototype of **one analysis screen plus onboarding**. The spec describes a multi-tenant platform. Roughly **10–15% of P0 is done**, and the done part (Earth Engine from Go) is the spec's biggest technical risk.

### 1.1 Keep and build on

| Area | Location | Size | Why it carries over |
|---|---|---|---|
| Earth Engine expression builder | `internal/gee/eeexpr` | 1.1k lines + fixtures | Solves "Go EE REST expression proof" (§02.7 gate, §04.1) |
| Analysis pipeline | `internal/pipeline` | 1.7k lines | Sentinel-2/Sentinel-1 collections, index math, grid, stats |
| Earth Engine client and session | `internal/gee` | 670 lines | Auth, paging, retry on 429/5xx only, token refresh fixed |
| Polygon validation | `internal/geo` | 200 lines, tested | Basis for T08 |
| Middleware | `internal/httpapi/middleware` | tested | Rate limit, body cap, in-flight cap, request IDs |
| Config pattern | `internal/config` | tested | Single tuning surface stays |
| Chatbot | `internal/chatbot`, `internal/gemini` | prototype | Basis for PR-17 after the pilot |
| Frontend pieces | `HeatmapLayer.jsx`, `Legend.jsx`, `colorUtils.js`, `pages/steps/*` | — | UX reference to port into Next.js |

### 1.2 Gaps against the spec

| Area | Today | Spec requires |
|---|---|---|
| Process model | One Gin server; EE analysis runs inside the HTTP request (300 s write timeout) | `cmd/api`, `cmd/worker`, `cmd/tile`; SQL jobs; outbox; no work after the response (§02.4–5) |
| Persistence of results | **None.** `vi_reports` is never written (AUDIT L3) | Immutable observations + latest projection (§04.3, §07.4) |
| Database | 8 farmer-centric tables; `schema.sql` and `mindstrix_setup.sql` disagree; no migration runner (AUDIT M4); M2 open | ~43 tables, tenant-scoped, RLS FORCE (§07, §17, §18) |
| Identity | Phone OTP + custom JWT + Werkzeug hashes | Identity Platform tokens; memberships, roles, field grants (§09) |
| API | 24 unversioned routes; 3 error envelopes; `/api/sample` global slot (AUDIT H7) | 104 `/v1` endpoints; problem+json; ETag; Idempotency-Key; signed cursors (§06.2–3, §15) |
| Science | SCL mask; NDVI/EVI/SAVI/NDMI/NDWI/GNDVI/CVI; mean + std only; Gaussian-smoothed grid | Cloud Score+; NDVI/NDMI/NDRE/RECI/MSAVI/EVI at native resolution; valid fraction, p10/p50/p90; COG + tile gateway (§04) |
| Tests | 0 tests in `repo`, `db`, `firebase`, `firestore`, `gemini`, `jwtutil`, `cmd` | SQL integration, isolation, E2E, performance (§12.1) |
| Frontend | Vite + React + Leaflet, 5.9k lines | Next.js `output: 'export'`, 17 routes, offline scouting (§08) |
| Not started | — | Import, seasons/crop cycles, weather, alerts, scouting, activities, reports, notifications, entitlements, privacy, audit |
| DevOps | Dockerfile only; no CI; JSON key file | CI, migrations, Terraform, WIF (Phase 5) |

---

## 2. Ground rules

1. **The frozen-contract rule in `CLAUDE.md` is lifted.** The new `/v1` API and `apps/web` are built alongside the legacy app. The legacy app keeps running as a reference and is deleted at the end of Phase 4.
2. **P0 only.** Anything in §13 of this document waits for the pilot.
3. **Cloud last.** No one provisions or depends on GCP before Phase 5. Every cloud service sits behind a Go interface with a local implementation (§3).
4. **Contract first.** `contracts/openapi.json` is frozen at the end of Sprint 2. Frontend builds against the mock server until endpoints land.
5. **Earth Engine and Gemini are called live** from dev machines (they are external APIs, not our infrastructure). Every new EE call gets a recorded fixture.
6. **Owners decide inside their folders.** Cross-folder changes need the other owner's review (CODEOWNERS).

---

## 3. Local stack (replaces the cloud until Phase 5)

Owned by **P1**. Ready by the end of Sprint 1. `docker compose up` must start everything.

| Spec component (Phase 5) | Local implementation | Go interface |
|---|---|---|
| Cloud SQL PostgreSQL + PostGIS | `postgis/postgis` container | `pgxpool` (unchanged) |
| Memorystore Redis | `redis` container | `cache.Store` |
| Cloud Storage (quarantine / ready buckets) | MinIO or `fake-gcs-server` | `storage.Bucket` |
| Pub/Sub + Cloud Tasks | `jobs` table + in-process dispatcher | `queue.Dispatcher` |
| Identity Platform | Firebase Auth emulator | `auth.Verifier` |
| Secret Manager | `.env` | `config` |
| Google Weather API | Open-Meteo adapter | `weather.Provider` |
| Cloud Logging / Trace | stdout slog + local OTel collector (optional) | `telemetry` |

Rule: **no domain package imports a concrete adapter.** Phase 5 swaps implementations without touching domain code.

---

## 4. Team and ownership

| ID | Role | Primary requirements | Owns (CODEOWNERS) |
|---|---|---|---|
| **P1** | Tech lead / platform backend | PR-01, PR-27 (platform parts) | `cmd/api`, `internal/platform/**`, `internal/domain/{tenancy,identity,audit}`, `internal/adapters/{postgres,redis,storage,queue}`, `migrations/`, `contracts/`, `docker-compose.yml`, `AGENTS.md` |
| **P2** | Geospatial engineer | PR-05, PR-06 (data), PR-08 (detection) | `internal/gee/**`, `internal/pipeline/**`, `internal/domain/observations`, `cmd/worker/analysis`, `cmd/tile` |
| **P3** | Backend — fields and farm data | PR-02, PR-03, PR-04, onboarding, legacy data | `internal/domain/{farms,fields,seasons,imports,soil,consent}`, `tools/migrate-legacy` |
| **P4** | Backend — operational workflows | PR-07, PR-08 (lifecycle), PR-09, PR-10, PR-11, PR-12, PR-25, PR-26 | `internal/domain/{weather,alerts,scouting,activities,reports,notifications,usage,privacy}`, `internal/adapters/weather` |
| **P5** | Frontend lead | PR-06 UI, UI for PR-01 – PR-08 | `apps/web/**` except the folders owned by P6 |
| **P6** | Frontend + QA/DevEx, **cloud lead in Phase 5** | UI for PR-09 – PR-12, PR-26; PR-27 (release, cloud) | `apps/web/src/features/{scouting,activities,reports,settings,privacy}`, `apps/web/src/offline`, `tests/**`, `.github/**`, `infra/**` |

**Tie-breaks:** P1 decides architecture and contract questions. P2 decides scientific method questions. The whole team decides scope changes in sprint review.

---

## 5. Phase plan

| Phase | Sprints | Weeks | Goal | Exit gate (all must pass) |
|---|---|---|---|---|
| **0 — Foundation** | S1 | 1–2 | New layout, local stack, contract draft, science proof | `docker compose up` green; CI running; Cloud Score+ fixture passes; old/new table map approved |
| **1 — Platform core** | S2–S3 | 3–6 | Tenancy, identity, RLS, fields, jobs framework | T01, T02, T03, T08 pass; OpenAPI frozen (end S2); field created via `/v1` from the new UI |
| **2 — Monitoring** | S4–S6 | 7–12 | Observations, maps, seasons, import, weather, alerts | T05, T09, T10–T14 pass; 1,000-field local benchmark; field detail shows persisted data |
| **3 — Workflows** | S7–S9 | 13–18 | Scouting (offline), activities, reports, notifications, entitlements, privacy | T15–T18, T20, T25, T30 pass; W01–W16, W21, W23, W24, W28 demoed end to end |
| **4 — Hardening** | S10 | 19–20 | Security, accessibility, performance, legacy migration, legacy removal | All P0 T-scenarios green locally; legacy data migrated twice on a copy; `frontend/` and legacy routes deleted |
| **5 — Cloud and pilot** | S11–S12 | 21–24 | Terraform, CI/CD, staging, production, DR, pilot | Staging and production live; restore drill passed; T26–T29 pass in staging; 20 pilot farms onboarded |

**Critical path:** OpenAPI + tenancy/RLS (P1, S2) → fields (P3, S2–S3) → observation jobs (P2, S4–S5) → map & alerts (P5/P4, S5–S6) → scouting & activities (P4/P6, S7–S8) → cloud (P6/P1, S11–S12).

---

## 6. Sprint board

| Sprint | P1 Platform | P2 Geospatial | P3 Fields | P4 Workflows | P5 Frontend | P6 Frontend + QA |
|---|---|---|---|---|---|---|
| **S1** (wk 1–2) | Repo layout, local stack, `AGENTS.md`, OpenAPI draft | Cloud Score+ proof, fixtures, index spec | Legacy → new table map | Weather adapter (Open-Meteo), alert rule spec | Next.js static shell, routes, tokens | CI, test harness, isolation suite skeleton |
| **S2** (wk 3–4) | Tenancy migrations, RLS, auth verifier, tx pattern. **OpenAPI frozen** | NDRE/RECI/MSAVI, 20 m handling, per-field stats | Farms, fields, boundary versioning | Weather storage and field bindings | API client from OpenAPI, sign-in, tenant switch | T01/T02 tests, fill untested legacy packages |
| **S3** (wk 5–6) | Idempotency, ETag, cursors, audit, outbox, jobs + leases | Quality classes (usable/partial/insufficient) | Field groups, archive, field API complete | Entitlements & usage tables | Field list, MapLibre, draw/edit | T03/T08 tests, E2E: sign-in → field |
| **S4** (wk 7–8) | Queue dispatcher, storage adapter, reaper | Pipeline in worker jobs, EE adapter ops | Seasons, crop cycles, overlap lock | Admission checks before costly work | Scene timeline, index chart | E2E harness vs exported build |
| **S5** (wk 9–10) | Membership & invitation API | COG export, manifests, observations, latest projection | Import: upload, dry-run | Alert engine: episodes, dedupe, data-gap | Field detail, map tiles, quality/source panel | T09/T10/T12 tests, benchmark harness |
| **S6** (wk 11–12) | Contract review, security review of S1–S5 | Tile gateway, change detection, **1,000-field benchmark** | Import commit, resume, dedupe | Alert triage, acknowledgement | Home work list, alerts, weather, compare dates | T11/T13/T14 tests, import wizard UI |
| **S7** (wk 13–14) | Audit queries, admin endpoints | Processing versions, reprocessing rules | Soil tests, consent records | Scout tasks, inspections | Team & invitations UI | Offline storage (IndexedDB), sync queue |
| **S8** (wk 15–16) | Privacy job framework | Backfill limits, numeric goldens | New onboarding flow API | Offline sync API, activities & costs | Onboarding UI on new API | Scouting UI, conflict screen, activities UI |
| **S9** (wk 17–18) | Retention jobs, cursor hardening | Tune profiles, cost accounting | Legacy migration script v1 | Reports worker, notifications, privacy export/erase | Accessibility pass, English/Hindi | Reports & settings UI, T15–T18/T20 tests |
| **S10** (wk 19–20) | Security fixes, final contract, remove legacy routes | Science sign-off, docs | Legacy migration rehearsal ×2 | Bug fixes, T25/T30 | Performance, delete `frontend/` | Full regression, local load test, release checklist |
| **S11** (wk 21–22) | Swap adapters to Cloud SQL/Tasks/GCS/Identity Platform | EE service account & quota verification in staging | Migrate legacy data into staging | Google Weather adapter in staging | Firebase Hosting config, CSP headers | **Terraform staging**, WIF, CI/CD deploy, monitoring |
| **S12** (wk 23–24) | Production readiness review | Production data-quality check | Pilot farm onboarding support | Notification provider in production | Pilot UI fixes | **Terraform production**, restore drill, T26–T29, pilot rollout |

---

## 7. Detailed work by person

Each task lists **what**, **where**, **done when** and **spec**.

### P1 — Tech lead / platform backend

**Mission:** everyone else builds on your contract, transaction pattern and adapters. In S1–S2 you do nothing else.

#### Phase 0 (S1)
| # | Task | Where | Done when | Spec |
|---|---|---|---|---|
| 1.1 | New repository layout; keep legacy under `cmd/server` + `internal/httpapi` until S10 | `cmd/{api,worker,tile}`, `internal/{platform,domain,adapters}` | `go build ./...` passes; legacy `make verify` still passes | §06.1 |
| 1.2 | Choose and pin `chi`, `goose`, `sqlc`; record as ADRs | `docs/adr/` | ADR merged | §06.1, §13 |
| 1.3 | Local stack | `docker-compose.yml` | One command starts PostGIS, Redis, MinIO, Firebase emulator, API, worker | §3 of this doc |
| 1.4 | `AGENTS.md` rules for Antigravity | repo root | Merged; every engineer has read it | §11 of this doc |
| 1.5 | OpenAPI draft for PR-01 – PR-12, PR-25 – PR-27 resources from spec §14 and §15 | `contracts/openapi.json` | Validates; mock server (Prism) runs | §06.2, §14, §15 |
| 1.6 | Decide the fate of `schema.sql` vs `mindstrix_setup.sql` | `docs/adr/` | ADR merged | AUDIT M4 |

#### Phase 1 (S2–S3)
| # | Task | Where | Done when | Spec |
|---|---|---|---|---|
| 1.7 | Migrations: `tenants`, `memberships`, `invitations`, `membership_field_grants`, `authorization_revisions`, `audit_records`, `outbox`, `inbox`, `idempotency_records`, `jobs`, `job_execution` | `migrations/` | Up/down from empty DB in CI | §17, §18 |
| 1.8 | RLS: `ENABLE` + `FORCE` on tenant tables; runtime role without BYPASSRLS | `migrations/` | T01 isolation suite passes | §07.3 |
| 1.9 | Token verifier (Firebase emulator locally) and principal resolution | `internal/platform/auth` | Invalid → 401; suspended member → 403 | §09.3, W01 |
| 1.10 | Transaction helper: `set_config('app.tenant_id', …, true)` + actor | `internal/platform/db` | No handler can query without it; test proves pooled connection does not leak tenant | §06.6 |
| 1.11 | problem+json errors, request ID, body cap (reuse middleware) | `internal/platform/http` | All `/v1` errors match schema | §06.2 |
| 1.12 | **Freeze OpenAPI** (end S2) | `contracts/` | Tagged `contract-v1.0.0-rc1` | §06.2 |
| 1.13 | Idempotency-Key reservation in-transaction | `internal/platform/idempotency` | T03, T04 pass | §06.3 |
| 1.14 | ETag / If-Match, version increment | `internal/platform/http` | Stale If-Match → 412 | §06.2 |
| 1.15 | HMAC-signed keyset cursors | `internal/platform/pagination` | Revocation invalidates cursor | §06.2 |
| 1.16 | Audit + outbox rows written in the same transaction | `internal/domain/audit` | Every write endpoint emits both | §02.4 |
| 1.17 | Jobs with SQL leases and fence tokens | `internal/platform/jobs` | Only current lease holder can publish | §02.5 |

#### Phase 2–3 (S4–S9)
| # | Task | Done when | Spec |
|---|---|---|---|
| 1.18 | `queue.Dispatcher` local implementation + reaper | Killed worker's job is re-dispatched once (T07) | §02.5 |
| 1.19 | `storage.Bucket` with quarantine/ready separation | Upload cannot reach ready without validation (T17 groundwork) | §07.6 |
| 1.20 | Memberships, invitations, field-grant API | W02, W03 demoed; T02 passes | PR-01 |
| 1.21 | Security review of every domain package merged in S1–S5 | Findings filed and closed | §09 |
| 1.22 | Privacy job framework (used by P4) | Erasure job plan persisted and resumable | §07.7 |
| 1.23 | Retention jobs (idempotency 24 h, inbox 30 d, logs policy) | Jobs run and are tested | §07.7 |

#### Phase 4–5 (S10–S12)
| # | Task | Done when |
|---|---|---|
| 1.24 | Remove legacy routes, `internal/httpapi`, `cmd/server` | Build green without them |
| 1.25 | Swap adapters to Cloud SQL, Cloud Tasks, Pub/Sub, GCS, Identity Platform (with P6) | Staging runs the same test suite |
| 1.26 | Production readiness review | Release checklist signed |

---

### P2 — Geospatial engineer

**Mission:** turn the synchronous heatmap prototype into a job-based, provenance-tracked observation pipeline that never reports missing data as healthy.

#### Phase 0 (S1)
| # | Task | Where | Done when | Spec |
|---|---|---|---|---|
| 2.1 | Cloud Score+ linking proof (`GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED`, `cs_cdf ≥ 0.60`) | `internal/pipeline/sentinel2.go`, `eeexpr/testdata` | Fixture captured; live test under `GEE_LIVE_TEST=1` passes | §04.2 |
| 2.2 | Rename `MaskCloudsSCL` path to an explicitly labelled degraded fallback | `internal/pipeline` | Output carries `mask_method` | §04.3 step 5 |
| 2.3 | Write the index registry as config | `internal/config` | Matches §04.4 table exactly | §04.4 |

#### Phase 1 (S2–S3)
| # | Task | Done when | Spec |
|---|---|---|---|
| 2.4 | Add NDRE, RECI, MSAVI; keep NDVI, NDMI, EVI; drop CVI/SAVI/NDWI/GNDVI from `/v1` | Formula tests with scaled reflectance (T12) | §04.4 |
| 2.5 | Aggregate N to 20 m for NDMI; red-edge indices on 20 m grid | Effective resolution stored per result (T11) | §04.3 step 7 |
| 2.6 | Denominator epsilon 1e-6; invalid → masked, never Inf/0 | T10 unit test: all-cloud → insufficient | §04.4 |
| 2.7 | Per-field reducer: valid area fraction, pixel count, area-weighted mean, p10/p50/p90, population std | Golden values for the 5 existing numeric fixture polygons | §04.3 step 8 |
| 2.8 | Quality classes: usable (≥0.70, ≥20 px), partial (≥0.30, ≥5 px), insufficient | Classes returned on every observation | §04.5 |

#### Phase 2 (S4–S6)
| # | Task | Done when | Spec |
|---|---|---|---|
| 2.9 | Move analysis out of HTTP into worker jobs (`AnalysisRequest` → 202 + job) | No EE call on the request path | §02.4, W09 |
| 2.10 | EE adapter: `DiscoverScenes`, `SubmitStatistics`, `SubmitRasterExport`, `GetOperation`, `CancelOperation` | Each has recorded fixtures incl. 429/5xx/timeout | §04.1 |
| 2.11 | Persist EE operation names; reconcile uncertain submissions | T05 passes | §02.5 |
| 2.12 | COG export to `storage.Bucket` with overviews, CRS, no-data mask, checksum, manifest | Manifest validated before publish | §04.3 step 9 |
| 2.13 | `observations` (immutable) + latest-observation projection (with P3 for FKs) | Boundary edit mid-job does not update current projection (T09) | §04.3 step 10 |
| 2.14 | Tile gateway: grant check per request, COG range reads, cache key tenant+digest+style+z/x/y | Revoked user gets 404 on next tile | §02.6 |
| 2.15 | Change detection on common valid pixels (ΔNDVI ≥ 0.15, gap 3–30 d, common valid ≥ 0.70) → events for P4 | T13 passes | §04.5 |
| 2.16 | Batching by tile/time window, concurrency 2, adaptive split | **1,000-field local benchmark** report | §04.7 |

#### Phase 3–5 (S7–S12)
| # | Task | Done when |
|---|---|---|
| 2.17 | `processing_version` = graph digest + profile; reprocessing rules | Two profiles coexist without collision |
| 2.18 | Historical backfill limits separate from fresh scenes | Backfill cannot starve fresh processing |
| 2.19 | Retire `smooth.go` from `/v1` (resampling is not new detail) | Maps show real rasters only |
| 2.20 | Science documentation and sign-off | Index registry, quality policy, known limitations documented |
| 2.21 | S11: verify EE service account and batch quota in staging (with P6) | Benchmark rerun in staging |

---

### P3 — Backend: fields and farm data

**Mission:** permanent field identity, versioned boundaries, seasons and import — and move the existing farmers' data safely.

#### Phase 0 (S1)
| # | Task | Done when | Spec |
|---|---|---|---|
| 3.1 | Map legacy tables (`farmers`, `farmer_locations`, `farms`, `crops`, `irrigation`, `soil_info`, `consents`, `vi_reports`) to spec tables | Mapping doc approved by P1 | §17 |
| 3.2 | Geometry fixture set: self-intersection, bad holes, swapped coords, antimeridian, >10,000 vertices, <0.01 ha, >20,000 ha | Fixtures committed | T08, §04.3 step 2 |

#### Phase 1 (S2–S3)
| # | Task | Done when | Spec |
|---|---|---|---|
| 3.3 | Migrations: `farms`, `fields`, `field_boundaries`, `field_groups`, `group_fields` | With tenant FKs and GiST index | §17, §18 |
| 3.4 | Field create/edit: PostGIS validation, geodesic area (holes excluded), boundary row appended in the same transaction | Client-supplied area rejected | §07.2, W04, W06 |
| 3.5 | Reuse `internal/geo` checks before PostGIS conversion | T08 passes with precise errors | T08 |
| 3.6 | Unique active field name within farm; archive flow | W07 demoed | PR-02 |
| 3.7 | Field groups CRUD | Grant filter respected | PR-02 |

#### Phase 2 (S4–S6)
| # | Task | Done when | Spec |
|---|---|---|---|
| 3.8 | `seasons`, `season_fields`, `crop_cycles`; lock (tenant, field) for overlap checks | Overlapping same-field cycles rejected under concurrency test | §07.2, W08, PR-04 |
| 3.9 | Import upload via `storage.Bucket` grant; archive limits (100 MiB, 500 MiB extracted, 10,000 entries, traversal/symlink rejection) | Malicious archive fixtures rejected | §06.4 |
| 3.10 | Parsers: GeoJSON, KML, KMZ, SHP (zipped); reject ambiguous CRS | Per-format fixtures | W05 |
| 3.11 | Dry-run with per-row results and column mapping | UI can show every row outcome | PR-03 |
| 3.12 | Commit: resumable, deduplicated by normalized geometry hash | Re-running commit creates no duplicates | PR-03 |

#### Phase 3–5 (S7–S12)
| # | Task | Done when | Spec |
|---|---|---|---|
| 3.13 | `soil_tests` with method, depth, date, units, source | W17 data path works (feeds onboarding) | PR-13 data |
| 3.14 | Consent records per purpose | Consent withdrawal blocks monitoring | §05 commercial |
| 3.15 | New onboarding API replacing the 9 legacy steps | Frontend onboarding runs on `/v1` | — |
| 3.16 | `tools/migrate-legacy`: farmers → users/memberships, farms → farms/fields, crops → crop cycles | Dry-run report + idempotent run | — |
| 3.17 | S10: rehearse migration twice on a copy of the live DB | Row counts and spot checks signed off |
| 3.18 | S11–S12: migrate into staging, then production; support pilot onboarding | Pilot farms visible with history |

---

### P4 — Backend: operational workflows

**Mission:** turn observations into action: weather, alerts, scouting, activities, reports, notifications — plus the commercial and privacy controls.

#### Phase 0–1 (S1–S3)
| # | Task | Done when | Spec |
|---|---|---|---|
| 4.1 | `weather.Provider` interface; Open-Meteo implementation (provider, issue time, valid interval, units, attribution) | Adapter fixtures incl. 429/5xx/timeout | §06.5, PR-07 |
| 4.2 | Alert rule specification document with P2 (thresholds from §04.5, suppression reasons) | Approved | PR-08 |
| 4.3 | `weather_samples` storage + field-grid binding (no per-field copies of identical data) | T14 passes (timezone/DST) | §07.4, W11 |
| 4.4 | `entitlements`, `usage_buckets`, `usage_ledger` | Plan limits stored and versioned | PR-25 |

#### Phase 2 (S4–S6)
| # | Task | Done when | Spec |
|---|---|---|---|
| 4.5 | Atomic admission check before costly work (analysis, report) | Over-limit → rejected before job creation | PR-25, W28 |
| 4.6 | `alerts`: episodes, dedupe, severity, evidence date, factual reason | Duplicate events do not create a second episode (T06) | W12 |
| 4.7 | Data-gap alerts: "no new image" ≠ "processing failed" | T30 passes | PR-08 |
| 4.8 | Alert triage: acknowledge, dismiss with reason code (`false_positive`), convert to scout task | W13 demoed | W13 |

#### Phase 3 (S7–S9)
| # | Task | Done when | Spec |
|---|---|---|---|
| 4.9 | `scout_tasks`, `inspections` with state machine | W14 demoed | §03 state tables |
| 4.10 | Offline sync endpoint: `offline_operations`, operation ID dedupe, base_version conflicts | T15, T16 pass | W15 |
| 4.11 | Photo evidence via quarantine → validated → ready | T17 passes | §06.4 |
| 4.12 | `activities`: planned vs actual dates, costs in integer minor units, no mixed currency totals | T18 passes | W16, PR-10 |
| 4.13 | `reports` worker: CSV and PDF, snapshot cutoff, reauthorize on download | T20 passes | W21, PR-11 |
| 4.14 | `notification_preferences`, `notifications`, `delivery_attempts`; quiet hours; unknown-outcome state | W23 demoed | PR-12 |
| 4.15 | `privacy_requests`: export and erasure using P1's job framework | W24 demoed | PR-26 |

#### Phase 4–5 (S10–S12)
| # | Task | Done when |
|---|---|---|
| 4.16 | T25 (Redis loss keeps quota/idempotency) and T30 regression | Pass |
| 4.17 | Google Weather API adapter behind the same interface (S11) | Staging uses it |
| 4.18 | Production notification (SMS/email) provider wiring (S12) | Pilot receives notifications |

---

### P5 — Frontend lead

**Mission:** a static Next.js app that never shows missing data as healthy and never lets UI hide authorization problems.

#### Phase 0–1 (S1–S3)
| # | Task | Done when | Spec |
|---|---|---|---|
| 5.1 | `apps/web`: Next.js, `output: 'export'`, `trailingSlash`, unoptimized images | Build emits only static files | §08.1 |
| 5.2 | Routes: `/login/`, `/app/`, `/app/fields/`, `/app/field/`, `/app/seasons/`, `/app/scouting/`, `/app/task/`, `/app/activities/`, `/app/weather/`, `/app/alerts/`, `/app/zoning/`, `/app/advice/`, `/app/reports/`, `/app/integrations/`, `/app/team/`, `/app/settings/`, `/oauth/callback/` (P1+ routes as placeholders) | Deep links work from static hosting (T28) | §08.2 |
| 5.3 | Design tokens, components, map library decision (MapLibre) as ADR | ADR merged | §08.3 |
| 5.4 | Typed API client generated from `contracts/openapi.json`; TanStack Query with keys incl. tenant + scope revision | Tenant switch clears caches | §08.3 |
| 5.5 | Sign-in with Firebase emulator, token refresh via SDK, tenant selector | W01 demoed | §08.4 |
| 5.6 | Field list + map, draw/edit polygon, validation errors displayed from problem+json | W04, W06 demoed | PR-02 |

#### Phase 2 (S4–S6)
| # | Task | Done when | Spec |
|---|---|---|---|
| 5.7 | Scene timeline and index chart: forecast vs observation, missing ≠ zero | Visual check against fixtures | §01.4 |
| 5.8 | Field detail: crop cycle, history, quality class, source, sensing time, resolution, processing version | PR-05 acceptance visible on screen | PR-05 |
| 5.9 | Map tiles through the gateway with bearer header; legend with textual numbers, never colour alone | Accessibility check passes | §02.6, §08.6 |
| 5.10 | Compare dates, natural-colour check, contrast mode shows actual min/max | W10 demoed | §04.4 |
| 5.11 | Home work list: urgent tasks, new evidence, data gaps; alerts screen; weather screen | PR-07/08 visible | §01.4 |
| 5.12 | Port useful pieces of legacy `HeatmapLayer.jsx`, `Legend.jsx`, `colorUtils.js` | — | — |

#### Phase 3–4 (S7–S10)
| # | Task | Done when | Spec |
|---|---|---|---|
| 5.13 | Team and invitations UI, protected owner controls | W03 demoed | PR-01 |
| 5.14 | Onboarding UI on the new API (reuse the step UX from `pages/steps`) | New farmer onboards end to end | — |
| 5.15 | Accessibility WCAG 2.2 AA on primary flows; RTL-safe layout | Automated + manual checks pass | §08.6 |
| 5.16 | English/Hindi via message keys | All strings externalized | §01.4 |
| 5.17 | Performance: lazy-load map/charts, virtualize lists, abort superseded requests | Shell usable < 3 s on mid-range device | §01.6 |
| 5.18 | Delete `frontend/` (S10) | Repo builds without it | — |
| 5.19 | S11: Firebase Hosting config, cache headers, CSP (with P6) | Headers verified in staging | §08.5 |

---

### P6 — Frontend + QA/DevEx, cloud lead in Phase 5

**Mission:** prove every claim with tests, build the offline workflow UI, then take the product to the cloud.

#### Phase 0–1 (S1–S3)
| # | Task | Done when | Spec |
|---|---|---|---|
| 6.1 | GitHub Actions CI: `go vet`, staticcheck, `go test -race`, migrations up on PostGIS container, web lint/build, OpenAPI validation | Required on every PR | §12.1 |
| 6.2 | Keep legacy `make contract` running in CI until S10 | Legacy stays green | — |
| 6.3 | Test harness: Go integration tests with ephemeral PostGIS, Playwright, k6 | Sample test in each layer | §12.1 |
| 6.4 | Tenant isolation suite (with P1): every endpoint × wrong tenant / revoked member | T01, T02 in CI | T01, T02 |
| 6.5 | Tests for untested packages still used after migration (`jwtutil`, `firebase`) | Coverage no longer 0% | AUDIT M9 |
| 6.6 | T03 (100 repeated keys) and T08 geometry tests in CI | Pass | T03, T08 |

#### Phase 2 (S4–S6)
| # | Task | Done when |
|---|---|---|
| 6.7 | E2E against the **exported static build**, not `next dev` | Sign-in → draw field → first observation → map |
| 6.8 | T09, T10, T11, T12, T13, T14 as automated tests with P2/P4 | Pass in CI |
| 6.9 | Benchmark harness for P2's 1,000-field run | Repeatable report |
| 6.10 | Import wizard UI: upload, column mapping, dry-run table, commit progress | W05 demoed |

#### Phase 3–4 (S7–S10)
| # | Task | Done when | Spec |
|---|---|---|---|
| 6.11 | Offline store in IndexedDB: assigned tasks, selected outlines, drafts; 7-day retention; purge control | Works in airplane mode | §08.4 |
| 6.12 | Sync queue: operation_id, device_id, base_version; foreground retry without Background Sync | T15 passes on device | §08.4 |
| 6.13 | Conflict screen: server version vs local draft, nothing lost | T15, T16 pass | W15 |
| 6.14 | Scouting UI (assignment, map point, photos, submit), activities UI, reports UI, settings/notifications/privacy UI | W14, W16, W21, W23, W24 demoed | — |
| 6.15 | Security regression: T17, T20, SSRF, malicious files | Pass | §09.7 |
| 6.16 | Local load test (baseline + burst) | Report with p50/p95/p99 | §12.4 |
| 6.17 | Release checklist and full regression (S10) | Signed | §11.6 |

#### Phase 5 (S11–S12) — cloud lead
| # | Task | Done when | Spec |
|---|---|---|---|
| 6.18 | Terraform modules: projects, VPC, Cloud NAT, Cloud SQL (HA, PITR, PostGIS), Memorystore, GCS buckets, Pub/Sub, Cloud Tasks, Secret Manager, Cloud Run (api/worker/tile/maintenance, one service account each), LB + Cloud Armor, Firebase Hosting, Identity Platform | `terraform plan` clean for staging and production | §02, §10.6 |
| 6.19 | Workload Identity Federation for CI; **no JSON key files** in any environment | `serviceAccountKey.json` unused in staging/prod | §02.3 |
| 6.20 | CI/CD: build image → migration Cloud Run job → deploy staging → smoke → manual prod promotion with traffic split → rollback by revision | Demonstrated rollback | §10.6 |
| 6.21 | Monitoring: SLO dashboards, alerts, structured logs, traces; budget alerts for EE and AI | Alerts fire in a test | §10.3–5 |
| 6.22 | Restore drill and cross-region DR test | Measured RPO/RTO recorded; T27 passes | §10.7 |
| 6.23 | T26 (connection budget), T28, T29 in staging | Pass | §12.2 |
| 6.24 | Pilot rollout (20 farms) with runbooks | Go/no-go signed | §11.6 |

---

## 8. Handoffs between people

| From → To | What | Due |
|---|---|---|
| P1 → all | Local stack, `AGENTS.md`, OpenAPI draft + mock | End S1 |
| P1 → all | Frozen OpenAPI, tx helper, auth verifier, RLS | End S2 |
| P3 → P1 | Legacy → new table mapping | End S1 |
| P1 → P2, P4 | Jobs + leases, outbox | End S3 |
| P3 → P2 | Fields + boundary versions (FK target for observations) | End S3 |
| P1 → P2, P3, P4 | `queue.Dispatcher`, `storage.Bucket` | End S4 |
| P2 → P5 | Observation + latest-projection endpoints | End S5 |
| P2 → P5 | Tile gateway | End S6 |
| P2 → P4 | Change-detection events | End S6 |
| P4 → P5 | Alerts and weather endpoints | End S6 |
| P3 → P6 | Import dry-run/commit endpoints | S5 / S6 |
| P4 → P6 | Scouting, sync, activities endpoints | End S8 |
| P4 → P6 | Reports, notifications, privacy endpoints | End S9 |
| P1, P3 → P6 | Adapter swap list + migration plan for staging | End S10 |

A handoff is complete only when the endpoint is in the frozen contract, implemented, tested, and demoed on the local stack.

---

## 9. Acceptance scenarios by owner

Scenarios from spec §12.2 that apply to P0. The owner writes the implementation; P6 makes sure the test runs in CI.

| Scenario | Owner | Sprint |
|---|---|---|
| T01 cross-tenant access denied everywhere | P1 | S2 |
| T02 revoked membership denied on next request | P1 | S2 |
| T03 same key ×100 → one effect; changed body conflicts | P1 | S3 |
| T04 crash after commit replays response | P1 | S3 |
| T05 crash after export before commit reconciles once | P2 | S5 |
| T06 duplicate/out-of-order events do not regress version | P1 / P4 | S6 |
| T07 failed dispatch retried without losing work | P1 | S4 |
| T08 invalid geometries return precise errors | P3 | S3 |
| T09 boundary edit during analysis keeps provenance | P2 / P3 | S5 |
| T10 all-cloud scene → insufficient, never NDVI 0 | P2 | S5 |
| T11 20 m resolution stays explicit | P2 | S6 |
| T12 scaled reflectance formulas, masked denominators | P2 | S3 |
| T13 change detection on common valid area | P2 | S6 |
| T14 weather times survive timezone/DST | P4 | S6 |
| T15 offline duplicate → one inspection; draft kept | P4 / P6 | S8 |
| T16 revoked scout cannot sync to old field | P4 | S8 |
| T17 photo upload cannot bypass scan | P4 | S8 |
| T18 activity completion needs actual dates, units, currency | P4 | S8 |
| T20 report download blocked after revocation | P4 | S9 |
| T25 Redis loss keeps quota/idempotency | P1 / P4 | S10 |
| T26 DB connection budget during deploy and burst | P6 | S12 |
| T27 restore applies erasure ledger first | P6 / P1 | S12 |
| T28 static deep links work without Next server | P5 | S2 |
| T29 logs/metrics carry no private fields | P6 | S12 |
| T30 provider outage shows stale/degraded state | P4 / P5 | S6 |

T19, T21–T24 belong to post-pilot features (§13).

---

## 10. Definition of done

A task is done only when **all** apply (spec §11.6):

- [ ] Code reviewed by the folder owner (and P1 for anything touching tenancy, auth or transactions)
- [ ] Unit tests including negative cases; integration test against real PostGIS where SQL is involved
- [ ] OpenAPI updated (if contract-affecting) and approved by P1
- [ ] Migration tested up from empty DB
- [ ] Structured logs with request ID; no private fields logged
- [ ] Permission and retention implications written in the PR description
- [ ] UI work: keyboard accessible, text alternative for colour, loading ≠ empty ≠ error states
- [ ] Demoed on the local stack at the Friday review

A demo alone is not done.

---

## 11. Working agreements

### Branching and PRs
- Trunk-based: short branches off `main`, merged daily.
- PRs under ~400 changed lines where possible.
- CODEOWNERS enforces §4 ownership; CI is required to merge.

### Rituals
| When | What | Who |
|---|---|---|
| Daily, 15 min | Stand-up: yesterday, today, blocked | All |
| Tue & Thu | Dependency check against §8 handoffs | P1 + anyone blocked |
| Friday | Demo on the local stack; scope decisions | All |
| Sprint end | Review + retro; update this document | All |

### `AGENTS.md` rules (Antigravity)
1. Only edit folders owned by the person running the agent (see §4).
2. Never edit `contracts/`, `migrations/` or `internal/platform/` without P1 review.
3. Every repository query uses the tenant transaction helper; no unscoped `GetByID`.
4. Every new Earth Engine call ships with a recorded fixture.
5. Masked or missing values serialize as absent/`null`, never `0`.
6. No new third-party dependency without an ADR.
7. Run the full test target before opening a PR.
8. Never commit `.env`, key files or real farmer data.

### Metrics tracked each sprint
Cycle time, blocked days, escaped defects, open handoffs, scope changes.

---

## 12. Risks

| Risk | Owner | Trigger | Mitigation |
|---|---|---|---|
| Contract slips past S2 | P1 | OpenAPI not frozen end S2 | P1 has no other work in S1–S2; frontend uses mock |
| Cloud-last surprises (Cloud Run CPU suspension, private networking, EE commercial quota) | P6 / P2 | Staging differs from local | All adapters behind interfaces; Phase 5 budgeted at 4 weeks; EE quota verified first in S11 |
| EE batch export complexity from Go | P2 | Export/reconcile not working by S5 | Start with `SubmitStatistics` only; exports for large fields follow |
| Small fields / cloud cover make data insufficient | P2 | Many pilot fields "insufficient" | Quality classes shown honestly; scouting fallback |
| Legacy data loss | P3 | Migration mismatch | Two rehearsals on a copy; idempotent script; row-count checks |
| Offline conflicts lose drafts | P6 / P4 | T15 failures | Operation ledger, explicit conflict UI, device tests |
| Agents overwriting each other | P1 | Merge conflicts across folders | CODEOWNERS, `AGENTS.md`, small daily PRs |
| Scope creep into AI/VRA | All | Requests before pilot | §13 list is closed until the pilot starts |
| One person out for a sprint | All | Absence | Pair on critical-path items (P1↔P3, P2↔P4, P5↔P6) |

---

## 13. After the pilot

Not in this plan. Candidate owners once the pilot runs:

| Requirement | Feature | Likely owner |
|---|---|---|
| PR-13 – PR-15 | Soil interpretation, growth stages, water stress | P2 + P4 |
| PR-16 | VRA zoning and prescriptions (W18, W19, T19) | P2 |
| PR-17 | AI assistant with citations and review (W20, T22, T23) — builds on `internal/chatbot` | P4 |
| PR-18 | John Deere, sensors, OAuth (W22, T21) | P3 |
| PR-19 – PR-22 | Yield, disease, classification, damage, commercial imagery (T24) | P2 + ML hire |
| PR-23 – PR-24 | Enterprise branding, imagery exploration | P5 |
