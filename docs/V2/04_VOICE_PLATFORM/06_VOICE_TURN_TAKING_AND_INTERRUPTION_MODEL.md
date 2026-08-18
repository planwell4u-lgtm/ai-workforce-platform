# 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL

**Version:** 1.2  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document defines how the Voice Platform detects and coordinates speaking activity, silence, barge-in, output interruption, and Voice-domain turn signals.

Voice may determine that media evidence indicates speech has started, ended, overlapped, or become uncertain. It does not determine canonical conversation turn ownership, participant intent, accountable agent/human ownership, response content, or whether agent execution and external work should continue.

---

# Purpose

The Turn-Taking and Interruption Model provides a provider-neutral, low-latency control boundary between real-time Voice media and the Conversation/Agent platforms. It prevents stale or overlapping output, unsafe automatic resumption, duplicate responses, and provider-specific VAD or interruption behavior from becoming canonical state.

---

# Objectives

The model must:

- Normalize Voice activity, silence, overlap, interruption, and output-control evidence across Voice providers and media transports.
- Coordinate bounded capture and output stop/start behavior within the current Voice media lifecycle.
- Preserve Conversation Platform ownership of canonical response-turn and handoff state.
- Preserve Agent Platform ownership of reasoning, execution, tool-work, and execution cancellation.
- Support configurable VAD, endpointing, barge-in, push-to-talk, DTMF fallback, and accessibility constraints without treating detection as intent or authorization.
- Prevent stale, duplicate, or conflicting participant-facing audio under reconnect, cancellation, handoff, policy, or provider-event races.
- Emit versioned, tenant-scoped turn/interruption evidence with correlation and privacy controls.

---

# Scope

This document defines Voice turn concepts, activity signals, state and authority, interruption control, output gating, multi-party behavior, race/recovery handling, security/privacy, observability, testing, and required implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Canonical conversation turns, work ownership, routing, handoff, participant visibility, or state transitions | 03_CONVERSATION_PLATFORM |
| Agent reasoning, response content, tool execution, workflow behavior, or agent-side cancellation | 02_AGENT_PLATFORM |
| Call/session/leg lifecycle, terminal outcomes, and operation transition authority | 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md |
| Media-resource state, signaling, buffering, transport flow control, or output transport evidence | 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md |
| STT/TTS processing, transcript/synthesis content, confidence, language/voice selection, or provider/model cost policy | 05_VOICE_SPEECH_PIPELINE.md |
| PSTN/SIP DTMF protocol, carrier call control, or telephony adapter behavior | 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md |
| Enterprise identity, authorization, consent, safety policy, retention, or compliance controls | 09_SECURITY_PLATFORM and 08_DATA_PLATFORM |

---

# Platform Foundation and Digital Channel Boundaries

Platform Foundation supplies tenant, membership, entitlement, shared configuration, and API-edge facts used to select an eligible interaction profile. Voice applies those facts to local observation and output gating; it does not own their control-plane lifecycle.

Digital Channel Platform owns non-voice delivery and channel interaction behavior. Voice interruption signals apply only to the current correlated Voice output operation and cannot cancel, restart, or expose another channel's delivery or context.

---

# Architecture Principles

## Activity Is Evidence, Not Intent

Voice activity detection (VAD), silence, endpointing, DTMF, push-to-talk, and barge-in signals describe observed transport/media conditions. They do not prove who is speaking, what the speaker intends, whether input is complete, or whether a canonical response turn may change.

## Voice Can Stop Its Own Output Safely

Voice may promptly stop or suppress active output when a valid local interruption, disconnect, safety/policy stop, or current approved cancellation requires it. This is a bounded transport action. It does not grant Voice authority to assign a next owner, generate a replacement response, or cancel agent/workflow execution directly.

## Conversation Owns the Next Permitted Action

Conversation Platform determines whether a participant, agent, human, workflow, or safe waiting state owns the next canonical work/response turn. Voice submits activity and interruption evidence and obeys approved output requests.

## Output Must Be Current

Every output operation is linked to an approved delivery request, media resource, Voice call/leg, correlation/idempotency reference, and cancellation/turn-authorization snapshot. Voice must suppress or stop output if the current operation no longer has valid delivery authority.

## Provider Behavior Is Contained

Provider-specific VAD thresholds, endpointing modes, interruption events, acoustic scores, DTMF tokens, room/track signals, and SDK callbacks remain adapter-local. The rest of the platform consumes normalized Voice turn evidence and outcomes.

---

# Core Concepts

## Voice Activity Signal

A Voice activity signal is normalized evidence that a bounded inbound media resource is active, inactive, uncertain, or has crossed a configured endpointing threshold. It includes timing, source/media reference, configuration profile, signal category, confidence/quality where available, and protected provider evidence.

## Voice Turn Window

A Voice turn window is a bounded Voice-domain observation window used to correlate media activity, recognition segments, interruption, and output control. It is not a canonical Conversation turn or a grant to act.

## Endpointing

Endpointing is a configured Voice decision that an input segment may be ready for recognition finalization or downstream consideration based on bounded evidence such as silence, explicit action, DTMF, or channel-specific completion signal. It never independently decides that a participant is finished, understood, or entitled to trigger business action.

## Barge-In

Barge-in is observed inbound activity that occurs while approved outbound Voice output is being prepared or streamed. It is a signal that may cause the Voice Platform to stop/suppress output according to current configuration and policy. It is not a canonical interruption decision, proof of participant intent, or automatic agent-cancellation authority.

## Interruption Request

An interruption request is a bounded instruction to stop, suppress, or prevent a specific Voice output operation. It records the operation, cause, caller/authority, timing, correlation, and outcome. It does not itself cancel broader agent/tool/workflow execution.

---

## Explicit Participant and Accessibility Controls

A channel may provide an explicit Voice control such as push-to-talk press/release, mute, a declared stop action, DTMF fallback, relay/assistive control, or another approved input. Voice normalizes this as a bounded control signal with source, timing, capability/profile, resource binding, and validation evidence.

| Signal | Meaning | Not implied |
|---|---|---|
| `input.control.start` | An approved channel control requests input capture/observation. | Identity, Conversation access, or a canonical turn. |
| `input.control.end` | An approved channel control indicates an input boundary. | Transcript finality, intent certainty, or response authorization. |
| `input.control.stop-output` | A validated control requests that the named current Voice output be stopped/suppressed. | Agent/tool/workflow cancellation or a canonical handoff. |
| `input.control.mute` | A channel/media input-control state changed. | Consent change, recording deletion, or a durable participant preference. |

Voice honors a valid stop-output control only for the current, correlated output operation and reports the bounded result. Conversation and Agent owners determine any broader work or state effect.
# Turn Signal Model

## Normalized Signal Types

| Signal | Meaning | Not implied |
|---|---|---|
| `input.activity.started` | Validated inbound media activity is observed. | Participant identity, intent, or a canonical turn change. |
| `input.activity.ended` | Inbound activity appears to have ended. | Completion of a participant's request. |
| `input.endpoint.candidate` | Configured Voice evidence suggests an input segment may be bounded. | Final transcript, intent certainty, or permission to act. |
| `input.endpoint.confirmed` | A configured endpointing rule completed for the Voice window. | Canonical interaction acceptance or response authorization. |
| `input.overlap.detected` | Inbound activity and outbound output overlap. | Which party owns the next response. |
| `output.interruption.requested` | A valid cause requires a named Voice output operation to stop/suppress. | Agent/workflow cancellation or canonical state change. |
| `output.interrupted` | Voice stopped/suppressed the named output operation or recorded an uncertain outcome. | Participant comprehension or delivery success. |
| `input.activity.uncertain` | Activity/endpointing cannot be safely determined. | Silence, completion, or safe resumption. |

## Tenant Interaction Profile

Each tenant/channel configuration references a versioned interaction profile. The profile defines allowed VAD/endpointing mode, endpoint timing range, barge-in eligibility, explicit-control support, push-to-talk/DTMF/relay behavior, no-barge-in and supervised modes, output-rate constraints, accessibility accommodations, quality/fallback rules, and operational owner.

The profile is evidence and configuration, not a participant preference or authorization grant by itself. A materially different profile must not be silently applied to an active Voice operation; it uses a controlled new operation, migration, or safe restriction path.
## Signal Quality and Configuration

Every signal includes the effective VAD/endpointing/interaction profile reference, channel/media capability, timing range, source quality category, and protected provider evidence reference. A low-quality or uncertain signal is reported as such; it is never normalized into a false silence, endpoint, participant identity, or completed interaction.

---

# Voice Turn Window State

~~~text
Created -> Observing -> InputActive -> EndpointCandidate -> EndpointConfirmed
                     |        |                  |
                     v        v                  v
                  Uncertain  Closed             Closed

Output operations are separately gated and may be Prepared, Streaming,
Interrupted, Completed, Suppressed, Failed, or Uncertain. An output interruption
is an output-operation outcome; it does not become a turn-window state.
~~~

| State | Meaning |
|---|---|
| Created | A bounded Voice observation context exists; no activity conclusion has been made. |
| Observing | Voice is monitoring eligible inbound media according to the active profile. |
| InputActive | Valid inbound activity is currently observed. |
| EndpointCandidate | Configured evidence suggests a potential boundary; further evidence or policy may be required. |
| EndpointConfirmed | The Voice endpointing rule completed for this observation window. |
| Uncertain | Voice cannot determine reliable activity/endpoint outcome. |
| Closed | The Voice window no longer accepts new observation events. |

A Voice Turn Window cannot become a canonical turn, change response ownership, reactivate a closed Conversation session, or cause a new agent execution. It may only produce normalized evidence through the approved boundary.

---

# Transition Authority and Guards

| Operation | Allowed source | Required guards | Voice result |
|---|---|---|---|
| Start observation | Voice media/lifecycle coordinator | Eligible inbound media resource, active configuration/profile, tenant/policy/capture checks, nonterminal lifecycle | Create/observe a Voice turn window. |
| Activity/endpoint signal | Validated VAD, explicit channel signal, or adapter event | Current window/resource correlation, profile version, ordering/idempotency, quality evidence | Publish normalized input signal or uncertainty. |
| Recognizer finalization request | Voice speech boundary after endpoint evidence | Eligible recognition sequence, current capture policy, idempotency, speech-pipeline contract | Request bounded recognition finalization; do not create canonical interaction. |
| Output interruption | Valid barge-in, approved Conversation cancellation, disconnect, safety/policy control, or applicable explicit input | Current named output operation, valid authority/cause, operation correlation, current lifecycle | Stop/suppress media output and record result. |
| Output start/resume | Approved Conversation delivery request | Current delivery/turn authorization snapshot, media/speech readiness, no pending interruption/cancellation, idempotency | Begin only the named bounded output operation. |
| Close/reconcile | Valid terminal resource, policy stop, timeout outcome, or reconciliation procedure | Current window, ordering/conflict checks, durable evidence | Close the window and publish outcome/uncertainty. |

Voice may act rapidly on a local output stop, but it records the cause and reports evidence. Conversation and Agent owners decide any broader work disposition through their own contracts.

---

# Barge-In and Output Interruption

## Interruption Precedence

When several stop/suppress causes compete, Voice applies them in this order:

1. security, safety, legal, consent, or policy stop;
2. call/media disconnect or terminal Voice lifecycle condition;
3. current Conversation-authorized cancellation or handoff disposition;
4. configured valid barge-in or explicit participant input signal;
5. routine output completion.

A lower-precedence cause cannot override a higher-precedence stop. All observed competing causes are recorded by correlation; the operation has one final Voice outcome.

## Barge-In Handling

