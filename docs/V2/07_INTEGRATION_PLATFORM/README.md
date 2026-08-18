# 07_INTEGRATION_PLATFORM

**Version:** 1.18
**Status:** Approved
**Owner:** Integration Platform Owner
**Phase:** Platform Architecture

---

# Overview

The Integration Platform connects approved platform capabilities to external business systems and executes authorized business actions through governed tools, connectors, workflows, APIs, webhooks, and MCP-compatible interfaces.

It makes external effects reliable, traceable, tenant-scoped, and replaceable. It is not an agent brain, canonical conversation engine, customer-memory store, generic data warehouse, or enterprise identity platform.

---

# Purpose

This README is the navigation and boundary document for the Integration Platform. It identifies its authoritative documents, intended reading order, ownership, cross-platform dependencies, and approval state.

It does not replace the detailed architecture documents listed below.

---

# Ownership

Integration Platform owns:

- Connector and tool implementation for approved external systems, APIs, webhooks, files, and business-action endpoints.
- Tool/connector capability registration, schemas, external-system mappings, connector-specific authentication delegation, and provider adaptation.
- Authorized action execution, request validation, idempotency, confirmation, external outcome normalization, retry/reconciliation, and external-effect evidence.
- Long-running external workflow coordination, callback/event intake, delivery status, and integration-domain reliability, observability, testing, and technology requirements.

Integration Platform does not own:

- Agent identity, reasoning, tool selection, workflow intent, prompt behavior, or business decision-making.
- Canonical conversation/session state, participant association, routing, handoff, or conversation-event meaning.
- Reusable business knowledge, personal memory, source publication, or Memory/Knowledge retrieval semantics.
- Tenant/organization/membership/entitlement/configuration/API-edge ownership; enterprise identity, authorization, secrets, cryptography, audit infrastructure, or compliance control ownership.
- Physical storage, backups, shared telemetry/test infrastructure, deployment, operations processes, user-interface ownership, voice media, or digital-channel transport.

---

# Reading Order

Read these documents in order when designing, implementing, or reviewing Integration Platform behavior:

1. 01_INTEGRATION_PLATFORM_ARCHITECTURE.md
2. 02_INTEGRATION_DOMAIN_MODEL.md
3. 03_TOOL_AND_CONNECTOR_REGISTRY.md
4. 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md
5. 05_ACTION_AUTHORIZATION_AND_APPROVAL.md
6. 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md
7. 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md
8. 08_EXTERNAL_API_AND_MCP_BOUNDARY.md
9. 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md
10. 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md
11. 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md
12. 12_INTEGRATION_SECURITY_AND_PRIVACY.md
13. 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md
14. 14_INTEGRATION_OBSERVABILITY.md
15. 15_INTEGRATION_TESTING.md
16. 16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP.md

---

# Document Map

| Document | Primary question answered |
|---|---|
| 01_INTEGRATION_PLATFORM_ARCHITECTURE.md | What does Integration Platform own and how does it relate to the rest of the platform? |
| 02_INTEGRATION_DOMAIN_MODEL.md | Which canonical integration entities, identifiers, action states, and evidence must exist? |
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | How are tools, connectors, capabilities, schemas, versions, and availability governed? |
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | How are connector-specific external credentials and delegated grants requested, scoped, rotated, and revoked? |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | How are requested business effects authorized, confirmed, approved, constrained, and audited? |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | How are external actions executed exactly once where possible, retried safely, and normalized? |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | How are long-running workflows, callbacks, compensation, and recovery controlled? |
| 08_EXTERNAL_API_AND_MCP_BOUNDARY.md | How are external APIs, MCP-compatible interfaces, and tool contracts exposed without bypassing policy? |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | How are incoming callbacks/events validated, normalized, deduplicated, and correlated? |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | How are tenant, subject, purpose, connector, credential, and external-resource boundaries enforced? |
| 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md | Who may enable connectors, approve actions, change scopes, review outcomes, and audit effects? |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | How are external trust, credentials, data egress, injection, abuse, and incidents controlled? |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | How do actions, workflows, callbacks, reconciliation, and safe failure behave under uncertainty? |
| 14_INTEGRATION_OBSERVABILITY.md | Which signals make connector, action, workflow, callback, and external-effect behavior observable? |
| 15_INTEGRATION_TESTING.md | Which evidence proves actions are authorized, isolated, reliable, and safe? |
| 16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP.md | Which standards and technologies may fill bounded integration roles, and what may they not own? |

---

# Cross-Platform Boundaries

| Platform | Integration Platform relationship |
|---|---|
| 16_PLATFORM_FOUNDATION | Supplies tenant, membership, entitlement, configuration, and API-edge facts. Integration applies them to connector/action scope; it does not own the control plane. |
| 02_AGENT_PLATFORM | Selects approved tools/workflows and requests intended actions through controlled contracts. Integration validates and executes the external effect; it does not decide intent. |
| 03_CONVERSATION_PLATFORM | Supplies canonical interaction/work ownership and records approved outcome facts. Integration does not own conversation state or participant routing. |
| 04_VOICE_PLATFORM | May request or consume approved integration outcomes for voice journeys. Voice owns media/telephony; Integration owns external business-system effects. |
| 17_DIGITAL_CHANNEL_PLATFORM | May submit or consume approved actions for digital-channel journeys. Digital Channel owns transport/delivery; Integration owns external business-system effects. |
| 05_KNOWLEDGE_PLATFORM | May supply governed business knowledge to an Agent; Integration does not treat retrieved knowledge as authority to execute an action. |
| 06_MEMORY_PLATFORM | May supply purpose-bound personal context; Integration does not store or expand personal memory from external data without the governed Memory path. |
| 08_DATA_PLATFORM | Provides persistence, queues, cache, backups, and data-service operations. Integration owns logical action/workflow records and external-effect requirements. |
| 09_SECURITY_PLATFORM | Provides enterprise identity, authorization, secrets, cryptography, audit infrastructure, compliance, and incident controls. Integration applies them to connector grants and actions. |
| 10_FRONTEND_PLATFORM | Provides operator/participant interfaces. Integration defines capability, approval, confirmation, outcome, and error information those interfaces require. |
| 13_OBSERVABILITY_PLATFORM | Provides shared telemetry infrastructure. Integration defines connector/action/workflow signals and outcome semantics. |
| 14_TESTING_PLATFORM | Provides test standards and infrastructure. Integration defines action safety scenarios, fixtures, and release evidence. |

---

# Current Status

The complete 16-document Integration Platform architecture set, including this README and documents `01_INTEGRATION_PLATFORM_ARCHITECTURE.md` through `16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP.md`, is approved.

The initial delivery goal is a narrow governed action path: an authorized tenant can enable one approved connector, let an approved agent request one bounded business action, require any needed confirmation, execute it idempotently, receive an auditable normalized outcome, and reconcile an uncertain external result without duplicate participant or business impact.

---

# Change Rules

Changes to this module must:

- Preserve Agent ownership of intent, selection, reasoning, and business decision-making; Integration owns execution, not decision authority.
- Preserve Conversation ownership of canonical interaction/work state and outcome meaning; Integration returns normalized external facts through controlled contracts.
- Treat every external request, callback, connector configuration, credential/grant, action parameter, provider response, and imported data as untrusted until validated for its intended use.
- Use controlled APIs, events, or contracts rather than direct cross-module database access or provider calls from Agent/Conversation/Channel code.
- Enforce tenant, subject, purpose, entitlement, connector, credential, external-resource, action, approval, retention, and egress boundaries at every representation.
- Keep enterprise identity, authorization, secrets, encryption, audit infrastructure, and compliance controls with Security Platform.
- Update affected governance, security, privacy, isolation, reliability, observability, testing, and reference documents together.
- Create or update a Decision Log record when changing a long-lived connector model, external effect, credential scope, approval rule, workflow/compensation behavior, data-egress posture, or ownership boundary.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/02_PROJECT_ROADMAP.md | Defines the approved-business-action delivery outcome. |
| 00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md | Defines platform-wide architectural principles. |
| 00_CONTROL/04_SYSTEM_BOUNDARIES.md | Defines platform ownership boundaries. |
| 00_CONTROL/05_MODULE_OWNERSHIP.md | Defines Integration Platform responsibility. |
| 00_CONTROL/06_DOCUMENTATION_STANDARDS.md | Defines document lifecycle and approval rules. |
| 00_CONTROL/07_DOCUMENTATION_INDEX.md | Registers this module and document set. |
| 00_CONTROL/08_DECISION_LOG.md | Records material architecture and technology decisions. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Registers the LiveKit Supabase Hacker Starter as a restricted evaluation reference. |
| 02_AGENT_PLATFORM/README.md | Defines agent intent, tool selection, and execution ownership boundaries. |
| 03_CONVERSATION_PLATFORM/README.md | Defines canonical interaction and outcome ownership. |
| 16_PLATFORM_FOUNDATION/README.md | Defines control-plane and entitlement ownership. |
| 09_SECURITY_PLATFORM/README.md | Defines enterprise security-control ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration Platform navigation, ownership, planned document set, delivery boundary, and cross-platform relationships. |
| 1.1 | 2026-08-06 | Recorded the draft Integration Platform Architecture document. |
| 1.2 | 2026-08-06 | Linked the restricted LiveKit Supabase Hacker Starter reference and its adoption limits. |
| 1.3 | 2026-08-06 | Recorded approval of the Integration Platform Architecture document. |
| 1.4 | 2026-08-06 | Recorded approval of the Integration Domain Model. |
| 1.5 | 2026-08-06 | Recorded approval of the Tool and Connector Registry. |
| 1.6 | 2026-08-06 | Recorded approval of Connector Authentication and Credential Delegation. |
| 1.7 | 2026-08-06 | Recorded approval of Action Authorization and Approval. |
| 1.8 | 2026-08-06 | Recorded approval of Action Execution and Idempotency. |
| 1.9 | 2026-08-06 | Recorded approval of Workflow and Asynchronous Execution. |
| 1.10 | 2026-08-06 | Recorded approval of the External API and MCP Boundary. |
| 1.11 | 2026-08-06 | Recorded approval of the Webhook and External Event Model. |
| 1.12 | 2026-08-06 | Recorded approval of Integration Access and Tenant Isolation. |
| 1.13 | 2026-08-06 | Recorded approval of Integration Governance and Audit. |
| 1.14 | 2026-08-06 | Recorded approval of Integration Security and Privacy. |
| 1.15 | 2026-08-06 | Recorded approval of Integration Reliability and Failure Handling. |
| 1.16 | 2026-08-06 | Recorded approval of Integration Observability. |
| 1.17 | 2026-08-06 | Recorded approval of Integration Testing. |
| 1.18 | 2026-08-06 | Recorded approval of the Integration Technology Reference Map and complete Integration Platform architecture set. |
