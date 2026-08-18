# 09_DATA_ACCESS_AND_TENANT_ISOLATION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines Data Platform enforcement of tenant, environment, domain, subject, purpose, representation, storage, queue, cache, backup, and administrative isolation.

Data applies authoritative Platform Foundation and Security facts to physical mechanisms. It does not create a separate tenant or authorization model.

# Principles

## One Trusted Scope per Representation

Every table row, object, vector, index record, cache entry, queue message, backup, export, replica, migration, and operational record carries immutable tenant/environment and owning-domain scope. Cross-scope access requires an explicit governed platform administration relationship.

## Server-Resolved, Revalidated Scope

Tenant/environment comes from trusted server-side context and is validated at every read, write, query, transaction, job, restore, export, support, and recovery action. Client input, storage key, provider account, vector ID, cache key, URL, or backup ID cannot select scope.

## Ambiguity Fails Closed

Missing, stale, mismatched, recycled, or conflicting scope is denied, restricted, quarantined, or reconciled without revealing target existence, owner, provider, or content.

# Required Controls

| Boundary | Required control |
|---|---|
| Relational query/transaction | Mandatory server-side tenant/environment predicate or equivalent Data/Security scope enforcement. |
| Vector/index query | Tenant/environment and domain access/lifecycle filters before exposure. |
| Object/export | Current purpose, representation, destination, expiry, residency, and audit. |
| Cache/queue/job | Protected scope key/envelope, expiry, consumer validation, no wildcard fallback. |
| Backup/restore/replica | Scope inventory, encryption/access, lifecycle/hold/deletion/residency revalidation before activation. |
| Admin/support | Explicit tenant, purpose, least privilege, expiry, approval, audit, and post-review. |

# Access Guard

Before material Data work validate trusted principal/workload, tenant/environment, owning domain/reference, subject/purpose where applicable, authorization/entitlement, representation/classification, lifecycle/deletion/hold, residency, operation type, correlation/idempotency, and audit/incident restrictions.

An active connection, prior query, replica, cached result, migration, or restore never grants future access. Unscoped queries, cross-tenant joins, tenant-blind workers, global cache fallbacks, and client-supplied tenant filters are prohibited.

# Administration, Migration, and Recovery

Tenant administrators access only authorized tenant representations. Operators/support receive no implicit content or broad database access. Exceptional access is delegated, time-bound, purpose-bound, minimized, auditable, and revoked.

Migration, provider move, backup/restore, or regional recovery identifies source/destination scope, current authorization, lifecycle/hold/deletion, residency, rollback, historical evidence, and revalidation. It never transfers data through key reuse, cache recovery, provider default, or ordinary support action.

# Observability and Testing

Data records scope validation/denial/ambiguity/staleness, cross-tenant attempt, query/filter violation, cache/queue mismatch, backup/restore scope failure, export/support access, migration, and containment evidence. Tests run adversarial concurrent tenants across every mechanism and prove no enumeration, leakage, cross-tenant effect, or stale resurrection.

# Required Artifacts

| Artifact | Purpose |
|---|---|
| Data access-context contract | Required scope, propagation, validation, mismatch, and audit fields. |
| Mechanism isolation standard | Controls for SQL, vector, object, cache, queue, backup, export, admin/support. |
| Tenant recovery/migration procedure | Scope, residency, lifecycle, rollback, evidence, and revalidation. |
| Isolation conformance suite | Proves no cross-tenant query, cache, queue, backup, support, or recovery effect. |

# Anti-Patterns

## Storage Key Selects Tenant

Keys are evidence only; trusted server context selects and validates scope.

## Database Uniqueness Is Tenant Isolation

Constraints help but do not replace current access predicates and mechanism-wide validation.

## Restore Bypasses Access

Recovered data remains unusable until current scope, lifecycle, residency, and authorization validation succeeds.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Data access and tenant isolation architecture for all physical representations and recovery paths. |
| 1.1 | 2026-08-07 | Approved after completeness, ownership, and long-term maintainability review. |
