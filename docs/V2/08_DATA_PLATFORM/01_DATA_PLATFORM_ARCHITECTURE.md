# 01_DATA_PLATFORM_ARCHITECTURE

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

Data Platform provides shared physical data mechanisms: Supabase-managed PostgreSQL, pgvector, storage, queues, caches, lifecycle, recovery, residency, and data-service observability. It implements these mechanisms without owning the domain meaning of Knowledge, Memory, Conversation, Integration, Voice, or Digital Channel records.

# Purpose

Provide a reliable, tenant-safe, portable data foundation without direct cross-module database coupling or provider storage becoming domain authority.

# Ownership Boundary

Data owns physical schemas, migrations, indexes, persistence, vector representations, queues, caches, backup/restore, retention/deletion/hold mechanisms, residency implementation, and data-service reliability.

Data does not own tenant/membership/entitlement/configuration/API-edge facts (Platform Foundation); identity, authorization, secrets, cryptography, compliance, or audit infrastructure (Security); or domain lifecycle, canonical record meaning, retrieval eligibility, business action, channel, or Agent semantics (owning domain platforms).

# Principles

## Data Mechanism Is Not Domain Authority

A table row, vector entry, cache value, object, queue message, or backup is implementation evidence. The owning domain contract determines canonical identity, lifecycle, eligibility, access, and business meaning.

## Contracted Access, Not Shared Database Access

Modules use versioned APIs, events, or approved data-service contracts. They do not query or mutate another module's tables, vectors, queues, caches, or storage objects directly.

## Canonical and Derived Data Stay Distinct

Canonical records remain domain-owned. Embeddings, indexes, chunks, summaries, caches, projections, exports, and backups are derived representations with lineage, tenant scope, invalidation, retention, deletion, and restore controls.

## Scope and Lifecycle Are Enforced Everywhere

Every operation validates trusted tenant/environment, current purpose/access, representation/classification, lifecycle, residency, and audit requirements. Storage identity, provider account, URL, cache key, or vector ID cannot select tenant scope.

# Logical Components

| Component | Responsibility | Must not own |
|---|---|---|
| Relational persistence | PostgreSQL schemas, transactions, migrations, indexes, durable records. | Domain semantics or enterprise authorization. |
| Vector representation | pgvector for approved derived embeddings/similarity support. | Knowledge/Memory eligibility, access, or truth. |
| Artifact storage | Protected object/attachment representations and lifecycle mechanisms. | Artifact meaning or access decisions. |
| Queue/cache services | Tenant-safe asynchronous delivery, idempotency, buffering, short-lived performance data. | Durable truth or authorization. |
| Lifecycle services | Retention, deletion, hold, export, backup, restore, residency, recovery. | Domain policy or legal authority. |

# Supabase, PostgreSQL, and pgvector Boundary

ADR-005 approves Supabase-managed PostgreSQL and pgvector as the shared data foundation. This selects only managed PostgreSQL and the vector extension; it does not automatically adopt Supabase Auth, Storage, Realtime, Edge Functions, RLS policies, schemas, secret-key patterns, or application architecture.

Data owns approved operational use; Security supplies identity/authorization/secrets controls; Platform Foundation supplies tenant/control-plane facts; domains own logical records and lifecycle rules.

# Data Flow

~~~text
Owning Domain Contract -> approved Data API/event/service -> scoped Data mechanism
  -> PostgreSQL / pgvector / storage / queue / cache -> protected operational evidence
~~~

Each read, write, representation, queue/cache operation, migration, backup/restore, export, deletion, and recovery revalidates scope and lifecycle. A successful physical write does not prove domain completion.

# Reliability, Privacy, and Portability

Data mechanisms support transactional integrity where required, tenant-safe idempotency, bounded retries, migration, backup/restore, recovery, lifecycle outcomes, and observability. Restore never revives a representation without current lifecycle/access validation.

Data is minimized, classified, representation-limited, residency-aware, access-controlled, auditable, and retained/deleted/held through current policy. Canonical records and required evidence must be exportable independently of a provider; derived representations must be rebuildable or removable.

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Data ownership catalog | Defines domain/data boundary and canonical versus derived representations. | Data with domain owners |
| PostgreSQL/pgvector standard | Defines schemas, migrations, indexing, vector lineage, capacity, security, backup, recovery. | Data with Security and Operations |
| Lifecycle/residency standard | Defines retention, deletion, hold, export, restore, and evidence. | Data with Security and domains |
| Data conformance suite | Proves scope, isolation, lifecycle, portability, recovery, no direct cross-module access. | Data with Testing and Security |

# Anti-Patterns

## Database Row Is the Domain Contract

Physical records implement domain contracts; they do not replace them or define public cross-module meaning.

## pgvector Decides Retrieval Access

Vector similarity supports derived retrieval only; Knowledge/Memory and current access controls determine eligible use.

## Shared Database Means Shared Access

Every module boundary remains contractual and tenant-scoped even when infrastructure is shared.

## Backup Restore Revives Everything

Restore revalidates current lifecycle, deletion, hold, access, and tenant controls before any representation becomes usable.

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Data Platform scope and document set. |
| 00_CONTROL/08_DECISION_LOG.md | ADR-005 selects the shared data foundation. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Records Supabase/PostgreSQL/pgvector limits. |
| 05_KNOWLEDGE_PLATFORM and 06_MEMORY_PLATFORM | Define governed domain use of persistence/vector representations. |

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Data Platform architecture for shared data mechanisms, PostgreSQL, pgvector, lifecycle, and boundaries. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |
