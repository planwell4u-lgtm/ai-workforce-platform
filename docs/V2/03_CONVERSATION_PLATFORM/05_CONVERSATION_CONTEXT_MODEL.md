# 05_CONVERSATION_CONTEXT_MODEL

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform assembles, authorizes, snapshots, delivers, expires, and audits conversation context for agent execution, routing, human handoff, workflow interaction, and authorized delivery.

Conversation context is a bounded view of relevant interaction state. It is not the full transcript, agent memory, knowledge store, user profile, runtime state, or a general authorization grant.

---

# Purpose

The purpose of the Conversation Context Model is to make context useful enough for a coherent interaction while preventing unnecessary data exposure, stale assumptions, cross-tenant leakage, prompt injection, and unbounded cost.

It gives the Agent Platform and authorized human/workflow paths a stable, tenant-safe contract for requesting only the context required for an approved purpose.

---

# Objectives

The Conversation Context Model must:

- Define context sources, composition, classification, provenance, minimization, and access rules.
- Produce immutable, purpose-bound, expiry-bound context snapshots for authorized uses.
- Distinguish conversation history from Knowledge Platform retrieval, Memory Platform access, and Agent runtime state.
- Preserve tenant, participant visibility, consent, identity assurance, lifecycle, channel, and handoff restrictions.
- Support current interaction, recent turns, relevant state, controlled summaries, and authorized reference retrieval.
- Prevent raw untrusted content from overriding instructions, policy, permission, or agent behavior.
- Support context refresh, invalidation, redaction, deletion, audit, and recovery.
- Remain independent of a prompt format, model provider, token limit, database, or vector store.

---

# Scope

This document defines context concepts, sources, selection, snapshot contract, access, lifecycle, integrity, security, observability, testing, and required artifacts for the Conversation Platform.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent reasoning, prompt hierarchy, model context window, capability selection, and response generation | 02_AGENT_PLATFORM |
| Long-term customer memory, preferences, profiles, and memory retention | 06_MEMORY_PLATFORM |
| Organizational documents, retrieval, RAG implementation, and knowledge governance | 05_KNOWLEDGE_PLATFORM |
| Canonical conversation/session entities and lifecycle | 02_CONVERSATION_LIFECYCLE.md, 03_CONVERSATION_MODEL.md, and 04_CONVERSATION_SESSION_MODEL.md |
| Routing, queue, or handoff policy | 06_CONVERSATION_ROUTING.md and 08_CONVERSATION_HANDOFF_MODEL.md |
| Raw transcript, recording, attachment, or channel-media storage | Channel, Voice, and Data Platforms |
| Permission enforcement, encryption, secrets, and privacy policy | 09_SECURITY_PLATFORM |

---

# Context Principles

## Context Is a View, Not a Store

Conversation Platform assembles metadata, references, approved summaries, and relevant interaction history for a defined use. It does not become a duplicate owner of memory, knowledge, raw media, or private model state.

## Minimum Necessary

Each context request specifies purpose, consumer, tenant, conversation/session, required sources, classification, and expiry. The Context Service returns only data and references authorized for that use.

## Provenance and Trust Are Explicit

Every context item records source category, owner, occurrence/refresh time, classification, integrity/provenance, and trust level. User text, external events, tool results, channel metadata, and retrieved documents are untrusted data; they cannot override approved instructions or policy.

## Immutable Snapshot

A context snapshot is immutable once issued. It identifies the conversation/session version, authorized contents/references, policy basis, expiry, consumer, and digest. New information produces a new snapshot rather than silently changing an in-flight execution.

## Current Authorization on Retrieval

A reference in a snapshot is not permission to retrieve its target indefinitely. Sensitive or deferred retrieval rechecks current tenant, purpose, classification, consent, participant visibility, and authorization.

## Bounded Composition

Context selection observes approved size, time, relevance, channel, risk, and cost budgets. Truncation, summarization, and omission are explicit and auditable; they must not remove required safety, identity, consent, or workflow state.

---

# Context Model

~~~text
Canonical Conversation and Session State
    +-- Current Interaction and Recent History
    +-- Participant and Visibility Metadata
    +-- Channel and Delivery Capability
    +-- Routing, Handoff, and Workflow References
    +-- Authorized Summary and Content References
    |
    v
Context Policy and Access Validation
    |
    v
Immutable Context Snapshot
    |
    v
Agent Execution / Human Handoff / Workflow Boundary
~~~

## Context Item

A context item has item ID, source type, source reference, tenant, conversation/session relationship, classification, visibility, provenance/trust, time/sequence, relevance/priority, integrity/digest, redaction state, and retrieval authorization reference where needed.

## Context Snapshot

A snapshot has snapshot ID, parent conversation/session, consumer, purpose, tenant, classification, source-state versions, item/reference list, composition policy version, budget outcome, created/expiry time, authorization/consent references, digest, and audit/correlation fields.

## Context Request

A request identifies consumer type, purpose, conversation/session, desired context categories, allowed classification, budget, channel/risk constraints, and current authorization. Unsupported or overbroad requests are denied, constrained, or routed to human review.

---

# Context Categories

| Category | Typical content | Owner |
|---|---|---|
| Current interaction | Latest validated user/event input and channel metadata | Conversation Platform and Channel owner |
| Recent history | Approved recent turns, summaries, interaction references, and state | Conversation Platform |
| Participant context | Identity assurance, role, visibility, consent, and relationship references | Conversation Platform with Security |
| Conversation state | Lifecycle, routing, handoff, waiting, and delivery disposition | Conversation Platform |
| Channel context | Channel capability, delivery constraints, language/media indicators | Channel/Voice Platform |
| Workflow/tool correlation | Approved work status/reference and required next-step context | Integration Platform |
| Knowledge reference | Authorized retrieval query/reference only | Knowledge Platform |
| Memory reference | Authorized profile/memory query/reference only | Memory Platform |
| Safety/policy context | Applicable policy, classification, approval, and restriction references | Security and Agent Platforms |

Conversation context may reference another category but cannot absorb its authoritative data ownership.

## Context Priority Matrix

| Priority | Use |
|---|---|
| Mandatory | Tenant, identity/consent, classification, safety, lifecycle, routing/handoff, unresolved-action, and required workflow state |
| High | Current interaction, directly relevant recent turns, participant role, channel capability, and approved task state |
| Optional | Authorized summaries, older relevant history, and approved external references within budget |
| Excluded | Hidden instructions, secrets, private reasoning, cross-tenant data, unauthorized content, and irrelevant history |

The composition policy may refine priority by consumer, risk, channel, and purpose but cannot omit mandatory controls or include excluded content.

## Context-Sharing Decisions

| Consumer | Default context entitlement |
|---|---|
| Agent execution | Immutable snapshot for one authorized purpose and execution |
| Human handoff | Minimum role- and purpose-scoped context granted by handoff policy |
| Workflow boundary | Approved state/reference necessary for the defined business process |
| Tool boundary | Minimum correlation/reference; no broad history unless separately authorized |
| Support/diagnostic user | Protected, time-limited evidence through separate authorization |
| Analytics/evaluation | Approved aggregated, synthetic, or separately authorized reference only |

Context sharing never substitutes for the receiving system’s own authorization and classification checks.

---

# Composition and Selection

## Selection Order

1. Validate tenant, conversation/session, consumer, purpose, lifecycle, and current authorization.
2. Apply participant visibility, consent, classification, residency, and legal restrictions.
3. Include required safety, identity, routing, handoff, and workflow state.
4. Select current interaction and relevant recent conversation history by policy.
5. Add authorized summaries or external references within the defined budget.
6. Record omitted, redacted, unavailable, stale, or conflicting items and issue the snapshot.

## Relevance and Summarization

Relevance policy uses conversation purpose, current task, participant role, lifecycle, time, channel, explicit user reference, and approved routing/workflow needs. Summaries are versioned derived artifacts with source range, policy, time, classification, and freshness; they are not treated as unverified truth.

A summary cannot remove or contradict required policy, consent, identity, safety, or unresolved-action state. When a detail is uncertain or omitted, the consumer receives the appropriate reference or uncertainty marker.

## Budget and Degradation

Budget policy defines maximum items, time range, size, retrieval count, cost, and latency by consumer, channel, risk, and tenant. When limits are reached, the service retains mandatory controls, returns a documented reduced context, requests clarification, defers work, or routes to human review.

## Content Format and Language

Context items declare content format, language, transcription/translation confidence where applicable, structured-data schema, attachment/media reference, accessibility marker, and safe rendering requirement. Raw audio, image, document, or attachment content remains with its owner and enters context only through approved classified references or extracted bounded representation.

Low-confidence transcription, translation, OCR, or structured extraction is marked as uncertain. It cannot be treated as verified identity, instruction, policy, consent, or authoritative business outcome without separate validation.

---

# Context Lifecycle

## Creation and Use

Snapshots are created only for an approved consumer and purpose. An agent execution, handoff, or workflow request records the snapshot ID it used. A snapshot cannot be repurposed for unrelated delivery, analytics, training, or another participant.

## Refresh and Invalidation

A new interaction, lifecycle/routing/handoff change, identity/consent change, policy update, source deletion, classification change, or expiry may invalidate a snapshot. The Context Service issues a new snapshot after revalidation; it does not mutate an issued snapshot.

## Expiry and Revocation

Snapshots expire according to purpose, risk, channel, classification, tenant policy, and session state. Expiry or revocation blocks ordinary use and retrieval. Historical snapshot metadata is retained only for approved audit/diagnostic use.

## Redaction and Source Removal

When source content is redacted, deleted, anonymized, reclassified, or made unavailable, derived snapshot references are invalidated or marked unavailable according to policy. The platform does not preserve prohibited content to keep a snapshot convenient.

## Context Policy Migration

When source eligibility, priority, budget, summarization, sharing, format, or access rules change, the Conversation Platform versions the context policy and maintains a migration plan for active sessions and retained snapshots.

An issued immutable snapshot retains its original policy reference for audit, but new retrieval/use follows current policy. If a material change makes an active snapshot unsafe or ineligible, it is revoked and the consumer must request a new authorized snapshot.

---

# Security, Privacy, and Tenant Controls

Context access is tenant-scoped, purpose-bound, classified, and authorized. A consumer receives only items visible to its participant/role and allowed by current consent, identity assurance, channel, lifecycle, and data policy.

External/user/channel/tool content is labeled as untrusted and isolated from instruction authority. Context snapshots never contain secrets, reusable credentials, hidden instructions, private reasoning, cross-tenant data, or unbounded raw content.

Human diagnostic or support access uses a separate, time-limited, audited authorization path. Snapshot identifiers and content references are not bearer permissions.

---

# Integrity, Concurrency, and Recovery

The snapshot records source versions and item digests. If a source changes during composition, the Context Service retries safely or returns a consistent bounded result with an explicit freshness marker.

Concurrent requests may create separate snapshots for distinct consumers/purposes. They cannot overwrite canonical conversation state. After restart, the service reconstructs only from durable source references and policy; it does not recover from in-memory prompt or model state.

## Context Cache Controls

Caches may store only approved tenant-scoped metadata or derived references with explicit TTL, encryption, classification, invalidation, and access rules. Cache keys include tenant, consumer/purpose, source/policy version, and visibility scope. Secrets, private reasoning, unrestricted raw content, and reusable authorization material are prohibited from context caches.

A cache is never authoritative. On expiry, invalidation, policy/consent change, or integrity uncertainty, the Context Service revalidates against authoritative records rather than serving stale context.

---

# Observability and Audit

The platform records context request, consumer, purpose, tenant, source categories, authorization result, classification, item count, budget/degradation, snapshot digest, expiry, invalidation, retrieval failure, and correlation references.

Metrics include context latency, source availability, item count, budget reduction, stale/invalidated snapshot use, redaction, denied request, cross-tenant attempt, summary freshness, and consumer outcome correlation. Raw content is not emitted in general telemetry.

## Context Effectiveness and Emergency Use

The platform links approved evaluation and analytics findings to context policy signals such as missing context, irrelevant items, stale summaries, budget reduction, source failure, unsafe content, handoff quality, and consumer outcome. Findings create a governed policy, source, summary, or test improvement request; they do not automatically broaden context access.

Emergency or safety context is limited to the minimum information needed for authorized human escalation, safety response, or incident containment. It remains tenant-scoped, classified, auditable, and subject to separate emergency-access policy; urgency does not permit unrestricted history or privacy bypass.

---

# Testing Strategy

## Contract Tests

