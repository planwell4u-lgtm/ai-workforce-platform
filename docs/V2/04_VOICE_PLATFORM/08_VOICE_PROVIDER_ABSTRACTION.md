# 08_VOICE_PROVIDER_ABSTRACTION

**Version:** 1.2  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document defines the provider abstraction boundary for the Voice Platform. It keeps media, telephony, speech, recording, and related Voice providers interchangeable behind provider-neutral contracts.

LiveKit, ElevenLabs, OpenAI, Twilio, SIP carriers, STT/TTS services, contact-center platforms, and future providers are implementation options. They do not own canonical Conversation state, participant identity, agent reasoning, business workflow, tenant policy, or the public Voice contract.

---

# Purpose

The Provider Abstraction enables the platform to adopt, compare, replace, migrate, and fail over providers without rewriting the Voice domain or leaking provider-specific identifiers, credentials, event formats, limits, or semantics into other platform modules.

It supports tenant-aware selection based on compliance, capability, quality, latency, reliability, cost, and operational requirements while preserving safe behavior during provider failure, version change, migration, and uncertain external effects.

---

# Objectives

The abstraction must:

- Define stable provider-neutral contracts for Voice channel, lifecycle, media, speech, turn-taking, telephony, recording-reference, and outcome behavior.
- Isolate each provider SDK, webhook, resource, credential, identifier, error, and billing format inside a bounded adapter.
- Support multiple providers simultaneously by tenant, environment, channel, capability, operation, and controlled rollout.
- Select providers only from approved, current tenant profiles using ordered compliance, capability, quality, latency, reliability, and cost constraints.
- Provide deterministic, duplicate-safe fallback and migration behavior.
- Make provider capability limits, degradation, compatibility, change, and deprecation visible to operations and downstream owners through normalized evidence.
- Prevent a provider from becoming a canonical identifier, authorization boundary, direct Agent tool, or hidden owner of business state.
- Require test, security, privacy, tenant-isolation, observability, cost, and rollback evidence before provider activation or material change.

---

# Scope

This document defines provider roles, adapter architecture, provider registry and capability profiles, contract/version rules, tenant selection, fallback/migration, data/security controls, observability, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Voice channel/endpoint configuration, generic capability semantics, or channel lifecycle | 02_VOICE_CHANNEL_MODEL.md |
| Voice call/session/leg lifecycle, state authority, correlation, timing, and terminal outcomes | 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md |
| Media signaling/resources, buffering, flow control, media state, and delivery transport facts | 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md |
| STT/TTS result semantics, speech quality, tenant speech profile, and speech operational targets | 05_VOICE_SPEECH_PIPELINE.md |
| VAD, endpointing, barge-in, turn windows, and output interruption behavior | 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md |
| Telephony endpoint, SIP/carrier signaling, route, call-control, and telephony error semantics | 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md |
| Recording/transcript capture governance, retention, deletion, legal hold, or data export | 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md and 08_DATA_PLATFORM |
| Enterprise identity, authorization, secrets, procurement, contract/legal policy, or billing implementation | 09_SECURITY_PLATFORM, Finance/Billing ownership, and Operations |
| Canonical Conversation, participant, routing, handoff, or event semantics | 03_CONVERSATION_PLATFORM |
| Agent content, reasoning, tools, workflow, or provider/model decision outside the Voice domain | 02_AGENT_PLATFORM |

---

# Platform Foundation and Digital Channel Boundaries

Platform Foundation supplies tenant, membership, entitlement, shared configuration, and API-edge facts that constrain provider eligibility. Voice resolves a provider only within those control-plane limits; it does not own their lifecycle.

Digital Channel Platform owns non-voice provider selection and delivery. A Voice provider fallback or migration applies only to the current bounded Voice operation and cannot select, invoke, or expose a digital-channel provider/resource.

---

# Architecture Principles

## Provider Neutrality Is a Product Boundary

Every capability used outside an adapter is described by a Voice contract owned by this platform. A provider may implement the capability differently, but cannot redefine its canonical identifiers, security meaning, event semantics, outcome, or ownership boundaries.

## Adapters Translate; They Do Not Decide

An adapter validates and maps provider-specific inputs/outputs to approved Voice contracts. It does not choose a canonical conversation, associate a participant, route work, author content, decide policy, grant authorization, or select another provider outside its current bounded operation.

## Capability Does Not Equal Eligibility

A provider may technically support a function yet be ineligible because of tenant scope, compliance, region, contract, data policy, quality/latency class, cost/quota, health, or current operation constraints.

## Selection Is Explicit and Versioned

Every operation uses an immutable provider-selection snapshot containing the selected adapter/profile/version, capability, relevant configuration, eligibility evidence, fallback policy reference, correlation, and time. A provider change affects new work only unless an explicit controlled migration applies.

## Fallback Must Be Duplicate-Safe

A provider timeout, error, or health signal never permits automatic replay of a participant-visible call, audio output, DTMF action, transfer, or interaction. Fallback is allowed only when the platform can prove the operation is eligible and its externally visible effect is absent or safely governed.

---

# Provider Roles

A provider may occupy one or more roles, but each role is separately registered, evaluated, selected, and governed.

| Provider role | Examples | Bounded responsibility |
|---|---|---|
| Real-time media | LiveKit, WebRTC/media service, contact-center media bridge | Media resource setup, stream coordination, room/track/provider evidence. |
| Telephony / SIP | Twilio, carrier, SIP trunk, contact-center platform | PSTN/SIP ingress/egress, call-control, number/trunk/provider evidence. |
| Speech recognition | OpenAI, ElevenLabs, specialized STT provider | Audio-to-speech evidence through the Speech Pipeline contract. |
| Speech synthesis | ElevenLabs, OpenAI, specialized TTS provider | Approved text-to-audio preparation/output through the Speech Pipeline contract. |
| Recording/transcript support | Provider capture or storage integration | Controlled capture/reference support; not retention or access-policy ownership. |
| Routing/relay infrastructure | Approved provider relay/edge capability | Bounded transport assistance; not canonical Conversation routing. |

A provider name is never used as a proxy for a role, capability, trust level, compliance status, tenant entitlement, or future availability.

---

# Conceptual Architecture

~~~text
Voice Domain Contracts
    |
    +--> Provider Registry and Capability Catalog
    |
    +--> Tenant Provider Selection Profile
    |
    +--> Provider-Neutral Coordinator
             |
             +--> Media Adapter
             +--> Telephony / SIP Adapter
             +--> STT Adapter
             +--> TTS Adapter
             +--> Recording/Transcript Reference Adapter
             |
             v
       Provider SDKs, APIs, Webhooks, Resources, and Accounts
~~~

## Provider-Neutral Coordinator

The coordinator resolves an eligible provider profile for the current Voice operation, creates the immutable selection snapshot, invokes the bounded adapter, validates normalized results, applies duplicate-safe fallback rules, and emits Voice evidence.

The coordinator does not replace the lifecycle, media, speech, telephony, security, Conversation, or Agent owners. It composes their approved contracts for a provider operation.

## Provider Adapter

An adapter is the only component allowed to use a provider-specific SDK/API/webhook/protocol/resource. It maps provider requests and results to/from the corresponding Voice contract, validates provider input, contains retries and error mapping, and returns protected provider-evidence references.

An adapter may not directly call another platform's internal state store, invoke Agent tools, publish a canonical Conversation event, or expose a provider resource as a cross-platform authorization token.

---

# Provider Registry and Capability Catalog

## Registry Record

Every approved provider role/version has a registry record with:

- provider and adapter identity, version, owner, supported contract versions, and lifecycle state;
- provider role(s), capabilities, limitations, region/residency, language/voice/media/telephony support, and operational dependencies;
- security, privacy, data-processing, certification/contract, and credential-management references;
- quality, latency, availability, capacity, cost-unit, quota/billing, and operational support references;
- compatibility, deprecation, migration, rollback, change-control, test, and approval evidence; and
- incident, escalation, observability, and tenant eligibility references.

The registry stores provider-specific values as protected configuration or references. It must not expose credentials, full account details, or commercial terms to ordinary application consumers.

## Capability States

| State | Meaning |
|---|---|
| Proposed | Provider/role is under evaluation and cannot receive production operations. |
| Validating | Contract, security, tenant, quality, cost, operational, and test checks are in progress. |
| Active | Eligible for the approved role/tenant profiles. |
| Restricted | Eligible only for recorded capabilities, tenants, regions, operation types, or controlled rollout. |
| Degraded | Active with registered limitations or safe fallback requirements. |
| Deprecated | New use is limited or blocked; a migration path is recorded. |
| Suspended | No new operations because of incident, policy, security, capacity, or contractual condition. |
| Retired | No new operations; historical references remain governed. |

A provider may be Active for one role and Restricted/Suspended for another. Lifecycle state is evaluated with the tenant profile and current operation, not globally assumed.

---

# Provider Account Ownership and Lifecycle

A provider account is either platform-managed, tenant-owned, or a separately approved shared-service account. Account ownership is recorded explicitly and does not change the provider-neutral contract, tenant isolation, or operation authorization rules.

| Account model | Required controls |
|---|---|
| Platform-managed | Tenant-scoped configuration, least-privilege provider access, usage allocation, credential rotation, incident ownership, and controlled offboarding. |
| Tenant-owned | Verified tenant authorization, delegated/scoped credentials, account/resource binding, commercial/billing separation, revocation, and supported-operation limits. |
| Approved shared-service | Explicit tenant isolation, per-tenant resource/access controls, usage attribution, data boundary, operational ownership, and exit treatment. |

Account onboarding, credential rotation, scope change, suspension, revocation, billing/usage attribution, provider-account migration, and offboarding require current authorization, audit evidence, and a safe disposition for active operations. Client-owned credentials are never exposed to clients as Voice/Conversation tokens or shared across tenants; they remain Security-managed adapter inputs.

---
# Provider-Neutral Contract Rules

## Contract Ownership

The Voice Platform owns the semantic contract. Each specialized Voice document owns its related contract details:

| Contract family | Owner document |
|---|---|
| Channel capability, endpoint/resource eligibility | 02_VOICE_CHANNEL_MODEL.md |
| Call/session/leg lifecycle and outcome | 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md |
| Media resource, readiness, health, output transport | 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md |
| Recognition, synthesis, language/voice, speech outcome | 05_VOICE_SPEECH_PIPELINE.md |
| Activity, endpointing, barge-in, output interruption | 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md |
| PSTN/SIP endpoints, call control, DTMF, carrier outcome | 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md |
| Provider selection, adapter mapping, compatibility, fallback, migration | This document |

## Identifier Rules

Provider call IDs, room IDs, track IDs, model IDs, voice IDs, number inventory IDs, webhook event IDs, recording IDs, and account IDs remain adapter-local. Voice creates opaque Voice identifiers and protected mapping references. No provider identifier is a canonical Conversation ID, participant ID, tenant ID, session ID, public API token, or authorization credential.

## Compatibility and Change

Additive adapter changes are preferred. A new required field, semantic/type change, changed delivery/cancellation meaning, altered security/data handling, provider model/voice behavior, cost unit, or removed capability requires compatibility assessment, versioned registry/profile change, rollout plan, test evidence, and migration/rollback path.

A provider update must not silently reinterpret active Voice evidence or change a canonical Conversation/Agent contract without the affected owners' approval.

---

# Tenant Provider Selection

## Tenant Provider Profile

A tenant provider profile identifies which approved provider roles, adapters, versions, capabilities, regions, data-processing conditions, quality/latency classes, cost/quota limits, fallback orders, and operational restrictions may serve that tenant/environment/channel/operation.

A profile is not a provider credential, a participant authorization grant, or a promise that a provider is currently healthy. It is resolved with current registry, channel, policy, lifecycle, capability, and operational evidence for every operation.

## Profile Composition and Precedence

Provider selection uses composable profiles with one authoritative order. No role-specific profile may expand the eligible-provider boundary established above it.

1. Enterprise/Security policy establishes non-overridable legal, contract, residency, data-processing, credential, and tenant-isolation restrictions.
2. The generic tenant provider profile defines the providers, roles, account model, regions, commercial boundaries, and broad quality/latency/cost/fallback eligibility for the tenant/environment.
3. Channel configuration and capability profile narrow eligibility to the current endpoint, media, regional, accessibility, and operational constraints.
4. The role-specific profile makes the choice within that eligible boundary: the Speech Pipeline's tenant speech profile selects STT/TTS model/voice behavior; Telephony's route/failover policy selects an eligible endpoint/carrier route; Media and Turn-Taking profiles select eligible transport and interaction behavior.
5. The current operation snapshot validates lifecycle, participant/delivery binding, purpose, cancellation, capacity/health, idempotency, and any current restriction before invocation.

A conflict resolves to the most restrictive valid setting. If no provider remains eligible, Voice returns an explicit unavailable, deferred, restricted, denied, or uncertain outcome. It never invents a default provider or silently weakens a higher-precedence rule.

## Cross-Provider Dependency Map

An operation using more than one provider records a compatibility set: the selected roles/adapters/versions, region/data-flow relationship, media and codec compatibility, language/voice/model compatibility, latency class, security/data-processing constraints, supported fallback combinations, and known limitations.

