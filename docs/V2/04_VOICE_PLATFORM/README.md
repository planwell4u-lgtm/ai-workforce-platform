# 04_VOICE_PLATFORM

**Version:** 1.16  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Platform Architecture

---

# Overview

The Voice Platform provides real-time voice communication capabilities for the AI Workforce Platform.

It receives and delivers voice interactions through approved voice and telephony channels while preserving the One Brain, Multi-Channel architecture. Voice is a communication capability; it does not create a separate agent brain or become the owner of canonical conversation behavior.

---

# Purpose

This README defines the Voice Platform's ownership, boundaries, planned document set, reading order, and relationship to adjacent platforms.

It is the module navigation document. Detailed architecture decisions belong in the numbered Voice Platform documents.

---

# Ownership

Voice Platform owns:

- Voice-channel ingress and egress.
- Real-time media/session coordination for voice transport.
- Audio streaming, signaling, call control, SIP/telephony integration, and provider adaptation.
- Speech pipeline coordination, including STT, TTS, voice activity, interruption, and audio delivery behavior.
- Voice-specific provider, media, recording/transcript capture, reliability, observability, and testing requirements.
- The provider abstraction that allows LiveKit, Twilio, and future voice providers to be adopted without moving business ownership into a vendor.

Voice Platform does not own:

- Canonical conversations, participant associations, normalized interaction state, conversation sessions, context, routing, handoff, or conversation events.
- Agent identity, reasoning, instructions, model selection, tools, workflows, knowledge, or memory.
- Enterprise identity, authorization, secrets, retention infrastructure, data storage, telemetry infrastructure, or testing infrastructure.
- CRM, ticketing, workflow-engine, or other external business-system implementation.

---

# Core Boundary

~~~text
Voice / PSTN / SIP / WebRTC Participant
    |
    v
Voice Platform
    |  validated voice interaction and approved delivery outcome
    v
Conversation Platform
    |  authorized execution request and bounded context
    v
Agent Platform
~~~

Voice Platform validates and normalizes voice-channel evidence according to its own transport contracts. Conversation Platform decides canonical conversation association, lifecycle, session continuity, routing, handoff, state, and conversation-event facts. Agent Platform decides intelligence and execution.

---

# Provider Replaceability

LiveKit and Twilio are approved references and possible implementation providers, not architecture owners.

The Voice Platform uses provider-neutral contracts for voice interactions, call/media lifecycle, speech results, delivery outcomes, recording/transcript references, errors, and observability. Provider-specific behavior remains inside a bounded adapter or integration boundary.

A provider must not dictate canonical conversation identifiers, participant identity, agent behavior, state model, routing policy, handoff policy, or data-retention policy.

---

# Planned Document Set

| Document | Primary question answered |
|---|---|
| 01_VOICE_PLATFORM_ARCHITECTURE.md | What does Voice Platform own and how does it relate to other platforms? |
| 02_VOICE_CHANNEL_MODEL.md | How are supported voice channels and provider-native capabilities represented? |
| 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md | How do call and voice-session states progress without replacing conversation state? |
| 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md | How are real-time media, signaling, audio streams, and transport coordinated? |
| 05_VOICE_SPEECH_PIPELINE.md | How are STT, TTS, transcription, synthesis, confidence, and language handled? |
| 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md | How are VAD, barge-in, turn ownership, interruption, and response cancellation controlled? |
| 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md | How are PSTN, SIP, numbers, call control, and telephony providers integrated? |
| 08_VOICE_PROVIDER_ABSTRACTION.md | How are LiveKit, Twilio, and future providers kept replaceable? |
| 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md | How are capture, provenance, consent, access, and controlled references handled? |
| 10_VOICE_SECURITY.md | Which voice-specific trust, authorization, fraud, and privacy requirements apply? |
| 11_VOICE_TENANT_ISOLATION.md | How are voice configuration, provider resources, calls, and media isolated by tenant? |
| 12_VOICE_RELIABILITY_AND_FAILURE_HANDLING.md | How does voice behavior degrade, recover, reconcile, and fail safely? |
| 13_VOICE_OBSERVABILITY.md | Which voice-domain signals, indicators, alerts, and diagnostics are required? |
| 14_VOICE_TESTING.md | Which voice-domain test evidence proves quality, safety, and resilience? |
| 15_VOICE_TECHNOLOGY_REFERENCE_MAP.md | Which technologies and external references fit each Voice responsibility? |

---

# Reading Order

1. 01_VOICE_PLATFORM_ARCHITECTURE.md
2. 02_VOICE_CHANNEL_MODEL.md
3. 03_VOICE_CALL_AND_SESSION_LIFECYCLE.md
4. 04_VOICE_REALTIME_MEDIA_ARCHITECTURE.md
5. 05_VOICE_SPEECH_PIPELINE.md
6. 06_VOICE_TURN_TAKING_AND_INTERRUPTION_MODEL.md
7. 07_VOICE_TELEPHONY_AND_SIP_INTEGRATION.md
8. 08_VOICE_PROVIDER_ABSTRACTION.md
9. 09_VOICE_RECORDING_AND_TRANSCRIPT_GOVERNANCE.md
10. 10_VOICE_SECURITY.md
11. 11_VOICE_TENANT_ISOLATION.md
12. 12_VOICE_RELIABILITY_AND_FAILURE_HANDLING.md
13. 13_VOICE_OBSERVABILITY.md
14. 14_VOICE_TESTING.md
15. 15_VOICE_TECHNOLOGY_REFERENCE_MAP.md

---

# Cross-Platform Boundaries

| Platform | Relationship |
|---|---|
| 03_CONVERSATION_PLATFORM | Owns canonical conversation lifecycle, sessions, state, context, routing, handoff, and conversation-event semantics. Voice supplies validated voice interaction and delivery evidence through approved contracts. |
| 02_AGENT_PLATFORM | Owns agent intelligence and execution. Voice presents approved audio input/output; it does not decide agent behavior. |
| 16_PLATFORM_FOUNDATION | Provides tenant, membership, entitlement, configuration, and API-edge facts. Voice applies them to voice resources and operations; it does not own the control plane. |
| 17_DIGITAL_CHANNEL_PLATFORM | Owns non-voice participant transport and delivery. Voice owns real-time voice media, telephony, and speech behavior; neither module owns canonical Conversation state. |
| 07_INTEGRATION_PLATFORM | Owns external connector and workflow implementation. Voice owns the voice-provider domain contract and delegates provider adapters through approved integration boundaries. |
| 08_DATA_PLATFORM | Provides storage/lifecycle mechanisms. Voice owns recording/transcript capture semantics and references, not storage implementation. |
| 09_SECURITY_PLATFORM | Provides enterprise identity, authorization, secrets, compliance, and security controls. Voice applies those controls to voice-specific operations. |
| 13_OBSERVABILITY_PLATFORM | Provides shared telemetry infrastructure. Voice defines voice-domain signals and required outcomes. |
| 14_TESTING_PLATFORM | Provides shared test infrastructure. Voice defines voice-domain scenarios and evidence. |

---

# Current Status

The complete 15-document Voice Platform architecture set, including this README and documents `01_VOICE_PLATFORM_ARCHITECTURE.md` through `15_VOICE_TECHNOLOGY_REFERENCE_MAP.md`, is approved.

The approved set preserves Conversation Platform ownership of canonical conversation lifecycle, session, state, routing, handoff, and event semantics, and Agent Platform ownership of intelligence and execution. Voice remains a bounded communication capability and does not supersede Platform Foundation or Digital Channel ownership.

---

# Change Rules

Voice changes must:

- Preserve Conversation Platform ownership of canonical conversation behavior.
- Preserve Agent Platform ownership of intelligence and execution.
- Keep provider-specific logic behind replaceable Voice/Integration boundaries.
- Treat caller/channel/provider data as untrusted until validated for its intended use.
- Update security, tenant isolation, data governance, observability, testing, and operational documents when voice behavior changes.
- Create or update a decision record for a major provider, protocol, call-control, recording, security, or ownership decision.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/04_SYSTEM_BOUNDARIES.md | Defines platform ownership boundaries. |
| 00_CONTROL/06_DOCUMENTATION_STANDARDS.md | Defines documentation lifecycle and approval rules. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Registers approved LiveKit references and their adoption limits. |
| 03_CONVERSATION_PLATFORM/README.md | Defines the approved canonical Conversation Platform boundary. |
| 03_CONVERSATION_PLATFORM/01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform ownership and voice integration boundary. |
| 03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md | Defines canonical conversation session coordination. |
| 03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md | Defines response destination selection and ownership. |
| 03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md | Defines agent/human transfer behavior. |
| 02_AGENT_PLATFORM/README.md | Defines Agent Platform ownership and execution boundary. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Voice Platform module navigation, ownership, boundaries, and planned document set. |
| 1.1 | 2026-08-06 | Recorded completion of the draft set and its cross-platform boundary review; formal approval remains pending. |
| 1.2 | 2026-08-06 | Recorded approval of the Voice Platform Architecture document and added Platform Foundation/Digital Channel boundaries. |
| 1.3 | 2026-08-06 | Recorded approval of the Voice Channel Model and its Platform Foundation/Digital Channel boundaries. |
| 1.4 | 2026-08-06 | Recorded approval of the Voice Call and Session Lifecycle model. |
| 1.5 | 2026-08-06 | Recorded approval of the Voice Realtime Media Architecture model. |
| 1.6 | 2026-08-06 | Recorded approval of the Voice Speech Pipeline model. |
| 1.7 | 2026-08-06 | Recorded approval of the Voice Turn-Taking and Interruption model. |
| 1.8 | 2026-08-06 | Recorded approval of the Voice Telephony and SIP Integration model. |
| 1.9 | 2026-08-06 | Recorded approval of the Voice Provider Abstraction model. |
| 1.10 | 2026-08-06 | Recorded approval of the Voice Recording and Transcript Governance model. |
| 1.11 | 2026-08-06 | Recorded approval of the Voice Security model. |
| 1.12 | 2026-08-06 | Recorded approval of the Voice Tenant Isolation model. |
| 1.13 | 2026-08-06 | Recorded approval of the Voice Reliability and Failure Handling model. |
| 1.14 | 2026-08-06 | Recorded approval of the Voice Observability model. |
| 1.15 | 2026-08-06 | Recorded approval of the Voice Testing model. |
| 1.16 | 2026-08-06 | Recorded approval of the Voice Technology Reference Map and complete Voice Platform architecture set. |
