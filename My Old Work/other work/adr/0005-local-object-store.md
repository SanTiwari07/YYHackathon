# ADR 0005 — Local object store: MinIO for now, decision gate before Sprint 4

- **Status:** **Superseded by ADR 0009** (2026-09-20): the spike ran and fake-gcs-server was chosen. Kept for the record.
- **Date:** 2026-09-19
- **Owner:** P1 (platform)
- **Spec:** 6182 §06.4, §07.6, §09.4

## Context

The plan names MinIO as the default local stand-in for Cloud Storage and allows
fake-gcs-server "if S1 spikes show GCS-specific semantics matter". Two facts
argue for a deliberate decision rather than silently taking the default:

1. **The spec relies on GCS-specific behaviour.** Object writes and promotion
   use *generation preconditions* to avoid overwrite races (§07.6); quarantine
   and ready buckets have different IAM; signed URLs are the download and upload
   capability (§06.4, §09.4). MinIO speaks the S3 API, which has no generation
   number; a MinIO-backed adapter would exercise a different concurrency
   mechanism (ETag / version-id) than production.
2. **MinIO's community edition is no longer distributed the way the plan assumes.**
   Verified 2026-09-19: the `minio/minio` repository no longer exists on Docker Hub
   (the API answers 404 and `docker pull minio/minio:<tag>` is denied). The official
   registry is now `quay.io/minio/minio`, whose newest plain release is
   `RELEASE.2025-09-07T16-13-09Z` (Sep 2025); only `.hotfix` builds have been
   published since (latest seen: `RELEASE.2025-09-07T16-13-09Z.hotfix.7aa24e772`,
   Apr 2026). Treat the community edition as maintenance-only.

## Options

| Option | For | Against |
|---|---|---|
| **MinIO** (plan default) | S3-compatible, widely known, has console | GCS semantics differ (no generation preconditions); community edition in maintenance |
| **fake-gcs-server** | Same API family as production (Phase 5 swap changes the endpoint, not the client); supports generation preconditions | Smaller project; signed-URL semantics are emulated, not enforced |

## Decision (provisional)

Phase 0 ships MinIO in `docker-compose.yml` as the plan states, so the stack is
complete and the Phase 0 exit criterion can be evaluated. The pinned image is
`quay.io/minio/minio:RELEASE.2025-09-07T16-13-09Z`, digest
`sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e`
(pulled, started, `/minio/health/live` and `/ready` return 200, `mc` present for the
healthcheck). The `.hotfix` builds were deliberately not adopted: they are unverified
here and the stack is loopback-only local development; revisit when the spike runs. **Before
Sprint 4**, P1 runs a one-day spike: implement `PutQuarantine` → `Promote` with a
generation precondition against both emulators and choose. If fake-gcs-server
passes, replace the compose service and record the change here (superseding
this ADR); if not, keep MinIO and document how the precondition is emulated
(e.g. conditional copy on ETag) and why that is an acceptable proxy.

## Consequences

- No storage code is written against S3-specific or GCS-specific types in
  Phase 0–1.
- The `storage.Bucket` port (`internal/platform/storage`) is designed against the
  specification's requirements, not against either emulator.
