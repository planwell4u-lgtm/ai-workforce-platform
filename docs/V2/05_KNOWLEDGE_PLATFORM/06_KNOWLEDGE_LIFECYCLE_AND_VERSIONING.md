# 06_KNOWLEDGE_LIFECYCLE_AND_VERSIONING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Knowledge Platform Owner  
**Phase:** Knowledge Platform

---

# Overview

This document defines how Knowledge sources, versions, representations, and publication decisions change over time without silently changing live retrieval behavior.

It makes publication, activation eligibility, freshness, supersession, rollback, suspension, retirement, revocation, and historical traceability explicit and recoverable.

---

# Purpose

Knowledge changes must be deliberate, reviewable, versioned, and reversible. This model prevents a new crawl, reprocessing run, index rebuild, source correction, provider change, or policy update from silently changing the evidence available to an AI employee.

---

# Scope and Boundaries

This document owns Knowledge lifecycle semantics and lifecycle evidence. It does not own source acquisition (Document 03), content transformation (Document 04), retrieval algorithm (Document 05), access-policy enforcement (Document 07), approval authority (Document 08), storage/deletion execution (Data), or security policy (Security).

| Topic | Owner |
|---|---|
| Version, freshness, publication eligibility, supersession, rollback, suspension, retirement, and lifecycle invalidation semantics | Knowledge Platform |
| Review roles, approval thresholds, separation of duties, and publication workflow | 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md with Security |
| Physical records, retention, deletion, backup, holds, and archival execution | 08_DATA_PLATFORM |
| Source observation, refresh request, and ingestion evidence | 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md |
| Agent behavior, conversation continuity, customer memory, and external action | Agent, Conversation, Memory, and Integration Platforms |

---

# Lifecycle Principles

## Immutable Versions

A SourceRevision, ContentArtifact, KnowledgeVersion, KnowledgeRepresentation, PublicationDecision, RetrievalResult, and Citation is immutable once issued. Corrections create a successor or revocation record; they do not rewrite historical evidence.

## Publication and Retrieval Are Separate

Processing can create a candidate version. Governance may approve it for a scope. Retrieval still rechecks current tenant, purpose, authorization, rights, classification, freshness, and lifecycle state for every request.

## Future Requests Change; Historical Evidence Remains Traceable

Activation, rollback, suspension, or retirement changes eligibility for new retrieval. Historical result/audit evidence remains traceable only under its retention and access rules; it does not stay normally retrievable merely for convenience.

## Freshness Is Policy-Bound

Freshness is evaluated against the source class, business criticality, publication scope, source observation, and current policy. It is not inferred from a file timestamp or index rebuild alone.

## Revocation Wins Over Convenience

Rights loss, security finding, classification change, legal restriction, source withdrawal, or integrity failure can suspend/revoke access ahead of ordinary rollout or retention schedules. The platform blocks new use while preserving only permitted audit and recovery evidence.

---

# Lifecycle Model

~~~text
Candidate KnowledgeVersion
    |
    +--> Reviewed --> Approved PublicationDecision --> Published / Eligible
    |                                                |
    |                                                +--> Superseded --> Retired
    |                                                |
    |                                                +--> Suspended / Revoked
    |
    +--> Rejected

At any point: rights/policy/integrity event --> Suspension or Revocation
~~~

## Source States

| State | Meaning | Retrieval effect |
|---|---|---|
| `Registered` | Source admission exists but active use may not yet be enabled. | None by itself. |
| `Active` | Source may accept authorized ingestion/refresh. | No direct effect on a version. |
| `Restricted` | Source scope/use is constrained pending policy or rights resolution. | Affected new processing/retrieval is limited. |
| `Suspended` | New ingestion/use is stopped pending investigation or remediation. | Affected versions are re-evaluated. |
| `Retired` | Source is no longer used for new ingestion. | Existing versions follow their own lifecycle/retention rules. |

## KnowledgeVersion States

| State | Meaning | May support new retrieval? |
|---|---|---|
| `Candidate` | Derived evidence awaiting validation/governance. | No. |
| `Reviewed` | Required checks/evidence are complete. | No, absent publication. |
| `Published` | Has a current approved PublicationDecision for a declared scope. | Only after current request checks. |
| `Superseded` | Replaced for future use by another eligible version. | No, unless an explicit controlled rollback reactivates it. |
| `Suspended` | Temporarily ineligible due to unresolved concern. | No. |
| `Revoked` | Ineligible due to rights, security, classification, or integrity condition. | No. |
| `Retired` | Permanently unavailable for new retrieval. | No. |
| `Rejected` | Candidate did not meet lifecycle/governance requirements. | No. |

## Representation States

Representations may be `prepared`, `indexed`, `unavailable`, or `invalidated`. Their state never independently changes the parent KnowledgeVersion lifecycle. A representation is excluded whenever its parent version or relevant policy is ineligible.

---

# Versioning Model

Each KnowledgeVersion has an immutable opaque ID, a human-readable version label where useful, a manifest/digest, predecessor/successor references, source/artifact/provenance links, processing and policy versions, classification/rights scope, freshness evidence, and lifecycle/audit references.

The version manifest is the authoritative description of the governed evidence available for review: its supporting sources, processing transformation, artifacts/representations, constraints, and known uncertainty. It contains protected references, not raw content, secrets, credentials, or unrestricted source metadata.

## Change Classification

| Change | Required posture |
|---|---|
| Source correction, material content/structure change, classification/rights change, redaction change, or scope change | New candidate version and full governance evaluation. |
| Processing/index/ranking policy change with material output impact | New derived outputs; assess affected published versions and migration/rollback evidence. |
| Non-material metadata clarification | Auditable annotation if it does not alter evidence, eligibility, citation, or retrieval behavior. |
| Source refresh found unchanged | Update observation/freshness evidence only; do not create a duplicate version. |
| Security/rights/integrity withdrawal | Immediate suspension/revocation assessment; no silent substitution. |

Version labels describe human review intent; immutable IDs and manifest digest identify the exact governed evidence.

---

# Publication, Activation, and Supersession

## Publication

Publication creates an immutable PublicationDecision for a specific KnowledgeVersion and effective tenant, audience, purpose, classification, time, and policy scope. It records authority, validation evidence, attribution, freshness requirement, rollback target, and audit reason.

Publication makes a version eligible for future retrieval only. It does not grant a consumer access, deliver content, alter in-flight Agent work, or replace an existing version outside its explicitly defined scope.

## Supersession

Supersession designates a later eligible version as the preferred candidate for new requests in an overlapping scope. It preserves prior version/history references and provides a migration/rollback relationship. It does not erase prior citations or alter completed retrieval results.

## Controlled Rollback

Rollback changes future eligibility to a prior compatible, non-revoked version through a new auditable decision. Before rollback, the platform validates current tenant scope, source rights, classification, security conditions, policy compatibility, representation availability, and known issues.

Rollback does not restore deleted/restricted content, undo participant-facing actions, mutate historical facts, or bypass a rights/security revocation.

---

# Freshness and Revalidation

Freshness policy defines expected observation interval, source class, criticality, tolerance, responsible owner, acceptable degraded behavior, and escalation/refresh actions. A version can be `current`, `approaching-stale`, `stale`, `unknown`, or `unavailable` for a given request policy.

The platform recalculates freshness when source observation, rights, policy, classification, source availability, or publication scope changes. A stale result is returned only when current policy permits it and clearly marks the condition; otherwise it is restricted or unavailable.

Source refresh success updates freshness evidence but cannot silently overwrite a published version. A source removal or failure does not automatically delete earlier evidence; it triggers the documented lifecycle and retention assessment.

---

# Suspension, Revocation, Retirement, and Deletion

## Suspension

Suspension is a reversible protective state used while an issue is investigated. It records the affected scope, reason/evidence, initiating authority, time, required remediation, and retrieval block. It propagates to affected representations and cache eligibility without changing the historical version record.

## Revocation

Revocation blocks a version or scope because it must not support new retrieval: for example, rights withdrawal, security incident, invalid provenance, prohibited classification, or material integrity failure. It requires immediate invalidation/recheck of affected representations, caches, citations, and active request assembly according to policy.

## Retirement

Retirement ends new retrieval after planned migration, supersession, or end of life. The version remains accessible only through approved audit/retention paths. Retirement is not deletion.

## Deletion and Holds

Data Platform executes deletion, backup, legal hold, and retention operations. Knowledge defines the lifecycle intent, affected evidence, and access consequences. A hold may delay physical deletion but never restores ordinary retrieval eligibility.

---

# Concurrency, Migration, and Recovery

- Lifecycle transitions use expected-version checks, idempotency, correlation, authority, and audit evidence. Delayed events cannot overwrite a suspension, revocation, or later valid transition.
- A publication, rollback, or revocation is resolved per effective scope. Overlapping audience/purpose scopes must not yield competing eligible versions without an explicitly documented selection rule.
- Policy, schema, provider, or representation migration creates a compatibility plan, affected-version inventory, rollout, monitoring, stop condition, rollback target, and support end date.
- In-flight retrieval revalidates eligibility before result assembly. New requests resolve the current eligible version; completed results remain immutable evidence.
- Recovery reconstructs lifecycle state from durable decisions and transitions. It never assumes that an index or cache state is authoritative.

---

# Security, Observability, and Audit

Lifecycle operations are tenant/environment scoped and require current, separated authorization for proposing, reviewing, publishing, superseding, rolling back, suspending, revoking, retiring, and viewing protected history.

Events include `knowledge.version.candidate_created`, `knowledge.version.published`, `knowledge.version.superseded`, `knowledge.version.rolled_back`, `knowledge.version.suspended`, `knowledge.version.revoked`, `knowledge.version.retired`, and `knowledge.freshness.changed`. They contain minimized references, scope, reason, policy/version, authority, correlation, and outcome—not raw content or secrets.

Metrics include candidate-to-publication time, freshness distribution, stale/restricted result rate, rollback/suspension/revocation frequency, invalidation propagation, affected-version count, lifecycle transition failure, and policy-migration status. Audit records every privileged transition and its evidence, scope, authority, reason, and resulting eligibility.

---

# Testing Strategy

Validate state transitions, immutable manifests, publication scope, freshness recomputation, unchanged refresh, supersession, rollback compatibility, suspension/revocation propagation, retirement, hold/deletion separation, concurrent transition conflicts, index/cache invalidation, tenant isolation, authorization separation, and restart reconciliation.

Test that no source refresh, processing result, index rebuild, agent request, or provider callback can directly publish, overwrite, revive, or broaden a version’s eligibility.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Lifecycle transition schema | Defines states, guards, scope, idempotency, authority, events, and audit fields | Knowledge Platform |
| Version manifest and compatibility contract | Defines immutable evidence, dependencies, successor/rollback, migration, and support end | Knowledge Platform |
| Publication/rollback/suspension procedure | Defines validation, approvals, effective scope, propagation, monitoring, and recovery | Knowledge Platform with Governance, Security, and Operations |
| Freshness policy catalog | Defines source-class intervals, tolerance, stale behavior, escalation, and evidence | Knowledge Platform with source owners |
| Revocation and invalidation procedure | Defines rights/security/classification/integrity withdrawal and downstream cache/index/result effects | Knowledge Platform with Security and Data |
| Lifecycle audit and test suite | Defines evidence, metrics, transition, security, tenant, and resilience validation | Knowledge Platform with Observability and Testing |

---

# Anti-Patterns

## Reprocess in Place

Changing processing outputs or source material in an existing version destroys traceability. Create successor evidence and a governed lifecycle decision.

## Published Means Permanently Current

Publication is scoped and conditional. Freshness, rights, classification, authorization, and lifecycle are re-evaluated at retrieval.

## Rollback Means Ignore Revocation

Rollback may select only a currently compatible, eligible version. It cannot reactivate prohibited or insecure content.

## Retired Means Deleted

Retirement ends new retrieval. Retention, hold, and physical deletion are separate governed processes.

## Index State Is Lifecycle State

Indexes and caches are derived. Publication decisions and lifecycle records remain authoritative.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_KNOWLEDGE_DOMAIN_MODEL.md | Defines version, representation, and PublicationDecision entities. |
| 03_KNOWLEDGE_SOURCE_AND_INGESTION_MODEL.md | Defines refresh/source observation and candidate creation. |
| 05_KNOWLEDGE_INDEXING_AND_RETRIEVAL.md | Defines current eligibility filtering and invalidation use at retrieval. |
| 07_KNOWLEDGE_ACCESS_AND_TENANT_ISOLATION.md | Defines access rechecks and tenant enforcement. |
| 08_KNOWLEDGE_GOVERNANCE_AND_PUBLICATION.md | Defines review, approval, and publication authority. |
| 08_DATA_PLATFORM | Owns physical retention, hold, and deletion execution. |
| 09_SECURITY_PLATFORM | Owns authorization and security-policy controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Knowledge lifecycle, versioning, freshness, publication, rollback, revocation, retirement, and recovery model. |
| 1.1 | 2026-08-06 | Finalized and approved the Knowledge Lifecycle and Versioning model. |
