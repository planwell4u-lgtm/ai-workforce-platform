# 23_AGENT_SESSION_MANAGEMENT

**Version:** 3.1  
**Status:** Approved  
**Phase:** Agent Platform

---

# Purpose

This document defines how Agent Platform receives and uses Conversation Platform-approved execution-session associations, context snapshots, and outcome-reporting paths.

Conversation Platform provides the canonical continuity layer for the **One Brain, Multi-Channel** architecture. Agent Platform receives bounded execution work for an authorized conversation or approved event trigger without allowing a channel address, provider thread, or transient runtime process to become the authoritative record of user context.

---

# Objectives

The Session Management model must:

- Consume an authoritative, tenant-scoped conversation/session association from Conversation Platform.
- Separate long-lived conversation continuity from short-lived Agent Runtime execution state.
- Support safe, explicit cross-channel continuation and human handoff.
- Preserve identity-assurance, consent, authorization, classification, and audit context.
- Prevent unauthorized conversation linking, session fixation, replay, and cross-tenant access.
- Allow concurrent, asynchronous, and event-triggered work without corrupting state.
- Support expiry, closure, recovery, retention, and controlled replay.
- Keep session state independent of any channel, model provider, runtime worker, or deployment instance.

---

# Scope

This document defines:

- Agent use of conversation, participant, channel-thread, execution-session, and work-item references.
- Agent execution lifecycle after Conversation Platform has resolved, created, resumed, transferred, or closed canonical conversation/session state.
- Agent-side consistency, outcome reporting, cancellation, tenant context, observability, and testing requirements.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Canonical conversation state, session lifecycle, participant association, channel mapping, routing, handoff, and context authorization | Conversation Platform |
| Channel protocol mapping, transport, and message delivery implementation | Digital Channel Platform or Voice Platform; Integration Platform provides shared connector controls where applicable |
| Agent reasoning and response generation | `08_AGENT_EXECUTION_ENGINE.md` |
| Runtime worker lifecycle and execution scheduling | `07_AGENT_RUNTIME_ARCHITECTURE.md` |
| Durable business-process state | `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` |
| Conversation event schema and broker delivery behavior | `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md` and `07_INTEGRATION_PLATFORM` |
| Memory retention, retrieval, and forgetting policy | `18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT.md` |
| Tool authorization and external action execution | `15_AGENT_TOOL_SYSTEM.md` and `16_AGENT_TOOL_EXECUTION_MODEL.md` |
| Enterprise identity, privacy, authorization, and retention policy | Security Platform |

---

# Core Concepts

## Conversation

A **conversation** is the canonical, tenant-scoped record of an ongoing or historical interaction context around a permitted business purpose. It may span one or more channels, participants, agent executions, workflow instances, and human handoffs.

A conversation is not a raw transcript, a provider thread, or an agent memory store. It contains controlled references and metadata that allow authorized services to locate the right context.

## Execution Session

An **execution session** is a bounded runtime context used to process one interaction, event, scheduled task, or approved continuation. It has a defined start, state snapshot, authorization context, execution outcome, and expiry.

One conversation may have many execution sessions. An execution session must not be assumed to persist simply because the conversation remains open.

## Channel Thread

A **channel thread** is a provider- or channel-native grouping such as a phone call, chat thread, email chain, or messaging conversation. It is an external reference mapped to a canonical conversation only after validation and authorization.

## Participant

A **participant** is a tenant-scoped representation of a person, organization, service, or agent involved in a conversation. Channel identifiers are evidence associated with a participant; they do not themselves prove identity or authorization.

## Work Item

A **work item** represents durable work that may outlive an execution session, such as a human-review request, deferred notification, or follow-up task. Workflows own workflow state; Session Management only records the authorized relationship to the originating conversation.

---

# Architecture Principles

## Conversation Platform Is the Canonical Owner

Conversation Platform owns authoritative conversation/session identifiers, lifecycle state, participant associations, channel-thread mappings, and continuity metadata. Agent Runtime consumes approved references and snapshots but cannot become a source of truth for canonical conversation/session state.

## Conversation Is Not Execution

