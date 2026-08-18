# 21_AGENT_EVENT_INTEGRATION

**Version:** 3.1  
**Status:** Approved  
**Phase:** Agent Platform

---

# Purpose

This document defines how the Agent Platform publishes and consumes governed events at its integration boundary.

Event integration lets platform components communicate important facts without requiring direct, synchronous dependencies. It enables the Agent Platform to react to changes in conversations, workflows, tools, knowledge, memory, security, and external business systems while preserving clear ownership boundaries.

The event model supports the platform's **One Brain, Multi-Channel** architecture. A business event is represented once and may be consumed by voice, chat, WhatsApp, email, API, operations, analytics, and future channels without duplicating agent intelligence.

---

# Objectives

The Event Integration model must:

- Decouple producers from consumers.
- Provide a shared, versioned vocabulary for platform and business events.
- Preserve tenant isolation, authorization, traceability, and auditability.
- Support reliable asynchronous integration with internal and external systems.
- Allow agents to react to relevant events without polling for state.
- Prevent event handling from bypassing workflow, tool, security, and permission boundaries.
- Support replay, recovery, observability, and controlled evolution.
- Remain transport-independent so implementations may evolve without changing business semantics.

---

# Scope

This document defines:

- Agent-owned event categories and producer/consumer responsibilities.
- How Agent Platform adopts the shared event envelope and contract requirements.
- Agent-side publication, subscription, and consumption patterns.
- Agent Runtime integration and reaction patterns.
- Event lifecycle, schema evolution, delivery, idempotency, and ordering principles.
- Multi-tenant, security, permission, observability, and failure-handling requirements.
- Boundaries with workflows, tools, sessions, channels, and external integrations.

---

# This Document Does Not Define

This document does not define:

| Topic | Owner |
|---|---|
| Agent reasoning, planning, and response generation | `08_AGENT_EXECUTION_ENGINE.md` |
| Workflow definitions and workflow state transitions | `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` |
| Tool contracts or how an external action is executed | `15_AGENT_TOOL_SYSTEM.md` and `16_AGENT_TOOL_EXECUTION_MODEL.md` |
| Canonical conversation/session state and conversation event semantics | `03_CONVERSATION_PLATFORM` |
| Channel protocol adapters and channel UX | Digital Channel Platform and Frontend Platform |
| Platform-wide telemetry storage and dashboards | Observability Platform |
| Enterprise-wide authorization policy | Security Platform |
| Shared event envelope, Conversation event schema, broker, queue, and transport implementation | `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md` and `07_INTEGRATION_PLATFORM` |

Agent Event Integration owns the Agent Platform's producer and consumer behavior for agent facts. It does not own the shared event transport, common envelope, broker delivery implementation, or the domain state represented by an event.

Conversation Platform owns the meaning, schema, and lifecycle of conversation facts. Integration Platform owns shared broker, connector, and transport implementation. Agent Platform adopts those contracts and owns only facts about Agent Platform behavior.

---

# Architecture Principles

## Events Represent Facts

An event records that something meaningful has happened. It is not a command, a query, an instruction, or a mutable state document.

Examples:

```text
ConversationStarted
CustomerIdentityVerified
WorkflowCompleted
KnowledgeSourcePublished
ToolExecutionFailed
HumanApprovalRequested
```

Names should be expressed in the past tense because an event describes an observed fact.

## Producers Own Event Meaning

The service or platform capability that owns a business fact owns the authoritative event schema for that fact. Consumers may react to it, but must not redefine it or infer ownership of the underlying data.

## Consumers Remain Independent

Publishers must not need to know which consumers exist. Adding a consumer must not require a producer change unless the event contract itself must evolve.

## Events Are Not a Back Door

Receiving an event does not grant an agent permission to access data, invoke a tool, change workflow state, or send a user-facing message. Every resulting action must pass its normal authorization and execution controls.

## At-Least-Once Delivery Is Assumed

Distributed delivery may duplicate messages. Consumers must be idempotent and must safely handle retries. Business correctness must never depend on exactly-once delivery from infrastructure.

## Schema Evolution Is Intentional

Event contracts are versioned public interfaces. Additive, compatible change is preferred. Breaking change requires a new version or migration strategy.

## Minimal Events, Controlled Enrichment

Events contain the minimum data required for reliable routing and safe initial handling. Consumers retrieve additional authorized data through owned interfaces; they must not place sensitive, unbounded, or stale data into every event.

---

# Agent Event Ownership Model

The Agent Platform both publishes events about agent activity and consumes events from adjacent platform capabilities.

```text
Domain Owner
    |
    v
Authoritative Event
    |
    v
Event Router / Broker
    |
    +--> Agent Runtime Subscription
    +--> Workflow Subscription
    +--> Operations Subscription
    +--> Analytics Subscription
    +--> Authorized External Integration
```

## Platform Events

Platform events describe platform behavior and are owned by the platform component that produced them.

Examples include:

- `AgentExecutionStarted`
- `AgentExecutionCompleted`
- `AgentExecutionFailed`
- `AgentCapabilitySelected`
- `ToolExecutionRequested`
- `ToolExecutionCompleted`
- `WorkflowInvocationRequested`
- `WorkflowExecutionCompleted`
- `HumanEscalationRequested`

## Tenant Events

Tenant events describe tenant-scoped business activity, configuration, or operational changes. Every tenant event must carry tenant context and remain inaccessible to other tenants.

Examples include:

- `TenantAgentActivated`
- `TenantKnowledgePublished`
- `CustomerAppointmentCreated`
- `CustomerPaymentReceived`

## External Integration Events

External systems may provide events through approved connectors. Their payloads are untrusted until validated, normalized, authorized, and mapped to an internal contract.

An external provider event must never be exposed directly as a trusted internal platform event.

---

# Event Taxonomy

## Lifecycle Events

Lifecycle events record the beginning, completion, failure, cancellation, or retirement of a platform entity.

```text
AgentSessionStarted
AgentSessionEnded
AgentExecutionStarted
AgentExecutionCompleted
WorkflowStarted
WorkflowCompleted
```

## State Change Events

State change events record a meaningful approved change in business or platform state.

```text
CustomerProfileUpdated
KnowledgeDocumentPublished
AgentConfigurationActivated
PermissionGrantRevoked
```

## Decision Events

Decision events record an outcome of a controlled process. They provide traceability but do not expose private reasoning or sensitive prompt content.

```text
CapabilitySelected
WorkflowSelected
HumanApprovalRequired
EscalationDetermined
```

## Integration Events

Integration events represent normalized facts received from or sent to external systems.

```text
CRMContactUpdated
CalendarBookingConfirmed
PaymentStatusChanged
TelephonyCallEnded
```

## Operational Events

Operational events support recovery, control, and incident response.

```text
EventDeliveryFailed
SubscriptionPaused
DeadLetterCreated
SchemaValidationFailed
```

Operational events must not replace observability logs, traces, or metrics. They are domain-relevant facts that may require a business or operational response.

---

# Agent Event Contract Adoption

Every event uses a common envelope plus a domain-specific payload.

```text
Shared Event Envelope Adopted by Agent Platform
|
+-- eventId
+-- eventType
+-- eventVersion
+-- occurredAt
+-- producer
+-- tenantId
+-- organizationId (when applicable)
+-- actorContext (when applicable)
+-- aggregateType
+-- aggregateId
+-- correlationId
+-- causationId
+-- traceId
+-- classification
+-- payload
```

## Event Identity

`eventId` is globally unique and immutable. It is used for deduplication, audit correlation, and operational investigation.

## Event Type and Version

`eventType` identifies the business fact, for example `agent.workflow.completed`. `eventVersion` identifies the schema contract version, not the version of the producing service.

## Occurrence Time

`occurredAt` records when the fact occurred in the producing domain. Broker receipt time and consumer processing time are separate operational timestamps.

## Aggregate Reference

`aggregateType` and `aggregateId` identify the owned entity related to the event, such as an agent execution, workflow instance, customer interaction, or knowledge document.

## Correlation and Causation

`correlationId` connects the complete business journey across services. `causationId` identifies the immediate event, command, or request that caused this event.

These identifiers enable a sequence such as:

