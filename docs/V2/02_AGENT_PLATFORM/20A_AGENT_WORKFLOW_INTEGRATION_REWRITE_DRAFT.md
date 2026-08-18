# 20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `20_AGENT_WORKFLOW_INTEGRATION.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Integration workflow boundary.  

---

# Purpose

This draft defines the Agent Platform boundary for using workflows. An agent may propose, initiate, observe, resume, or respond to an approved workflow through the Integration Platform. It does not define or own workflow engines, workflow definitions, workflow state, workflow execution, scheduling, retries, compensation, or workflow governance.

The Integration Platform is the authoritative owner of workflow and asynchronous-execution behavior. The Agent Platform remains responsible for deciding whether an eligible agent behavior should request a workflow and for incorporating the authorized outcome into bounded agent execution.

---

# Ownership and Non-Ownership

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Workflow definition, lifecycle, step state, waits, callbacks, retries, compensation, and recovery | Integration Platform | Request an approved workflow by stable contract reference; consume the normalized outcome. |
| Connector, tool, credential, approval, and external-effect execution | Integration Platform, under Security controls | Propose an eligible action; never dispatch an external effect directly. |
| Authorization, delegated access, policy, secrets, and audit controls | Security Platform; Integration applies them to action execution | Supply bounded execution context and honor denial, expiry, revocation, and approval outcomes. |
| Conversation continuity, routing, handoff, and canonical interaction state | Conversation Platform | Receive authorized work and report a response or outcome through approved contracts. |
| Agent behavior, instruction hierarchy, capability selection, and execution intent | Agent Platform | Own and govern this responsibility. |

An Agent workflow reference is not a transfer of workflow ownership. Agent runtime state is not workflow state, and an agent response is not evidence that an external effect completed.

---

# Permitted Integration Flow

```text
Authorized conversation or event trigger
        ↓
Agent evaluates approved capability and current policy context
        ↓
Agent proposes a workflow request using a versioned Integration contract
        ↓
Integration validates authorization, approvals, idempotency, and dependencies
        ↓
Integration accepts, rejects, waits, completes, or reports an uncertain outcome
        ↓
Agent receives the normalized disposition and responds only within that disposition
        ↓
Conversation records the participant-visible outcome; Integration retains workflow authority
```

The Agent Platform must not infer completion from request acceptance, an optimistic client response, a provider callback, or a missing error. It must use the latest authorized workflow disposition.

---

# Workflow Request Contract

The Agent submits only the minimum information required by the approved Integration contract:

- Stable workflow identifier and compatible version or policy-approved alias.
- Tenant, actor, purpose, conversation, and agent-version references resolved by trusted services.
- An idempotency key scoped to the requested effect.
- Validated, classification-appropriate input parameters.
- Required approval or confirmation reference when the action policy requires one.
- Trace and correlation references that permit audit without exposing sensitive prompt or credential material.

The Agent must not supply client-controlled tenant authority, raw credentials, unrestricted instructions, unvalidated tool arguments, or hidden side-channel state. Integration must independently revalidate all authorization and execution inputs.

---

# Eligibility and Authorization

An agent may request a workflow only when all of the following are true:

1. The agent version exposes the relevant approved capability.
2. The current tenant is entitled to use it.
3. The request has an authorized trigger, actor, purpose, and tenant scope.
4. Required user confirmation, delegated access, separation of duties, or human approval is present and current.
5. The workflow version is approved for the relevant environment and risk classification.
6. The request complies with current Security, Integration, Conversation, channel, and data-handling constraints.

Model confidence, intent recognition, prior behavior, a visible UI control, or possession of a token is not authorization. On uncertainty, the Agent must request clarification, defer, or return a safe non-execution outcome.

---

# Outcome Model

Integration returns a normalized workflow disposition. The Agent must preserve its distinction from user-visible language:

| Disposition | Agent behavior |
|---|---|
| Rejected or denied | Do not retry or imply execution; provide the permitted explanation or escalation path. |
| Awaiting confirmation or approval | State what is needed without implying the action will occur. |
| Accepted or queued | State only that processing has begun, if policy allows. |
| Waiting on external input or callback | Preserve correlation and offer the approved follow-up path. |
| Completed | Communicate the approved outcome; do not fabricate details outside returned evidence. |
| Failed | Provide the safe failure disposition and eligible recovery option. |
| Unknown or reconciliation pending | Do not retry automatically or claim success; preserve idempotency and direct recovery through Integration. |
| Cancelled, expired, or revoked | Stop related agent work and resolve again under current policy. |

Workflow outcomes are durable Integration facts. The Agent may retain a bounded reference for execution continuity but must not create an independent workflow state machine.

---

# Asynchronous and Human-Approval Behavior

The Agent may not hold a live execution open merely because a workflow waits. It returns control to Conversation through the approved asynchronous pattern, then resumes only from a valid, authorized event or status resolution.

Human approval belongs to the Integration authorization and approval model. The Agent may explain a required approval or gather approved information, but cannot approve its own proposal, impersonate an approver, extend an expired approval, or convert silence into consent.

---

# Failure, Retry, and Recovery

- Only Integration determines whether a workflow or external effect is retryable.
- The Agent must reuse or reference the idempotency key when a retry is permitted; it must not create a new request to escape an uncertain outcome.
- Timeouts, delayed events, stale status, and provider errors are uncertain until Integration supplies a reconciled disposition.
- Agent fallback must be safe and non-effecting unless a separate authorized workflow is accepted.
- Suspension, revocation, tenant lifecycle change, or security containment terminates or revalidates related Agent activity according to the owning platform controls.

---

# Security, Privacy, and Tenant Isolation

All requests and outcomes are tenant-scoped, purpose-limited, least-privilege, versioned, and auditable. The Agent receives only the workflow data needed for behavior and participant communication. It must not expose credentials, internal approval notes, sensitive provider responses, cross-tenant identifiers, or protected data beyond the caller's authorized view.

Secrets, cryptographic material, token exchange, delegated credentials, and external-provider trust remain outside Agent Platform. The Agent uses approved opaque references and server-mediated contracts only.

---

# Observability and Evidence

For each material request, the Agent records or propagates correlation sufficient to link:

- tenant, actor, conversation, and agent version;
- the approved capability and workflow contract version;
- authorization and approval disposition references;
- idempotency and asynchronous correlation references;
- normalized workflow outcome and participant-visible response.

The Agent owns its behavior/evaluation evidence. Integration owns workflow execution evidence. Shared telemetry infrastructure remains outside both domains.

---

# Required Validation

Before approval, this boundary must be proven with tests that show:

- an authorized workflow request reaches Integration with trusted tenant and purpose context;
- denied, expired, revoked, and missing approvals prevent execution;
- duplicate and uncertain requests do not produce duplicate external effects;
- asynchronous completion resumes the correct conversation without transferring workflow ownership;
- cross-tenant data, credentials, and sensitive implementation details are not exposed to the Agent or participant;
- Agent language distinguishes queued, completed, failed, and unknown outcomes;
- security containment and tenant suspension stop or revalidate pending work.

---

# Authoritative References

- `07_INTEGRATION_PLATFORM/05_ACTION_AUTHORIZATION_AND_APPROVAL.md`
- `07_INTEGRATION_PLATFORM/06_ACTION_EXECUTION_AND_IDEMPOTENCY.md`
- `07_INTEGRATION_PLATFORM/07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md`
- `07_INTEGRATION_PLATFORM/13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md`
- `03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `09_SECURITY_PLATFORM/04_SESSION_TOKEN_AND_DELEGATED_ACCESS.md`

---

# Approval Conditions

The Agent and Integration review confirmed this document's request, outcome, authorization, evidence, and recovery boundaries. `20_AGENT_WORKFLOW_INTEGRATION.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.
