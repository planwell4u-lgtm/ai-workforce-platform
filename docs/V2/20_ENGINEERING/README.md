# 20_ENGINEERING

**Version:** 1.6
**Status:** Approved  
**Owner:** Engineering Owner  
**Phase:** Implementation Planning

---

# Purpose

`20_ENGINEERING` translates the approved V2 architecture into implementation-ready plans, contracts, backlog slices, validation evidence, and delivery records. It is the bridge between architecture approval and code. It does not replace the architecture, module contracts, Security/Data/Operations/Deployment/Observability/Testing controls, or the control-layer change process.

# Ownership

Engineering documentation owns:

- Bounded implementation plans, vertical-slice backlogs, sequencing, and dependency mapping.
- Codebase/module organization guidance that realizes approved architecture without changing its ownership.
- Feature-level acceptance, validation, rollout/recovery, and documentation-alignment records.
- Implementation decision capture that routes material architecture changes to the correct control process.

It does not own:

- Product scope, platform boundaries, canonical domain facts, security policy, data lifecycle, deployment controls, operational decisions, telemetry infrastructure, test standards, or domain contracts.
- Approval to bypass a required owner, public interface, migration, or security/release gate.

# Initial Document Set

1. `01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md` — the smallest safe end-to-end build sequence, owners, dependencies, acceptance criteria, and evidence.
2. `02_ENGINEERING_WORKSPACE_AND_MODULE_STRUCTURE.md` — source-code organization, package/module boundaries, and dependency rules aligned to V2 ownership.
3. `03_ENGINEERING_DELIVERY_WORKFLOW.md` — feature planning, review, validation, release, recovery, and durable change-record workflow.
4. `04_IMPLEMENTATION_DECISION_AND_TRACEABILITY.md` — links between requirements, architecture, code, tests, migrations, operations, and decisions.
5. `05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md` — approved and implemented,
   constrained contract for the Cloud agent to read only the current tenant's
   approved support-FAQ context.

The set may expand only when an implementation need cannot be covered by an existing authoritative module document.

# Reading Order

Read `00_CONTROL` and the relevant platform modules first. Then read Document 01 before starting the first code change, Document 02 before creating packages/services, Document 03 before executing a feature, and Document 04 when recording a material implementation decision or evidence trail.

# Engineering Invariants

- Build the smallest complete vertical slice before expanding channels, integrations, administration, or autonomous behavior.
- Every code change has a primary owner, trusted tenant/identity/authorization context, clear interface and state ownership, proportionate tests, observability, and recovery path.
- Code consumes approved APIs, events, and contracts; it does not directly access another module's internal data or redefine its semantics.
- A feature is not done until its documentation, validation evidence, and operational/recovery behavior are aligned with the approved architecture.
- The repository—not chat history—is the durable record of implementation decisions, assumptions, risks, and next work.

# Initial Delivery Boundary

The first implementation plan proves one authorized tenant can use one approved agent through canonical Conversation, one Voice and one Digital Channel path, one bounded Integration action, and one authorized operator experience, with required Security, Data, Operations, Deployment, Observability, and Testing evidence.

## Staging verification records

- `B4_B5_STAGING_VERIFICATION_RECORD.md` — configured-staging evidence for
  Web Chat persistence, Admin history, saved Jira ticket state, and repeat
  escalation suppression.
- `LIVEKIT_LOCAL_SANDBOX_EVALUATION_RECORD.md` — bounded local LiveKit
  realtime-media evaluation evidence; it excludes Twilio and cloud deployment.

It excludes broad multi-tenant administration, additional channels, unbounded integrations, autonomous changes, direct provider/database access, and unrelated infrastructure expansion.

# Change Rules

- Every implementation plan references its authoritative architecture and owner documents.
- A plan records what is in scope, out of scope, assumed, blocked, or deferred before code is written.
- Material architecture, security, data, deployment, or public-contract deviations are routed through `00_CONTROL/09_CHANGE_MANAGEMENT.md`.
- Update the relevant module docs, project status, decision record, tests, and operational evidence when implementation materially changes reality.

# Current Status

The Engineering implementation-planning set is complete. Documents 01–04 define the first vertical slice, workspace boundaries, delivery workflow, and durable decision/evidence trace. B0–B9 and the approved read-only FAQ boundary are implemented and locally verified, including the `v0.2.0-rc.1` exact-digest signed-image rehearsal. The local LiveKit and Cloud-agent rehearsals are complete. Cloud deployment and Twilio remain deferred.

# Related Documents

- `../00_CONTROL/AI_DRIVEN_ENTERPRISE_SAAS_DEVELOPMENT_PLAYBOOK.md`
- `../00_CONTROL/10_PROJECT_STATUS.md`
- `../01_ARCHITECTURE/README.md`
- `../02_AGENT_PLATFORM/README.md`
- `../03_CONVERSATION_PLATFORM/README.md`
- `../11_OPERATIONS_PLATFORM/README.md`
- `../12_DEPLOYMENT_PLATFORM/README.md`
- `../14_TESTING_PLATFORM/README.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.6 | 2026-08-23 | Recorded implementation and exact signed-image rehearsal of the approved constrained Cloud-agent FAQ boundary. |
| 1.5 | 2026-08-22 | Added the proposed, separately gated read-only application-data boundary for Cloud-agent support-FAQ context. |
| 1.4 | 2026-08-18 | Reconciled the Engineering status with completed B0–B9 local slice evidence and the next Voice-provider decision. |
| 1.2 | 2026-08-09 | Completed the initial Engineering document set (02–04) and confirmed the pre-coding planning boundary. |
| 1.0 | 2026-08-09 | Created the Engineering implementation-planning entry point. |
| 1.1 | 2026-08-09 | Finalized after architecture-boundary and maintainability review. |
