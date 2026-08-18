# Backend Application

The protected API composition root validates Auth0 RS256 access tokens against
the configured tenant JWKS endpoint. Configure `AUTH0_DOMAIN`,
`AUTH0_AUDIENCE`, and `APP_ENV` through deployment configuration; do not put
issuer keys or bearer tokens in source control.

The verifier establishes an issuer-bound Auth0 subject only. Tenant membership
and permissions remain server-owned decisions.
