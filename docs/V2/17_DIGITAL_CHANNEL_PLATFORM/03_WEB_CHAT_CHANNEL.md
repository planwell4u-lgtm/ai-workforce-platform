# 03_WEB_CHAT_CHANNEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Digital Channel Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines the web-chat transport boundary. It covers browser/widget connection, channel-native identity evidence, message delivery, reconnect behavior, and safe recovery. Conversation Platform remains the canonical owner of conversations, sessions, participants, routing, and continuity; Frontend Platform owns interface composition and presentation.

# Boundary and Flow

The web client obtains a short-lived, purpose-bound channel credential through approved server-side identity and authorization controls. The adapter validates it, applies tenant/channel eligibility and consent rules, then normalizes inbound traffic into the Conversation interaction contract. A browser conversation key, socket identifier, or client storage value is never canonical identity or conversation authority.

Outbound work arrives only as an authorized Conversation delivery intent. The adapter applies channel capability, recipient, idempotency, and content-safety checks before delivery and returns a normalized acknowledgement or disposition.

# Required Controls

- Bind browser access to an approved tenant, participant assurance level, channel configuration, expiry, and revocation path.
- Treat browser payloads, attachments, URLs, metadata, and claimed conversation identifiers as untrusted.
- Prevent replay, cross-tenant access, duplicate sends, cross-origin misuse, script injection, attachment abuse, and reconnect races.
- Resume through Conversation-approved association and cursors; do not reconstruct or mutate canonical state from client cache.
- Preserve ordered participant-visible delivery where the channel guarantees it; explicitly surface delayed or unknown delivery.
- Support a safe unavailable state and approved handoff/fallback path without silently changing channel or recipient.

# Evidence

Release evidence includes expired/revoked credential rejection, tenant-isolation tests, reconnect and concurrent-tab behavior, duplicate-submit prevention, content/media validation, canonical Conversation association, opt-out handling, delivery disposition reconciliation, and accessible safe-error behavior.

# References

- `01_DIGITAL_CHANNEL_ARCHITECTURE.md`
- `02_CHANNEL_ADAPTER_AND_MESSAGE_MODEL.md`
- `03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md`
- `03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `10_FRONTEND_PLATFORM/README.md`
- `09_SECURITY_PLATFORM/02_IDENTITY_AND_AUTHENTICATION_ARCHITECTURE.md`
