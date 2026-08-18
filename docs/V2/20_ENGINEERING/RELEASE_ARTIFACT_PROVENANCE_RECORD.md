# Release Artifact and Provenance Record

**Status:** Container build and release-candidate evidence workflow validated; signing remains an owner gate.  
**Date:** 2026-08-18

## Implemented

- `apps/backend/Dockerfile` builds the Python API image from the repository root.
- `apps/frontend/Dockerfile` builds and serves the Web Chat/Admin application.
- `container-build.yml` validates both image builds on pull requests and `main`.
- `release-candidate.yml` creates Linux/AMD64 image archives, `SHA256SUMS`, and
  a source/workflow provenance manifest for a version tag or manual run.

## Validation

- Local Docker builds completed for the backend and frontend images.
- The frontend image served a successful HTTP response on local port `3001`.
- GitHub Actions Container Build run `32107804474` passed for source revision
  `1040d5a91c6d6515a245280b2b4173c15c93bb03`.

## Remaining signing gate

GitHub artifact attestations require `id-token: write`, `attestations: write`,
and a plan that supports private-repository attestations. The current private
repository must not claim signed provenance until the accountable release owner
selects and enables an approved signing/attestation service.

## Verification

For each release candidate, retain the uploaded image archives, checksum file,
provenance manifest, workflow URL, source revision, and validation results.
