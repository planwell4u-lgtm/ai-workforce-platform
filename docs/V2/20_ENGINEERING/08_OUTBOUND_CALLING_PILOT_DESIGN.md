# Outbound Calling Pilot Design

**Status:** Guard implemented and tested; no calls or provider requests made  
**Date:** 2026-08-24

## Purpose

Define one controlled outbound-call pilot after Customer Support Worker V1
acceptance. The pilot proves call initiation and status handling only. It is
not a campaign, a sales dialer, or an autonomous customer-contact capability.

## Strict Scope

- One owner-designated recipient, verified in Twilio while the account remains
  on trial.
- One owner-designated outbound-capable Twilio number.
- One manually approved call at a time, during 08:00–21:00 in the recipient's
  local time.
- Static, reviewed greeting only: “Hello. This is a Planwell outbound pilot
  test. No action is required. Goodbye.”
- Record only the provider call reference and terminal status for the pilot
  evidence; do not store audio, transcripts, phone numbers, or message text.
- Terminal states are `completed`, `busy`, `no-answer`, and `failed`. No
  automatic retry is permitted.

## Excluded

- Campaigns, bulk dialing, customer lists, CRM/account/order access, payment
  handling, voicemail drops, AI conversation, AMD, recording, transcription,
  SMS/email follow-up, transfers, and local or Cloud-agent connection.
- Elastic SIP Trunking and LiveKit are not part of the first outbound pilot.
- No deployment, number purchase, credential creation, or source-code change
  is authorized by this design alone.

## Required Gates Before Any Call

1. The owner supplies and confirms the recipient number, recipient local time,
   and explicit consent for this single test.
2. The recipient is verified in Twilio if the account is still a trial.
3. The owner confirms the exact source number and greeting.
4. The owner gives action-time approval immediately before the API request.

## Acceptance Evidence

- The owner receives the disclosed pilot greeting or confirms a terminal
  no-answer/busy/failed status.
- The provider call reference and terminal status are recorded without a phone
  number or audio.
- No recording, retry, follow-up, agent handoff, or customer-data access is
  observed.

## Next Action

Collect the four required gates, then implement a disabled-by-default,
single-call pilot request. A call is never placed merely by opening the app or
running tests.

## Implementation Record

The pilot guard now validates the approved recipient and caller, exact greeting,
consent, trial-recipient verification, recipient-local quiet hours, and a
separate final-approval flag before a provider client can be called. It has no
recording, AMD, voicemail, retry, callback, agent, or data-access path. Focused
safety tests and the complete Python suite passed (70 tests; 3
environment-dependent skips). No provider request was made.

The owner then configured the dedicated Twilio Account SID, API Key SID, and
API Key Secret in local ignored configuration. The pilot client uses those API
key credentials rather than the Account Auth Token. Values were neither
displayed nor used against Twilio; the complete Python suite passed (71 tests;
3 environment-dependent skips).

One owner-confirmed provider request was then attempted within the approved
recipient-local window. Twilio returned HTTP 401 before it issued a call
reference, so no call was created or delivered. The Account SID and API Key
SID had valid identifier formats; correct the local API Key Secret/account
pairing before a new request. A fresh final approval is required for any retry.

After the credential was corrected and the owner again approved at action time,
Twilio accepted one outbound pilot request with initial status `queued` and
provider call reference `CA76b29e7fcca3da88ba7d7091a724f075`. The request
contained only the static disclosed greeting and did not request recording,
voicemail, AMD, AI conversation, retry, or follow-up.

The owner then created a TwiML Bin containing that same static greeting. Its
HTTPS handler URL is local ignored configuration, and the client validates that
it is a Twilio TwiML Bin URL before requesting a call. With fresh action-time
approval, Twilio accepted a second request with provider call reference
`CA5c9b8ea3dda66a956957bd9db9af7505`. Its terminal status was `completed`
after 17 seconds with no provider error. The trial account's mandatory notice
plays before the configured TwiML; no recording, voicemail, AMD, AI
conversation, retry, or follow-up was requested.
