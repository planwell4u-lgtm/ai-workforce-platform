# 01_CONVERSATION_ARCHITECTURE

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines the architecture of the Conversation Platform: the unified interaction-management layer between users, channels, and the Agent Platform.

The Conversation Platform owns the canonical conversation experience across voice, web chat, messaging, email, API, and future channels. It creates and maintains conversations, coordinates sessions and participants, manages conversation state and context availability, routes interactions to eligible agents or humans, and preserves continuity as users move across approved channels.

---

# Purpose

The purpose of the Conversation Architecture is to ensure that users experience one coherent conversation while the underlying communication channel, agent version, provider, workflow, or human participant may change.

It applies the One Brain, Multi-Channel principle by separating conversation management from channel transport and agent intelligence. Channels deliver interactions; the Conversation Platform gives them a durable, tenant-safe conversation context; the Agent Platform reasons and acts within approved boundaries.

---

# Objectives

The Conversation Architecture must:

- Provide a canonical, channel-independent model for conversations, participants, interactions, sessions, state, and handoff.
- Preserve safe continuity when a user changes channel, a human joins, an agent version changes, or work is deferred.
- Route validated interactions to eligible agents, workflows, queues, or human operators without taking ownership of agent reasoning.
- Supply bounded, authorized conversation context to Agent Platform execution.
- Preserve tenant isolation, identity assurance, consent, classification, authorization, audit, and retention requirements.
- Support synchronous, asynchronous, event-driven, and multi-participant interactions.
- Remain resilient to duplicate, delayed, out-of-order, and failed channel/provider events.
- Expose stable contracts so channels, agents, workflows, tools, and operators can evolve independently.

---

# Scope

This document defines:

- Conversation Platform responsibilities, components, data ownership, and boundaries.
- The high-level flow for interaction ingress, resolution, routing, context, execution, delivery, and handoff.
- Conversation architecture principles for multi-channel continuity, state, security, tenant isolation, reliability, observability, and governance.
- The document sequence and implementation artifacts required for detailed Conversation Platform design.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent purpose, reasoning, instructions, capability selection, tool selection, and model behavior | 02_AGENT_PLATFORM |
| Voice/media transport, telephony, SIP, WebRTC, STT, TTS, and call-provider behavior | 04_VOICE_PLATFORM |
| Channel-client protocol adapters, provider credentials, and delivery implementation | Relevant Channel Platform |
| Knowledge ingestion, retrieval implementation, and document governance | 05_KNOWLEDGE_PLATFORM |
| Customer memory storage, preferences, profiles, and memory lifecycle | 06_MEMORY_PLATFORM |
| External connector, tool, MCP, webhook, API, and workflow-engine implementation | 07_INTEGRATION_PLATFORM |
| Data storage technology, backup, migrations, retention engine, and analytical infrastructure | 08_DATA_PLATFORM |
| Enterprise identity, authorization infrastructure, secrets, and compliance controls | 09_SECURITY_PLATFORM |
| Infrastructure, CI/CD, environment hosting, telemetry infrastructure, or operations process | Deployment, Observability, and Operations Platforms |

---

# Architecture Principles

## Conversation Is a Platform Capability

A conversation is not a provider thread, browser session, call ID, model prompt, agent memory record, or runtime-worker state. It is a canonical tenant-scoped interaction record owned by the Conversation Platform.

## Channels Transport; Conversations Persist

Voice, chat, messaging, email, and API channels map their native interactions to a governed conversation contract. A channel thread may be associated with a conversation after validation and authorization, but no channel becomes the source of truth for conversation state.

## Agent Platform Reasons; Conversation Platform Coordinates

The Conversation Platform determines the interaction’s conversation, state, routing eligibility, participant context, and handoff path. The Agent Platform determines reasoning, capability selection, and proposed action under current permission and policy controls.

## Context Is Bounded and Authorized

The Conversation Platform makes the minimum relevant interaction history, state, participant, and channel context available through a bounded reference or snapshot. It does not grant unrestricted transcript, memory, knowledge, or data access.

## Continuity Is Explicit

Channel switching, agent reassignment, human handoff, deferred work, and conversation reopening are recorded controlled transitions. A matching contact detail, session identifier, or provider thread does not silently establish continuity for sensitive work.

## Tenant and Purpose First

Every conversation, interaction, participant association, channel mapping, routing decision, context reference, handoff, and operational action is tenant-scoped and purpose-bound. Missing or conflicting tenant context fails closed.

## Events Record Facts

Conversation events describe observed facts such as interaction received, conversation created, participant verified, agent assigned, handoff requested, or conversation closed. They do not directly authorize reasoning, delivery, tool actions, or workflow changes.

---

# High-Level Architecture

~~~text
User or External System
    |
    v
Voice / Chat / Messaging / Email / API Channel
    |
    v
Channel Adapter and Interaction Validation
    |
    v
Conversation Ingress and Resolution
    |
    +--> Create or Resolve Conversation
    +--> Resolve Participant and Session
    +--> Apply Tenant, Identity, Consent, and Policy Checks
    |
    v
Conversation State, Context, and Routing
    |
    +--> Agent Execution Request
    +--> Human Queue or Handoff
    +--> Approved Workflow Request
    +--> Safe Defer or Fallback
    |
    v
Agent Platform / Human / Workflow Outcome
    |
    v
Conversation Update and Authorized Delivery Request
    |
    v
Channel Adapter and Participant
~~~

---

# Core Components

## Interaction Gateway

The Interaction Gateway receives normalized, validated interactions from channel adapters or approved external sources. It verifies tenant/provider binding, message integrity, idempotency, classification, identity evidence, consent context, and correlation before requesting conversation resolution.

The gateway does not perform agent reasoning, execute tools, store raw channel-specific business state, or bypass channel/provider security controls.

## Conversation Resolver

The Conversation Resolver creates a new conversation or identifies an eligible existing one. It evaluates tenant, participant evidence, channel-thread mapping, purpose, classification, lifecycle, continuity policy, and current authorization.

Ambiguous or insufficient evidence routes to verification, safe restricted handling, or human review; it does not silently choose a conversation.

## Conversation State Service

The Conversation State Service owns canonical conversation lifecycle, participants, interaction references, channel mappings, routing state, handoff state, context references, and durable transition history. It uses concurrency control and immutable event/history references to protect state integrity.

## Context Service

The Context Service assembles or references the bounded conversation context permitted for a particular agent execution, workflow interaction, human handoff, or delivery decision. It applies tenant, participant, classification, purpose, authorization, and lifecycle rules.

## Routing Service

The Routing Service determines the eligible destination for an interaction based on conversation state, tenant configuration, participant/identity state, channel capabilities, queue/handoff policy, agent assignment eligibility, and current operational conditions.

Routing may select an eligible agent or queue, but it does not determine the agent’s reasoning or override agent, permission, workflow, or tool controls.

## Handoff and Collaboration Service

The Handoff and Collaboration Service coordinates assignment, queueing, participant notification, authorized context transfer, agent/human ownership, return-to-agent behavior, and outcome recording. It does not grant the human unrestricted access to conversation history or tenant data.

## Conversation Event Publisher

The Event Publisher emits governed conversation facts after durable state changes. It supports authorized consumers such as the Agent Platform, channels, workflows, analytics, and operations without exposing raw provider payloads as trusted events.

---

# Canonical Conversation Model

~~~text
Conversation
    |
    +-- tenant and organization scope
    +-- purpose, classification, lifecycle, and retention references
    +-- participant associations and identity-assurance references
    +-- channel-thread mappings and interaction references
    +-- routing, handoff, and ownership state
    +-- authorized context references
    +-- agent, workflow, and delivery correlation references
    +-- version, audit, correlation, and trace metadata
~~~

The canonical model stores minimal state and references. Full transcripts, recordings, attachments, knowledge documents, memory records, tool payloads, workflow state, credentials, and private model reasoning remain in their authoritative systems.

## Participant and Multi-Party Model

A participant is a tenant-scoped user, customer, agent, human operator, group/shared endpoint, or authorized external system associated with a conversation for a defined role and purpose. Participant records reference identity evidence, relationship, channel address, assurance, consent, classification, and access boundaries; a channel address alone is not a verified participant.

Multi-party conversations record participant roles, visibility, ownership, turn/assignment state, and authorized context scope. Adding, removing, or revealing a participant is a controlled transition. A participant must not receive another participant’s restricted context merely because they share a conversation or channel.

## Canonical Identifier Policy

Conversation Platform owns stable identifiers for conversation, interaction, participant association, channel-thread mapping, session coordination, routing decision, handoff, and context snapshot reference. Identifiers are globally unique, immutable, tenant-scoped in use, and safe to correlate only through authorized services.

Channel/provider identifiers are stored as governed mappings. Correlation, causation, and trace identifiers link processing but are not authorization credentials or substitutes for a canonical conversation identifier.

## Retention and Residency Reference

The Conversation Platform classifies conversation records and provides retention, archival, deletion, legal-hold, and residency references to the Data and Security Platforms. It does not independently define storage implementation or retention law.

Conversation closure, archival, export, deletion, and restoration use the current tenant, classification, authorization, and data-lifecycle policy. Historical identifiers and audit references are minimized or retained only as required by approved policy.

---

# Interaction and Execution Flow

## Inbound Interaction

1. A channel adapter authenticates, validates, and normalizes a channel-native interaction.
2. The Interaction Gateway validates tenant binding, integrity, idempotency, classification, consent, and correlation.
3. The Conversation Resolver creates or resolves the conversation and participant association under current policy.
4. The Conversation State Service records the accepted interaction and state transition durably.
5. The Routing Service identifies the next eligible destination.
6. The Conversation Platform issues a bounded, authorized request to the Agent Platform, human queue, or approved workflow boundary.

## Agent Outcome

1. The Agent Platform resolves an eligible agent version and executes under current authorization.
2. The outcome may be an approved response, work request, handoff, deferment, workflow/tool result, or safe refusal.
3. The Conversation Platform records the resulting conversation state and delivery/handoff disposition.
4. An authorized delivery request is sent to the relevant channel boundary.
5. Delivery and participant outcomes are recorded as governed conversation facts.

## Routing Decision Hierarchy

Routing applies the following precedence before selecting an eligible destination:

1. Tenant, environment, legal, classification, and security restrictions.
2. Participant identity assurance, consent, relationship, and conversation lifecycle state.
3. Channel capability, delivery eligibility, and current provider/operational condition.
4. Required human review, approval, safety, or incident restriction.
5. Eligible agent, queue, workflow boundary, assignment, and capacity policy.
6. Approved fallback, deferment, or safe refusal when no eligible destination remains.

Routing records the applied policy, selected destination, alternatives considered where required, reason, expiry, and correlation evidence. It never bypasses the destination’s own authorization or execution checks.

---

# Platform Boundaries

## Agent Platform

Conversation Platform provides authorized interaction, state, context, routing, and handoff references. Agent Platform provides approved reasoning, capability selection, execution outcome, and controlled action requests.

Neither platform directly owns the other’s state. Conversation routing does not grant an agent permission; agent outcome does not grant delivery permission or mutate conversation state directly.

## Channel and Voice Platforms

Channels and Voice Platform own transport protocols, provider integration, media, and channel-specific delivery constraints. Conversation Platform owns the normalized interaction relationship, canonical continuity, and channel-thread mapping after validation.

## Knowledge and Memory Platforms

Conversation Platform references authorized knowledge and memory only through owned interfaces. It does not store organizational knowledge as conversation state or turn conversation history into ungoverned long-term memory.

## Integration and Workflow Boundaries

Conversation Platform may route an interaction to an approved workflow boundary or record a workflow correlation reference. Integration Platform owns connector and workflow implementation; agent and workflow authorization remain separate from conversation routing.

## Security, Data, and Operations Boundaries

Security Platform provides identity, authorization, secrets, and compliance controls. Data Platform provides durable storage and lifecycle mechanisms. Operations, Deployment, Observability, and Testing Platforms provide shared production capabilities. Conversation Platform supplies its own contracts, context, state, and domain evidence to those platforms.

---

# Security, Privacy, and Tenant Controls

All conversation records and operations are tenant-scoped. The platform verifies identity evidence, participant relationship, purpose, classification, consent, and current authorization before resolving, linking, retrieving, routing, handing off, or delivering an interaction.

Channel identifiers are evidence, not automatic account identity. Cross-channel association requires approved continuity rules and may require step-up verification. Human operators receive only the minimum authorized context for their role and purpose.

Conversation data is minimized, classified, encrypted, retained, exported, deleted, and audited according to Security and Data Platform policy. The Conversation Platform does not log secrets, raw restricted content, hidden instructions, or private model reasoning in general operational telemetry.

---

# Reliability and Failure Handling

The platform assumes duplicate, delayed, unordered, malformed, and failed interactions. It uses stable identifiers, idempotency, concurrency control, bounded retry, durable transition recording, dead-letter/quarantine paths, reconciliation, safe fallback, and human handoff.

A failure never causes a cross-tenant association, hidden context exposure, duplicate delivery, duplicate external action, automatic less-secure-channel fallback, or a false claim that an action completed.

## Concurrent and Conflicting Updates

The platform expects simultaneous messages, channel callbacks, agent outcomes, handoff changes, and workflow updates. Canonical state transitions use an expected version or equivalent concurrency control. Conflicts are resolved through current lifecycle, participant, routing, and policy rules rather than last-write-wins behavior.

When channel updates disagree or arrive out of order, the platform records source sequence/time evidence, preserves the conflict, and reconciles through the authoritative channel/provider contract, durable state, or authorized review. It does not overwrite a newer controlled transition with a delayed callback.

Detailed conversation failure behavior is defined in the Conversation Lifecycle, Session, State, Events, Handoff, Security, Observability, and Testing documents.

---

# Contract Governance

The normalized interaction, conversation, participant, context, routing, handoff, and event contracts are versioned public interfaces. Their executable schemas define required fields, identifier formats, compatibility, error categories, deprecation, and migration behavior.

Additive compatible change is preferred. Removing a field, changing its meaning/type, changing authorization semantics, or requiring new context creates a new contract version and documented consumer migration. Agent, Channel, Voice, Integration, Security, and Data Platform implementations consume approved contract versions rather than private copies.

---

# Agent Platform Alignment Requirement

Conversation Platform is the canonical owner of conversation lifecycle, session coordination, context availability, multi-channel conversation abstraction, routing, and human-handoff coordination.

The documents 22_AGENT_MULTI_CHANNEL_MODEL and 23_AGENT_SESSION_MANAGEMENT in 02_AGENT_PLATFORM describe the Agent Platform integration boundary only. Before either module is approved, their ownership language, architecture-boundary tables, and future implementation contracts must be aligned to this document and the detailed Conversation Platform documents. They must not create a competing canonical session, conversation, routing, or handoff model.

---

# Observability and Audit

Every material conversation operation is correlated with tenant, conversation, interaction, participant, channel, session, routing, agent/version, workflow, handoff, delivery, authorization, event, correlation, and trace references where applicable.

The platform emits health, latency, routing, handoff, delivery, duplicate, policy-denial, continuity, and failure signals. Observability infrastructure is owned externally; Conversation Platform defines the domain semantics and protected evidence required for diagnostics and audit.

---

# Detailed Document Sequence

| Document | Focus |
|---|---|
| 02_CONVERSATION_LIFECYCLE.md | Lifecycle states, transitions, expiry, closure, reopening, and retention |
| 03_CONVERSATION_MODEL.md | Canonical data model, participants, interactions, channel mappings, and ownership |
| 04_CONVERSATION_SESSION_MODEL.md | Session coordination, continuity, execution association, and recovery |
| 05_CONVERSATION_CONTEXT_MODEL.md | Context assembly, snapshots, access, minimization, and lifecycle |
| 06_CONVERSATION_ROUTING.md | Agent/queue/workflow routing, eligibility, assignment, and fallback |
| 07_CONVERSATION_EVENTS.md | Event contracts, publication, subscription, replay, and observability |
| 08_CONVERSATION_HANDOFF_MODEL.md | Human/agent collaboration, queueing, transfer, and return behavior |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Concurrency, consistency, state update, recovery, and retention patterns |
| 10_CONVERSATION_SECURITY.md | Identity, tenant, consent, classification, access, and privacy controls |
| 11_CONVERSATION_OBSERVABILITY.md | Conversation telemetry, health, audit, diagnostics, and SLOs |
| 12_CONVERSATION_TESTING.md | Contract, integration, security, resilience, channel, and production tests |

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Normalized interaction contract | Defines inbound/outbound interaction, identity, tenant, channel, classification, and correlation fields | Conversation Platform with Channel owners |
| Conversation and participant schema | Defines canonical records, lifecycle, mappings, ownership, and versioning | Conversation Platform with Data Platform |
| Identifier and relationship standard | Defines canonical identifiers, mappings, participant roles, visibility, assurance, and correlation use | Conversation Platform with Security owner |
| Routing and handoff policy | Defines eligible destinations, assignment, escalation, fallback, and ownership | Conversation Platform with Agent and Operations owners |
| Routing decision hierarchy | Defines policy precedence, destination eligibility, reason, conflict, and fallback behavior | Conversation Platform with Agent, Security, and Operations owners |
| Context access contract | Defines bounded context references, authorization, classification, and snapshot behavior | Conversation Platform with Agent and Security owners |
| Conversation event registry | Defines facts, schemas, producers, consumers, retention, and replay controls | Conversation Platform with Integration owner |
| Contract-versioning and migration policy | Defines compatibility, schema, deprecation, migration, and consumer support rules | Conversation Platform with dependent owners |
| Conversation security and tenant matrix | Defines identity, consent, tenant, classification, and access controls | Conversation Platform with Security owner |
| Concurrency and reconciliation policy | Defines state versions, conflict handling, sequencing, authoritative source, and review paths | Conversation Platform with Data, Channel, and Integration owners |
| Retention and residency reference map | Defines classification, lifecycle, data-policy link, archive, deletion, export, and restoration references | Conversation Platform with Data and Security owners |
| Conversation SLI/SLO catalog | Defines reliability, latency, routing, handoff, delivery, and continuity measures | Conversation, Operations, and Observability owners |
| Conversation test plan | Defines contract, integration, security, resilience, channel, and release evidence | Conversation Platform with Testing owner |

---

# Anti-Patterns

## Channel Thread as the Conversation

A provider thread, call ID, browser session, or email chain is not canonical conversation state. It is only a governed mapping to a conversation after validation.

## Conversation Platform as Agent Brain

Embedding prompts, reasoning, tool selection, or model behavior in routing or context services duplicates agent intelligence and violates ownership boundaries.

## Context as Unrestricted History

Sending full conversation history, raw attachments, private data, or hidden instructions to every execution creates privacy, cost, and injection risk. Context is bounded and authorized.

## Routing as Authorization

Selecting an agent, queue, or workflow destination does not authorize data access, tool use, external action, or delivery. Each action uses its own current policy decision.

## Silent Cross-Channel Linking

Linking voice, chat, email, or messaging activity solely because a contact detail matches can disclose sensitive context. Continuity requires verified policy conditions.

## Direct Cross-Platform Database Access

Channels, agents, tools, workflows, and analytics must use APIs, events, or contracts rather than direct access to Conversation Platform internal state.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/PROJECT_CONTEXT.md | Defines platform vision and high-level Conversation Platform responsibility. |
| 00_CONTROL/ARCHITECTURE_PRINCIPLES.md | Defines One Brain, Multi-Channel, modularity, contract-first, and tenant-first principles. |
| 02_AGENT_PLATFORM/README.md | Defines Agent Platform ownership and the integration boundary. |
| 02_AGENT_PLATFORM/07_AGENT_RUNTIME_ARCHITECTURE.md | Receives authorized conversation-triggered execution. |
| 02_AGENT_PLATFORM/11_AGENT_CONTEXT_MODEL.md | Consumes bounded context through the Conversation Platform contract. |
| 02_AGENT_PLATFORM/21_AGENT_EVENT_INTEGRATION.md | Governs event transport and cross-platform event controls. |
| 02_AGENT_PLATFORM/22_AGENT_MULTI_CHANNEL_MODEL.md | Defines the Agent Platform’s channel-integration boundary. |
| 02_AGENT_PLATFORM/23_AGENT_SESSION_MANAGEMENT.md | Defines the Agent Platform’s session-integration boundary; canonical conversation/session ownership belongs here. |
| 02_AGENT_PLATFORM/24_AGENT_SECURITY_MODEL.md | Defines agent-specific zero-trust security controls. |
| 02_AGENT_PLATFORM/26_AGENT_TENANT_ISOLATION.md | Defines agent-specific tenant-context requirements. |
| 04_VOICE_PLATFORM | Owns voice and telephony interaction transport. |
| 05_KNOWLEDGE_PLATFORM | Owns knowledge retrieval and governance. |
| 06_MEMORY_PLATFORM | Owns durable memory and profile lifecycle. |
| 07_INTEGRATION_PLATFORM | Owns external connectors, tools, and workflow implementation. |
| 08_DATA_PLATFORM | Owns data storage, lifecycle, backup, and analytical infrastructure. |
| 09_SECURITY_PLATFORM | Owns enterprise identity, authorization, privacy, and compliance controls. |
| 13_OBSERVABILITY_PLATFORM | Owns telemetry infrastructure, dashboards, and alerting. |
| 14_TESTING_PLATFORM | Owns shared testing infrastructure and standards. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Architecture document. |
| 2.1 | 2026-08-05 | Added participant/identifier model, routing precedence, reconciliation, contract governance, retention, alignment, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |
