# Earth Engine Staging Verification Runbook (Task 2.21)

This runbook defines the operational verification procedure for Earth Engine service account credentials, quotas, and batch processing performance in the staging environment (Phase 5 / Sprint 11), jointly executed by P2 (Geospatial Engineer) and P6 (DevEx / Cloud Lead).

---

## 1. Prerequisites and Credentials Setup

1. **Google Cloud Project & Earth Engine API**:
   - Ensure `earthengine.googleapis.com` is enabled in the staging project.
   - Verify commercial registration or research registration is active on the Earth Engine project.

2. **Service Account Configuration**:
   - Service account name: `pragya-ee-worker@<staging-project-id>.iam.gserviceaccount.com`.
   - IAM Roles:
     - `roles/earthengine.writer` (for batch export jobs)
     - `roles/storage.objectAdmin` (for destination GCS quarantine bucket)
   - In staging, credentials are bound via Workload Identity (Kubernetes / Cloud Run) rather than long-lived keys.

3. **Destination Storage Bucket**:
   - Staging quarantine bucket: `gs://<staging-project-id>-quarantine/`
   - Staging ready bucket: `gs://<staging-project-id>-ready/`

---

## 2. Quota & Concurrency Verification Gates

Earth Engine imposes rate limits and batch export parallelism constraints:
- **Interactive requests**: 40 QPS per project.
- **Batch compute concurrency**: 2 concurrent batch exports per project (as specified in §04.7).
- **Client concurrency throttle**: The Pragya batch dispatcher bounds batch execution to `concurrency = 2`.

### Verification Step 1: Service Account Authentication Probe
```bash
# Verify credentials and access to Sentinel-2 Harmonized & Cloud Score+
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://earthengine.googleapis.com/v1/projects/<staging-project-id>/image:computePixels" \
  -H "Content-Type: application/json" -d @- <<EOF
{
  "expression": {
    "functionInvocationValue": {
      "functionName": "Image.load",
      "arguments": {
        "id": { "constantValue": "COPERNICUS/S2_SR_HARMONIZED" }
      }
    }
  },
  "fileFormat": "GEO_TIFF"
}
EOF
```
Expected response: HTTP 200 with GeoTIFF binary data, confirming active project registration.

---

## 3. Staging 1,000-Field Benchmark Verification

Execute the benchmark suite against staging PostgreSQL and live Earth Engine:

```bash
# Run benchmark with GEE_LIVE_TEST=1
export GEE_LIVE_TEST=1
export GEE_PROJECT=<staging-project-id>

go test -v -run TestBenchmark_1000FieldsSpatialBatching ./internal/pipeline -timeout 15m
```

### Pass Criteria:
1. **Concurrency limit enforced**: At no point do active Earth Engine batch tasks exceed 2.
2. **Adaptive splitting**: Polygons with >5,000 vertices or groups with >50 fields are automatically subdivided.
3. **Fault isolation**: Transient 429 / 503 errors trigger exponential backoff without failing the entire batch group.
4. **Completion time**: 1,000 fields processed in under 10 minutes (600 seconds).
5. **No 0s as missing**: Masked pixels serialize as `null`. All quality classes conform to `usable` / `partial` / `insufficient`.
