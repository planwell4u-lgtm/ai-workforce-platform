# 03_TEST_STRATEGY_AND_TEST_LEVELS

**Version:** 1.1  
**Status:** Approved  
**Owner:** Testing Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines the risk-based test strategy, test-level selection, coverage expectations, and evidence mapping for platform changes. It ensures that tests are chosen for the actual ownership, security, data, channel, failure, and release risk—not merely for code coverage or a generic checklist.

# Risk-Based Selection

Every change is assessed for tenant/identity/authorization impact; protected-data lifecycle; public API/event compatibility; external/provider effect; AI/channel behavior; asynchronous/retry/reconciliation behavior; production availability/recovery; and customer/operator experience. Higher-risk changes require broader and more independent evidence.

| Risk condition | Minimum additional evidence |
|---|---|
| Tenant, identity, authorization, privilege, or secret change | Security review; tenant/authorization negative tests; audit/revocation evidence. |
| Data schema, retention, deletion, export, restore, or residency change | Data review; migration/lifecycle/recovery tests; volume/compatibility evidence. |
| Public API/event/contract change | Contract/version compatibility and consumer/producer failure tests. |
| Provider, channel, tool, or external business action | Simulation/sandbox, idempotency, timeout/uncertainty, callback/authentication, reconciliation, and safe-effect evidence. |
| Agent, model, prompt, knowledge, memory, or tool-eligibility change | Versioned evaluation, access/guardrail, regression, and behavior-limit evidence. |
| Release, infrastructure, capacity, or recovery change | Deployment/Operations evidence, rollback/recovery exercise, telemetry/alert validation. |
| Participant/operator experience | End-to-end journey, accessibility, privacy/redaction, degraded/error/forbidden state evidence. |

# Test Levels

| Level | Question answered | Boundary |
|---|---|---|
| Unit/component | Does owned logic behave correctly in isolation? | No real cross-module/provider dependency. |
| Contract | Does an approved interface preserve schema, authorization/context, errors, and compatibility? | Public/shared API, event, configuration, or protocol boundary. |
| Integration | Do selected owners interoperate through approved contracts? | Controlled dependencies and test data. |
| System/end-to-end | Does the narrow intended user/system journey work across required boundaries? | Production-like controlled environment with explicit limitations. |
| Negative/security | Does the platform safely reject invalid, unauthorized, cross-tenant, malformed, replayed, or unsafe behavior? | Security/tenant/data/channel boundary. |
| Resilience/recovery | Does failure, retry, delay, duplicate, cancellation, timeout, rollback, and reconciliation behave safely? | Dependency, state, delivery, and recovery boundaries. |
| Performance/evaluation | Does behavior meet approved objectives under representative load or quality scenarios? | Owner-defined service/AI/channel objective. |

No test level replaces another. A high unit-test count cannot prove integration, authorization, participant delivery, provider behavior, accessibility, recovery, or production readiness.

# Coverage and Test Design Rules

Test cases are derived from owner-approved acceptance criteria, contracts, state transitions, inputs, failure modes, threat/data scenarios, and observed regressions. Each material test identifies the owner, requirement/contract reference, environment, fixture/data classification, assertion, expected outcome, and evidence location.

Coverage measurements are diagnostic indicators, not release authorization. The team investigates uncovered critical paths, meaningful mutation/regression risk, and branch/state/failure coverage where appropriate. Tests must not be deleted, weakened, skipped, or made non-deterministic merely to improve a dashboard or unblock an unrelated delivery target.

# Change-to-Evidence Matrix

| Change scope | Required test levels | Required owners |
|---|---|---|
| Internal local change | Unit/component; focused regression as relevant. | Owning module. |
| New/changed module capability | Unit, contract, integration, negative/failure as relevant. | Owner plus affected interface consumers. |
| Cross-platform journey | Contract, integration, end-to-end, tenant/security negatives, observability evidence. | Participating owners, Security, Testing. |
| Data/security/production-critical change | Relevant levels plus recovery/rollback/performance and formal evidence. | Data/Security/Operations/Deployment/Testing and owner. |
| Agent/channel/external-effect change | Contract, integration, evaluation, delivery/action outcome, uncertainty/reconciliation, end-to-end. | Agent/channel/Integration/Security/Testing owners. |

# Test Planning and Review

Before implementation, the owner records the selected levels, risks, fixtures/dependencies, required simulations, data/privacy restrictions, environment, gate evidence, known gaps, and recovery/rollback test need. Missing non-blocking evidence is explicitly deferred with owner, risk, deadline, and release constraint; blocking ambiguity is resolved before code proceeds.

Review checks that assertions are independent enough to catch the intended failure, use approved contracts, preserve tenant isolation, distinguish observed technical state from domain outcome, and remain maintainable when versions/providers/channels evolve. A test that relies on private implementation details is refactored toward the appropriate boundary unless it is an intentional owned-unit test.

# Required Evidence

Before implementation approval, retain risk assessment; test plan and owner mapping; selected-level results; negative/failure/recovery evidence; data/environment controls; contract compatibility; limitations/deferred evidence; quality-gate result; and required owner/security/data/operations/deployment acceptance.

# Related Documents

- `01_SHARED_TEST_ASSURANCE_CONTRACT.md`
- `02_TESTING_PLATFORM_ARCHITECTURE.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../09_SECURITY_PLATFORM/14_SECURITY_TESTING_AND_ASSURANCE.md`
- `../08_DATA_PLATFORM/13_DATA_TESTING.md`
- `../12_DEPLOYMENT_PLATFORM/08_DEPLOYMENT_TESTING_AND_ASSURANCE.md`
- `../13_OBSERVABILITY_PLATFORM/07_OBSERVABILITY_TESTING_AND_ASSURANCE.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created the risk-based testing strategy and test-level model. |
| 1.1 | 2026-08-09 | Finalized after cross-platform risk, evidence, and maintainability review. |
