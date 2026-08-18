# B3 Implementation Record — Agent with Governed Knowledge and Memory

**Status:** Implemented locally; pending domain-owner review.  
**Date:** 2026-08-10

- One immutable released agent version is selected only for its tenant and an authorized requester.
- The approved local Knowledge source is a tenant-scoped `internal` FAQ; only published excerpts are returned.
- Memory is explicitly limited to service-continuity facts for the same tenant, subject, and session. No profile or long-term memory is used.
- Knowledge and Memory are optional agent capabilities; neither becomes visible if the agent version does not allow it.
- Tests prove tenant isolation, published-only Knowledge, session/subject-bound Memory, version selection, and fail-closed denial.
