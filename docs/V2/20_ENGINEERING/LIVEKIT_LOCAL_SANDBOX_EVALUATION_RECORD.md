# LiveKit Local Sandbox Evaluation Record

**Status:** Active local evaluation  
**Date:** 2026-08-18

## Decision

Evaluate LiveKit as the first realtime-media provider in an isolated local
Docker sandbox. The existing provider-neutral Voice contracts and canonical
Conversation ownership remain unchanged.

## Local Evidence

- Container: `ai-workforce-livekit-sandbox`
- Image digest: `livekit/livekit-server@sha256:3497163e15c48fef6e7830c78716f9e9d5edc28abf7aa90b61c86e93bbc306b1`
- Mode: LiveKit development mode, using its documented development-only
  credentials.
- Local signaling endpoint: `ws://localhost:7880`
- Local media TCP endpoint: `localhost:7881`
- Both endpoints were reachable on 2026-08-18.

## Scope and Boundaries

- This sandbox evaluates local realtime-media connection and provider-adapter
  behavior only.
- It does not use a LiveKit Cloud account, publish a cloud deployment, contact
  participants, record media, or introduce production credentials.
- LiveKit rooms, participants, tracks, and provider identifiers do not replace
  canonical Conversation, tenant, identity, authorization, or turn ownership.
- Twilio PSTN/SIP, phone numbers, messaging, and any external telephony effect
  remain out of scope until separately approved.

## Completed Evaluation Step

The test-only provider adapter connects to this local sandbox through the
existing Voice boundary and proves connection/disconnection evidence does not
create a competing or falsely successful Conversation turn. The backend image
also builds with the LiveKit dependency and Voice package included.

## Next Evaluation Step

Evaluate a browser media client and synthetic local audio track through the
same provider-neutral Voice boundary. Do not add recording, external
participants, Twilio, or cloud resources without a separate approved decision.
