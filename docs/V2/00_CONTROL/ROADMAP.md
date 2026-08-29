# AI Workforce Platform Roadmap

**Version:** 1.5
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
| B4 Canonical conversation | Completed | Tenant-scoped session/turn lifecycle, correlation, duplicate/order safety, and recovery state. |
| B7 Jira support-ticket action | Staging verified | Authenticated request, PostgreSQL record, and Jira ticket creation completed. |
| B5–B9 vertical slice | Completed locally | Web Chat, Voice simulation, authorized operator journey, signed release artifacts, and exact-digest local rehearsal. |
| Client Workspace and Platform Admin | Planned | Deliver the tenant-facing frontend incrementally: Support Worker control center, governed worker lifecycle, channels, analytics, and separate internal administration. |
| Broader platform delivery | Planned | Expand channels, integrations, administration, resilience, and product capabilities only after the safe slice proves the architecture. |

# Current Focus

Checkpoint 2026-08-27: Front Desk test routing is complete. Sales Worker has
a fictional-catalog test endpoint and `/sales` chat screen; resume with Sales
Auth0 logout configuration and catalog-answer testing. Record the next
Voice-provider decision: evaluate LiveKit in a sandbox for
realtime media, then decide separately whether/when Twilio PSTN/SIP is in
scope. Cloud deployment remains deferred.

# Milestones

| Milestone | Status |
|---|---|
| Architecture and module documentation | Completed |
| Engineering implementation planning | Completed |
| Diagram review package | Review-ready |
| B0 Engineering Foundation | Completed |
| B1–B3 identity, persistence, and FAQ support agent | Completed |
| B4 Canonical conversation and turn control | Completed |
| B7 Jira support-ticket action | Staging verified |
| First vertical slice | Locally verified with signed exact-digest images |
| Production-ready enterprise platform | Future |

# Delivery Tracks

The platform has one master roadmap. Frontend and backend work are coordinated delivery tracks within each shared milestone, alongside Security, Data, Integration, Testing, Operations, and Deployment work. They must not become disconnected roadmaps with incompatible sequence or authority.

The planned frontend track is defined in `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`.

# Related Documents

- `02_PROJECT_ROADMAP.md`
- `10_PROJECT_STATUS.md`
- `../20_ENGINEERING/README.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.5 | 2026-08-27 | Added the planned Client Workspace and Platform Admin frontend delivery track under the shared platform roadmap. |
| 1.4 | 2026-08-18 | Reconciled the concise roadmap with B4–B9 completion, signed local release evidence, deferred cloud deployment, and the next Voice-provider decision. |
| 1.3 | 2026-08-17 | Recorded verified staging provider wiring and protected FAQ agent; set B4 as next. |
| 1.2 | 2026-08-09 | Recorded B0 Engineering Foundation completion and B1 tenant-aware identity/API entry as next. |
| 1.1 | 2026-08-09 | Replaced stale phase/module statuses with the current implementation-readiness roadmap. |
| 1.0 | 2026-08-05 | Created the initial concise roadmap. |
