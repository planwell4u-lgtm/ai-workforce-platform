# 02_AGENT_PLATFORM

**Version:** 3.7  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

The Agent Platform is the centralized intelligence layer of the Voice Agent SaaS Platform. It defines and operates the Agent Brain: agent identity, configuration, instructions, capabilities, reasoning orchestration, controlled tool and workflow selection, versioned behavior, governance, and accountable execution.

The platform follows One Brain, Multi-Channel. Voice, chat, messaging, email, API, and future channels use the same approved Agent Brain; they do not duplicate intelligence or business logic.

---

# Purpose

This module provides the architecture documentation for designing, governing, validating, and evolving AI agents as tenant-scoped, secure, observable, versioned business capabilities.

It is the primary reference for engineers, architects, AI assistants, and reviewers working on agent behavior and agent-controlled execution.

---

# Ownership

The Agent Platform owns:

- Agent identity, purpose, configuration, instructions, persona, capabilities, and lifecycle.
- Agent runtime and reasoning orchestration.
- Selection of approved capabilities, tools, and workflows.
- Versioned agent definitions, deployment assignments, evaluation evidence, and governance records.
- Agent-specific observability, analytics, testing, failure behavior, and technology-reference mapping.

The Agent Platform does not own:

- Conversation lifecycle, conversation state, context routing, or human handoff coordination.
- Voice/media/telephony or channel-provider transport.
- Knowledge documents/retrieval implementation or customer-memory lifecycle.
- External integration/connector implementation, data storage, identity/security infrastructure, deployment infrastructure, shared observability, or testing infrastructure.

Those responsibilities belong to their respective platform modules and are accessed through governed contracts.

---

# Module Reading Order

Start with the core agent definition and runtime documents:

1. 01_AGENT_PLATFORM_OVERVIEW.md
2. 02_AI_EMPLOYEE_CONCEPT.md
3. 03_AGENT_ARCHITECTURE.md
4. 04_AGENT_LIFECYCLE.md
5. 05_AGENT_IDENTITY_MODEL.md
6. 06_AGENT_CONFIGURATION_MODEL.md
7. 07_AGENT_RUNTIME_ARCHITECTURE.md
8. 08_AGENT_EXECUTION_ENGINE.md
9. 09_AGENT_ORCHESTRATION_MODEL.md
10. 10_AGENT_STATE_MANAGEMENT.md
11. 11_AGENT_CONTEXT_MODEL.md
12. 12_AGENT_INSTRUCTION_SYSTEM.md
13. 13_AGENT_PERSONA_AND_BEHAVIOR_MODEL.md
14. 14_AGENT_CAPABILITY_MODEL.md

Then read the controlled action and integration boundaries:

15. 15_AGENT_TOOL_SYSTEM.md
16. 16_AGENT_TOOL_EXECUTION_MODEL.md
17. 17_AGENT_PLUGIN_ARCHITECTURE.md
18. 18_AGENT_MEMORY_INTEGRATION.md
18A. 18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT.md
19. 19_AGENT_KNOWLEDGE_INTEGRATION.md
19A. 19A_AGENT_KNOWLEDGE_INTEGRATION_REWRITE_DRAFT.md
20. 20_AGENT_WORKFLOW_INTEGRATION.md
20A. 20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md
21. 21_AGENT_EVENT_INTEGRATION.md

Then read the platform controls and lifecycle documents:

22. 22_AGENT_MULTI_CHANNEL_MODEL.md
23. 23_AGENT_SESSION_MANAGEMENT.md
24. 24_AGENT_SECURITY_MODEL.md
24A. 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md
25. 25_AGENT_PERMISSION_MODEL.md
25A. 25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md
26. 26_AGENT_TENANT_ISOLATION.md
26A. 26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md
27. 27_AGENT_VERSIONING_MODEL.md
28. 28_AGENT_DEPLOYMENT_MODEL.md
29. 29_AGENT_OBSERVABILITY_MODEL.md
30. 30_AGENT_ANALYTICS_MODEL.md
31. 31_AGENT_TESTING_STRATEGY.md
32. 32_AGENT_FAILURE_HANDLING.md
33. 33_AGENT_EVALUATION_FRAMEWORK.md
34. 34_AGENT_GOVERNANCE_MODEL.md
35. 35_AGENT_TECHNOLOGY_REFERENCE_MAP.md

---

# Documentation Map

| Range | Focus |
|---|---|
| 01–06 | Agent purpose, architecture, lifecycle, identity, and configuration |
| 07–14 | Runtime, execution, state, context, instructions, persona, and capabilities |
| 15–21 | Tools, plugins, memory/knowledge boundaries, workflows, and events |
| 22–26 | Channel/session integration and agent-specific security, permission, and tenant controls |
| 27–30 | Versioning, deployment, observability, and analytics |
| 31–35 | Testing, failure handling, evaluation, governance, and technology references |

---

# Document Status and Ownership

The Agent Platform Owner is accountable for maintaining this module. Each document also has the cross-platform owners named in its boundaries and required-artifacts sections.

| Documents | Current declared status | Primary owner | Review expectation |
|---|---|---|---|
| 01–12 | Approved | Agent Platform Owner | Reconfirm only when a material architecture or dependency change occurs |
| 13–17 | Approved | Agent Platform Owner | Reconfirm on a material Agent or dependency architecture change |
| 18–20 | Deprecated | Agent Platform Owner | Retained as historical reference; do not use as the authoritative integration boundary |
| 18A–20A | Approved | Agent Platform Owner | Authoritative replacement boundaries for Agent consumption of Memory, Knowledge, and Integration workflow contracts |
| 21–23 | Approved | Agent Platform Owner | Reconfirm on a material Conversation, Digital Channel, Observability, or Testing contract change |
| 24–26 | Deprecated | Agent Platform Owner | Retained as historical reference; do not use as the authoritative security, authorization, or tenant boundary |
| 24A–26A | Approved | Agent Platform Owner | Authoritative Agent-to-Security, Authorization, and Tenant boundary documents |
| 27–35 | Approved | Agent Platform Owner | Reconfirm on a material Agent or dependency architecture change |
| README.md | Approved | Agent Platform Owner | Update when module map, ownership, or document status changes |

Document-level status, owner, last-review date, and approval evidence are maintained in each document header and the module governance record. A missing status is a documentation finding, not an implicit approval.

---

# Cross-Platform Boundaries

| Platform | Relationship to Agent Platform |
|---|---|
| 03_CONVERSATION_PLATFORM | Owns conversation lifecycle, state, context routing, and handoff; provides governed interaction/context contracts |
| 04_VOICE_PLATFORM | Owns telephony, media, speech, and voice-provider behavior; invokes the approved Agent Brain through controlled interfaces |
| 05_KNOWLEDGE_PLATFORM | Owns organizational knowledge, ingestion, retrieval, and knowledge governance |
| 06_MEMORY_PLATFORM | Owns user/customer memory, preferences, history, and memory lifecycle |
| 07_INTEGRATION_PLATFORM | Owns connector implementation, external APIs, webhooks, MCP, and third-party integrations |
| 08_DATA_PLATFORM | Owns persistence, cache, vector storage, analytics storage, backup, migration, and data lifecycle |
| 09_SECURITY_PLATFORM | Owns enterprise identity, authorization infrastructure, secrets, compliance, and security tooling |
| 11_OPERATIONS_PLATFORM | Owns incident, support, release, and service-management operations |
| 12_DEPLOYMENT_PLATFORM | Owns infrastructure, environments, CI/CD, runtime hosting, and deployment operations |
| 13_OBSERVABILITY_PLATFORM | Owns telemetry infrastructure, dashboards, alerting, and retention |
| 14_TESTING_PLATFORM | Owns shared testing infrastructure, environments, execution, and quality standards |
| 20_ENGINEERING | Owns shared packages, infrastructure code, protocols, and engineering utilities |

---

# Dependency Map

| Agent Platform concern | Required external platform contract or evidence |
|---|---|
| User interaction, conversation state, context routing, handoff | 03_CONVERSATION_PLATFORM |
| Voice, telephony, media, speech, call lifecycle | 04_VOICE_PLATFORM |
| Organizational knowledge and retrieval | 05_KNOWLEDGE_PLATFORM |
| Customer history, preferences, and memory lifecycle | 06_MEMORY_PLATFORM |
| External APIs, MCP, connectors, webhooks, and automation | 07_INTEGRATION_PLATFORM |
| Storage, cache, vector, retention, analytics data | 08_DATA_PLATFORM |
| Identity, authorization, secrets, compliance, and tenant security | 09_SECURITY_PLATFORM |
| Support, incident, service, and release operations | 11_OPERATIONS_PLATFORM |
| Infrastructure, environments, CI/CD, and runtime hosting | 12_DEPLOYMENT_PLATFORM |
| Telemetry infrastructure, dashboards, alerting, and retention | 13_OBSERVABILITY_PLATFORM |
| Shared test environments, runners, and quality standards | 14_TESTING_PLATFORM |

The Agent Platform can define how it uses these dependencies, but it cannot substitute for their authoritative contracts, data ownership, security controls, or operational procedures.

---

# Reading Paths by Role

| Role | Start with | Then focus on |
|---|---|---|
| Architect or product owner | 01–06, 24–28, 34–35 | Purpose, boundaries, risk, governance, versioning, deployment, technology decisions |
| AI or backend engineer | 06–17, 20–21, 27–32 | Configuration, runtime, execution, tools, workflows, events, versions, testing, failures |
| Security or privacy reviewer | 21–26, 31–34 | Events, channels, sessions, security, permissions, tenant isolation, testing, evaluation, governance |
| Operations or reliability engineer | 07, 21, 27–32, 34 | Runtime, events, versions, deployment, observability, analytics, testing, failures, governance |
| Channel or integration engineer | 15–22, 28–32 | Tools, workflows, events, channel boundaries, deployment, observability, testing, failures |
| AI coding assistant | 00_CONTROL first, then 01, 03, 06–08, 14–16, and relevant boundary documents | Ownership, current agent behavior, controlled action, and affected dependency contracts |

---

# Conversation Platform Boundary Note

The Conversation Platform is the authoritative owner of conversation lifecycle, conversation state, context routing, multi-channel conversation abstraction, and human-handoff coordination.

Agent documents that discuss sessions, channels, context, or handoff describe only the Agent Platform’s integration boundary and required controls. They do not transfer ownership of these concepts from 03_CONVERSATION_PLATFORM. Future Conversation Platform documentation must define the canonical contracts that Agent Platform implementations consume.

---

# Key Architecture Rules

- One approved Agent Brain serves all channels; channels do not fork agent intelligence.
- Agents are tenant-scoped, versioned, permission-controlled, and governed.
- Agent reasoning may propose work but cannot bypass deterministic authorization, workflow, tool, security, or delivery controls.
- External inputs, events, tool results, knowledge, and channel content are untrusted until validated and authorized.
- Agent Platform uses references and contracts to access Conversation, Knowledge, Memory, Integration, Data, Security, and Channel capabilities.
- Every material execution is traceable to a tenant, agent version, authorized trigger, policy decision, controlled actions, and outcome.
- High-impact behavior requires proportionate evaluation, approval, deployment, monitoring, failure handling, and governance evidence.

---

# Working With This Module

Before changing Agent Platform architecture or implementation:

1. Read the active 00_CONTROL project context, architecture principles, development guide, roadmap, decision log, and current status.
2. Identify the affected agent capability and cross-platform boundary.
3. Confirm that the Agent Platform owns the requested responsibility.
4. Review the related documents in this module and the owning external platform documents.
5. Record material architectural decisions through the project Decision Log or ADR process.
6. Update relevant documentation, tests, evaluation, deployment, observability, and governance evidence together.

No implementation should introduce a new provider, framework, tool, workflow, channel behavior, data path, or security model without following the applicable technology, security, permission, tenant, testing, and governance controls.

---

# Module Readiness

The Agent Platform documentation set is complete as an architecture set: all numbered documents through 35 and this module README are present. The current approval review reconciles the active and draft documents with the approved dependent platform architecture.

## Resolved Approval Findings

- `18_AGENT_MEMORY_INTEGRATION.md` is deprecated; `18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT.md` is the approved Agent-to-Memory boundary.
- `19_AGENT_KNOWLEDGE_INTEGRATION.md` is deprecated; `19A_AGENT_KNOWLEDGE_INTEGRATION_REWRITE_DRAFT.md` is the approved Agent-to-Knowledge boundary.
- `20_AGENT_WORKFLOW_INTEGRATION.md` is deprecated; `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` is the approved Agent-to-Integration workflow boundary.

The ownership findings are resolved. Memory, Knowledge, and Integration retain their respective domain ownership; Agent Platform consumes their governed contracts only.

## Final Approval Findings

- Documents 21–23 are approved after Digital Channel, Observability, Testing, Conversation, Security, and Integration boundary review. They consume approved contracts and do not own channel transport, canonical continuity, shared telemetry, or shared testing infrastructure.
- Documents 24–26 are deprecated; documents 24A–26A are their approved authoritative Agent-to-Security, Authorization, and Tenant replacements.

The module is approved as an architecture set but is not yet implementation-ready as a whole. Before implementation begins, the team must complete dependent Operations and Deployment contracts and pass the applicable validation, evaluation, governance, and coding-readiness reviews.

---

# Related Documents

## Current Approval Record

The complete Agent Platform architecture set was approved on 2026-08-08 after review of the Agent-to-Conversation, Digital Channel, Observability, Testing, Security, Data, Integration, Knowledge, and Memory boundaries. This is an architecture approval; implementation remains subject to the documented Operations, Deployment, validation, evaluation, governance, and coding-readiness gates.

- 00_CONTROL/PROJECT_CONTEXT.md
- 00_CONTROL/ARCHITECTURE_PRINCIPLES.md
- 00_CONTROL/AI_DEVELOPMENT_GUIDE.md
- 00_CONTROL/ROADMAP.md
- 00_CONTROL/DECISION_LOG.md
- 03_CONVERSATION_PLATFORM
- 04_VOICE_PLATFORM
- 05_KNOWLEDGE_PLATFORM
- 06_MEMORY_PLATFORM
- 07_INTEGRATION_PLATFORM
- 08_DATA_PLATFORM
- 09_SECURITY_PLATFORM
- 11_OPERATIONS_PLATFORM
- 12_DEPLOYMENT_PLATFORM
- 13_OBSERVABILITY_PLATFORM
- 14_TESTING_PLATFORM
- 20_ENGINEERING

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 3.6 | 2026-08-07 | Reconciled document 22 to the Digital Channel boundary: adapters enter canonical Conversation before Agent execution. |
| 2.0 | 2026-08-05 | Completed Agent Platform module index, boundaries, reading order, and documentation map. |
| 2.1 | 2026-08-05 | Added document status, ownership, dependency map, role reading paths, Conversation boundary, readiness, and final module guidance. |
| 2.2 | 2026-08-07 | Corrected declared document statuses and recorded the active cross-platform approval review. |
| 2.3 | 2026-08-07 | Recorded cross-platform ownership findings that must be resolved before Agent Platform approval. |
| 2.4 | 2026-08-07 | Moved Memory, Knowledge, and Workflow integration documents to Draft pending ownership re-scoping; recorded the Workflow document's legacy structural defect. |
| 2.5 | 2026-08-07 | Added the controlled Workflow integration replacement draft while preserving the legacy document for historical reference. |
| 2.6 | 2026-08-07 | Added the controlled Memory integration replacement draft while preserving the legacy document for historical reference. |
| 2.7 | 2026-08-07 | Added the controlled Knowledge integration replacement draft while preserving the legacy document for historical reference. |
| 2.8 | 2026-08-07 | Approved the Memory, Knowledge, and Workflow integration replacements; deprecated the three legacy documents without deleting them. |
| 2.9 | 2026-08-07 | Reconciled legacy integration references and recorded approval gates for Event, Channel, Session, Security, Permission, and Tenant-isolation documents. |
| 3.0 | 2026-08-07 | Added the controlled Agent Security boundary replacement draft. |
| 3.1 | 2026-08-07 | Added the controlled Agent Authorization boundary replacement draft. |
| 3.2 | 2026-08-07 | Added the controlled Agent Tenant boundary replacement draft. |
| 3.3 | 2026-08-07 | Approved the Security, Authorization, and Tenant replacements; deprecated the three legacy documents without deleting them. |
| 3.4 | 2026-08-07 | Approved documents 27–35 after cross-platform reference and ownership audit. |
| 3.5 | 2026-08-07 | Approved documents 13–17 after cross-platform reference and ownership audit. |
