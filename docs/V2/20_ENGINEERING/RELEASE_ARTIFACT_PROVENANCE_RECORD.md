# Release Artifact and Provenance Record

**Status:** Container build and release-candidate evidence workflow validated; Sigstore/Cosign signing is configured for the first candidate run.  
**Date:** 2026-08-18

## Implemented

- `apps/backend/Dockerfile` builds the Python API image from the repository root.
- `apps/frontend/Dockerfile` builds and serves the Web Chat/Admin application.
- `container-build.yml` validates both image builds on pull requests and `main`.
- `release-candidate.yml` publishes Linux/AMD64 backend and frontend images to
  GitHub Container Registry, signs their immutable digests through keyless
  Sigstore/Cosign GitHub OIDC, verifies each signature, and uploads a
  source/workflow provenance manifest for a version tag or manual run.

## Validation

- Local Docker builds completed for the backend and frontend images.
- The frontend image served a successful HTTP response on local port `3001`.
- GitHub Actions Container Build run `32107804474` passed for source revision
  `1040d5a91c6d6515a245280b2b4173c15c93bb03`.

## Signing boundary

The signing workflow uses short-lived GitHub OIDC credentials. It does not
store a signing key, package credential, or release secret in the repository.
The release owner must still approve the first workflow dispatch because it
publishes versioned images to GitHub Container Registry.

## Verification

For each release candidate, retain the uploaded image archives, checksum file,
provenance manifest, workflow URL, source revision, and validation results.
