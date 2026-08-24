# Inbound Telephone Integration

**Status:** Local admission and isolated LiveKit proof complete; original managed route preserved
**Date:** 2026-08-24
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

- Production deployment of the local worker.
- Co-dispatching the local worker with the active managed support agent.
- Application-data context, FAQ retrieval, transcripts, recordings, caller
  profiles, actions, human transfer, outbound calling, and Twilio.
- Any external telephone routing change beyond the owner-approved pilot rule.

## Admission-Only Worker

The local worker connects to its assigned room only to admit the SIP event. It
does not create an `AgentSession`, subscribe to audio, process turn signals,
record, transcribe, access application data, take actions, or publish a
response. In a shared room, LiveKit broadcasts other participants' data streams
to all participants, so this worker must use an isolated worker-only route.

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
- The separate LiveKit Agents entrypoint connects to the room, waits for a SIP
  participant, derives a provider call reference from SIP attributes, and
  invokes the local worker harness. Its default agent name is distinct from
  the active pilot dispatch.
- Managed LiveKit phone participants can provide an invalid or unusable
  `sip.trunkPhoneNumber`. The adapter then accepts only an exact,
  deployment-configured dispatch-metadata token that maps to a configured
  called-number-to-tenant route. Unknown or missing tokens fail closed.
- A controlled isolated-project call reached the local worker, supplied the
  trusted token, and admitted without error. No managed agent shared that room;
  the worker was stopped immediately after the proof.
- The original managed phone route is restored to its support agent only.
  The worker logs only dispatch-metadata presence/length and SIP attribute
  names, never metadata values, phone numbers, audio, or transcript contents.

Focused tests: `tests.voice.test_livekit_telephony` and
`tests.voice.test_telephone_worker`.

## Next Implementation Slice

The isolated local-worker proof is complete. Keep the worker stopped unless a
new isolated rehearsal is explicitly approved. Do not co-dispatch it with the
managed agent under the strict no-transcript-data boundary. Any subsequent FAQ
context requires a separate extension of
`05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`.

## References

- `../../04_VOICE_PLATFORM/10_VOICE_SECURITY.md`
- `../../03_CONVERSATION_PLATFORM/04_CONVERSATION_SESSION_MODEL.md`
- `05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`
- `../../../packages/voice/python/src/ai_workforce_voice/telephony.py`
