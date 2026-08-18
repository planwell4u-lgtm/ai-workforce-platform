# Local Scripted Voice-Agent Worker

This is a bounded local rehearsal worker. It discovers only explicitly created
`local-agent-...` sandbox rooms, joins once as a separate LiveKit participant,
publishes an offline synthesized greeting, and disconnects.

It is not a production Voice Agent or an AI-model integration: it does not
receive support data, record media, call external services, or use cloud
credentials. Its purpose is to prove the browser can receive audio published by
an independent, programmatic LiveKit participant before model and telephony
work are considered.
