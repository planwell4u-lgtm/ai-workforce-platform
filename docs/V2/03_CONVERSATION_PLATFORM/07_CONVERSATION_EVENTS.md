# 07_CONVERSATION_EVENTS

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines the conversation facts that the Conversation Platform publishes and consumes through governed events.

Conversation events communicate durable changes in conversation lifecycle, participant association, interaction, session, routing, handoff, context, and delivery disposition. They enable loose coupling between channels, Agent Platform, workflows, analytics, operations, and other authorized consumers without making the event bus a substitute for canonical state or authorization.

---

# Purpose

The purpose of the Conversation Events Model is to provide a shared, versioned, tenant-safe vocabulary for cross-platform reaction to conversation activity.

It ensures events represent owned facts, use stable schemas and correlation, preserve tenant/classification boundaries, support idempotent consumption and recovery, and never grant direct permission to read conversations, act externally, or deliver messages.

---

# Objectives

The Conversation Events Model must:

- Define Conversation Platform-owned event categories, ownership, naming, envelopes, and lifecycle.
- Publish events only after durable canonical state or fact recording.
- Carry required tenant, classification, correlation, causation, provenance, and version context.
- Support authorized subscriptions, idempotency, ordering, retry, dead-letter, replay, and audit.
- Treat channel/provider input as untrusted until validation and normalization complete.
- Keep event payloads minimal and use authorized references instead of broad content duplication.
- Preserve event compatibility during schema and lifecycle evolution.
- Remain independent of broker, queue, cloud vendor, or consumer implementation.

---

# Scope

This document defines conversation event taxonomy, envelope, publication, subscription, consumption, schema governance, security, recovery, observability, testing, and artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise event broker, queue, storage, transport, and deployment implementation | 07_INTEGRATION_PLATFORM and 12_DEPLOYMENT_PLATFORM |
| Agent Platform-owned execution, tool, workflow, or model events | 02_AGENT_PLATFORM |
| Channel-native webhook, telephony, media, or delivery protocol implementation | Voice and relevant Channel Platforms |
| Canonical conversation state, session, routing, context, and handoff rules | 01–06 and 08–09 Conversation Platform documents |
| Enterprise authorization, key management, security monitoring, and retention infrastructure | 09_SECURITY_PLATFORM |
| Analytics storage, transformations, and reporting | 08_DATA_PLATFORM |
| Project-wide event standard and architecture decision | 00_CONTROL and system architecture documentation |

---

# Event Principles

## Events Represent Conversation Facts

An event records an observed conversation fact, not a command, query, mutable snapshot, or instruction. For example, conversation.created, interaction.received, participant.verified, routing.decided, handoff.requested, and conversation.closed.

## Conversation Platform Owns Meaning

Conversation Platform owns schema and semantic meaning for facts about its canonical entities. Consumers may react but cannot redefine state, infer permission, or make a channel/provider payload the authoritative conversation fact.

## Publish After Durable State

A state-changing event is published only after the corresponding canonical transition or fact is durably recorded. Transactional outbox or equivalent reliable publication pattern is used where required.

## Minimal Payload, Controlled Retrieval

Events contain routing and integrity context plus the minimum safe payload. They reference protected content, context, session, or participant data through authorized interfaces instead of copying raw transcripts, recordings, attachments, credentials, or private reasoning.

## At-Least-Once Delivery

Consumers assume duplicate delivery and use idempotency. Business correctness never depends on exactly-once broker behavior.

## Events Do Not Authorize Action

Receiving an event does not authorize agent reasoning, context access, workflow start, tool execution, delivery, or human visibility. Each resulting operation evaluates current policy and permission.

---

# Event Taxonomy

| Category | Examples |
|---|---|
| Conversation lifecycle | conversation.created, conversation.activated, conversation.waiting, conversation.closed, conversation.archived |
| Interaction | interaction.received, interaction.accepted, interaction.rejected, interaction.delivery_requested, interaction.delivery_recorded |
| Participant and identity | participant.association_created, participant.verification_completed, participant.visibility_changed |
| Session and context | session.created, session.expired, context.snapshot_issued, context.snapshot_revoked |
| Routing and handoff | routing.decided, routing.deferred, handoff.requested, handoff.assigned, handoff.completed |
| Security and policy | conversation.access_denied, conversation.tenant_mismatch_detected, conversation.consent_changed |
| Recovery and operations | conversation.reconciliation_required, conversation.state_conflict_detected, conversation.restore_requested |

