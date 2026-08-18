# 01_INTEGRATION_PLATFORM_ARCHITECTURE

**Version:** 1.2  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the Integration Platform architecture for safely connecting the AI Workforce Platform to external systems and producing authorized external effects.

Integration is an execution boundary. It receives a bounded, authorized action request; validates the current scope and constraints; invokes a connector or workflow; and returns normalized evidence of the external outcome. It does not decide the business intent, become the canonical Conversation state store, or make external-system data an unrestricted platform source of truth.

---

# Purpose

The purpose of this architecture is to make integrations replaceable, tenant-safe, auditable, and reliable while preventing direct provider calls, hidden credentials, ungoverned data egress, duplicate external effects, and cross-platform ownership drift.

It establishes the durable boundary that later Integration documents refine for domain records, connector registry, credential delegation, authorization, execution, workflows, APIs, webhooks, isolation, governance, security, reliability, observability, testing, and technology selection.

---

# Objectives

Integration Platform must:

- Execute only a current, bounded action that has passed the applicable authorization and approval controls.
- Keep the Agent Platform responsible for intent, tool selection, reasoning, and requested business outcome.
- Keep the Conversation Platform responsible for canonical interaction/work state, participant association, routing, handoff, and outcome meaning.
- Normalize connector, provider, webhook, workflow, and external-system behavior behind versioned platform contracts.
- Enforce tenant, subject, purpose, entitlement, connector, credential, external-resource, action, approval, classification, retention, and egress scope on every material operation.
- Make external effects idempotent where possible, explicit when uncertain, reconcilable when delayed or contradictory, and auditable throughout.
- Keep external credentials, provider identifiers, payloads, callbacks, and imported data protected and minimally exposed.
- Support controlled connector adoption, rollout, configuration, deprecation, migration, and exit without embedding provider behavior in Agent, Conversation, Voice, or Digital Channel code.

---

# Scope

This document defines the Integration Platform ownership model, components, action path, cross-platform contracts, trust boundaries, external-effect principles, lifecycle, and implementation guardrails.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent identity, reasoning, tool selection, workflow intent, prompt behavior, or business decision | 02_AGENT_PLATFORM |
| Canonical conversation/work/session state, participant association, routing, handoff, or participant communication | 03_CONVERSATION_PLATFORM |
| Tenant, membership, entitlement, shared configuration, API-edge, or service-discovery control plane | 16_PLATFORM_FOUNDATION |
| Enterprise identity, authorization policy engine, secrets infrastructure, cryptography, compliance, audit infrastructure, or incident command | 09_SECURITY_PLATFORM |
| Voice media, telephony, speech, call lifecycle, or recording behavior | 04_VOICE_PLATFORM |
| Digital participant transport, delivery, channel-native identity translation, or non-voice channel capability | 17_DIGITAL_CHANNEL_PLATFORM |
| Knowledge publication/retrieval or Memory admission/retrieval/lifecycle | 05_KNOWLEDGE_PLATFORM and 06_MEMORY_PLATFORM |
| Physical persistence, queues, storage, backups, retention/deletion execution, or data infrastructure | 08_DATA_PLATFORM |
| Shared telemetry, test, deployment, operations, or frontend infrastructure | 10_FRONTEND_PLATFORM through 14_TESTING_PLATFORM, as applicable |

---

# Architecture Principles

## Execution Is Not Decision Authority

An Agent may select an eligible tool and request an intended action. Integration validates and executes the bounded effect, but cannot invent an objective, broaden parameters, select a recipient, infer approval, or continue work after a cancellation or restriction.

## External Success Is Evidence, Not Canonical State

An external provider response, webhook, or workflow completion is an Integration fact. Conversation Platform determines whether it changes canonical interaction/work state, routing, handoff, or participant communication through its own current contracts.

## Every External Effect Has a Current Scope

Every action validates current tenant/environment, subject/principal, purpose, entitlement, connector/capability, credential grant, target resource, parameters, classification/egress, approval, lifecycle, idempotency, and time bounds. A prior provider authorization or cached configuration cannot authorize a new effect.

## Connectors Are Replaceable Adapters

Provider SDKs, APIs, callbacks, credentials, identifiers, errors, and data shapes stay inside a connector adapter. Cross-platform consumers use platform-defined contracts, opaque references, normalized outcomes, and declared capability profiles.

## External Data Is Untrusted Until Governed

Provider responses, webhooks, files, metadata, schema claims, rate-limit headers, and imported records are untrusted evidence. They are validated, scoped, minimized, classified, and routed only through an approved owner path; they never directly grant authority or become canonical business truth.

## Fail Safely Under Uncertainty

If an effect may have occurred but cannot be confirmed, Integration records uncertainty, suppresses unsafe repetition, and reconciles through current authority. Availability, cost, or a convenient fallback cannot override security, tenant, approval, duplicate-safety, or data-egress controls.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies authoritative tenant, membership, entitlement, configuration, API-edge, and environment facts. Integration consumes and validates those facts for connector and action scope; it does not create a parallel control plane, accept client-selected tenant scope, or use an external account as a tenant authority.

Voice Platform owns voice media and telephony effects. Digital Channel Platform owns non-voice participant transport and delivery. Integration may execute an approved external business-system action for a Voice or Digital Channel journey, but it does not send participant communications, select a channel, place calls, or claim delivery success.

---

# Logical Components

| Component | Responsibility | Must not do |
|---|---|---|
| Integration API and contract boundary | Accept validated platform action requests and return normalized outcomes. | Accept arbitrary provider payloads or bypass current authorization. |
| Action coordinator | Creates bounded action records, applies guards, idempotency, dispatch, and outcome normalization. | Decide business intent or canonical Conversation state. |
| Tool and connector registry | Publishes versioned capabilities, schemas, profiles, availability, and ownership metadata. | Store broad credentials or let providers define platform semantics. |
| Connector adapter | Maps a bounded platform operation to one provider/external-system protocol. | Expose provider identifiers/errors as canonical public contracts. |
| Credential-delegation boundary | Obtains and applies scoped external grants through Security-owned mechanisms. | Persist, reveal, or broaden credentials outside current scope. |
| Approval and policy guard | Evaluates required current authorization, confirmation, approval, purpose, egress, and lifecycle constraints. | Replace Security policy or infer approval from tool selection. |
| Workflow coordinator | Manages bounded asynchronous action steps, callbacks, compensation, and reconciliation. | Become a general business-process owner or bypass action guards. |
| Webhook/event gateway | Validates, deduplicates, normalizes, and correlates external evidence. | Treat a signed callback as broad authority or a command. |
| Evidence and audit publisher | Emits protected action, outcome, governance, and reliability facts. | Store canonical conversation state or raw provider content in telemetry. |

---

# Governed Action Path

~~~text
Agent Platform
  |  selected eligible tool + bounded intended action
  v
Conversation / Platform Foundation context
  |  canonical work reference + current tenant, entitlement, lifecycle facts
  v
Integration action guard
  |  authorization, approval, purpose, connector, credential, egress, idempotency
  v
Connector adapter / approved external system
  |  normalized external evidence
  v
Integration outcome and reconciliation boundary
  |  protected outcome fact; no canonical state write
  v
Conversation Platform and other approved consumers
~~~

The action guard is re-evaluated before sensitive transitions, including credential use, external dispatch, callback processing, artifact exchange, workflow continuation, compensation, retry, fallback, and reconciliation.

---

# Action Lifecycle

The Integration Platform maintains an execution lifecycle separate from canonical Conversation and Agent state.

| State | Meaning |
|---|---|
| Requested | A bounded intended action has been submitted through an approved contract. |
| Validating | Current scope, parameters, policy, entitlement, connector, credential, approval, and idempotency evidence are being checked. |
| AwaitingApproval | A required human, policy, or delegated approval has not yet been satisfied. |
| Authorized | The action may proceed only within its recorded scope and expiry. |
| Dispatching | The connector is preparing or submitting the external operation. |
| InProgress | The external system or governed workflow is processing the action. |
| Succeeded | Evidence confirms the bounded external effect. |
| Failed | Evidence confirms that the bounded effect did not complete. |
| Denied | Current controls rejected the action before effect. |
| Cancelled | A current authorized cancellation stopped remaining permitted work. |
| Deferred | Work cannot proceed now and needs a future approved re-evaluation. |
| Uncertain | The external effect cannot be confirmed; duplicate-sensitive retries are prohibited pending reconciliation. |
| Reconciled | A governed reconciliation established the safe final disposition. |

Lifecycle transitions are controlled by the action guard and action coordinator. They are not an authorization grant, a statement of business completion, or a replacement for Conversation work state.

---

# Cross-Platform Contracts

| Producer or consumer | Integration contract responsibility |
|---|---|
| Agent Platform | Receives only selected eligible capability and may submit a bounded intended action. It does not invoke providers directly or treat a tool result as unrestricted truth. |
| Conversation Platform | Supplies approved work/cancellation/context references and receives normalized external outcome evidence. It decides canonical meaning and participant communication. |
| Platform Foundation | Supplies trusted tenant, environment, entitlement, configuration, and API-edge facts; Integration validates them at each effect. |
| Security Platform | Supplies identity, authorization, secrets, cryptography, compliance, audit, and incident controls; Integration applies them to connector and action operations. |
| Data Platform | Provides governed storage/queue/lifecycle mechanisms. Integration owns logical action/evidence requirements, not physical data services. |
| Voice and Digital Channel Platforms | May request or consume approved business-effect facts through public contracts. Integration does not own their transport, delivery, or participant identity semantics. |
| Knowledge and Memory Platforms | May provide governed context through their own contracts. That context does not by itself authorize an external effect or create an imported-memory path. |

Cross-platform communication uses versioned APIs, events, or contracts—never direct database access, shared provider credentials, or provider-specific types.

---

# External Trust and Data-Egress Boundary

Before data leaves the platform or an external system is contacted, Integration validates the current action purpose, permitted representation, target resource, connector capability, provider/account/region profile, credential scope, tenant/subject scope, classification, consent/policy, retention, and audit requirements.

Only the minimum approved representation is sent. Provider responses are minimized before wider platform use. Sensitive content, credentials, direct identifiers, tokens, external resource IDs, and raw payloads are not emitted in routine events, logs, traces, or unscoped action results.

---

# Reliability and Reconciliation Boundary

An outbound effect, webhook, callback, workflow step, or compensation is never repeated merely because a timeout occurred. Integration records a protected idempotency/correlation boundary, classifies the latest trustworthy evidence, and permits retry or fallback only when duplicate safety and current scope are proven.

Uncertain actions create a reconciliation record with the bounded request, external evidence references, idempotency/correlation, current guard snapshot, deadline, owner, and permitted next disposition. Reconciliation may confirm success, confirm failure, determine safe no-effect, defer, escalate, or retain uncertainty; it cannot assume completion.

---

# Security and Tenant Isolation Boundary

Connector configuration, credentials, provider accounts, action records, workflows, callbacks, queues, caches, audit records, telemetry, and external-resource mappings are all bound to a trusted tenant and environment. An external account, callback, API key, URL, provider ID, or client-supplied reference cannot select or widen tenant scope.

Each adapter uses the least privilege and shortest-lived credential material practical for its current approved operation. Sensitive operations—including connector enablement, credential grant, scope change, data export, high-impact action, approval override, provider migration, and recovery—require current delegated authority, separation of duties where required, expiry, and audit.

---

# Required Implementation Artifacts

# Official Starter Reference Boundary

The LiveKit Supabase Hacker Starter is registered as a restricted evaluation reference. It may be used only in a separate sandbox to study synthetic function-tool CRUD, session reporting, local developer workflow, and test-fixture patterns.

It does not authorize direct database access from an Agent, shared secret-key use, provider-selected tenant scope, provider-specific action contracts, or bypass of the Integration action guard. Any usable pattern must be independently implemented behind the approved connector, authorization, credential, idempotency, and audit contracts.

| Artifact | Purpose | Owner |
|---|---|---|
| Integration action contract | Defines the bounded request, scope, guard snapshot, outcome, uncertainty, and compatibility rules. | Integration with Agent, Conversation, Security, and Platform Foundation owners |
| Connector adapter interface | Defines provider-neutral capability, request/result, error, callback, idempotency, and evidence mappings. | Integration with Security and Testing owners |
| Governed action guard | Defines current authorization, approval, purpose, egress, tenant, credential, lifecycle, and idempotency prerequisites. | Integration with Security, Conversation, and Agent owners |
| Connector onboarding and exit procedure | Defines evaluation, configuration, capability profile, conformance, rollout, credential/data treatment, rollback, and retirement. | Integration with Operations, Security, Data, and Testing owners |
| External-effect reconciliation procedure | Defines uncertain-effect evidence, ownership, deadlines, safe disposition, escalation, and audit. | Integration with Conversation, Security, Data, and Operations owners |
| Integration cross-platform contract suite | Proves ownership, isolation, version compatibility, prohibited direct effect, and outcome handling. | Integration with Testing and all affected platform owners |

---

# Anti-Patterns

## Agent Calls a Provider Directly

Agent reasoning or tool selection does not grant direct provider SDK, credential, or network access. Every external effect passes through the governed Integration boundary.

## Provider Success Becomes Conversation Completion

A provider response is normalized external evidence. Conversation Platform decides whether and how it changes canonical work or participant experience.

## Connector Credential Is a General Platform Secret

Credentials are scoped to one current connector operation through Security-owned mechanisms. They are never shared broadly with Agent, Conversation, channel, frontend, or client code.

## Webhook Is a Trusted Command

A callback is untrusted evidence until source, freshness, replay, schema, tenant/resource, ordering, and operation correlation are validated. It cannot grant broad authority.

## Timeout Means No External Effect

A timeout creates uncertainty unless independent evidence proves success or failure. Duplicate-sensitive effects remain suppressed until reconciliation permits a safe next step.

## Integration Owns the Business Workflow

Integration coordinates technical external steps only. Agent and Conversation contracts remain authoritative for intent and canonical work meaning.

---

# Related Documents

| Document | Relationship |
|---|---|
| README.md | Defines Integration Platform navigation, scope, and reading order. |
| 02_INTEGRATION_DOMAIN_MODEL.md | Defines Integration entities, identifiers, states, and evidence in detail. |
| 03–16 Integration Platform documents | Refine registry, credentials, authorization, execution, workflows, APIs, events, isolation, governance, security, reliability, observability, testing, and technology choices. |
| 02_AGENT_PLATFORM/README.md | Defines Agent intent, reasoning, selection, and execution boundary. |
| 03_CONVERSATION_PLATFORM/README.md | Defines canonical interaction/work ownership and outcome meaning. |
| 16_PLATFORM_FOUNDATION/README.md | Defines tenant, entitlement, configuration, and API-edge ownership. |
| 09_SECURITY_PLATFORM/README.md | Defines enterprise identity, authorization, secrets, compliance, and audit-control ownership. |
| 00_CONTROL/04_SYSTEM_BOUNDARIES.md | Defines platform ownership boundaries. |
| 00_CONTROL/08_DECISION_LOG.md | Records material integration and technology decisions. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration Platform architecture covering execution boundaries, governed action lifecycle, cross-platform contracts, external trust, reconciliation, security, and tenant isolation. |
| 1.1 | 2026-08-06 | Added the LiveKit Supabase Hacker Starter restricted evaluation boundary. |
| 1.2 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |
