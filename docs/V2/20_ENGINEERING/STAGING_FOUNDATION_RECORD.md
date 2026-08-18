# Staging Foundation Record

**Date:** 2026-08-16  
**Status:** Verified

## Completed

- B0-B9 local first vertical-slice implementation is complete, with local test evidence.
- Auth0 is configured as the staging identity provider with the approved API audience, RBAC, and access-token permissions.
- A Supabase-managed PostgreSQL staging project is configured.
- The backend PostgreSQL tenant-record adapter was added and verified against the hosted database.
- The hosted migration created `schema_migrations` and `tenant_records`; the temporary verification record was removed after the isolation check.
- Supabase MCP access is connected for future managed database checks and migrations.

## Deliberate Boundaries

- Auth0 remains the identity provider; Supabase Auth is not enabled for this path.
- Browser clients do not receive database credentials.
- SQLite remains available for local fast tests; PostgreSQL is the approved hosted persistence path.
- Database secrets remain in the ignored local `.env` file only.

## Next Action

Configure Jira Service Management as the support-ticket destination. Obtain and store the service-desk identifier, request-type identifier, and a scoped integration credential without committing secrets.

## Verification Evidence

- PostgreSQL tenant-scope integration test passed against the hosted Supabase project.
- Local lint and static type checks for the PostgreSQL adapter passed.
