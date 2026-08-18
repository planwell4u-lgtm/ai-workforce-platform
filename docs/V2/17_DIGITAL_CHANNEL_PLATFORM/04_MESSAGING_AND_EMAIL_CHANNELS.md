# 04_MESSAGING_AND_EMAIL_CHANNELS

**Version:** 1.1  
**Status:** Approved  
**Owner:** Digital Channel Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines provider-facing boundaries for messaging and email. It governs sender/recipient address handling, verified provider callbacks, consent and opt-out evidence, templates, attachment constraints, and normalized delivery outcomes. It does not make agent decisions, own canonical conversation state, or implement generic credentials/connectors.

# Channel Rules

- Each provider profile declares its supported media, templates, consent requirements, rate and quiet-hour limits, status semantics, idempotency characteristics, and deprecation policy.
- Outbound delivery requires an authorized Conversation intent plus an active, tenant-scoped channel configuration and current recipient eligibility; an earlier consent record is not a permanent authorization.
- Inbound provider webhooks are authenticated, replay-protected, schema-limited, and normalized before content can reach Conversation.
- Sender and recipient addresses are protected edge data. They are not agent instructions, authorization facts, or canonical participant records.
- Opt-out, suppression, unsubscribe, and invalid-recipient signals take precedence over queued or retrying delivery unless a lawful, approved exception contract applies.
- A provider acceptance, message sent state, delivery receipt, read receipt, bounce, or complaint is represented distinctly; no state is overstated.

# Templates and Attachments

Provider-mandated templates, approved sender identities, localization rules, and attachment capabilities are adapter configuration and policy inputs. Templates cannot introduce unreviewed instructions, bypass approval, or change the recipient/channel. Attachments and links require content and malware controls defined by the responsible security and data contracts.

# Recovery and Evidence

Unknown outcomes enter reconciliation before any repeat send. Tests cover signature verification, replay, consent changes, suppression, template mismatch, duplicate receipts, partial provider outage, recipient ambiguity, and receipt-to-canonical-conversation correlation.

# References

- `01_DIGITAL_CHANNEL_ARCHITECTURE.md`
- `02_CHANNEL_ADAPTER_AND_MESSAGE_MODEL.md`
- `06_CHANNEL_DELIVERY_RELIABILITY.md`
- `07_CHANNEL_SECURITY_AND_PRIVACY.md`
- `09_SECURITY_PLATFORM/07_PROVIDER_AND_SUPPLY_CHAIN_SECURITY.md`