Validate request, item, snapshot, provenance, classification, budget, expiry, invalidation, and audit schemas.

## Integration Tests

Validate history selection, routing/handoff inclusion, knowledge/memory reference, workflow correlation, agent/human consumers, refresh, channel switch, and source removal.

## Security and Tenant Tests

Validate purpose abuse, overbroad request, cross-tenant source, revoked consent, participant visibility, hidden-instruction exclusion, prompt injection labeling, redaction, and support access.

## Resilience Tests

Simulate concurrent change, missing source, stale summary, budget exhaustion, source deletion, policy change, restart, duplicate request, and dependency outage. Prove context remains bounded, consistent, authorized, and safe.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Context request and snapshot schema | Defines consumer, purpose, sources, item/reference, budget, expiry, policy, and audit fields | Conversation Platform |
| Context source and visibility matrix | Defines source categories, ownership, trust, classification, participant/role visibility, and retrieval controls | Conversation Platform with Security and dependent owners |
| Context priority and sharing matrix | Defines mandatory, optional, excluded items and consumer-specific context entitlement | Conversation Platform with Agent, Security, and tenant owners |
| Composition and budget policy | Defines selection order, relevance, summarization, omission, size/cost/latency limits, and degradation | Conversation Platform with Agent owner |
| Context format and language standard | Defines media, attachment, structured data, language, confidence, translation, accessibility, and safe representation | Conversation Platform with Channel and Voice owners |
| Context provenance and summarization standard | Defines source range, digest, trust, freshness, derived summary, and uncertainty behavior | Conversation Platform with Data and Agent owners |
| Context invalidation and revocation procedure | Defines triggers, expiry, redaction, deletion, reclassification, and recovery | Conversation Platform with Data and Security owners |
| Context policy migration procedure | Defines active/retained policy change, revocation, reauthorization, compatibility, audit, and rollout | Conversation Platform with Data and Security owners |
| Context cache policy | Defines tenant keying, TTL, encryption, classification, invalidation, and prohibited content | Conversation Platform with Data and Security owners |
| Context effectiveness and emergency-use policy | Defines feedback measures, improvement route, minimum emergency context, approval, and audit | Conversation Platform with Evaluation, Operations, and Security owners |
| Context security test suite | Validates authorization, tenant, visibility, injection, redaction, budget, and resilience controls | Conversation Platform and Testing Platform |
| Context observability catalog | Defines metrics, audit, SLOs, diagnostics, and prohibited telemetry content | Conversation, Operations, and Observability owners |

---

# Anti-Patterns

## Full History by Default

Sending all transcript, attachments, old turns, and references to every execution increases privacy, cost, stale-context, and injection risk.

## Context Equals Memory

Conversation history is not a replacement for governed long-term memory. Use Memory Platform through authorized references.

## Retrieved Content Overrides Policy

A document, user message, tool result, or event may inform reasoning but cannot modify instruction authority, permission, tenant scope, or safety controls.

## Snapshot Reuse for New Purpose

A snapshot created for an agent execution cannot be reused for analytics, another participant, delivery, or a new execution without current authorization.

## Hidden Budget Truncation

Silently omitting material safety, identity, or unresolved-action context creates unsafe behavior. Record budget reduction and use an approved fallback.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Context Service responsibility and boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines lifecycle state that gates context availability. |
| 03_CONVERSATION_MODEL.md | Defines canonical context, participant, interaction, and relationship references. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session/consumer association and expiry. |
| 06_CONVERSATION_ROUTING.md | Defines routing context and destination eligibility. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines authorized human context transfer. |
| 02_AGENT_PLATFORM/11_AGENT_CONTEXT_MODEL.md | Defines Agent Platform use of validated context. |
| 02_AGENT_PLATFORM/12_AGENT_INSTRUCTION_SYSTEM.md | Defines instruction authority over untrusted context. |
| 05_KNOWLEDGE_PLATFORM | Owns retrieval and knowledge content. |
| 06_MEMORY_PLATFORM | Owns memory content and lifecycle. |
| 09_SECURITY_PLATFORM | Owns identity, authorization, privacy, and compliance controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Context Model document. |
| 2.1 | 2026-08-05 | Added priority, sharing, format, migration, cache, effectiveness, emergency controls, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |
