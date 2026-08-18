# 03_CONVERSATION_MODEL

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines the canonical data model for conversations. It establishes the tenant-scoped entities and references needed to represent a conversation consistently across voice, chat, messaging, email, API, agents, workflows, tools, and human operators.

The model is contract-first and implementation-independent. Data Platform owns physical storage; Conversation Platform owns the meaning, ownership, lifecycle references, relationships, and access expectations for conversation records.

---

# Purpose

The purpose of the Conversation Model is to provide one stable representation of a conversation without making a channel thread, call ID, browser session, transcript, agent memory, or workflow instance the source of truth.

It enables controlled continuity, routing, context, handoff, audit, and cross-platform correlation while preserving tenant isolation, classification, minimization, and ownership boundaries.

---

# Objectives

The Conversation Model must:

- Define canonical tenant-scoped conversation, participant, interaction, channel-thread, routing, handoff, and context-reference entities.
- Use immutable identifiers, explicit relationships, ownership, classification, and versioning.
- Keep raw messages, recordings, documents, memories, tool payloads, workflow state, and private reasoning in their authoritative systems.
- Support one-to-one, multi-party, asynchronous, and cross-channel conversations.
- Make identity evidence and channel addresses distinct from verified participant identity.
- Support durable correlation with agent execution, workflow, tool, delivery, event, and audit evidence.
- Provide backward-compatible, versioned contracts for producers and consumers.

---

# Scope

This document defines the logical entity model, required attributes, relationship rules, identity/participant association, channel mapping, interaction references, ownership, classification, versioning, retention references, and contract governance.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Lifecycle states and transition behavior | 02_CONVERSATION_LIFECYCLE.md |
| Session coordination and execution association | 04_CONVERSATION_SESSION_MODEL.md |
| Context composition and snapshot behavior | 05_CONVERSATION_CONTEXT_MODEL.md |
| Routing and handoff decision policy | 06_CONVERSATION_ROUTING.md and 08_CONVERSATION_HANDOFF_MODEL.md |
| Raw message, media, transcript, attachment, recording, document, memory, tool, and workflow storage | Owning Channel, Voice, Knowledge, Memory, Integration, and Data Platforms |
| Database schemas, indexing, encryption, backup, retention engine, and migration implementation | 08_DATA_PLATFORM |
| Identity provider, authorization infrastructure, consent policy, and compliance controls | 09_SECURITY_PLATFORM |

---

# Model Principles

## Canonical but Minimal

Conversation Platform stores the minimum canonical metadata and references needed to coordinate an interaction. It uses stable references to authoritative content rather than copying unbounded or sensitive payloads.

## One Immutable Tenant Owner

Each conversation and child association has one immutable tenant owner. A resource with missing, conflicting, or unverifiable tenant ownership is inaccessible until corrected through an authorized process.

## Identity Evidence Is Not Identity

Phone number, sender address, browser session, provider account, and API client are channel evidence. They become a participant association only after tenant, purpose, assurance, consent, and policy checks.

## Explicit Relationship and Visibility

Every participant, channel mapping, interaction reference, context reference, route, and handoff records its role, scope, visibility, source, and lifecycle relationship. Shared conversation membership does not create unrestricted content access.

## Reference, Do Not Duplicate

The model holds references and classification to raw content. A reference is not permission to retrieve its target; retrieval is separately authorized by the owning platform.

---

# Core Entities

~~~text
Conversation
    +-- Participant Association
    +-- Interaction Reference
    +-- Channel-Thread Mapping
    +-- Session Reference
    +-- Routing Decision Reference
    +-- Handoff Assignment Reference
    +-- Context Snapshot Reference
    +-- Agent / Workflow / Tool / Delivery Correlation Reference
~~~

## Conversation

A Conversation is the canonical tenant-scoped interaction record. Required attributes include conversation ID, tenant/organization, purpose, classification, lifecycle reference/state, owner/version, created/updated time, retention/residency reference, and correlation/trace metadata.