Event names use lowercase domain namespace plus past-tense fact. A provider-specific event is normalized before it enters this taxonomy.

---

# Event Envelope

~~~text
Conversation Event Envelope
    +-- eventId
    +-- eventType
    +-- eventVersion
    +-- occurredAt / recordedAt
    +-- producer and producerVersion
    +-- tenantId / organizationId / environment
    +-- conversationId / interactionId / participantId / sessionId
    +-- aggregateType / aggregateId / aggregateVersion
    +-- correlationId / causationId / traceId
    +-- classification / retention reference
    +-- source provenance / idempotency reference
    +-- payload or authorized payload reference
~~~

The envelope distinguishes fact occurrence from platform recording, broker receipt, and consumer processing. It does not contain reusable credentials or broad sensitive content.

---

# Publication Model

## Publication Triggers

Conversation Platform publishes after durable creation, transition, association, routing, handoff, context, delivery disposition, reconciliation, or retention fact. The producer validates schema, tenant, classification, naming, source provenance, authorization, and data minimization before publication.

## Transactional Publication

When an event represents persisted state, canonical state and outbox record are committed together or through an equivalent durable pattern. Publication retries do not create a new fact; they reuse the original event ID and idempotency reference.

## Event Registry

Each event type has business/technical owner, schema, classification, producer eligibility, consumer eligibility, retention, compatibility, delivery criticality, volume expectation, documentation, lifecycle status, and test evidence.

---

# Subscription and Consumption

## Delivery Classes

Each registered event has one delivery class. The class guides operational handling; it does not change the event's domain meaning or authorize a consumer action.

| Class | Use | Expected handling |
|---|---|---|
| Critical operational | A lost or delayed fact can materially affect active conversation safety, continuity, or required recovery. | Durable publication, defined consumer acknowledgement, rapid alerting, controlled reconciliation, and documented recovery owner. |
| Standard business | A durable fact supports normal platform coordination, automation, audit, or reporting. | Durable publication, bounded retry, monitoring, dead-letter handling, and replay procedure. |
| Informational | A non-authoritative fact supports diagnostics, measurement, or optional experience improvement. | Best-effort or bounded durable handling as registered; it must not be the sole trigger for a required business outcome. |

## Subscription Registration

A consumer subscription identifies service identity, owner, event type/version, tenant scope, filter, delivery target, retry/dead-letter policy, classification eligibility, and operational contact. Restricted events require review before activation.

## Consumer Flow

~~~text
Event Received
    |
    v
Envelope and Schema Validation
    |
    v
Tenant, Classification, and Subscription Authorization
    |
    v
Idempotency and Aggregate/State Check
    |
    v
Authorized Consumer Handling
    |
    v
Durable Outcome and Acknowledgement
~~~

## Ordering and Idempotency

Global ordering is not assumed. Consumers use aggregate version, aggregate ID, occurrence/recorded time, and state validation where sequence matters. Idempotency key is normally event ID plus consumer identity; duplicate handling must not repeat delivery, route, handoff, external action, or business change.

---

# Schema Evolution and Lifecycle

Additive optional fields are preferred. Removing a field, changing meaning/type, changing tenant/classification semantics, or adding required fields creates a new event version and migration plan.

An event type progresses through designed, registered, validated, published, active, deprecated, retired, and archived. Deprecation records replacement, consumer inventory, authoritative schema location, support end, compatibility, migration owner, and retirement conditions. A producer must not retire a version until its registered support window has ended and affected consumer owners have completed or accepted the documented migration path.

---

# Security, Privacy, and Tenant Controls

Every tenant event includes authoritative tenant scope. Publisher, broker, consumer, replay, dead-letter, and operational access validate tenant, classification, subscription, purpose, and current authorization.

External/provider payloads are untrusted until signature/authenticity, source binding, replay, schema, content, tenant, and normalization checks complete. Events exclude secrets, raw hidden instructions, private reasoning, unnecessary content, and cross-tenant references.

Replay, dead-letter inspection, discard, and subscription change are controlled tenant-scoped operations. Historical event access does not override current classification, consent, retention, or authorization.

## Retention, Redaction, and Legal Hold

The registry records the event's retention category and whether its payload is self-contained or references protected data. Retention and deletion are implemented by the Data and Security Platforms, while this document requires conversation event handling to honor their decisions.

When consent is withdrawn, content is redacted, data is deleted, or a legal hold applies, the event's immutable audit identity may remain only as policy permits; protected payload references must resolve according to current access, retention, and hold rules. Replay must tolerate an unavailable, redacted, or access-restricted reference and must not restore deleted content or bypass a hold.

---

# Failure, Replay, and Reconciliation

Malformed, unknown, unauthorized, incompatible, or tenant-mismatched events are rejected or quarantined. Transient delivery failure uses bounded retry/backoff. Poison events move to restricted dead-letter flow with error/category/consumer/attempt/correlation evidence.

Replay verifies tenant, schema, idempotency, current policy, aggregate state, retention, consumer eligibility, and external-side-effect risk. It does not blindly recreate a delivery, workflow, or tool action.

A state conflict or uncertain outcome emits a reconciliation-required fact. The authoritative Conversation state and controlled source/provider checks determine resolution; consumers must not overwrite canonical state from an event.

---

# Observability and Audit

Telemetry records event type/version/ID, producer/consumer, tenant/classification, aggregate, correlation, delivery/processing latency, validation/authorization/idempotency result, retry, dead-letter, replay, and final disposition.

Metrics include publication rate, schema failure, unauthorized subscription, duplicate delivery, consumer success, lag, dead-letter, replay, tenant mismatch, conflict, and event-to-outcome correlation. Raw payload is excluded from normal telemetry.

---

# Testing Strategy

## Contract Tests

Validate envelope, event schema, naming, ownership, classification, version, provenance, required fields, and compatibility.

## Integration Tests

Validate durable publication, subscription authorization, tenant routing, correlation, idempotency, aggregate ordering, Agent/Channel/Workflow consumer boundaries, retry, dead-letter, and replay.

## Security and Resilience Tests

Simulate forged provider event, missing tenant, schema mismatch, duplicate, delayed/out-of-order event, consumer restart, poison event, unauthorized dead-letter access, replay, and conflicting aggregate state. Prove no event bypasses policy or duplicates side effects.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation event registry | Defines types, owners, schemas, status, classification, retention, consumers, and compatibility | Conversation Platform |
| Event envelope and schema catalog | Defines the Conversation semantic profile, versioned envelope use, and event payload contracts; records the authoritative schema location and support window | Conversation Platform with Integration owner |
| Producer publication policy | Defines validation, outbox, provenance, minimization, authorization, and error behavior | Conversation Platform |
| Subscription and consumer policy | Defines registration, eligibility, tenant/filter scope, idempotency, retry, dead-letter, and ownership | Conversation Platform with Security and Operations owners |
| Event compatibility and migration policy | Defines change, deprecation, inventory, overlap, support end, and retirement | Conversation Platform with dependent owners |
| Replay and reconciliation procedure | Defines authorization, aggregate/state, side-effect, audit, and recovery safeguards | Conversation Platform with Integration and Operations owners |
| Conversation event test suite | Validates contract, tenant, integration, security, resilience, replay, and compatibility | Conversation Platform and Testing Platform |

---

# Anti-Patterns

## Event as Command

Publishing a conversation event while expecting a specific consumer to perform required synchronous work creates hidden coupling. Use an accountable API/workflow boundary for direct request.

## Raw Provider Webhook as Trusted Fact

Provider payloads require validation and normalization; they cannot directly become internal canonical events.

## Event Payload as Transcript

Large mutable transcripts and sensitive snapshots create stale data, privacy risk, and coupling. Publish facts and authorized references.

## Consumer Writes Canonical State Directly

A consumer must request a controlled Conversation Platform transition rather than updating conversation state from an event.

## Replay Repeats External Action

Replay is recovery of event handling, not permission to resend a message or repeat a business action.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Event Publisher and platform boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines lifecycle facts and transition state. |
| 03_CONVERSATION_MODEL.md | Defines event aggregate/entity references. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session facts and associations. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context snapshot/revocation facts. |
| 06_CONVERSATION_ROUTING.md | Defines routing/assignment facts. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines handoff facts and collaboration behavior. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines canonical state, concurrency, and reconciliation. |
| 02_AGENT_PLATFORM/21_AGENT_EVENT_INTEGRATION.md | Defines Agent Platform event integration boundary; Conversation owns conversation-event meaning. |
| 07_INTEGRATION_PLATFORM | Owns broker/connector implementation. |
| 09_SECURITY_PLATFORM | Owns enterprise event security controls. |
| 13_OBSERVABILITY_PLATFORM | Owns telemetry infrastructure. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Events document. |
| 2.1 | 2026-08-06 | Added delivery classes, schema support controls, and retention/redaction/legal-hold replay safeguards. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |
