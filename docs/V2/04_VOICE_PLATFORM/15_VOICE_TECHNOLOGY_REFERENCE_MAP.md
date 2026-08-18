# 15_VOICE_TECHNOLOGY_REFERENCE_MAP

**Version:** 1.3  
**Status:** Approved  
**Owner:** Voice Platform Owner  
**Phase:** Voice Platform

---

# Overview

This document maps Voice Platform responsibilities to technology categories, standards, approved references, and candidate implementation options. It is a decision aid and adoption boundary—not a vendor commitment, architecture replacement, procurement decision, or implementation backlog.

The platform remains provider-neutral. Technologies are selected only through the contracts, tenant/provider profiles, security, testing, operations, and change controls defined in the preceding Voice documents.

---

# Purpose

The Technology Reference Map helps engineering choose an appropriate tool for each Voice responsibility while preserving One Brain, Multi-Channel ownership boundaries, tenant isolation, security, provider replaceability, operational resilience, and long-term maintainability.

It prevents one runtime, media platform, telephony carrier, speech provider, starter project, SDK, or managed service from silently becoming the owner of canonical Conversation state, agent intelligence, business logic, data governance, or enterprise policy.

---

# Objectives

This map must:

- Associate each Voice responsibility with an allowed technology category and its owning platform contract.
- Identify standards and official references that should be reviewed before implementation.
- Distinguish approved references, candidate technologies, and future evaluation items from adopted production decisions.
- State what each technology may do and what it must not own.
- Define selection criteria, adoption gates, proof-of-concept evidence, rollout, and exit requirements.
- Keep provider/model/cost choices tenant-aware, contract-driven, secure, testable, and reversible.

---

# Scope

This document covers technology roles for Voice media, WebRTC, telephony/SIP, speech, turn-taking, recording/transcripts, provider adapters, security, data, observability, testing, deployment, and developer tooling.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Voice behavior, contracts, state machines, security, tenant isolation, reliability, observability, testing, or provider-selection semantics | Voice documents 01–14 |
| Canonical Conversation, participant, routing, handoff, context, or event semantics | 03_CONVERSATION_PLATFORM |
| Agent reasoning, tools, workflows, prompts, knowledge, memory, or model policy | 02_AGENT_PLATFORM |
| Enterprise technology standard, procurement, vendor contract, legal/compliance decision, budget, or billing implementation | Architecture, Security, Operations, Finance/Billing, and Project governance owners |
| Final infrastructure, deployment, database, identity, storage, CI/CD, or frontend selection | Their respective platform/engineering documents |

---

# Technology Mapping Principles

# Platform Foundation and Digital Channel Boundaries

Platform Foundation owns technology choices for the shared tenant, membership, entitlement, configuration, and API-edge control plane. Voice may consume those approved capabilities for its bounded operations, but a Voice media, speech, telephony, or provider decision cannot substitute for an enterprise control-plane decision.

Digital Channel Platform owns technologies for non-voice participant transport and delivery. This map governs Voice technology only; shared Conversation or participant correlation does not make a Voice provider, client SDK, or media runtime a Digital Channel implementation choice.

## Technology Implements a Bounded Role

A technology may implement only the responsibility assigned by the relevant platform contract. For example, a media platform can coordinate a room/track; it cannot become the canonical Conversation, participant identity, agent brain, authorization system, or business workflow.

## Standards First, Providers Second

Use applicable open standards and provider-neutral contracts before a provider SDK. WebRTC, SIP, secure transport, event/schema versioning, and current enterprise security/data controls provide the stable boundary; SDKs and managed services are contained adapters.

## Official Documentation Before Adoption

Before implementation, review the current official documentation, SDK/API version, security/data/residency behavior, pricing/limits, regional availability, operational model, and migration/exit path. Record material adoption decisions in the Decision Log and the Architecture Reference Registry.

## No Technology Is a Default Commitment

A listed technology is an approved reference or candidate category, not an automatic production selection. The active tenant/provider/profile and controlled evaluation process determine what may serve an operation.

## Prefer Replaceable Integration

Use stable internal contracts, adapter interfaces, opaque identifiers, configuration snapshots, conformance suites, compatibility matrices, controlled rollout, and exit procedures. Avoid direct provider IDs, SDK types, credentials, callbacks, or errors in cross-platform business code.

---

# Reference Status and Terminology

| Status | Meaning |
|---|---|
| Approved reference | An official source that may inform design and evaluation under the Architecture Reference Registry. |
| Candidate technology | A category or named option that may be evaluated; it is not selected for production. |
| Adopted technology | A technology approved through documented decision, security review, provider profile, conformance, and rollout evidence. |
| Restricted technology | Allowed only for stated role, tenant, region, environment, or controlled evaluation. |
| Rejected/retired technology | Not eligible for new work; historical reasoning remains documented. |

At the date of this document, LiveKit is an active approved reference in the Architecture Reference Registry. Other names in this map are examples of technology categories or candidates and require their own current review and adoption decision before use.

---

# Technology Role Map

| Voice responsibility | Allowed technology category | Current approved reference or candidates | Must not own |
|---|---|---|---|
| Real-time media coordination | WebRTC SFU/media platform, realtime media SDK/service | LiveKit as active reference; other evaluated WebRTC-compatible media services | Canonical Conversation, participant identity, routing, agent reasoning, tenant policy. |
| Browser/mobile media client | WebRTC client SDK and platform-native media APIs | LiveKit client SDKs as reference where appropriate; standard browser/mobile APIs | Server authorization, canonical state, provider credentials, business workflow. |
| Web client implementation | TypeScript and React client application through Frontend/Voice contracts | Project-stack TypeScript/React; LiveKit TypeScript/React examples as implementation references | Tenant authority, authorization, provider secret custody, canonical Conversation state. |
| Agent/media service implementation | Python agent/runtime service, or another reviewed backend runtime | Project-stack Python; LiveKit Python Agent Starter and related examples as implementation references | Platform-wide workflow, security policy, data architecture, or direct business ownership. |
| PSTN/SIP connectivity | SIP trunk/carrier/telephony platform and adapter | LiveKit telephony/SIP reference; approved carriers/telephony providers such as Twilio or future evaluated options | Participant identity, handoff ownership, policy, conversation state. |
| Telephony control | Provider-neutral Voice call-control adapter | SIP methods/standards; provider SDKs contained behind adapter | Conversation routing/handoff, Agent actions, authorization decisions. |
| Speech recognition | STT provider/model behind Speech Pipeline adapter | OpenAI, ElevenLabs, Deepgram, Azure Speech, Google Cloud, or other evaluated providers | Canonical interaction truth, participant identity, policy, tool execution. |
| Speech synthesis | TTS provider/model behind Speech Pipeline adapter | ElevenLabs, OpenAI, Azure Speech, Google Cloud, Cartesia, or other evaluated providers | Response authorization, recipient selection, agent persona ownership. |
| Turn detection / VAD | VAD/endpointing/turn-detection library or provider capability | LiveKit Agents turn/VAD references; evaluated local/hosted capabilities | Canonical turn/work ownership or agent cancellation authority. |
| Recording/transcript capture | Provider capture/egress, controlled artifact adapter | LiveKit ingress/egress references; storage/capture services evaluated with Data/Security | Retention, deletion, legal hold, unrestricted access/export. |
| Provider abstraction | Internal adapter layer and registry/profile system | Platform-owned contracts; provider SDKs only inside adapters | Vendor lock-in, cross-platform identifiers, direct business logic. |
| Tenant/profile configuration | Platform configuration/feature/profile control plane | Platform-owned implementation; approved configuration store/runtime | Client-controlled tenant selection, provider credentials, unversioned behavior. |
| Secrets and workload identity | Enterprise secrets, identity, certificates, token service | Security Platform-selected technology | Provider-specific app logic or tenant-blind access. |
| Artifact storage/data lifecycle | Encrypted object/data storage, retention/deletion/hold services | Data Platform-selected technology | Voice capture meaning, access authorization, canonical conversation use. |
| Observability | Metrics/traces/logs/audit/alert platform | Observability Platform-selected technology; provider metrics mapped through adapters | Raw-content store or tenant-unscoped access path. |
| Testing | Contract, simulation, sandbox, journey, chaos, and conformance tooling | Testing Platform-selected technology; LiveKit testing/evaluation concepts as reference | Production participant contact or bypass of runtime controls. |
| Deployment/runtime | Container/orchestration/managed service/edge runtime | Operations/Deployment Platform-selected technology; LiveKit deployment guidance as reference | Platform-wide architecture or canonical business state. |

---

# Standards and Protocol References

| Standard or protocol | Voice role | Adoption limit |
|---|---|---|
| WebRTC | Realtime browser/device media transport and capability negotiation. | Use through media contract; room/track/client identifiers remain provider/client evidence. |
| SIP | Telephony signaling, trunking, call-control, transfer, and related provider integration. | Headers/dialogs/methods are untrusted adapter evidence; not canonical IDs or authorization. |
| SRTP / secure media transport | Media confidentiality/integrity where the approved profile requires it. | Security Platform defines required protection; Voice applies per operation/profile. |
| TLS / mutual authentication controls | Service, provider, callback, and signaling transport security. | Enterprise Security owns standards and credential lifecycle. |
| OpenAPI / event-schema versioning | Public/integration contracts and compatibility management. | Contract versioning does not expose provider internals or become an access grant. |
| MCP | Approved Agent/tool integration surface where relevant. | Agent/Integration owns tool semantics and authorization; Voice does not grant tool access from audio. |

Standards must be applied through the documented Voice Security, Tenant Isolation, Provider Abstraction, Testing, and Operations controls. Support for a standard feature is capability evidence, not an unconditional enablement decision.

---

# LiveKit Reference Map

LiveKit is an active official reference for Voice Platform design. Its currently documented capabilities include realtime WebRTC media, rooms/participants/tracks, Agents framework, telephony/SIP integration, ingress/egress, provider plugins, and deployment/operational guidance. These capabilities are useful implementation references, not replacements for this platform's contracts or ownership boundaries.

| Potential LiveKit role | Allowed evaluation/adoption use | Explicit boundary |
|---|---|---|
| Media server / SFU | Evaluate realtime media rooms, tracks, connection, transport quality, and provider-neutral media adapter design. | A LiveKit room/participant/track is not a canonical Conversation/session/participant identity. |
| Client SDK | Evaluate web/mobile realtime media integration and device/media controls. | Client tokens/room references do not grant platform authorization or select a tenant. |
| Agents framework | Evaluate voice runtime patterns, session/job lifecycle, turn/VAD concepts, model/provider plugins, and test/deployment practices. | Agent runtime does not replace Agent Platform, Conversation ownership, tool policy, or business workflow. |
| Telephony/SIP | Evaluate SIP ingress/egress, call-control, secure trunking, transfer, and region concepts. | Telephony success does not create participant identity, handoff ownership, or canonical state. |
| Ingress/egress | Evaluate controlled media ingestion/recording/streaming patterns. | Capture remains governed by Voice artifact policy and Data/Security lifecycle. |
| Metrics/testing examples | Evaluate operational metrics, testing, simulation, and evaluation concepts. | Platform observability/test contracts remain authoritative and privacy/tenant controls apply. |

Before code is written, review the specific current LiveKit documentation and SDK version for the selected role, then record the result, limitations, security/data implications, and adoption decision in the registry/Decision Log.

## LiveKit Supabase Hacker Starter Reference

The LiveKit Supabase Hacker Starter is an active **restricted evaluation reference** in the Architecture Reference Registry. It may inform a separately sandboxed proof of concept for LiveKit client/agent wiring, synthetic RAG or memory fixtures, session reporting, and local test workflow.

It must not be copied into the production platform as a repository structure, tenant model, database schema, Supabase policy, secret-key pattern, canonical Conversation model, or business workflow. Any adopted Voice pattern must be rebuilt behind the approved Voice, Platform Foundation, Data, Security, and Testing contracts.

---

# Speech Technology Evaluation Map

Speech providers and models are selected through the Speech Pipeline and Provider Abstraction profiles. The map below guides evaluation; it does not select a provider.

| Evaluation area | Required evidence |
|---|---|
| Recognition quality | Supported language/locale/accent/dialect/acoustic/channel coverage, finality/correction behavior, representative test-set results, limitations. |
| Synthesis quality | Voice/language/accessibility support, intelligibility/naturalness evaluation, output controls, interruption behavior, limitations. |
| Real-time performance | Time to partial/final/prepared/first output, streaming behavior, concurrency, availability, regional capacity, fallback compatibility. |
| Security and data | Data processing/residency, account/credential controls, retention/provider logging, redaction/minimization, contract/compliance review. |
| Tenant fit | Profile scope, quality/latency class, cost unit/quota, provider account model, usage attribution, support/incident posture. |
| Operational fit | API/SDK maturity, versioning, observability, error behavior, rate limits, migration/exit, conformance results. |

A speech provider/model can be the best technical fit for one tenant, region, language, or operation and ineligible for another. The lowest-cost option is considered only after compliance, capability, quality, latency, reliability, and operational constraints are met.

---

# Telephony and Carrier Evaluation Map

| Evaluation area | Required evidence |
|---|---|
| Endpoint/trunk capability | Inbound/outbound, SIP, media/codec, DTMF, caller identity, transfer/conference, region, capacity, and emergency status. |
| Trust/security | Source/callback validation, secure transport, account/credential controls, attestation/reputation signals, fraud protection, audit. |
| Policy/participant controls | Contactability, caller identity, consent/purpose/region/time inputs, recording, accessibility, safe no-route behavior. |
| Reliability | Route health, failover eligibility, callback ordering, uncertainty, porting/migration, support/escalation, regional recovery. |
| Cost/operations | Units/rates/quota, usage attribution, capacity limits, support model, commercial/exit review, tenant profiles. |

Telephony providers/carriers are evaluated per endpoint/route/tenant profile. A carrier's dial capability does not authorize contact, and a successful transport transfer does not prove canonical handoff completion.

---

# Supporting Technology Boundaries

## Data and Storage

Use Data Platform-selected storage, database, object, encryption, retention, deletion, backup, legal-hold, residency, and analytics technology. Voice provides protected artifact/provenance/access references and never makes a storage technology the authority for capture purpose, participant access, or canonical Conversation meaning.

## Security and Identity

Use Security Platform-selected identity, authorization, secrets, key/certificate, workload identity, policy, fraud, and monitoring technology. Voice applies current decisions per operation and never relies on phone numbers, provider IDs, media tokens, or transcript content as standalone authorization.

## Integration and API

Use Integration Platform-selected gateway, connector, webhook, workflow, API, and MCP technology. Voice provider adapters expose only validated, provider-neutral Voice contracts; Agent/Integration owns tools and external business actions.

## Frontend and Client Experience

Use Frontend Platform-selected web/mobile UI technology. Voice client/media SDKs may implement device and transport interaction, but frontend remains responsible for user experience, permission presentation, accessibility UI, and secure token acquisition paths.

## Operations, Deployment, and Observability

Use the selected platform tools for containers, orchestration, infrastructure, configuration delivery, monitoring, tracing, logs, alerts, incident handling, and cost control. Voice defines the required roles, signals, safety controls, and runbooks; infrastructure tools do not decide Voice business or security ownership.

---

# Technology Adoption Workflow

## Evaluation Gate

Before adopting a technology/provider/SDK/model/standard feature, the responsible owners must:

1. review current official documentation and licensing/commercial terms as appropriate;
2. map the technology to one bounded Voice role and contract;
3. assess security, privacy, tenant isolation, residency, accessibility, quality, latency, cost, reliability, observability, testing, and operational support;
4. build a controlled proof of concept using dedicated test tenants/accounts/resources;
5. run adapter conformance, compatibility, security/privacy/tenant, resilience, and performance tests;
6. define configuration/profile, rollout, rollback, migration/exit, support, and audit requirements; and
7. record a material decision in the Architecture Reference Registry and Decision Log before production adoption.

## Adoption Evidence

A technology is eligible for Active provider/profile use only when the required owner approvals, contract/version compatibility, security/data assessment, tenant/resource isolation, capability/quality/latency/cost evidence, observability, test results, operational runbooks, and rollback/exit path are current.

## Reassessment and Exit

Technology references and adopted integrations are reviewed before related implementation, at material SDK/provider/security/pricing/region/capability change, after relevant incidents, and on the architecture review cadence. Deprecation/exit prevents new selection, preserves governed historical evidence, migrates only eligible resources, revokes credentials, and avoids stranded canonical/business state in a provider.

---

# Technology Decision Record Template

Every material adoption records at least:

| Field | Required content |
|---|---|
| Decision | Adopt, restrict, defer, replace, or reject a technology for one bounded Voice role. |
| Scope | Tenant/environment/channel/provider role/operation/capability and contract versions. |
| Alternatives | Evaluated options and why they were not selected for this scope. |
| Evidence | Official documentation review, POC, conformance, quality/latency/cost, security/data, tenant, reliability, observability, and test results. |
| Constraints | Data/residency, policy, accessibility, capacity, commercial, support, region, and known limitations. |
| Rollout | Configuration/profile, cohort, monitoring, alert/SLO, owner, rollback, and approval. |
| Exit | Migration/replacement, data/reference treatment, credential revocation, retention, and audit. |

---

# Anti-Patterns

## LiveKit Room Is the Conversation

A media room/participant/track is transport evidence. Conversation Platform owns canonical conversation/session/participant state.

## Provider Plugin Chooses the Architecture

A convenient SDK/plugin may implement an adapter role but cannot choose platform ownership, business workflow, data model, security posture, or tenant model.

## Lowest-Cost Model Is Always Best

Cost is evaluated only after required compliance, capability, quality, latency, reliability, accessibility, and tenant constraints.

## Starter Repository Becomes the SaaS Blueprint

Starter projects can inform runtime, testing, deployment, or integration patterns. They do not dictate the platform repository structure, tenant model, product workflow, or business logic.

## Provider ID Escapes the Adapter

Call/room/track/model/voice/account/resource IDs remain protected adapter mappings, not canonical IDs, client tokens, or cross-platform keys.

## Technology Adoption Skips Exit Planning

Every material technology choice has a compatibility, rollback, migration, and exit path before production use.

## Standard Feature Means It Is Enabled

A supported protocol/capability is enabled only after current policy, security, tenant, profile, operation, and testing controls approve it.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Voice Platform ownership and document sequence. |
| 01–14 Voice Platform documents | Define the responsibilities, contracts, controls, evidence, and boundaries that technologies must implement. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Authoritative registry for approved external references and adoption limits. |
| 00_CONTROL/08_DECISION_LOG.md | Records material technology and architecture decisions. |
| 00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md | Defines platform-wide technology selection principles. |
| 02_AGENT_PLATFORM | Owns agent/runtime/model/tool/workflow technology decisions. |
| 07_INTEGRATION_PLATFORM | Owns connector, API, webhook, workflow, and MCP implementation technology. |
| 08_DATA_PLATFORM | Owns storage/data-lifecycle technology. |
| 09_SECURITY_PLATFORM | Owns enterprise identity/security/compliance technology. |
| 10_FRONTEND_PLATFORM | Owns frontend/client experience technology. |
| 11_OPERATIONS_PLATFORM | Owns operations/support technology. |
| 12_DEPLOYMENT_PLATFORM | Owns deployment/infrastructure technology. |
| 13_OBSERVABILITY_PLATFORM | Owns telemetry/alert tooling. |
| 14_TESTING_PLATFORM | Owns test infrastructure/tooling. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created provider-neutral Voice Technology Reference Map covering roles, standards, LiveKit reference boundaries, provider evaluation, adoption workflow, and exit controls. |
| 1.1 | 2026-08-06 | Approved after boundary review; clarified Platform Foundation and Digital Channel technology ownership. |
| 1.2 | 2026-08-06 | Added the LiveKit Supabase Hacker Starter as a restricted evaluation reference and recorded its Voice adoption limits. |
| 1.3 | 2026-08-07 | Recorded TypeScript, React, and Python as project-stack implementation options for LiveKit client and agent references, with platform-boundary limits. |