Conversation continuity and runtime execution are deliberately separated. A session receives a bounded, authorized snapshot of relevant conversation context; it does not hold an unrestricted mutable lock on the conversation.

## Identity and Purpose Precede Linking

Before associating an interaction with an existing conversation, the platform verifies tenant, participant evidence, business purpose, classification, and required identity assurance. Matching an email address or phone number is never sufficient on its own for sensitive linkage.

## State Is Minimal and Referenced

The canonical record stores only the metadata and references needed for continuity, routing, policy, and audit. Large transcripts, attachments, tool payloads, sensitive records, and model context remain in their governed owner systems.

## Every Continuation Is Reauthorized

Resuming a conversation, accepting an event trigger, switching channel, or transferring to a human does not inherit unlimited authorization from an earlier interaction. The current action is evaluated under current policy, permissions, consent, and identity evidence.

## Optimistic Concurrency Is the Default

Concurrent channel messages, callbacks, agent executions, and workflow outcomes are expected. State changes use versioning or equivalent concurrency control; conflicting updates are resolved through defined business rules rather than last-write-wins behavior.

---

# Session Architecture

```text
Channel Adapter / Event Source
    |
    v
Session Resolver
    |
    +--> Create New Conversation
    +--> Resolve Existing Conversation
    +--> Require Identity Verification
    +--> Queue Human Review
    |
    v
Conversation and Session Store
    |
    +--> Authorized Context Snapshot --> Agent Runtime
    +--> Conversation Reference -------> Workflow / Tool Systems
    +--> Lifecycle Events -------------> Event Integration
```

## Conversation Session Resolver

Conversation Platform's Session Resolver receives a validated interaction or approved trigger and determines whether to create a new conversation, associate it with an existing conversation, resume an eligible session, request verification, or route the interaction for review. Agent Platform receives only the resulting authorized execution request.

It must apply tenant scope, identity assurance, consent, channel mapping, purpose, classification, lifecycle state, and concurrency rules before making the association.

## Conversation and Session Store Boundary

Conversation Platform provides durable, auditable canonical state for conversation and execution-session records. Agent Platform keeps only bounded runtime execution state and submits outcomes or controlled change requests through approved Conversation Platform contracts.

---

# Canonical Data Model

```text
Conversation
|
+-- conversationId
+-- tenantId
+-- organizationId (when applicable)
+-- lifecycleState
+-- purpose and classification
+-- participantReferences
+-- channelThreadMappings
+-- identityAssuranceSummary
+-- consentSummary
+-- currentVersion
+-- createdAt / updatedAt / expiresAt / closedAt
+-- correlationId / traceId
|
+-- Execution Session
    |
    +-- sessionId
    +-- conversationId (when applicable)
    +-- triggerReference
    +-- executionMode
    +-- authorizedContextSnapshotReference
    +-- authorizationDecisionReference
    +-- state and version
    +-- startedAt / expiresAt / completedAt
    +-- runtimeExecutionReference
```

## Required Conversation Fields

Every conversation record must include a globally unique immutable `conversationId`, tenant identity, lifecycle state, classification, creation metadata, current version, and retention or expiry policy reference.

Participant associations, channel mappings, and identity evidence use separately auditable records or references so that they can be updated, revoked, or restricted without rewriting historical interaction facts.

## Required Execution Session Fields

Every session must include a globally unique immutable `sessionId`, a trigger reference, execution mode, tenant identity, state, expiry, state version, and references to the authorization decision and context snapshot used for that execution.

An agent execution must record its session reference. A session may link to a conversation where permitted, but approved background and event-triggered work may have no user conversation.

---

# Contract Governance

The conceptual model in this document must be implemented as a versioned, machine-readable Conversation and Session contract, using JSON Schema, OpenAPI, Protobuf, or an equivalent platform standard.

The executable contract defines field types, required and optional fields, identifier formats, lifecycle enumerations, retention attributes, context-snapshot references, error responses, and compatibility policy. Additive changes are preferred. Removing or changing the meaning, type, or required status of a field requires a new contract version and documented migration.

Conversation Platform owns this canonical contract. Agent Runtime, channel adapters, workflows, and tools consume it through approved interfaces and must not create private competing session models.

---

# Lifecycle Model

## Conversation Lifecycle

```text
Created
    -> Active
    -> Waiting for Participant / Waiting for Human / Suspended
    -> Resumed
    -> Closed
    -> Retained / Archived
    -> Deleted or Anonymized (when policy requires)
```

A conversation can be closed by completion, explicit participant request, inactivity, policy, security action, or operational recovery. Closed conversations are not automatically reopened: any new interaction must pass current resolution and authorization rules.

## Execution Session Lifecycle

```text
Created
    -> Authorized
    -> Running
    -> Waiting for Controlled Work
    -> Completed / Failed / Cancelled / Expired
    -> Retained for Audit
```

An execution session is terminal after completion, failure, cancellation, or expiry. Continuation creates a new session linked by correlation and, when permitted, by conversation reference.

## Lifecycle Transition Rules

Conversation Platform enforces the canonical lifecycle state machine; Agent Runtime may request controlled transitions or submit outcomes but cannot write canonical state directly.

| Entity | Transition | Authorized initiator | Required condition | Result |
|---|---|---|---|---|
| Conversation | Created → Active | Session Resolver | Valid tenant, purpose, and initial policy decision | Canonical conversation is available for authorized sessions |
| Conversation | Active → Waiting | Agent, workflow, or human handoff service | A durable follow-up, participant response, or human action is required | Waiting reason and owner are recorded |
| Conversation | Active/Waiting/Suspended → Closed | Authorized system or operator | Completion, expiry, explicit request, security action, or policy condition | New inbound work must resolve again under current policy |
| Conversation | Closed → Active | Session Resolver only | New interaction passes current identity, consent, purpose, and continuity rules | Reopened lifecycle history is recorded |
| Session | Created → Authorized | Session Resolver | Context, authorization, and expected conversation version are valid | Immutable context snapshot is issued |
| Session | Authorized → Running | Agent Runtime | Assigned execution is permitted and not expired | Runtime execution reference is recorded |
| Session | Running/Waiting → Completed/Failed/Cancelled | Authorized runtime, workflow, or operator process | Durable outcome and audit details are available | Terminal state and resulting references are recorded |
| Session | Created/Authorized/Running/Waiting → Expired | Session Management | Expiry policy is reached | Any later continuation requires a new session |

Every transition records actor or service identity, reason, timestamp, expected and resulting version, correlation identifiers, and any relevant policy decision reference.

## Expiry and Inactivity

Session expiry is determined by execution mode, channel constraints, tenant policy, risk classification, and operational need. Inactivity may close a conversation or move it to a waiting state, but must not erase retained records before the approved retention policy permits it.

Expiry is not a substitute for revoking consent, access, or sensitive context. Those changes take effect immediately according to their owning policy system.

---

# Session Resolution and Continuity

## Inbound Resolution Flow

```text
Validated Interaction or Trigger
    |
    v
Tenant and Channel Binding
    |
    v
Participant Evidence and Consent Check
    |
    +--> Insufficient Evidence --> Verification or Review
    |
    v
Eligible Conversation Lookup
    |
    +--> No Eligible Match --> Create New Conversation
    |
    v
Purpose, Classification, and Lifecycle Check
    |
    v
Create Authorized Execution Session
```

## Conversation Lookup Boundary

Conversation Platform performs lookup using tenant, approved channel-thread mapping, participant evidence, business purpose, lifecycle state, data classification, and configured continuity window. Agent Runtime does not query or expose canonical conversation data outside its authorized execution scope.

The resolver may identify candidate conversations, but automatic association is permitted only when the configured assurance and policy conditions are satisfied. Ambiguity creates a verification or human-review path.

## Session Resolution Decision Table

