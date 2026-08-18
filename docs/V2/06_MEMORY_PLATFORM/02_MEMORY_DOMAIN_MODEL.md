# 02_MEMORY_DOMAIN_MODEL

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines the canonical Memory domain model for durable, participant-specific context. The model makes every memory record attributable, scoped, reviewable, lifecycle-managed, and separable from its derived representations.

It models what Memory Platform owns. It does not recreate platform identity, canonical conversation history, organizational Knowledge, or external CRM data.

---

# Purpose

The domain model prevents an unstructured collection of notes, vectors, prompts, or provider records from becoming de facto personal memory. It provides stable identifiers and relationships for memory admission, retrieval, correction, suppression, expiry, deletion, provenance, and audit.

---

# Canonical Entity Rules

## Stable Logical Identifiers

Every canonical entity has a stable Memory-domain identifier. Provider IDs, database keys, cache keys, embeddings, index-document IDs, and connector record IDs are implementation references, never public Memory identity.

## References, Not Duplicated Ownership

Memory stores validated references to the tenant, subject, interaction, source system, policy, consent basis, and requester context needed to enforce its rules. The referenced platform remains the owner of its canonical record.

## Immutable Evidence and Versioned Meaning

Evidence, admission decisions, lifecycle decisions, and released Memory revisions are append-only. A correction, confidence change, policy change, or deletion decision produces a new accountable state rather than overwriting the historical reason a record existed.

## Derived Data Is Not Canonical

Embeddings, summaries, search documents, caches, projections, and provider copies are `MemoryRepresentation` instances derived from an eligible Memory revision. They can be rebuilt and must become ineligible when their source revision is corrected, suppressed, expired, or deleted.

---

# Core Entities

| Entity | Meaning | Canonical owner | Key invariants |
|---|---|---|---|
| `MemorySubjectBinding` | A tenant-scoped reference linking Memory to an approved participant/customer subject. | Memory for the binding; Foundation/Conversation/Identity for referenced identity facts. | One tenant scope; no identity duplication; binding status can prevent use. |
| `MemoryProfile` | A governed Memory view for one subject binding, containing no independent identity authority. | Memory Platform | Belongs to one tenant and subject binding; profile is a container, not a source of truth for identity. |
| `MemoryCandidate` | A proposed durable memory statement before admission. | Memory Platform | Is not retrievable as memory; preserves capture purpose, evidence references, and proposal origin. |
| `MemoryRecord` | The stable logical identity of a durable memory concept. | Memory Platform | Belongs to one profile; has one current lifecycle state; never changes tenant or subject binding. |
| `MemoryRevision` | An immutable, versioned statement of a MemoryRecord's value, classification, confidence, constraints, and evidence links. | Memory Platform | Exactly one revision may be current for an eligible record; revision cannot be edited in place. |
| `MemoryEvidence` | Immutable evidence supporting or disputing a candidate/revision. | Memory Platform | Identifies origin, locator/reference, observed time, capture method, classification, and integrity context. |
| `AdmissionDecision` | The accountable decision to admit, reject, hold, merge, or require review for a candidate. | Memory Platform | Names policy/consent basis, evaluator, time, outcome, and linked candidate/evidence. |
| `MemoryUseConstraint` | A versioned Memory-domain constraint for allowed purposes, representations, audience, sensitivity, freshness, or review requirements. | Memory Platform | Does not replace Security authorization or platform policy engines; restrictive constraints win. |
| `MemoryLifecycleDecision` | An accountable correction, supersession, suppression, expiry, retention, deletion, restoration, or dispute outcome. | Memory Platform | Is append-only; names trigger, actor/authority, effective time, and derived-data obligations. |
| `MemoryRepresentation` | A derived retrieval representation of an eligible MemoryRevision. | Memory Platform logical contract; Data/approved provider implements storage. | Carries revision, tenant, profile, constraint, and invalidation linkage; never becomes canonical truth. |
| `MemoryRetrievalRequest` | A purpose-bound request for eligible memory context. | Memory Platform | Includes server-resolved tenant, authorized requester context, subject scope, purpose, and correlation ID. |
| `MemoryRetrievalResult` | A bounded response with explicit outcome and, when allowed, minimal memory evidence. | Memory Platform | Uses only supported/restricted/stale/degraded/unavailable/unsupported outcomes; cannot reveal hidden memory. |

---

# Entity Relationships

```text
Tenant reference
   |
   +-- MemorySubjectBinding -- 1:1 --> MemoryProfile
                                      |
                                      +-- 1:N --> MemoryRecord -- 1:N --> MemoryRevision
                                                        |                    |
                                                        |                    +-- N:N --> MemoryEvidence
                                                        |                    +-- 1:N --> MemoryRepresentation
                                                        |
MemoryCandidate -- AdmissionDecision ------------------+
                                                        |
MemoryLifecycleDecision -------------------------------+

MemoryRetrievalRequest --> eligible MemoryRevision / MemoryRepresentation --> MemoryRetrievalResult
```

The logical model permits multiple memory records for a profile but does not permit a record to span profiles or tenants. A relation across participants requires its own explicitly governed representation; it must not be inferred by sharing a record or index entry.

---

# Memory Record Semantics

## Record Types

Each MemoryRecord has an explicit, policy-governed type. Initial types are deliberately narrow:

| Type | Intended use | Examples | Not for |
|---|---|---|---|
| Preference | A participant's stated or verified preference relevant to an approved service purpose. | Preferred contact language; permitted communication window. | Sensitive inference or unrestricted marketing profile. |
| Relationship context | A limited fact needed to maintain an approved service relationship. | Assigned account relationship; confirmed accessibility accommodation reference. | Reconstructing a full interaction history. |
| Continuity fact | A time-bounded fact needed to continue authorized work. | Open case preference; confirmed follow-up constraint. | Replacing Conversation session state. |

New record types require governance review, defined evidence/consent/retention rules, misuse analysis, and tests before admission is enabled.

## Revision Content

A MemoryRevision contains only the minimum fields required to express its approved meaning:

- normalized value or protected value reference;
- record type and semantic schema version;
- classification and sensitivity;
- confidence and verification state;
- effective, observed, freshness, expiry, and retention times where applicable;
- purpose, audience, representation, and review constraints;
- evidence and policy/consent references; and
- capture, admission, and revision lineage.

The revision does not contain a raw transcript, a provider prompt, a mutable external CRM object, or a general-purpose behavioral score.

---

# State and Version Rules

## Candidate State

`proposed` → `validating` → `admitted`, `rejected`, `held`, or `merged`.

Only `admitted` creates or revises a MemoryRecord. `held` and `rejected` candidates are never eligible for retrieval. A merge preserves evidence and decision lineage for every candidate involved.

## Record Lifecycle State

`active` → `superseded`, `suppressed`, `expired`, `pending_deletion`, `deleted`, or `held`.

Restoration is a new LifecycleDecision and is permitted only where policy allows. `deleted` ends retrieval eligibility and triggers required deletion/invalidation processing; retained audit evidence must be minimized and governed separately.

## Currentness

An `active` record is not necessarily usable. A revision is eligible only if it is current, within its effective/freshness/expiry limits, compliant with its UseConstraints, and permitted by the current authorization and purpose context.

---

# Retrieval Model

The retrieval model intentionally separates selection from agent behavior.

1. Resolve tenant, requester, subject, purpose, and requested representation on the server.
2. Identify records and revisions that are lifecycle-eligible.
3. Apply current authorization, consent/purpose, classification, audience, and freshness constraints before relevance or ranking.
4. Select the minimum permitted evidence and representation.
5. Return an explicit outcome, provenance, freshness, and restriction metadata appropriate to the requester.

`MemoryRetrievalResult` does not prescribe how an agent reasons, what it says, or which action it takes. It contains evidence, not instructions.

---

# Boundary Mapping

| External concept | Relationship to Memory model |
|---|---|
| Tenant, organization, workspace, membership, entitlement, and API-edge claims | Referenced from 16_PLATFORM_FOUNDATION; Memory does not own their lifecycle. |
| Identity, authentication, authorization decision, secret, and enterprise audit infrastructure | Supplied by 09_SECURITY_PLATFORM; Memory records policy/decision references needed for domain traceability. |
| Conversation, participant, interaction, session, and transcript | Referenced from 03_CONVERSATION_PLATFORM; Memory may retain a minimal evidence locator, not the canonical interaction data. |
| Voice or digital-channel event and delivery consent signal | Supplied by 04_VOICE_PLATFORM or 17_DIGITAL_CHANNEL_PLATFORM through approved contracts; Memory separately evaluates durable capture/use. |
| Reusable business knowledge and its source provenance | Owned by 05_KNOWLEDGE_PLATFORM; personal Memory does not become shared Knowledge. |
| CRM/profile/contact object | Externally owned and connected through 07_INTEGRATION_PLATFORM; Memory retains only approved evidence/reference and its own memory semantics. |
| Storage, index, cache, queue, backup, and data operations | Provided by 08_DATA_PLATFORM; Memory defines logical records and lifecycle requirements. |

---

# Integrity Invariants

- A MemoryRecord has exactly one tenant and one MemorySubjectBinding for its full lifetime.
- No candidate, rejected record, held record, suppressed record, expired record, pending-deletion record, or deleted record is retrievable as supported memory.
- Every eligible revision has linked evidence, an AdmissionDecision, and applicable policy/consent references.
- A restrictive constraint, current authorization denial, withdrawal, or lifecycle decision overrides relevance and ranking.
- Every representation can be traced to one MemoryRevision and is invalidated when that revision is no longer eligible.
- A caller cannot use identifiers, outcomes, timings, result counts, or errors to infer another tenant's or subject's memory.
- Memory has no authoritative dependency on a provider, cache, search index, prompt, or external CRM object.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_MEMORY_PLATFORM_ARCHITECTURE.md | Defines Memory ownership, operating principles, and public boundaries. |
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines candidate creation, evidence validation, and admission decisions. |
| 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md | Defines profile and preference semantics in more detail. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines purpose-bound retrieval and result contracts. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines lifecycle decisions and derived-data invalidation. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines access and isolation enforcement. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, consent, review, and audit requirements. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines privacy and security requirements. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the canonical Memory domain model, entities, relationships, lifecycle states, retrieval model, and integrity invariants. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |
