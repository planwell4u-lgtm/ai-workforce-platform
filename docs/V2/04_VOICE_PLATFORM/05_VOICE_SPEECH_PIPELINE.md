# 05_VOICE_SPEECH_PIPELINE

**Version:** 1.2  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document defines the provider-neutral speech pipeline for the Voice Platform. The pipeline transforms approved inbound audio into bounded speech evidence and transforms approved outbound delivery content into bounded synthesized audio.

Speech recognition and synthesis are Voice capabilities. They do not own canonical conversation interactions, participant identity, agent reasoning, response content, routing, handoff, consent policy, or durable recording/transcript storage.

---

# Purpose

The Speech Pipeline provides a stable, auditable boundary for speech-to-text (STT), text-to-speech (TTS), language handling, confidence, partial/final results, output synthesis, and speech-provider recovery.

It allows providers and models to evolve without exposing provider-specific payloads, model identifiers, or transcript semantics to Conversation or Agent Platform.

---

# Objectives

The Speech Pipeline must:

- Convert approved inbound Voice media into normalized speech evidence with source, timing, language, confidence, and finality metadata.
- Convert only approved Voice delivery content into synthesized output suitable for the current media resource and channel capability.
- Keep partial, final, corrected, unavailable, and uncertain speech outcomes distinct.
- Support configured language, locale, voice, acoustic, accessibility, and channel constraints without treating a capability as authorization.
- Keep STT/TTS providers, model choices, resource identifiers, and error conventions behind replaceable adapters.
- Respect tenant, environment, policy, consent, classification, and recording/transcript constraints throughout speech processing.
- Handle latency, cancellation, interruption, provider failure, replay, and out-of-order results without duplicate or stale participant-facing effects.
- Emit versioned, provider-neutral speech facts and protected references for downstream owners.

---

# Scope

This document defines speech concepts, pipeline components, input/output contracts, result finality, language and voice selection, quality/confidence treatment, lifecycle/recovery, security/privacy, observability, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Voice call/session/leg lifecycle, terminal outcomes, timing, and transition authority | 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md |
| Media resource/signaling lifecycle, buffering, readiness, and transport quality | 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md |
| Canonical conversation interaction meaning, participant association, state, context, routing, handoff, or events | 03_CONVERSATION_PLATFORM |
| Agent instructions, reasoning, tool use, response content, or execution lifecycle | 02_AGENT_PLATFORM |
| Turn ownership, voice activity, barge-in policy, interruption decision, and response cancellation semantics | 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md |
| PSTN/SIP DTMF, carrier controls, and telephony-specific behavior | 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md |
| Provider selection, provider model configuration, or adapter internals | 08_VOICE_PROVIDER_ABSTRACTION.md |
| Durable recording/transcript storage, retention, deletion, or legal-hold execution | 08_DATA_PLATFORM and 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md |
| Enterprise identity, authorization, consent policy, secrets, compliance controls, or security monitoring | 09_SECURITY_PLATFORM |

---

# Platform Foundation and Digital Channel Boundaries

Platform Foundation supplies tenant, membership, entitlement, shared configuration, and API-edge facts used to select an eligible speech profile. Voice applies those facts to speech operations; it does not own their control-plane lifecycle.

Digital Channel Platform owns non-voice delivery. Speech output is prepared only for an approved Voice delivery request and cannot be reused as a messaging, email, web-chat, or other digital-channel payload without a new approved channel operation.

---

# Architecture Principles

## Speech Evidence Is Not Canonical Interaction State

A recognition result is provider-normalized Voice evidence. Conversation Platform decides whether and how a final speech result becomes a canonical interaction associated with a participant, conversation, session, or event.

## Synthesis Is Not Response Authorization

TTS may prepare audio only from an approved Voice delivery request. It cannot create response content, select a recipient, choose a channel, or send output merely because a call/media resource is active.

## Partial Is Provisional

Partial recognition is volatile and may be revised or withdrawn. It is never a durable transcript, a canonical interaction, a tool input, or a basis for irreversible action unless another approved contract explicitly permits a bounded use.

## Confidence Is Evidence, Not Truth

Confidence, language identification, diarization, and model metadata describe the speech pipeline's assessment. They do not prove participant identity, intent, authorization, consent, business fact, or successful understanding.

## Speech Provider Details Are Contained

Provider model names, endpoint IDs, raw hypotheses, acoustic artifacts, token timestamps, proprietary scores, voice IDs, and SDK formats remain adapter-local. Downstream contracts use normalized categories, opaque references, and versioned semantics.

---

# Conceptual Architecture

~~~text
Inbound Approved Media
    -> Speech Recognition Adapter
    -> Recognition Coordinator
    -> Normalized Speech Evidence
    -> Conversation Interaction Boundary

Approved Voice Delivery Request
    -> Synthesis Coordinator
    -> Speech Synthesis Adapter
    -> Bounded Output Audio
    -> Approved Media Resource
~~~

## Recognition Coordinator

The coordinator accepts approved inbound media references, verifies current resource/policy/capture conditions, selects an eligible configured recognition capability, correlates results to the Voice resource, normalizes finality and errors, and submits speech evidence to the Voice-to-Conversation boundary.

It does not decide whether text is a canonical interaction, whether an agent should respond, or whether another party may see the result.

## Synthesis Coordinator

The coordinator accepts an approved Voice delivery request, resolves the eligible voice/language/output profile, prepares bounded synthesis work, streams or buffers output according to Media and Turn-Taking constraints, and reports delivery-related speech facts.

It does not author content or override delivery cancellation, channel eligibility, participant preferences, accessibility needs, policy, or Conversation ownership.

## Provider Adapters

Adapters map provider requests, streams, events, errors, model/voice capability, and output resources to the provider-neutral contracts. They hold provider credentials and identifiers behind approved security boundaries and never expose them as canonical IDs or client-held authority.

---

# Core Speech Concepts

## Recognition Segment

A recognition segment is a bounded sequence of speech evidence associated with a specific Voice media resource and time range. It may contain one or more partial revisions and at most one accepted final result for a given recognition sequence.

## Partial Result

A partial result is an incomplete, mutable hypothesis. It includes a sequence and revision reference, observed range, normalized language/confidence evidence where available, and protected content/reference. A newer partial may replace it; it may never be silently converted into a final result.

## Final Result

A final result is the recognition pipeline's terminal result for a bounded sequence. It includes finality, timing, language, normalized confidence/quality category, provenance, content or protected content reference, and the finalization reason. Final only means recognition processing has concluded; it does not mean the content is true, permitted, or canonically accepted.

## Speaker Attribution and Diarization

Where a provider supports diarization, speaker labels, channel direction, or voiceprint-like evidence, Voice records them only as bounded speech evidence with quality and provenance. A label such as `speaker-1`, a detected voice characteristic, or a channel/media position is not participant identity, role, consent, authorization, or a canonical participant association.

Conversation Platform alone resolves any canonical participant relationship through its approved identity, presence, visibility, and policy controls. Voice must report ambiguous, unavailable, or low-quality attribution explicitly rather than assigning a person or carrying an attribution to another channel.
## Synthesis Request

A synthesis request is a bounded Voice operation derived from an approved Voice delivery request. It identifies the authorized content/reference, target language/voice requirements, media/output constraints, correlation, idempotency, cancellation conditions, and current configuration snapshot.

## Synthesis Output

A synthesis output is a Voice-domain result such as prepared, started, completed, interrupted, suppressed, failed, or uncertain. It may reference generated audio only through a protected, governed media/recording reference.

---

# Recognition Pipeline

## Admission and Input Guard

Recognition begins only when all of the following are true:

- the associated Voice call/leg and inbound media resource are in an eligible current state;
- the channel configuration and capability profile support the requested recognition operation;
- capture, language, classification, consent/recording, tenant/environment, and policy requirements have been verified for this operation;
- the adapter/provider contract and resource binding are current; and
- the recognition sequence is correlated and protected against duplicate/replayed input.

Failure of any guard produces a governed unavailable, denied, deferred, failed, or uncertain result. Voice must not invent transcript content, reuse a stale resource, or silently broaden capture scope.

## Result Finality and Revision Rules

| Result type | Permitted use | Prohibited use |
|---|---|---|
| Partial | Time-bounded Voice/turn-taking coordination where policy permits; authorized UX feedback through the owning channel/UI boundary. | Canonical interaction, tool input, durable transcript, irreversible action, or unreviewed cross-channel sharing. |
| Final | Candidate submission to Conversation Platform with provenance and policy references. | Automatic truth claim, identity proof, authorization decision, or uncontrolled publication. |
| Corrected final | A separately versioned correction with cause and supersession reference where an adapter produces one. | Silent mutation of a previously emitted final result. |
| Unavailable/failed | Explicit fallback, deferment, or safe no-input outcome. | Substitution with guessed text or unsupported default language. |

A final result is immutable. A later provider correction creates a new, explicitly related corrected-final result; Conversation Platform decides whether it has any canonical effect.

## Recognition Sequence State

~~~text
Requested -> Preparing -> Listening -> Partial* -> Finalized
                                     |              |
                                     v              v
                                  Failed / Cancelled / Uncertain
~~~

`Partial*` represents zero or more mutable partial revisions. The sequence is terminal after Finalized, Failed, Cancelled, or Uncertain. A new segment requires a new recognition sequence and idempotency reference.

---

# Synthesis Pipeline

## Synthesis Admission and Output Guard

Synthesis begins only from a current approved Voice delivery request. Voice verifies target media readiness, output direction, channel capability, configured voice/language profile, policy/consent and classification constraints, current cancellation state, idempotency, and operation correlation.

A provider's ability to synthesize content or an active media path is not permission to send it. If required conditions are not met, Voice suppresses, defers, or reports the operation without producing participant-facing output.

## Output State

| State | Meaning |
|---|---|
| Requested | Approved delivery has requested bounded synthesis; output is not yet prepared. |
| Preparing | Voice is resolving eligible language/voice/capability and requesting synthesis. |
| Prepared | Output is available for the approved media operation but has not started delivery. |
| Streaming | Approved audio is actively sent through the current media resource. |
| Interrupted | Output was stopped by a valid interruption, cancellation, disconnect, or safety/policy condition. |
| Completed | Synthesis/output finished with transport-level completion evidence. |
| Suppressed | Voice correctly prevented output before delivery. |
| Failed | Synthesis or required output processing failed. |
| Uncertain | Voice cannot safely determine the externally visible output result. |

Prepared output is transient and purpose-bound. It is invalidated when its approved delivery request expires, is cancelled, loses turn ownership, changes recipient/channel binding, or becomes policy-ineligible.

## Streaming and Cancellation

Speech output must honor the Media flow-control rules and the next Turn-Taking model. A valid cancellation or interruption stops/suppresses output as quickly as the active resource permits and records whether audible output may have occurred.

Voice never replays synthesized output after reconnect or provider retry unless the current delivery request, idempotency, recipient binding, cancellation state, and operation policy explicitly allow it.

---

# Language, Locale, and Voice Selection

Language identification and selection use the current channel capability profile and approved operation configuration. They are recorded as evidence, not as assumptions about a participant.

| Decision | Rule |
|---|---|
| Inbound language detection | May provide a candidate language/locale and confidence category; ambiguity produces an explicit ambiguous/unsupported outcome or approved clarification path. |
| Recognition language selection | Use configured/approved language constraints and current evidence. Do not silently switch to a language that violates policy or capability. |
| Outbound language selection | Conversation/Agent-approved delivery content and current participant/channel policy determine the requested language; Voice checks technical support. |
| Voice selection | Use a tenant-approved, language-compatible, accessibility-compatible voice profile. A voice ID is provider-local and not a participant identity/persona authority. |
| Unsupported language/voice | Return governed unavailable/degraded outcome with capability evidence; do not substitute a materially different language/voice without approval. |

Accent, dialect, code switching, speech impairment, background noise, and low-quality audio may reduce recognition quality. The pipeline reports normalized evidence and follows approved fallback/clarification behavior; it does not infer participant intent or capability from those conditions.

---

# Speech Service Selection, Quality, and Cost

Each tenant may use one or more approved recognition and synthesis providers/models, including client-selected services where Security, procurement, capability, and operational requirements permit. Provider/model selection is resolved from a versioned tenant speech profile; it is never inferred from a provider default or silently changed during an active participant interaction.

## Eligibility Order

Voice selects only from profiles that satisfy, in this order:

1. tenant/environment scope and current authorization;
2. legal, residency, privacy, retention, consent, and contractual requirements;
3. required language, accessibility, channel, media, and operational capabilities;
4. configured quality and latency class for the operation; and
5. cost, quota, budget, and capacity preferences among the remaining eligible profiles.

The lowest-cost profile may be selected only when it meets all higher-priority constraints. A provider outage, quota limit, or budget threshold produces an explicit fallback, deferment, suppression, or unavailable outcome. Voice never silently downgrades a live interaction to a materially lower quality, less compliant, or unsupported provider/model.

## Tenant Speech Profile

A tenant speech profile records approved provider/model references, supported languages/locales, voice profiles, quality/latency class, eligible channel/media capabilities, cost unit and usage-meter reference, quota/budget policy reference, data-processing/residency controls, fallback order, operational owner, and version/effective-time information.

The profile contains references to protected provider credentials and commercial terms; it does not expose credentials, account identifiers, or sensitive pricing details in routine telemetry or events.

## Evaluation and Release Criteria

Before a profile is activated or materially changed, the responsible owners evaluate it with a versioned, policy-approved test set representative of the supported language, accent/dialect, acoustic, accessibility, channel, and business-domain conditions. Evaluation records the applicable recognition accuracy/semantic-correctness measures, finalization and correction behavior, synthesis intelligibility/naturalness measures, interruption behavior, latency, availability, cost/usage, safety/privacy constraints, and known limitations.

No single score is universally sufficient. The tenant's approved quality/latency class and risk context determine acceptance. Release evidence must include comparison to the replaced profile where applicable, rollback readiness, and an approval record.

---
# Quality, Confidence, and Accessibility

## Normalized Quality Evidence

Recognition and synthesis report normalized quality categories such as adequate, degraded, unavailable, ambiguous, unsupported, and uncertain, with protected provider evidence references where needed. Configuration defines thresholds and approved mitigation for the applicable channel, language, tenant, and use case.

## Confidence Handling

Confidence is normalized into configured categories and supplied with the recognition result where available. A low-confidence final result is not discarded silently; it is marked and made available to Conversation/Agent/Turn-Taking owners through approved contracts for safe clarification, escalation, or no-action behavior.

No fixed confidence threshold in this document authorizes a business action, proves a fact, or determines a canonical conversation transition. Those decisions require the owning platform's current policy and context.

## Accessibility

Voice speech capabilities must describe supported languages, voice styles, speech rate, volume, relay/assistive paths, transcript/caption availability, DTMF-only fallback where applicable, and known constraints. Accessibility selection and user experience remain owned by Frontend/Channel and policy owners; the speech pipeline exposes capability and outcome evidence.

---

# Speech Evidence Contract

Speech events describe speech-processing facts: recognition hypotheses/finality and synthesis preparation/output generation. They correlate with, but do not replace, the media events in `04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md`.

- A `speech.output.started` event means synthesis has begun producing output for the approved media operation.
- A media `output.started` event means the media layer has evidence that output transport began.
- A `speech.output.stopped` event describes synthesis completion, interruption, suppression, or failure.
- A media `output.stopped` event describes the transport-level stop/outcome.

Neither event independently proves participant receipt, comprehension, or business completion. Implementations must preserve correlation and causal references between the two event families and must not emit one as a duplicate substitute for the other.
All speech evidence extends the versioned Voice lifecycle-evidence contract and contains common tenant/environment, Voice resource, configuration/capability snapshot, correlation, causation, idempotency, trace, timing, and protected provider-evidence references.

| Event type | Required speech-specific evidence |
|---|---|
| `speech.recognition.requested` | Recognition sequence, input media reference, requested language/capability profile, capture purpose. |
| `speech.partial` | Sequence/revision, time range, normalized language/confidence/quality categories, protected content reference. |
| `speech.final` | Sequence, finalization reason, time range, language, confidence/quality, content or protected content reference. |
| `speech.final.corrected` | New final result, superseded-final reference, correction cause, provider evidence reference. |
| `speech.recognition.failed` | Error category, retry/fallback eligibility, last trustworthy state, and no-content assertion. |
| `speech.synthesis.requested` | Approved delivery reference, requested language/voice/output profile, cancellation/idempotency snapshot. |
| `speech.synthesis.prepared` | Prepared-output reference, effective profile, expiry/cancellation binding, media compatibility result. |
| `speech.output.started` | Delivery reference, effective output profile, target media resource, and start evidence. |
| `speech.output.stopped` | Completion/interruption/suppression/failure reason and externally visible outcome certainty. |

Speech events contain references and normalized categories instead of raw audio, credentials, provider-local identifiers, unrestricted participant data, or broad transcript content.

---

# Reliability, Recovery, and Failure Handling

## Speech Operational Profile

Every active tenant speech profile defines an approved operational class for recognition and synthesis. The class sets release-specific targets and alert thresholds for time to first partial where enabled, time to final, time to prepared output, time to first synthesized output, cancellation stop, provider error, quality degradation, fallback, and cost/usage variance.

The profile also defines bounded queue/buffer behavior, overload handling, retry limits, failover eligibility, and the safe disposition when targets cannot be met. Media Architecture owns transport buffering and delivery flow control; this profile owns the speech-stage targets and selection/failover conditions that feed those controls.
Speech behavior assumes provider timeout, stream interruption, duplicate/reordered results, malformed output, model/capability change, unsupported language, partial-result loss, synthesis failure, cancellation race, and uncertain output delivery.

- Recognition retries use bounded, idempotent rules and must not duplicate canonical interaction candidates.
- A failed or lost partial is discarded or marked unavailable; it is not promoted to final.
- Synthesis retry is permitted only when externally visible output has not started or when current delivery/idempotency policy proves a retry is safe.
- Provider/model changes use versioned capability/configuration references and may not silently reinterpret a final result or active output.
- When external effect cannot be determined, Voice emits an uncertain outcome and requires controlled reconciliation rather than assuming success or failure.
- Speech recovery never revives a closed Conversation session or bypasses current delivery, policy, consent, or authorization checks.

---

# Security, Privacy, and Tenant Isolation

Each recognition and synthesis operation is tenant-, environment-, resource-, purpose-, classification-, configuration-, and policy-scoped. Speech providers receive only the minimum approved media/content and metadata required for the operation through approved adapters.

- Inbound audio, transcript content, partial hypotheses, DTMF, timestamps, provider model metadata, and synthesized audio are protected data subject to current policy.
- Partial results have short-lived, restricted access and are excluded from ordinary logging, analytics, handoff, and durable storage unless an approved policy/contract says otherwise.
- Final speech evidence does not grant broader access to raw audio or transcripts.
- Redaction is applied at the earliest policy-required stage: before provider submission where technically and operationally required; before durable transcript/recording storage; and before analytics, support, export, or broad observability access. The effective redaction stage, method, exceptions, and outcome are recorded by reference.
- If required pre-submission redaction cannot preserve the approved operation safely, Voice defers, suppresses, or routes to the configured controlled alternative; it does not send unapproved content to a speech provider.
- Provider credentials, model/voice identifiers, and generated-resource references are never logged as secrets or exposed as client-held authorization.
- Tenant isolation applies to model configuration, language/voice profiles, speech resources, caching, buffering, error reports, and observability.
- Recording/transcript retention, deletion, export, legal hold, and access requests remain governed by their Data/Security owners.

---

# Observability and Audit

Telemetry records recognition/synthesis request, preparation, latency category, language/voice capability category, partial/final/error count, confidence/quality category, cancellation/interruption, provider-adapter category, resource correlation, fallback, retry, and terminal/uncertain outcome.

Required measures include time to first partial where used, time to final, recognition availability, finalization/correction rate, low-confidence/ambiguous rate, language/voice unsupported rate, time to prepared output, time to first audible output, synthesis failure, interruption latency, retry/reconciliation rate, and quality by authorized aggregate dimensions.

Audit records configuration/profile changes, privileged language/voice/recording behavior, recognition/synthesis admission, exceptional fallback, correction, policy/security stop, and access to protected speech references. Routine telemetry excludes raw audio, broad transcript content, DTMF, credentials, and direct participant identifiers.

---

# Testing Strategy

## Contract and State Tests

Validate speech event schemas, finality/revision rules, required provenance, content-reference protections, language/voice compatibility, state transitions, idempotency, cancellation, and contract-version compatibility.

## Integration and Journey Tests

Validate approved inbound recognition, partial/final handling, final correction, Conversation candidate submission, approved outbound synthesis, output preparation/streaming, language/voice selection, accessibility capability, speaker-attribution safeguards, interruption, speech-versus-media event correlation, tenant profile selection, cost/quota fallback, and Voice media/lifecycle integration.

## Security and Resilience Tests

Simulate wrong tenant/resource, forged/replayed/out-of-order provider events, stale configuration, revoked consent, unauthorized capture/output, partial-to-final confusion, unsupported language, provider outage, malformed result, cancellation race, reconnect, and uncertain delivery. Prove that no test creates canonical Conversation state, exposes protected speech data, or delivers participant-facing output without the approved boundary.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Speech recognition contract | Defines recognition admission, segment/sequence, partial/final/corrected evidence, errors, provenance, and compatibility | Voice Platform with Conversation owner |
| Speech synthesis contract | Defines approved synthesis request, output preparation, streaming, cancellation, outcomes, and compatibility | Voice Platform with Conversation and Agent owners |
| Language and voice capability catalog | Defines supported languages/locales, voice profiles, accessibility constraints, quality limitations, and versioning | Voice Platform with Channel, Frontend, and Security owners |
| Tenant speech profile and selection policy | Defines approved provider/model eligibility, quality/latency class, cost/quota controls, fallback, commercial references, and versioning | Voice Platform with Security, Operations, and tenant owners |
| Speech evaluation and release framework | Defines representative test sets, quality/latency/cost measures, acceptance, comparison, approval, known limitations, and rollback evidence | Voice Platform with Testing, Operations, and Security owners |
| Speech provider adapter contract | Defines provider containment, capability mapping, protected references, retry, error normalization, and migration | Voice Platform with Integration owner |
| Speech privacy and retention controls | Defines protected content, partial-result handling, staged redaction, recording/transcript references, access, and lifecycle integration | Voice Platform with Security and Data owners |
| Speech operational profile | Defines speech-stage targets, queue/retry/failover limits, overload handling, and required outcome evidence | Voice Platform with Operations and Observability owners |
| Speech quality and fallback policy | Defines normalized quality/confidence categories, thresholds, clarification/fallback evidence, and observability | Voice Platform with Conversation, Operations, and Observability owners |
| Speech pipeline test suite | Validates contracts, journey, privacy, tenant isolation, performance, resilience, and provider-neutral behavior | Voice Platform with Testing owner |

---

# Anti-Patterns

## Partial Transcript Becomes a Tool Input

Partial recognition is provisional. It cannot trigger an irreversible action or become a canonical interaction without an explicit, approved contract.

## Final Transcript Means the Participant Meant It

A final recognition result is only the pipeline's completed output. Intent, identity, authorization, and business truth require their own validation.

## TTS Sends Whatever the Agent Produces

Voice synthesizes and delivers only content from a current approved delivery request. Active media is not delivery authorization.

## Confidence Threshold Becomes Business Policy

Confidence is evidence for safe clarification or handling; it cannot replace current policy, context, confirmation, or authorization.

## Provider Voice or Model ID Escapes the Adapter

Provider-specific identifiers, payloads, and credentials must remain bounded. Other modules consume normalized capability and outcome contracts.

## Raw Speech Data in General Logs

Raw audio, partial hypotheses, full transcripts, DTMF, and secrets are not routine telemetry or debugging material.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 01_VOICE_PLATFORM_ARCHITECTURE.md | Defines high-level Voice architecture and provider-neutral boundaries. |
| 02_VOICE_CHANNEL_MODEL.md | Defines Voice channel configuration and capabilities. |
| 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md | Defines call/session/leg lifecycle, state authority, timing, and outcomes. |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | Defines signaling, media resources, readiness, buffering, recovery, and media events. |
| 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md | Defines VAD, turn ownership, barge-in, and response cancellation. |
| 08_VOICE_PROVIDER_ABSTRACTION.md | Defines provider implementation boundaries and replaceability. |
| 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md | Defines recording/transcript governance and controlled references. |
| 03_CONVERSATION_PLATFORM/03_CONVERSATION_MODEL.md | Defines canonical interaction and participant concepts. |
| 03_CONVERSATION_PLATFORM/05_CONVERSATION_CONTEXT_MODEL.md | Defines bounded context and content-reference controls. |
| 03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md | Defines canonical Conversation event semantics. |
| 02_AGENT_PLATFORM/12_AGENT_INSTRUCTION_SYSTEM.md | Defines agent instruction ownership. |
| 02_AGENT_PLATFORM/13_AGENT_PERSONA_AND_BEHAVIOR_MODEL.md | Defines agent persona ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created provider-neutral Speech Pipeline architecture covering STT, TTS, finality, language/voice capability, evidence, privacy, and recovery boundaries. |
| 1.1 | 2026-08-06 | Finalized provider/cost selection, evaluation, speaker-attribution, redaction, operational-profile, and speech/media event-boundary rules. |
| 1.2 | 2026-08-06 | Finalized after review for completeness, ownership overlap, long-term maintainability, and Platform Foundation/Digital Channel boundaries. |

