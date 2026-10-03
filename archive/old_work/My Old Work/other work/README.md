<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:21262d&height=200&section=header&text=MindstriX&fontSize=68&fontColor=58a6ff&animation=fadeIn&fontAlignY=35&desc=Satellite+Farm+Analysis+Platform&descAlignY=58&descColor=8b949e&descSize=20" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=15&duration=3000&pause=900&color=58A6FF&center=true&vCenter=true&multiline=true&width=760&height=55&lines=Sentinel-2+Optical+%7C+Sentinel-1+SAR+Radar+%7C+Real-time+Analysis;NDVI+%7C+EVI+%7C+SAVI+%7C+NDMI+%7C+NDWI+%7C+GNDVI+%7C+CVI+%7C+SMI+%7C+RVI;Krishi+Mitra+—+Grounded+Agronomy+AI+on+Live+Farm+Data" alt="Typing SVG"/>

<br/><br/>

<img src="https://img.shields.io/badge/Go-1.25-00ADD8?style=flat-square&logo=go&logoColor=white"/>
<img src="https://img.shields.io/badge/Gin-1.10%2B-008ECF?style=flat-square&logo=go&logoColor=white"/>
<img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black"/>
<img src="https://img.shields.io/badge/Vite-8.0-646CFF?style=flat-square&logo=vite&logoColor=white"/>
<img src="https://img.shields.io/badge/Google_Earth_Engine-API-4285F4?style=flat-square&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/Firebase-Auth_%26_Firestore-FFCA28?style=flat-square&logo=firebase&logoColor=black"/>
<img src="https://img.shields.io/badge/PostgreSQL_%2B_PostGIS-16-4169E1?style=flat-square&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=flat-square&logo=google&logoColor=white"/>

<br/><br/>

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Documentation](#documentation)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Overview](#api-overview)
- [Satellite Analysis](#satellite-analysis)
- [Contributing](#contributing)

> 📖 **Frontend Compatibility & Engineering Guide**: For strict directory rules, HeroUI v3 standards, Apple design principles, and automated verification (`npm run verify`), see [**`FRONTEND_GUIDE.md`**](FRONTEND_GUIDE.md).

---

## Overview

### Purpose

MindstriX is a full-stack satellite agronomy intelligence platform that delivers high-resolution multi-spectral and radar satellite imagery analysis directly to farm-level workflows. The platform transforms raw **Sentinel-2** optical and **Sentinel-1 SAR** radar bands into actionable vegetation health heatmaps, soil moisture assessments, and AI-grounded agronomic recommendations.

### Problem Statement

Small and medium-scale farmers lack access to affordable, real-time satellite crop health monitoring. Traditional field scouting is slow, expensive, and incomplete. Existing cloud-based satellite platforms are complex and not optimized for the agronomist or farmer workflow.

### System Layers

| Layer | Technology | Responsibility |
|---|---|---|
| Interactive Map | React + Leaflet | Draw and submit farm boundary polygons |
| REST API | Go + Gin, Earth Engine REST API | Satellite imagery processing pipeline |
| Optical Pipeline | Sentinel-2 SR (COPERNICUS/S2_SR_HARMONIZED) | Cloud-free vegetation index heatmaps at 10m |
| Radar Pipeline | Sentinel-1 GRD (COPERNICUS/S1_GRD) | Cloud-penetrating soil moisture and vegetation maps |
| AI Assistant | Google Gemini (Ollama fallback), called directly over HTTP | Grounded agronomy Q&A on live farm data |
| Authentication | Firebase Phone OTP + JWT | Secure, mobile-first farmer login |
| Database | PostgreSQL + PostGIS | Persistent farmer, farm, and crop data |

---

## Features

All features listed are implemented and verified in the current codebase.

### Remote Sensing

| Feature | Implementation |
|---|---|
| Sentinel-2 90-day cloud-free median composite | `internal/gee/`, `internal/pipeline/sentinel2.go` |
| SCL-based per-pixel cloud and shadow masking | `internal/gee/`, `internal/pipeline/sentinel2.go` |
| Vegetation index computation: NDVI, EVI, SAVI, NDMI, NDWI, GNDVI, CVI | `internal/pipeline/indices.go` |
| Sentinel-1 SAR speckle-filtered VV/VH composite | `internal/pipeline/sentinel1.go` |
| Radar index computation: SMI, RVI, VV, VH, Ratio | `internal/pipeline/radar_indices.go` |
| 10m heatmap grid generation with Gaussian smoothing | `internal/pipeline/grid.go`, `radar_grid.go` |
| GEE bicubic-smoothed tile URL generation | `internal/gee/`, `internal/pipeline/sentinel2.go` |
| Single-date Sentinel-2 and Sentinel-1 analysis | `internal/httpapi/` |
| Single-pixel hover sampling | `internal/httpapi/analyze_handler.go` (`/api/sample`) |

### Frontend

| Feature | Implementation |
|---|---|
| Interactive Leaflet map with polygon drawing | `frontend/src/MapView.jsx`, `HeatmapLayer.jsx` |
| Farm boundary delineation and rendering | `frontend/src/MapView.jsx` |
| Optical and Radar layer mode toggle | `frontend/src/LayerToggle.jsx` |
| Vegetation index heatmap grid renderer | `frontend/src/HeatmapLayer.jsx` |
| Farm statistics sidebar | `frontend/src/FarmSummary.jsx`, `Legend.jsx` |
| Timeline bar for date navigation | `frontend/src/TimelineBar.jsx` |
| Krishi Mitra AI chatbot panel | `frontend/src/KrishiMitraPanel.jsx` |

### Authentication and Data

| Feature | Implementation |
|---|---|
| Firebase Phone OTP login | `internal/httpapi/onboarding_handler.go`, `internal/service/sms.go` |
| Firebase JWT token verification | `internal/firebase/admin.go` |
| 8-step farmer onboarding flow | `frontend/src/pages/steps/`, `internal/httpapi/` |
| PostgreSQL + PostGIS data persistence | `internal/db/`, `internal/repo/`, `scripts/db/legacy/schema.sql` |
| Firestore ephemeral session synchronisation | `internal/firestore/` |
| Protected routes and JWT session management | `frontend/src/App.jsx` |

---

## Tech Stack

### Frontend

<div align="center">

![React](https://img.shields.io/badge/React_19-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite_8-646CFF?style=flat-square&logo=vite&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router_7-CA4245?style=flat-square&logo=react-router&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS_3-0F172A?style=flat-square&logo=tailwindcss&logoColor=38BDF8)
![Leaflet](https://img.shields.io/badge/Leaflet_1.9-199900?style=flat-square&logo=leaflet&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts_3-22C55E?style=flat-square)
![Axios](https://img.shields.io/badge/Axios_1-5A29E4?style=flat-square&logo=axios&logoColor=white)
![Turf.js](https://img.shields.io/badge/Turf.js_7-00A896?style=flat-square)
![Firebase SDK](https://img.shields.io/badge/Firebase_SDK_12-FFCA28?style=flat-square&logo=firebase&logoColor=black)

</div>

| Package | Version | Role |
|---|---|---|
| react | 19 | UI component framework |
| vite | 8 | Build tool and dev server |
| react-router-dom | 7 | Client-side routing |
| leaflet / react-leaflet | 1.9 / 5.0 | Interactive map rendering |
| leaflet-draw | 1.0 | Polygon drawing tools |
| recharts | 3 | Data visualisation charts |
| axios | 1 | HTTP API client |
| @turf/turf | 7 | GeoJSON geometry operations |
| tailwindcss | 3 | Utility-first styling |
| firebase | 12 | Firebase Auth client |

### Backend

<div align="center">

![Go](https://img.shields.io/badge/Go_1.23%2B-00ADD8?style=flat-square&logo=go&logoColor=white)
![Gin](https://img.shields.io/badge/Gin_1.10%2B-008ECF?style=flat-square&logo=go&logoColor=white)
![JWT](https://img.shields.io/badge/golang--jwt_v5-1F2937?style=flat-square)
![pgx](https://img.shields.io/badge/pgx_v5-4169E1?style=flat-square&logo=postgresql&logoColor=white)

</div>

| Package | Version | Role |
|---|---|---|
| gin-gonic/gin | 1.10+ | REST API framework |
| gin-contrib/cors | 1.7+ | Cross-origin request handling |
| golang-jwt/jwt | v5 | JWT issuance and validation, wire-compatible with the previous Flask-JWT-Extended tokens |
| go-playground/validator | v10 | Input validation and schema enforcement |
| jackc/pgx | v5 | PostgreSQL driver and connection pool |
| joho/godotenv | 1.5+ | Environment variable loading |
| golang.org/x/crypto | latest | scrypt / pbkdf2, for verifying existing Werkzeug password hashes |

### GIS and Remote Sensing

<div align="center">

![GEE](https://img.shields.io/badge/Google_Earth_Engine-REST_v1-4285F4?style=flat-square&logo=google&logoColor=white)
![Sentinel-2](https://img.shields.io/badge/Sentinel--2_SR_L2A-10m_Optical-2E7D32?style=flat-square)
![Sentinel-1](https://img.shields.io/badge/Sentinel--1_GRD-SAR_Radar-1565C0?style=flat-square)

</div>

| Technology | Role |
|---|---|
| Earth Engine REST API (`earthengine.googleapis.com/v1`) | Sentinel-2 and Sentinel-1 collection filtering, compositing, index computation, and tile generation. No Go EE SDK exists, so `internal/gee/eeexpr` builds the expression graphs by hand and posts them to `value:compute`, `table:computeFeatures` and `maps`. |
| COPERNICUS/S2_SR_HARMONIZED | Optical multispectral imagery — 10m/20m resolution |
| COPERNICUS/S1_GRD | C-band SAR radar imagery — VV/VH polarisation, DESCENDING orbit pass |

### Database and Authentication

<div align="center">

![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![PostGIS](https://img.shields.io/badge/PostGIS_3.x-336791?style=flat-square)
![Firebase Auth](https://img.shields.io/badge/Firebase_Auth_Phone_OTP-FFCA28?style=flat-square&logo=firebase&logoColor=black)
![Firebase Admin](https://img.shields.io/badge/Firebase_Admin_SDK-FFA000?style=flat-square&logo=firebase&logoColor=black)

</div>

| Technology | Role |
|---|---|
| PostgreSQL 16 | Primary relational store for farmer, farm, crop, irrigation, and soil records |
| PostGIS 3.x | Spatial extension — farm polygons stored as GEOMETRY(POLYGON, 4326) |
| jackc/pgx v5 | PostgreSQL driver and connection pool (min 2 / max 20) |
| Firebase Auth (Phone) | Phone number OTP-based authentication |
| Firebase Admin SDK | Server-side Firebase JWT token verification |

### AI

<div align="center">

![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-Hosted_LLM-4285F4?style=flat-square&logo=google&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama_llama3.2-Local_fallback-00A67E?style=flat-square)
![Go](https://img.shields.io/badge/net%2Fhttp-Direct_Ollama_API-00ADD8?style=flat-square&logo=go&logoColor=white)

</div>

| Technology | Role |
|---|---|
| Google Gemini (`gemini-2.5-flash`) | Hosted LLM, selected by setting `GEMINI_API_KEY` |
| Ollama (llama3.2) | Local LLM runtime, used when no Gemini key is configured — no external API dependency |
| `internal/gemini`, `internal/ollama` | Direct HTTP clients, interchangeable behind one interface. LangChain was dropped in the Go port: the chain was a system prompt plus history plus one user turn, which is a short HTTP client. |
| `internal/chatbot` | Per-session conversation memory and the system-prompt template, rebuilt per request from the current field's live statistics |

---

## Project Structure

The repository holds two applications side by side. The **legacy app** (single-tenant heatmap
and onboarding) is the running reference; the **platform** (multi-tenant `/v1` API) is being
built alongside it per [`AGENTS.md`](./AGENTS.md) and replaces the legacy app at the end of
Phase 4.

```
Pragya/
├── cmd/
│   ├── server/          # legacy app entrypoint (Gin, port 5000)
│   ├── api/             # platform /v1 API (chi)
│   ├── worker/          # platform job worker (analysis, privacy, ...)
│   ├── maintenance/     # outbox publisher, dispatch sweep, reaper, retention, audit export
│   └── tile/            # tile gateway (Phase 2)
├── internal/
│   ├── gee/             # the only package that talks to Earth Engine (shared)
│   ├── pipeline/        # Sentinel-1/2 analytics core (shared)
│   ├── geo/             # polygon validation (shared)
│   ├── platform/        # platform ports: db, auth, http, idempotency, jobs, queue, storage, ...
│   ├── domain/          # platform domains: tenancy, fields, observations, alerts, privacy, ...
│   ├── adapters/        # platform adapters: postgres, redis, storage, queue, weather
│   ├── apiv1/           # platform HTTP handlers
│   └── httpapi/, repo/, service/, db/, config/, ...   # legacy app
├── migrations/          # goose migrations (platform schema, RLS forced)
├── contracts/           # OpenAPI contract for /v1 (frozen, hash-locked)
├── frontend/            # legacy React + Vite web app
├── docker/              # platform image, Firebase emulator, Postgres init
├── scripts/             # contract/spec tooling; db/legacy/ holds the frozen legacy SQL
├── tools/               # legacy contract runner, DB reset helper, legacy-data migration
├── testdata/            # golden fixtures for the legacy app and the pipeline
├── tests/               # cross-package benchmarks
├── build/tools/         # pinned goose and sqlc
└── docs/
    ├── adr/             # architecture decision records
    ├── platform/        # platform status, local stack, contract changes, cloud swap checklist
    ├── runbooks/        # operator procedures
    ├── references/      # product specification and team work division
    └── CHANGELOG.md, KNOWN_ISSUES.md, ENDPOINT_VERIFICATION.md   # legacy app
```

---

## Architecture Overview

```
+-------------------------------------------------------------+
|                      User (Browser)                         |
+-----------------------------+-------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|          React + Vite Frontend  (port 5173)                 |
|  - Leaflet map  :  draw farm boundary polygon               |
|  - Submit GeoJSON geometry to backend REST API              |
|  - Render heatmap grid and GEE tile overlay                 |
|  - Statistics sidebar, chatbot panel, layer toggle          |
+-----------------------------+-------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|          Go REST API Backend  (port 5000)                   |
|  - Validate GeoJSON polygon                                 |
|  - Build eeexpr.Geometry (internal/gee)                     |
|  - Route to optical or radar pipeline                       |
+----------+----------------------------------+---------------+
           |                                  |
           v                                  v
+---------------------+          +----------------------------+
| Sentinel-2 Optical  |          | Sentinel-1 Radar Pipeline  |
| sentinel2.go        |          | sentinel1.go               |
| - 90-day lookback   |          | - S1 GRD collection filter |
| - SCL cloud mask    |          | - Speckle filter (focal    |
| - Median composite  |          |   median, ~50m radius)     |
|          |          |          | - Median composite         |
|          v          |          |          |                  |
| indices.go          |          | radar_indices.go           |
| NDVI  EVI  SAVI     |          | SMI   RVI   VV/VH   Ratio  |
| NDMI  NDWI  GNDVI   |          |                            |
| CVI (weighted sum)  |          |                            |
+----------+----------+          +-------------+--------------+
           |                                   |
           +---------------+-------------------+
                           |
                           v
             grid.go / radar_grid.go
             - 10m grid cell generation
             - Per-cell band value reduction (ee.Reducer)
             - Gaussian smoothing
                           |
                           v
             Response: GeoJSON FeatureCollection
                      + GEE smooth tile URLs
                      + Farm-wide statistics
                           |
                           v
+-------------------------------------------------------------+
|               React Frontend — Visualisation                |
|  HeatmapLayer.jsx   ->  per-cell coloured polygons          |
|  GEE tile overlay   ->  bicubic-smoothed raster             |
|  FarmSummary.jsx    ->  vegetation index statistics         |
|  Legend.jsx         ->  colour gradient scale               |
+-----------------------------+-------------------------------+
                              |
                              v
              KrishiMitraPanel.jsx
              POST /chatbot/chat
              Body: { farmData, heatmapData, message }
                              |
                              v
              internal/chatbot  ->  grounded system prompt
              Ollama (llama3.2)  ->  agronomic answer
```

---

## Documentation

| Document | What it covers |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | Rules for everyone (and every coding agent) working in the repository; folder ownership |
| [`CLAUDE.md`](./CLAUDE.md) | Legacy app architecture and conventions |
| [`docs/platform/STATUS.md`](./docs/platform/STATUS.md) | Platform progress against the plan, open items and decisions |
| [`docs/platform/LOCAL_STACK.md`](./docs/platform/LOCAL_STACK.md) | Running the platform and its tests locally (Docker or native) |
| [`docs/adr/`](./docs/adr/) | Architecture decision records 0001–0018 |
| [`docs/platform/CONTRACT_CHANGES.md`](./docs/platform/CONTRACT_CHANGES.md) | Change record of the `/v1` contract |
| [`docs/platform/ADAPTER_SWAP_INVENTORY.md`](./docs/platform/ADAPTER_SWAP_INVENTORY.md) | Checklist for moving local adapters to Google Cloud |
| [`docs/runbooks/`](./docs/runbooks/) | Operator procedures (audit access, support access) |
| [`docs/references/`](./docs/references/) | Product specification (`6182`) and team work division |
| [`docs/KNOWN_ISSUES.md`](./docs/KNOWN_ISSUES.md) | Behaviours deliberately preserved in the legacy app (K1–K15) |
| [`docs/ENDPOINT_VERIFICATION.md`](./docs/ENDPOINT_VERIFICATION.md) | Legacy endpoint matrix with verified responses |
| [`docs/CHANGELOG.md`](./docs/CHANGELOG.md) | Version history of the Python → Go migration |

---

## Installation

### Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| Go | 1.25 | Backend runtime |
| Node.js | 20 | Frontend build toolchain |
| PostgreSQL | 16 | With PostGIS 3.x extension |
| Google Cloud project | — | Earth Engine API must be enabled |
| Firebase project | — | Phone Authentication must be enabled |
| Ollama | latest | `llama3.2` model must be pulled |

### 1. Clone the Repository

```bash
git clone https://github.com/KrishiSahAI/Pragya.git
cd Pragya
```

### 2. Backend Setup

```powershell
# Build the backend (Go 1.25+)
go build -o bin/server ./cmd/server

# Configure environment variables
copy .env.example .env
# Edit .env and set: GEE_PROJECT_ID, DATABASE_URL, FIREBASE_PROJECT_ID, JWT_SECRET_KEY

# Google Earth Engine credentials
# Production: point GEE_SERVICE_ACCOUNT_KEY at a service-account JSON key that
#             has been registered for Earth Engine.
# Local dev:  reuse an existing `earthengine authenticate` refresh token by also
#             setting GEE_OAUTH_CLIENT_ID and GEE_OAUTH_CLIENT_SECRET.

# Start the API server
./bin/server
```

The server starts even with no credentials at all: `/health` reports
`gee_ready: false`, the analysis routes answer 503, and auth, onboarding and the
dashboard keep working.

The backend API will be available at `http://127.0.0.1:5000`.

### 3. Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

The frontend dev server will be available at `http://localhost:5173`.

### 4. Database Setup

```sql
psql -U postgres
CREATE DATABASE mindstrix;
\c mindstrix
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\i scripts/db/legacy/schema.sql
```

### 5. Ollama Chatbot Service

```bash
ollama serve
ollama pull llama3.2
```

---

## Configuration

### Backend — `.env`

Copy `.env.example` to `.env` at the repository root and populate all variables.

| Variable | Description |
|---|---|
| `GEE_PROJECT_ID` | Google Cloud project ID with Earth Engine API enabled |
| `DATABASE_URL` | PostgreSQL connection string: `postgresql://user:password@host:5432/dbname` |
| `FIREBASE_PROJECT_ID` | Firebase project ID for Admin SDK initialisation |
| `JWT_SECRET_KEY` | HS256 signing key. Tokens stay wire-compatible with the previous Flask-JWT-Extended ones, so existing sessions survive — change in production |
| `FLASK_PORT` | Server port (default: `5000`). The env var name is kept for ops continuity |
| `FLASK_ENV` | `development` or `production` |

### Frontend — `frontend/.env`

| Variable | Description |
|---|---|
| `VITE_FIREBASE_API_KEY` | Firebase web API key |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase auth domain |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase storage bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID |
| `VITE_FIREBASE_APP_ID` | Firebase app ID |

> GEE credentials are written to `~/.config/earthengine/credentials` by `earthengine authenticate`. No service account key file is required.

---

## API Overview

Legacy endpoints with verified responses: [`docs/ENDPOINT_VERIFICATION.md`](./docs/ENDPOINT_VERIFICATION.md). The platform `/v1` API is specified in [`contracts/openapi.json`](./contracts/openapi.json).

### Satellite Analysis

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — GEE and Firebase initialisation status |
| `POST` | `/api/analyze` | Sentinel-2 analysis: vegetation indices + heatmap grid + farm stats |
| `POST` | `/api/analyze-dates` | List available Sentinel-2 acquisition dates for a polygon |
| `POST` | `/api/analyze-day` | Single-date Sentinel-2 analysis |
| `GET` | `/api/sample` | Single-pixel hover sampling (`?lat=&lng=&band=NDVI`) |
| `POST` | `/api/analyze-radar` | Sentinel-1 radar analysis: SMI, RVI, VV/VH ratio + grid |
| `POST` | `/api/analyze-radar-dates` | List available Sentinel-1 acquisition dates for a polygon |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/send-otp` | Send a 6-digit OTP to an Indian mobile number |
| `POST` | `/api/auth/verify-otp` | Verify OTP and issue a JWT session token |
| `POST` | `/api/auth/verify-token` | Verify a Firebase ID token via Admin SDK |

### Chatbot

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chatbot/chat` | Send a user message; receive a grounded AI reply |
| `POST` | `/chatbot/reset` | Clear the conversation memory for a session |
| `GET` | `/chatbot/health` | Chatbot health check — Ollama model name and base URL |

---

## Satellite Analysis

### Sentinel-2 — Vegetation Indices

Computed by `internal/pipeline/indices.go` from a scaled Sentinel-2 SR median composite with reflectance values in `[0.0, 1.0]`.

| Index | Formula | Agronomic Meaning |
|---|---|---|
| NDVI | `(NIR - RED) / (NIR + RED)` | Overall vegetation greenness and canopy density |
| EVI | `2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)` | Atmospheric-corrected vegetation; reduces canopy saturation |
| SAVI | `((NIR - RED) / (NIR + RED + 0.5)) * 1.5` | Vegetation with soil brightness bias correction |
| NDMI | `(NIR - SWIR) / (NIR + SWIR)` | Canopy moisture content and drought stress |
| NDWI | `(GREEN - NIR) / (GREEN + NIR)` | Water body detection |
| GNDVI | `(NIR - GREEN) / (NIR + GREEN)` | Chlorophyll content and nutritional status |
| CVI | `0.70·NDVI + 0.10·EVI + 0.05·SAVI + 0.10·NDMI + 0.05·GNDVI` | Composite multi-index fusion. Weights live in `internal/config/config.go` and must sum to 1.0; NDWI is computed and returned but carries no weight |

### Sentinel-1 — Radar Indices

Computed by `internal/pipeline/radar_indices.go` from a speckle-filtered VV/VH dB composite.

| Index | Formula | Agronomic Meaning |
|---|---|---|
| VV | Raw backscatter (dB) | Surface soil moisture and roughness sensitivity |
| VH | Raw backscatter (dB) | Vegetation volume structure and canopy scattering |
| SMI | `(VV - VV_dry) / (VV_wet - VV_dry)`, clamped to [0, 1] | Soil Moisture Index: 0 = dry, 1 = wet |
| RVI | `4 * VH_linear / (VV_linear + VH_linear)`, clamped to [0, 1] | Radar Vegetation Index — canopy density from SAR backscatter |
| Ratio | `VV_dB - VH_dB` | VV/VH ratio: soil dominance vs. vegetation dominance |

The Sentinel-1 pipeline is fully independent of cloud cover conditions, enabling continuous monitoring regardless of weather.

---

## Contributing

Read [`AGENTS.md`](./AGENTS.md) before opening a pull request: it defines folder ownership, the
eight working rules and what "done" means. CI (`.github/workflows/ci.yml`) must be green to merge.

### Architectural Rules

| Rule | Requirement |
|---|---|
| GEE Isolation | All Earth Engine calls must remain strictly within `internal/gee`. `internal/pipeline` builds expression graphs but performs no I/O, and `internal/httpapi` builds no graphs at all. Other packages only pass `eeexpr.Image` / `eeexpr.Geometry` values around. |
| Centralised Configuration | All threshold values, index weights, cloud cover limits, and array bounds must be defined in `internal/config/config.go`. Do not scatter constants through service logic. |
| No Silent Fallbacks | Return the correct HTTP error code on failure: `503` for GEE unavailable, `400` for invalid polygon. Do not swallow errors with fake or empty fallback data. |
| Tenant Isolation (platform) | Every platform query runs inside the tenant transaction helper; no unscoped lookups. Enforced by RLS and by `internal/archtest`. |
| Contract First (platform) | `/v1` changes go through `contracts/openapi.json`, its lock and [`CONTRACT_CHANGES.md`](./docs/platform/CONTRACT_CHANGES.md). |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:21262d,50:161b22,100:0d1117&height=110&section=footer&animation=fadeIn" width="100%"/>

Architecture decisions, platform status and references live in [`/docs`](./docs/); start with [Documentation](#documentation).

</div>
