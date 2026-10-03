# Adapter-swap inventory (Sprint 9 deliverable for S10/S11)

Purpose: for each local stand-in, what the production service replaces, **what must change and what must not**, and the **conformance suite that proves the
swap**. A swap is accepted when the suite passes against the real service *and* the behaviours listed under "must not change" are unchanged. Nothing in this
file has been run against a Google Cloud service: it is the checklist, not evidence. Where a suite exists it is named; where it does not, it is marked
**TO WRITE** with what it must assert.

Layering rule (`internal/archtest`): domain and platform packages depend on the ports; only `cmd/*/main.go` (and `cmd/api/wire.go`) name adapters. A swap
changes an adapter package and the wiring, never a domain.

## 1. PostgreSQL → Cloud SQL for PostgreSQL 16 (+ PostGIS)

| | |
|---|---|
| Port / code | `internal/platform/db` (`Pool`, `WithTenant`, `WithActor`), `internal/adapters/postgres`, `migrations/` |
| Local stand-in | compose `postgres` (PostGIS 16 image); this session's evidence ran on PostgreSQL **18.4 + PostGIS 3.6.2** (the 16/3.4 image never started: Docker unavailable) |
| Must change | connection path: Cloud SQL Auth Proxy / connector with IAM or password auth, private IP, TLS `verify-full`; pool sizes to the connection budget (`DB_CONNECTION_BUDGET`, `DB_RESERVED_CONNECTIONS`); the three logins (`app_runtime`, `app_maintenance`, migrator) created by Terraform, **not** by migrations (migrations create only NOLOGIN group roles) |
| Must NOT change | RLS `ENABLE` + `FORCE` on every table, `app_runtime` / `app_maintenance` without `BYPASSRLS`, the startup check that refuses a superuser / BYPASSRLS / owner login (`db.OpenRuntime`), per-tenant transactions, SECURITY DEFINER functions owned by NOLOGIN roles (`app_eraser`, `app_retention`), advisory locks, `pg_advisory_xact_lock` semantics |
| Cloud-specific risks | Cloud SQL does not grant `SUPERUSER`: `ALTER FUNCTION … OWNER TO app_eraser/app_retention` in migrations 00020/00021 needs the migrator to be a member of those roles (`GRANT app_eraser TO <migrator>`), and `CREATE EXTENSION postgis` needs `cloudsqlsuperuser`; role membership and `GRANT CREATE ON SCHEMA` steps must be rehearsed on a real instance **before** S11. `SET LOCAL` and `set_config(..., true)` are unaffected |
| Conformance | **Exists:** the whole DB-backed suite (`PLATFORM_TEST_DATABASE_URL`), notably `migrations` (up/down/up, RLS coverage, grants), `internal/platform/db` (isolation, maintenance identity, retention floors), `internal/platform/jobs`, `idempotency`. **Run it against a Cloud SQL instance with the production role layout.** **TO WRITE:** a role-layout test that fails if the migrator is a superuser (proves the migrations do not silently rely on it) |

## 2. HTTP task dispatcher → Cloud Tasks

| | |
|---|---|
| Port / code | `queue.Dispatcher` (`Create(ctx, Task)`), `internal/adapters/queue` (`HTTPDispatcher`), worker task endpoint (`internal/platform/worker`) |
| Local stand-in | direct HTTP POST to the worker with a shared token (`WORKER_TASK_URL`, `WORKER_TASK_TOKEN`) |
| Must change | `Create` becomes a Cloud Tasks `CreateTask` with the **task name derived from the dispatch id** (dedupe: creating the same name twice is `ALREADY_EXISTS`, which the adapter must treat as success), OIDC token to the worker, queue rate/concurrency from `TASK_DISPATCH_QPS` / `TASK_MAX_CONCURRENT`, dispatch deadline from `TASK_DISPATCH_DEADLINE_S` |
| Must NOT change | at-least-once delivery with **fenced leases** (a duplicate or late task must lose to the lease), "no HTTP handler waits for an entire multi-hour export", the worker validates the caller (OIDC audience/service account) and never trusts the body's tenant without loading the job |
| Conformance | **TO WRITE** `queuetest.RunDispatcher`: (a) creating the same task name twice yields one execution, (b) a task created before the job exists is retried, not lost, (c) an unauthenticated POST to the task endpoint is refused, (d) 429/5xx from the worker are retried with backoff and a 4xx (except 429) is not. The existing `internal/platform/maintenance` dispatch tests are the behavioural reference |

## 3. Event bus → Pub/Sub

| | |
|---|---|
| Port / code | `queue.Publisher`, `queue.Handler`, `queue.Inbox` (`Consume`, `ConsumeOrdered`, `VersionGuard`), `internal/adapters/queue` (`Bus`); outbox in `internal/platform/maintenance` |
| Local stand-in | in-process `Bus` (no subscriptions yet) |
| Must change | `Publish` → Pub/Sub publish with `ordering_key` **not required** (ordering is handled by `VersionGuard`, T06); the private push endpoint `POST /internal/events` validates the OIDC invoker, size, schema and originating project (spec §04) before inserting the inbox key; dead-letter topic and retry policy |
| Must NOT change | outbox row published only after commit; **consumer dedupe by (consumer, event id) in the same transaction as the effect**; out-of-order and duplicate events are safe (T06); a consumer never depends on delivery order or exactly-once |
| Conformance | **Exists:** `internal/platform/queue` (`Inbox`, `ConsumeOrdered`, out-of-order/duplicate tables, T06) and `internal/platform/maintenance` outbox tests — run them with a Pub/Sub-backed `Publisher` between outbox and inbox. **TO WRITE:** an end-to-end publish → push → inbox test with duplicate and reordered delivery injected at the emulator |

## 4. Object storage → Cloud Storage (two buckets)

| | |
|---|---|
| Port / code | `storage.Bucket` (`ReserveUpload`, `Stat`, `Open`, `Promote`, `Delete`, `SignedDownload`, `List`, `Ping`), `internal/adapters/storage` (`gcs.go`, `proxy.go`) |
| Local stand-in | fake-gcs-server (native in this session, compose image otherwise); the dev capability proxy signs local URLs (dev only) |
| Must change | real V4 signed URLs by the attached service account (no downloaded key files), separate IAM per bucket (**quarantine**: client PUT via signed URL, maintenance read + delete; **ready**: promote by the validator identity only, signed download by the API), lifecycle rules as a backstop to the retention duties, regional location per tenant policy, uniform bucket-level access |
| Must NOT change | keys of the layout `tenant/<uuid>/<purpose>/<uuid>/<version>/<sha256>.<ext>`; **no code path reaches `Promote` without a passing validation record** (T17); `Promote` reads exactly the verified generation and creates the ready object only if none exists; retention never touches the ready zone except for reports; orphan objects are found by listing, not assumed absent |
| Conformance | **Exists:** `storagetest.Run(t, Harness)` — the same suite runs against `Memory` (always) and fake-gcs (`PLATFORM_TEST_STORAGE_URL`). **Run it against a real GCS bucket pair.** **TO WRITE:** an IAM test (quarantine service account cannot write the ready bucket) and a signed-URL expiry test on real time |

## 5. Identity → Identity Platform

| | |
|---|---|
| Port / code | `auth.TokenVerifier`, `auth.NewFirebaseVerifier(project)`, `authtest`, `emulator_test.go` |
| Local stand-in | Firebase Auth emulator (native in this session, compose image otherwise) |
| Must change | `IDENTITY_PROJECT_ID` to the real project; verifier keys fetched from Google's JWKS with caching; **App Check** / multi-tenancy decisions are product items (not in P1); email verification claim source |
| Must NOT change | audience **and** issuer both checked against the project; internal user id derived from (issuer, subject) only (`DerivedResolver`), never from an email; an unverified email is never treated as verified (invitation acceptance); a suspended member is denied on the next request |
| Conformance | **Exists:** `internal/platform/auth` (verifier tables) and `internal/apiv1/emulator_test.go` (real emulator tokens through the real router). **TO WRITE:** a staging smoke that mints a real Identity Platform token and calls `GET /v1/me` |

## 6. Cache and counters → Memorystore for Redis

| | |
|---|---|
| Port / code | `cache.Store`, `ratelimit.Counter`, `internal/adapters/redis`, `redistest` |
| Local stand-in | compose `redis:7-alpine`; this session ran **Redis 7.2.6 built from source in WSL** for the conformance test and T25 |
| Must change | `REDIS_ENDPOINT` = the private Memorystore address, `REDIS_TLS_ENABLED=true` with the server certificate authority (the adapter takes a `tls.Config`; wiring currently uses the system pool with TLS 1.2 minimum — add the instance CA), `REDIS_AUTH_SECRET` from Secret Manager, HA tier |
| Must NOT change | every key has a TTL; no key is ever the only record of anything; a Redis failure is a miss or a local decision, never an error to an authorised caller; keys are namespaced by environment and cell; `maxmemory-policy allkeys-lru`, no persistence |
| Conformance | **Exists:** `internal/adapters/redis` (`redistest` behaviours + `conformance_test.go`, real server via `REDIS_TEST_ADDR`), `TestT25AgainstARealRedis`. **Run both against Memorystore** (TLS + AUTH). **TO WRITE:** a failover drill (primary failover mid-run: the breaker opens, shedding stays bounded, service resumes) |

## Sequencing advice for S10/S11

1. Cloud SQL role layout rehearsal (§1) — it is the only swap that can invalidate migrations already written.
2. GCS and Identity Platform (§4, §5): the suites exist; they only need real credentials.
3. Cloud Tasks and Pub/Sub (§2, §3): write the two missing suites first; both must prove duplicate-safe delivery, which is the property everything above relies on.
4. Memorystore (§6) last: it is optional to correctness, so a late or failed swap cannot block a release.
