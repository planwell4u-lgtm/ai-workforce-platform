# AI Workforce Platform Roadmap

**Version:** 1.3  
**Status:** Active  
**Phase:** Implementation Readiness & First Vertical Slice

---

# Purpose

This is the concise delivery roadmap. `02_PROJECT_ROADMAP.md` is the detailed authoritative roadmap; this file summarizes the active sequence without redefining module ownership or scope.

# Delivery Sequence

| Stage | Status | Outcome |
|---|---|---|
| Governance and architecture | Completed | Approved ownership, boundaries, contracts, and cross-platform rules. |
| Platform module documentation | Completed | Approved module sets, including Operations, Deployment, Observability, Testing, Examples, and Engineering planning. |
| Diagram finalization | In final review | Draw.io and SVG set complete; PNG exports and reviewer metadata pending. |
| B0 Engineering Foundation | Completed | Workspace/module structure, safe configuration, quality checks, test runner, and CI baseline. |
| B1–B3 foundation and governed FAQ agent | Completed | Auth0 identity, Supabase persistence, tenant authorization, durable audits, and protected FAQ answer flow. |
| B4 Canonical conversation | Next | Tenant-scoped session/turn lifecycle, correlation, duplicate/order safety, and recovery state. |
| B7 Jira support-ticket action | Staging verified | Authenticated request, PostgreSQL record, and Jira ticket creation completed. |
| Remaining vertical slice | Planned | Digital Channel, Voice, operator journey, and release-assurance work. |
| Broader platform delivery | Planned | Expand channels, integrations, administration, resilience, and product capabilities only after the safe slice proves the architecture. |

# Current Focus

Start B4 Canonical Conversation and Turn Control. Keep the upcoming Twilio and LiveKit adapters behind this shared conversation boundary.

# Milestones

| Milestone | Status |
|---|---|
| Architecture and module documentation | Completed |
| Engineering implementation planning | Completed |
| Diagram review package | Review-ready |
| B0 Engineering Foundation | Completed |
| B1–B3 identity, persistence, and FAQ support agent | Completed |
| B4 Canonical conversation and turn control | Next |
| B7 Jira support-ticket action | Staging verified |
| First vertical slice | Planned |
| Production-ready enterprise platform | Future |

# Related Documents

- `02_PROJECT_ROADMAP.md`
- `10_PROJECT_STATUS.md`
- `../20_ENGINEERING/README.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.3 | 2026-08-17 | Recorded verified staging provider wiring and protected FAQ agent; set B4 as next. |
| 1.2 | 2026-08-09 | Recorded B0 Engineering Foundation completion and B1 tenant-aware identity/API entry as next. |
| 1.1 | 2026-08-09 | Replaced stale phase/module statuses with the current implementation-readiness roadmap. |
| 1.0 | 2026-08-05 | Created the initial concise roadmap. |
