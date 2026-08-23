# Inbound Telephone Integration

**Status:** Local admission implementation complete; controlled dispatch test did not reach the worker and the pilot route was restored
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

## Minimal Media Subscription

The owner approved a narrowly scoped LiveKit `AgentSession` for the local
telephone worker. It subscribes transiently to caller audio so LiveKit can
answer an inbound SIP call. It configures no STT, VAD, LLM, TTS, recording,
transcription, data access, action, storage, or generated response.

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
- The separate LiveKit Agents entrypoint starts the owner-approved model-free
  `AgentSession`, connects to the room, waits for a SIP participant, derives a
  provider call reference from SIP attributes, and invokes the local worker
  harness. Its default agent name is distinct from the active pilot dispatch.
- The local worker registered under the separate `planwell-inbound-local`
  agent name with a test-only tenant route. Empty-room dispatch confirmed the
  session starts successfully. The LiveKit Phone Number/SIP test also delivered
  a SIP participant, but the managed-phone participant omitted the required
  called-number attribute, so B11 correctly failed closed. The diagnostic
  worker was stopped and the known-good pilot dispatch was immediately restored.

Focused tests: `tests.voice.test_telephony` and `tests.voice.test_adapter`.

## Next Implementation Slice

Choose and approve a trusted route-binding design for LiveKit-managed Phone
Numbers that omit the called-number attribute before another real-call test.
The minimal media session is verified; it must not retrieve application data.
Any subsequent FAQ context for a
telephone call requires a separate extension of
`05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`.

## References

- `../../04_VOICE_PLATFORM/10_VOICE_SECURITY.md`
- `../../03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md`
- `05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`
- `../../../packages/voice/python/src/ai_workforce_voice/telephony.py`
