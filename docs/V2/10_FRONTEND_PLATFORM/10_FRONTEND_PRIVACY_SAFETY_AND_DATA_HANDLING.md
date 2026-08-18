# 10_FRONTEND_PRIVACY_SAFETY_AND_DATA_HANDLING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Frontend Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines privacy-, safety-, and classification-aware frontend presentation. Security and Data Platforms own policy, classification, access, retention, deletion, residency, audit, and incident controls; domain platforms own the meaning and lifecycle of their records. Frontend applies approved display, minimization, notice, redaction, and request patterns.

# Data-Handling Rules

- Request and display only the minimum information needed for the approved user task and current tenant/role/purpose.
- Treat all rendered data—participant content, agent output, provider metadata, knowledge, memory, attachments, records, and errors—as potentially sensitive and untrusted for presentation.
- Do not place protected data in URLs, browser history, local storage, client logs, analytics, crash reports, screenshots, clipboard, exports, support tooling, or third-party scripts unless an approved, purpose-limited contract permits it.
- Use backend-provided classification, masking, consent, retention, and access outcomes. The client may render them but cannot downgrade, override, or infer them.
- Clear or revalidate protected client state on session/tenant/purpose change, access revocation, expiry, logout, and retention/deletion notification.

# Display and Reveal

Sensitive fields use approved masking/redaction and explicit reveal behavior where permitted. A reveal request is server-authorized, purpose-limited, audited, and expiry-aware. The UI makes classification, availability, and redaction understandable without revealing protected policy/internal evidence.

Attachments, links, rich content, and provider/agent-generated text are safely rendered, scanned/classified through owner contracts where required, and never treated as instructions, trusted markup, or authorization evidence.

# Consent, Notice, and Preferences

The UI presents required notices, consent choices, privacy preferences, recording/transcript notices, and opt-out effects returned by the owning contracts. It records a user request only through the authorized backend path and shows the resulting authoritative state. A checked box, preference widget, or local setting is not proof that consent or delivery eligibility changed.

# Export, Support, and Sharing

Download, export, copy, print, share, support, and administrative evidence views are separate high-risk actions. They require current server authorization, tenant/purpose/classification checks, bounded scope, audit outcome, and approved retention/recipient controls. The frontend must not implement a broad data dump, hidden bulk export, or unrestricted diagnostic view.

# Required Evidence

Provide data-flow and browser-storage review, tenant/scope redaction tests, session/revocation clearance tests, safe rich-content and attachment rendering tests, consent/notice/outcome mapping tests, export/support authorization negatives, analytics/crash-report minimization checks, and accessibility evidence for masked/revealed/sensitive-state presentation.

# Related Documents

- `01_FRONTEND_PLATFORM_ARCHITECTURE.md`
- `05_FRONTEND_IDENTITY_SESSION_AND_CLIENT_SECURITY.md`
- `07_FRONTEND_CONVERSATION_AGENT_AND_CHANNEL_EXPERIENCE.md`
- `09_SECURITY_PLATFORM/08_TENANT_ISOLATION_AND_DATA_PROTECTION.md`
- `09_SECURITY_PLATFORM/09_SECURITY_EVENTS_AUDIT_AND_COMPLIANCE.md`
- `08_DATA_PLATFORM/06_DATA_LIFECYCLE_RETENTION_DELETION_AND_HOLD.md`
- `17_DIGITAL_CHANNEL_PLATFORM/07_CHANNEL_SECURITY_AND_PRIVACY.md`
