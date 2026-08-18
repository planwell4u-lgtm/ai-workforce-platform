# 03_VOICE_CALL_AND_SESSION_LIFECYCLE

**Version:** 1.2  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document defines the Voice-domain lifecycle for calls, media resources, and bounded Voice sessions. It explains how Voice observes, validates, coordinates, and retires transport resources without becoming the owner of a canonical conversation, Conversation session, participant relationship, routing decision, or agent execution.

A Voice call or session is a time-bounded transport and media coordination record. It may be created for an inbound PSTN/SIP/WebRTC interaction, an approved outbound delivery, a conference, a transfer leg, or a provider-specific resource. It is not a canonical conversation session and must not be used as one.

---

# Purpose

The lifecycle model provides a provider-neutral, auditable way to coordinate signaling, media readiness, interaction capture, output delivery, recovery, and termination across Voice channels.

It ensures that delayed, duplicated, missing, or conflicting provider events do not silently change canonical Conversation state or cause unintended participant-facing call control or output.

---

# Objectives

The Voice call and session lifecycle must:

- Define Voice-domain resources, states, transitions, ownership, and terminal outcomes.
- Support inbound, outbound, bidirectional, transfer, conference, reconnect, and provider-recovery paths.
- Keep call/resource lifecycle distinct from canonical Conversation and Agent execution lifecycles.
- Produce validated, versioned evidence for Conversation Platform rather than canonical state changes.
- Require tenant/environment, channel, capability, policy, consent, and authorization checks at appropriate transitions.
- Handle retries, duplicate callbacks, out-of-order delivery, partial media failure, cancellation, and uncertain provider outcomes safely.
- Keep provider call, room, stream, and leg identifiers bounded to the Voice domain.

---

# Scope

This document defines Voice call/session concepts, state machines, transition rules, correlation, recovery, multi-party resources, lifecycle security, observability, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Canonical conversation lifecycle, participant association, Conversation sessions, state, routing, handoff, or events | 03_CONVERSATION_PLATFORM |
| Agent reasoning, work ownership, execution lifecycle, tool cancellation, or response content | 02_AGENT_PLATFORM |
| Detailed real-time media protocol, codec, stream processing, or signaling implementation | 04_VOICE_REALTIME_MEDIA_ARCHITECTURE |
| Speech recognition, synthesis, transcript semantics, VAD, or interruption policy details | 05_VOICE_SPEECH_PIPELINE.md and 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md |
| PSTN/SIP provider integration details | 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md |
| Enterprise identity, authorization, consent policy, secrets, retention execution, or compliance controls | 09_SECURITY_PLATFORM and 08_DATA_PLATFORM |

---

# Platform Foundation and Digital Channel Boundaries

Platform Foundation supplies the tenant, membership, entitlement, configuration, and API-edge facts that Voice checks before admitting or operating a Voice resource. Voice does not create or alter those control-plane facts.

Digital Channel Platform owns non-voice transport and delivery. A Voice call/session may correlate with an approved cross-channel conversation operation, but it cannot create a digital-channel resource, expose another channel's context, or replace Conversation Platform's continuity rules.

---

# Core Concepts

## Voice Call

A Voice call is a bounded Voice-domain coordination record for a channel-level communication attempt or active connection. It may contain one or more provider legs, media streams, and participants. It records validated transport evidence, state, configuration snapshots, and outcomes.

## Voice Session

A Voice session is a bounded coordination context for media and interaction activity. It may be one-to-one with a call, may span a reconnect of the same approved resource, or may contain multiple call legs where the channel supports it. It is not a Conversation session and does not decide continuity across channels.

## Call Leg

A call leg is a provider/channel-specific connection segment, such as an inbound carrier leg, an outbound dial attempt, a SIP dialog, a WebRTC participant connection, or a transfer/conference leg. A leg has its own local state and may end while the Voice call continues.

## Media Resource

A media resource is a bounded reference to an audio stream, room, track, bridge, device connection, or equivalent provider resource. It conveys transport availability and health only; it is not authority to access a conversation or its content.

## Lifecycle Evidence

Lifecycle evidence is a normalized Voice fact such as call detected, source validated, media ready, call connected, output started, disconnect observed, or outcome uncertain. Conversation Platform determines whether a validated fact has canonical consequence.

---

