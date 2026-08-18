# Release Artifact and Provenance Record

**Status:** First GitHub Container Registry release candidate published, signed, and verified.  
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
- Release-candidate run [`32108470562`](https://github.com/planwell4u-lgtm/ai-workforce-platform/actions/runs/32108470562)
  completed successfully for source revision
  `432b6c12febbf09237d3ab74aed7267aaea4b7a2`.
- The run published, keylessly signed through GitHub OIDC, and verified these
  immutable image references:
  - `ghcr.io/planwell4u-lgtm/ai-workforce-backend@sha256:43b4eaae264e68ac8f54bf680d3d96e6b861f9faa0a40d0f169ff70d902a8733`
  - `ghcr.io/planwell4u-lgtm/ai-workforce-frontend@sha256:c9faed6eea868ab652736382846e2ec63d09d2f3f8ca1bf97ce1d47954129135`
- The signed provenance manifest is retained as the run artifact
  `ai-workforce-release-432b6c12febbf09237d3ab74aed7267aaea4b7a2`.

## Signing boundary

The signing workflow uses short-lived GitHub OIDC credentials. It does not
store a signing key, package credential, or release secret in the repository.
The release owner must still approve the first workflow dispatch because it
publishes versioned images to GitHub Container Registry.

## Verification

For each release candidate, retain the uploaded image archives, checksum file,
provenance manifest, workflow URL, source revision, and validation results.
