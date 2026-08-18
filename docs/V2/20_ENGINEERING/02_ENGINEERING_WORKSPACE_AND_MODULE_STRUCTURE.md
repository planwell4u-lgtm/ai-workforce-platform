# 02_ENGINEERING_WORKSPACE_AND_MODULE_STRUCTURE

**Version:** 1.1  
**Status:** Approved  
**Owner:** Engineering Owner  
**Phase:** Implementation Planning

---

# Purpose

This document defines the source-code organization rules for implementing V2. It makes module ownership visible in the repository without turning folders, packages, or shared libraries into a second architecture.

# Required Workspace Shape

The workspace must separate executable products, module-owned capabilities, shared contracts, and delivery tooling. Names may follow the selected language ecosystem, but the boundary meaning must remain stable.

```text
apps/                 deployable entry points and operator-facing products
platform/             module-owned application capabilities
contracts/            versioned public APIs, events, schemas, and SDK surfaces
shared/               small technical utilities with no domain ownership
infra/                environment, deployment, policy, and observability definitions
tests/                cross-module, end-to-end, performance, and resilience suites
docs/                 approved architecture, decisions, runbooks, and evidence links
```

Each `platform/<module>` area corresponds to one approved V2 owner. The first slice may initially create only the module areas it uses, but must preserve the layout for later independent evolution.

# Dependency Rules

- An application composes public module interfaces; it does not bypass them to reach module internals or storage.
- A module may depend on its own internals, `contracts`, and narrow technical utilities in `shared`.
- Cross-module calls use an approved API, command, query, event, or adapter contract. Imports between another module's internal packages are prohibited.
- `contracts` contains types and compatibility rules, not business policy, provider clients, database access, or orchestration.
- `shared` is limited to genuinely generic technical capabilities such as correlation identifiers, error envelopes, and safe configuration helpers. Moving domain logic there requires the relevant owner approval.
- Provider SDKs and database drivers are kept behind the owning module's adapter/persistence boundary.
- Test fixtures may cross module boundaries only through public contracts or explicitly owned test-support interfaces.

# Ownership Mapping

| Repository area | Primary responsibility | Must not contain |
|---|---|---|
| `apps/` | Composition, routing, dependency wiring, presentation entry points | Domain state ownership or direct persistence access |
| `platform/<module>/api` | Public commands, queries, events, and contract adapters | Other modules' internal behavior |
| `platform/<module>/domain` | Module-owned behavior and state rules | Provider-specific transport or unrelated workflow logic |
| `platform/<module>/adapters` | Provider, transport, persistence, and external-system implementations | Business-policy redefinition |
| `contracts/` | Versioned interoperable interface definitions | Secrets, direct storage access, or runtime policy |
| `infra/` | Declarative delivery controls and environment configuration references | Application domain decisions or plaintext credentials |
| `tests/` | Cross-boundary assurance and evidence-producing scenarios | A shadow implementation of production behavior |

# Configuration, Secrets, and Data Boundaries

- Configuration is typed, validated at startup, tenant-safe, and documented by purpose and owner.
- Source code, tests, and documentation contain secret references or placeholders only; no real credentials, private keys, or production data are committed.
- A module writes only through its owned persistence mechanism. Read models exposed to others must be deliberate public contracts.
- Migrations are versioned, owned, reviewed, tested, and paired with rollback or recovery instructions before use in a controlled environment.
- Correlation, tenant, identity, and authorization context travel through approved request/event boundaries and are never reconstructed from an untrusted client assertion.

# First-Slice Setup Checklist

1. Create the workspace shape and ownership boundary checks before feature packages proliferate.
2. Define the first API/event schemas in `contracts` and publish compatibility expectations.
3. Establish formatting, linting, type checking, unit tests, integration tests, and a minimal CI gate.
4. Provide safe local configuration, sandbox references, fake/test adapters, and no-credential contributor setup.
5. Add architecture-boundary tests or lint rules that detect prohibited internal imports and direct storage access.
6. Record exceptions, temporary adapters, and deferred packaging choices in the engineering decision record.

# Acceptance Criteria

The workspace structure is ready when a new contributor can identify the owner of each package, run the documented checks without production credentials, introduce one module through a public contract, and demonstrate that prohibited cross-module imports and storage access are rejected or review-visible.

# Related Documents

- `README.md`
- `01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `03_ENGINEERING_DELIVERY_WORKFLOW.md`
- `../00_CONTROL/05_MODULE_OWNERSHIP.md`
- `../01_ARCHITECTURE/08_ARCHITECTURE_PRINCIPLES_APPLICATION.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.1 | 2026-08-09 | Created the approved workspace and module-boundary implementation standard. |
