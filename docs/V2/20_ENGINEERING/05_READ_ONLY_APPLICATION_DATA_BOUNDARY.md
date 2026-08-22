# Read-Only Application-Data Boundary

**Status:** Approved for constrained implementation  
**Date:** 2026-08-22  
**Scope:** Bounded Cloud voice-agent access to approved support knowledge only

---

## Decision

Introduce an **Application Data Context Broker** only after approval. It may
return a short-lived, tenant-scoped set of published support-FAQ snippets to
the approved Cloud agent for one active support interaction. It is a read-only
context source, not a general data API, database connection, or tool/action
gateway.

The Project Owner explicitly approved this constrained scope on 2026-08-22.
Implementation may proceed only within this document's controls.

## In Scope

- The current tenant's published, versioned FAQ entries already approved for
  participant-facing support answers.
- A minimal retrieval request for `support.answer` only.
- Maximum three redacted snippets, each with a source/version reference and
  configured size limit.
- Transient use within one server-issued room/conversation correlation and a
  short expiry (five minutes or less).
- Tenant, agent-version, purpose, policy-decision, source-version, correlation,
  and outcome metadata in audit evidence; raw snippet text is excluded from
  audit and telemetry.

## Explicitly Out of Scope

- Conversation history, microphone audio, transcripts, recordings, memory,
  customer profiles, attachments, tickets, credentials, payment data, or any
  personal/sensitive data.
- Direct PostgreSQL, Supabase, storage, vector-store, or backend-network access
  from the Cloud agent.
- Writes, Jira escalation, arbitrary HTTP tools, MCP tools, actions, number
  rental, telephony, recording, or automatic publication.
- Cross-tenant lookup, bulk export, cache persistence, provider training use,
  or fallback to broader data when retrieval fails.

## Required Request and Response Contract

The Cloud agent uses a dedicated workload identity to call one broker endpoint.
The backend validates that identity and independently rechecks current tenant,
agent version, room/conversation correlation, purpose, expiry, and policy
decision before retrieval. A browser token, room token, model output, or a
caller-provided tenant identifier is never accepted as authority for this read.

```text
Read request
  workload identity + tenant_ref + agent_version_ref + conversation_ref
  + room_ref + purpose=support.answer + bounded query + correlation_ref

Read response
  context_ref + expires_at + source_version_ref + snippets[]
  + retrieval_outcome
```

The broker derives tenant and data scope from trusted server-side facts. The
request may supply a bounded query but cannot choose a source, classification,
tenant, record identifier, or output scope. The response contains only approved
plain-text excerpts and source/version references; it never returns a database
identifier, secret, policy detail, or undisclosed record.

## Enforcement and Data Flow

```text
Cloud agent workload
  -> authenticated, purpose-bound broker request
  -> Security decision + tenant/lifecycle recheck
  -> Agent context assembly and minimization
  -> Knowledge/Data-owned published FAQ retrieval
  -> bounded transient context response
  -> Cloud agent response to the current participant
```

Security owns the authorization decision. Agent owns context assembly and
consumption. Knowledge/Data own publication, source version, classification,
and retrieval implementation. Conversation owns participant interaction and
correlation. Voice only transports realtime media. The broker does not take
ownership of any of those concerns.

## Safety Controls

- Deny by default: missing, expired, revoked, mismatched, suspended, or
  unavailable authorization produces no context.
- The workload credential is server-to-server, scoped to this one read action,
  stored only in the approved Cloud runtime, rotated and revocable; it is never
  sent to the browser or included in dispatch metadata.
- The broker applies an allowlist for `support.answer`, published FAQ source,
  tenant, agent version, classification, and response limits before any data
  lookup.
- Retrieval is non-mutating. Retry is allowed only for the same request
  correlation and cannot broaden query, source, tenant, or expiry.
- Context expires after the interaction and must not be written to browser
  storage, voice-room metadata, logs, traces, agent memory, or provider tools.
- The agent must state that it cannot access an account or perform an action
  when the requested information is unavailable; it must not infer or invent
  protected data.

## Acceptance Evidence Before Enablement

1. A reviewed policy decision allows only the approved tenant, Cloud workload,
   agent version, purpose, source version, and current interaction correlation.
2. Contract tests deny forged tenant/room/conversation identifiers, expired
   workload credentials, policy outage, revoked membership, source-version
   mismatch, oversized query/result, and every prohibited data class.
3. Tenant-isolation tests show that a request cannot retrieve another tenant's
   published FAQ, even with a valid Cloud workload credential.
4. A browser rehearsal proves the agent receives only approved FAQ snippets,
   answers a safe support question, and exposes no credential or raw context in
   the browser, agent logs, backend audit, or telemetry.
5. A failure rehearsal proves the agent receives no context and produces the
   approved safe-unavailable response when the broker, policy, or retrieval
   path is unavailable.
6. Security, Data, Knowledge, Agent, Voice, and Testing owners approve the
   contract, provider-data terms, retention/egress conditions, and rollback.

## Rollback and Operations

The feature flag defaults off. Disabling it immediately blocks new broker reads
and revokes the Cloud workload credential; active voice transport continues
without application context. Operations retain minimized decision/outcome
evidence and alert on denial spikes, scope mismatches, source/version mismatch,
and attempted prohibited data classes. No automated fallback connects the agent
to a broader source.

## Approval Record

The required approvals were explicitly granted on 2026-08-22 for this exact
read-only support-FAQ scope. They do not approve any excluded capability.

- [x] Security approves the workload identity, policy action, expiry, and
  revocation behavior.
- [x] Data and Knowledge approve the exact published FAQ classification,
  source/version, retention, and provider-egress treatment.
- [x] Agent and Conversation approve context/output semantics and safe failure.
- [x] Voice and provider owners approve the Cloud runtime boundary without
  recording, telephony, or browser-secret exposure.
- [x] Testing approves the acceptance and negative-path evidence.
- [x] The Project Owner authorizes implementation after all approvals above.

## Authoritative References

- `../02_AGENT_PLATFORM/11_AGENT_CONTEXT_MODEL.md`
- `../02_AGENT_PLATFORM/24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md`
- `../02_AGENT_PLATFORM/25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md`
- `../02_AGENT_PLATFORM/26_AGENT_TENANT_ISOLATION.md`
- `../03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md`
- `../04_VOICE_PLATFORM/10_VOICE_SECURITY.md`
- `../05_KNOWLEDGE_PLATFORM/01_KNOWLEDGE_PLATFORM_ARCHITECTURE.md`
- `../08_DATA_PLATFORM/README.md`
- `../09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `LIVEKIT_LOCAL_SANDBOX_EVALUATION_RECORD.md`
