# Authentication Design

How users and external integrations verify identity.

## User Authentication

- **Identity Provider:** OpenID Connect (OIDC) / OAuth 2.0 (e.g. Auth0, Clerk, or self-hosted Ory).
- **Session Mechanism:** JSON Web Tokens (JWT) signed via RS256 algorithm.
- **MFA:** Enforced for administration dashboards (Google Authenticator / SMS fallback).

## API Authentication

- **API Keys:** Generated as cryptographically secure random values (`ag_live_...`).
- **Storage:** SHA-256 hashed values are stored in the database.
