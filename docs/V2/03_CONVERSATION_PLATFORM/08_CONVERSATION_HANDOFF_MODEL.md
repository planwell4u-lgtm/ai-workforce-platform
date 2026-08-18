# 08_CONVERSATION_HANDOFF_MODEL

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how a canonical conversation transfers active responsibility between an AI agent, workflow, queue, human operator, supervisor, and approved fallback destination.

Handoff preserves tenant-scoped continuity while changing who is accountable for the next conversation action. It does not give the recipient unrestricted access to history, bypass policy, or redefine the conversation's canonical state.

---

# Purpose

The Conversation Handoff Model provides a controlled, auditable, and recoverable way to move a conversation to the party best able to continue it.

It ensures the request, eligibility, assignment, context sharing, acknowledgement, collaboration, return, timeout, and outcome are explicit facts recorded by the Conversation Platform.

---

# Objectives

The Conversation Handoff Model must:

- Preserve one canonical conversation across agent, human, workflow, queue, and channel changes.
- Separate a request to hand off from acceptance, active ownership, and completion.
- Apply current tenant, identity, skill, queue, workload, policy, availability, and consent restrictions before assignment.
- Transfer only the minimum authorized context needed by the receiving party.
- Make the accountable party, participant visibility, turn authority, and expected next action clear at every stage.
- Support warm, cold, supervised, asynchronous, and fallback handoffs.
- Remain safe under duplicate, delayed, failed, abandoned, and concurrent handoff activity.
- Produce durable evidence for audit, quality review, recovery, and analytics.

---

# Scope

This document defines handoff concepts, state, roles, requests, eligibility, assignment, controlled context transfer, collaboration, lifecycle, recovery, security, observability, testing, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Initial destination selection, ranking, or queue-routing policy | 06_CONVERSATION_ROUTING.md |
| Canonical conversation lifecycle, session lifetime, or state concurrency mechanics | 02_CONVERSATION_LIFECYCLE.md, 04_CONVERSATION_SESSION_MODEL.md, and 09_CONVERSATION_STATE_MANAGEMENT.md |
| Agent reasoning, tool execution, workflow implementation, or agent capability definition | 02_AGENT_PLATFORM |
| Human workforce staffing, HR policy, or contact-center vendor implementation | Operations Platform and relevant Channel Platform |
| Channel/media transport, telephony controls, messaging-provider transfer, or recording implementation | 04_VOICE_PLATFORM and relevant Channel Platforms |
| Enterprise identity, authorization, consent, retention, audit infrastructure, and compliance controls | 09_SECURITY_PLATFORM and 08_DATA_PLATFORM |
| Connector, CRM, ticketing, workflow-engine, broker, or notification implementation | 07_INTEGRATION_PLATFORM |

---

# Core Concepts

## Handoff

A handoff is a governed transfer of accountable next-action responsibility for a conversation or defined work segment. It has its own immutable identifier, state history, reason, source, destination, authorization evidence, context grant, and outcome.

A handoff is not a message, a routing suggestion, a transcript export, a permanent reassignment of customer ownership, or proof that a recipient has accepted responsibility.

## Accountable Owner

The accountable owner is the active agent, workflow, human operator, or queue that is responsible for the next permitted conversation action. The Conversation Platform records this ownership; it does not grant the owner broader conversation access than policy allows.

## Handoff Context

Handoff context is a purpose-limited, time-bounded view containing only the information needed to continue work safely. It may include a summary, current intent, language, verified facts, pending work, prior outcome references, risk flags, and approved interaction references.

Handoff context is a controlled reference or snapshot. It is not an unrestricted transcript, raw recording, private model reasoning, credential, or cross-tenant data export.

---

# Handoff Parties and Roles

| Role | Responsibility |
|---|---|
| Initiator | Requests the handoff and supplies a reason, requested destination criteria, and permitted context intent. |
| Source owner | Is accountable before the transfer becomes active and remains responsible until the handoff reaches a defined transfer point. |
| Destination | The proposed agent, workflow, queue, human operator, or fallback capability. |
| Receiver | The authorized destination representative that accepts responsibility when acknowledgement is required. |
| Coordinator | Conversation Platform capability that records state, validates transitions, issues context access, and publishes facts. |
| Supervisor | Authorized party that can observe, intervene, reassign, or close an escalated handoff. |
| Participant | Customer or other conversation member whose visibility, notification, consent, and channel constraints apply. |

A single human may be receiver and supervisor only where tenant policy permits. A queue can be an interim accountable owner, but it is not treated as evidence that a named human has accepted the handoff.

---

# Handoff Types

| Type | Description |
|---|---|
| Agent-to-human escalation | An agent requests an eligible human or queue because policy, capability, confidence, risk, or participant need requires it. |
| Human-to-agent return | A human returns a conversation to an approved agent after recording the permitted return reason and next action. |
| Agent-to-agent transfer | Responsibility moves to an eligible specialist agent without exposing private reasoning or bypassing agent policy. |
| Workflow transfer | Responsibility moves to an approved workflow or work queue; workflow execution remains Agent/Integration-owned. |
| Queue transfer | Responsibility moves to a governed queue while a receiver is selected or becomes available. |
| Supervisor intervention | An authorized supervisor assumes or changes responsibility because of risk, quality, capacity, or failure. |
| Fallback transfer | A defined safe destination is used after primary destination failure, timeout, or ineligibility. |

Warm handoff means the source and receiver may collaborate during a controlled overlap. Cold handoff means the source stops active participation once transfer is effective. These are collaboration modes, not separate authorization models.

---

# Handoff State Model

~~~text
Requested
    |
    +--> Validating
    |       |
    |       +--> Rejected
    |       +--> Queued
    |       +--> Offered
    |
Queued / Offered
    |
    +--> Accepted
    |       |
    |       +--> Active
    |               |
    |               +--> Completed
    |               +--> Returned
    |               +--> Reassigned
    |
    +--> Expired
    +--> Cancelled
    +--> Failed
~~~

## State Meanings

| State | Meaning |
|---|---|
| Requested | An authorized initiator has asked for transfer; the source owner remains accountable. |
| Validating | Eligibility, policy, destination, participant, session, and context checks are in progress. |
| Queued | An approved queue is accountable while selection or capacity is pending. |
| Offered | An eligible receiver/destination has been invited; acceptance is pending where required. |
| Accepted | Receiver has acknowledged the offer but active transfer conditions may still be completing. |
| Active | The receiving owner is accountable for the next permitted action. |
| Completed | The transfer objective was met or the destination completed its defined work. |
| Returned | Responsibility has been formally returned to a previous or new eligible owner. |
| Reassigned | An authorized coordinator or supervisor changed the receiving destination. |
| Rejected | The request could not proceed because eligibility, policy, state, or destination checks failed. |
| Expired | Required acknowledgement or progress did not occur within the governing time limit. |
| Cancelled | An authorized actor withdrew a pending handoff before it became active. |
| Failed | A technical or uncertain transfer outcome requires controlled recovery or reconciliation. |

Only the Conversation Platform records authoritative handoff transition facts. Routing may propose or select a destination, but it must use this model to make the transfer effective.

---

# Handoff Invariants

- A conversation work segment has exactly one accountable owner or one explicitly recorded safe waiting state.
- Only one active or acceptance-pending handoff may govern the same work segment unless a supervisor-approved collaboration mode explicitly records otherwise.
- A handoff state change never changes tenant, classification, consent, participant visibility, or authorization scope by itself.
- The source owner remains responsible until an active receiving owner or approved waiting state is durably recorded.
- Activation records the effective owner, work segment, policy/eligibility evidence, context-grant reference, and collaboration mode together.
- A failed, expired, cancelled, or superseded handoff has a recorded accountable disposition; it cannot leave the conversation silently unowned.

---

# Handoff Request and Validation

## Required Request Information

A request records the initiating actor, tenant and environment, conversation, interaction, session, and work-segment or response-turn references, source owner, reason code, requested destination or eligibility criteria, urgency, requested collaboration mode, participant notification intent, context purpose, correlation/causation references, and idempotency reference.

The request records links to source evidence rather than copying unrestricted transcript, recording, attachment, customer profile, or model reasoning.

## Validation Order

1. Confirm canonical conversation, session, and source-owner state.
2. Validate initiator identity, permission, tenant, environment, and purpose.
3. Apply participant consent, visibility, channel, legal, classification, residency, and retention restrictions.
4. Validate destination type and route/queue eligibility using the Routing Model.
5. Confirm receiver availability, capacity, skills, language, and policy eligibility where applicable.
6. Create the minimum context grant or reference that the proposed receiver may request.
7. Record the durable request and publish the corresponding conversation fact.

A denied handoff does not expose protected context or destination details to an unauthorized initiator.

---

# Assignment, Acceptance, and Transfer

## Assignment

Routing proposes the destination according to its policy. The Handoff Model records the assignment as an offer, queue transfer, or direct activation according to destination type and tenant policy.

Assignment must include an expiry or review condition. A named receiver does not become accountable merely because they were selected.

## Acceptance and Active Transfer

Where acknowledgement is required, the receiver accepts after current authorization and context eligibility checks. The coordinator then atomically records the receiving owner, handoff active state, effective time, permitted collaboration mode, and context grant.

For direct queue or automated-workflow transfer, policy may permit activation without named-human acceptance. The registry must make this exception explicit.

## In-Flight Work at Transfer

Before activation, the coordinator records the required disposition for source-side agent execution, workflow work, pending tool action, and queued participant-facing delivery that relates to the transferred work segment. The Agent Platform and Integration Platform implement cancellation, completion, or controlled drain through their own contracts.

No in-flight action may continue to produce a conflicting participant-facing response after the receiving owner becomes active. If safe interruption cannot be confirmed, the handoff remains pending or enters failed/reconciliation-required state rather than claiming a clean transfer.

## Participant Notification

Notification is determined by policy, channel capability, safety requirements, and participant preference. It may be required before, during, or after a transfer. Failure to notify does not silently invalidate a transfer; it creates a recorded delivery/notification outcome for recovery.

---

# Context and Collaboration Controls

## Context Grant

The receiving party receives a handoff-scoped grant that states purpose, classification, fields or references, visibility constraints, expiry, revocation conditions, and audit correlation. Every retrieval rechecks current authorization.

## Overlap and Turn Authority

A warm handoff may temporarily allow source and receiver participation. The active owner and turn authority remain explicit so two parties do not send conflicting participant-facing actions.

A supervisor may observe or intervene only within a separately authorized visibility and action scope.

## Restricted Content

The coordinator must exclude or redact content that is unrelated, consent-restricted, legally restricted, unavailable under residency policy, hidden from the receiver role, or prohibited from cross-channel transfer.

---

# Timeout, Failure, and Recovery

## Timeouts and Fallback

Each offer, queue, and active transfer has governing time limits and escalation rules. On timeout, the coordinator may extend, re-offer, reassign, return responsibility, route to a safe fallback, or require supervisor review according to policy.

The source owner must not be released without a known accountable destination or a documented safe waiting state.

## Duplicate and Concurrent Requests

Requests use idempotency references. Conflicting pending handoffs for the same accountable work segment are rejected, merged, superseded, or placed under supervisor review according to canonical state and policy.

## Uncertain Outcomes

If channel/provider failure, receiver disconnect, or persistence uncertainty prevents confirmation, the handoff enters Failed or reconciliation-required status. The Conversation Platform's authoritative state, current authorization, and controlled operational evidence determine the outcome. Retrying must not create duplicate participant messages, assignments, or external actions.

---

# Security, Privacy, and Tenant Isolation

Every handoff, context grant, assignment, notification, audit record, replay, and recovery operation is tenant-scoped and current-policy checked.

Handoff history records who requested, evaluated, selected, accepted, activated, changed, timed out, cancelled, or completed responsibility, with correlation and reason evidence. It must not expose raw protected content in ordinary telemetry or audit views.

A human or service receiving a handoff receives only the access granted for that handoff. Transfer does not confer permanent customer, tenant, transcript, recording, tool, or memory access.

---

# Events and Integration

Conversation Platform publishes governed facts such as handoff.requested, handoff.offered, handoff.accepted, handoff.activated, handoff.reassigned, handoff.expired, handoff.returned, handoff.completed, and handoff.failed after durable state changes.

Events are facts, not commands or authorization. Consumers such as Agent Platform, channels, operations, analytics, and integrations must re-evaluate current policy before acting. 07_CONVERSATION_EVENTS.md owns conversation event semantics; Integration Platform owns broker and connector implementation.

---

# Observability and Audit

Telemetry must capture handoff identifier, state, type, reason, source/destination category, tenant/classification, queue/receiver eligibility result, timing, acceptance, context grant outcome, notification outcome, timeout, fallback, failure, correlation, and final result.

Operational measures include handoff volume, request-to-activation time, queue wait, offer acceptance, expiry, rejection, reassignment, return, failure, fallback, active duration, participant-impacting delay, and outcome by reason/channel/agent/queue. Reporting must use authorized aggregates and avoid raw conversation content.

---

# Testing Strategy

## Contract Tests

Validate request, state transitions, ownership changes, reason codes, context-grant metadata, event schemas, idempotency, correlation, and version compatibility.

## Integration Tests

Validate agent-to-human, human-to-agent, agent-to-agent, workflow, queue, supervisor, fallback, channel-continuity, notification, event, and authorized context-retrieval paths.

## Security and Resilience Tests

Simulate unauthorized initiator or receiver, tenant mismatch, restricted context, revoked consent, unavailable receiver, queue saturation, duplicate request, simultaneous transfer, disconnect during acceptance, delayed provider event, timeout, replay, and uncertain persistence outcome. Prove that no test results in uncontrolled context disclosure, duplicate participant action, or missing accountable owner.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Handoff state contract | Defines states, transitions, invariants, and concurrency rules | Conversation Platform |
| Handoff reason and outcome registry | Defines governed reasons, urgency, outcomes, and reporting semantics | Conversation Platform with Operations owner |
| Destination eligibility contract | Defines inputs from routing, availability, skill, capacity, language, and policy systems | Conversation Platform with Routing and Security owners |
| Context-transfer policy | Defines purpose, minimization, visibility, expiry, revocation, and retrieval controls | Conversation Platform with Security and Context owners |
| Queue and acknowledgement policy | Defines offer, queue, acceptance, timeout, fallback, and supervisor behavior | Conversation Platform with Operations owner |
| Handoff event catalog | Defines conversation facts and consumer boundaries | Conversation Platform with Events owner |
| Handoff test suite | Validates contract, integration, security, resilience, and recovery cases | Conversation Platform with Testing Platform |

---

# Anti-Patterns

## Assignment Is Treated as Acceptance

Selecting a human or agent does not make them accountable until the policy-defined transfer point is recorded.

## Transcript Dump Handoff

Copying the full transcript or recording into a queue or ticket ignores purpose, privacy, and staleness controls. Use minimal, authorized context.

## Source Owner Disappears Too Early

The current owner remains accountable until an active receiving owner or approved waiting state exists.

## Queue Is Treated as a Human Receiver

A queue coordinates pending responsibility; it does not imply a named human accepted or accessed the conversation.

## Handoff Bypasses Routing or Authorization

A handoff may not select an ineligible destination or grant broader access merely because an initiator requested it.

## Retry Sends Another Participant Message

Recovery must reconcile current state and external effects before retrying notification, delivery, or transfer action.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines the Handoff and Collaboration Service and platform boundary. |
| 02_CONVERSATION_LIFECYCLE.md | Defines conversation lifecycle and waiting-state effects. |
| 03_CONVERSATION_MODEL.md | Defines conversation, participant, interaction, and assignment references. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session continuity and transfer constraints. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context selection, provenance, sharing, expiry, and revocation. |
| 06_CONVERSATION_ROUTING.md | Defines destination eligibility and routing decisions. |
| 07_CONVERSATION_EVENTS.md | Defines handoff-event semantics, publication, and consumption controls. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines canonical state, concurrency, history, and reconciliation. |
| 02_AGENT_PLATFORM | Defines agent execution, agent eligibility inputs, and agent-side handoff integration. |
| 04_VOICE_PLATFORM | Defines voice/media transfer and channel-specific constraints. |
| 07_INTEGRATION_PLATFORM | Defines connector, workflow, CRM, ticketing, and notification implementation. |
| 09_SECURITY_PLATFORM | Defines enterprise identity, authorization, consent, and compliance controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Conversation Handoff Model document. |
| 2.1 | 2026-08-06 | Added handoff invariants, work-segment identity, activation evidence, and safe in-flight work disposition. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |
