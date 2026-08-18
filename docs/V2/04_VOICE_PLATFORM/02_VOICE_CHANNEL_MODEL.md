# 02_VOICE_CHANNEL_MODEL

**Version:** 2.2  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document defines the provider-neutral model used to represent voice channels, channel configurations, endpoint evidence, capabilities, and approved Voice interaction/delivery paths.

A voice channel is the transport and media path through which a participant communicates with the platform. It may use PSTN, SIP, WebRTC, an in-app client, a contact-center connection, or a future approved transport. A voice channel is not a canonical conversation, participant identity, agent, session, or authorization grant.

---

# Purpose

The Voice Channel Model gives the platform a stable way to add, configure, secure, observe, test, and retire voice channels without exposing provider-specific details to Conversation or Agent Platform.

It ensures channel selection and media behavior can evolve independently while canonical conversation continuity and agent intelligence remain centralized.

---

# Objectives

The Voice Channel Model must:

- Define Voice channel concepts, channel classes, capabilities, configuration scope, lifecycle, and ownership.
- Support inbound, outbound, bidirectional, transfer, conference, and future approved voice interaction paths.
- Keep provider-specific identifiers, resources, credentials, and behavior inside bounded Voice/Integration adapters.
- Provide Conversation Platform with validated Voice interaction candidates and receive only approved Voice delivery requests.
- Bind every Voice channel and resource to tenant, environment, capability, policy, and operational context.
- Describe channel constraints such as region, language, codec, media direction, DTMF, recording, transfer, participant count, and delivery support without treating them as authorization.
- Support controlled channel onboarding, configuration change, suspension, deprecation, and retirement.
- Remain independent of LiveKit, Twilio, carrier, SIP, WebRTC, STT, or TTS implementation choices.

---

# Scope

This document defines Voice channel concepts, channel configuration, endpoint evidence, capability model, interaction/delivery boundary, channel selection, lifecycle, security/tenant controls, observability, testing, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Canonical conversation association, participant identity/visibility, conversation session, lifecycle, routing, handoff, context, state, or conversation-event meaning | 03_CONVERSATION_PLATFORM |
| Agent purpose, reasoning, response content, model/tool/workflow selection, or execution lifecycle | 02_AGENT_PLATFORM |
| Real-time media setup, audio-stream processing, voice call lifecycle, speech pipeline, turn-taking, telephony/SIP behavior, or provider adapter implementation | Voice documents 03–08 |
| Enterprise identity, permission, consent, secrets, legal/compliance policy, security monitoring, or data-lifecycle implementation | 09_SECURITY_PLATFORM and 08_DATA_PLATFORM |
| Browser/device application UI, microphone permission presentation, accessibility UI, or client experience design | 10_FRONTEND_PLATFORM |
| External connector, CRM, ticketing, workflow, broker, or provider SDK implementation | 07_INTEGRATION_PLATFORM |
| Shared telemetry, testing, deployment, release, and operations infrastructure | 11_OPERATIONS_PLATFORM, 12_DEPLOYMENT_PLATFORM, 13_OBSERVABILITY_PLATFORM, and 14_TESTING_PLATFORM |

---

# Platform Foundation and Digital Channel Boundaries

Platform Foundation supplies the tenant, membership, entitlement, shared configuration, and API-edge facts used to activate and operate a Voice channel. Voice applies those facts to channel and resource eligibility; it does not own their control-plane lifecycle.

Digital Channel Platform owns non-voice participant transport and delivery. Voice owns real-time voice media, telephony, speech, and Voice-channel resources. Both supply evidence through Conversation Platform; neither owns canonical conversation state or may use a Voice endpoint to expose another channel's context.

---

# Core Concepts

## Voice Channel

A Voice channel is an approved communication path that defines how audio and call-control evidence enters or exits the platform. It is described by its class, capabilities, tenant/environment configuration, provider adapter, endpoint/resource references, policy constraints, and operational status.

## Channel Class

A channel class describes transport-level behavior, not a vendor:

| Channel class | Examples | Typical capability focus |
|---|---|---|
| PSTN | Inbound/outbound telephone call | Number association, caller/called evidence, DTMF, call progress, transfer constraints. |
| SIP | Enterprise PBX, trunk, contact-center endpoint | SIP identity evidence, signaling, routing, transfer, codec/capability negotiation. |
| WebRTC | Browser, mobile, embedded voice client | Device/media permission, network adaptation, room/participant media, reconnect, accessibility integration. |
| Provider-hosted voice | Provider-managed voice entry point or room | Bounded provider resource mapping, callback validation, media/call evidence. |
| Contact-center bridge | Approved human/operator telephony path | Queue/agent endpoint media coordination and controlled transfer evidence. |
| Future voice transport | New approved protocol or hardware path | Provider-neutral contract mapping and documented capability/constraint profile. |

## Channel Configuration

A channel configuration is a versioned, tenant/environment-scoped declaration of how an approved Voice channel may be used. It references the channel class, provider adapter, permitted resource, capability profile, policy/consent requirements, operational owner, and lifecycle state.

A configuration is not a credential, participant identity, delivery permission, or a canonical conversation association.

## Endpoint and Resource Evidence

An endpoint or resource is a Voice-level reference such as a phone number, SIP address, room, device/media stream, provider call, trunk, or contact-center endpoint. It is opaque, tenant-scoped evidence.

Possession or observation of an endpoint does not prove a participant identity, participant consent, tenant entitlement, or authority to link to a conversation.

---

# Channel Capability Model

Each channel configuration points to a versioned capability profile. The profile states which actions are technically and policy-operationally supported, and which constraints apply.

| Capability category | Examples |
|---|---|
| Direction | Inbound, outbound, bidirectional, callback, transfer-only, conference. |
| Signaling/call control | Ring, answer, decline, hold, resume, disconnect, provider transfer request, DTMF. |
| Media | Input/output audio, duplex mode, codec range, sample-rate constraints, media reconnect, mute. |
| Speech | STT/TTS availability, supported languages/voices, confidence, partial/final results, interruption support. |
| Participant model | Single participant, conference, human/operator bridge, supervisor/listen-only capability. |
| Recording/transcript | Capture availability, consent/policy requirement, provenance, pause/resume, retention reference. |
| Accessibility | Relay/assistive-path support, captions or transcript availability, DTMF-only fallback, and documented device/channel constraints. |
| Regional/policy | Eligible regions, time windows, caller identity restrictions, emergency capability status, legal constraints. |
| Delivery | Approved output modes, delivery acknowledgement, cancellation, fallback, latency/quality characteristics. |
| Operational | Quota, capacity, maintenance state, health/degradation, support owner, test eligibility. |

A capability profile says what a channel can support. Conversation Platform and Security Platform still decide whether a particular participant interaction, handoff, recording, or delivery is currently permitted.

---

# Channel Configuration Model

~~~text
Voice Channel Configuration
    +-- channelConfigurationId and version
    +-- tenant / organization / environment
    +-- channel class and provider-adapter reference
    +-- approved resource / endpoint reference
    +-- capability-profile reference
    +-- policy, consent, classification, and residency constraints
    +-- operational owner and support status
    +-- lifecycle state and change/audit references
~~~

## Configuration States

| State | Meaning |
|---|---|
| Designed | Proposed but not usable. |
| Validating | Contract, security, tenant, capability, and operational checks are in progress. |
| Active | Eligible for approved Voice interaction and delivery operations. |
| Degraded | Available with registered constraints or safe fallback behavior. |
| Suspended | Temporarily ineligible because of policy, security, incident, maintenance, or capacity condition. |
| Deprecated | Still supported for a defined transition period; replacement and migration are recorded. |
| Retired | No longer eligible for new Voice work; historical references remain governed. |

Only an Active or policy-permitted Degraded configuration may receive an approved Voice operation. A provider resource may exist outside this model, but it is not an approved platform channel until it is registered and activated.

---

# Configuration Precedence and Operation Snapshot

Configuration is resolved in this order: non-overridable enterprise/security constraints; tenant and environment policy; active channel-configuration settings; approved resource/endpoint settings; then temporary operational restrictions such as degradation or maintenance. A lower-precedence setting cannot weaken a higher-precedence security, consent, residency, classification, or legal restriction.

Every accepted Voice interaction candidate and delivery attempt records an immutable snapshot reference for the effective channel configuration, capability profile, contract version, relevant policy/consent constraints, resource binding, and operational state. Later changes affect new work only unless an explicit, safe migration procedure governs an active Voice resource.

---

# Voice Interaction and Delivery Boundary

## Inbound Voice Interaction

Voice Platform accepts provider/channel evidence, validates it for the Voice operation, performs transport-level normalization, and creates a Voice interaction candidate.

