# 03_CONTRACT_AND_EVENT_EXAMPLES

**Version:** 1.1  
**Status:** Approved  
**Owner:** Architecture Owner and Engineering Owner  
**Phase:** Implementation Planning

---

# Purpose

This document provides synthetic illustrative API, event, correlation, and outcome examples for the first vertical slice. It shows the shape of safe contracts without defining a production protocol, schema registry, endpoint, data model, authentication mechanism, or provider integration.

# Example Contract Rules

- The actual owner publishes and versions each contract; examples do not establish ownership or compatibility policy.
- Trusted identity, tenant, membership, authorization, and consent context are validated by the receiving boundary; caller-supplied fields are not authority.
- Correlation and idempotency references link work safely but are not secrets, participant identities, or permission tokens.
- Outcomes are explicit and separate: accepted, processing, restricted, failed, uncertain, reconciled, requested delivery, provider acceptance, participant delivery, and business result.
- Payloads are synthetic and omit protected data, secrets, raw messages/prompts/transcripts, and provider credentials.

# Example 1 — Authorized Agent Status Request

```json
{
  "contract_version": "v1",
  "request_id": "req-example-100",
  "correlation_id": "corr-example-100",
  "agent_reference": "agent-avery-v1",
  "requested_view": "operator_status"
}
```

The server derives the tenant, identity, membership, entitlement, and authorization from trusted context. The request does not include a trusted tenant ID, role claim, provider credential, or direct data-store reference.

```json
{
  "contract_version": "v1",
  "agent_reference": "agent-avery-v1",
  "status": "active",
  "configuration_version": "cfg-example-7",
  "visibility": "authorized_snapshot",
  "correlation_id": "corr-example-100"
}
```

This response is a presentation snapshot, not client-side authority to mutate the agent or bypass a later authorization change.

# Example 2 — Normalized Interaction Candidate

```json
{
  "event_type": "channel.interaction.candidate.v1",
  "event_id": "evt-example-200",
  "occurred_at": "2026-08-09T12:00:00Z",
  "correlation_id": "corr-example-200",
  "channel_reference": "digital-example",
  "channel_interaction_reference": "channel-msg-example-200",
  "capability_reference": "digital-capability-v1",
  "consent_reference": "consent-example-200",
  "payload_reference": "protected-input-reference"
}
```

Digital Channel validates channel/provider input and forwards a normalized candidate. Conversation decides whether and how it associates to canonical Conversation/session state. The event does not claim a participant identity, canonical conversation, Agent decision, or participant delivery.

# Example 3 — Conversation Turn and Agent Intent

```json
{
  "event_type": "conversation.turn.authorized.v1",
  "event_id": "evt-example-300",
  "conversation_reference": "conv-example-100",
  "session_reference": "session-example-100",
  "turn_reference": "turn-example-3",
  "agent_reference": "agent-avery-v1",
  "correlation_id": "corr-example-200",
  "authorization_reference": "authz-example-300"
}
```

```json
{
  "event_type": "agent.action.intent.v1",
  "event_id": "evt-example-301",
  "intent_reference": "intent-example-301",
  "integration_action_type": "appointment_lookup",
  "idempotency_reference": "idem-example-301",
  "correlation_id": "corr-example-200",
  "policy_reference": "policy-example-4"
}
```

Conversation owns turn authority; Agent owns intent. Neither event executes the external action. Integration validates current authorization and action constraints before any provider submission.

# Example 4 — Integration Outcome With Uncertainty

```json
{
  "event_type": "integration.action.outcome.v1",
  "event_id": "evt-example-400",
  "intent_reference": "intent-example-301",
  "idempotency_reference": "idem-example-301",
  "outcome": "uncertain",
  "reconciliation_reference": "reconcile-example-400",
  "retry_permitted": false,
  "correlation_id": "corr-example-200"
}
```

`uncertain` does not mean failure or success. The Agent and Conversation may communicate only the approved pending state. Integration reconciliation, not a blind retry, determines whether a follow-up action is safe.

# Example 5 — Requested Delivery Versus Delivery Evidence

```json
{
  "event_type": "conversation.output.requested.v1",
  "event_id": "evt-example-500",
  "conversation_reference": "conv-example-100",
  "turn_reference": "turn-example-3",
  "channel_reference": "digital-example",
  "output_reference": "protected-output-reference",
  "correlation_id": "corr-example-200"
}
```

```json
{
  "event_type": "channel.delivery.outcome.v1",
  "event_id": "evt-example-501",
  "delivery_reference": "delivery-example-501",
  "requested_output_event": "evt-example-500",
  "outcome": "provider_accepted",
  "participant_delivery": "not_verified",
  "correlation_id": "corr-example-200"
}
```

Provider acceptance is not participant delivery. Voice and Digital Channel contracts define their own delivery evidence and reconciliation behavior.

# Compatibility Example

An additive `safe_error_category` field may be introduced in `v1` when consumers ignore unknown fields and the producer documents its semantic owner. Removing or changing an existing outcome's meaning requires a new compatible contract version, consumer migration inventory, support window, test evidence, and retirement record.

# What These Examples Do Not Authorize

They do not authorize direct database access, event replay without idempotency/reconciliation controls, secrets in payloads, client-provided tenant/role authority, real appointment lookup, cross-tenant correlation, provider assumptions, or production deployment. The owning module's approved contract and implementation plan determine those details.

# Related Documents

- `README.md`
- `01_FIRST_VERTICAL_SLICE_REFERENCE_SCENARIO.md`
- `02_SAFE_FAILURE_AND_RECOVERY_SCENARIOS.md`
- `../01_ARCHITECTURE/06_EVENT_DRIVEN_ARCHITECTURE.md`
- `../03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md`
- `../07_INTEGRATION_PLATFORM/06_ACTION_EXECUTION_AND_IDEMPOTENCY.md`
- `../13_OBSERVABILITY_PLATFORM/03_TELEMETRY_DATA_MODEL_AND_CORRELATION.md`
- `../14_TESTING_PLATFORM/05_CONTRACT_INTEGRATION_AND_END_TO_END_TESTING.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created synthetic contract and event examples. |
| 1.1 | 2026-08-09 | Finalized after ownership, compatibility, outcome, and maintainability review. |
