# 15_INTEGRATION_TESTING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines Integration-domain test scenarios, invariants, fixtures, acceptance evidence, and release gates for connectors, credentials, approvals, actions, workflows, APIs/MCP, callbacks, isolation, security, reliability, and observability.

Integration owns what must be proven for external effects. Testing Platform owns shared runners, environments, reporting, quality tooling, and test governance infrastructure.

---

# Purpose

Testing proves that an Integration capability is bounded, authorized, tenant-safe, provider-neutral, observable, recoverable, and unable to create unintended external effects before it is enabled for a tenant or participant journey.

---

# Objectives

- Validate each Integration contract, guard, adapter, lifecycle, and normalized outcome.
- Prove no test can contact real participants, use production tenant data, expose secrets, bypass approval, or cross tenant scope.
- Cover happy, denial, malicious, concurrent, degraded, recovery, replay, and uncertain-effect paths.
- Produce traceable evidence for connector onboarding, profile change, credential rotation, migration, rollout, incident recovery, and retirement.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| CI/CD, test runner, environment provisioning, reporting, performance/chaos tooling, or test policy infrastructure | 14_TESTING_PLATFORM, Deployment, and Operations Platforms |
| Enterprise penetration/red-team/compliance program | 09_SECURITY_PLATFORM |
| Production data access, retention/deletion, backup, or storage test infrastructure | 08_DATA_PLATFORM and 09_SECURITY_PLATFORM |
| Agent reasoning or canonical Conversation test semantics | Agent and Conversation Platforms |

---

# Testing Principles

## Contract Before Provider Quirk

Tests assert platform-defined capability, request, outcome, idempotency, and evidence contracts. Provider-specific behavior belongs inside adapter conformance tests and cannot change public semantics.

## Safe by Default

Every suite uses dedicated test tenants, accounts, credentials, endpoints, provider sandboxes, queues, data namespaces, cost budgets, telemetry tags, and cleanup rules. No test contacts a real participant or uses ordinary customer data unless a separately approved production validation explicitly permits it.

## Test Negative and Uncertain Paths

Every material effect is tested for denial, expiry, cancellation, malformed/replayed/out-of-order callback, credential revocation, policy change, timeout, duplicate request, provider failure, tenant mismatch, and uncertain external result.

## Passing Tests Do Not Override Runtime Controls

Current production tenant, policy, consent, approval, credential, lifecycle, and security checks remain authoritative.

---

# Test Environments and Data

| Environment | Purpose | Constraint |
|---|---|---|
| Unit/contract | Deterministic schema, state, guard, error, and idempotency tests. | No live provider credential or endpoint. |
| Simulation | Controlled adapter/callback/provider fixtures and adversarial evidence. | Versioned fixtures; no external effect. |
| Sandbox/integration | Approved provider test accounts and allowlisted targets. | Dedicated tenant, quota, cleanup, no real participant contact. |
| Staging/journey | Cross-platform release candidate verification. | Synthetic data, production-like controls, controlled load. |
| Production synthetic | Narrow continuous safe probe. | Dedicated identities/endpoints, explicit approval, no customer data/action. |

Fixtures have provenance, classification, provider-use, retention/deletion, access/export, and cleanup rules. Credentials and raw provider payloads are never copied into ordinary test reports.

---

# Required Test Suites

| Suite | Required evidence |
|---|---|
| Domain/contract | Entity/state/schema/version compatibility, protected IDs, outcomes, forbidden direct writes. |
| Registry/adapter | Capability lifecycle, provider mapping, conformance, account/profile, error normalization, migration/rollback. |
| Credential/access | Lease/grant scope, rotation/revocation, purpose/target/tenant binding, no secret leakage. |
| Authorization/approval | Risk, confirmation, expiry, separation, cancellation, limit, denial, audit. |
| Execution/idempotency | Duplicate/retry/order/timeout/fallback/uncertain effect and reconciliation. |
| Workflow/callback | Step/wait/deadline/compensation, forged/stale/replayed/out-of-order webhook, recovery. |
| API/MCP | Schema, visibility, rate/replay, tool/resource scope, no provider/action bypass. |
| Security/privacy/tenant | Injection, egress, cross-tenant, cache/queue/support/migration, raw-data/trace/log leak. |
| Reliability/observability | Circuit/bulkhead, failover, data quality, signal/alert/SLO/audit completeness. |
| Journey/release | Approved end-to-end action path across Agent, Conversation, Integration, and controlled provider. |

---

# Traceability and Release Gates

Every requirement, threat/control, capability/profile, contract, risk class, SLO, migration, and release gate maps to versioned test cases and retained evidence: environment, fixture/provider profile, execution time/result, exception/defect, owner, and release disposition.

A connector, capability, or change is eligible only when applicable contract/conformance/security/privacy/tenant/authorization/execution/recovery/observability tests pass; test-data and environment drift are validated; required runbooks/rollback/exit evidence is current; and no critical/high-risk finding is unaccepted. Quarantined or flaky tests cannot count as passing evidence for safety-critical requirements.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration test strategy and traceability matrix | Maps requirements, threats, contracts, SLOs, gates, tests, owners, and evidence. | Integration with Testing owner |
| Adapter/API/MCP conformance suite | Proves provider-neutral contracts, compatibility, scope, security, callbacks, and migration. | Integration with Security and Testing owners |
| Sandbox/fixture standard | Defines accounts, data, credentials, quotas, isolation, cleanup, and drift checks. | Integration with Operations, Data, Security, Testing owners |
| Integration journey/resilience suite | Proves safe end-to-end effects, uncertainty, recovery, and no participant/cross-tenant harm. | Integration with Agent, Conversation, Security, Testing owners |
| Release gate checklist | Defines required evidence, approval, rollout/rollback, defects, and support readiness. | Integration with Operations and Testing owners |

---

# Anti-Patterns

## Mock Pass Means Provider Works

Use provider sandbox and controlled conformance tests before enablement.

## Test Grant Contacts a Real Customer

Dedicated test accounts and allowlisted synthetic targets prevent external harm and data contamination.

## Happy Path Is Enough

Denial, replay, expiry, cancellation, outage, recovery, and uncertainty are mandatory evidence.

## Test Result Overrides Runtime Guard

Current production controls remain authoritative regardless of prior test success.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03–14 Integration documents | Define contracts, controls, outcomes, signals, and invariants to validate. |
| 14_TESTING_PLATFORM | Owns shared testing infrastructure and standards. |
| 13_OBSERVABILITY_PLATFORM | Owns shared telemetry/alert infrastructure. |
| 09_SECURITY_PLATFORM | Owns enterprise security/compliance policy. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration testing architecture covering safety, fixtures, conformance, journeys, resilience, traceability, and release gates. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |
