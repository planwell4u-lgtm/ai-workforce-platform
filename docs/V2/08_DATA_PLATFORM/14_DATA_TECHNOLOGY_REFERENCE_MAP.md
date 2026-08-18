# 14_DATA_TECHNOLOGY_REFERENCE_MAP

**Version:** 1.1  
**Status:** Approved  
**Owner:** Data Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document maps Data Platform responsibilities to technology categories, approved references, and adoption limits. It is a decision aid for implementation and review; it is not a vendor commitment, procurement decision, schema design, or exception to platform controls.

Technology may implement a Data mechanism only through the relevant contracts, trusted scope, lifecycle, access, residency, security, testing, operational, and change controls.

# Decision Status

| Status | Meaning |
|---|---|
| Approved foundation | A technology selected through an Architecture Decision Record for its stated Data role. |
| Approved reference | An external source that may guide design or evaluation under the Architecture Reference Registry. |
| Candidate technology | A category or named option that requires a current adoption decision before production use. |
| Restricted evaluation | Permitted only in the explicitly documented sandboxed role. |
| Retired/rejected | Not eligible for new work; rationale remains available for review. |

At this document's date, Supabase-managed PostgreSQL and pgvector are the approved shared relational and vector foundation under ADR-005. The decision does not automatically adopt Supabase Auth, Storage, Realtime, Edge Functions, RLS as enterprise policy, a schema, an SDK access pattern, or a starter application's architecture.

# Data Technology Role Map

| Data responsibility | Allowed technology category | Approved foundation/reference or candidate | Must not own |
|---|---|---|---|
| Shared relational persistence | Managed PostgreSQL service and approved access/migration tooling | Supabase-managed PostgreSQL under ADR-005; PostgreSQL references | Tenant/control-plane truth, identity, authorization policy, domain semantics. |
| Vector representation and similarity | PostgreSQL vector extension and governed retrieval/index tooling | pgvector under ADR-005 | Knowledge/Memory admission, retrieval eligibility, canonical source, or user-visible answer selection. |
| Data service access | Internal Data contract/service, approved driver/query layer, repository/adapter tooling | Data-owned implementation selected during delivery | Direct client/database bypass, tenant authority, business workflow ownership. |
| Schema migration/versioning | Versioned migration runner, compatibility checks, backfill/reconciliation tooling | Data-owned selected tooling; PostgreSQL ecosystem candidates | Unreviewed production schema mutation or domain lifecycle decisions. |
| Object/artifact storage | Encrypted object storage and controlled artifact adapter | Candidate selected with Data, Security, Operations, and residency review | Artifact meaning, access decision, retention policy, or unrestricted export. |
| Cache | Scoped cache service and invalidation/rebuild tooling | Candidate selected with Data and Operations review | Authoritative state, lifecycle bypass, tenant fallback, or audit substitute. |
| Queue/asynchronous storage | Durable queue/stream and bounded worker/replay tooling | Candidate selected with Integration, Data, and Operations review | Action authorization, workflow semantics, unlimited replay, or canonical business effects. |
| Backup/disaster recovery | Managed backup, encrypted snapshot, restore/reconciliation tooling | PostgreSQL/Supabase capability evaluated against Data/Security/Operations requirements | Automatic activation without scope, lifecycle, integrity, and residency validation. |
| Encryption/key handling | Platform-approved encryption, KMS/key management, secret/workload identity controls | Security Platform-selected technology | Data-local cryptographic policy or tenant-blind key access. |
| Observability/audit transport | Metrics, logs, traces, audit pipeline, alerting tooling | Observability/Security Platform-selected technology | Shadow data retention, enterprise audit policy, or domain event meaning. |
| Infrastructure/deployment | Containers, orchestration, infrastructure-as-code, managed-service configuration | Operations/Deployment Platform-selected technology | Data contract ownership or unreviewed mutable production configuration. |
| Testing | Synthetic-fixture, contract, migration, resilience, and recovery tooling | Testing Platform-selected technology; PostgreSQL/pgvector test references | Production data as default fixture or release-policy bypass. |

# Approved Foundation: Supabase PostgreSQL and pgvector

ADR-005 approves Supabase-managed PostgreSQL as the shared relational foundation and pgvector as its vector extension. Adoption is limited to Data-owned persistence and derived-vector mechanisms. Data retains schema, migration, access-contract, representation, backup/restore, lifecycle, portability, and exit obligations.

Before production implementation, the delivery owner records the selected service plan/region, extension/version support, network/access profile, backup/restore evidence, monitoring, capacity assumptions, residency fit, migration/exit plan, and current security review. Provider capability is evidence, not a substitute for a platform control.

# External Reference Use

| Reference | Permitted use | Limit |
|---|---|---|
| PostgreSQL documentation | Relational design, transactions, indexes, constraints, performance, backup/recovery, and compatibility research. | Follow Data contracts and approved migration/security controls. |
| pgvector documentation | Vector column, index, distance, filtering, performance, and version research. | Vectors remain derived, scoped, lifecycle-controlled representations. |
| Supabase documentation | Managed PostgreSQL capability, operational limits, backup/connectivity, and extension research. | ADR-005 limits adoption; no implicit product adoption beyond the shared data foundation. |
| LiveKit Supabase Hacker Starter | Restricted sandbox pattern review using synthetic data. | Never imports its schema, identity/RLS, secret access, direct database access, or SaaS architecture into production. |

# Adoption Workflow

1. Identify the Data responsibility, owning platform, trusted scope, data classes, lifecycle, residency, and exit need.
2. Select an allowed category and check the Architecture Reference Registry, ADRs, Security requirements, and current provider documentation.
3. Record a bounded adoption proposal: version/region, interface, access model, evidence, capacity, failure posture, monitoring, test plan, rollback, migration, and exit plan.
4. Obtain required Data, Security, Operations, and affected-domain review before production use.
5. Prove contract, isolation, lifecycle, recovery, observability, and portability behavior in controlled environments.
6. Register the final decision and re-evaluate it on material capability, cost, security, residency, or contract change.

# Portability and Exit

Every adopted technology has a documented owner, contract boundary, data/representation export path, dependency inventory, configuration/secrets handoff, migration/reconciliation plan, evidence retention plan, safe rollback/restriction posture, and retirement procedure. Provider identifiers, SDK types, query dialect shortcuts, and event formats stay behind Data-owned adapters where practical.

# Anti-Patterns

## A Managed Provider Becomes the Control Plane

Supabase/PostgreSQL/pgvector provide data mechanisms; they do not define tenant authority, authorization, enterprise audit policy, or domain meaning.

## A Vector Index Chooses What Is Allowed

Similarity tooling accelerates a retrieval operation only after the owning Knowledge or Memory platform has supplied current eligibility and scope controls.

## Example Code Is an Adoption Decision

Starter repositories remain restricted references until a specific, reviewed implementation decision maps a narrow use to Data contracts and controls.

# Related Documents

| Document | Relationship |
|---|---|
| 00_CONTROL/08_DECISION_LOG.md | ADR-005 records the approved Supabase PostgreSQL and pgvector foundation. |
| 00_CONTROL/13_ARCHITECTURE_REFERENCE_REGISTRY.md | Records approved documentation and restricted external examples. |
| README.md | Defines Data Platform ownership and document sequence. |
| 01–13 Data Platform documents | Define the mechanisms and controls technologies must implement. |
| 09_SECURITY_PLATFORM/README.md | Owns enterprise identity, secrets, cryptography, policy, and audit controls. |
| 11_OPERATIONS_PLATFORM/README.md and 12_DEPLOYMENT_PLATFORM/README.md | Own operational and deployment technology decisions. |

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Data Platform technology reference map. |
| 1.1 | 2026-08-07 | Approved after completeness, boundary, and long-term maintainability review. |
