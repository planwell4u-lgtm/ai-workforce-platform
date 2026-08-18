# 35_AGENT_TECHNOLOGY_REFERENCE_MAP

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document maps the technology categories, reference sources, ownership boundaries, and adoption status relevant to the Agent Platform.

It is a decision-support and traceability document, not a technology-selection mandate. The map helps engineers and AI assistants understand which technologies may support an Agent Platform capability, where the authoritative technical decision belongs, what boundaries must be preserved, and what review is required before adoption.

---

# Purpose

The purpose of the Agent Technology Reference Map is to keep the Agent Platform implementation model-agnostic, modular, and maintainable while connecting architecture to approved technical references.

It prevents accidental vendor coupling, duplicate capability ownership, undocumented dependencies, and implementation choices that bypass project governance, security, tenant isolation, evaluation, deployment, or operational review.

---

# Objectives

The Agent Technology Reference Map must:

- Map Agent Platform capabilities to technology categories and authoritative owners.
- Identify approved, planned, reference-only, deprecated, and prohibited technology use.
- Preserve One Brain, Multi-Channel and platform ownership boundaries.
- Distinguish architecture concepts from framework, provider, SDK, protocol, and infrastructure choices.
- Require official documentation, compatibility, security, tenant, evaluation, deployment, and operational review before adoption.
- Support replaceability, version tracking, dependency inventory, and controlled retirement.
- Help implementation teams choose within approved boundaries without silently creating new architecture.
- Remain useful as vendors, models, frameworks, and infrastructure evolve.

---

# Scope

This document defines:

- Technology categories relevant to Agent Platform capabilities.
- Ownership and boundary mapping for technologies used by Agent Platform.
- Adoption status, reference review, compatibility, lifecycle, and change-management requirements.
- Required technical reference artifacts and implementation decision evidence.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Final technology selection, contract, budget, procurement, licensing, or vendor agreement | Architecture, Engineering, Security, Procurement, and tenant governance owners |
| Infrastructure, deployment, cluster, network, CI/CD, and runtime-hosting technology | 12_DEPLOYMENT_PLATFORM and 20_ENGINEERING |
| Voice/media, telephony, SIP, WebRTC, speech, and provider implementation selection | 04_VOICE_PLATFORM |
| Channel-client/provider implementation selection | Relevant Channel Platform |
| Data storage, cache, vector store, analytics engine, backup, and migration technology | 08_DATA_PLATFORM |
| Enterprise identity, secrets, security tooling, SIEM, and compliance technology | 09_SECURITY_PLATFORM |
| Shared testing, evaluation execution, or observability tooling implementation | 14_TESTING_PLATFORM and 13_OBSERVABILITY_PLATFORM |
| Project-level approved reference registry | 00_CONTROL architecture reference registry and Decision Log |

---

# Reference Map Principles

## Technology Supports a Capability; It Does Not Own It

An LLM SDK, orchestration framework, tool protocol, vector store, queue, or provider is an implementation option. It does not change the platform owner of agent reasoning, conversation, knowledge, memory, integration, data, security, or channels.

## Adopt Ideas, Not Architectures

External projects, starter repositories, and framework examples may inform patterns but do not define this platform’s module boundaries, multi-tenant model, business logic, or governance. Adoption follows the project architecture, not the reverse.

## Prefer Official and Replaceable Interfaces

Official documentation, supported APIs, open standards, and bounded adapters are preferred. Provider-specific behavior is isolated behind owned contracts so that an alternative can be evaluated without redesigning the Agent Brain.

## No Hidden Latest Dependency

Production agent versions reference approved provider/model/configuration and dependency versions through governed manifests. Mutable latest references, unreviewed SDK upgrades, and undocumented provider fallbacks are prohibited for material behavior.

## Technology Choice Is a Controlled Change

A new technology, material provider/model change, protocol adoption, or architecture-affecting SDK requires review of ownership, security, tenant isolation, data classification, contract, testing, evaluation, deployment, observability, operations, cost, and exit implications.

---

# Capability-to-Technology Map

| Agent Platform capability | Technology category | Typical examples or reference types | Primary owner |
|---|---|---|---|
| Agent reasoning and model invocation | Model provider abstraction and model API | OpenAI APIs, other approved model providers, model gateway | Agent Platform |
| Agent execution orchestration | Agent runtime and orchestration framework | Controlled runtime implementation, LangGraph-style orchestration reference | Agent Platform |
| Instructions and structured output | Prompt/configuration, schema validation, policy-aware response control | Versioned instructions, structured output schema, validation library | Agent Platform |
| Capability selection | Internal capability registry and policy interface | Capability registry, decision contract, policy enforcement interface | Agent Platform |
| Tool invocation | Tool protocol and controlled connector interface | MCP, typed API client, tool gateway | Agent Platform with Integration Platform |
| Workflow coordination | Workflow engine or integration contract | Workflow runtime, durable work queue, orchestration adapter | Agent Platform with Integration Platform |
| Event reaction | Event contract and consumer interface | Versioned event schema, broker adapter, subscription contract | Agent Platform with Integration Platform |
| Knowledge retrieval request | Knowledge access contract | Retrieval API, RAG support interface, source authorization contract | Knowledge Platform |
| Memory access request | Memory access contract | Profile/memory API, retention and policy interface | Memory Platform |
| Conversation/context request | Conversation and context contract | Conversation API, session/context reference | Conversation Platform |
| Channel adaptation and delivery request | Channel interaction contract | Normalized interaction, delivery API, provider adapter | Conversation and Channel Platforms |
| Tenant and permission decision | Identity, policy, and authorization interface | OIDC/OAuth, policy decision point, decision contract | Security Platform |
| Runtime configuration and secrets | Configuration and secret-management interface | Secret manager, configuration registry, workload identity | Security and Deployment Platforms |
| Telemetry and diagnostics | Observability standard and instrumentation | OpenTelemetry-style instrumentation, trace/metric/log contract | Observability Platform |
| Evaluation and testing | Test/evaluation runner, dataset, and rubric interface | Scenario harness, evaluator adapter, test framework | Testing Platform with Agent Platform |

The examples are reference categories, not blanket approval to use every named product or framework.

---

# Technology Reference Status

## Status Definitions

| Status | Meaning |
|---|---|
| Approved | Reviewed and authorized for the defined scope, version, environment, and data classification |
| Planned | Identified for evaluation but not approved for production use |
| Reference only | May inform design or testing; not an approved production dependency |
| Deprecated | Existing use is being replaced; new use is prohibited unless exception is approved |
| Prohibited | Not allowed for the defined scope because of security, architecture, legal, operational, or tenant constraint |
| Retired | No longer used; retained for historical traceability |

## Current Reference Direction

Based on the project context, the following are intended technology directions requiring normal review before production adoption:

| Category | Reference direction | Status |
|---|---|---|
| Agent model integration | OpenAI model and realtime APIs through a provider abstraction | Planned |
| Agent orchestration | LangChain and LangGraph concepts or controlled equivalent | Planned |
| Tool protocol | MCP where it meets approved Integration and Security requirements | Planned |
| API service implementation | Python and FastAPI patterns | Planned |
| Voice/media integration | LiveKit and Twilio/SIP patterns, owned by Voice Platform | Planned |
| Data foundations | PostgreSQL, Redis, vector storage, and governed analytics storage, owned by Data Platform | Planned |
| Frontend | Next.js, React, TypeScript, and Tailwind patterns, owned by Frontend Platform | Planned |
| Infrastructure | Docker, Kubernetes, Helm, Terraform, and CI/CD patterns, owned by Deployment/Engineering Platforms | Planned |
| Telemetry | OpenTelemetry-compatible instrumentation patterns, owned by Observability Platform | Planned |

A technology becomes Approved only through the applicable technical, security, licensing, compatibility, and operational decision process.

## Official Source and Version Review

Every active or planned reference records its official source URL, documentation or API version reviewed, SDK/runtime version where applicable, review date, support status, owner, scope, and next review date. Community examples may be retained as reference-only but cannot replace official source verification.

Fast-moving model providers, SDKs, APIs, protocols, and security-sensitive dependencies receive a shorter review cadence. A material source change creates a compatibility and change-review item before it affects an active agent version or deployment.

---

# Technology Decision and Approval Model

## Technology Decision Matrix

For every material technology decision, the owner records the capability need, candidate options, evaluation criteria, selected option, rejected alternatives, rationale, limitations, decision owner, affected platforms, ADR or Decision Log reference where required, and review date.

The matrix prevents a framework, provider, or starter repository from becoming the default architecture merely because it was used first. A decision remains scoped to its approved purpose, environment, tenant/data eligibility, and version.

## Technology Risk Scorecard

Each candidate is assessed for:

- Security posture, identity/secret model, vulnerability history, and incident transparency.
- Data classification, privacy, retention, training/data-use terms, and region/residency eligibility.
- Tenant-isolation impact, contract maturity, compatibility, and replaceability.
- Reliability, performance, capacity, observability, operational burden, and support model.
- Cost, licensing, commercial continuity, migration difficulty, and exit risk.

The scorecard records evidence, unknowns, mitigations, residual risk, owner, and approval requirement. It informs a decision but does not replace required security, legal, procurement, or tenant review.

## Approval Gates

| Transition | Minimum evidence |
|---|---|
| Proposed to Planned | Capability owner, official source, initial boundary review, and defined evaluation hypothesis |
| Planned to Approved | Decision matrix, risk scorecard, security/data review, contract/compatibility evidence, test/evaluation plan, operational/exit plan, and required decision approval |
| Approved to Active | Registered version/scope, implementation evidence, SBOM/provenance, deployment readiness, observability, support owner, rollback/withdrawal path, and active agent-version eligibility |
| Active to Deprecated | Affected-version inventory, replacement/migration plan, support-end date, owner, and continuity controls |
| Deprecated to Retired | Migration/withdrawal completion, evidence retention, dependency removal/containment, and authorized closure |

An approval is never broader than the reviewed technology version, scope, environment, region, data class, tenant eligibility, and integration boundary.

---

# Agent Platform Technology Boundaries

## Model Providers

The Agent Platform uses a provider abstraction that separates agent purpose, instructions, capabilities, policy, tool selection, and evaluation from a specific model API. Provider/model eligibility is controlled by the agent version manifest, security assurance, data classification, region, tenant policy, cost, latency, and fallback requirements.

No agent implementation may embed a provider-specific model identity, credential, prompt secret, or fallback path outside the approved configuration and versioning controls.

## Orchestration Frameworks

An orchestration framework may support execution state, graph control, retries, tool coordination, or human review. It must not become the owner of conversation state, customer memory, business workflow, authorization, tenant scope, or platform governance.

Framework state is adapted to the owning platform contracts and can be replaced without changing the documented business capability boundaries.

## Tool and Protocol Technologies

MCP, REST clients, webhooks, queues, SDKs, and external APIs are integration mechanisms. All tool discovery, authorization, parameter validation, execution, idempotency, audit, and tenant binding remain governed by Agent and Integration Platform controls.

A protocol capability does not authorize a model or agent to reach any endpoint or use a credential.

## Model-Evaluation Technologies

Model-assisted evaluators, benchmark tools, and scenario harnesses are evaluated like other sensitive dependencies. They must meet data classification, tenant, region, retention, calibration, reproducibility, and access requirements before they receive evaluation evidence.

---

# Adoption and Review Process

## Pre-Adoption Review

Before adopting a technology for Agent Platform use, the owner records:

- Business capability and platform owner.
- Official source, version, maintenance status, license, and support model.
- Required interface, contract, compatibility, and replaceability boundary.
- Tenant, security, privacy, data classification, residency, and secret implications.
- Performance, cost, capacity, reliability, failure, observability, and operational impact.
- Testing, evaluation, rollout, rollback, deprecation, and exit strategy.
- Affected documents, owners, and whether a project Decision Log or ADR is required.

## Proof of Concept

A proof of concept is isolated, non-production, tenant-safe, and time-bound. It validates a defined hypothesis and records results, limitations, security/data posture, operational implications, and recommendation. A proof of concept does not authorize production use or redefine architecture.

## Approval and Registration

Approved technologies are recorded with scope, owner, version, environment, data eligibility, dependencies, support status, review date, and retirement/exit plan. Material adoption updates the relevant architecture, security, testing, deployment, observability, and operational documentation.

## Upgrade and Change Review

SDK, model, provider, protocol, framework, or configuration changes are reviewed for compatibility, behavior, security, tenant, data, evaluation, test, cost, deployment, and rollback impact. A material change creates a new agent version or architecture decision where required; it is not silently introduced through a package update.

---

# Compatibility and Replaceability

## Adapter Boundary

Each external technology is accessed through an owned interface that isolates vendor-specific requests, responses, errors, credentials, and lifecycle behavior. The adapter preserves shared contracts for tenant context, authorization, classification, correlation, observability, idempotency, and failure handling.

## Compatibility Record

The technology compatibility record identifies supported versions, API/protocol versions, agent capabilities, data classifications, environments, regions, model/provider configurations, known limitations, test evidence, and deprecation status.

## Exit and Continuity

For material dependencies, the owner defines alternatives, migration approach, data/export considerations, contract compatibility, rollback, operational runbook, and business continuity behavior. Replaceability does not require immediate duplicate implementation; it requires that no unbounded vendor coupling prevents a controlled exit.

---

# Security, Tenant, and Data Requirements

Every technology adoption is reviewed for service/workload identity, credential scope and rotation, authentication, authorization, tenant separation, data flow, classification, encryption, retention, residency, logging, support access, third-party terms, vulnerability posture, and incident notification.

A tool, provider, SDK, evaluator, or framework cannot receive data or perform work outside the tenant, purpose, classification, and permission scope approved for the current execution. Technology convenience does not override platform security or ownership.

---

# Observability, Testing, and Operational Readiness

Every approved production technology exposes or supports the required agent correlation, health, error, latency, cost, capacity, audit, and failure signals through the Observability Model.

Adoption requires contract, integration, security, tenant-isolation, resilience, performance, and evaluation evidence appropriate to risk. Operational readiness includes support owner, runbook, alert inputs, quota/capacity policy, rollback/withdrawal path, dependency health, and known limitation disclosure.

---

# Technology Lifecycle

~~~text
Proposed
    -> Evaluated
    -> Approved
    -> Active
    -> Deprecated
    -> Retired
~~~

A technology is reviewed periodically and on material provider/model change, security finding, end-of-support notice, cost/reliability issue, contract incompatibility, ownership change, regulatory change, or replacement opportunity.

Deprecation identifies affected agent versions and deployments, replacement path, support end, migration owner, timeline, risk, and rollback/continuity plan. A retired technology is not selected for new work.

## Vendor Continuity and Exit

For critical model, tool, integration, channel, evaluator, or infrastructure dependencies, the owner maintains a continuity plan. It defines outage behavior, safe fallback, support/escalation contact, dependency-health signal, contractual or commercial risk, data export/portability, migration trigger, replacement candidate, and exit deadline where applicable.

The continuity plan is exercised or reviewed proportionately to dependency criticality. A provider outage or contract change does not authorize the platform to route tenant data to an unapproved alternative.

## Reference Review Cadence

Reference review occurs before initial adoption, before material upgrade, on vendor/API/model/security/end-of-support notice, after relevant incident, and at the defined cadence for its risk category. The registry records the next review date and flags overdue critical references.

An overdue review does not silently invalidate all use, but it triggers assessment, restriction, or escalation according to risk and policy.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Agent technology registry | Records category, technology, status, scope, owner, version, environment, eligibility, and review date | Agent Platform with Architecture owner |
| Official reference and version register | Links official URL, reviewed version, support status, owner, scope, and next review | Agent Platform with 00_CONTROL reference owner |
| Technology decision matrix | Records need, options, criteria, selection, alternatives, rationale, owner, and ADR/Decision Log link | Agent Platform and Architecture owner |
| Technology assessment template | Captures capability, contract, security, data, cost, testing, operations, and exit analysis | Agent Platform and Architecture owner |
| Technology risk scorecard | Records security, data, tenant, lock-in, maturity, cost, operations, exit, residual risk, and approval | Agent, Security, and Architecture owners |
| Technology approval-gate checklist | Defines required evidence for planned, approved, active, deprecated, and retired status | Agent, Security, Operations, and Architecture owners |
| Compatibility record | Defines supported versions, interfaces, classifications, regions, limitations, and evidence | Agent Platform with dependent owners |
| Provider/model assurance record | Defines model/provider eligibility, data use, region, retention, cost, fallback, and review | Security and Agent Platform |
| Adapter contract catalog | Defines owned vendor-neutral interfaces and vendor-specific implementation mapping | Agent Platform and Integration Platform |
| SBOM and dependency-provenance link | Connects code packages, SDKs, images, artifacts, and supply-chain evidence to approved technology scope | Engineering, Deployment, and Security owners |
| Technology lifecycle and migration register | Tracks adoption, upgrade, deprecation, affected versions, replacement, and retirement | Agent Platform and Operations owner |
| Vendor continuity and exit plan | Defines outage, support, portability, migration trigger, fallback, and exit deadline for critical dependency | Agent, Operations, Security, and Procurement owners |
| Reference review schedule | Defines cadence, trigger, next review, overdue escalation, and evidence | Agent Platform and Architecture owner |
| Proof-of-concept report | Records hypothesis, isolated result, risk, limitation, and recommendation | Feature and Architecture owners |
| Technology readiness checklist | Defines security, tenant, test, evaluation, deployment, observability, support, and exit readiness | Agent, Security, Operations, and Architecture owners |

---

# Anti-Patterns

## Framework Owns the Architecture

Allowing a framework’s internal concepts or repository layout to determine platform boundaries creates lock-in and duplicate ownership. The platform architecture remains authoritative.

## Direct Vendor Calls Across the Codebase

Calling model, tool, provider, or evaluator APIs directly from multiple agent components makes replacement, security review, observability, and testing inconsistent. Use controlled adapters and contracts.

## Latest SDK or Model in Production

Unpinned upgrades can change behavior, cost, compatibility, or data handling without review. Production use requires approved version and change management.

## Technology Map as Blanket Approval

Listing a provider or framework in this document does not approve it for every tenant, model, region, data class, or environment. Scope and assurance remain explicit.

## Proof of Concept Becomes Production

An experiment or starter project may use weaker controls than production. It cannot become a production dependency without the normal approval, evidence, and registration process.

## Data Platform or Security Bypass

Choosing a convenient vector store, cache, secret path, or identity method outside Data and Security ownership violates the modular architecture even if it works technically.

---

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/PROJECT_CONTEXT.md | Provides current technology directions and project philosophy. |
| 00_CONTROL/ARCHITECTURE_PRINCIPLES.md | Defines modularity, replaceability, API/contract-first, and architecture-change rules. |
| 00_CONTROL/AI_DEVELOPMENT_GUIDE.md | Defines AI-assisted development and technology-change discipline. |
| 00_CONTROL/DECISION_LOG.md | Records project-level material technology and architecture decisions. |
| 06_AGENT_CONFIGURATION_MODEL.md | Defines configuration references governed by technology eligibility. |
| 07_AGENT_RUNTIME_ARCHITECTURE.md | Uses controlled runtime and provider abstractions. |
| 15_AGENT_TOOL_SYSTEM.md | Defines tool/protocol boundaries and controlled integration behavior. |
| 17_AGENT_PLUGIN_ARCHITECTURE.md | Defines plugin boundaries relevant to technology extension. |
| 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md | Defines Agent application of provider, supply-chain, secret, and technology security requirements. |
| 27_AGENT_VERSIONING_MODEL.md | Pins approved technology references through immutable versions. |
| 28_AGENT_DEPLOYMENT_MODEL.md | Requires technology readiness for target activation. |
| 29_AGENT_OBSERVABILITY_MODEL.md | Defines telemetry requirements for production technologies. |
| 31_AGENT_TESTING_STRATEGY.md | Defines technology adoption and upgrade test evidence. |
| 33_AGENT_EVALUATION_FRAMEWORK.md | Defines evaluator and model quality assessment controls. |
| 34_AGENT_GOVERNANCE_MODEL.md | Defines technology governance, ownership, and exception review. |
| 04_VOICE_PLATFORM | Owns voice/media/telephony technology choices. |
| 08_DATA_PLATFORM | Owns storage, cache, vector, data lifecycle, and analytics technologies. |
| 09_SECURITY_PLATFORM | Owns identity, secrets, compliance, and security-tool choices. |
| 12_DEPLOYMENT_PLATFORM | Owns infrastructure and deployment technology choices. |
| 13_OBSERVABILITY_PLATFORM | Owns telemetry platform technology choices. |
| 14_TESTING_PLATFORM | Owns shared testing technology choices. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Technology Reference Map architecture document. |
| 2.1 | 2026-08-05 | Added source/version review, decision and approval model, risk scorecard, provenance, continuity, cadence, and final artifacts. |
