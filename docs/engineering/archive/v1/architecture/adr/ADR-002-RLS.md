# ADR 002: Row-Level Security (RLS)

## Context
Logical isolation via `organization_id` relies heavily on application-level filtering, which is prone to developers forgetting to apply filters.

## Decision
We will enable PostgreSQL Row-Level Security (RLS) on all tenant-scoped tables as a second layer of defense.

## Consequences
- Protects against accidental leakage of data.
- Adds overhead to query parsing and connection pool setups to set the tenant context in PostgreSQL.