```text
InboundCallReceived
  -> AgentSessionStarted
  -> IdentityVerificationRequested
  -> CustomerIdentityVerified
  -> WorkflowStarted
  -> AppointmentCreated
  -> WorkflowCompleted
```

## Classification

Classification describes handling requirements, such as public platform metadata, tenant confidential, restricted, or regulated. It informs routing, retention, encryption, and consumer authorization.

---

# Event Publication Model

## Publication Boundary

Events are published only after the producing component has committed the corresponding authoritative state change, or after it has durably recorded the fact it is reporting.

The platform must not publish an event that claims a change succeeded before the responsible component can prove that it succeeded.

## Transactional Publication

Where an event represents a persisted state change, the producer should use a transactional outbox or equivalent durable publication mechanism. This avoids the inconsistency where a database update succeeds but message delivery is lost, or a message is published for a change that never committed.

```text
Domain Change
    |
    v
Domain Store + Durable Outbox
    |
    v
Publisher
    |
    v
Event Router
```

## Publication Validation

Before publication, producers must validate:

- Schema conformance.
- Required tenant and correlation context.
- Event type and version registration.
- Classification and data-minimization requirements.
- Producer authorization to emit the event.
- Absence of secrets, credentials, raw sensitive prompts, or unnecessary personal data.

## Agent Event Registry

The platform maintains a registry for approved event types. Each registered event has:

- A business owner.
- A technical owner.
- Schema and current version.
- Classification and retention requirements.
- Allowed producers and consumer eligibility rules.
- Compatibility policy.
- Documentation and lifecycle status.

---

# Event Contract Governance

Event contracts are governed interfaces. A producer must not introduce, rename, repurpose, or retire an event without a documented compatibility review.

## Naming and Namespace Rules

Event names use an explicit domain namespace and a past-tense fact name.

```text
agent.execution.completed
workflow.instance.failed
knowledge.document.published
integration.crm.contact.updated
```

The namespace identifies the owning domain. The name must describe the fact, not the transport, implementation, or intended consumer action.

## Schema Compatibility

The default compatibility policy is additive change only. Adding an optional field is normally compatible. Removing a field, changing its meaning, changing a type, or adding a required field is a breaking change.

Breaking changes require a new event version and a documented migration period. Producers and consumers must be able to operate safely during the migration period.

## Contract Approval

Before a new event type or a breaking version is published, its owner must record:

- The business purpose and authoritative producer.
- Schema, classification, and retention requirements.
- Tenant scope and consumer eligibility.
- Compatibility assessment and migration plan.
- Expected delivery volume and criticality.
- Tests proving producer and consumer conformance.

The Event Registry is the source of truth for these approvals. Source code, generated schemas, and broker configuration must remain aligned with the registered contract.

---

# Event Lifecycle and Retention

An event progresses through a controlled lifecycle:

```text
Designed
  -> Registered
  -> Validated
  -> Published
  -> Delivered
  -> Processed
  -> Retained / Archived
  -> Deprecated
  -> Retired
```

## Retention and Archival

Each event type has an approved retention classification. Retention must account for operational recovery, audit obligations, tenant agreements, data-minimization rules, and applicable regulation.

Retention of an event stream does not create permission for every consumer to access historical payloads. Archived and replayed events remain subject to their original classification and current authorization checks.

## Deprecation and Retirement

An event contract is deprecated only after its replacement, migration guidance, consumer inventory, and end-of-support date are registered. A retired event must no longer be published, but its historical records are retained or deleted according to the approved retention policy.

---

# Subscription and Consumption Model

## Subscription Registration

A consumer registers for approved event types through an explicit subscription. A subscription defines its consumer identity, allowed tenant scope, filter criteria, delivery target, retry policy, and operational owner.

Subscriptions must be reviewed when they access restricted event classes or cause externally visible actions.

## Consumer Processing Flow

```text
Event Received
    |
    v
Envelope and Schema Validation
    |
    v
Tenant and Consumer Authorization
    |
    v
Deduplication / Idempotency Check
    |
    v
Business Handling
    |
    +--> No Action
    +--> Create Authorized Work Item
    +--> Invoke Workflow
    +--> Request Tool Execution
    +--> Request Agent Execution
    |
    v
Record Outcome and Acknowledge
```

## Idempotency

Every consumer stores or derives an idempotency key, normally based on `eventId` plus consumer identity. Reprocessing the same event must not create duplicate messages, duplicate transactions, duplicate workflow instances, or repeated external actions.

## Ordering

Global ordering is neither required nor assumed. Where a sequence matters, the responsible domain must define an ordering key, normally the aggregate identifier, and the consumer must validate state before acting.

An event consumer must never assume that unrelated events arrive in chronological order.

## Acknowledgement

An event is acknowledged only after the consumer has durably recorded successful handling or has safely delegated the work to a durable, controlled process. Temporary in-memory processing is not sufficient.

---

# Agent Runtime Integration

The Agent Runtime consumes events as contextual triggers, not as direct instructions.

```text
Authorized Event
    |
    v
Event Subscription
    |
    v
Agent Trigger Policy
    |
    v
Context Assembly
    |
    v
Instruction, Permission, and Safety Validation
    |
    v
Agent Execution or Workflow Invocation
```

## Trigger Policy

An agent may react only when an approved trigger policy maps an event type to a defined capability, workflow, notification, or review queue.

A trigger policy defines:

- Eligible event types and schema versions.
- Tenant, agent, and channel scope.
- Filter and deduplication rules.
- Required permissions and approval conditions.
- The allowed response mode.
- Rate limits, cooldowns, and escalation policy.

## Event Context Is Not Instruction

Event payload data is external context. It may inform an execution but cannot override platform policy, approved instructions, permissions, persona rules, or security constraints.

This prevents event injection, including malicious upstream payloads that try to direct agent behavior.

## Reaction Modes

An event-triggered agent may:

- Record or enrich context.
- Evaluate a policy.
- Create an internal work item.
- Start an approved workflow.
- Request a tool action through the Tool System.
- Notify a human or an authorized user through a channel service.
- Take no action when relevance, authorization, or safety conditions are not met.

The agent must not directly mutate external systems merely because an event was received.

---

# Workflow Integration Boundary

Events and workflows serve different purposes.

| Concern | Event Integration | Workflow Integration |
|---|---|---|
| Primary role | Communicate a fact | Coordinate a business process |
| Control flow | Asynchronous, decoupled | Explicit, stateful, ordered |
| Owner | Producer owns event meaning | Workflow owns process state |
| Consumer behavior | React if eligible | Execute defined steps |
| Retry | Delivery and handler retry | Business recovery and compensation |

An event can start a workflow, and a workflow can publish events. Neither replaces the other.

Example:

```text
PaymentReceived event
    -> eligible workflow starts
    -> invoice is reconciled
    -> ReceiptIssued event is published
```

The event does not itself perform invoice reconciliation. The workflow owns that business process.

---

# Tool Integration Boundary

Events may request evaluation of a tool action, but they never execute tools directly.

```text
External Event
    -> Trigger Policy
    -> Agent or Workflow Decision
    -> Tool Authorization
    -> Tool Execution
    -> ToolExecutionCompleted event
```

This preserves centralized permission checks, audit records, rate limits, validation, and failure handling.

---

# Multi-Channel Event Model

Channels emit and consume normalized platform events rather than embedding channel-specific business logic inside the Agent Platform.

```text
Voice Adapter -----+
Chat Adapter ------+--> Normalized Interaction Events --> Agent Platform
WhatsApp Adapter --+
Email Adapter -----+
API Adapter -------+
```

Examples of normalized interaction events:

- `InteractionReceived`
- `InteractionDelivered`
- `InteractionFailed`
- `ConversationTransferred`
- `HumanHandoffRequested`

Channel adapters own protocol delivery details. The Agent Platform owns the agent reaction decision. A channel event must include channel identity and delivery context, but business logic must remain channel-independent whenever possible.

---

# Security Model

## Authentication and Producer Trust

Every producer and consumer has a verifiable service identity. The event infrastructure must authenticate the publisher before accepting an event and authenticate the consumer before delivery.

## Authorization

Authorization is checked at publication, subscription, and consumption time. Consumer authorization is scoped by event type, tenant, classification, and permitted action.

## Tenant Isolation

Tenant identity is required for tenant-scoped events. Routing, storage, replay, dead-letter processing, and operator access must preserve the tenant boundary.

Platform-wide events are explicitly marked as platform-scoped; absence of a tenant ID is never used as an implicit cross-tenant permission.

## Data Minimization

Events must not include:

- Secrets, tokens, passwords, or credentials.
- Full raw conversation transcripts unless explicitly justified, authorized, and protected.
- Unnecessary personal, payment, health, or regulated data.
- Hidden instructions or private model reasoning.

When sensitive details are required, publish a reference to an authorized resource rather than duplicating the data in broad event streams.

## Integrity and Non-Repudiation

The platform records producer identity, event ID, schema version, timestamps, and handling outcomes. Sensitive or regulated events may require stronger integrity controls according to Security Platform policy.

---

# Observability and Audit

Every event must be traceable from production to final handling outcome.

## Required Telemetry

- Event type, version, and ID.
- Producer and consumer identities.
- Tenant scope and classification, without leaking sensitive payloads.
- Correlation, causation, and trace identifiers.
- Delivery attempts, latency, and final disposition.
- Validation, authorization, filtering, and deduplication decisions.
- Trigger-policy and resulting workflow or tool references.

## Metrics

```text
Event Metrics
|
+-- Publication rate
+-- Delivery latency
+-- Consumer success rate
+-- Retry count
+-- Dead-letter count
+-- Schema validation failures
+-- Duplicate deliveries
+-- Trigger-policy matches
+-- Unauthorized access attempts
```

## Audit Trail

Audit records must identify which event caused a material automated action. The audit record links the event, applicable trigger policy, agent/workflow execution, authorization decision, tool action if any, and final outcome.

---

# Failure Handling and Recovery

## Validation Failure

Malformed, unknown, unauthorized, or incompatible events must be rejected or quarantined. They must not reach the Agent Runtime as usable context.

## Transient Delivery Failure

Delivery failures use bounded retry with exponential backoff and observability. Retry policy must avoid overwhelming dependent systems.

## Poison Event

An event that repeatedly fails consumer handling is moved to a restricted dead-letter flow with the error classification, consumer identity, attempts, and correlation metadata. It is not silently discarded.

## Replay

Replay is an operationally controlled recovery action. Before replay, operators must verify tenant scope, schema compatibility, idempotency behavior, permission changes, and potential external side effects.

Replaying an event must not bypass current security or policy controls.

## Graceful Degradation

When event processing is delayed or unavailable, the platform should preserve durable events, surface appropriate operational health, and defer non-critical reactions. Safety-critical or user-impacting processes must follow their defined escalation and recovery procedures.

---

# Capacity and Operational Controls

Event processing must remain stable during normal demand, burst traffic, consumer failure, and controlled replay.

## Backpressure and Prioritization

Consumers must apply bounded concurrency and backpressure rather than accepting unlimited work. The platform may classify event flows by criticality so that safety, security, and customer-impacting events receive appropriate processing priority.

Low-priority processing such as analytics enrichment must not prevent time-sensitive operational events from being delivered.

## Lag, Quotas, and Rate Limits

Every subscription has an observable lag threshold, throughput expectation, and bounded retry policy. Producers, consumers, tenants, and external integrations may be subject to rate limits and quotas to prevent a faulty or abusive source from degrading the platform.

Threshold breaches must create an operational signal and follow the service's escalation policy.

## Operational Ownership

Each production subscription has a named operational owner responsible for its configuration, health, recovery procedure, and consumer lifecycle. Only authorized operators may:

- Pause or resume a subscription.
- Inspect restricted dead-letter payloads.
- Approve a replay or discard operation.
- Change retention, filtering, rate limits, or delivery configuration.

These actions must produce an audit record with the actor, scope, reason, and resulting outcome.

---

# Testing Strategy

Event Integration is validated before release and during operational change.

## Contract Tests

Producers must test generated events against the registered schema. Consumers must test the supported schema versions and explicitly reject or quarantine incompatible input.

## Integration Tests

Integration tests verify authorization, tenant routing, correlation propagation, durable publication, subscription filters, and the controlled handoff to workflows or tools.

## Resilience Tests

Resilience tests simulate duplicate delivery, out-of-order delivery, consumer restart, broker interruption, retry exhaustion, dead-letter routing, and approved replay. These tests verify that external actions are not duplicated and that recovery remains observable.

## Security Tests

Security tests verify producer and consumer identity, subscription authorization, tenant isolation, payload classification, redaction, and protection against event-injection attempts.

---

# Best Practices

- Publish facts, not commands disguised as events.
- Keep event schemas small, explicit, versioned, and owned.
- Include correlation, causation, tenant, and classification context.
- Make all consumer handling idempotent.
- Use workflows for stateful business processes and tools for controlled external actions.
- Treat incoming external events as untrusted until normalized and authorized.
- Create explicit trigger policies for any agent reaction.
- Monitor lag, delivery failure, replay, and dead-letter flows.
- Document producer, consumer, schema, retention, and ownership in the event registry.

---

# Anti-Patterns

## Event as Remote Procedure Call

Publishing an event while expecting one specific consumer to perform an immediate required action creates hidden synchronous coupling. Use a command or workflow interface when a direct, accountable request is needed.

## Event Payload as a Database Snapshot

Large mutable entity snapshots create leakage, stale reads, brittle contracts, and unnecessary coupling. Publish the relevant fact and stable references instead.

## Agent Action Without Policy

Allowing any received event to automatically trigger an agent response or external action bypasses safety and authorization controls. Use an explicit trigger policy.

## Cross-Tenant Fan-Out

Routing tenant data to broad platform or external subscriptions violates isolation. Tenant scope must be explicit and enforced end-to-end.

## Unbounded Retry

Retrying failures indefinitely can duplicate business action and amplify an incident. Retry must be bounded, observable, and paired with dead-letter handling.

## Breaking Schema Change in Place

Changing the meaning or required fields of a live event without versioning breaks independent consumers. Use a compatible additive change or publish a new version.

---

# Architecture Boundaries

| Document | Relationship |
|---|---|
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Defines how runtime components receive approved event context. |
| `08_AGENT_EXECUTION_ENGINE.md` | Determines reasoning and execution after an eligible trigger; it does not trust event payloads as instructions. |
| `11_AGENT_CONTEXT_MODEL.md` | Defines how validated event data enters transient execution context. |
| `12_AGENT_INSTRUCTION_SYSTEM.md` | Governs agent behavior and always remains authoritative over event content. |
| `14_AGENT_CAPABILITY_MODEL.md` | Defines capabilities an event-triggered execution may select. |
| `15_AGENT_TOOL_SYSTEM.md` | Controls tool authorization and execution requested as a result of an event. |
| `18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Memory-owned, governed memory signals. |
| `19A_AGENT_KNOWLEDGE_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Knowledge-owned lifecycle signals and retrieval. |
| `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Integration-owned workflow contracts that can start from or publish events. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Defines channel adapters that normalize interaction events. |
| `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md` | Owns conversation-event meaning, schemas, and lifecycle. |
| `03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md` | Owns canonical conversation/session coordination and session facts. |
| `07_INTEGRATION_PLATFORM` | Owns shared event broker, connector, and transport implementation. |
| `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent consumption of Security-owned controls applied to event-triggered actions. |
| `13_OBSERVABILITY_PLATFORM` | Owns telemetry infrastructure, retention, dashboards, and alerting. |

---

# Final Summary

Event Integration provides the Agent Platform with a reliable, secure, and extensible way to communicate and react across platform capabilities and external systems. Events represent owned facts, not instructions or uncontrolled execution paths.

By using explicit event contracts, trigger policies, tenant isolation, idempotent consumers, controlled replay, and end-to-end observability, the platform can evolve toward a large multi-channel AI Employee ecosystem without coupling agent intelligence to individual channels, services, or vendors.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Event Integration architecture document. |
| 2.1 | 2026-08-05 | Added contract governance, lifecycle and retention, capacity controls, operational ownership, and validation strategy. |
| 3.0 | 2026-08-06 | Re-scoped this document to Agent event integration; Conversation owns conversation facts and Integration owns shared event transport. |
| 3.1 | 2026-08-08 | Approved after Digital Channel, Observability, Testing, Conversation, Security, and Integration boundary review; replaced deprecated boundary references. |
