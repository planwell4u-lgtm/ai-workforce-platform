# Supabase Backend Wiring Record

**Date:** 2026-08-17  
**Status:** Implemented locally; ready for configured staging validation.

## Implemented boundary

- Staging backend startup requires a complete `DATABASE_URL` for Supabase
  PostgreSQL; it does not fall back to SQLite.
- Startup instantiates the Data-owned `PostgresTenantStore`, applies only its
  approved migrations, and verifies the migration ledger before accepting
  traffic.
- The application lifecycle owns the store and exposes `close()` for graceful
  shutdown.
- A failed connection, migration, or schema check closes the connection and
  fails startup.

SQLite remains a test-only local adapter and is not selected for the staging
backend runtime.