A channel/profile may permit, restrict, or disable barge-in based on media capability, accessibility mode, tenant policy, output type, participant/channel constraints, and safety requirements. When enabled, a valid barge-in signal causes Voice to stop or suppress only the named active/prepared output operation.

Voice then continues bounded inbound observation where eligible and submits the resulting speech/activity evidence. It does not assume the participant wants a new response, that the earlier response should be discarded canonically, or that the agent must stop all processing.

## Output Interruption Outcome

| Outcome | Meaning |
|---|---|
| StoppedBeforeAudible | Voice prevented output before transport-start evidence. |
| InterruptedAfterStart | Voice stopped output after transport-start evidence; receipt/comprehension remains unknown. |
| Suppressed | Voice correctly prevented a stale, cancelled, unauthorized, or ineligible output operation. |
| CompletedBeforeStop | Stop arrived after transport-level completion; record the ordering conflict. |
| StopUncertain | Voice cannot safely establish whether participant-facing output stopped. |
| StopFailed | Voice could not stop the output as required; escalation/reconciliation evidence is required. |

---

# Endpointing and Recognition Coordination

Voice endpointing may request recognition finalization, but Speech Pipeline owns recognition sequence/finality semantics. A Voice endpoint candidate must not force an STT provider to return a false final result. The recognition provider may report final, corrected-final, unavailable, failed, or uncertain according to its contract.

Conversation Platform receives a final speech candidate only through the approved Speech/Conversation boundary. It resolves canonical interaction association, context, turn/work ownership, routing, handoff, and whether any response should be produced.

Explicit participant controls such as push-to-talk release, DTMF confirmation, or client action are normalized as Voice evidence and remain subject to the active channel, security, accessibility, and Conversation policies.

---

# Output Gating and Race Safety

## Delivery Snapshot

Before streaming output, Voice records the delivery request reference, target media resource, speech output reference, current configuration/capability profile, delivery/turn-authorization snapshot, idempotency key, cancellation reference, and trace/correlation fields. This snapshot is rechecked before transition to Streaming and at material interruption/reconnect points.

## Concurrent Events

Voice handles output, input, agent result, handoff, provider callback, cancellation, reconnect, and policy changes as potentially concurrent. It uses ordered source evidence, idempotency, operation versions, and current lifecycle checks rather than last-write-wins behavior.

- A stale output start cannot start after a later valid cancellation, handoff, resource release, or policy stop.
- A late barge-in cannot interrupt a completed/released output as though it were active; the conflict is recorded.
- A new approved delivery is a separate operation and must not reuse an earlier output's cancellation or media authority.
- Reconnect does not resume or replay output by default; current delivery authority and idempotency must permit it.
- If ordering or externally visible effect is uncertain, Voice stops/suppresses where safe and emits an uncertain/reconciliation outcome.

---

# Multi-Party, Accessibility, and Channel Constraints

A media resource may support multiple speakers or output listeners, but Voice records only Voice-domain activity/overlap evidence for each bound leg/resource. It does not infer participant roles, visibility, ownership, consent, or who may receive a response.

## Multi-Party Floor Control

Conversation Platform determines canonical participant roles, accountable response/work owner, visibility, and who is entitled to the next permitted action. Voice enforces only the resulting bounded media floor: which currently approved leg/resource may receive output, whether a bridge may mix audio, and whether an output must be muted, stopped, or isolated.

A change in speaking activity, conference membership, or media direction never grants floor ownership by itself. When no valid approved output target is present, Voice safely suppresses output and reports the reason for Conversation-controlled routing, handoff, waiting, or no-route handling.


Profiles may define accessibility and channel behavior such as push-to-talk, explicit end-of-turn control, longer endpointing windows, relay/assistive paths, DTMF fallback, output-rate restrictions, no-barge-in mode, or supervised/operator mode. These settings are versioned capability/policy evidence; they do not weaken security, consent, or canonical Conversation controls.

When speaker/leg attribution is ambiguous, Voice reports ambiguity rather than assigning a participant or stopping an unrelated party's output.

---

# Reliability, Recovery, and Failure Handling

Voice assumes false-positive/false-negative VAD, missing endpoint, noisy media, duplicate/out-of-order provider events, output-start/stop races, reconnect, provider failure, cancellation latency, and uncertain external effect.

- A VAD signal is bounded by its configuration version and quality evidence; it is not replayed into a new call/leg/window.
- Timeouts create explicit endpoint-unavailable, observation-uncertain, or output-reconciliation outcomes. They do not prove silence or completion.
- Bounded retries may apply to internal control signaling only when they cannot duplicate participant-facing output or alter canonical state.
- If Voice cannot stop output safely, it records `StopFailed` or `StopUncertain`, preserves evidence, and follows the configured operational escalation path.
- After restart/failover, Voice restores only the minimum current operation references and revalidates lifecycle, tenant/policy, resource binding, delivery/cancellation state, and idempotency before observing or outputting further media.

---

# VAD and Endpointing Evaluation

Before an interaction profile is activated or materially changed, Voice evaluates it against a versioned, policy-approved test set representing the supported channel, language/accent/dialect, acoustic/noise, accessibility, endpoint-control, and multi-party conditions.

Evaluation evidence records false-positive and false-negative activity/endpoint rates, endpoint latency, barge-in/stop success and latency, output-overlap incidence, uncertainty rate, quality degradation, accessibility behavior, known limitations, and operational/cost impact where applicable. The tenant's approved risk and interaction class define acceptance thresholds; no universal threshold is assumed.

Profile release requires comparison with the replaced profile where applicable, rollback readiness, owner approval, and test evidence. Production telemetry is used to detect drift or degradation, but it never silently changes an active profile or participant-facing behavior.

---
# Security, Privacy, and Tenant Isolation

Turn/activity operations are tenant-, environment-, media-resource-, call/leg-, configuration-, policy-, and purpose-scoped. VAD scores, timing, overlap evidence, DTMF, push-to-talk actions, interruption causes, and output state are protected Voice data.

- Provider activity or interruption callbacks are untrusted until validated for source, freshness, replay, resource binding, and operation scope.
- Activity/diarization evidence cannot prove identity, grant Conversation access, or expose another participant's restricted context.
- Routine telemetry uses normalized categories and protected references; it excludes raw audio, full transcript content, DTMF, credentials, and direct participant identifiers.
- Voice retains turn/interruption evidence only under approved data/recording/observability policy and does not create a shadow transcript or durable participant profile.
- A policy or security suspension immediately blocks new output/observation work as required and follows the documented safe stop/reconciliation path.

---

# Observability and Audit

Telemetry records profile/configuration version, media/call/leg references, input-activity/endpoint/overlap category, quality/uncertainty, output operation, interruption cause/outcome, cancellation latency, ordering conflict, retry/recovery, and terminal/reconciliation status.

Required measures include activity/endpoint rate, endpoint latency, false/interrupted output indicators, barge-in success, stop latency, stale-output suppression, output overlap, cancellation race, uncertain/failed stop, profile effectiveness, and results by authorized channel/language/accessibility aggregates.

Audit records changes to VAD/endpointing/barge-in profiles, privileged overrides, output stop/suppression, safety/policy stops, exceptional recovery, and associated principal/service, scope, evidence, correlation, and result.

---

# Testing Strategy

## Contract and State Tests

Validate turn-window and output-gate states, normalized signal schema, authority/guard matrix, precedence, finality boundary, idempotency, ordering, profile versioning, and prohibited canonical-state writes.

## Integration and Journey Tests

Validate quiet input, continuous speech, explicit end-of-turn, partial speech, barge-in during output, cancellation before/after output start, handoff during output, reconnect, multi-party/media attribution ambiguity, accessibility modes, and Voice-to-Speech-to-Conversation evidence flow.

## Security and Resilience Tests

Simulate forged/replayed VAD/provider events, wrong tenant/resource, stale profile, unauthorized output stop/start, false endpoint, duplicate/out-of-order barge-in, policy revocation, provider outage, output-stop failure, restart, and uncertain transport result. Prove no test changes canonical Conversation ownership, exposes protected data, or sends duplicate/stale participant-facing audio.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Turn signal contract | Defines normalized activity, endpoint, overlap, interruption, uncertainty, provenance, and compatibility semantics | Voice Platform with Conversation owner |
| Turn-window and output-gate state machine | Defines state, authority, guards, ordering, idempotency, and terminal outcomes | Voice Platform |
| Tenant interaction profile catalog | Defines configurable VAD/endpointing, barge-in, explicit control, accessibility, channel, quality, fallback, and versioning constraints | Voice Platform with Channel, Frontend, Security, and Operations owners |
| VAD and endpointing evaluation framework | Defines representative test sets, accuracy/latency/overlap measures, acceptance, drift, approval, and rollback evidence | Voice Platform with Testing, Operations, and Security owners |
| Barge-in and interruption policy | Defines eligibility, precedence, stop/suppress behavior, output-only outcomes, escalation, and audit | Voice Platform with Conversation, Agent, Security, and Operations owners |
| Multi-party media floor-control contract | Defines approved output targets, media isolation/mixing, ambiguity, and safe suppression without assigning canonical ownership | Voice Platform with Conversation and Security owners |
| Output delivery snapshot contract | Defines current delivery/turn authorization, cancellation, media/speech correlation, and stale-output prevention | Voice Platform with Conversation and Agent owners |
| Turn observability catalog | Defines measures, alerts, protected telemetry, audit, and diagnostic references | Voice Platform with Observability owner |
| Turn-taking test suite | Validates state, interaction, security, accessibility, resilience, and participant-facing safety | Voice Platform with Testing owner |

---

# Anti-Patterns

## VAD Becomes Participant Intent

Detected speech or silence is transport evidence only. It cannot prove meaning, completion, or a right to act.

## Barge-In Cancels the Agent Directly

Voice stops its bounded output and reports evidence. Agent execution cancellation follows the Agent/Conversation contracts.

## Output Resumes Automatically After Reconnect

Reconnect restores only eligible transport coordination. Current delivery authority, cancellation, and idempotency must authorize any output continuation.

## Latest Event Wins

Concurrent provider callbacks, cancellation, handoff, and output events require ordered evidence and state guards—not last-write-wins behavior.

## Speaker Label Grants Visibility

A media/speaker/leg label is not participant identity or authorization to access conversation context.

## Turn Signals Become a Shadow Conversation Model

Voice turn windows are transient transport observations. Conversation Platform remains the canonical owner of response/work turns and continuity.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md | Defines Voice lifecycle authority, timing, and terminal outcomes. |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | Defines media resources, buffering, output transport, and media-event semantics. |
| 05_VOICE_SPEECH_PIPELINE.md | Defines recognition/synthesis, finality, speech events, and provider selection. |
| 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md | Defines telephony-specific DTMF and provider behavior. |
| 12_VOICE_RELIABILITY_AND_FAILURE_HANDLING.md | Defines broader Voice recovery and operational handling. |
| 03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md | Defines canonical session and turn-ownership coordination. |
| 03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md | Defines destination and response ownership. |
| 03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md | Defines accountable handoff and in-flight work disposition. |
| 02_AGENT_PLATFORM/08_AGENT_EXECUTION_ENGINE.md | Defines agent execution lifecycle and cancellation boundary. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created provider-neutral Voice turn-taking and interruption model covering activity, endpointing, barge-in, output control, race safety, and ownership boundaries. |
| 1.1 | 2026-08-06 | Finalized output-interruption separation, explicit controls, tenant interaction profiles, floor control, and VAD/endpointing evaluation rules. |
| 1.2 | 2026-08-06 | Finalized after review for completeness, ownership overlap, long-term maintainability, and Platform Foundation/Digital Channel boundaries. |


