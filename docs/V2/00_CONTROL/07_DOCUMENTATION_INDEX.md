# 07_DOCUMENTATION_INDEX

**Version:** 2.41

**Status:** Approved

---

# Overview

This document provides the master index for the AI Workforce Platform documentation system.

It defines the organization, location, purpose, ownership reference, and status of documentation across the project.

The Documentation Index acts as the navigation layer for engineers, architects, contributors, and AI assistants.

---

# Purpose

The purpose of this document is to:

- Provide a complete documentation map.
- Identify where information belongs.
- Prevent duplicate documentation.
- Identify authoritative sources.
- Improve documentation discovery.
- Support documentation maintenance.

---

# Documentation Organization

The documentation follows this structure:

```
00_CONTROL

        ↓

01_ARCHITECTURE

        ↓

02_AGENT_PLATFORM

        ↓

03_CONVERSATION_PLATFORM

        ↓

04_VOICE_PLATFORM

        ↓

05_KNOWLEDGE_PLATFORM

        ↓

06_MEMORY_PLATFORM

        ↓

07_INTEGRATION_PLATFORM

        ↓

08_DATA_PLATFORM

        ↓

09_SECURITY_PLATFORM

        ↓

11_OPERATIONS_PLATFORM
```

Each directory represents a major governance area or platform capability.

---

# Documentation Discovery Rules

New documentation must be placed according to its primary responsibility.

## Governance

Location:

```
00_CONTROL
```

Examples:

- Project management
- Documentation standards
- Decision records
- Change management

---

## System Architecture

Location:

```
01_ARCHITECTURE
```

Examples:

- Platform architecture
- System flows
- Cross-platform design
- Architecture patterns

---

## Platform Capability

Location:

Platform-specific directories.

Examples:

```
02_AGENT_PLATFORM

04_VOICE_PLATFORM

05_KNOWLEDGE_PLATFORM
```

Use these locations for capability-specific design and implementation documentation.

---

## Implementation Details

Implementation documentation should live close to the platform or service it describes.

Avoid placing implementation details in governance documents.

---

# Authoritative Source Mapping

Each major topic has one primary source of truth.

| Topic | Authoritative Document |
|---|---|
| Project vision | 01_PROJECT_CHARTER.md |
| Project sequence | 02_PROJECT_ROADMAP.md |
| Architecture rules | 03_ARCHITECTURE_PRINCIPLES.md |
| Capability ownership | 04_SYSTEM_BOUNDARIES.md |
| Module responsibilities | 05_MODULE_OWNERSHIP.md |
| Documentation rules | 06_DOCUMENTATION_STANDARDS.md |
| Architectural decisions | 08_DECISION_LOG.md |
| Project changes | 09_CHANGE_MANAGEMENT.md |
| Project state | 10_PROJECT_STATUS.md |
| Terminology | 11_TERMINOLOGY_GLOSSARY.md |

Other documents should reference these sources instead of duplicating their content.

---

# Documentation Registry

The following table tracks the current documentation structure.

| Directory | Purpose | Status | Owner | Last Updated |
|---|---|---|---|---|
| 00_CONTROL | Project governance and standards | Active | Architecture Owner | 2026-08-03 |
| 01_ARCHITECTURE | System architecture | Approved | Architecture Owner | 2026-08-09 |
| 18_ARCHITECTURE_DIAGRAMS | Governed cross-platform visual architecture references | Approved; PNG/reviewer finalization pending | Architecture Owner | 2026-08-09 |
| 16_PLATFORM_FOUNDATION | Tenant-aware SaaS control plane | Approved | Platform Foundation Owner | 2026-08-07 |
| 02_AGENT_PLATFORM | AI agent capabilities | Approved | Agent Platform Owner | 2026-08-08 |
| 03_CONVERSATION_PLATFORM | Conversation capabilities | Approved | Conversation Platform Owner | 2026-08-06 |
| 04_VOICE_PLATFORM | Voice capabilities | Approved | Voice Platform Owner | 2026-08-06 |
| 17_DIGITAL_CHANNEL_PLATFORM | Non-voice participant channels | Approved | Digital Channel Platform Owner | 2026-08-08 |
| 05_KNOWLEDGE_PLATFORM | Knowledge and RAG capabilities | Approved | Knowledge Platform Owner | 2026-08-06 |
| 06_MEMORY_PLATFORM | Memory capabilities | Approved | Memory Platform Owner | 2026-08-06 |
| 07_INTEGRATION_PLATFORM | External integrations | Approved | Integration Platform Owner | 2026-08-06 |
| 08_DATA_PLATFORM | Data capabilities | Approved | Data Platform Owner | 2026-08-07 |
| 09_SECURITY_PLATFORM | Security capabilities | Approved | Security Platform Owner | 2026-08-07 |
| 10_FRONTEND_PLATFORM | User and operator interfaces | Approved | Frontend Platform Owner | 2026-08-08 |
| 11_OPERATIONS_PLATFORM | Operations capabilities | Approved | Operations Platform Owner | 2026-08-09 |
| 12_DEPLOYMENT_PLATFORM | Delivery infrastructure | Approved | Deployment Platform Owner | 2026-08-09 |
| 13_OBSERVABILITY_PLATFORM | Platform telemetry | Approved | Observability Platform Owner | 2026-08-09 |
| 14_TESTING_PLATFORM | Quality assurance | Approved | Testing Platform Owner | 2026-08-09 |
| 15_EXAMPLES | Safe reference scenarios and contract examples | Approved | Architecture Owner | 2026-08-09 |
| 20_ENGINEERING | Implementation-planning bridge and first vertical-slice delivery record | Approved | Engineering Owner | 2026-08-09 |

---

# 00_CONTROL

Purpose:

Project governance, standards, decisions, and documentation management.

| File | Purpose | Status |
|---|---|---|
| README.md | Control directory overview | Approved |
| 01_PROJECT_CHARTER.md | Project vision and objectives | Approved |
| 02_PROJECT_ROADMAP.md | Development phases and milestones | Approved |
| 03_ARCHITECTURE_PRINCIPLES.md | Architectural rules | Approved |
| 04_SYSTEM_BOUNDARIES.md | Capability ownership boundaries | Approved |
| 05_MODULE_OWNERSHIP.md | Platform responsibilities | Approved |
| 06_DOCUMENTATION_STANDARDS.md | Documentation rules | Approved |
| 07_DOCUMENTATION_INDEX.md | Documentation navigation map | Approved |
| 08_DECISION_LOG.md | Important decisions | Approved |
| 09_CHANGE_MANAGEMENT.md | Change process | Approved |
| 10_PROJECT_STATUS.md | Current project state | Approved |
| 11_TERMINOLOGY_GLOSSARY.md | Standard terminology | Approved |
| AI_DRIVEN_ENTERPRISE_SAAS_DEVELOPMENT_PLAYBOOK.md | AI-assisted implementation operating guide; references the authoritative governance and platform documents. | Approved |

---

# Platform Documentation Index

## 01_ARCHITECTURE

Purpose:

Defines the system-level logical architecture: One Brain, Multi-Channel, ownership and layers, multi-tenant boundaries, system data/event flows, capability relationships, and architecture-principle application.

Status:

Approved

Owner:

Architecture Owner

Current README:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Architecture navigation, ownership, document set, invariants, and initial implementation boundary. | 2.1 | Approved |

Approved documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| 01_SYSTEM_OVERVIEW.md | Defines system purpose, scope, architectural vision, domains, and goals. | 2.1 | Approved |
| 02_ONE_BRAIN_MULTI_CHANNEL.md | Defines centralized intelligence, channel boundaries, continuity, and interaction invariants. | 2.1 | Approved |
| 03_PLATFORM_LAYER_MODEL.md | Defines logical layers, ownership, dependency direction, and cross-cutting capabilities. | 2.1 | Approved |
| 04_MULTI_TENANT_ARCHITECTURE.md | Defines tenant boundaries and isolation architecture. | 2.1 | Approved |
| 05_SYSTEM_DATA_FLOW.md | Defines governed system data movement and lifecycle boundaries. | 2.1 | Approved |
| 06_EVENT_DRIVEN_ARCHITECTURE.md | Defines event patterns, contracts, reliability, and ownership boundaries. | 2.1 | Approved |
| 07_HIGH_LEVEL_SERVICE_MAP.md | Defines high-level capability relationships and service map. | 2.1 | Approved |
| 08_ARCHITECTURE_PRINCIPLES_APPLICATION.md | Defines practical architecture application, feature checks, and review path. | 2.1 | Approved |

Completed:

The complete 01_ARCHITECTURE document set, including module navigation and Documents 01-08, was approved on 2026-08-09. It is the current system-level architecture reference for all platform implementation planning.

---

## 02_AGENT_PLATFORM

Purpose:

Defines AI agent capabilities.

Expected topics:

- Agent architecture
- Agent lifecycle
- Agent runtime
- Prompt management
- Tool orchestration

Status:

Draft / approval review

The complete 35-document Agent Platform draft set is present. Its approval review is reconciling Agent boundaries with the approved Conversation, Voice, Knowledge, Memory, Integration, Data, Security, and Platform Foundation modules before the set is finalized.

---

## 03_CONVERSATION_PLATFORM

Purpose:

Defines conversation management.

Status:

Approved

Owner:

Conversation Platform Owner

The planned Conversation Platform document set is complete. It is undergoing cross-module approval review before its documents are marked Approved.

Authoritative documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines the module navigation, ownership summary, reading order, and approval status. | 1.2 | Approved |
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform ownership, components, canonical model, and boundaries. | 2.4 | Approved |
| 02_CONVERSATION_LIFECYCLE.md | Defines canonical lifecycle states, transition authority, timing, and recovery. | 2.4 | Approved |
| 03_CONVERSATION_MODEL.md | Defines canonical conversation entities, relationships, and references. | 2.4 | Approved |
| 04_CONVERSATION_SESSION_MODEL.md | Defines bounded sessions, continuity, concurrency, and recovery. | 2.4 | Approved |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines authorized conversation context snapshots and lifecycle. | 2.4 | Approved |
| 06_CONVERSATION_ROUTING.md | Defines destination selection, response ownership, fallback, and routing governance. | 2.4 | Approved |
| 07_CONVERSATION_EVENTS.md | Defines Conversation-owned event semantics, publication, consumption, and replay controls. | 2.4 | Approved |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines controlled transfer, collaboration, return, and handoff recovery. | 2.4 | Approved |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines canonical state integrity, concurrency, projections, reconciliation, and repair. | 2.4 | Approved |
| 10_CONVERSATION_SECURITY.md | Defines conversation-specific authorization, trust, revocation, and incident requirements. | 2.4 | Approved |
| 11_CONVERSATION_OBSERVABILITY.md | Defines conversation-domain telemetry, indicators, alerts, and diagnostics. | 2.4 | Approved |
| 12_CONVERSATION_TESTING.md | Defines risk-based validation, safe fixtures, release evidence, and regression coverage. | 2.4 | Approved |

Approval dependency:

- Agent documents 21–23 define the corresponding Agent integration boundaries and remain Draft. Their contracts must stay aligned with the Conversation Platform before either module is approved.

Primary topics:

- Conversation lifecycle
- Participants and normalized interactions
- Sessions and multi-channel continuity
- Context, routing, handoff, state, and events
- Security, observability, and testing

---

## 04_VOICE_PLATFORM

Purpose:

Defines voice communication capabilities.

Status:

Approved

Owner:

Voice Platform Owner

Current documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Voice Platform navigation, ownership, boundaries, and the approved document set. | 1.16 | Approved |
| 01–15 Voice Platform documents | Define approved Voice architecture, channel, lifecycle, media, speech, telephony, provider, governance, security, isolation, reliability, observability, testing, and technology boundaries. | Current | Approved |

Planned topics:

- Voice architecture
- Telephony
- Speech pipeline
- Call lifecycle

---

## 05_KNOWLEDGE_PLATFORM

Purpose:

Defines business knowledge capabilities.

Expected topics:

- Knowledge ingestion
- RAG architecture
- Retrieval systems
- Knowledge management

---

## 06_MEMORY_PLATFORM

Purpose:

Defines memory capabilities.

Expected topics:

- Memory architecture
- User memory
- Long-term context
- Memory policies

---

## 07_INTEGRATION_PLATFORM

Purpose:

Defines external system connectivity.

Status:

Review

Current documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Integration Platform navigation, ownership, boundaries, and the approved document set. | 1.18 | Approved |
| 01_INTEGRATION_PLATFORM_ARCHITECTURE.md | Defines the governed external-action architecture and cross-platform execution boundary. | 1.2 | Approved |
| 02_INTEGRATION_DOMAIN_MODEL.md | Defines provider-neutral Integration entities, identifiers, action states, and evidence. | 1.1 | Approved |
| 03_TOOL_AND_CONNECTOR_REGISTRY.md | Defines connector, tool, capability, profile, availability, versioning, and lifecycle governance. | 1.1 | Approved |
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines connector account bindings, delegated grants, credential leases, rotation, revocation, and audit. | 1.1 | Approved |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines action risk, current authorization guard, confirmation, approval, separation of duties, and audit. | 1.1 | Approved |
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines guarded dispatch, idempotency, normalized outcomes, retry, fallback, and reconciliation. | 1.1 | Approved |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Defines bounded asynchronous workflows, steps, waits, callbacks, compensation, and recovery. | 1.1 | Approved |
| 08_EXTERNAL_API_AND_MCP_BOUNDARY.md | Defines versioned Integration APIs, events, and MCP-compatible tool/resource exposure. | 1.1 | Approved |
| 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md | Defines external callback validation, normalization, replay, ordering, and reconciliation. | 1.1 | Approved |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines tenant, subject, purpose, connector, credential, action, and external-resource isolation. | 1.1 | Approved |
| 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md | Defines integration decision rights, separation of duties, lifecycle governance, and audit evidence. | 1.1 | Approved |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines external trust, data egress, credential, injection, supply-chain, and incident controls. | 1.1 | Approved |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines safe outcomes, retries, fallback, circuits, bulkheads, reconciliation, and recovery. | 1.1 | Approved |
| 14_INTEGRATION_OBSERVABILITY.md | Defines Integration signals, SLOs, diagnostics, alerts, privacy, and data quality. | 1.1 | Approved |
| 15_INTEGRATION_TESTING.md | Defines Integration contract, adapter, safety, journey, resilience, and release evidence. | 1.1 | Approved |
| 16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP.md | Defines bounded technology roles for APIs, webhooks, MCP, workflows, connector SDKs, and exit. | 1.1 | Approved |

Expected topics:

- Connectors
- Tools
- Automation
- External APIs

---

## 08_DATA_PLATFORM

Purpose:

Defines data capabilities.

Status:

Approved

The complete Data Platform set, consisting of the module README and documents 01â€“14, is approved. It is authoritative for shared persistence, PostgreSQL/pgvector, lifecycle, recovery, tenant isolation, residency, reliability, observability, testing, and technology boundaries.

Expected topics:

- Data architecture
- Storage
- Database design
- Data lifecycle

---

## 09_SECURITY_PLATFORM

Purpose:

Defines security capabilities.

Status:

Approved

The complete Security Platform set, consisting of the module README and documents 01â€“15, is approved. It is authoritative for identity, authorization, secrets, cryptography, service trust, security evidence, compliance, incident response, resilience, observability, testing, and technology boundaries.

Expected topics:

- Identity
- Access control
- Compliance
- Security controls

---

## 11_OPERATIONS_PLATFORM

Purpose:

Defines operational coordination for incident and service management, on-call and runbooks, release readiness, maintenance, support communication, and continual improvement without duplicating Security, Data, Deployment, Observability, Testing, or domain ownership.

Status:

Approved

Owner:

Operations Platform Owner

Current README:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Operations navigation, ownership boundaries, approved document set, delivery boundary, and change rules. | 1.1 | Approved |

Approved documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| 01_OPERATIONS_PLATFORM_ARCHITECTURE.md | Defines Operations ownership, lifecycle, responsibilities, runbook/recovery requirements, and the initial vertical slice. | 1.1 | Approved |
| 02_INCIDENT_AND_SERVICE_MANAGEMENT.md | Defines incident/service intake, severity, escalation, response, closure, and learning. | 1.1 | Approved |
| 03_OPERATIONAL_RUNBOOKS_AND_ON_CALL.md | Defines runbook governance, on-call roles, handoffs, paging, safety, and exercises. | 1.1 | Approved |
| 04_RELEASE_READINESS_AND_CHANGE_COORDINATION.md | Defines readiness, go/no-go, change-window, rollout, abort/recovery, and post-change coordination. | 1.1 | Approved |
| 05_SERVICE_HEALTH_CAPACITY_AND_MAINTENANCE.md | Defines health, capacity/dependency planning, maintenance, provider degradation, and controlled degradation. | 1.1 | Approved |
| 06_OPERATIONS_SUPPORT_AND_CUSTOMER_COMMUNICATION.md | Defines support routing, verified service communication, request handoff, closure, and feedback. | 1.1 | Approved |
| 07_OPERATIONAL_GOVERNANCE_AND_CONTINUAL_IMPROVEMENT.md | Defines operational review, decisions, corrective actions, problem management, and effectiveness review. | 1.1 | Approved |

Cross-platform dependencies:

- 09_SECURITY_PLATFORM owns security, privacy, authorization, incident-policy, and sensitive-evidence controls; Operations coordinates only within those controls.
- 08_DATA_PLATFORM owns data lifecycle, restore, retention, and legal-hold controls; Operations coordinates recovery impact and communication.
- 12_DEPLOYMENT_PLATFORM owns environments, CI/CD, infrastructure delivery, and rollback mechanisms; Operations owns operational readiness and release coordination.
- 13_OBSERVABILITY_PLATFORM owns telemetry, alerting, and investigation infrastructure; Operations consumes approved evidence and owns response process.
- 14_TESTING_PLATFORM owns shared assurance methods and evidence conventions; Operations requires proportionate operational/recovery evidence.

Completed:

The complete 11_OPERATIONS_PLATFORM architecture set, including module navigation and Documents 01–07, was approved on 2026-08-09. It is the current source of truth for operational coordination, incident/service management, on-call/runbooks, release readiness, health/capacity, support communication, and continual improvement.

---

## 12_DEPLOYMENT_PLATFORM

Purpose:

Defines delivery infrastructure and execution for environments, infrastructure-as-code, CI/CD, artifact provenance, configuration and secret integration, controlled releases, rollback, delivery resilience, assurance, and technology adoption without duplicating Operations, Security, Data, Observability, Testing, or domain ownership.

Status:

Approved

Owner:

Deployment Platform Owner

Current README:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Deployment navigation, ownership boundaries, approved document set, delivery boundary, and change rules. | 1.1 | Approved |

Approved documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| 01_DEPLOYMENT_PLATFORM_ARCHITECTURE.md | Defines Deployment ownership, environment/delivery architecture, lifecycle, controls, and initial vertical slice. | 1.1 | Approved |
| 02_ENVIRONMENT_AND_INFRASTRUCTURE_MODEL.md | Defines environment topology, infrastructure lifecycle, isolation, connectivity, capacity, drift, and retirement. | 1.1 | Approved |
| 03_CI_CD_AND_ARTIFACT_SUPPLY_CHAIN.md | Defines CI/CD, artifact provenance, promotion, gates, lifecycle, and emergency control. | 1.1 | Approved |
| 04_DEPLOYMENT_CONFIGURATION_AND_SECRETS_INTEGRATION.md | Defines classified configuration, Security-managed secret integration, rollout, rotation, and drift. | 1.1 | Approved |
| 05_DEPLOYMENT_RELEASE_AND_ROLLBACK_STRATEGY.md | Defines staged release, hold, abort, rollback/recovery, compatibility, and retirement. | 1.1 | Approved |
| 06_DEPLOYMENT_SECURITY_AND_ACCESS_CONTROL.md | Defines secure delivery access, workload identity, privileged access, audit, and revocation. | 1.1 | Approved |
| 07_DEPLOYMENT_OBSERVABILITY_RELIABILITY_AND_DISASTER_RECOVERY.md | Defines delivery resilience, recovery execution, observability integration, and exercises. | 1.1 | Approved |
| 08_DEPLOYMENT_TESTING_AND_ASSURANCE.md | Defines delivery-specific test/assurance responsibilities, gates, and evidence. | 1.1 | Approved |
| 09_DEPLOYMENT_TECHNOLOGY_REFERENCE_MAP.md | Defines approved technology roles, adoption/exit controls, and anti-patterns. | 1.1 | Approved |

Cross-platform dependencies:

- 11_OPERATIONS_PLATFORM owns readiness, go/no-go, incident command, support, and communication; Deployment executes approved delivery and recovery mechanisms.
- 09_SECURITY_PLATFORM owns identity, authorization, secrets, supply-chain policy, exceptions, and security incident authority; Deployment integrates the controls.
- 08_DATA_PLATFORM owns data migration semantics, lifecycle, recovery, and validation; Deployment supplies approved delivery hooks and infrastructure dependencies.
- 13_OBSERVABILITY_PLATFORM owns telemetry/alerting infrastructure and safe signal policy; Deployment supplies delivery/environment evidence through approved contracts.
- 14_TESTING_PLATFORM owns shared methods, environments, reporting, and evidence conventions; Deployment provides delivery assurance under those standards.

Completed:

The complete 12_DEPLOYMENT_PLATFORM architecture set, including module navigation and Documents 01-09, was approved on 2026-08-09. It is the current source of truth for controlled environments, CI/CD, infrastructure, secure configuration, release/rollback, delivery resilience, and deployment assurance.

---

## 16_PLATFORM_FOUNDATION

Purpose:

Defines the tenant-aware SaaS control plane for organizations, memberships, configuration, entitlements, API entry, and service discovery.

Status:

Approved

Owner:

Platform Foundation Owner

Current README:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines module navigation, ownership boundaries, the approved document set, cross-platform relationships, and change rules. | 1.3 | Approved |

Approved documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| 01_PLATFORM_FOUNDATION_ARCHITECTURE.md | Defines Platform Foundation ownership, control-plane architecture, contracts, lifecycle boundaries, and implementation rules. | 1.1 | Approved |
| 02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md | Defines tenant, organization, workspace, membership, and lifecycle facts. | 1.2 | Approved |
| 03_CONFIGURATION_AND_ENTITLEMENT_MODEL.md | Defines governed configuration, defaults, feature entitlement, rollout, and reversal rules. | 1.2 | Approved |
| 04_API_EDGE_AND_SERVICE_DISCOVERY.md | Defines gateway admission, routing, versioning, service discovery, and contract boundaries. | 1.2 | Approved |
| 05_FOUNDATION_SECURITY_AND_TENANT_ISOLATION.md | Defines application of Security controls to Foundation records and operations. | 1.2 | Approved |
| 06_FOUNDATION_OBSERVABILITY_AND_RELIABILITY.md | Defines Foundation signals, safe degradation, reconciliation, recovery, and reliability requirements. | 1.2 | Approved |
| 07_FOUNDATION_TESTING.md | Defines Foundation-domain proof obligations, test coverage, release gates, and evidence. | 1.2 | Approved |

Cross-platform dependencies:

- 09_SECURITY_PLATFORM supplies identity, authorization, secrets, audit, and compliance controls; Foundation supplies tenant and membership facts as authorized inputs.
- 08_DATA_PLATFORM supplies approved persistence and data-lifecycle mechanisms; Foundation owns logical control-plane records and requirements.
- All domain platforms consume tenant, membership, configuration, entitlement, and API-edge contracts while retaining their own domain records and policies.
- 07_INTEGRATION_PLATFORM may expose approved external developer-facing routes; Foundation owns shared gateway admission and route policy, not connector behavior.
- 10_FRONTEND_PLATFORM consumes organization, membership, configuration, and entitlement contracts; Frontend owns the user experience.

Completion and reconfirmation history:

- 2026-08-07: The README and Document 01 were approved.
- 2026-08-07: Documents 02â€“07 were approved, completing the Platform Foundation architecture-document set.
- 2026-08-07: Documents 02â€“07 were reopened and expanded after completeness review; the complete approved set was reconfirmed.

---

## 20_ENGINEERING

Purpose:

Defines the implementation-planning bridge from approved V2 architecture to safe, traceable coding and controlled delivery.

Status:

Approved

Owner:

Engineering Owner

Current README:

| File | Purpose | Version | Status |
|---|---|---|---|
| README.md | Defines Engineering ownership, pre-coding rules, document set, and implementation boundary. | 1.2 | Approved |

Approved documents:

| File | Purpose | Version | Status |
|---|---|---|---|
| 01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md | Defines the smallest safe end-to-end build sequence, dependencies, acceptance criteria, and evidence. | 1.1 | Approved |
| 02_ENGINEERING_WORKSPACE_AND_MODULE_STRUCTURE.md | Defines source-code organization, package/module boundaries, dependencies, and safe workspace setup. | 1.1 | Approved |
| 03_ENGINEERING_DELIVERY_WORKFLOW.md | Defines implementation, validation, release, recovery, and evidence workflow. | 1.1 | Approved |
| 04_IMPLEMENTATION_DECISION_AND_TRACEABILITY.md | Defines durable links between authority, decisions, code, tests, delivery, and operating evidence. | 1.1 | Approved |

Completion:

The initial Engineering implementation-planning set was completed on 2026-08-09. It is the approved entry point for beginning the first vertical-slice codebase after the remaining documentation finalization work is closed.

---

# Deprecated Documentation Archive

Deprecated documents must not be deleted.

They should remain available for:

- Historical reference
- Migration context
- Understanding previous decisions

Deprecated documents should record:

- Original location
- Replacement document
- Deprecation date

Example:

| Document | Replacement | Status |
|---|---|---|
| OLD_DOCUMENT.md | NEW_DOCUMENT.md | Deprecated |

---

# Index Maintenance Rules

This index must be updated when:

- A new documentation directory is created.
- A document is added or removed.
- A document changes location.
- A document status changes.
- A document becomes deprecated.
- Ownership changes.

---

# Related Documents

- README.md
- 06_DOCUMENTATION_STANDARDS.md
- 08_DECISION_LOG.md
- 09_CHANGE_MANAGEMENT.md

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-03 | Initial documentation index structure. |
| 2.1 | 2026-08-03 | Added discovery rules, authoritative sources, registry tracking, and archive handling. |
| 2.2 | 2026-08-06 | Registered the completed Conversation Platform document set and its Draft/Under Review approval state. |
| 2.3 | 2026-08-06 | Added the Conversation Platform module README to the authoritative document map. |
| 2.4 | 2026-08-06 | Moved the Conversation Platform document set to Review after the internal approval audit. |
| 2.5 | 2026-08-06 | Approved the Conversation Platform document set as the current architecture source of truth. |
| 2.6 | 2026-08-06 | Registered the Voice Platform module README and Draft status. |
| 2.7 | 2026-08-06 | Registered Platform Foundation and Digital Channel Platform and refreshed module status coverage. |
| 2.8 | 2026-08-06 | Recorded approval of the complete Memory Platform architecture set. |
| 2.9 | 2026-08-06 | Recorded approval of the complete Voice Platform architecture set. |
| 2.10 | 2026-08-06 | Recorded approval of the Integration Platform Architecture document and module review status. |
| 2.11 | 2026-08-06 | Recorded approval of the Integration Domain Model. |
| 2.12 | 2026-08-06 | Recorded approval of the Tool and Connector Registry. |
| 2.13 | 2026-08-06 | Recorded approval of Connector Authentication and Credential Delegation. |
| 2.14 | 2026-08-06 | Recorded approval of Action Authorization and Approval. |
| 2.15 | 2026-08-06 | Recorded approval of Action Execution and Idempotency. |
| 2.16 | 2026-08-06 | Recorded approval of Workflow and Asynchronous Execution. |
| 2.17 | 2026-08-06 | Recorded approval of the External API and MCP Boundary. |
| 2.18 | 2026-08-06 | Recorded approval of the Webhook and External Event Model. |
| 2.19 | 2026-08-06 | Recorded approval of Integration Access and Tenant Isolation. |
| 2.20 | 2026-08-06 | Recorded approval of Integration Governance and Audit. |
| 2.21 | 2026-08-06 | Recorded approval of Integration Security and Privacy. |
| 2.22 | 2026-08-06 | Recorded approval of Integration Reliability and Failure Handling. |
| 2.23 | 2026-08-06 | Recorded approval of Integration Observability. |
| 2.24 | 2026-08-06 | Recorded approval of Integration Testing. |
| 2.25 | 2026-08-06 | Recorded approval of the complete Integration Platform architecture set. |
| 2.26 | 2026-08-06 | Recorded approval of the Data Platform Architecture document. |
| 2.27 | 2026-08-06 | Recorded approval of the Data Domain Model. |
| 2.28 | 2026-08-07 | Recorded approval of Data Storage and PostgreSQL Architecture. |
| 2.29 | 2026-08-07 | Registered the Architecture Diagrams module and its approved diagram-governance README. |
| 2.30 | 2026-08-07 | Registered the finalized AI-Driven Enterprise SaaS Development Playbook as an approved governance operating guide. |
| 2.31 | 2026-08-07 | Registered the seven approved Platform Foundation documents, current README status, cross-platform dependencies, and completion/reconfirmation history. |
| 2.32 | 2026-08-07 | Reconciled registry status for Data and Agent, updated approved Control records, and recorded the completed Data and Security architecture sets. |
| 2.33 | 2026-08-07 | Registered completion of the initial nine-document Digital Channel architecture set in Draft, pending cross-platform approval. |
| 2.34 | 2026-08-07 | Registered initial Draft shared Observability and Testing contracts required for platform approval review. |
| 2.35 | 2026-08-08 | Approved the initial shared Observability and Testing contracts after cross-platform boundary review. |
| 2.36 | 2026-08-08 | Approved the complete Digital Channel architecture set after cross-platform boundary review. |
| 2.37 | 2026-08-08 | Approved the complete Agent Platform architecture set after cross-platform boundary review. |
| 2.38 | 2026-08-08 | Started the detailed Frontend Platform architecture set with the application-composition boundary draft. |
| 2.39 | 2026-08-08 | Approved the complete Frontend Platform architecture set after cross-platform boundary review. |
| 2.40 | 2026-08-09 | Registered the complete Engineering implementation-planning set and its approved pre-coding boundary. |
| 2.41 | 2026-08-09 | Reconciled registry dates and top-level coverage for Observability, Testing, Examples, Engineering, and Architecture Diagram finalization. |
| 2.26 | 2026-08-06 | Registered the Data Platform module README and Draft status. |
| 2.27 | 2026-08-06 | Recorded approval of the Data Platform navigation and boundary README. |
