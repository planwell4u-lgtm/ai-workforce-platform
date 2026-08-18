# ADR 001: Multi-Tenancy

## Context
The platform needs to support multiple organizations (tenants) with strict data isolation.

## Decision
We will use a shared database schema with a logical isolation approach using an `organization_id` column on all tenant-scoped tables.

## Consequences
- Requires strict validation on all query entry points.
- Enables simple database administration and scaling compared to database-per-tenant designs.
