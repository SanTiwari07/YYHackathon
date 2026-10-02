# Local stack (new platform)

One command brings up everything the new platform needs locally (plan section 3).
Nothing here touches the legacy application, which keeps its own `.env`,
`Dockerfile` and `make run`.

```bash
make up                                  # docker compose up -d --build --wait, then make migrate
docker compose ps                        # every service should be "healthy"
docker compose down                      # stop; add -v to also drop the data volumes
```

| Service | Image / build | Host port (127.0.0.1 only) | Stands in for (Phase 5) |
|---|---|---|---|
| `postgres` | `postgis/postgis:16-3.4`, database `farmer` | 5434 | Cloud SQL PostgreSQL + PostGIS |
| `redis` | `redis:7-alpine`, cache-only settings | 6380 | Memorystore |
| `fake-gcs` | `fsouza/fake-gcs-server:1.56.1` (digest-pinned) | 4443 (GCS JSON API) | Cloud Storage (ADR 0009) |
| `firebase-emulator` | `docker/firebase-emulator` (firebase-tools, Auth only, project `demo-pragya`) | 9099 | Identity Platform |
| `api` | `docker/platform.Dockerfile --target api` | 8081 | Cloud Run API |
| `worker` | `docker/platform.Dockerfile --target worker` | none (private task endpoint on the compose network) | Cloud Run worker + Cloud Tasks target |
| `maintenance` | `docker/platform.Dockerfile --target maintenance` | none | Cloud Run Jobs: outbox publisher, dispatch sweep, reaper, asset validation |

Host ports differ from the service defaults on purpose (5434 for PostgreSQL, 6380
for Redis, 8081 for the API) so the stack does not collide with a PostgreSQL,
Redis or Apache already running on a developer machine. Override any of them with
`PLATFORM_*` variables, for example `PLATFORM_POSTGRES_PORT=5440 docker compose up -d`.
The legacy `.env` is not read. If `docker compose up` reports "ports are not
available", something on the host already holds that port: check
`netstat -ano | findstr :<port>` and override the variable.

## Sprint 4 additions

| | |
|---|---|
| `maintenance` login | `pragya_maintenance` (override `PLATFORM_DB_MAINTENANCE_USER`), member of `app_maintenance`, created by the init script next to the runtime login. Only `cmd/maintenance` holds it (ADR 0010). **The init script changed: recreate the Postgres volume once** (`docker compose down && docker volume rm pragya-platform_pgdata && make up`). |
| Job execution | `maintenance` scans (outbox, queued jobs, expired leases, quarantined uploads) and pushes named tasks over HTTP to the worker's **private** task endpoint (`WORKER_TASK_ADDR`, bearer `WORKER_TASK_TOKEN`; not published on the host). The worker runs handlers registered in `cmd/worker/handlers.go`. |
| Object store | `fake-gcs` on `4443`; the API creates the `quarantine` and `ready` buckets at start (`STORAGE_ENSURE_BUCKETS=1`, dev only). Browsers upload to `PUT {API_ORIGIN}/local-storage/upload/{token}` (a dev capability proxy that enforces key, content type, exact size and expiry; refused outside `ENVIRONMENT=dev`). |
| Health | `/readyz` reports `database` and `storage`; `/livez` stays process-only. |

## The application database

| | |
|---|---|
| Database name | `farmer` (spec 6182 s16 `DB_NAME` default; override with `PLATFORM_DB_NAME`) |
| Created by | `POSTGRES_DB` in `docker-compose.yml`, when the `pgdata` volume is first initialised. The postgis image installs PostGIS into it. |
| Schema owner / migrations | the `postgres` superuser, via `make migrate` (goose up). `make up` runs it after the stack is healthy. |
| Runtime login | `pragya_runtime` (override `PLATFORM_DB_RUNTIME_USER`), created by `docker/postgres-init/20-runtime-role.sh` on first init: LOGIN, member of `app_runtime`, NOSUPERUSER, NOBYPASSRLS, owns nothing. |
| api/worker settings | `DB_HOST=postgres`, `DB_PORT=5432`, `DB_NAME`, `DB_RUNTIME_USER`, `DB_RUNTIME_PASSWORD` (set in compose). `DB_NAME` and `DB_RUNTIME_USER` are spec s16 names; host, port and password are local wiring, replaced in Phase 5 by the Cloud SQL connector and IAM authentication. |
| From the host | `postgres://postgres:<throwaway>@127.0.0.1:5434/farmer` (migrations, psql); the runtime login on the same port. |

`cmd/api` and `cmd/worker` connect at startup **only if `DB_HOST` is set**, and refuse to run
(exit 1) if the connection fails or the role is a superuser, has BYPASSRLS or owns an application
table (`db.OpenRuntime`). Neither uses the pool yet; connecting early makes a wrong name or
credential fail at start-up. A half-set configuration (for example `DB_RUNTIME_USER` without
`DB_HOST`) is a configuration error, not a silent "no database".

Init scripts run **only on an empty data volume**. After changing the database name, the runtime
login or `docker/postgres-init/`, recreate the volume (this deletes the local database):

```bash
docker compose down
docker volume rm pragya-platform_pgdata
make up
```

`make migrate-status` shows the applied version. `make migrate-verify` deliberately uses a
scratch database (up, down to 0, up), so it never wipes `farmer`.

Passwords are throwaway values for disposable local containers and are bound to
loopback only. They are not secrets; do not reuse them, and never put real
credentials in `docker-compose.yml`.

`cmd/tile` is added to the stack in Sprint 6 when it exists.

## Tests against the stack

```bash
make up                # once
make platform-test-db  # every new-stack test, with PostGIS and the Firebase emulator REQUIRED
make migrate           # goose up on the application database (farmer); make up already does this
make migrate-verify    # real goose: up, down-to 0, up on a SCRATCH database
```

SQL integration tests create and drop their own database and a throwaway login role with a random
password per test; nothing persistent is created and no credential is stored. `go test -race`
cannot run on the Windows dev box (only a 32-bit C compiler); run it in the Linux Go image on the
compose network, which is how the Phase 1 race run was done.

## Contract and mock

```bash
make contract-lint     # Redocly lint of contracts/openapi.json
make mock              # Prism mock of the contract on http://127.0.0.1:4010
go test ./contracts    # offline structural + security invariants of the contract
```

The mock runs in static mode (Prism's dynamic mode, `-d`, hangs on this contract). It enforces the contract: missing bearer token →
401, missing `Idempotency-Key` or `If-Match` → 422, unknown request properties →
422 (bodies are closed), and it returns the spec's own example payloads where
the contract carries them. Prism reports 422 for header/body violations rather
than the real API's 409/412/428 problem codes; do not treat mock status codes for
validation failures as the API's behaviour.

## Native run (no Docker)

```bash
PORT=8080 ENVIRONMENT=dev go run ./cmd/api      # GET /livez, /readyz
go run ./cmd/worker
# with the database of the running stack:
#   DB_HOST=127.0.0.1 DB_PORT=5434 DB_RUNTIME_USER=pragya_runtime DB_RUNTIME_PASSWORD=... go run ./cmd/api
```

### DB-backed tests without Docker

When Docker Desktop is unavailable, the full suite runs against native processes instead of the
compose containers:

```bash
# 1. Throwaway PostgreSQL + PostGIS (any version >= 16 with PostGIS installed)
initdb -D ./pgdata -U postgres --auth=trust --encoding=UTF8 --locale=C
pg_ctl -D ./pgdata -l pg.log -o "-p 5455 -c listen_addresses=127.0.0.1" start
psql -h 127.0.0.1 -p 5455 -U postgres -d template1 -c "CREATE EXTENSION postgis"

# 2. Object store and identity emulators
go install github.com/fsouza/fake-gcs-server@v1.56.1
fake-gcs-server -scheme http -port 4443 -backend memory &
firebase emulators:start --only auth --project demo-pragya --config docker/firebase-emulator/firebase.json &

# 3. The suite, with every dependency REQUIRED (a missing one fails instead of skipping)
export PLATFORM_REQUIRE_DB=1 PLATFORM_REQUIRE_STORAGE=1 PLATFORM_REQUIRE_EMULATOR=1
export PLATFORM_TEST_DATABASE_URL="postgres://postgres@127.0.0.1:5455/postgres?sslmode=disable"
export PLATFORM_TEST_STORAGE_URL=http://localhost:4443 FIREBASE_AUTH_EMULATOR_HOST=127.0.0.1:9099
go test -p 1 -count=1 ./...
```

- **The emulator project must be `demo-pragya`**, the default of `IDENTITY_PROJECT_ID` and what CI
  uses. Starting it with the real Firebase project from `.firebaserc` makes every emulator-token
  test fail with `auth: invalid token`.
- **`-p 1` is required:** packages share cluster-level roles, and running them in parallel against
  one cluster collides on `app_runtime`.
- `go test ./...` **without** `PLATFORM_REQUIRE_DB=1` skips every SQL test and is not a meaningful
  signal for anything that touches PostgreSQL.
- `govulncheck` results depend on the local Go patch level. Check with the toolchain CI resolves
  (`go-version: 1.25.x`, i.e. the latest 1.25 patch), not an older local install.

## Legacy stack

Unchanged: `go run ./cmd/server` (port 5000), `make verify` (needs a server on
5001 and, for the full contract suite, a PostgreSQL with the legacy schema).
