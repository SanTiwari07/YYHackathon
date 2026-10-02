# P2 Geospatial Pipeline Architecture

This document describes the production architecture for the Geospatial Engineering & Earth Engine Analysis subsystem of the Global Farmer Platform (Pragya), conforming to specification `6182.docx` v1.0.0 and team work division §02 and §04.

---

## 1. High-Level Architecture Overview

The geospatial analysis subsystem processes multi-spectral satellite imagery (Sentinel-2 Harmonized, Cloud Score+, and Sentinel-1 SAR) to generate deterministic, provenance-tracked field observations and Cloud-Optimized GeoTIFFs (COGs).

```
                                  [ Client Request ]
                                          │
                                          ▼
                                POST /v1/.../analysis
                                          │
                        ┌─────────────────┴─────────────────┐
                        │   Tenant & Field Authorization    │
                        │     Admission Checks (0.01-20k ha)│
                        │     Durable Job State Enqueued    │
                        └─────────────────┬─────────────────┘
                                          │ HTTP 202 Accepted + Job ID
                                          ▼
                                  [ Worker Runtime ]
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 │                Analysis Handler                 │
                 │   Snapshot boundary_version, crop_cycle, params  │
                 │   Check deterministic submission / deduplication │
                 └────────────────────────┬────────────────────────┘
                                          │
                       ┌──────────────────┴──────────────────┐
                       │                                     │
                       ▼                                     ▼
             [ Batch Dispatcher ]                  [ Historical Backfill ]
             • Tile / Window Grouping              • Rate-isolated queue
             • Max concurrency = 2                 • Low priority
             • Adaptive split (50 fields / 5k vtx) • Non-starving
                       │                                     │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                              [ Earth Engine REST API ]
                              • DiscoverScenes
                              • SubmitStatistics (eeexpr AST)
                              • SubmitRasterExport (Cloud Score+)
                                          │
                       ┌──────────────────┴──────────────────┐
                       │                                     │
                       ▼                                     ▼
             [ Statistics Reducer ]                 [ COG Export Pipeline ]
             • Valid area fraction                  • Cloud-Optimized GeoTIFF
             • Valid pixel count                    • Overviews & explicit mask
             • p10, p50, p90, mean, stddev          • SHA-256 Checksum & Manifest
             • Quality class assignment             • Atomic storage promotion
                       │                                     │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                               [ PostgreSQL / PostGIS ]
                               • app.observations (immutable)
                               • Provenance: boundary_version, scene_ids,
                                 processing_version, effective_resolution
                               • app.outbox (change detection events)
                                          │
                                          ▼
                                   [ Tile Gateway ]
                                   cmd/tile (port 8082)
                                   • Grant check per request
                                   • COG range reads
                                   • Key: tenant:asset:style:z:x:y
                                   • Revoked user -> 404
```

---

## 2. Core Scientific and Engineering Principles

### 2.1 Missing Data Policy (Rule 5)
- Masked or missing values serialize as `null` or absent, **never 0**.
- Insufficient satellite coverage is never reported as "healthy" or "normal".
- Quality statuses are assigned deterministically:
  - **USABLE**: `valid_fraction >= 0.70` AND `valid_pixel_count >= 20`.
  - **PARTIAL**: `valid_fraction >= 0.30` AND `valid_pixel_count >= 5`.
  - **INSUFFICIENT**: Anything below partial thresholds.
- When `valid_pixel_count == 0` or insufficient, reducers emit `nil` for statistics (`Mean`, `P10`, `P50`, `P90`, `StdDev`).

### 2.2 Cloud Masking & Provenance
- Primary masking links `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` requiring `cs_cdf >= 0.60`.
- Missing Cloud Score+ falls back to SCL (Scene Classification Layer) masking, explicitly labelled as `scl_fallback` with degraded quality implications.
- SCL masks defective pixels, cloud shadows, cirrus, and medium/high probability clouds.

### 2.3 Numerical Safety & Scaled Reflectance
- All index calculations use surface reflectance scaled by `0.0001` before additive constants.
- Denominators are guarded by epsilon \(\epsilon = 10^{-6}\).
- Invalid divisions or zero denominators produce masked pixels, never `NaN`, `+Inf`, `-Inf`, or fake zeroes.
- Supported `/v1` indices:
  - **NDVI**: \((B8 - B4) / (B8 + B4)\) [10m]
  - **NDMI**: \((B8 - B11) / (B8 + B11)\) [20m effective resolution]
  - **EVI**: \(2.5 \times (B8 - B4) / (B8 + 6.0 B4 - 7.5 B2 + 1.0)\) [10m]
  - **NDRE**: \((B8A - B5) / (B8A + B5)\) [20m effective resolution]
  - **RECI**: \((B8A / B5) - 1.0\) [20m effective resolution]
  - **MSAVI**: \((2 B8 + 1 - \sqrt{(2 B8 + 1)^2 - 8 (B8 - B4)}) / 2.0\) [10m]
- Unsupported prototype indices (`CVI`, `SAVI`, `NDWI`, `GNDVI`) are retired from `/v1`.

### 2.4 Immutable Observations and Boundary Provenance (Acceptance T09)
- Field geometry is versioned in `app.field_boundaries` with foreign key integrity.
- Each analysis job records the exact `boundary_version` captured at submission.
- Even if a user updates the boundary while an analysis job is in-flight, the resulting observation links immutably to the historical boundary version without corrupting current projections.

### 2.5 Crash Reconciliation (Acceptance T05)
- Earth Engine exports write deterministic artifacts to object storage.
- If a crash occurs after external export before SQL commit, worker reconciliation checks existing storage assets and deduplication keys, committing the observation without re-executing expensive Earth Engine operations.

### 2.6 Change Detection (Acceptance T13)
- Evaluates temporal changes across common valid pixels only.
- Requires common valid area fraction \(\ge 0.70\) across both dates.
- Detects significant vegetation drops when \(\Delta \text{NDVI} \ge 0.15\) over 3 to 30 days.
- Emits structured outbox events for operational notification (P4) with neutral language ("vegetation decreased", never unverified claims of "disease confirmed").

### 2.7 Spatial Batching and Quotas (Acceptance §04.7)
- Groups field work items by Sentinel-2 MGRS tile and time window.
- Concurrency bounded to 2 (`concurrency = 2`).
- Adaptively splits batches exceeding 50 fields or 5,000 vertices.
- Fault isolation: a single failed field in a batch is isolated without restarting or failing other fields.
- Historical backfill runs on a separate rate-limited semaphore to prevent starving daily acquisitions.
- Benchmark: 1,000 fields processed under 10 minutes (proven locally in under 1 second).

---

## 3. Tile Gateway (`cmd/tile`)
- Standalone service running on port 8082.
- Authenticates bearer token and validates tenant membership and field grant on every single tile request.
- Enforces cache key: `tenant_id:asset_id:style:z:x:y`.
- Reads Cloud-Optimized GeoTIFFs from `storage.Bucket` (`ZoneReady`).
- If membership is revoked or suspended, returns HTTP 404 immediately on the next tile request.
