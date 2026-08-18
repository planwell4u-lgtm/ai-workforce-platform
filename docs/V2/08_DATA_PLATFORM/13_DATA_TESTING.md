# 13_DATA_TESTING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how the Data Platform proves that its physical persistence, vector, storage, cache, queue, migration, lifecycle, backup/recovery, tenant-isolation, security, residency, reliability, and observability mechanisms behave safely.

It does not replace domain acceptance tests, Security control certification, or the Testing Platform's shared tooling and release governance.

# Principles

## Prove Boundaries, Not Just Happy Paths

Tests prove that mechanisms preserve trusted scope, lifecycle, access, residency, representation/version, correlation, idempotency, and audit requirements under success, failure, replay, delay, and recovery. A successful database call is insufficient evidence.

## Test With Safe, Representative Data

Automated tests use synthetic, minimized, approved, and tenant-distinct fixtures. Production data, credentials, raw recordings, unrestricted exports, and live provider side effects are prohibited unless a separately approved controlled test requires them.

## Evidence Is Reproducible

Each test has an owner, purpose, environment, fixture provenance, expected safe outcome, evidence location, and cleanup/lifecycle rule. Failures preserve bounded diagnostics without leaking protected contents or creating a shadow data store.

# Test Layers

| Layer | Data Platform proves | Does not replace |
|---|---|---|
| Unit/component | Validation, tenant predicates, serialization, migration rules, lifecycle guards, idempotency, and adapter behavior. | Cross-service contract or production readiness tests. |
| Contract | Data service schemas, error/outcome envelopes, version compatibility, and required scope propagation. | Domain ownership of business semantics. |
| Integration | PostgreSQL/pgvector, storage, queue, cache, backup, and provider adapters under controlled dependencies. | Vendor certification or enterprise policy approval. |
| End-to-end | Approved cross-platform data paths, reconciliation, audit correlation, and safe terminal outcomes. | Full product workflow acceptance. |
| Resilience/chaos | Failure, lag, capacity pressure, restore, failover, and degraded-observability safety. | Operations incident command exercises. |
| Security/privacy | Isolation, least privilege, redaction, deletion/hold, residency, and controlled export behavior. | Security Platform's independent assurance. |

# Required Test Scenarios

Data maintains automated and repeatable coverage for:

- Tenant/environment isolation for reads, writes, indexes, vectors, queues, caches, storage objects, backups, logs, and audit retrieval.
- Contract and schema evolution: expand/verify/contract, incompatible producer/consumer behavior, migration interruption, backfill, rollback, and reconciliation.
- Derived representations: vector/profile/version correctness, current eligibility filters, invalidation, stale/unavailable outcomes, and rebuild from governed source.
- Lifecycle: retention, deletion, legal hold, access revocation, residency restriction, archive, restore, and proof that recovery cannot revive ineligible data.
- Asynchronous behavior: idempotent write, duplicate/out-of-order delivery, bounded retry, dead-letter, cache invalidation, replay prevention, and terminal evidence.
- Backup/disaster recovery: backup integrity, restore verification, scoped recovery, recovery-time objectives, activation restrictions, and audit linkage.
- Capacity/reliability: connection/lock pressure, quota/bulkhead behavior, queue lag, provider failure, timeout, partial success, degraded telemetry, and safe deferment.
- Observability/audit: signal completeness, scope, correlation, redaction, access control, delivery/reconciliation, alert routing, and tamper-evidence behavior.

# Environments and Test Data

| Environment | Allowed purpose | Required constraints |
|---|---|---|
| Local/developer | Fast component and contract feedback. | Synthetic data, isolated credentials, disposable resources, no production integrations. |
| Shared integration | Adapter and dependency compatibility. | Tenant-distinct fixtures, controlled provider accounts, cleanup verification, restricted access. |
| Pre-production | Release, migration, resilience, and recovery evidence. | Production-like controls with non-production data, approved change window, evidence retention. |
| Controlled production validation | Narrow post-release verification only. | Explicit approval, least privilege, no content capture beyond necessity, rollback/restriction plan, audit evidence. |

# Quality Gates

No Data change is eligible for release until it has proportionate evidence for affected contracts, schema/representation compatibility, tenant isolation, lifecycle/residency, security controls, migration/rollback, observability, and recovery impact.

High-risk changes—shared schema, tenant predicate, RLS/permission configuration, deletion/hold, encryption/key, residency, vector retrieval filter, backup/restore, or queue/replay behavior—also require an owner-reviewed test plan, controlled environment evidence, rollback or restriction procedure, and Security/Data/Operations review as applicable.

# Defect and Regression Handling

Defects are classified by mechanism, scope, data risk, lifecycle/residency impact, reproducibility, customer exposure, and required containment. A regression fixture is added when safe and feasible. Tests never normalize an unsafe historical behavior merely to preserve compatibility; contracts follow the approved change and migration policy.

# Required Artifacts

| Artifact | Purpose |
|---|---|
| Data test strategy and coverage matrix | Maps each mechanism and risk to layers, owner, evidence, cadence, and gate. |
| Synthetic fixture catalog | Defines fixture provenance, tenant distinctions, sensitivity, cleanup, and lifecycle. |
| Contract and migration compatibility suite | Proves version behavior, expand/verify/contract, rollback, and reconciliation. |
| Resilience and recovery exercise record | Captures outage, restore, reconciliation, capacity, and degraded-mode evidence. |
| Release test evidence | Links changed mechanisms to results, exceptions, approvals, and post-release verification. |

# Anti-Patterns

## Production Data Is the Default Test Fixture

Tests use synthetic or explicitly approved minimized data; convenience does not override privacy, residency, access, or lifecycle rules.

## One Successful Query Proves Isolation

Isolation tests include negative cases across every representation and asynchronous/recovery path, not only the primary table.

## Migration Tests End at Deployment

Migration evidence includes backfill, compatibility, rollback/restriction, lifecycle, observability, and reconciliation outcomes.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Data Platform testing architecture. |
| 1.1 | 2026-08-07 | Approved after completeness, boundary, and long-term maintainability review. |