For example, a real-time media provider, STT provider, TTS provider, and telephony route may each be individually eligible but incompatible together for a specific tenant, region, language, or latency class. The Provider Coordinator must validate the whole set before the operation begins. It must not substitute one role independently when doing so violates the recorded compatibility set or creates an unsafe visible effect.
## Selection Order

Provider selection applies the following order:

1. non-overridable security, legal, consent, residency, contract, and tenant-isolation requirements;
2. required Voice role, channel/media/telephony/speech capability, and operation compatibility;
3. current lifecycle, participant/delivery binding, operation policy, accessibility, and Conversation-approved request constraints;
4. tenant-approved quality and latency class, reliability/availability, and capacity restrictions;
5. tenant cost, quota, budget, preferred-provider, and operational routing preferences.

The lowest-cost provider is selected only among profiles satisfying all prior constraints. An unknown, stale, unsupported, or ineligible profile yields a governed unavailable/deferred/denied outcome; it never falls back to an arbitrary provider.

## Selection Snapshot

Each accepted provider operation records provider role, adapter/registry version, tenant profile/version, capability/configuration/policy references, selected route/model/voice/resource category, quality/latency class, cost/quota reference, fallback policy reference, correlation/idempotency/trace, and effective time.

The snapshot is immutable. Later provider/profile changes apply only to new work unless a documented migration handles an active resource safely.

---

# Provider Fallback and Failover

## Eligibility

Fallback can occur only if the alternate provider is independently active/eligible for the same tenant, role, operation, data/residency, capability, quality/latency, caller/endpoint, and policy constraints.

## Operation Classes

| Operation class | Default fallback posture |
|---|---|
| Stateless pre-operation validation or capability lookup | Bounded retry/fallback may be permitted with idempotency and current profile checks. |
| Inbound provider event/callback | Validate/deduplicate the source; never resubmit or fabricate an event through another provider. |
| Media/session establishment before visible connection | Alternate establishment may be permitted if no external connection/output occurred and correlation is controlled. |
| Speech recognition before final candidate submission | Bounded fallback may be permitted only with approved media/data policy and duplicate suppression. |
| Synthesized output not yet sent | Alternate preparation may be permitted if the delivery/cancellation snapshot remains current. |
| Visible call, audio output, DTMF, transfer, conference, or caller-ID operation | Do not replay/fail over automatically unless evidence proves no visible effect and policy explicitly allows it. |
| Recording/transcript reference | Use governed capture/reconciliation rules; never duplicate or expose protected content by default. |

## Uncertain Outcome

If the provider's externally visible outcome is uncertain, Voice records `OutcomeUncertain`, retains protected evidence, prevents unsafe retry/failover, and invokes the relevant lifecycle/reconciliation procedure. Cost or availability pressure never overrides this rule.

---

# Migration, Rollout, and Provider Exit

## Migration Principles

Provider migration is versioned and staged. It identifies source/destination adapter/profile, affected roles/tenants/channels, data and credential treatment, contract/capability differences, active-resource handling, acceptance criteria, rollout, monitoring, rollback, communication, and audit.

An active call, media resource, synthesis output, recognition sequence, transfer, or recording reference is not silently moved to a new provider. The migration either preserves the original provider for the bounded operation, uses a separately admitted replacement operation, or applies a documented safe termination/reconciliation path.

## Controlled Rollout

New adapters, models, voices, routes, or provider versions begin in Proposed/Validating or Restricted state. Activation uses approved test evidence, a controlled tenant/environment cohort, metrics/alerts, error/cost/quality monitoring, rollback readiness, and owner approval before expansion.

## Data Portability and Provider Exit

Provider exit includes a governed portability assessment for provider-held resources and references. The assessment identifies which metadata, configuration, recordings/transcripts, media references, usage records, call/resource mappings, and audit evidence can be exported, transferred, retained, deleted, or rendered unavailable under current contract, data, retention, security, and tenant policy.

Portability does not authorize unrestricted data extraction. It uses approved Data/Security access, classification, retention, residency, and audit controls. Historical provider mappings remain protected evidence where required, even when the provider is no longer eligible for new work.
## Provider Exit

Deprecation or exit prevents new selection, communicates the replacement/fallback condition to affected owners, migrates configuration and eligible resources safely, revokes credentials/resources as applicable, retains governed historical mappings, and verifies no stale provider reference remains eligible.

---

# Security, Privacy, and Tenant Isolation

Every provider operation is tenant-, environment-, role-, adapter-, capability-, resource-, purpose-, classification-, and policy-scoped.

