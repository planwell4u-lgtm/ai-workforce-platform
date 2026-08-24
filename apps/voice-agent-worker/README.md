# Local Scripted Voice-Agent Worker

This is a bounded local rehearsal worker. It discovers only explicitly created
`local-agent-...` sandbox rooms, joins once as a separate LiveKit participant,
publishes an offline synthesized greeting, and disconnects.

It is not a production Voice Agent or an AI-model integration: it does not
receive support data, record media, call external services, or use cloud
credentials. Its purpose is to prove the browser can receive audio published by
an independent, programmatic LiveKit participant before model and telephony
work are considered.

## Inbound telephone admission worker

`inbound_telephone_worker.py` is a separate, local LiveKit Agents entrypoint.
It accepts only SIP participants, derives a provider call reference from SIP
attributes, and invokes the tested B11 call-admission boundary. It does not
start a model, publish audio, record, transcribe, retrieve support data, take
actions, place calls, or use the active pilot agent name.

It requires an explicit deployment-only mapping such as:

```text
INBOUND_TELEPHONE_TENANT_MAP_JSON={"+1...":"staging-demo"}
LIVEKIT_TRUSTED_DISPATCH_ROUTE_MAP_JSON={"planwell-native-support-v1":"+1..."}
LIVEKIT_INBOUND_AGENT_NAME=planwell-inbound-local
```

Do not point the active phone dispatch rule at this worker until its local
runtime rehearsal and a separate routing approval are complete.
