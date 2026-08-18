# 00_CONTROL

**Version:** 1.2  
**Status:** Active  
**Phase:** Implementation Readiness & First Vertical Slice

---

# Purpose

`00_CONTROL` is the governance and continuity layer for the AI Workforce Platform. It defines the project direction, architecture rules, ownership, documentation standards, decisions, change process, development workflow, and current state that humans and AI assistants must use before changing the platform.

It governs implementation; it does not replace module-specific architecture or code documentation.

---

# Authoritative Navigation

`07_DOCUMENTATION_INDEX.md` is the complete navigation and authoritative-source map. The core control documents are:

| File | Purpose |
|---|---|
| `01_PROJECT_CHARTER.md` | Project vision and objectives |
| `02_PROJECT_ROADMAP.md` | Phases, milestones, and delivery sequence |
| `03_ARCHITECTURE_PRINCIPLES.md` | Platform-wide architecture rules |
| `04_SYSTEM_BOUNDARIES.md` | Capability ownership boundaries |
| `05_MODULE_OWNERSHIP.md` | Module responsibilities |
| `06_DOCUMENTATION_STANDARDS.md` | Documentation lifecycle and quality standards |
| `07_DOCUMENTATION_INDEX.md` | Documentation discovery and authoritative-source map |
| `08_DECISION_LOG.md` | Material decisions and rationale |
| `09_CHANGE_MANAGEMENT.md` | Change approval and control process |
| `10_PROJECT_STATUS.md` | Current state, risks, blockers, and priorities |
| `11_TERMINOLOGY_GLOSSARY.md` | Shared vocabulary |
| `12_DEVELOPMENT_WORKFLOW.md` | Standard delivery lifecycle |
| `AI_DRIVEN_ENTERPRISE_SAAS_DEVELOPMENT_PLAYBOOK.md` | AI-assisted implementation operating procedure |

`PROJECT_CONTEXT.md` may provide a concise orientation for contributors. It must remain aligned with `01_PROJECT_CHARTER.md` and the approved control documents.

---

# AI Assistant Reading Order

For a non-trivial change, read:

1. `07_DOCUMENTATION_INDEX.md`
2. `01_PROJECT_CHARTER.md` and `PROJECT_CONTEXT.md`, where applicable
3. `03_ARCHITECTURE_PRINCIPLES.md`, `04_SYSTEM_BOUNDARIES.md`, and `05_MODULE_OWNERSHIP.md`
4. `10_PROJECT_STATUS.md`, `02_PROJECT_ROADMAP.md`, and relevant decisions in `08_DECISION_LOG.md`
5. `AI_DRIVEN_ENTERPRISE_SAAS_DEVELOPMENT_PLAYBOOK.md`
6. Relevant module documentation, code, tests, and contracts
7. `09_CHANGE_MANAGEMENT.md` when the change is material or production-sensitive

This order prevents incorrect assumptions, duplicate implementations, and silent architecture changes.

---

# Change Rules

Before adding or changing a capability:

- Confirm that it does not already exist and identify its owning module.
- Review the relevant decisions, boundaries, contracts, and module documentation.
- Follow the AI-driven playbook for task scope, change classification, validation, review, and durable change evidence.
- Update the authoritative documentation and project state when behavior, ownership, risks, decisions, or next work change.

Code must follow approved architecture. Architecture must not be changed silently for implementation convenience.

---

# Relationship with Platform Modules

Each platform directory owns the design and implementation guidance for its domain. `00_CONTROL` provides the cross-platform governance that keeps those modules coherent; it is not a duplicate architecture layer.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.2 | 2026-08-09 | Updated the control-area phase after completion of architecture and Engineering planning; aligned current-status and roadmap summaries. |
| 1.0 | 2026-08-05 | Initial control-directory overview. |
| 1.1 | 2026-08-07 | Replaced legacy navigation with the numbered control-document set and added the AI-assisted development playbook. |