# Resource Association and Cardinality

The following relationships are explicit so implementation does not confuse transient Voice resources with canonical Conversation coordination:

~~~text
Voice Session
    +-- zero or more Voice Calls
            +-- one or more Voice Legs
                    +-- zero or more bounded Media Resources
~~~

- A Voice call belongs to exactly one Voice session for its active lifetime.
- A Voice session may contain multiple calls only where a documented operation requires it, such as a controlled transfer, a conference bridge, or a provider-approved replacement resource.
- A Voice call has one or more legs. A new provider connection, transfer target, or conference participant creates a distinct leg; it never silently reuses another leg's identity, authority, or media access.
- A reconnect normally creates a new leg on the existing eligible call/session. If provider evidence cannot safely correlate it, Voice creates a new call/session and reports it as a separate candidate to Conversation Platform.
- A Voice call/session may reference at most one Conversation correlation reference for a given operation, but that reference does not prove association to a canonical Conversation or Conversation session. Conversation Platform resolves and owns that association.
- A Voice session may close, be replaced, or be abandoned while the related canonical Conversation session remains active, waiting, handed off, or closed according to Conversation rules.

---
# Identifier and Correlation Rules

Every Voice resource has a Voice-generated opaque identifier. Provider identifiers remain adapter-scoped and are never used as canonical Conversation, participant, or authorization identifiers.

| Identifier/reference | Use | Restriction |
|---|---|---|
| `voiceCallId` | Voice call coordination and audit | Not a conversation ID or participant identity. |
| `voiceSessionId` | Bounded Voice media/interaction context | Not a Conversation session ID. |
| `voiceLegId` | Individual transport leg coordination | Not exposed as a reusable authorization token. |
| `mediaResourceRef` | Protected stream/room/bridge reference | Access requires current Voice and Security authorization. |
| Conversation correlation reference | Links approved Voice evidence to a Conversation operation | Conversation Platform owns its meaning and association. |
| Provider resource reference | Adapter-local evidence mapping | Never crosses the adapter as a trusted canonical identifier. |

All transitions carry tenant, environment, channel-configuration/version, capability-profile/version, correlation, idempotency, trace, and timestamp evidence. The effective configuration and policy snapshot is immutable for the operation; a later configuration change applies only through a controlled migration or new operation.

---

# Voice Call Lifecycle

## State Model

~~~text
Detected
  -> Validating
  -> Admitted
  -> Establishing
  -> Connected
  -> MediaReady
  -> Active
  -> Ending
  -> Ended

Any non-terminal state may move to Denied, Failed, Cancelled, or OutcomeUncertain.
Connected / MediaReady / Active may move to Degraded or Reconnecting, then return
to the latest safe state or finish with Failed, Ended, or OutcomeUncertain.
~~~

| State | Meaning | Permitted next states |
|---|---|---|
| Detected | A provider/channel event suggests a new call or leg. No trust or canonical association is implied. | Validating, Denied, Failed |
| Validating | Voice validates source, replay protection, tenant/resource binding, configuration, and basic channel eligibility. | Admitted, Denied, Failed |
| Admitted | Voice has accepted the operation into its bounded domain and created an auditable resource record. | Establishing, Cancelled, Failed |
| Establishing | Signaling, call control, and media resource setup are in progress. | Connected, MediaReady, Degraded, Failed, Cancelled, OutcomeUncertain |
| Connected | Channel-level connection evidence is validated; media may not be usable yet. | MediaReady, Active, Degraded, Ending, Failed, OutcomeUncertain |
| MediaReady | Required media direction is available according to the operation. | Active, Degraded, Reconnecting, Ending, Failed |
| Active | The resource can capture approved Voice interaction or execute an approved Voice delivery. | Degraded, Reconnecting, Ending, Failed, OutcomeUncertain |
| Degraded | The resource remains available only with documented limitations or safe fallback. | MediaReady, Active, Reconnecting, Ending, Failed |
| Reconnecting | Previously admitted resource is attempting controlled restoration. | MediaReady, Active, Ending, Failed, OutcomeUncertain |
| Ending | A validated local, provider, Conversation-authorized, or policy-driven request is closing the resource. | Ended, Failed, OutcomeUncertain |
| Ended | A terminal, validated completion/disconnect outcome has been recorded. | None |
| Denied | A required admission check failed; no Voice work proceeds. | None |
| Cancelled | A valid cancellation occurred before final completion. | None |
| Failed | Voice has a confirmed unsuccessful outcome. | None |
| OutcomeUncertain | Completion/disconnect cannot be confirmed safely. Reconciliation is required. | None |

No transition is inferred solely from elapsed time. A timeout creates a bounded failure, retry, reconciliation, or uncertain-outcome action according to the operation and available evidence.

---

# Transition Authority and Guards

The state tables define the permissible state graph. This matrix defines who may request or cause a transition and what must be true before it is accepted.

| Transition class | Allowed trigger/source | Required guards | Voice result |
|---|---|---|---|
| Detection and validation | Channel/provider adapter or approved inbound gateway | Current adapter contract, source authenticity, freshness/replay checks, tenant/resource mapping | Create evidence; move only to Validating, Admitted, Denied, or Failed. |
| Admission | Voice lifecycle coordinator | Active channel configuration, capability, operational eligibility, required policy/consent references, idempotency check | Create bounded call/session and immutable operation snapshot. |
| Establishment and readiness | Voice coordinator using validated provider/media evidence | Admitted resource, supported state transition, current resource binding, required media direction | Move to Establishing, Connected, MediaReady, Degraded, or terminal outcome. |
| Interaction capture | Voice media/speech boundary | MediaReady/Active resource, current capture policy, source provenance, duplicate suppression | Submit a Voice interaction candidate; do not alter canonical state. |
| Participant-facing delivery | Approved Conversation delivery request | Current request authorization, recipient/channel binding, capability, policy/consent, cancellation, and resource-state checks | Start, suppress, interrupt, or report delivery outcome. |
| Call control | Approved Conversation request, valid participant/provider event, or Voice safety control | Active resource, operation capability, current policy, and operation-specific authorization | Perform bounded hold/resume/transfer/conference/disconnect or report denial/failure. |
| Reconnect and recovery | Valid provider/media evidence or controlled Voice recovery process | Existing eligible resource, correlation, bounded recovery window, current configuration/policy, idempotency | Restore only allowed transport coordination or record terminal/reconciliation outcome. |
| Closure and terminal outcome | Valid provider disconnect, approved request, policy/safety stop, or confirmed failure | Transition is valid from current state; competing operations are cancelled, drained, or reconciled | Release resource and emit terminal Voice evidence. |

Conversation Platform is never a direct writer of Voice state. It issues authorized delivery or call-control requests and consumes Voice evidence. Voice Platform is never a direct writer of canonical Conversation, Conversation-session, routing, handoff, or Agent-execution state.

---
# Voice Session Lifecycle

The Voice session lifecycle tracks coordination availability, not canonical conversational continuity.

| State | Meaning |
|---|---|
| Created | A Voice session record exists after admission. |
| Preparing | Required media, speech, and call-control prerequisites are being coordinated. |
| Ready | The session can accept approved Voice interaction or delivery work. |
| Engaged | An approved capture or delivery operation is active. |
| Paused | Media/call control is intentionally paused, held, or policy-restricted. No new work is assumed valid. |
| Recovering | The session is reconciling a reconnect, provider delay, or partial failure. |
| Closing | The session is draining/cancelling bounded work and releasing resources. |
| Closed | Voice session coordination has ended. |

A Voice session can close while its related Conversation remains active. A Conversation may also remain active while a new Voice session is later admitted through an approved Channel and Conversation path.

---

# Timing, Expiry, and Bounded Work

Voice owns the enforcement of Voice-domain timers, while tenant/channel policy and Operations/Security governance define their configured values and permitted exceptions. At minimum, configuration must define admission validity, signaling/connection timeout, media-readiness timeout, ring/no-answer timeout where applicable, reconnect window, output-drain/cancellation window, provider-callback freshness window, and reconciliation deadline.

Timer expiry never supplies missing evidence or changes canonical state. It produces an explicit Voice result such as denied, failed, cancelled, degraded, or outcome uncertain. Any resulting Conversation session expiry, waiting state, reroute, participant notification, or handoff action remains owned by Conversation Platform.

---
# Admission and Establishment

## Inbound Admission

For inbound activity, Voice Platform:

1. receives provider/channel evidence;
2. verifies provider authenticity, freshness, replay/idempotency data, and adapter contract compatibility;
3. resolves the active tenant/environment channel configuration and resource binding;
4. evaluates channel capability, operational availability, and applicable Voice policy/consent constraints;
5. creates the bounded Voice call/session record and configuration snapshot; and
6. emits a validated Voice lifecycle fact or a governed denied/failed result.

Admission does not authenticate a participant for Conversation access, create a canonical conversation, infer a Conversation session, or authorize agent work.

## Outbound Admission

An outbound call or participant-facing Voice delivery begins only from an approved Conversation Platform request. Voice revalidates the request against current channel state, tenant/resource binding, capability, caller identity, regional/time restrictions, consent/policy evidence, cancellation state, and provider readiness.

If any required evidence is missing, stale, contradictory, or unauthorized, Voice must deny, defer, or report an unavailable outcome. It must not select a recipient, substitute a channel, or place a call based on provider capability alone.

---

# Active Interaction and Delivery Boundaries

## Interaction Capture

When a session is MediaReady or Active, Voice may capture transport and speech evidence and form a Voice interaction candidate. The candidate retains source/provenance, timing, confidence, language, protected-content reference, idempotency, and current resource/configuration evidence.

Conversation Platform alone determines whether the candidate belongs to a canonical conversation, whether a participant is associated, and whether it changes canonical state.

## Delivery

Voice performs output preparation and delivery only after receiving an approved Voice delivery request. It reports distinct outcomes such as accepted, media output started, interrupted, provider acknowledged, delivery failed, cancelled, or uncertain. Provider acceptance and audio stream start do not prove receipt, comprehension, or business completion.

## Cancellation

Cancellation is explicit and idempotent. Voice honors a valid Conversation-authorized cancellation, Voice safety/policy stop, disconnect, or terminal provider event. It stops or suppresses pending participant-facing output where technically possible and reports the resulting evidence.

Agent execution cancellation is owned by Agent Platform through its approved contracts. Voice may signal a delivery interruption or resource loss; it does not decide whether reasoning or external work should continue.

---

# Call Control, Holds, Transfers, and Multi-Party Resources

Voice Platform may coordinate technically supported ring, answer, hold, resume, disconnect, transfer request, conference bridge, mute, or media-direction operations. Each action requires an active resource, channel capability, current policy, and the appropriate approved request.

| Operation | Voice responsibility | Not Voice responsibility |
|---|---|---|
| Hold/resume | Apply supported transport control and report outcome. | Determine canonical waiting state or work ownership. |
| Transfer | Validate technical capability and establish controlled legs/bridge evidence. | Decide accountable human/agent handoff or expose context. |
| Conference | Coordinate approved media participants and their Voice evidence. | Define canonical participant roles, visibility, or authorization. |
| Disconnect | End the Voice resource on valid request or evidence. | Close the canonical conversation automatically. |

A new transfer or conference leg does not inherit participant identity, consent, authorization, or conversation visibility from an existing leg. Those conditions must be re-evaluated through their owning platform contracts.

---

# Recovery, Reconciliation, and Terminal Outcomes

## Reconnect

Reconnect requires a bounded window, verified resource binding, fresh provider evidence, and an idempotent correlation to the existing Voice resource. On reconnect, Voice restores only allowed transport/media coordination. It does not replay output, re-open canonical conversation state, or resume stale delivery without current approval.

## Provider Event Ordering and Duplication

Adapters preserve source sequence/evidence where available. Voice deduplicates idempotent events and records contradictory or out-of-order evidence for reconciliation. A late `connected` event cannot revive a Voice resource already terminally ended unless a separately admitted new resource is created.

## Uncertain Outcome

Voice uses `OutcomeUncertain` when it cannot prove whether a call-control or participant-facing operation completed. It records the last trustworthy state, provider evidence, correlation, and required reconciliation action. It must not retry an externally visible operation automatically when that could create a duplicate call, duplicate output, or conflicting participant experience.

## Resource Release

On closure, Voice stops new media/speech/output work, revokes transient resource access, closes or detaches provider resources according to policy, and emits the appropriate normalized outcome. Historical evidence, recordings, and transcripts remain subject to their separately governed retention and access controls.

---

# Terminal Outcome Taxonomy

Every terminal Voice call, session, and leg records one primary outcome and may record secondary contributing causes. The taxonomy is provider-neutral and distinct from canonical Conversation session, delivery, handoff, and business outcomes.

| Outcome | Meaning |
|---|---|
| Completed | The bounded Voice operation finished with its expected transport-level completion evidence. |
| ParticipantEnded | Valid evidence indicates the participant ended or abandoned the channel resource. |
| ProviderEnded | The provider/carrier ended the resource without a more specific safe classification. |
| NoAnswerOrTimeout | An approved outbound/ring operation expired without an answer or completion evidence. |
| BusyOrRejected | Provider/channel evidence indicates busy, decline, or equivalent transport refusal. |
| PolicyDenied | A required policy, consent, authorization, capability, or tenant/resource guard prevented the operation. |
| Cancelled | A valid cancellation or safety stop ended pending or active Voice work. |
| MediaFailed | Required audio/signaling/media capability failed and safe recovery was unavailable. |
| ProviderFailed | A confirmed provider, adapter, or external dependency failure prevented completion. |
| SecuritySuspended | A security, fraud, integrity, or tenant-isolation control stopped the resource. |
| OutcomeUncertain | Voice cannot safely determine the externally visible result; reconciliation is required. |

The terminal record includes the outcome, contributing causes, last trustworthy state, relevant provider evidence category, correlation/idempotency references, and whether any participant-facing effect requires reconciliation. It never treats a Voice outcome alone as proof of delivery receipt, participant comprehension, or business completion.

---

# Minimum Lifecycle Evidence Contract

The implementation must publish versioned lifecycle evidence using a provider-neutral shape. Provider adapters may add protected adapter-local fields but cannot change the required semantics.

| Field | Requirement |
|---|---|
| `eventId`, `eventType`, `contractVersion`, `occurredAt` | Required unique event identity, normalized fact type, compatibility version, and observed time. |
| `tenantRef`, `environmentRef` | Required tenant and environment scope. |
| `voiceCallId`, `voiceSessionId`, `voiceLegId` | Required when the relevant Voice resource exists; opaque Voice-domain identifiers only. |
| `channelConfigurationRef`, `capabilityProfileRef`, `operationSnapshotRef` | Required configuration/capability/policy-operation provenance. |
| `correlationRef`, `causationRef`, `idempotencyKey`, `traceRef` | Required ordering, duplicate-control, and diagnostic linkage as applicable. |
| `stateBefore`, `stateAfter`, `transitionCause` | Required for a state transition; cause identifies validated provider, approved request, policy, safety, or recovery source. |
| `providerEvidenceRef` | Protected, adapter-bounded reference to supporting provider evidence; never a canonical ID or credential. |
| `outcome`, `errorCategory`, `retryOrReconciliationStatus` | Required for terminal, denied, failed, cancelled, or uncertain outcomes. |
| `conversationCorrelationRef` | Optional opaque reference supplied for an approved operation; its canonical meaning is resolved only by Conversation Platform. |

The contract carries references rather than raw audio, DTMF, full transcripts, credentials, or unrestricted participant identifiers. Semantic changes, new required fields, or altered security/delivery/cancellation meaning require a new contract version and compatibility plan.

---
# Security, Privacy, and Tenant Isolation

Every state transition is authorized within the current tenant, environment, channel configuration, provider account/resource, service/principal, purpose, and policy context.

- Provider callbacks, caller/called identifiers, SIP headers, room names, device claims, DTMF, audio metadata, and provider lifecycle states are untrusted until validated.
- A Voice call/session/leg/media reference is opaque and tenant-scoped; it cannot be used to discover or access a canonical conversation.
- Raw audio, DTMF, full transcript content, direct participant identifiers, and credentials are excluded from routine lifecycle logs and metrics.
- Hold, transfer, conference, recording, outbound dialing, and caller identity actions require operation-specific policy and authorization checks.
- Suspension, revocation, or policy change prevents new Voice operations and applies the documented safe action to active resources; it never silently weakens consent, tenant, or legal constraints.

---

# Observability and Audit

Voice lifecycle telemetry records tenant-safe identifiers/references, state transition, cause, adapter category, channel/configuration version, capability profile, correlation, idempotency result, timing, degradation, retry/reconciliation status, and terminal outcome.

Required measures include admission success/denial, time to connection and media readiness, active duration, reconnect rate, transition failure, cancellation latency, duplicate/out-of-order callback rate, transfer/conference outcome, output interruption, uncertain outcome, and resource-release completion.

Audit records lifecycle-impacting configuration changes, admission, outbound initiation, call-control operations, exceptional recovery, cancellation, and terminal reconciliation with principal/service, approved scope, policy/configuration version, reason, evidence, and outcome.

---

# Testing Strategy

## State and Contract Tests

Validate every allowed and forbidden transition, terminal-state immutability, idempotency, contract compatibility, configuration snapshot behavior, and provider-neutral identifier rules.

## Integration and Journey Tests

Validate inbound and outbound lifecycle paths, media readiness, controlled interaction capture, authorized delivery, holds, transfer/conference legs, disconnect, reconnect, and Voice-to-Conversation boundary behavior.

## Security and Resilience Tests

Simulate forged/replayed callbacks, wrong tenant/resource, stale configuration, duplicate/out-of-order events, provider timeout, partial media loss, forced disconnect, cancellation race, uncertain delivery, and policy revocation. Prove no scenario creates canonical conversation state, exposes context, or contacts a participant without the approved boundary.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Voice lifecycle state machine | Defines call/session/leg states, transitions, causes, terminal outcomes, and invariants | Voice Platform |
| Lifecycle evidence contract | Defines provider-neutral facts, required fields, correlations, idempotency, ordering, errors, compatibility, and protected evidence references | Voice Platform with Conversation owner |
| Transition authority and guard matrix | Defines accepted triggers, authority, prerequisites, state effects, and prohibited cross-platform writes | Voice Platform with Conversation, Security, and Operations owners |
| Voice resource association rules | Defines call/session/leg/media cardinality, reconnect treatment, and Conversation correlation boundary | Voice Platform with Conversation owner |
| Voice timing policy | Defines configured Voice-domain time bounds, expiry effects, exceptions, and operational ownership | Voice Platform with Operations, Security, and Channel owners |
| Call-control operation contract | Defines approved hold, resume, transfer, conference, disconnect, cancellation, and outcomes | Voice Platform with Conversation and Security owners |
| Reconnect and reconciliation procedure | Defines bounded recovery, uncertain outcomes, retry limits, evidence, and operator action | Voice Platform with Operations owner |
| Lifecycle test suite | Proves state safety, tenant isolation, contract behavior, recovery, and participant-facing controls | Voice Platform with Testing owner |

---

# Anti-Patterns

## Call End Means Conversation Closed

Voice resource termination is evidence only. Conversation Platform decides canonical lifecycle outcomes.

## Voice Session Equals Conversation Session

A Voice session coordinates transport/media and can be brief or reconnectable. It never replaces Conversation session ownership or cross-channel continuity rules.

## Provider Callback Is a State Transition Authority

Provider events are validated evidence. They cannot directly change canonical conversation state or grant access.

## Reconnect Replays Work Automatically

Reconnect restores only eligible transport coordination. Pending output and work require current, idempotent authorization.

## Transfer Leg Inherits Participant Authority

A new leg provides transport evidence only. Participant identity, consent, visibility, and handoff ownership remain governed by their respective contracts.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 01_VOICE_PLATFORM_ARCHITECTURE.md | Defines high-level Voice boundaries and contracts. |
| 02_VOICE_CHANNEL_MODEL.md | Defines channel configuration, capabilities, and resource eligibility. |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | Defines detailed signaling and media coordination. |
| 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md | Defines interruption and output cancellation coordination. |
| 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md | Defines PSTN/SIP call-control implementation boundaries. |
| 12_VOICE_RELIABILITY_AND_FAILURE_HANDLING.md | Defines detailed failure and operational recovery behavior. |
| 03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md | Defines canonical Conversation session ownership. |
| 03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md | Defines canonical Conversation event semantics. |
| 03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md | Defines accountable handoff behavior. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created provider-neutral Voice call and session lifecycle model with state, boundary, recovery, and governance rules. |
| 1.1 | 2026-08-06 | Finalized resource cardinality, transition authority, time-bound, terminal-outcome, and lifecycle-evidence rules. |
| 1.2 | 2026-08-06 | Finalized after review for completeness, ownership overlap, long-term maintainability, and Platform Foundation/Digital Channel boundaries. |



