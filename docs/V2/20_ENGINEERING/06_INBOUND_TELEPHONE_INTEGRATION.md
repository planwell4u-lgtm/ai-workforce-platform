# Inbound Telephone Integration

**Status:** Implemented locally — LiveKit Agents admission entrypoint, event adapter, and worker harness complete; production routing deferred
**Date:** 2026-08-23  
**Scope:** Tenant-safe admission of an inbound telephone call into canonical Voice and Conversation state

---

## Decision

The first coded telephone boundary is provider-neutral. A telephony worker may
supply only trusted carrier facts: a provider call reference, the configured
called number, and a LiveKit room reference. The Voice boundary maps the
called number to a deployment-configured tenant, creates a canonical
Conversation, and preserves uncertain output on disconnect.

The caller number, audio, transcript, recordings, and support content are not
accepted or persisted by this boundary.

## Implemented Contract

`ai_workforce_voice.telephony.InboundTelephoneAdapter` accepts:

```text
call_ref + called_number + room_ref
  -> configured called-number-to-tenant lookup
  -> canonical Conversation and Voice interaction
```

It denies missing facts and unknown called numbers before opening a
Conversation. Canonical session and conversation references derive from the
provider call reference, not a telephone number. An interrupted or
disconnected output turn remains `uncertain`.

## Explicitly Deferred

- A LiveKit Agents worker, SIP-event validation, and production deployment.
- Adding the new boundary to the active LiveKit dispatch rule.
- Application-data context, FAQ retrieval, transcripts, recordings, caller
  profiles, actions, human transfer, outbound calling, and Twilio.
- Any external telephone routing change beyond the owner-approved pilot rule.

## Local Evidence

- Configured-number admission creates the expected tenant-scoped canonical
  Conversation without including the telephone number in its session scope.
- Unknown called numbers fail closed before opening a Conversation.
- Disconnect keeps an active output turn `uncertain`.
- The LiveKit event adapter admits only SIP participants carrying a valid
  `sip.trunkPhoneNumber`; it ignores caller-number attributes.
- The local worker harness keeps one interaction per LiveKit call reference,
  rejects a reused call reference in another room, and clears an interaction
  with uncertain output on disconnect.
- The separate LiveKit Agents entrypoint waits only for a SIP participant,
  derives a provider call reference from SIP attributes, and invokes the local
  worker harness. Its default agent name is distinct from the active pilot
  dispatch and it starts no model, media, recording, transcript, data, action,
  or outbound-call capability.

Focused tests: `tests.voice.test_telephony` and `tests.voice.test_adapter`.

## Next Implementation Slice

Run a local LiveKit Agents rehearsal with a dedicated, non-pilot dispatch rule
and an explicit test-only tenant mapping. It must not retrieve application data
or modify the active cloud dispatch rule. Any subsequent FAQ context for a
telephone call requires a separate extension of
`05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`.

## References

- `../../04_VOICE_PLATFORM/10_VOICE_SECURITY.md`
- `../../03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md`
- `05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`
- `../../../packages/voice/python/src/ai_workforce_voice/telephony.py`
