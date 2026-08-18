# 22_AGENT_MULTI_CHANNEL_MODEL

**Version:** 3.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Purpose

This document defines how the Agent Platform provides one coherent agent experience across voice, web chat, WhatsApp, email, API, and future channels without duplicating agent intelligence or embedding channel-specific business logic in the core platform.

The model implements the **One Brain, Multi-Channel** architecture: channels are delivery and interaction surfaces; the Agent Platform remains the authoritative owner of agent identity, instructions, capabilities, agent-side policy evaluation, execution, memory access, and workflow coordination.

Conversation Platform owns canonical conversations, normalized interactions, session continuity, participant/channel associations, routing, handoff, and conversation delivery disposition. This document defines how Agent Platform consumes those approved contracts without creating competing channel or conversation state.

---

# Objectives

The Multi-Channel Model must:

- Provide a consistent agent identity and policy posture across supported channels.
- Normalize inbound interactions into a channel-independent platform contract.
- Select the most suitable response representation for each channel without changing business intent.
- Preserve tenant isolation, user identity, consent, authorization, and auditability end-to-end.
- Support channel-specific capabilities without allowing them to bypass platform controls.
- Maintain a coherent conversation and handoff experience when users move between channels.
- Allow channels and providers to evolve independently from agent reasoning and workflows.
- Degrade safely when a channel is unavailable or cannot support a requested interaction.

---

# Scope

This document defines:

- Channel responsibilities and ownership boundaries.
- The normalized interaction model for inbound and outbound communication.
- Channel selection, response adaptation, and capability negotiation.
- Cross-channel conversation continuity and human handoff principles.
- Channel identity, consent, security, privacy, observability, and failure-handling requirements.
- The relationship between channels, the Agent Runtime, Event Integration, workflows, tools, and sessions.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent reasoning, planning, and response generation | `08_AGENT_EXECUTION_ENGINE.md` |
| Runtime execution, scheduling, and worker lifecycle | `07_AGENT_RUNTIME_ARCHITECTURE.md` |
| Canonical conversation, interaction, and session state | `03_CONVERSATION_PLATFORM` |
| Event contracts, broker delivery, and subscriptions | `21_AGENT_EVENT_INTEGRATION.md` |
| Voice recognition, synthesis, or telephony protocols | Voice Platform |
| Digital channel-provider protocol implementation, delivery receipts, and channel-native credentials | Digital Channel Platform; Integration Platform owns reusable connector and delegated-credential controls |
| Workflow definitions and business-process state | `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` |
| Tool authorization and external action execution | `15_AGENT_TOOL_SYSTEM.md` and `16_AGENT_TOOL_EXECUTION_MODEL.md` |
| Enterprise-wide authentication, authorization, and privacy policy | Security Platform |

---

# Architecture Principles

## One Brain, Multiple Surfaces

An agent's identity, instructions, permissions, knowledge access, memory policy, and capabilities are centrally governed. A channel changes how an interaction is received or delivered, not which agent is allowed to act or what policy applies.

## Channels Are Adapters, Not Agent Implementations

Each channel adapter translates between a provider protocol and the normalized platform interaction contract. It must not independently perform agent reasoning, retain authoritative conversation state, or execute business actions outside approved platform paths.

## Normalize Before Reasoning

Inbound channel data is untrusted until it has been authenticated, validated, classified, tenant-scoped, and normalized. The Agent Runtime receives approved interaction context, never raw provider payloads as instructions.

## Preserve Intent; Adapt Presentation

The platform may adapt wording, format, media, length, timing, and interaction controls for a channel. It must preserve the approved business intent, user-facing truthfulness, policy requirements, and audit trail.

## Channel Capability Does Not Create Permission

A channel's ability to place a call, send a template, upload a file, or expose a button does not authorize that action. All actions remain subject to tenant policy, user consent, workflow rules, tool authorization, and channel-specific restrictions.

## Explicit Handoff and Continuity

Moving an interaction between channels or to a human must be deliberate, authorized, and visible in the conversation record. The platform must not silently expose restricted context to a new channel or recipient.

---

# Channel Architecture

```text
Voice Adapter ------------------------------------+
Digital Channel adapters (web, messaging, email, API, future)
                                                   |
                                                   v
                                  Conversation Platform normalizes, associates,
                                  routes, and owns continuity
                                                   |
                                                   v
                                        Authorized Agent execution work
                                                   |
                                                   +--> Agent Runtime
                                                   +--> Workflow and Tool Systems
                                                   +--> Event Integration
```

## Channel Adapter Responsibilities

A Digital Channel adapter is responsible for:

- Authenticating and verifying its provider or client connection.
- Receiving and delivering channel-native messages and interaction controls.
- Validating provider signatures, message identifiers, timestamps, and replay protections.
- Mapping channel-native data to or from the normalized interaction contract.
- Reporting delivery status, channel capability, and provider errors.
- Enforcing provider constraints such as size limits, message windows, templates, and rate limits.

An adapter does not own agent policy, user authorization, durable session state, workflow state, or external business actions.

## Conversation Ingress Responsibilities

Conversation Platform consumes the validated Digital Channel interaction contract. It:

- Resolves canonical participant, conversation, session, routing, and continuity state.
- Applies Conversation-owned routing and work-ownership decisions.
- Produces authorized Agent execution work or delivery intent through approved contracts.

Digital Channel validates provider/client traffic, applies channel-specific consent and delivery controls, and records channel delivery evidence. It does not resolve or mutate canonical Conversation state.

---

# Normalized Interaction Model

Every inbound and outbound interaction is represented with a common envelope and a typed content body.

```text
Interaction Envelope
|
+-- interactionId
+-- direction                 (inbound | outbound)
+-- channel                   (voice | chat | whatsapp | email | api | ...)
+-- occurredAt
+-- tenantId
+-- organizationId            (when applicable)
+-- conversationId
+-- sessionId                 (when applicable)
+-- participant
+-- actorContext              (when authenticated)
+-- channelMessageId
+-- correlationId
+-- causationId
+-- traceId
+-- classification
+-- consentContext
+-- capabilities
+-- content
```

## Content Types

The normalized content model supports typed, bounded content rather than arbitrary provider payloads:

- Text and structured text.
- Voice transcript and speech-delivery directives.
- Attachments and authorized content references.
- Images, files, cards, buttons, forms, and approved interactive controls.
- Delivery receipts, typing indicators, call-state changes, and handoff signals.

Raw provider payloads may be retained only where authorized for troubleshooting or audit. They are not part of the general agent context.

## Channel Capability Profile

Each interaction carries a capability profile describing what the channel can safely support, for example:

- Synchronous or asynchronous delivery.
- Text, speech, attachments, buttons, forms, and rich cards.
- Maximum message and attachment sizes.
- Confirmation, read-receipt, and delivery-status support.
- User authentication strength and verified identity level.
- Provider-required consent, template, or messaging-window constraints.

The Runtime uses this profile to select a permitted response representation. It must not assume that a capability available in one channel exists in another.

---

# Interaction Contract Governance

The normalized interaction envelope is a versioned public platform contract. Its conceptual shape in this document must be implemented as a machine-readable schema, such as JSON Schema, OpenAPI, Protobuf, or an equivalent platform standard.

## Contract Requirements

The executable contract must define:

- Field types, formats, cardinality, required and optional fields, and default behavior.
- Permitted content types, attachment-reference rules, size limits, and classification metadata.
- Enumerations for direction, channel, interaction state, identity assurance, delivery disposition, and handoff state.
- Schema version, compatibility policy, validation errors, and deprecation process.
- Stable identifiers and idempotency keys for inbound messages, delivery requests, and provider callbacks.

Additive, backward-compatible changes are preferred. Removing a field, changing its meaning or type, or introducing a new required field requires a new contract version and a documented migration period.

## Agent Integration Contract Boundary

Conversation Platform owns the normalized interaction contract and canonical delivery disposition. Channel/Voice/Integration capabilities own provider-protocol mapping and transport behavior. Agent Platform consumes the approved interaction and delivery contracts to select and execute eligible agent behavior.

Provider-specific fields remain in bounded adapter extensions and must not become hidden dependencies of Agent Runtime, workflow, or tool systems.

---

# Channel Capability Matrix

The channel owner maintains a versioned capability matrix for every supported channel and provider configuration. Conversation Platform uses it for routing/delivery constraints; Agent Platform uses the approved capabilities for response adaptation. It is not an Agent Platform source of truth for channel continuity or delivery authorization.

At minimum, each matrix entry records:

| Capability area | Required decision |
|---|---|
| Supported content | Text, speech, attachments, rich controls, forms, links, and maximum sizes |
| Interaction behavior | Synchronous/asynchronous delivery, ordering, read receipts, and delivery confirmation |
| Identity | Available identity evidence, authentication strength, and step-up support |
| Consent and policy | Opt-in, opt-out, templates, message windows, quiet hours, and regional restrictions |
| Security | Classification limits, encryption, malware scanning, logging, and retention constraints |
| Reliability | Idempotency source, callback behavior, retry model, rate limits, and fallback eligibility |
| Operations | Provider owner, credentials, monitoring, incident runbook, and service-level expectations |

A new channel cannot be enabled in production until its capability-matrix entry, adapter contract tests, security review, and operational owner are approved.

---

# Inbound Interaction Flow

```text
Channel Provider / Client
    |
    v
Channel Adapter
    |
    v
Authentication, Validation, and Normalization
    |
    v
Conversation Platform canonical ingress and routing
    |
    +--> Rejected / Quarantined
    |
    v
Conversation session association and policy checks
    |
    v
Authorized Agent or Workflow Trigger
```

## Ingress Validation

Before an inbound interaction can influence an agent execution, the platform must validate:

- Adapter and provider authenticity.
- Tenant and channel binding.
- Message freshness, uniqueness, and replay protection.
- Participant identity evidence and consent context.
- Content size, type, malware scanning, and classification requirements.
- Supported channel capability and applicable provider policy.

Untrusted content remains data. It cannot override approved instructions, safety rules, permissions, or identity requirements.

## Identity Resolution

Channel addresses such as a phone number, email address, provider user ID, or browser session are identifiers, not automatically verified identities. The platform resolves them to a participant record only under the applicable tenant policy and records the confidence or assurance level.

Actions involving sensitive information, account changes, payments, or regulated data require the authentication and step-up verification defined by security policy, regardless of channel.

---

# Outbound Response and Delivery Model

```text
Agent or Workflow Outcome
    |
    v
Response Policy and Channel Adaptation
    |
    v
Delivery Authorization
    |
    v
Channel Adapter
    |
    v
Provider / Client
    |
    v
Delivery Status Event
```

## Response Adaptation

Response adaptation translates an approved outcome into a usable channel representation. Examples include converting a long explanation into a concise voice prompt, rendering a choice as approved buttons, or offering a secure web link when email cannot safely carry the content.

Adaptation may not change commitments, invent information, omit required disclosures, or turn an internal action into a user-visible claim before its outcome is confirmed.

## Delivery Authorization

Before delivery, the platform validates the recipient, tenant scope, channel consent, quiet-hour rules, message classification, template or provider requirements, and any workflow approval conditions.

Outbound delivery is an authorized communication action. A completed agent execution alone is not proof that a message may be sent.

## Delivery Outcomes

Delivery status is recorded as a normalized fact, such as `interaction.delivered`, `interaction.delivery_failed`, or `interaction.read` where supported. A delivery receipt does not necessarily prove that a user understood or accepted the message.

## Durable Outbound Delivery State

The platform persists a channel-independent delivery record for every authorized outbound communication. The record is separate from the agent response or workflow outcome, allowing delivery to be retried and reconciled safely.

```text
Requested
    -> Authorized
    -> Submitted to Provider
    -> Accepted by Provider
    -> Delivered / Read (when supported)
    -> Failed / Expired / Cancelled
```

Each transition records its timestamp, actor or system identity, channel/provider reference, reason, correlation identifiers, and idempotency key. Provider callbacks may arrive late, more than once, or out of order; the delivery state machine validates transitions before recording them.

Only an authorized delivery request may enter this state machine. Replaying a callback or retrying provider submission must not create a duplicate user-visible communication.

## Communication Preferences

The platform uses a governed Communication Preference service or equivalent tenant-approved source of truth for channel consent, opt-in and opt-out status, preferred contact method, quiet hours, regional restrictions, and legally required notices.

Channel adapters may report provider-specific preference signals, but they do not own the authoritative preference record. Delivery authorization obtains the current approved preference state at the time of delivery.

---

# Cross-Channel Conversation Continuity

## Conversation Platform Canonical Reference

Conversation Platform owns the canonical conversation and session records. Channel adapters keep only the mapping needed to relate a channel-native thread, call, or message sequence to the authorized platform conversation. Agent Runtime retains only bounded execution references and authorized snapshots.

## Conversation Linking

Two channel interactions may be linked to one conversation only after the platform verifies that the participant, tenant, purpose, and authorization level permit the association. Shared contact details alone are insufficient for sensitive contexts.

## Identity-Linking Rules

Cross-channel identity resolution is an explicit decision with an assurance level and audit record. The platform must distinguish between:

- **Observed channel identifier:** a phone number, sender address, browser session, or provider user ID.
- **Candidate participant:** a possible match based on a tenant-approved matching rule.
- **Verified participant:** a match supported by approved authentication or verification evidence.
- **Authorized conversation association:** permission to connect the interaction to a specific conversation or account for the current purpose.

Automatic linking may be used only where tenant policy permits the available assurance level and data classification. Sensitive account context, regulated data, and high-impact actions require verified identity and any required step-up authentication. Ambiguous matches must create a controlled verification or human-review path rather than selecting a participant silently.

## Channel Switching

When switching channels, the platform must:

- Obtain required user consent and validate the target address or identity.
- Re-evaluate the target channel's capabilities and classification limits.
- Transfer only the minimum context necessary for continuity.
- Record the reason, source, target, actor, and correlation identifiers.
- Inform the user when the handoff materially changes privacy, timing, or interaction expectations.

Example:

```text
Voice conversation
    -> user requests a written summary
    -> consent and recipient verification
    -> approved summary is adapted for email
    -> delivery is authorized and recorded
```

---

# Channel-Specific Interaction Rules

## Voice

Voice interactions require handling for call state, transcription confidence, interruption, latency, speech synthesis, and emergency or safety escalation. A transcript is an interpretation of audio and must retain confidence and provenance where it affects material action.

## Chat and Messaging

Chat and messaging channels may support richer controls, but buttons, forms, deep links, and attachments remain untrusted inputs on return. Provider messaging windows, template requirements, opt-in rules, and delivery limitations must be enforced by the relevant adapter and delivery policy.

## Email

Email is asynchronous and may be forwarded, delayed, or delivered to shared inboxes. The platform must avoid placing sensitive data in email unless classification, consent, and recipient verification permit it. Secure links should be preferred for restricted content.

## API

API clients integrate through an explicit machine identity, versioned contract, idempotency behavior, and tenant-scoped authorization. API calls are not implicitly trusted merely because they originate from an integration partner.

---

# Human Handoff

Human handoff is a controlled transition, not merely a channel delivery event.

```text
Agent Execution
    |
    v
Handoff Policy Evaluation
    |
    +--> Continue with Agent
    +--> Queue for Human Review
    +--> Transfer to Human Channel
    |
    v
Record Handoff Context and Outcome
```

The handoff policy defines eligible conditions, queue ownership, target role, allowed context, participant notification, and return-to-agent rules. The platform must give the human only the context they are authorized to receive and preserve the causal link to the initiating interaction.

---

# Event Integration Boundary

Channels publish and consume normalized events through the governed model in `21_AGENT_EVENT_INTEGRATION.md`.

Examples:

- `interaction.received`
- `interaction.delivery_requested`
- `interaction.delivered`
- `interaction.delivery_failed`
- `conversation.transfer_requested`
- `human.handoff_requested`

Channel adapters must not publish raw external-provider payloads as trusted internal events. They validate and normalize first; external events remain untrusted until this boundary is complete.

An event-triggered response still requires trigger policy, agent/workflow evaluation, authorization, and delivery approval. Receiving a channel event never directly authorizes a user-facing communication or business action.

---

# Security, Privacy, and Tenant Isolation

## Tenant Isolation

Every interaction, delivery target, channel configuration, provider credential, conversation mapping, and channel event is tenant-scoped. A channel address or provider account must never be used to infer cross-tenant access.

## Consent and Preference Management

The platform records communication consent, channel preferences, opt-out status, contactability restrictions, and legally required notices according to tenant and regulatory policy. Consent must be checked for every outbound communication where applicable; it is not assumed permanently from an earlier interaction.

## Content Protection

Content classification determines whether a channel may receive, store, or render an interaction. Restricted data must be minimized, redacted, encrypted, or redirected to an approved secure surface as required by policy.

## Channel Credentials

Provider credentials are owned and rotated through approved secrets and integration controls. They are never exposed in interaction payloads, agent context, logs, or event streams.

---

# Reliability and Failure Handling

## Idempotency

Inbound messages, outbound delivery requests, and provider callbacks use stable identifiers and idempotency controls. Retried delivery must not create duplicate messages, duplicate handoffs, or repeated externally visible actions.

## Ordering and Timing

Global delivery ordering is not assumed. The platform records ordering and channel sequence information when available, validates current session state before acting, and avoids treating delayed messages as current instructions without policy checks.

## Fallback and Degradation

If a channel cannot deliver a response, the platform records the outcome and follows an approved fallback policy. Fallback may queue work, request human review, retry safely, or offer another verified channel; it must not send sensitive content through a less suitable channel by default.

## Provider Failure

Provider outages, rate limits, malformed callbacks, and repeated delivery failures are observable operational conditions. They use bounded retries, dead-letter or quarantine handling where applicable, and the recovery controls defined by Event Integration and Operations Platform.

---

# Observability and Audit

The platform must trace each interaction from ingress to final outcome without exposing unnecessary content.

Required records include:

- Interaction, conversation, session, tenant, channel, and provider references.
- Correlation, causation, and trace identifiers.
- Authentication and identity-assurance result.
- Consent and delivery-authorization decisions.
- Normalization, policy, routing, and adaptation decisions.
- Agent, workflow, tool, handoff, and delivery outcomes.
- Retry, failure, fallback, and provider-status information.

Metrics should include inbound volume, response latency, delivery success, duplicate rejection, channel-switch rate, handoff rate, provider failure, consent rejection, and per-tenant quota use.

---

# Testing Strategy

## Contract Tests

Adapters must verify their mapping to the normalized interaction schema, capability profile, authentication metadata, and delivery-status contract.

## Integration Tests

Integration tests verify tenant routing, identity resolution, session association, policy enforcement, event publication, response adaptation, and controlled handoff to workflows or tools.

## Security Tests

Security tests verify provider signature handling, replay resistance, tenant isolation, consent enforcement, redaction, attachment handling, authorization, and protection against prompt or event injection through channel content.

## Resilience Tests

Resilience tests simulate duplicate callbacks, delayed or out-of-order messages, provider outage, rate limiting, failed delivery, channel switching, and human handoff. They must prove that external communication and business actions are not duplicated.

---

# Implementation Artifacts

Before a channel adapter is implemented or enabled, the following maintained artifacts are required:

| Artifact | Purpose | Owner |
|---|---|---|
| Normalized interaction schema | Executable, versioned interaction and delivery contract | Conversation Platform; Agent Platform consumes it |
| Channel capability matrix | Declares supported behavior, limits, policy, and operational readiness | Channel owner with Agent Platform approval |
| Adapter implementation guide | Defines protocol mapping, idempotency, callbacks, retries, telemetry, and test obligations | Digital Channel Platform with Integration review for shared connector/credential controls |
| Provider runbook | Defines credential rotation, outage response, reconciliation, fallback, and escalation | Operational owner |

These artifacts are implementation companions to this architecture document. They prevent providers, SDKs, and application teams from inventing incompatible interpretations while allowing the underlying technology to change.

---

# Anti-Patterns

## Separate Agent Per Channel

Duplicating prompts, policy, memory behavior, or business logic per channel creates inconsistent customer experiences and governance gaps. Use a shared agent model with controlled channel adaptation.

## Raw Provider Payload to Agent Context

Passing raw webhooks, email markup, or provider metadata directly to an agent creates injection, privacy, and coupling risks. Normalize and classify before execution.

## Silent Sensitive-Channel Fallback

Automatically moving restricted content from a secure channel to email or messaging can violate consent and classification rules. Fallback requires explicit policy and recipient validation.

## Channel as an Authorization Boundary

Treating a phone call, sender address, or chat account as sufficient authorization for a high-impact action is unsafe. Apply identity assurance and permission checks appropriate to the action.

## Delivery Equals Completion

A message being accepted by a provider does not prove user receipt, understanding, or business completion. Record delivery state separately from workflow and business outcomes.

---

# Architecture Boundaries

| Document | Relationship |
|---|---|
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Receives authorized, normalized interaction triggers and executes approved work. |
| `08_AGENT_EXECUTION_ENGINE.md` | Determines agent reasoning and response intent after channel validation; it does not trust channel content as instructions. |
| `11_AGENT_CONTEXT_MODEL.md` | Defines how approved interaction data enters transient execution context. |
| `12_AGENT_INSTRUCTION_SYSTEM.md` | Remains authoritative over behavior regardless of channel content. |
| `15_AGENT_TOOL_SYSTEM.md` | Governs tool actions that may result from an interaction. |
| `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` | Defines Agent consumption of Integration-owned workflow contracts for channel-triggered work. |
| `21_AGENT_EVENT_INTEGRATION.md` | Defines normalized interaction event contracts, subscription controls, and delivery principles. |
| `03_CONVERSATION_PLATFORM/01_CONVERSATION_ARCHITECTURE.md` | Owns canonical conversation, interaction, and cross-channel continuity. |
| `03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md` | Owns canonical conversation session coordination. |
| `03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md` | Owns routing and canonical response ownership. |
| `03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md` | Owns handoff transfer, collaboration, and return behavior. |
| `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent consumption of Security-owned controls applied to channel-triggered activity. |
| `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent use of Security-owned authorization and step-up decisions. |
| `26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent use of tenant-boundary controls for channel-triggered work. |

---

# Final Summary

The Multi-Channel Model enables a single governed agent platform to serve many communication surfaces without duplicating intelligence or weakening controls. Digital Channel adapters normalize non-voice protocols, Conversation owns continuity and routing, and Agent owns policy, execution, and governed use of workflows and tools.

By separating channel presentation from agent behavior, enforcing tenant and consent boundaries, and treating channel content as untrusted context, the platform can extend to new channels while preserving a coherent and secure AI Employee experience.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Multi-Channel Model architecture document. |
| 2.1 | 2026-08-05 | Added contract governance, capability-matrix requirements, durable delivery state, communication-preference ownership, identity-linking rules, and required implementation artifacts. |
| 3.0 | 2026-08-06 | Re-scoped canonical conversation, interaction, session, routing, handoff, and delivery ownership to Conversation Platform. |
| 3.1 | 2026-08-07 | Reconciled the Digital Channel boundary: channel adapters use Digital Channel contracts and must pass through canonical Conversation routing before Agent execution. |
| 3.2 | 2026-08-08 | Approved after Digital Channel, Observability, Testing, Conversation, Security, and Integration boundary review; clarified Conversation ownership of the normalized interaction contract. |
