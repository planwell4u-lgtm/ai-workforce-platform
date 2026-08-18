# Auth0 Backend Wiring Record

**Date:** 2026-08-17  
**Status:** Implemented locally; ready for configured staging validation.

## Implemented boundary

- The backend composition root now requires `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, and `APP_ENV`.
- `Auth0JwtVerifier` validates Auth0 access tokens using the tenant's JWKS endpoint.
- Only RS256 tokens with a key ID are accepted. Issuer, audience, expiry,
  issued-at time, and subject are required and validated.
- JWKS retrieval and all token-validation failures deny authentication; bearer
  credentials and provider errors are not exposed in the API response or audit
  reason.
- The verified Auth0 `sub` becomes the external principal reference. Tenant
  membership and permissions remain server-owned and are intentionally not
  trusted from the token.

## Configuration

`AUTH0_DOMAIN` is the Auth0 tenant hostname (without a scheme or path), and
`AUTH0_AUDIENCE` must exactly match the configured API audience. No Auth0
private key is stored by or required in the backend.

## Validation

Focused tests cover valid RS256 authentication and rejection of wrong issuer,
wrong audience, expired token, unsupported algorithm, missing bearer token,
and JWKS retrieval failure.
