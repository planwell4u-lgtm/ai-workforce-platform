# 03_DATA_STORAGE_AND_POSTGRESQL_ARCHITECTURE

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the shared relational storage architecture built on Supabase-managed PostgreSQL. It covers logical database boundaries, connection/access patterns, tenant scope, schema ownership, transaction rules, operational controls, and portability.

PostgreSQL is a Data Platform mechanism. It does not define domain semantics, tenant authority, enterprise authorization, or public cross-module APIs.

# Purpose

Provide a dependable relational foundation for domain-owned records while preventing shared-database coupling, unscoped access, unsafe administrative access, schema drift, and provider lock-in.

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Domain table semantics, canonical IDs, lifecycle, access meaning, or business rules | Owning domain platform |
| Tenant/membership/entitlement/configuration/API-edge facts | 16_PLATFORM_FOUNDATION |
| Identity, authorization policy, secrets, cryptography, compliance, or audit infrastructure | 09_SECURITY_PLATFORM |
| Vector representation/index design | 04_DATA_VECTOR_AND_PGVECTOR_ARCHITECTURE.md |
| Retention/deletion/backup/restore policy mechanics | Data documents 06–07 |

# Principles

## Domain-Owned Schemas, Data-Operated Foundation

Each domain owns its logical schema and migration intent. Data Platform owns shared PostgreSQL standards, provisioning, connection policy, migration execution controls, performance, recovery, and physical operational evidence.

## Contracted Access Only

No domain reads or writes another domain's tables directly. Cross-domain needs use versioned APIs, events, or approved projections. Shared PostgreSQL infrastructure does not imply shared table authority.

## Server-Resolved Tenant Scope

All queries, transactions, jobs, admin paths, and maintenance operations use trusted tenant/environment scope from Platform Foundation/Security context. Client fields, connection strings, provider accounts, row keys, or URLs cannot select or widen scope.

## Transaction and Outbox Discipline

Changes requiring durable events use an approved transactional outbox or equivalent pattern. A transaction commits only its owned data and required outbox evidence; consumers revalidate scope and idempotency.

# Logical Storage Model

| Layer | Responsibility | Boundary |
|---|---|---|
| Domain schema | Tables, constraints, domain-owned projections, owned migrations. | No other domain direct access. |
| Shared data schema | Migration metadata, representation/lineage, operational support tables under Data ownership. | No domain semantic authority. |
| Security/admin schema | Security-managed access/audit support where approved. | Not a business-data shortcut. |
| Extensions schema | PostgreSQL extensions such as pgvector under Data-controlled configuration. | No ordinary application objects. |

Schema, table, index, connection, and role naming follow an approved convention. Provider-specific Supabase schema defaults and RLS behavior are reviewed controls, not substitutes for platform access architecture.

# Access and Connection Boundary

Application workloads authenticate using distinct Security-managed identities and least-privilege connection/lease mechanisms. Direct database connectivity is limited to approved Data-owned service paths, migrations, controlled operations, and explicitly authorized administration.

Frontend, Agent, Conversation, Voice, Digital Channel, and Integration code do not receive broad database credentials or query shared tables directly. Supabase Auth, Storage, Realtime, Edge Functions, and public client keys are not implicitly selected by ADR-005 and require separate decisions.

# Tenant Isolation and Query Rules

Every tenant-scoped table has an immutable tenant/environment binding, appropriate constraints/indexes, and mandatory server-side query predicates or equivalent Data/Security-enforced scope. Unscoped bulk reads, wildcard joins, client-provided tenant filters, cross-tenant foreign keys, and tenant-blind maintenance jobs are prohibited.

RLS may be used as defense in depth only when an approved Security/Data design defines claims, roles, bypass prevention, operational paths, testing, and audit. It does not remove service-side authorization, domain access checks, or tenant context validation.

# Schema Migration and Operations

Migrations are versioned, reviewed, idempotent where possible, tenant-safe, observable, backward-compatible or explicitly staged, rollback-aware, and tested against realistic volume and failure. Material migrations record domain owner, data classification, lock/performance impact, lifecycle/residency effects, backfill/verification, rollback, and audit evidence.

Data operations monitor connection health, transaction/error/lock latency, index health, capacity, replication/backup state, migration status, tenant-safe query pressure, and recovery readiness. Raw row content, credentials, and unrestricted identifiers are excluded from routine diagnostics.

# Portability and Recovery

Canonical domain records and required audit evidence must be exportable independently of Supabase. Provider-specific configuration, pooler behavior, or extension use cannot strand canonical data. Restore, replica promotion, migration, or region recovery revalidates current tenant, lifecycle, deletion/hold, access, residency, and schema compatibility before data is usable.

# Required Implementation Artifacts

| Artifact | Purpose |
|---|---|
| PostgreSQL schema/ownership standard | Defines schema boundaries, naming, constraints, tenant bindings, and direct-access prohibition. |
| Connection and workload identity standard | Defines least privilege, leases, pooling, admin access, rotation, and audit. |
| Migration/outbox standard | Defines versioning, compatibility, backfill, events, verification, rollback, and evidence. |
| PostgreSQL operations/runbook catalog | Defines performance, capacity, incident, backup/recovery, and provider exit controls. |
| Storage conformance suite | Proves isolation, transaction/outbox, migration, access, portability, and recovery safety. |

# Anti-Patterns

## Shared Database Means Shared Table Access

Infrastructure is shared; ownership and access remain domain-specific and contractual.

## RLS Is the Whole Authorization Model

RLS is optional defense in depth, not a replacement for Security, domain, and service-side controls.

## Supabase Client Key Is a Backend Boundary

Public/client connectivity does not authorize broad domain access or replace approved service contracts.

## Migration Success Means Data Is Valid

Migration completion requires verification, tenant/lifecycle/residency checks, and domain-owner acceptance where material.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Data Storage and PostgreSQL architecture covering schema ownership, access, tenant scope, migrations, operations, portability, and recovery. |
| 1.1 | 2026-08-07 | Approved after completeness, ownership, and long-term maintainability review. |
