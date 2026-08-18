# 01_FIRST_VERTICAL_SLICE_REFERENCE_SCENARIO

**Version:** 1.1  
**Status:** Approved  
**Owner:** Architecture Owner and Engineering Owner  
**Phase:** Implementation Planning

---

# Purpose

This synthetic scenario illustrates the approved first vertical slice. It demonstrates how one authorized tenant can use one governed agent through Voice and a Digital Channel, maintain canonical Conversation continuity, request one bounded Integration action, and provide an authorized operator with safe visibility and intervention.

It is illustrative only. Module contracts and owner documents remain authoritative.

# Synthetic Scenario

Tenant `northstar-example` has an approved customer-support agent named `Avery`. An authorized operator, `Casey`, configures and reviews the agent. A participant begins an interaction through the Digital Channel and later uses the approved Voice path. Avery retrieves approved business knowledge and, after required authorization, requests a simulated appointment lookup action through Integration.

All names, identifiers, content, and outcomes below are synthetic. No real participant data, credentials, provider endpoint, or business action is represented.

# Preconditions

1. Platform Foundation has established the tenant, membership, entitlement, and approved configuration facts.
2. Security has authenticated Casey and the relevant workloads and can make current tenant-scoped authorization decisions.
3. Agent Platform has published Avery version `v1` with approved instructions, Knowledge/Memory access, and tool eligibility.
4. Conversation, Voice, Digital Channel, Integration, Data, Observability, Testing, Operations, and Deployment contracts are available in the selected controlled environment.
5. The Integration appointment lookup uses a simulation or approved sandbox with idempotency and uncertain-outcome behavior.

# End-to-End Flow

```text
Authorized operator / participant
        |
        v
Trusted tenant + identity + authorization context
        |
        +--> Operator views Avery through Frontend backend contracts
        +--> Digital Channel receives validated participant input
        |
        v
Conversation creates/associates canonical conversation and session
        |
        v
Agent Avery v1 receives approved context
        +--> governed Knowledge retrieval
        +--> authorized Memory use when permitted
        +--> Integration action request when needed
        |
        v
Conversation owns response turn and channel request
        |
        +--> Digital Channel delivery evidence
        +--> Voice interaction through approved channel contract
        |
        v
Operator sees authorized status/outcome; telemetry, audit, alert/runbook, and test evidence correlate the flow
```

# Step-by-Step Reference

| Step | Owner | Illustrative action | Required evidence / boundary |
|---|---|---|---|
| 1 | Platform Foundation + Security | Casey enters the approved tenant scope and requests Avery status. | Trusted identity/membership/entitlement and backend authorization; route visibility alone is not authorization. |
| 2 | Frontend + Agent | Frontend renders the authorized Avery configuration/status snapshot. | No secrets/direct database access; server remains authoritative. |
| 3 | Digital Channel | Validated inbound participant message becomes a normalized interaction request. | Channel identity/consent/capability evidence; no channel reasoning loop. |
| 4 | Conversation | Creates or associates canonical conversation `C-100` and session `S-100`. | Tenant-safe correlation, routing/turn authority, duplicate/order safety. |
| 5 | Agent + Knowledge/Memory | Avery v1 receives authorized context and retrieves approved support information. | Agent/version/context provenance; governed retrieval/memory scope and redaction. |
| 6 | Agent + Integration + Security | Avery requests simulated appointment lookup `A-100`. | Current authorization/tool eligibility, idempotency key, audit, timeout/uncertainty path. |
| 7 | Conversation + Digital Channel | Conversation authorizes one response delivery request. | Requested output is distinct from provider acceptance/participant delivery. |
| 8 | Voice + Conversation | Participant continues via approved Voice interaction associated with `C-100` when authorized. | Consent/context grant, channel capability, interruption/disconnect, no unverified identity merge. |
| 9 | Frontend + Conversation/Integration | Casey views authorized conversation/action status and requests permitted intervention. | Backend authorization, tenant scope, bounded intervention; UI cannot alter canonical state directly. |
| 10 | Observability + Operations + Testing | Trace/evidence links the journey, alert/runbook is available, and tests retain results. | Safe telemetry, no protected content, release/rollback/recovery evidence. |

# Outcome Distinctions

The scenario never reports a generic “success.” It records distinct outcomes:

| Outcome | Owning contract |
|---|---|
| Request accepted | API/channel/Conversation boundary |
| Agent response/action intent | Agent Platform |
| Integration request accepted, failed, or uncertain | Integration Platform |
| Provider/channel accepted output | Voice or Digital Channel Platform |
| Participant delivery | Voice or Digital Channel Platform with its evidence |
| Appointment lookup business result | Integration owner/provider reconciliation |
| Canonical conversation continuity | Conversation Platform |
| Operator intervention result | Conversation/Agent/Integration owner as applicable |

# Safe Failure Examples

- If Casey loses membership or changes tenant, the frontend refreshes and backend access is denied or re-scoped; cached visibility does not remain authority.
- If the participant callback is invalid or consent is absent, the channel rejects/restricts it without creating an unauthorized Conversation or Agent turn.
- If the appointment action times out, Integration records `uncertain`; Avery does not repeat the action until reconciliation permits it.
- If Voice disconnects, the platform records channel evidence and current uncertainty; it does not claim participant delivery or transfer turn ownership without Conversation authority.
- If telemetry is delayed, Operations sees the limitation; domain processing follows its approved behavior and does not manufacture a success/failure outcome.

# Evidence Checklist

- tenant, identity, membership, entitlement, authorization, and audit references;
- agent/version, Knowledge/Memory access, tool eligibility, and evaluation references;
- canonical conversation/session, correlation, routing, and handoff/turn evidence;
- channel consent/capability, delivery/uncertainty, interruption/disconnect evidence;
- Integration authorization/idempotency/timeout/reconciliation/audit evidence;
- safe trace/log/metric/alert/runbook references and access/redaction proof;
- contract, end-to-end, tenant/security negative, failure/recovery, accessibility, and release/rollback test evidence.

# What This Example Does Not Demonstrate

This example does not demonstrate real provider integration, production tenant onboarding, broad role administration, cross-channel identity merging, live booking, autonomous knowledge/prompt changes, direct database access, or a production release approval. Each requires its own owner-approved implementation and evidence.

# Related Documents

- `README.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../01_ARCHITECTURE/02_ONE_BRAIN_MULTI_CHANNEL.md`
- `../02_AGENT_PLATFORM/README.md`
- `../03_CONVERSATION_PLATFORM/README.md`
- `../04_VOICE_PLATFORM/README.md`
- `../17_DIGITAL_CHANNEL_PLATFORM/README.md`
- `../07_INTEGRATION_PLATFORM/README.md`
- `../14_TESTING_PLATFORM/README.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created the synthetic first vertical-slice reference scenario. |
| 1.1 | 2026-08-09 | Finalized after boundary, outcome, failure, and maintainability review. |
