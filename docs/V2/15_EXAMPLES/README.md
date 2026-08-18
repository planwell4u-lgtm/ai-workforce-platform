# 15_EXAMPLES

**Version:** 1.2  
**Status:** Approved  
**Owner:** Architecture Owner and Engineering Owner  
**Phase:** Implementation Planning

---

# Purpose

`15_EXAMPLES` contains small, governed reference scenarios that show how approved V2 platform contracts fit together. Examples help contributors understand the intended vertical slice, interfaces, safety boundaries, evidence, and common failure paths before implementation begins.

Examples are explanatory artifacts. They do not create production APIs, domain state, security policy, data models, deployment configuration, provider credentials, or an alternate implementation path.

# Example Rules

- Every example identifies its authoritative architecture/module documents and uses their ownership boundaries.
- Examples use synthetic identities, tenants, data, channels, tools, and provider outcomes. They contain no secrets, participant content, production endpoints, or real credentials.
- An example labels request acceptance, agent intent, provider acknowledgement, participant delivery, business-action completion, and uncertainty as distinct outcomes.
- Examples do not demonstrate direct cross-module database access, client-held secrets, bypassed authorization, unreviewed tenant switching, or uncontrolled external effects.
- Copying an example into code requires the relevant owner contracts, Security/Data/Operations/Deployment/Observability/Testing review, and a proportionate implementation plan.

# Initial Document Set

1. `01_FIRST_VERTICAL_SLICE_REFERENCE_SCENARIO.md` — tenant-aware agent, Conversation, Voice/Digital Channel, Integration action, operator journey, and evidence flow.
2. `02_SAFE_FAILURE_AND_RECOVERY_SCENARIOS.md` — authorization denial, duplicate/timeout/uncertain outcome, channel/provider degradation, rollback, and reconciliation examples.
3. `03_CONTRACT_AND_EVENT_EXAMPLES.md` — safe illustrative API/event/correlation/outcome examples with compatibility boundaries.

# Reading Order

Read the relevant architecture/module document first. Then use the matching example only to understand a bounded interaction or failure path; never treat it as the owner contract or implementation specification.

# Current Status

The complete initial Examples set, Documents 01–03, is approved. It provides synthetic first-slice, failure/recovery, and contract/event references; it remains explanatory and is not production implementation.

# Related Documents

- `../01_ARCHITECTURE/README.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../02_AGENT_PLATFORM/README.md`
- `../03_CONVERSATION_PLATFORM/README.md`
- `../11_OPERATIONS_PLATFORM/README.md`
- `../14_TESTING_PLATFORM/README.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created the governed examples directory and initial reference plan. |
| 1.1 | 2026-08-09 | Finalized after architecture-boundary and maintainability review. |
| 1.2 | 2026-08-09 | Finalized the complete initial Examples set, Documents 01–03. |
