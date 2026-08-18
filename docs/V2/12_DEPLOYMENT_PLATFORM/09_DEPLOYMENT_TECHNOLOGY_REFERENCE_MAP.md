# 09_DEPLOYMENT_TECHNOLOGY_REFERENCE_MAP

**Version:** 1.1  
**Status:** Approved  
**Owner:** Deployment Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document maps approved deployment technology roles to the Deployment Platform architecture. It records why a technology category is used, its boundary, adoption requirements, and exit considerations. It does not lock the implementation to a vendor, version, managed service, or repository layout without a governed decision.

# Approved Technology Roles

| Technology/category | Approved role | Boundary and adoption requirement |
|---|---|---|
| Containers and container images | Package services and workers into traceable, deployable runtime artifacts. | Images are immutable, scanned/verified under Security policy, minimally privileged, and contain no secrets or production data. |
| Docker-compatible build/runtime tooling | Local and CI build/runtime compatibility for containerized workloads. | Used through versioned build definitions; it does not define production orchestration or tenant isolation. |
| Kubernetes-compatible orchestration | Run, scale, isolate, update, and recover containerized production workloads where selected by the environment design. | Workload identity, network, policy, secrets, and tenancy controls remain Security/Data/Foundation responsibilities. |
| Helm-compatible deployment packaging | Version and parameterize Kubernetes release manifests where selected. | Values are classified; secrets are referenced through approved systems, not stored in charts or routine values. |
| Terraform-compatible infrastructure as code | Define, review, provision, and reconcile cloud/infrastructure resources. | Desired state is versioned and controlled; it does not authorize a change, own data lifecycle, or replace Operations release coordination. |
| CI/CD automation | Build, validate, attest, promote, and deploy approved artifacts/configuration. | Pipelines use workload identity, enforce approved gates, and do not replace Security policy, Testing acceptance, or Operations go/no-go. |
| Artifact registry | Store immutable versioned build artifacts and related provenance. | Registry permissions, retention, signing/trust, and revocation follow Security/Data policy. |
| Managed cloud/runtime services | Supply approved compute, network, storage bindings, load balancing, and regional capacity. | Provider selection is subject to Security, Data residency, cost, reliability, and exit review; provider success is not domain outcome proof. |
| Configuration delivery and secret references | Deliver versioned non-secret configuration and runtime references to Security-managed secret material. | Deployment never embeds secret values; domains own configuration semantics and Security owns secrets/access policy. |
| Infrastructure policy/drift tooling | Validate desired state, detect drift, and constrain unsafe delivery actions. | Policy authority belongs to Security/Control owners; tooling implements approved checks and evidence. |

# Selection Principles

- Prefer declarative, versioned, reviewable, reproducible mechanisms over manual environment changes.
- Select tools that support least-privilege workload identity, auditability, provenance, isolated environments, rollback/recovery, and safe configuration/secret integration.
- Avoid a new deployment tool, provider dependency, control plane, or persistent source of truth when an approved platform capability already fulfills the need.
- A tool is adopted only with a clear owner, supported environment scope, Security/Data/Operations review as applicable, documentation, test/recovery plan, cost/lock-in assessment, and retirement path.
- Tool output, build logs, manifests, metadata, and diagnostics are subject to secret redaction, tenant/data minimization, and access controls.

# Reference Architecture Mapping

```text
Versioned source and approved configuration
        |
        v
CI/CD automation -> container artifact + provenance -> artifact registry
        |
        v
Infrastructure-as-code -> cloud/runtime environment -> orchestration platform
        |
        v
Deployment packaging/configuration references -> approved workload identity and secrets integration
        |
        v
Operations, Security, Data, Observability, Testing, and domain-owner evidence
```

The map shows implementation roles, not ownership transfer. For example, Kubernetes may host a domain service, but it does not own that service's tenant authority, canonical state, business behavior, or external-effect outcome.

# Technology Adoption Record

Before adopting, replacing, or materially expanding a deployment technology, record:

1. the required capability and why the current approved mechanism is insufficient;
2. affected environments, workloads, tenant/data/security scope, cost, and operational support model;
3. identity, authorization, secret, supply-chain, network, residency, retention, and audit implications;
4. compatibility, migration, rollback/recovery, observability, testing, and failure-mode plan;
5. alternatives considered, owner/approvals, documentation, and sunset/exit requirements.

Material changes follow the control-layer change process and require the applicable Security, Data, Operations, Testing, and domain review. A pilot or prototype must not silently become production infrastructure.

# Exit and Portability Requirements

Deployment designs preserve reasonable portability through versioned source/build definitions, standard artifact formats where practical, documented environment/configuration interfaces, exportable infrastructure state/evidence, and tested recovery/migration procedures. Portability does not require premature multi-cloud duplication or prevent managed-service use when its benefits and risks are approved.

Provider or tool exit planning identifies artifact/configuration export, infrastructure replacement, identity/secret transition, data migration owner, rollback/recovery assumptions, operational training, retained evidence, and tenant/customer impact. Deployment cannot execute a provider exit that bypasses Data residency/lifecycle, Security access/trust, or Operations change/readiness controls.

# Technology Boundaries and Anti-Patterns

- Do not put secrets in images, source, chart values, Terraform variables/state without approved protection, logs, or tickets.
- Do not use an environment, cluster, provider account, or registry namespace as the only tenant-isolation or authorization control.
- Do not grant a CI/CD runner unrestricted production access, broad data access, or standing external credentials.
- Do not treat an infrastructure tool's successful apply as domain, data, participant, or business-action success.
- Do not add a technology to compensate for an unclear ownership boundary; resolve the boundary first.

# Required Evidence

Before implementation approval, retain the technology adoption record; capability/alternative assessment; Security/Data/Operations/Testing review; versioned configuration and identity model; supply-chain/provenance controls; cost/support/exit assessment; integration and recovery tests; documentation; and the approved change record.

# Related Documents

- `01_DEPLOYMENT_PLATFORM_ARCHITECTURE.md`
- `02_ENVIRONMENT_AND_INFRASTRUCTURE_MODEL.md`
- `03_CI_CD_AND_ARTIFACT_SUPPLY_CHAIN.md`
- `04_DEPLOYMENT_CONFIGURATION_AND_SECRETS_INTEGRATION.md`
- `05_DEPLOYMENT_RELEASE_AND_ROLLBACK_STRATEGY.md`
- `06_DEPLOYMENT_SECURITY_AND_ACCESS_CONTROL.md`
- `07_DEPLOYMENT_OBSERVABILITY_RELIABILITY_AND_DISASTER_RECOVERY.md`
- `08_DEPLOYMENT_TESTING_AND_ASSURANCE.md`
- `00_CONTROL/08_DECISION_LOG.md`
- `00_CONTROL/09_CHANGE_MANAGEMENT.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created the deployment technology reference map. |
| 1.1 | 2026-08-09 | Finalized after ownership, adoption-boundary, and maintainability review. |
