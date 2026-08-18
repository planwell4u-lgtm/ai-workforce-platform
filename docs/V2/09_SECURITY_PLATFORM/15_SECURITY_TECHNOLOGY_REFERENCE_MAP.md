
**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document maps Security Platform responsibilities to technology categories, approved-reference use, adoption decisions, and exit requirements. It is a decision aid, not a vendor commitment or permission to introduce a security tool without documented review.

# Technology Status

| Status | Meaning |
|---|---|
| Approved foundation | A documented decision authorizes a technology for a stated role and scope. |
| Approved reference | Documentation/source may guide evaluation but is not automatically deployed. |
| Candidate | Requires security, architecture, data, operations, and affected-owner review before production use. |
| Restricted evaluation | Allowed only in named sandbox/scope with synthetic or approved data and exit plan. |
| Retired/rejected | Not eligible for new work; rationale remains recorded. |

# Role Map

| Responsibility | Allowed category | Required adoption boundary |
|---|---|---|
| Human authentication | Enterprise IdP, federation, MFA, session/auth service. | Must meet issuer, assurance, recovery, tenant, evidence, and exit requirements. |
| Authorization | Policy administration/decision/enforcement capability. | Must support scoped current decisions, obligations, revocation, audit, simulation, and contracts. |
| Workload trust | Workload identity, attestation, certificate/mTLS, service-trust controls. | No implicit network trust or shared universal credential. |
| Secrets/keys | Secret manager, KMS/HSM, certificate authority, rotation/revocation tools. | Security-owned lifecycle; plaintext never becomes a general application artifact. |
| Protection | Encryption, masking/redaction, DLP/classification, access-review/export-control capability. | Implements policy with Data/domain ownership and residency/lifecycle evidence. |
| Detection/audit | SIEM, immutable event/audit, alert/case and investigation capability. | Does not become shadow customer-data store or replace domain/physical evidence. |
| Supply chain | Dependency/artifact/provenance/signing/scanning and CI security controls. | Deployment owns pipeline operation; Security defines assurance/response rules. |
| Testing | SAST/DAST, configuration/secret/IaC scanning, threat/penetration and assurance tooling. | Findings follow governed remediation, risk, and retest process. |

# Adoption Workflow

1. Identify the Security responsibility, affected owners, data/effect class, tenant/environment, trust boundary, and required outcome.
2. Check current ADRs, Reference Registry, Security control requirements, provider documentation, legal/compliance/residency, and exit implications.
3. Record a bounded proposal: technology/version/region, identity and authorization model, secrets/keys, data handling, interfaces, logging/audit, failure posture, capacity/cost, test plan, migration/rollback, and retirement path.
4. Obtain Security plus Architecture, Data, Operations/Deployment, and affected-domain review as applicable.
5. Prove isolation, least privilege, revocation, failure, observability, recovery, and portability in a controlled environment.
6. Record the decision and continuously re-evaluate material capability, provider, vulnerability, residency, cost, or contract change.

# Selection and Exit Requirements

Each adopted technology has a named owner, supported role, approved interface, trust/configuration inventory, secret/key/identity boundary, policy/control mapping, evidence source, SLO/failure posture, data/residency handling, dependency/vulnerability plan, export/migration route, rollback/restriction procedure, and retirement record.

Provider identifiers, SDK types, query/control dialects, and event formats remain behind owned adapters where practical. The platform preserves exportable policy/configuration/evidence references and cannot be locked into an unreviewed emergency account or opaque vendor-only control plane.

# Explicit Limits

- An identity provider does not own Platform Foundation tenant/membership facts or resource permission semantics.
- A policy engine does not own domain records, business workflows, or Data mechanisms.
- A secret manager does not authorize a business action or permit unrestricted secret disclosure.
- A SIEM/audit platform does not replace Data lifecycle/residency controls or domain event history.
- A framework, SDK, example, or starter repository is an implementation reference only; it does not import its security model, schema, identity, keys, deployment, or business architecture.

# Required Evidence

Maintain technology decision record, provider/security review, version and dependency inventory, threat/control mapping, configuration/identity/secrets references, test and exercise evidence, exception/risk record, change history, and exit/retirement plan.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created Security technology reference map. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with status model, role map, workflow, exit requirements, and explicit ownership limits. |
