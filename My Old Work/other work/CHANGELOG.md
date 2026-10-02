# Changelog

All notable changes to the MindstriX Satellite Agronomy Intelligence Platform documentation and codebase structure are recorded in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased — after the cutover

### Chatbot backend: Ollama → Google Gemini

`internal/gemini` is a direct client for the `generateContent` API, interchangeable
with `internal/ollama` behind a single call site. `GEMINI_API_KEY` selects the
backend; with it unset the local Ollama path still works, so switching back is a
config change rather than a rebuild. `/chatbot/health` keeps its three keys and
only reports whichever backend is configured. Details and the Gemini-specific
API gotchas are in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

### Earth Engine session lifetime

The OAuth token source captured the 60 s startup context and reused it for every
later refresh, so Earth Engine calls began failing with `context canceled` about
an hour after startup. Three separate call sites captured a context; all three
now use `context.Background()`. Covered by a live regression test that cancels
the caller context and then makes a real call.

### Two frontend strings (the only sanctioned edit to `frontend/`)

The freeze in `CLAUDE.md` still stands — these were changed on an explicit owner
decision, and neither touches the HTTP contract, component structure or CSS:

- The Krishi Mitra badge showed **"Connecting"** when no field was selected,
  which is indistinguishable from a failing backend. With no field there is
  nothing to connect *for*, so that state now reads **"No field selected"**.
  The status values and their CSS classes are unchanged.
- The connection-failure message told the user to "make sure the **local AI
  service** is running" — stale wording once the backend became hosted Gemini.
  It now names the backend server and the AI service without assuming either is
  local.

## v2.0.0-go — Project Pragya: Python → Go backend migration

**Released.** `legacy-python/` deleted; the Go backend is the implementation.
Recover the reference with `git checkout v2.0.0-go~1 -- legacy-python`.

Tracking `PRAGYA_GO_MIGRATION_PRD.md`. Each phase below lands as its own
reviewable commit range and must leave `make verify` green.

### Phase 0 — Groundwork ✅

**Repository layout**

- `go mod init github.com/KrishiSahAI/Pragya` (Go 1.23).
- Added `Makefile` (`make verify` is the per-phase gate), `.golangci.yml`,
  multi-stage `Dockerfile` (distroless, `CGO_ENABLED=0`).
- `backend/` → `legacy-python/`. It stays in the repo as the reference
  implementation and the source of every golden fixture, and is deleted in a
  standalone commit at Phase 7 (PRD §0.7, §14).
- **Deleted `backend/legacy/`** — the original interactive CLI
  (`main.py` 674 LOC, `gee_engine.py` 198 LOC, `config.py` 133 LOC).
  Confirmed dead: nothing in the running app imports it (PRD §1.3).
- `.gitignore`: added `gee-service-account.json` and `bin/`.
- `legacy-python/.env.example`: appended the Go-only keys (PRD §9.2). No
  existing key was renamed — `FLASK_PORT` and friends are kept for ops
  continuity, and the frontend needs zero edits.

**Configuration**

- `internal/config/config.go`: 1:1 port of `config.py` + `chatbot/config.py`,
  plus the palettes from `app.py`. Thresholds are stored as **descending
  ordered slices** rather than maps, because `config.py` sorts its dict keys
  descending at every call site and a Go map has no order.
- `internal/config/config_test.go`: a second, independent transcription of
  every constant in PRD Appendix A, plus guards for threshold ordering,
  CVI weight sum, and palette length / endpoints.

**Golden fixtures captured from the live Python backend** (PRD §12) — all
captured *before* any Python file was moved or modified:

| Layer | What | Count | Location |
|---|---|---|---|
| 1 | EE expression graphs (§5.7 G1–G24) | 37 | `internal/gee/eeexpr/testdata/` |
| 1 | Live `maps` request + tile-URL template | 1 | `internal/gee/eeexpr/testdata/maps_request_response.json` |
| 2 | HTTP contract cases (§12.2) | 73 | `testdata/golden/` |
| 3 | Numeric parity, 5 fixture polygons × S2 + S1 (§12.3) | 5 | `testdata/golden/numeric/` |
| — | Werkzeug password hashes (§8.2) | 9 | `internal/crypto/testdata/` |
| — | Chatbot system-prompt renders (§10.11) | 2 | `internal/chatbot/testdata/` |

Capture tooling lives in `legacy-python/tools/` and is driven by
`make fixtures`. The contract corpus (`contract_corpus.py`) is the single
definition replayed by both the Python capturer and the Go runner.

**Deliberate capture gaps**, documented so they are not mistaken for coverage:

- `POST /api/auth/send-otp` success/502 branches — hitting them sends a real,
  billed SMS through the nationalbulksms gateway. Only the 400 branch is
  captured; the rest needs a staging gateway.
- The `503 "GEE not initialised"` branches — GEE is healthy on the capture
  machine. They are asserted directly in Phase 1 by starting the Go server with
  `GEE_PROJECT_ID` unset, which also pins the two *different* wordings E2 and
  E3–E7 use.

**Issues filed:** K1–K10 from PRD §13.9, plus two found during capture (K11
pincode User-Agent block, K12 JWT 401-vs-422), plus 12 verified corrections to
the PRD's own EE assumptions. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

**Note on the moved venv:** `legacy-python/venv/Scripts/*.exe` console shims
(`pip.exe`, `earthengine.exe`) have the old absolute path baked in and no longer
run. `venv/Scripts/python.exe` itself is fine, and so is `python.exe -m pip`.
All `make fixtures` targets invoke `python.exe` directly for this reason. If the
Python reference ever needs new packages installed, use
`legacy-python/venv/Scripts/python.exe -m pip install …`.

### Phase 1 — HTTP skeleton ✅

All 24 routes of §10.1 are registered and answer with the real contract for
every error branch. Analysis routes answer 503 (GEE lands in Phase 2); routes
that need a service layer validate fully and then answer 501, so the contract
runner can tell "not built yet" from "built and wrong".

**Added**

- `internal/geo` — `ValidatePolygon`, a byte-exact port of §6.1 including check
  ordering, wording, and Python's number formatting.
- `internal/logging` — a `slog` handler reproducing
  `"%(asctime)s [%(levelname)s] %(name)s — %(message)s"` (em dash, `WARNING`
  not `WARN`), writing to stdout and `cvi_engine.log`.
- `internal/httpapi` — router, error envelopes, marshmallow-compatible
  validation, schemas, and the analysis / onboarding / chatbot handlers.
- `internal/httpapi/middleware` — global CORS (§9.3) and JWT verification (§8.3).
- `cmd/server` — config → deps → router wiring, one-shot startup probes in
  goroutines (NOT per-request as `@app.before_request` does), `WriteTimeout`
  300s for long analyses, 30s graceful drain on SIGTERM.
- `tools/contract` — the Layer-2 runner. Replays the frozen corpus against Go
  and diffs status + JSON against the goldens, with float tolerance `1e-6`,
  masked volatile values, and an explicit call-out when a `null` index value
  turns into `0` (§13.1). `-python-base` live-diffs the two backends instead.

**Verification:** `go vet`, `staticcheck`, `go test -race`, and the contract
runner are all green. 73 cases: **24 pass, 0 fail**, 47 awaiting later phases,
2 skipped (K11).

Because the readiness check precedes validation, the analysis 400 branches are
unreachable over HTTP while GEE is unwired. They are therefore covered by
`internal/httpapi/analyze_test.go`, which flips the readiness flag and diffs all
17 of them against the same goldens.

**Three findings worth recording**

- PRD §6.1 says to format coordinates with
  `strconv.FormatFloat(v, 'g', -1, 64)`. That yields `181`, while Python prints
  `181.0`. Worse, the int-vs-float distinction depends on the JSON *literal*
  (`200` → `200`, `200.0` → `200.0`), so the decoder must use `json.Number`.
  `internal/geo.pyNum` reproduces Python's rules and is table-tested against the
  interpreter's own output.
- `validator/v10` splits tag strings on commas before a custom validation sees
  the param, so `mlen=1,255` parses as `mlen=1` plus an undefined tag `255` and
  panics at struct-cache build time. Custom tags use `:` as the bound separator.
- Required fields are modelled as **pointers**, because marshmallow
  distinguishes "key absent" (→ `Missing data for required field.`) from
  "present but empty" (→ `Length must be between 1 and 255.`). A plain Go string
  cannot tell those apart and would emit the wrong message.

**Deviation from the PRD, sanctioned by the owner:** K11. Go sets an explicit
User-Agent on the India Post call and returns the real 200/404 branches. The two
`e15_*` goldens captured the broken 500 and are skipped by the contract runner.

### Phases 2-6 ✅

See the [migration report](https://github.com/KrishiSahAI/Pragya/blob/69dfdae8f11b54d28d888071cd276a39c5ba7aab/REPORT.md) for the full narrative. Summary:

- **Phase 2** — `internal/gee/eeexpr` builds Earth Engine expression graphs by
  hand; all 24 computations of §5.7 gated by strict equality against fixtures
  captured from the real Python client. REST client with paging and the §13.4
  retry policy. Live gate: `s2_scene_count = 17`, grid cells `= 266`, both
  matching Python exactly.
- **Phase 3/4** — Sentinel-2 and Sentinel-1 pipelines. Verified live against
  Python on the same day: 266 cells × 7 bands at **delta 0.0**.
- **Phase 5** — pgxpool, seven tables of hand-written SQL, Werkzeug hash
  compatibility, JWT issuance, Firebase, Firestore, SMS OTP, PIN lookup, and
  the nine onboarding steps. A Python-created user with a Python-issued JWT
  logs into Go, and vice versa.
- **Phase 6** — chatbot prompt (generated from the Python source, not retyped),
  session memory, and a direct Ollama client. LangChain dropped.

**Verification harnesses**, all under `legacy-python/tools/`:

| Tool | What it proves |
|---|---|
| `exercise_endpoints.py` | every endpoint × happy/invalid/auth/edge, real requests → `docs/ENDPOINT_VERIFICATION.md` (64/64) |
| `verify_endpoints.py` | Go vs Python analysis endpoints, same day, structural + numeric diff (10/10) |
| `verify_onboarding.py` | the 9-step flow on both backends, plus cross-runtime credential/token interchange (0 failing) |
| `dump_*.py` | regenerate every golden fixture from the reference implementation |

## [1.0.0] - 2026-07-27

### Added
- Created complete 27-document enterprise engineering documentation suite under `/docs/`.
- Created dedicated subsystem architecture guides for Google Earth Engine (`03_GOOGLE_EARTH_ENGINE.md`), Sentinel-2 (`04_SENTINEL2_PIPELINE.md`), Sentinel-1 (`05_SENTINEL1_PIPELINE.md`), and Vegetation Indices (`06_VEGETATION_INDICES.md`).
- Added comprehensive API specifications (`07_API_ARCHITECTURE.md`), Backend architecture (`08_BACKEND_ARCHITECTURE.md`), and Frontend architecture (`09_FRONTEND_ARCHITECTURE.md`).
- Documented Firebase Auth integration (`10_FIREBASE_AUTH.md`), dual-database architecture (`11_DATABASE.md`), and Krishi Mitra chatbot implementation (`12_CHATBOT.md`).
- Created dedicated dashboard pages and components documentation (`18_DASHBOARD.md` to `22_COMPONENTS.md`).
- Added evaluation metrics, performance analysis (`23_PERFORMANCE.md`), limitations (`24_LIMITATIONS.md`), known issues (`25_KNOWN_ISSUES.md`), and future roadmap (`26_FUTURE_WORK.md`, `27_ROADMAP.md`).

### Changed
- Standardized documentation paths to maintain zero drift with the live source code.
- Restructured `README.md` at project root to point directly to `docs/README.md`.

### Removed
- Removed legacy unorganized root markdown files (`SYSTEM_DESIGN.md`, `DATABASE_SETUP.md`, `DATABASE_SETUP_WINDOWS.md`), consolidating their technical facts into dedicated `/docs/` subsystem manuals.
