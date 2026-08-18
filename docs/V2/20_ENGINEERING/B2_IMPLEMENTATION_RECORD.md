# B2 Implementation Record — Contracts and Tenant-Safe Local Persistence

**Status:** Implemented locally; PostgreSQL production adapter deferred.  
**Owner:** Data Platform with Agent, Conversation, and Integration domain owners.  
**Date:** 2026-08-10

## Decisions and scope

- SQLite is the local-only persistence adapter. It is not a production database decision.
- `tenant-record` v1 is an opaque, versioned contract for the initial Agent, Conversation, and Action records. Domain payload semantics remain with the owning domain.
- Every read and write requires a server-resolved `TenantScope` containing tenant, environment, and correlation references. The storage adapter does not accept a client tenant filter.
- The migration ledger is idempotent and fails closed when it finds an unknown migration. Schema verification is the local recovery gate before reuse.

## Validation and recovery

`tests/data/test_sqlite_store.py` proves tenant and environment isolation, contract-version rejection, bounded record kinds, repeatable migration, schema verification, and reopen/recovery of local data.

Before production release, replace the adapter with Data-owned PostgreSQL migration tooling; define backup/restore, secrets, residency, retention/hold, concurrency, and operational evidence.
