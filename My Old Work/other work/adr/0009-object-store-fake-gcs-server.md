# ADR 0009 — Local object store: fake-gcs-server (supersedes ADR 0005)

- **Status:** Accepted (E4, approved 2026-09-20: "choose based on the Bucket port tests and GCS generation-precondition fidelity")
- **Owner:** P1 (platform)
- **Spec:** 6182 §06.4, §07.6, §09.4

## The spike

ADR 0005 required a one-day spike before Sprint 4: run the semantics the `Bucket` port depends on against both candidates and choose.
Both emulators were **built from source** (Go 1.26.5; `fake-gcs-server` v1.56.1, `minio` at `7aac2a2c5b7c`) and run natively, because Docker Desktop
could not start on the development machine (the known stale `dockerInference` file). MinIO was probed over the S3 API with a stdlib
SigV4/presign client, fake-gcs-server over the GCS JSON API with `curl`. Both probe transcripts are reproduced below.

| Behaviour the port relies on | fake-gcs-server 1.56.1 | MinIO |
|---|---|---|
| **Create-only write** (`ifGenerationMatch=0` / `If-None-Match: *`) — the quarantine write and the ready write | ✅ 200, then **412** | ✅ 200, then **412** |
| **Conditional overwrite** (generation / `If-Match` ETag) | ✅ 412 on a wrong generation, 200 on the right one | ✅ 412 / 200 |
| **Read pinned to the verified bytes** (`?generation=G` / `If-Match`) | ✅ an overwritten generation is **404** | ✅ stale ETag is **412** |
| Real **generation numbers** in metadata (what the spec's "generation preconditions" are) | ✅ int64 generation, `metageneration`, `md5Hash`, `crc32c` | ❌ ETag only (content identity, not a version: re-uploading identical bytes yields the same token) |
| Copy with source precondition | ❌ ignored (200 with a stale generation) | ✅ 412 |
| Copy with destination create-only | ❌ ignored | ❌ ignored |
| Delete with precondition | ❌ ignored | ❌ ignored |
| **Signed upload URL enforced** (signature, content-type, expiry, key) | ❌ no PUT upload endpoint on this version (`invalid uploadType`); nothing signed | ✅ 200 / 403 wrong type / 403 expired / 403 tampered key |
| Size bound in the URL | ❌ | ❌ (a larger body was accepted) |
| Same API family as production (Phase 5 = same requests, real endpoint + OAuth) | ✅ GCS JSON API | ❌ S3 API: a throwaway adapter |

## Decision

**fake-gcs-server.** The specification's guarantee is *generation preconditions* (§07.6), and only fake-gcs-server models a generation. The two
guarantees the port needs are create-only writes and reads pinned to what was verified, and **both emulators enforce those**; the emulators' shared weak
spots (copy destination and delete preconditions) are avoided by design: `Promote` is a **pinned read from quarantine + create-only write to ready**,
never a server-side copy, and deletes are treated as idempotent cleanup. The adapter speaks the plain GCS JSON API over `net/http` (no Google SDK
before Sprint 11, AGENTS.md rule), so in Phase 5 the same adapter runs against Cloud Storage with an OAuth token supplied by the environment.

What fake-gcs-server does not give us — an enforced signed URL — is supplied by the adapter, which is *stricter* than either emulator: the local upload
and download URLs point at a small **capability proxy** (`internal/adapters/storage.LocalProxy`, mounted by `cmd/api` only in `ENVIRONMENT=dev` with a
configured secret). A URL carries an HMAC-signed token binding one key, one content type, one exact size and an expiry; the proxy enforces all four,
streams to the emulator with `ifGenerationMatch=0`, and never lets a client reach the emulator directly. Its conformance tests prove the binding, so the
contract the frontend codes against (`PUT` the bytes to `upload_url` with `required_content_type`) is the production one.

## Consequences

- `docker-compose.yml` replaces the MinIO service with `fsouza/fake-gcs-server:1.56.1` (tag verified against Docker Hub on 2026-09-20; digest
  `sha256:797ce226d62f947c009dc40246b30cfb456b8473d8241407f9d6f2c04e4d69ef`, the version tested in the spike). **The image itself could not be started in
  this session (Docker Desktop was down); the pinned build was exercised as the identical native binary.** Its health check is therefore left at
  `service_started` rather than an unverified probe command.
- The adapter creates the two buckets on startup when `STORAGE_ENSURE_BUCKETS=1` (development only); in Phase 5 they are Terraform resources with different
  IAM (quarantine writable by the API's upload identity, ready readable by it and writable only by the promoter).
- `internal/platform/storage/storagetest` is the conformance suite of the port: the same tests run against fake-gcs-server now and against Cloud Storage in
  Sprint 11, which is what makes the adapter swap provable.
- MinIO stays out of the stack. If a later need for an S3-compatible store appears, an adapter can be written against the same suite.

## Spike transcript (abridged)

```
fake-gcs-server 1.56.1   create-only 200 / 412 | conditional overwrite 412 / 200 | pinned read of an overwritten generation 404
                         copy (stale source generation) 200 !  copy (dest exists) 200 !  delete (stale generation) 200 !  XML PUT 400
MinIO                    create-only 200 / 412 | If-Match overwrite 412 / 200 | copy source If-Match stale 412 | copy dest If-None-Match:* 200 !
                         GET If-Match stale 412 | DELETE If-Match stale 204 ! | presigned PUT 200 | wrong type 403 | expired 403 | wrong key 403 | oversize body 200
```
