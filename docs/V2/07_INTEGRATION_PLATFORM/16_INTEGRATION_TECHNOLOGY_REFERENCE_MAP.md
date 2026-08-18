# 16_INTEGRATION_TECHNOLOGY_REFERENCE_MAP

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document maps Integration responsibilities to technology categories, standards, approved references, and candidate implementation options. It is a decision aid and adoption boundary—not a vendor commitment, procurement list, or implementation backlog.

Technologies implement bounded Integration roles. They do not own Agent intent, canonical Conversation work, tenant control-plane facts, enterprise security policy, or data governance.

---

# Purpose

The map helps engineering choose APIs, webhooks, MCP servers, workflow engines, connector SDKs, queues, schemas, and operational tools while preserving provider replaceability, tenant isolation, safe external effects, audit, and long-term maintainability.

---

# Technology Principles

## Contract Before Technology

Choose a technology only after the Integration capability, action guard, idempotency, outcome, tenant/purpose, data-egress, audit, and exit contract are defined. Provider SDK objects and IDs remain inside adapters.

## One Bounded Role per Technology

A workflow engine coordinates permitted technical steps; it does not decide business intent. An API gateway routes/admit requests; it does not authorize external effects. An MCP server exposes approved capability views; it does not grant tool or credential authority.

## Standards First, Providers Second

Use HTTP, OpenAPI, JSON Schema, AsyncAPI, OAuth/OIDC where applicable, webhook signature patterns, structured event/versioning, and MCP protocol contracts before provider SDK convenience. Standards are capability evidence, not automatic enablement.

## Portability and Exit Are Required

Every adoption has versioned contracts, adapters, conformance, migration, rollback, credential revocation, audit/evidence treatment, and provider exit criteria before production use.

---

# Technology Role Map

| Integration role | Technology category/reference | Required evidence | Must not own |
|---|---|---|---|
| Public/internal APIs | Versioned HTTP APIs, OpenAPI, JSON Schema, Platform Foundation API edge | Schema compatibility, identity/scope, idempotency, error privacy, rate/replay, audit | Tenant control plane, action approval, provider internals. |
| Events/webhooks | AsyncAPI/event schema, signed webhook adapter, queue/broker technology selected by Data/Operations | Source/freshness/replay/order, delivery/retry, tenant scope, raw-evidence protection | Authorization, business intent, canonical Conversation event meaning. |
| MCP server/tools/resources | MCP-compatible server behind Integration registry and action path | Client identity, tool/resource schema, tenant/profile scope, guard/approval, audit, retirement | Direct provider SDK, arbitrary code/database access, credential disclosure. |
| Workflow/asynchronous execution | Durable workflow/scheduler/queue technology selected after evaluation | Step graph, deadlines, idempotency, cancellation, compensation, recovery, observability | Business process, participant communication, policy override. |
| Connector SDKs | Provider SDK/API contained in a versioned adapter | Conformance, credential scope, error mapping, callback handling, migration/exit | Public contracts, canonical IDs, tenant selection, business logic. |
| Identity/secrets | Security Platform-selected identity, vault, certificate, token, workload tools | Least privilege, lease, rotation, revocation, audit | Connector capability or action decision. |
| Persistence/index/queue | Data Platform-selected Supabase-managed PostgreSQL, pgvector where relevant, cache/broker/object storage | Scope, lifecycle, backup/recovery, portability, queue/idempotency controls | Integration semantics, authorization, durable business truth. |
| Observability/testing | Observability/Testing Platform-selected telemetry, alert, fixture, sandbox, conformance tools | Redaction, tenant-safe data, data quality, SLOs, release evidence | Raw provider-content store or automatic action approval. |

---

# Approved Reference Boundaries

| Reference | Allowed evaluation use | Explicit limit |
|---|---|---|
| Architecture Reference Registry | Source of approved references and adoption limits. | A listing is not production adoption. |
| LiveKit Examples Organization | Discovery of bounded starter/client/agent patterns relevant to integration journeys. | Individual repositories need their own review and cannot define Integration architecture. |
| LiveKit Supabase Hacker Starter | Sandbox study of synthetic tool CRUD, session reporting, and local workflow fixtures. | No direct adoption of schema, secret-key pattern, tenant model, or external-effect authorization. |
| Supabase-managed PostgreSQL and pgvector | Data Platform-managed persistence/vector support for Integration evidence only where required. | Not a direct API from Agent/Conversation/channel code and not an authorization/workflow engine. |

---

# APIs, Webhooks, MCP, Workflows, and SDKs

## APIs

Expose provider-neutral operations through versioned schemas and the Platform Foundation API edge. Each endpoint creates or reads a bounded Integration record and uses current identity, tenant, purpose, representation, idempotency, and audit controls. API choice must not bypass the action guard.

## Webhooks

Provider webhooks terminate at a validating adapter endpoint. Technology selection must support source verification, secret/certificate rotation, size/rate limits, replay/order handling, protected raw evidence, quarantine, and safe acknowledgement. Webhooks are evidence, never commands.

## MCP

MCP servers expose only registered Integration tools/resources for approved clients and tenant/profile scopes. A tool call follows the same ActionRequest, authorization, approval, credential, execution, and audit contracts as an API call. MCP is an interface protocol, not a tool-permission system.

## Workflows

Select workflow/scheduler technology only after proving durable step state, tenant-safe queues, deadlines, cancellation, idempotency, compensation, reconciliation, observability, recovery, and exit. It must coordinate technical effects without absorbing Agent/Conversation business ownership.

## Connector SDKs

SDKs stay inside adapters. Evaluation includes version/support, provider account model, credential handling, data egress/residency, API limits, callbacks, error semantics, observability, testing, licensing, migration, and removal. No provider SDK type reaches public contracts.

---

# Adoption Workflow

Before adoption, responsible owners must:

1. review current official documentation, licensing/commercial terms, security/data/residency behavior, and operational limits;
2. map the technology to one bounded Integration role and contract;
3. run a dedicated-tenant, synthetic-data proof of concept;
4. validate adapter/API/MCP compatibility, action guard, credential, egress, tenant, reliability, observability, and test evidence;
5. define profile/configuration, rollout, rollback, migration, credential/provider exit, support, and audit requirements; and
6. record material decisions in the Architecture Reference Registry and Decision Log.

A technology is Active only for the approved role/profile after current owner approvals and evidence. A material provider/SDK/security/pricing/region/capability change triggers reassessment.

---

# Platform Foundation and Channel Boundaries

Platform Foundation owns tenant/configuration/API-edge technology decisions. Security owns enterprise identity/secrets/compliance technology. Data owns persistence/queue implementation. Voice and Digital Channel own transport technologies. Integration selects only its bounded adapters and contracts; it cannot use an available technology to claim another platform's responsibility.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration technology decision record | Defines role, alternatives, evidence, constraints, rollout, exit, and audit. | Integration with Architecture and relevant owners |
| API/webhook/MCP/workflow/SDK evaluation matrix | Defines required compatibility, security, tenant, egress, reliability, observability, test, and exit evidence. | Integration with Security, Data, Operations, Testing owners |
| Adapter portability and exit plan | Defines contract preservation, provider migration, credential revocation, evidence/lifecycle, and rollback. | Integration with Data, Security, Operations owners |

---

# Anti-Patterns

## MCP Server Is a Privileged Tool Gateway

MCP remains a contract interface; every tool call still follows current Integration guard and audit controls.

## Workflow Engine Owns the Process

It coordinates allowed technical steps only; Agent, Conversation, and business owners retain intent and meaning.

## Provider SDK Is the Public API

SDKs are replaceable adapter internals, not platform contracts or identifiers.

## Supabase or a Starter Project Defines the Platform

They are scoped supporting references; platform ownership, tenant, security, and data-lifecycle contracts remain authoritative.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01–15 Integration documents | Define the responsibilities, controls, evidence, and boundaries technologies must implement. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Authoritative external-reference and adoption-limit registry. |
| 00_CONTROL/08_DECISION_LOG.md | Records material technology decisions. |
| 16_PLATFORM_FOUNDATION/README.md | Owns API-edge/control-plane technology. |
| 08_DATA_PLATFORM | Owns persistence and queue technology implementation. |
| 09_SECURITY_PLATFORM | Owns identity, secrets, compliance, and security technology. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration technology map covering APIs, webhooks, MCP, workflows, connector SDKs, adoption, and exit controls. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |
