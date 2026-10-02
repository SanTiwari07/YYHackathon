# Known Issues — preserved during the Go migration

PRD reference: `PRAGYA_GO_MIGRATION_PRD.md` §13.9.

These are **deliberately reproduced** by the Go port. Rule §0.8 forbids bundling
behavioural fixes into the migration: the frontend and the contract test suite
both depend on current behaviour, so each of these is ported as-is and fixed
afterwards in a separate, clearly-scoped commit (PRD §14 Phase 8).

Do not "fix" any of these while porting. If a Go response differs from the
Python one because of an issue below, the Go response is wrong.

| ID | Issue | Where (original Python) | Go handling |
|---|---|---|---|
| K1 | `confidence` is 0–1 in the API but documented 0–100 in `scripts/db/legacy/schema.sql` / README ("56.46%") | `stats_service.compute_confidence` | Emit 0–1. The frontend does the formatting. |
| K2 | `CVI_WEIGHTS` in `config.py` (0.70/0.10/0.05/0.10/0.05) disagree with README and the `vi_reports` comment (0.35/0.25/0.15/0.15/0.10) | `config.py` vs docs | `internal/config` uses the **config.py** values. Docs corrected in Phase 7. |
| K3 | `_interpret_cvi` docstring says 0.6/0.3; the config says 0.5/0.25 | `grid_service` | Config wins. The code was always right; only the docstring lied. |
| K4 | `.map(img => img.divide(10000))` also divides the SCL band, not just the reflectance bands | `gee_service` | Reproduced. The SCL mask is applied *before* the divide, so results are unaffected — but the graph shape must match. |
| K5 | SMS template text says **"LaundryLy"** — wrong brand, but the text is DLT-registered in India | `sms_service.send_otp` | Ported verbatim with a `// KNOWN-ISSUE` comment. Changing it silently breaks delivery; it needs re-registration, which is a product decision. |
| K6 | `/api/sample` reads a process-global last image, shared across all users and lost on restart | `app.py` | **Fixed (audit A-2, 2026-09-23).** Structurally replaced by the TTL'd `ExprCache` (§7.7), and the slot is now keyed by the verified JWT subject: `/api/*` requires a JWT (audit A-1), so the sample call carries an identity even though it carries no field id. One user can no longer sample another's analysis. Still lost on restart. |
| K7 | `GET /dashboard` runs one crops query per farm (N+1) | `dashboard.py` | Preserved for parity. Batching it is a Phase 8 change. |
| K8 | OTP store never evicts expired entries (unbounded growth) | `sms_service` | Go adds a janitor goroutine. Expiry *semantics* are identical, so this is invisible to the contract. **Still in process memory (2026-09-23):** a restart discards pending codes and two instances do not share them. Persisting them needs a legacy-schema change, which ADR 0004 freezes; the signup proof is a stateless signed token, so a code already verified survives a restart. |
| K9 | `vite.config.js` proxies `/api` only; `CLAUDE.md` documents `/chatbot` as proxied but it is not | frontend vs docs | Frontend is not modified (§0.2). The axios client reaches `/chatbot` via direct CORS, which is why CORS must be applied globally (§9.3). |
| K10 | `app._last_radar_image` is written but never read | `app.py` | The write is preserved with a `// parity: unused by any handler` comment, now under a per-owner `"__last_radar__:<subject>"` key like K6. |

## Found during Phase 0 (not in the PRD)

| ID | Issue | Where | Notes |
|---|---|---|---|
| K11 | `GET /farmer/pincode/<pin>` **always returns 500**. `api.postalpincode.in` rejects the default `python-requests/x.y.z` User-Agent with a TCP reset; any other UA works. Consequence: `POST /farmer/location` always stores empty `state`/`district`/`taluka` via the §7.10 "on any failure, continue" path. | `utils/pincode.py` (no UA header set) | **RESOLVED — fix accepted as the new baseline** (owner decision, Phase 0). Go sets an explicit non-blocked User-Agent and returns the real 200 / 404 / 500 branches per §10.10. This is the one sanctioned deviation from §0.8. The `e15_pincode_success` and `e15_pincode_notfound` goldens capture the *broken* 500 and are therefore superseded: the contract runner asserts them against the §10.10 spec instead of the golden, and they are excluded from the byte-parity gate. `POST /farmer/location` will now store real state/district/taluka, which is a data-shape change the frontend already tolerates (the fields were simply empty before). |
| K12 | `services/auth.py` mints tokens whose `sub` is the farmer UUID as a string, and `flask_jwt_extended` returns **401** (not 422) with `Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'` for a non-Bearer header. PRD §8.3's table claims 422 with different wording. | `middlewares/auth.py` via flask-jwt-extended 4.7.4 | Verified against the running app; goldens `jwt_*.json` are authoritative. The Go middleware must emit 401 here. |

## Found during Phase 5

| ID | Issue | Where | Notes |
|---|---|---|---|
| K13 | The confidence score's **cloud term is dead**. The two `.map()` calls strip image properties, so `aggregate_mean("CLOUDY_PIXEL_PERCENTAGE")` returns null; Python's `avg_cloud or 0` turns that into `0`, not the `MAX_CLOUD_COVER_PCT` fallback, so `cloud_score` is a constant `1.0` and contributes a fixed `0.30`. | `stats_service.extract_farm_statistics` | Verified against the running backend and reproduced exactly (§0.8). Only visible by diffing Go against Python live — invisible from the code. |
| K14 | `POST /farm` returns `total_area` as the **string** `"2.50"`, while `GET /dashboard` returns the same column as the **number** `2.5`. psycopg2 maps NUMERIC to `Decimal`, which Flask serialises as a string; `services/dashboard.py` explicitly calls `float()`. | `repositories/farm.py` vs `services/dashboard.py` | Both reproduced. PRD §10.10's "emit 2.5, not '2.50'" applies to the dashboard ONLY; applying it everywhere breaks `POST /farm`. |
| K15 | `POST /crop` returns `sowing_date` as **RFC 1123** (`"Sun, 15 Jun 2025 00:00:00 GMT"`), while `GET /dashboard` returns `"2025-06-15"`. Flask renders a raw `date` the first way; the dashboard calls `str()`. | `repositories/crop.py` vs `services/dashboard.py` | Both reproduced, same asymmetry as K14. |

## Post-migration changes (deliberate, not parity issues)

| Change | Detail |
|---|---|
| Chatbot backend: Ollama → **Google Gemini** | `GEMINI_API_KEY` selects the backend; with it unset the local Ollama path still works, so a developer without a key is unaffected. `/chatbot/health` keeps its three keys (`status`, `model`, `base_url`) and only the values change, which is why `e24_chatbot_health` is skipped by the contract runner and covered by `TestChatHealthReportsConfiguredBackend` instead. Two API-shape differences worth knowing: Gemini has no `system` role (the prompt goes in `system_instruction`, or the model would treat the farm statistics as user speech), and the assistant role is called `model`. On the 2.5 models `thinkingBudget` is set to 0 by default because reasoning tokens share the `maxOutputTokens` allowance — leaving it on can consume the whole 512-token budget and return an empty reply. |

## Verified PRD corrections

Captured empirically in Phase 0; the fixtures under `internal/gee/eeexpr/testdata/`
are authoritative over the PRD prose.

| PRD section | Claim | Reality |
|---|---|---|
| §5.3 | `Collection.filterDate{collection,start,end}` | `Collection.filter` + `Filter.dateRangeContains{leftValue: DateRange{start,end}, rightField:"system:time_start"}` |
| §5.3 | — | `filterBounds` → `Collection.filter` + `Filter.intersects{leftField:".all", rightValue: Feature{geometry}}` |
| §5.3 | — | `ee.Filter.lt` → `Filter.lessThan{leftField, rightValue}` |
| §11.1 | `Image.rename` takes `bandNames` | it takes `input`, **`names`** |
| §11.1 | `Image.divide(scalar)` | `Image.divide{image1, image2}`; the scalar is promoted to `Image.constant{value}` |
| §5.3 | `.median()` | `reduce.median{collection}` |
| §5.6 | `maps` body carries `visualizationOptions` + `bandIds:["NDVI"]` | body is `{expression, fileFormat:"AUTO_JPEG_PNG", bandIds:[]}`; vis params are folded into the **expression** as `Image.visualize{image,min,max,palette}` |
| §5.6 | palette hex must have `#` stripped | the `#` is **kept** — stripping it would break every tile |
| §5.5 | `~/.config/earthengine/credentials` holds `client_id`/`client_secret` | it holds only `refresh_token`, `redirect_uri`, `scopes`; the client id/secret are library constants in `ee.oauth` |
| §5.8 | `Collection.map` arg key unverified | confirmed `baseAlgorithm`, with `functionDefinitionValue{argumentNames:["_MAPPING_VAR_0_0"], body:"<ref string>"}` |
| §12.3 | `cloudy_region.json` yields zero clean scenes | mid-Pacific **has** S2 coverage and returns a success body. The real empty-collection case needs a polygon above ~84°N (`no_imagery.json`). |
| §12.3 | `tiny_plot.json` gives fewer than 2 grid cells | it gives 6. `coveringGrid` snaps to a grid, so the `n < 2` smoothing early-return is covered by a Go unit test instead. |
| §8.3 | the issued claim set is `sub, type, fresh, iat, nbf, exp, jti` | flask-jwt-extended also emits **`csrf`**. §8.3 says "if `csrf` or other claims appear, add them to the issue path" — it does, and they are. |
| §5.6 | `maps` request needs `visualizationOptions` | no such field; vis params are folded into the expression as `Image.visualize`, palette `#` retained. |

## OTP hardening (2026-09-23)

Behaviour deliberately changed from the Python reference, which accepted all of these:

| Change | Why |
|---|---|
| `/auth/signup` requires `verification_token` from `/api/auth/verify-otp` (403 without it) | Signup never checked verification, so anyone could register anyone's number: confirmed live, 201 and a login token with no OTP. The token is a stateless HMAC bound to the number, valid 10 minutes, signed with a key derived for this purpose so it is never a login JWT. |
| `/api/auth/send-otp` allows one code per number per 60 s and 5 per hour (429 with `Retry-After`) | The per-IP limit alone allowed ~120 paid SMS a minute to any victim's number, and each resend reset the wrong-guess budget. Tunable: `OTP_RESEND_COOLDOWN_S`, `OTP_MAX_SENDS_PER_HOUR`. |
| Only Indian mobiles (10 digits starting 6-9, optionally 91-prefixed) are sent a code | Any 12-digit number was sent unchanged as an international SMS on this account. |
| A gateway failure answers "Could not send the OTP right now. Please try again." | The gateway's own response body was returned to the user. It is still logged. |