| Condition | Resolution | Required control |
|---|---|---|
| No eligible canonical conversation | Create a new conversation and execution session | Validate tenant, channel, participant evidence, purpose, and consent |
| One eligible conversation with sufficient assurance | Associate the interaction and create a new execution session | Validate lifecycle, classification, continuity window, and current authorization |
| Multiple eligible candidates | Do not associate automatically | Request verification or queue human review |
| Existing channel thread with revoked consent or insufficient assurance | Do not resume the prior conversation | Apply current consent/identity policy and create restricted work or verification flow if permitted |
| Interaction targets a closed conversation | Re-evaluate as a new inbound resolution | Closed state never grants automatic reopening or inherited permissions |
| Approved event has no participant conversation | Create event-triggered execution session only | Trigger policy, tenant scope, and event authorization are required |
| Event references an existing conversation | Link only if the trigger policy permits it | Re-check classification, lifecycle, permissions, and idempotency |

## Cross-Channel Continuity

Cross-channel continuation requires a policy-approved link between the participant, source channel, target channel, and conversation purpose. The platform records the source, target, actor, evidence, consent, and resulting association.

Only the minimum authorized context is available through the target channel. For example, a verified voice interaction may request a secure email summary, but a sensitive transcript is not automatically copied into email.

## Event-Triggered Sessions

An approved event can create an execution session without a conversation. If it relates to an existing conversation, linkage occurs only through an explicit trigger policy and current authorization checks. Event payloads are untrusted context until validated through Event Integration.

---

# Context Snapshot and State Access

## Bounded Context Snapshot

Before execution, Session Management and the Context Model assemble a bounded snapshot containing only the conversation metadata, participant state, interaction references, channel capability, consent, classification, and other authorized context required for that execution.

The snapshot has an immutable reference, creation time, expiry, classification, and policy basis. It prevents an execution from silently receiving unrelated future conversation updates or unrestricted historical data.

## State Mutation

An agent or runtime worker does not directly mutate canonical conversation state. It requests an approved update through the Session Management service, which validates authorization, lifecycle, schema, tenant scope, and expected record version.

Typical approved updates include adding an authorized channel mapping, recording a handoff, changing lifecycle state, attaching a work-item reference, or recording a participant-verification outcome. Transcript storage, memory writing, workflow state, and tool side effects remain owned elsewhere.

## Concurrency and Ordering

Every mutable conversation and session record has a version or equivalent concurrency token. A state update supplies the expected version. If the state has changed, the platform retries only where the update is demonstrably safe; otherwise it re-resolves policy and context or routes for review.

The platform does not assume global message order. It records source sequence data where available and validates state before acting on delayed, duplicated, or out-of-order interactions.

## Persistence, Cache, and Conflict Rules

Canonical conversation and session records are durably stored in a tenant-scoped authoritative store. Lifecycle changes, channel links, handoffs, and session outcomes use atomic persistence with an expected version check. Events representing a committed state change use a transactional outbox or equivalent durable publication mechanism.

Caches are read-through performance aids only. They must be tenant-scoped, bounded by classification, invalidated or version-checked after writes, and never used as the authority for lifecycle or authorization decisions. A cache miss or stale cache must resolve through the authoritative store.

When an expected-version conflict occurs, the caller may retry only idempotent updates that do not depend on stale policy or context. Otherwise it must reload the current state and re-run resolution, authorization, and business rules; it must not overwrite the newer record.

---

# Human Handoff and Collaboration

## Handoff Model

Human handoff creates a governed assignment or work item linked to the conversation and initiating session. It records the reason, target role or queue, allowed context, participant notification state, and return-to-agent conditions.

The human receives only the data they are authorized to access. A handoff is not permission to reveal hidden instructions, private reasoning, unrelated tenant data, or restricted historical context.

## Human and Agent Coexistence

The lifecycle state indicates whether an agent may respond, whether a human has exclusive control, and whether the user is waiting. Concurrent agent and human responses must follow a defined ownership rule to prevent contradictory messages.

When a human returns work to the agent, a new authorized execution session is created; the original agent session is not silently revived.

---

# Workflow and Tool Boundaries

Workflows and tools may use conversation and session references for correlation, authorized context lookup, and audit. They do not own conversation lifecycle or mutate conversation records directly.

```text
Conversation / Session Reference
    -> Agent or Workflow Decision
    -> Tool Authorization and Execution
    -> Result Reference
    -> Approved Session Update or Event
```

A tool result or workflow completion does not automatically re-open a conversation, send a message, or expose data to a participant. Any follow-up requires the appropriate trigger, delivery authorization, and current session policy.

---

# Event Integration Boundary

Agent Platform publishes and consumes Agent-owned events through the approved shared event contract. Conversation session and lifecycle events are defined by `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md`.

Examples include:

- `conversation.created`
- `conversation.closed`
- `conversation.channel_linked`
- `session.created`
- `session.authorized`
- `session.completed`
- `session.expired`
- `human.handoff_requested`
- `participant.verification_completed`

Events record facts and support decoupled reactions. They do not create permission to read a conversation, resume a session, alter lifecycle state, or send a user-facing message without current authorization.

---

# Security, Privacy, and Tenant Isolation

## Tenant Boundary

Tenant identity is mandatory for tenant-scoped conversations and sessions. Storage partitioning, lookup, caching, events, operational tooling, replay, and support access must enforce that boundary. Missing tenant context never implies platform-wide access.

## Session Security

Session identifiers must be unguessable, scoped, and protected against fixation, replay, substitution, and unauthorized disclosure. Channel-native identifiers are stored as controlled mappings and must not be treated as bearer authorization tokens.

## Identity Assurance and Consent

The session record includes references to the evidence and policy decision used for the current interaction, rather than making a permanent claim that a participant is verified. High-impact actions require current identity assurance and permission checks appropriate to the action.

Communication consent, channel preferences, restrictions, and revocations are consulted at the time of delivery. A historical conversation association does not override a later opt-out or privacy restriction.

## Classification and Data Minimization

Conversation metadata, context snapshots, and linkage records follow classification and retention policy. The platform stores references instead of duplicating restricted transcripts, attachments, prompts, credentials, payment data, health data, or private model reasoning.

## Context Access Matrix

The authoritative Security, Permission, and Tenant Isolation models define final policy. This matrix establishes the default Session Management boundary.

| Consumer | Conversation metadata | Context snapshot | Transcript / attachment reference | State mutation |
|---|---|---|---|---|
| Channel adapter | Only its mapped thread and delivery metadata | No | No, except authorized channel-delivery reference | May request mapping updates; cannot write directly |
| Agent Runtime | Only for the authorized execution | Only its immutable authorized snapshot | Reference only when separately authorized | May request approved changes with expected version |
| Workflow service | Correlation and approved workflow context | No, unless explicitly authorized | Reference only when separately authorized | May request approved lifecycle/work-item updates |
| Tool service | Minimum correlation reference | No | No, unless separately authorized by Tool System | No direct mutation |
| Human operator | Role-, tenant-, and classification-scoped | Only when the handoff grants it | Only when policy permits | Through approved operator workflow |
| Operations/support | Restricted diagnostic metadata | No by default | No by default | Only controlled recovery operations with audit |

All access is tenant-scoped, purpose-limited, logged, and subject to current authorization; a reference is not itself permission to retrieve the underlying content.

---

# Reliability, Recovery, and Retention

## Durable State Changes

Lifecycle changes, cross-channel links, handoffs, and session completion are durably recorded before dependent events are acknowledged. Where an event represents a persisted change, the platform uses a transactional outbox or equivalent reliable publication pattern.

## Recovery

After a worker restart or transient failure, the platform recovers only durable session state and re-evaluates current authorization before continuing. In-memory model context is not treated as durable session truth.

## Replay

Replaying a session-related event is an operationally controlled action. Operators must verify tenant scope, policy changes, idempotency, lifecycle state, and external side-effect risk. Replay cannot bypass current permission, consent, or delivery controls.

## Retention and Deletion

Retention follows approved tenant agreements, classification, legal obligations, operational recovery needs, and privacy policy. Deletion or anonymization must preserve only the minimum audit evidence legally and operationally required, while removing or irreversibly de-identifying data according to policy.

---

# Observability and Audit

The platform must trace each resolution decision and state transition without exposing unnecessary content.

Required telemetry and audit records include:

- Conversation, session, tenant, participant, and channel-thread references.
- Correlation, causation, and trace identifiers.
- Resolution outcome, candidate-selection basis, identity assurance, and consent decision.
- Lifecycle transitions, expected and resulting version, and actor or system identity.
- Context snapshot, authorization, agent execution, workflow, tool, handoff, and delivery references.
- Expiry, retry, concurrency conflict, recovery, and replay outcomes.

Metrics include active conversations, session duration, resolution success, ambiguous-link rate, verification rate, handoff rate, concurrency conflicts, expiry, recovery success, and cross-channel continuation success.

---

# Testing Strategy

## Contract Tests

Contract tests verify canonical record schemas, lifecycle transitions, state-update validation, context-snapshot references, and event publication against registered contracts.

## Integration Tests

Integration tests verify tenant-scoped resolution, channel mapping, cross-channel consent, session creation, runtime context assembly, workflow/tool correlation, human handoff, and delivery boundaries.

## Security Tests

Security tests verify session identifier protection, fixation and replay resistance, identity-assurance rules, cross-tenant isolation, restricted-context handling, consent revocation, and unauthorized conversation linking.

## Resilience Tests

Resilience tests simulate duplicate interactions, delayed callbacks, out-of-order events, concurrent messages, worker restart, session expiry, failed handoff, and controlled replay. They must demonstrate that sessions remain consistent and that externally visible actions are not duplicated.

---

# Anti-Patterns

## Provider Thread as Canonical Conversation

Treating a messaging thread, call ID, or email chain as the authoritative conversation creates vendor coupling and weakens cross-channel security. Use it only as a governed channel-thread mapping.

## Long-Lived Runtime State

Keeping conversation truth inside a runtime worker or model context loses recoverability and causes inconsistent behavior across retries and scaling. Persist canonical lifecycle and metadata separately from execution state.

## Automatic Identity Linking by Contact Detail

Linking conversations solely because an address or phone number matches can disclose sensitive context to the wrong person. Use evidence, assurance, purpose, and tenant policy.

## Session as Authorization Grant

An existing conversation or session does not authorize any new sensitive action. Every action continues to require current permission, identity, consent, and policy checks.

## Last-Write-Wins Conversation Updates

Concurrent updates without version checks can overwrite handoffs, lifecycle transitions, or verification state. Use explicit concurrency control and resolution rules.

---

# Architecture Boundaries

| Document | Relationship |
|---|---|
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Creates and consumes bounded execution sessions; runtime workers do not own canonical continuity state. |
| `08_AGENT_EXECUTION_ENGINE.md` | Uses authorized context snapshots for reasoning and records execution outcome against a session. |
| `10_AGENT_STATE_MANAGEMENT.md` | Defines broader Agent Runtime state patterns; Conversation Platform owns canonical conversation/session continuity state. |
| `11_AGENT_CONTEXT_MODEL.md` | Defines the composition and use of the bounded context snapshot. |
| `18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Memory-owned durable-memory contracts separately from conversation/session metadata. |
| `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Integration-owned workflow contracts linked to sessions for correlation only. |
| `21_AGENT_EVENT_INTEGRATION.md` | Governs session lifecycle events, subscriptions, delivery, and replay. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Maps channel interactions and threads to canonical conversations through controlled resolution. |
| `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent consumption of Security-owned controls applied to session resolution and state access. |
| `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent use of Security-owned authorization for context access, linking, and action. |
| `26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent use of Security-owned tenant-boundary controls for session processing. |

---

# Final Summary

Conversation Platform provides the durable, secure, and channel-independent continuity layer. Agent Platform receives bounded authorized execution work, keeps transient runtime state separate, and reports outcomes through controlled Conversation Platform contracts.

By keeping state minimal, referenced, versioned, tenant-scoped, and auditable, the platform can scale across channels and runtime workers while preserving user trust and controlled agent behavior.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Session Management architecture document. |
| 2.1 | 2026-08-05 | Added contract governance, lifecycle-transition rules, session-resolution decisions, persistence and conflict rules, and a context-access matrix. |
| 3.0 | 2026-08-06 | Re-scoped this document to Agent execution-session integration; Conversation Platform owns canonical conversation/session state and continuity. |
| 3.1 | 2026-08-08 | Approved after Digital Channel, Observability, Testing, Conversation, Security, and Integration boundary review; replaced deprecated boundary references. |