- Provider API keys, tokens, signing material, account identifiers, callbacks, webhooks, and resource handles are Security-owned and adapter-bounded. They are never client-held Voice/Conversation credentials.
- Adapters validate provider source, signature/authentication, freshness, replay, schema/version, tenant/resource binding, and operation correlation before creating Voice evidence.
- Providers receive the minimum approved audio, text, metadata, endpoint, and operation data. Data minimization, redaction, residency, retention, and access constraints are resolved before provider use and recorded by reference.
- Provider logs, metrics, support exports, caches, prompts, transcripts, recordings, media, and diagnostics are protected according to tenant classification and approved data policy.
- A provider cannot correlate tenants or operations through shared identifiers, caches, connection pools, error reporting, or observability dimensions.
- A provider security incident, contract change, credential compromise, or compliance restriction suspends/restricts affected roles and triggers the documented safe operation/fallback/reconciliation path.

---

# Cost, Usage, and Operational Controls

Provider cost is an operational selection input, not a participant-facing authority. The relevant profile records supported cost units, usage-meter reference, quota/budget policy reference, capacity/rate restrictions, alerts, and permitted action when a threshold is approached or exceeded.

Usage is correlated with the tenant, approved operation, provider role, profile/version, and protected cost/usage reference. Ordinary Voice events expose normalized usage/cost categories only; detailed commercial data is restricted to authorized billing/operations paths.

A quota, budget, or rate condition produces a configured deferment, safe fallback, restricted capability, or unavailable outcome. It may not silently lower compliance, language/accessibility, quality/latency class, caller identity, or participant-delivery requirements.

---

# Observability and Audit

Provider telemetry records provider role/category, adapter/registry/profile version, capability state, operation selection/fallback/migration, eligibility/rejection reason category, quality/latency/capacity/cost category, provider error/outcome, retry/reconciliation, correlation, and terminal result.

Required measures include provider availability, selection distribution, operation latency, fallback rate/success, duplicate-suppression, provider error, uncertain outcome, capability mismatch, quality degradation, quota/capacity pressure, cost/usage variance, migration/rollout health, callback validation failure, and tenant-safe performance by authorized aggregate dimensions.

Audit records registry/profile creation/change/activation/restriction/suspension/deprecation, provider selection, high-risk override, credential/contract/security change reference, migration/rollback, incident action, and terminal reconciliation with principal/service, scope, reason, evidence, correlation, and outcome.

---

# Testing Strategy

## Contract and Adapter Tests

Validate provider-neutral contracts, identifier containment, capability mapping, required fields, event/error normalization, ordering/idempotency, version compatibility, protected-reference handling, and prohibited cross-platform writes for each adapter.

## Adapter Conformance Suite

Every provider adapter must pass the same versioned conformance suite before it can enter Validating or Active state. The suite validates provider-neutral request/result mapping; identifier and credential containment; source validation; tenant/resource/profile scope; ordering and idempotency; error/outcome normalization; data minimization/redaction; quality/latency/capacity reporting; fallback/uncertain-outcome behavior; migration/rollback; observability; and prohibited cross-platform writes.

The suite includes deterministic simulated provider cases and controlled integration/sandbox cases. A provider-specific feature may be exposed only as a documented optional capability; it cannot alter required contract semantics or weaken the conformance baseline.
## Selection, Fallback, and Migration Tests

Validate tenant profile selection order, compliance/capability/quality/latency/cost gates, quota restriction, ineligible provider rejection, duplicate-safe fallback, uncertain outcome handling, canary rollout, provider version change, migration, rollback, and provider exit.

## Security, Privacy, and Resilience Tests

Simulate forged/replayed provider callbacks, wrong tenant/resource/profile, stale credentials/configuration, malformed provider payload, provider data leak, rate limit, outage, partial response, changed capability, provider incident, duplicate/out-of-order events, visible-operation failover race, and recovery. Prove no test creates canonical Conversation state, exposes protected data, bypasses current policy, or duplicates participant-facing output/call control.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Provider registry and lifecycle catalog | Defines provider roles, adapter/version, capability, data/security, quality/latency/cost, lifecycle, compatibility, owner, and approval evidence | Voice Platform with Security and Operations owners |
| Provider account ownership policy | Defines platform-managed, tenant-owned, and shared-service account onboarding, isolation, credentials, usage, rotation, revocation, billing attribution, and offboarding | Voice Platform with Security, Operations, and Billing owners |
| Provider adapter contract standard | Defines adapter boundary, request/result mapping, identifier/credential containment, callback validation, errors, retry, and compatibility | Voice Platform with Integration owner |
| Adapter conformance suite | Defines mandatory simulated and sandbox validation for contract, security, privacy, ordering, failure, observability, migration, and rollback behavior | Voice Platform with Testing, Security, and Operations owners |
| Tenant provider profile | Defines eligible providers/roles, compliance/capability/quality/latency/cost/quota/fallback controls, scope, and versioning | Voice Platform with Security, Operations, and tenant owners |
| Provider profile composition policy | Defines the precedence and safe composition of Security, tenant, channel, speech, telephony, media, and operation-specific provider constraints | Voice Platform with Channel, Speech, Telephony, Conversation, and Security owners |
| Cross-provider compatibility map | Defines permitted provider-role combinations, region/data-flow, codec/language/latency compatibility, fallback combinations, and limitations | Voice Platform with Operations and Security owners |
| Provider selection and snapshot contract | Defines selection precedence, immutable operation evidence, rejection, correlation, and downstream visibility | Voice Platform with Conversation, Channel, and Security owners |
| Fallback and uncertain-outcome policy | Defines operation classes, alternate eligibility, duplicate prevention, reconciliation, and participant-facing safeguards | Voice Platform with Operations, Conversation, and Security owners |
| Provider migration and rollout procedure | Defines validation, controlled cohort, metrics, active-resource handling, rollback, exit, communication, and audit | Voice Platform with Operations, Security, and Testing owners |
| Provider cost/usage control policy | Defines metering references, quota/budget/capacity behavior, cost visibility, alerts, and safe restriction/fallback | Voice Platform with Operations and Billing owners |
| Provider observability and test suite | Defines metrics, audit, adapter/selection/security/resilience/migration evidence | Voice Platform with Observability and Testing owners |

---

# Anti-Patterns

## Provider Identifier Is a Platform Identifier

A provider call, room, track, model, voice, account, or event ID is adapter-local evidence. It cannot become canonical Conversation/participant/tenant identity or a public credential.

## Provider Callback Writes Conversation State

A provider callback is validated Voice evidence. Conversation Platform decides any canonical state, participant, routing, handoff, or event consequence.

## Cheapest Provider Wins Unconditionally

Cost is considered only after compliance, capability, policy, quality, latency, reliability, and current-operation requirements are satisfied.

## Provider Timeout Is Safe to Retry

A timeout can leave externally visible effect uncertain. Reconcile before retrying calls, output, DTMF, transfer, conference, or other participant-visible work.

## Adapter Owns Business Policy

Adapters translate provider behavior; they cannot select a participant, authorize delivery, choose an agent, or decide business workflow.

## Active Work Silently Migrates

An active Voice resource continues under its original bounded provider or follows a separately controlled replacement/termination path. It is never silently reinterpreted under a new provider.

## Provider Availability Overrides Security

A convenient or available provider may not receive data or work outside its current tenant, security, residency, consent, and contract eligibility.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 01_VOICE_PLATFORM_ARCHITECTURE.md | Defines high-level provider-neutral Voice architecture. |
| 02_VOICE_CHANNEL_MODEL.md | Defines channels, capabilities, and endpoint configuration. |
| 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md | Defines lifecycle, correlation, timing, and terminal outcomes. |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | Defines media resources and transport behavior. |
| 05_VOICE_SPEECH_PIPELINE.md | Defines STT/TTS, tenant speech profiles, quality, and cost selection. |
| 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md | Defines activity/interruption contracts. |
| 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md | Defines telephony/SIP resource and carrier behavior. |
| 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md | Defines recording/transcript governance. |
| 12_VOICE_RELIABILITY_AND_FAILURE_HANDLING.md | Defines Voice-domain operational recovery. |
| 03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md | Defines canonical Conversation event semantics. |
| 09_SECURITY_PLATFORM | Owns enterprise policy, secrets, identity, compliance, and security monitoring. |
| 07_INTEGRATION_PLATFORM | Owns generic connector and external-business integration implementation. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created provider-neutral Voice Provider Abstraction covering registry, adapters, tenant selection, quality/cost controls, fallback, migration, security, and governance boundaries. |
| 1.1 | 2026-08-06 | Finalized profile precedence, provider accounts, cross-provider compatibility, portability, and adapter conformance requirements. |
| 1.2 | 2026-08-06 | Finalized after review for completeness, ownership overlap, long-term maintainability, and Platform Foundation/Digital Channel boundaries. |