## Participant Association

A Participant Association connects a verified or candidate person, organization, agent, human operator, group endpoint, or external system to a conversation. It records role, relationship, identity-assurance reference, consent/reference, visibility, effective time, source, and status.

## Interaction Reference

An Interaction Reference records an accepted inbound or outbound conversational occurrence: interaction ID, direction, channel, source/delivery identifier, occurrence time, classification, content reference, idempotency reference, and correlation. It does not store unrestricted content.

## Channel-Thread Mapping

A Channel-Thread Mapping links a provider-native call, message thread, email chain, browser session, or API stream to a canonical conversation. It records channel, provider/source, mapping evidence, tenant binding, effective time, status, and policy basis.

## Session and Context References

Session and context references associate bounded active processing with a conversation. They record purpose, authorization/identity/policy reference, expiry, classification, and status. They do not embed runtime state or grant broad history access.

## Routing and Handoff References

Routing and handoff references record destination category, eligible assignment, reason, policy, queue/role, ownership, allowed context, expiry, and outcome. They are references to controlled decisions, not direct permission grants.

---

# Required Attribute Families

| Entity family | Required attributes |
|---|---|
| Identity and ownership | Immutable ID, tenant, owner/source, creation/updated time, state version |
| Purpose and policy | Purpose, classification, retention/residency reference, consent/authorization reference where applicable |
| Relationship | Parent conversation, participant/channel/session/route role, visibility, effective/expiry time |
| Correlation | Interaction, event, execution, workflow, tool, delivery, audit, causation, correlation, trace references |
| Integrity | Source identifier, schema version, idempotency/deduplication reference, expected version, provenance |
| Lifecycle | Current status, transition/history reference, closure/archive/deletion reference where applicable |

Sensitive attributes are represented through classified references or controlled tokens. Secrets, credentials, hidden instructions, private reasoning, and raw unnecessary content are prohibited from canonical records.

---

# Relationship Rules

## Participant Rules

A conversation may have multiple participants, agents, operators, and systems. Each has a distinct role and visibility scope. Candidate identity is labeled as such; it cannot unlock sensitive context or high-impact action without required verification.

## Channel Rules

One conversation may map to multiple channels and channel threads. One provider thread maps to at most one active canonical conversation at a time unless an authorized migration/reconciliation record states otherwise.

## Agent and Workflow Rules

A conversation may correlate with many agent executions, versions, workflows, tools, and deliveries over time. These references do not make the Conversation Platform owner of agent, workflow, or tool state.

## Context Rules

A context snapshot is immutable, purpose-bound, expiry-bound, and associated with one authorized execution or handoff use. It may refer to conversation history but is not the canonical conversation or an unlimited data grant.

## Relationship Cardinality

| Relationship | Cardinality and rule |
|---|---|
| Tenant to conversation | One tenant owns many conversations; each conversation has exactly one immutable tenant owner |
| Conversation to participant association | One conversation has one or more associations; each association belongs to one conversation and one participant/candidate reference |
| Conversation to interaction | One conversation has many interaction references; each accepted interaction belongs to one canonical conversation |
| Conversation to channel-thread mapping | One conversation may have many mappings; one active provider thread maps to at most one active canonical conversation unless controlled reconciliation records otherwise |
| Conversation to session/context/routing/handoff | One conversation may have many historical references; each reference has one parent conversation and explicit purpose/status/expiry |
| Conversation to agent/workflow/tool/delivery reference | One conversation may correlate to many references; correlation does not transfer ownership of the referenced state |

Relationship cardinality is enforced through approved contracts and owning Data Platform constraints. A missing or ambiguous parent relationship blocks normal processing until reconciled.

## Participant Merge, Split, and Correction

Duplicate candidate identity, merged customer accounts, shared contact details, or mistaken associations are corrected through a controlled merge, split, or reassociation record. The record preserves source evidence, prior/current association, tenant, policy, authorized actor, effective time, impact on visibility/context, and audit reason.

Correction does not silently rewrite historical identity evidence or expose restricted history to a newly linked participant. Sensitive associations require current verification and may require human review.

---

# Contract and Version Governance

The Conversation Model is implemented through versioned machine-readable schemas for conversation, participant association, interaction reference, channel mapping, and related decision references.

Additive compatible change is preferred. Changing a field’s meaning/type, ownership, visibility, authorization semantics, or required status requires a new contract version and migration plan. Producers and consumers must support approved versions during migration.

Entity IDs are immutable. State and mutable metadata use expected-version updates. Historical facts are append-only references; correcting metadata produces an auditable correction rather than rewriting the prior fact.

## Interaction Content Reference Contract

Every interaction content reference identifies content type, source/provenance, immutable digest or integrity reference, classification, redaction status, owner system, retention/deletion state, and authorized retrieval contract. Supported content types are explicitly registered; unknown or unsafe content is quarantined or rejected.

The Conversation Model does not embed raw content by default. When the owner system deletes, redacts, or makes content unavailable, the reference records the resulting availability state without preserving prohibited duplicate content.

## Time and Sequence Semantics

Conversation entities distinguish source occurrence time, platform receipt time, durable persistence time, processing time, and export time where applicable. They retain source sequence/order evidence when available, plus timezone/clock-source metadata when material.

Ordering is not inferred from a single timestamp. Clock skew, delayed callback, retry, and replay behavior are handled through source provenance, idempotency, expected version, and reconciliation rules.

---

# Data Classification, Retention, and Access

Every entity inherits or records classification and tenant scope. Conversation records link to Data/Security retention, residency, legal-hold, export, deletion, and anonymization policy. Lifecycle policy determines when a record is active, archived, or unavailable; it never makes the content broadly accessible.

Access requires current tenant, role, purpose, participant relationship, classification, consent, and authorization. Operational/support access is scoped, time-limited, and audited. Cross-tenant search or association is prohibited unless an explicit approved aggregate/migration process applies.

## Referential Integrity and Lifecycle Effects

When a conversation, participant association, interaction content, channel mapping, or referenced resource is archived, deleted, anonymized, merged, split, or made unavailable, dependent references follow a documented integrity rule: retain protected reference, revoke retrieval, redact derivation, re-resolve association, or expire derived context.

No lifecycle change leaves a dangling reference that can be used to bypass tenant, retention, or authorization checks. Data Platform implements physical deletion and constraints; Conversation Platform defines the business relationship and required observable outcome.

## Read Models and Projections

Derived routing, support, analytics, search, and agent-context views are permitted only as tenant-scoped projections of the canonical model with documented purpose, source version, freshness, classification, access, and invalidation behavior.

Projections are not an alternative source of truth. They cannot include broader content, visibility, or authorization than the canonical record and owning content systems permit. Conflicting or stale projections are rebuilt or reconciled from authoritative records.

---

# Concurrency and Integrity

Each mutable record includes a version or equivalent concurrency token. Updates validate tenant owner, parent relationship, authority, expected version, and policy before persistence. Conflicts preserve durable evidence and use reconciliation rather than last-write-wins overwrite.

The model uses stable source and idempotency references to prevent duplicate interactions, mappings, or participant associations. A provider callback, delayed event, or reused channel identifier cannot silently reassign a record to another conversation or tenant.

---

# Observability and Audit

Every entity creation, mapping, association, correction, access, lifecycle change, routing/handoff reference, and deletion/archive request emits tenant-safe audit and correlation evidence.

Telemetry measures conversation volume, participant/channel mapping, association confidence, duplicate prevention, context usage, routing/handoff, contract errors, conflict/reconciliation, retention state, and unauthorized access attempts. Raw content remains protected in its owner system.

---

# Testing Strategy

## Contract Tests

Validate schemas, required fields, identifiers, ownership, classification, version compatibility, relation cardinality, and prohibited content.

## Integration Tests

Validate channel mapping, participant resolution, interaction association, cross-channel continuity, context/session correlation, agent/workflow/tool reference, handoff, archive, and deletion relationships.

## Security and Tenant Tests

Validate forged identifiers, cross-tenant lookup, ambiguous identity, visibility, revoked consent, restricted context, support access, mapping reassignment, and export/deletion authorization.

## Resilience Tests

Simulate duplicate callbacks, concurrent updates, delayed events, conflicting mappings, worker restart, migration, schema-version overlap, and reconciliation. Prove no data leakage, duplicate conversation, or state overwrite.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation model schema | Defines canonical entities, attributes, relationships, classifications, and versioning | Conversation Platform |
| Participant and identity-association contract | Defines roles, evidence, assurance, visibility, consent, and lifecycle | Conversation Platform with Security owner |
| Relationship cardinality matrix | Defines permitted entity relationships, parent rules, uniqueness, and integrity behavior | Conversation Platform with Data owner |
| Participant merge/split/correction procedure | Defines evidence, authorization, visibility, historical integrity, reconciliation, and audit | Conversation Platform with Security and tenant owner |
| Interaction and channel-mapping schema | Defines channel/source mapping, idempotency, correlation, status, and policy evidence | Conversation Platform with Channel owners |
| Interaction content-reference contract | Defines content type, provenance, digest, classification, redaction, availability, and retrieval | Conversation Platform with Channel, Voice, and Data owners |
| Context/session reference contract | Defines bounded reference, purpose, expiry, classification, and authorization linkage | Conversation Platform with Agent and Security owners |
| Relationship and visibility matrix | Defines permitted participant, human, agent, system, and group relationships | Conversation Platform and tenant owner |
| Model migration and compatibility policy | Defines schema versions, correction, migration, overlap, and deprecation | Conversation Platform with Data owner |
| Time, sequence, and projection standard | Defines timestamp, ordering, clock, read-model, freshness, invalidation, and rebuild behavior | Conversation Platform with Data and Observability owners |
| Referential-integrity lifecycle policy | Defines archive, deletion, anonymization, merge, split, revocation, and dependent-reference behavior | Conversation Platform with Data and Security owners |
| Model integrity test suite | Validates contract, tenant, relationship, concurrency, and resilience behavior | Conversation Platform and Testing Platform |

---

# Anti-Patterns

## Provider Thread as Canonical Record

A call ID, email thread, chat session, or provider user account is a mapping, not the canonical conversation.

## Transcript as Conversation Model

A raw transcript is content owned by its channel/recording system. It is not enough to represent participants, lifecycle, routing, policy, visibility, or continuity.

## Identity by Contact Detail

Matching a phone number or email does not prove participant identity, tenant relationship, or permission to link sensitive conversation history.

## Copying Cross-Platform State

Embedding knowledge, memory, workflow, tool, runtime, or security state into the conversation record duplicates ownership and creates stale/unsafe data.

## Mutable History

Overwriting accepted interaction or transition facts destroys audit and reconciliation. Use append-only facts and auditable corrections.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines components, ownership, and integration boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines lifecycle state and transition behavior for model entities. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session coordination and execution association. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context snapshot content and lifecycle. |
| 06_CONVERSATION_ROUTING.md | Defines routing decision policy and assignment. |
| 07_CONVERSATION_EVENTS.md | Defines formal event contracts based on model entities. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines human/agent collaboration associations. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines persistence, concurrency, recovery, and reconciliation patterns. |
| 10_CONVERSATION_SECURITY.md | Defines detailed access, tenant, consent, and privacy controls. |
| 08_DATA_PLATFORM | Owns storage, migration, retention, backup, and deletion implementation. |
| 09_SECURITY_PLATFORM | Owns identity, authorization, privacy, and compliance controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Model document. |
| 2.1 | 2026-08-05 | Added cardinality, participant correction, content/time semantics, integrity, projections, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |
