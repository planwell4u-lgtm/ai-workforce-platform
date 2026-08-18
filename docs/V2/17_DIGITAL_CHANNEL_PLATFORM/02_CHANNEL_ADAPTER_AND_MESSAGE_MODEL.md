# 02_CHANNEL_ADAPTER_AND_MESSAGE_MODEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Digital Channel Platform Owner  
**Phase:** Platform Architecture  

---

# Purpose

This document defines the provider-neutral adapter and message boundary for Digital Channel Platform. It converts validated channel-native traffic into approved Conversation Platform interaction contracts and converts authorized outbound delivery intent into channel-native messages and receipts.

The adapter owns translation, validation, capability declaration, consent evidence, address handling, idempotency, and delivery normalization. It does not own canonical participants, conversations, sessions, routing, Agent reasoning, authorization policy, or external business effects.

---

# Adapter Contract

Each adapter declares a stable channel profile containing provider identity, channel type, supported message/media/control capabilities, consent requirements, delivery dispositions, retry/idempotency behavior, limits, and deprecation lifecycle.

An adapter implements four bounded operations:

| Operation | Input | Output |
|---|---|---|
| Inbound normalization | Authenticated provider payload | Validated normalized interaction request or safe rejection/quarantine disposition |
| Outbound adaptation | Authorized Conversation delivery intent | Provider-native request and normalized attempt reference |
| Receipt normalization | Verified provider callback or status poll | Normalized delivery disposition/evidence |
| Capability discovery | Approved tenant/channel configuration | Versioned capability declaration, never an authorization decision |

---

# Normalized Interaction Envelope

An inbound interaction contains only approved, minimum fields:

- stable interaction and correlation identifiers;
- trusted tenant, channel, provider, adapter-version, and environment references;
- provider message/thread/address references as untrusted edge evidence;
- normalized sender/recipient direction, timestamp, content/media references, language/format hints, and channel capabilities;
- consent/opt-out and identity-assurance evidence where applicable;
- classification, integrity, replay/idempotency, and validation disposition;
- provenance sufficient for audit without preserving raw credentials or unnecessary payload data.

Conversation Platform resolves canonical participants, conversations, sessions, routing, and context after receiving this envelope. No adapter field is canonical conversation authority by itself.

---

# Outbound Delivery Envelope

Conversation Platform provides a bounded, authorized delivery intent. Digital Channel validates tenant/channel capability, applicable consent, recipient constraints, template/format requirements, idempotency, and safety restrictions before adaptation.

The adapter returns a normalized disposition:

| Disposition | Meaning |
|---|---|
| Rejected | Delivery was not attempted; no safe send authorization or channel capability existed. |
| Accepted or queued | Provider accepted the attempt; participant delivery remains unconfirmed. |
| Sent | Adapter submitted to the provider; participant delivery remains unconfirmed. |
| Delivered | Verified provider evidence indicates delivery under the provider's definition. |
| Failed | The attempt failed with a normalized safe reason. |
| Unknown / reconciliation pending | The outcome cannot safely be determined; no automatic duplicate attempt is allowed. |
| Suppressed | Consent, opt-out, policy, safety, or lifecycle rules prevented delivery. |

---

# Validation and Safety Rules

- Verify provider authenticity, signature, replay protection, payload bounds, and adapter configuration before normalizing inbound traffic or receipts.
- Resolve tenant and channel eligibility through trusted server-side contracts; never accept a provider account, sender address, client claim, or request header as tenant authority.
- Treat inbound text, attachments, URLs, metadata, receipts, and callbacks as untrusted content, not instructions or authorization.
- Apply consent, opt-out, template, rate, quiet-hour, classification, and recipient restrictions before outbound delivery.
- Use stable idempotency and correlation references across retries, callbacks, reconciliation, and participant-visible status.
- Minimize raw payload retention and redact sensitive addresses/content from logs, telemetry, diagnostics, and exports.

---

# Failure and Recovery

Adapters must distinguish validation rejection, provider rejection, retryable transport failure, permanent failure, duplicate callback, late receipt, and unknown outcome. Retry policy is channel- and provider-specific but must be bounded, idempotent, observable, and prohibited when the outcome is unknown until reconciliation completes.

Provider outages or unsupported capabilities degrade to an approved channel-independent fallback or a safe non-delivery disposition. The adapter must never invent a delivery receipt, create a parallel conversation, or use a different recipient/channel without new authorization and consent evaluation.

---

# Validation Evidence

Tests prove provider signature validation, tenant isolation, normalization compatibility, idempotency, ordering/replay safety, consent enforcement, outbound adaptation, receipt normalization, redaction, and unknown-outcome reconciliation for each adapter profile.

---

# Authoritative References

- `17_DIGITAL_CHANNEL_PLATFORM/01_DIGITAL_CHANNEL_ARCHITECTURE.md`
- `03_CONVERSATION_PLATFORM/03_CONVERSATION_MODEL.md`
- `03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `03_CONVERSATION_PLATFORM/07_CONVERSATION_EVENTS.md`
- `07_INTEGRATION_PLATFORM/03_TOOL_AND_CONNECTOR_REGISTRY.md`
- `07_INTEGRATION_PLATFORM/09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `09_SECURITY_PLATFORM/07_PROVIDER_AND_SUPPLY_CHAIN_SECURITY.md`
- `16_PLATFORM_FOUNDATION/03_CONFIGURATION_AND_ENTITLEMENT_MODEL.md`
