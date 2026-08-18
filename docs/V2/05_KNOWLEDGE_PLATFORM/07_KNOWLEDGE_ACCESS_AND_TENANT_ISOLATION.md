# 07_KNOWLEDGE_ACCESS_AND_TENANT_ISOLATION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines how Knowledge Platform operations remain tenant-isolated and purpose-bound across source registration, ingestion, processing, governance, retrieval, citations, caches, telemetry, and support.

Knowledge may be highly sensitive business evidence. Publication makes it eligible for a declared scope; it never makes it public to every user, agent, tenant, channel, or administrative tool.

---

# Purpose

The model prevents a source ID, vector, citation, cache entry, connector result, operator role, shared provider, or internal tool from becoming a path to cross-tenant or overbroad knowledge access.

It defines Knowledge-domain enforcement requirements while Security owns enterprise identity, authorization, policy, secrets, and compliance infrastructure.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Knowledge tenant/purpose/audience/representation access semantics and required evidence | Knowledge Platform |
| Identity, authentication, authorization engine, roles, policy decision, secrets, encryption, and compliance controls | 09_SECURITY_PLATFORM |
| Tenant-wide architecture and identity model | 01_ARCHITECTURE and Security Platform |
| Storage partitioning, lifecycle, backup, deletion, and shared-data infrastructure | 08_DATA_PLATFORM |
| Connector credentials and external authorization exchange | 07_INTEGRATION_PLATFORM with Security |
| Publication/review authority and workflow | 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md |
| Retrieval eligibility and result assembly | 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md |

---

# Access Principles

## Tenant and Environment Are Server-Resolved

Every Knowledge operation binds to one trusted tenant and environment. Client fields, URLs, source IDs, connector accounts, user claims, files, callbacks, and correlation IDs are evidence only; they cannot select a tenant without server-side validation.

## Authorization Is Current and Operation-Specific

Access is evaluated for the requested operation—register, ingest, process, review, publish, retrieve, inspect citation, export, support, or administer—and against current tenant, purpose, actor/service, audience, classification, rights, lifecycle, and policy. A previous access, publication decision, citation, or cache entry is not a reusable grant.

## Minimum Necessary Representation

The service returns the least sensitive approved representation: metadata, bounded evidence, citation, protected content reference, or content excerpt. Full source contents, raw artifacts, internal scores, source paths, and historic versions require separate current authorization.

## Data Plane and Control Plane Are Both Scoped

Tenant isolation applies to records, indexes, vectors, caches, queues, worker jobs, provider calls, logs, metrics, audit, dashboards, and administrative actions—not merely APIs.

## Shared Infrastructure Does Not Permit Shared Access

Shared vector stores, databases, object storage, model providers, queues, and support tools must enforce tenant/environment bindings and current authorization. A shared implementation cannot expose corpus existence, similarity, membership, or content across tenants.

---

# Knowledge Access Context

Every operation resolves an immutable access context containing:

- tenant and environment;
- authenticated actor or workload identity and delegation chain;
- operation and bounded purpose;
- requested Knowledge entity/reference and allowed representation;
- audience, classification, rights/attribution, residency, and lifecycle constraints;
- current authorization/policy decision reference;
- correlation, expiry, idempotency, and audit references.

The context is validated at each boundary. It is not copied as a bearer token into caches, citations, jobs, events, or downstream consumer state.

---

# Access Matrix

| Operation | Required Knowledge checks | Never implied by |
|---|---|---|
| Register source | Tenant owner, source scope, intended use, rights/classification, registration authority | Connector access or file upload |
| Ingest/refresh | Registered source, current scope/rights, bounded acquisition authority, policy | Prior ingestion success |
| Process artifact | Admitted SourceRevision, processing scope/policy, artifact classification | Parser/provider success |
| Review/publish | Candidate/version scope, review authority, lifecycle, governance evidence | Ability to ingest or retrieve |
| Retrieve | Consumer, purpose, tenant, audience, classification, rights, publication, freshness, policy | KnowledgeVersion or citation ID |
| View source/artifact | Explicit representation/content authorization, reason, rights, retention | Retrieval-result membership |
| Export/support | Exceptional purpose, least privilege, approval, time limit, audit | Platform operator or tenant-admin role alone |

---

# Tenant Isolation Requirements

## Entity and Query Isolation

Every Knowledge record, relationship, query, update, search filter, index lookup, vector retrieval, source locator, and cache access uses a trusted tenant/environment predicate. Resource IDs are additionally verified against the resolved scope. Unscoped bulk queries, wildcard search, tenant-blind background jobs, client-selected tenant filters, and cross-tenant joins are prohibited in normal paths.

## Index, Vector, and Cache Isolation

Representations and indexes carry tenant/environment, classification, audience, purpose, lifecycle, and publication eligibility references. The retrieval eligibility filter remains authoritative even if an index has stale entries.

Cache keys include tenant/environment, operation/consumer purpose, representation level, authorization-relevant constraint versions, publication/freshness state, and expiry. Cache misses, eviction, or restart cannot fall back to another tenant, broader classification, or a previously authorized result.

## Async and Event Isolation

Ingestion, processing, invalidation, refresh, and audit messages carry trusted tenant/environment binding, source/artifact/version scope, policy/version, correlation, and idempotency. Consumers revalidate before effect. A delayed or replayed job cannot access or revive an artifact after its tenant, rights, lifecycle, or policy binding changes.

## Provider and Connector Isolation

External parser, OCR, embedding, search, or connector operations receive only the minimum authorized material through approved adapters. Provider accounts, credentials, data-processing settings, logs, quotas, and callbacks are tenant-scoped or separately isolated by Security/Integration controls. Provider success does not override Knowledge eligibility.

---

# Representation and Citation Controls

Source, artifact, segment, KnowledgeVersion, representation, citation, and RetrievalResult each have an allowed representation level. A citation permits only the minimized evidence/presentation approved for its associated result and request; it cannot be used to browse a source, retrieve a raw artifact, infer other source segments, or share evidence with a different participant.

Classification, rights, audience, and purpose are rechecked when a protected reference is resolved. Redaction, revocation, source-rights loss, lifecycle suspension, or policy change invalidates dependent representations and blocks new use according to the lifecycle propagation rule.

---

# Administration, Support, and Analytics

Tenant administrators may operate only their tenant-scoped sources, candidates, versions, reviews, and permitted reports. They cannot enumerate other tenants or select platform-wide source/index/provider context.

Platform support and administration have no implicit content access. Exceptional access requires delegated, time-bounded, purpose-bound, least-privilege authorization, explicit tenant scope, representation minimization, approval where policy requires, audit, expiry/revocation, and post-access review.

Analytics and evaluation use approved aggregates, synthetic data, or separately authorized evidence. Cross-tenant aggregates must prevent tenant, source, content, and corpus-membership disclosure.

---

# Tenant Lifecycle, Residency, and Migration

On tenant suspension/deactivation, Knowledge blocks new registration, ingestion, publication, retrieval, export, and ordinary administration except approved incident, retention, legal, or offboarding operations. Restoration revalidates tenant, source, rights, policy, publication, and access context; it does not revive stale grants or cached results.

Recovery, failover, provider migration, or data restoration may use only regions and providers currently eligible for the tenant's residency/data-processing constraints. Availability pressure never authorizes cross-region or cross-tenant content movement.

Cross-tenant transfer is exceptional and requires an explicit enterprise-approved migration record with source/destination scope, permitted data/evidence, rights and classification assessment, effective time, rollback, retention/deletion effect, and audit. It cannot occur through import, cache recovery, source URL reuse, provider account reuse, or ordinary support work.

---

# Mismatch Outcomes

| Outcome | Required action |
|---|---|
| `TenantScopeValidated` | Continue only the bounded, authorized operation. |
| `TenantScopeDenied` | Deny without revealing target existence, owner, source, or content. |
| `TenantScopeAmbiguous` | Quarantine/defer/reconcile; never guess scope. |
| `TenantScopeStale` | Stop/restrict and resolve through lifecycle/access revalidation. |
| `TenantScopeRestricted` | Apply the current policy constraint and record evidence. |
| `TenantScopeIncident` | Contain, suspend/restrict affected operations, preserve minimum evidence, and invoke incident response. |

---

# Reliability, Observability, and Audit

Every access-sensitive operation is idempotent where appropriate, records tenant-safe scope and policy evidence, and revalidates on retry, resume, cache use, or recovery. Unknown authorization or scope resolves to deny, restrict, defer, or unavailable—not broad fallback.

Telemetry records operation category, tenant-safe dimensions, policy/representation outcome, denial/restriction/mismatch, cache/invalidation, provider boundary, latency, and correlation. Routine telemetry excludes raw source content, queries, full citations, source paths, provider secrets, and direct identifiers.

Audit records source/artifact/version access, publication, export, privileged retrieval, exceptional support, policy override, migration, tenant lifecycle change, mismatch, and incident with actor/service, tenant scope, purpose, authority, policy, evidence, time, and outcome.

---

# Testing Strategy

Validate server-resolved scope, mandatory query predicates, resource binding, representation levels, authorization/purpose rechecks, cache/job/index/message isolation, provider-account separation, tenant lifecycle, residency-safe recovery, exceptional support, migration, and mismatch nondisclosure.

Run adversarial multi-tenant tests for forged tenant fields, guessed IDs, vector/index similarity probes, cache collisions, queue misdelivery, stale citation/reference, revoked rights, support overreach, provider callback confusion, stale worker restart, and cross-tenant analytics query. Prove no test can enumerate, expose, infer, modify, or affect another tenant's knowledge.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Knowledge access-context contract | Defines trusted scope, purpose, representation, policy, expiry, and audit fields | Knowledge Platform with Security |
| Knowledge authorization and representation matrix | Defines operations, actor categories, allowed representations, restrictions, and rechecks | Knowledge Platform with Security and Governance |
| Scoped data/index/cache/job standard | Defines tenant predicates, keys, messages, invalidation, recovery, and prohibited paths | Knowledge Platform with Data, Security, and Operations |
| Provider/connector data-boundary policy | Defines tenant scoping, minimum data, credentials, callbacks, residency, quotas, and incident controls | Knowledge Platform with Integration and Security |
| Exceptional support/export procedure | Defines delegation, approval, time limits, minimization, audit, and review | Knowledge Platform with Security and Operations |
| Tenant migration/offboarding procedure | Defines controlled transfer, suspension, restoration, residency, retention, and audit | Knowledge Platform with Data, Security, and Operations |
| Isolation telemetry and test suite | Defines metrics, alerts, audit, adversarial testing, and evidence | Knowledge Platform with Observability and Testing |

---

# Anti-Patterns

## Publication Grants Universal Access

Publication only creates potential eligibility for a declared scope. Every use still requires current tenant, purpose, policy, and representation checks.

## Citation Is a Bearer Token

A citation is bounded evidence for one result. It cannot unlock a source, artifact, other segment, or future request.

## Shared Vector Store Means Shared Corpus

Shared infrastructure must preserve tenant and policy isolation. Similarity is not authority to access another tenant's content.

## Platform Support Has Implicit Full Access

Support requires explicit, time-limited, purpose-bound authorization and audit; role alone is insufficient.

## Cache or Worker Can Trust Old Scope

Every asynchronous or cached operation revalidates current tenant, lifecycle, policy, rights, and authorization before use.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_KNOWLEDGE_PLATFORM_ARCHITECTURE.md | Defines Knowledge ownership and purpose-bound retrieval. |
| 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md | Defines eligibility filtering, results, citations, and cache consistency. |
| 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING.md | Defines suspension, revocation, retirement, and invalidation effects. |
| 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md | Defines publication/review authority. |
| 09_SECURITY_PLATFORM | Owns enterprise identity, authorization, secrets, and compliance controls. |
| 08_DATA_PLATFORM | Owns storage, partitioning, lifecycle, and recovery infrastructure. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Knowledge access, representation, tenant-isolation, support, migration, and recovery model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Access and Tenant Isolation model. |