The candidate includes tenant/environment, channel configuration, capability profile, provider/resource evidence, observed endpoint/participant evidence, media/speech reference, language/confidence, timing, source provenance, idempotency, correlation, validation result, and protected-content reference where needed.

Conversation Platform decides whether and how that candidate becomes a canonical interaction associated with a conversation.

## Outbound Voice Delivery

Conversation Platform issues an approved delivery request after it has evaluated current conversation ownership, participant/recipient binding, consent, classification, lifecycle, session, routing/handoff, and channel eligibility.

Voice Platform verifies the referenced channel configuration is active and capable, validates the Voice resource state and current constraints, performs the requested Voice operation, and reports an outcome. Provider acceptance does not prove participant receipt, comprehension, or business completion.

## Channel Selection and Routing

Conversation Platform selects the eligible response destination and channel according to its Routing Model. Voice Platform supplies the current capability, health, capacity, regional, and operational eligibility evidence required for that decision.

Voice Platform must not route canonical conversation work, choose an agent/human owner, or override a safe no-route outcome. It may reject a technically unavailable or policy-constrained Voice delivery attempt and report the reason for controlled re-routing or fallback.

## Missing or Unavailable Channel Capability

If the channel configuration, required capability, tenant/resource binding, or current operational eligibility is missing, stale, suspended, ambiguous, or unavailable, Voice Platform does not infer a default. It returns a governed denied, deferred, degraded, or unavailable outcome with the evidence required for Conversation Platform to apply a safe fallback or no-route decision.

---

# Channel Lifecycle and Change Management

## Onboarding

A new channel configuration requires:

1. approved channel class and provider-adapter contract;
2. tenant/environment/resource binding;
3. capability profile and supported contract versions;
4. security, consent, recording, data/residency, and tenant-isolation assessment;
5. operational owner, observability, test scope, failure/recovery, and support readiness;
6. controlled validation before activation.

## Configuration Change

A change to capability, resource binding, provider adapter, routing-relevant health/capacity signal, recording behavior, consent/legal constraint, caller identity, region, or contract version is versioned and reviewed according to risk.

A material change does not silently alter an active participant interaction. It uses a controlled migration, new Voice resource, or safe deprecation path.

## Retirement

Retirement stops new work, records replacement/fallback behavior, preserves historical references only as current retention and authorization permit, revokes operational/provider access as applicable, and removes the configuration after the governed retention window.

## Resource Migration and Porting

Changing a phone number, SIP endpoint, room, trunk, provider resource, or other Voice resource uses a versioned migration record. The record identifies the source/destination binding, tenant/environment, effective time, capability change, authorization, consent/regional impact, rollback path, and historical-reference treatment.

Migration preserves prior Voice evidence as governed historical references. It does not silently reassign a resource across tenants, imply participant identity continuity, or attach new Voice work to an earlier canonical conversation.

---

# Multi-Party and Cross-Channel Constraints

A channel may support multiple simultaneous media participants, but Voice Platform records only Voice-domain participation evidence. Conversation Platform controls canonical participant relationships, role/visibility, conversation association, and handoff.

A participant may change from Voice to another approved channel only through Conversation Platform's current identity, consent, purpose, and continuity rules. A phone number, SIP identity, room, or device is never enough to expose a conversation on another channel.

---

# Security, Privacy, and Tenant Isolation

Every configuration, endpoint/resource mapping, provider account, call/media reference, interaction candidate, delivery request, outcome, recording/transcript reference, and operational action is tenant- and environment-scoped.

Provider callbacks, caller/called identifiers, SIP headers, room names, device claims, media metadata, speech content, DTMF, delivery reports, and recording references are untrusted until validated for their specific operation. They cannot grant Conversation access, change canonical state, or authorize delivery.

Channel configuration access follows least privilege and separation of duties. Configuration activation, provider/resource binding, high-risk caller identity changes, recording changes, and exceptional operations require current authorization, evidence, audit, and approval according to policy.

---

# Observability and Audit

Voice telemetry records channel configuration/version, channel class, provider/adapter category, tenant-safe resource category, capability profile, lifecycle state, interaction/delivery outcome, media/call evidence category, validation result, error/degradation, timing, correlation, and test/synthetic status.

Metrics include channel availability, activation/deprecation progress, inbound validation success, interaction-candidate creation, approved delivery result, capability mismatch, provider callback rejection, configuration drift, tenant mismatch, capacity/degradation, and fallback/no-route contribution. Routine telemetry excludes raw audio, broad transcript content, secrets, and direct participant identifiers.

Audit evidence records configuration creation/change/activation/suspension/retirement, principal/service, tenant/environment, approved scope, capability/policy version, reason, approval, correlation, and outcome.

---

# Testing Strategy

## Contract and Configuration Tests

Validate channel class, configuration, capability profile, identifier/resource binding, tenant scope, lifecycle transition, contract version, compatibility, and provider-neutral mapping.

## Integration and Journey Tests

Validate controlled inbound interaction, approved outbound delivery, provider callback, capability mismatch, degraded/suspended channel, multi-party media evidence, Voice-to-Conversation boundary, and Agent execution handoff.

## Security and Resilience Tests

Simulate forged callback, replay, wrong tenant/resource, stale configuration, invalid capability claim, unsafe cross-channel association, unauthorized configuration change, suspended channel, provider outage, and uncertain delivery outcome. Prove no test creates canonical conversation state, participant disclosure, or external participant contact without the approved boundary and test controls.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Voice channel registry | Defines channel classes, tenant configurations, lifecycle, owner, status, and replacement path | Voice Platform |
| Capability profile catalog | Defines versioned Voice capabilities, limitations, policy-operational constraints, and compatibility | Voice Platform with Conversation and Security owners |
| Voice endpoint/resource binding policy | Defines tenant/environment scope, validation, lifecycle, resource rotation/porting, migration, and audit | Voice Platform with Security and Integration owners |
| Voice interaction/delivery boundary contract | Defines candidate submission, approved delivery, outcomes, errors, correlation, and idempotency | Voice Platform with Conversation owner |
| Channel onboarding/change/retirement procedure | Defines review, activation, migration, deprecation, recovery, and evidence | Voice Platform with Operations, Security, and Testing owners |
| Voice channel test suite | Validates contracts, capability, lifecycle, tenant isolation, security, resilience, and journeys | Voice Platform with Testing Platform |

---

# Anti-Patterns

## Provider Resource Equals Active Channel

A provider number, room, trunk, or call resource is not usable platform configuration until it is tenant-scoped, capability-defined, policy-reviewed, and active.

## Endpoint Equals Participant Identity

Caller ID, phone number, SIP address, browser/device reference, or room identity is evidence only. It cannot independently identify, authorize, or associate a participant with a conversation.

## Capability Equals Permission

A channel technically supporting recording, transfer, outbound calls, or a conference does not make the operation currently authorized.

## Channel Configuration Routes the Conversation

Channel configuration supplies eligibility evidence. Conversation Platform owns conversation routing and response ownership.

## Provider Callback Changes Canonical State

Voice/provider callbacks are validated evidence. Conversation Platform decides whether their facts alter canonical conversation state.

## Retirement Deletes History

Retiring a configuration prevents new work; it does not erase governed historical evidence or bypass retention/legal-hold rules.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 01_VOICE_PLATFORM_ARCHITECTURE.md | Defines Voice Platform components and provider-neutral boundary. |
| 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md | Defines detailed Voice call/resource lifecycle. |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | Defines detailed media and signaling behavior. |
| 05_VOICE_SPEECH_PIPELINE.md | Defines detailed speech capability behavior. |
| 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md | Defines PSTN/SIP and telephony integration behavior. |
| 08_VOICE_PROVIDER_ABSTRACTION.md | Defines provider adapter and replacement model. |
| 10_VOICE_SECURITY.md | Defines Voice-specific security controls. |
| 11_VOICE_TENANT_ISOLATION.md | Defines Voice tenant/resource isolation rules. |
| 03_CONVERSATION_PLATFORM/01_CONVERSATION_ARCHITECTURE.md | Defines canonical Conversation ownership and channel boundary. |
| 03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md | Defines response ownership and channel selection. |
| 03_CONVERSATION_PLATFORM/10_CONVERSATION_SECURITY.md | Defines conversation-domain authorization and continuity controls. |
| 07_INTEGRATION_PLATFORM | Owns provider connector implementation. |
| 09_SECURITY_PLATFORM | Owns enterprise identity, authorization, and compliance controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Voice Channel Model document. |
| 2.1 | 2026-08-06 | Added configuration precedence, operation snapshots, accessibility, unavailable-channel, and resource-migration controls. |
| 2.2 | 2026-08-06 | Finalized after review for completeness, ownership overlap, long-term maintainability, and Platform Foundation/Digital Channel boundaries. |
