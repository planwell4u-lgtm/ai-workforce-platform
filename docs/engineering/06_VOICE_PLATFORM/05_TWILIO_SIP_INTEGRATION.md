# 05 Twilio SIP Integration

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Voice Platform Engineering

---

# 1. Purpose

This document defines the Twilio SIP integration architecture for the Voice Agent SaaS Platform.

Twilio serves as the platform's Public Switched Telephone Network (PSTN) gateway, enabling AI voice agents to receive inbound calls and place outbound calls through standard telephone networks.

This document covers:

- PSTN connectivity
- SIP trunk architecture
- Inbound call routing
- Outbound call initiation
- Authentication
- Security
- Multi-tenant routing
- Failure handling

---

# 2. Objectives

The integration is designed to provide:

- Reliable PSTN connectivity
- Enterprise SIP trunking
- Low-latency call routing
- Secure signaling
- High availability
- Horizontal scalability
- Multi-tenant support

---

# 3. High-Level Architecture

```
             Telephone User

                    │

                    ▼

             PSTN Network

                    │

                    ▼

            Twilio Voice Cloud

                    │

                    ▼

             Elastic SIP Trunk

                    │

                    ▼

          LiveKit SIP Gateway

                    │

                    ▼

             LiveKit Server

                    │

                    ▼

          LiveKit Agent Runtime

                    │

                    ▼

               AI Runtime

                    │

                    ▼

            Backend Services
```

---

# 4. Responsibilities

Twilio is responsible for:

- Telephone numbers
- PSTN connectivity
- SIP signaling
- Call establishment
- Call termination
- Caller ID
- DTMF relay
- Call status callbacks

Twilio is **not** responsible for:

- AI reasoning
- Voice generation
- Agent execution
- Business workflows
- Conversation storage

---

# 5. SIP Trunk Architecture

Each production environment uses one or more Elastic SIP Trunks.

```
Twilio

│

├── SIP Domain

├── Authentication

├── Origination

├── Termination

└── Phone Numbers
```

The SIP trunk securely forwards voice traffic to the LiveKit SIP service.

---

# 6. Inbound Call Flow

```
Customer

↓

PSTN

↓

Twilio Number

↓

Elastic SIP Trunk

↓

LiveKit SIP

↓

Create Room

↓

Assign AI Agent

↓

Start Conversation
```

---

# 7. Outbound Call Flow

```
Campaign

↓

Backend

↓

Call Scheduler

↓

Twilio API

↓

Elastic SIP Trunk

↓

Customer

↓

LiveKit Room

↓

AI Agent
```

---

# 8. Phone Number Management

Phone numbers are managed per tenant.

Each number contains metadata such as:

- Tenant ID
- Default AI agent
- Language
- Business hours
- Routing rules
- Failover configuration

Example:

```
Phone Number

├── Tenant

├── Agent

├── Language

├── Region

├── Time Zone

└── Routing Policy
```

---

# 9. SIP Authentication

Authentication is performed using:

- SIP credentials
- IP allow lists
- TLS (where supported)
- API credentials for management operations

Secrets are stored using the platform's centralized secret management solution.

---

# 10. Call Routing

The backend determines which AI agent should answer a call.

Routing decisions may consider:

- Called number
- Tenant
- Business hours
- Language
- Campaign
- Customer profile
- Skill group
- Availability

---

# 11. LiveKit Integration

Twilio forwards SIP traffic to the LiveKit SIP Gateway.

The gateway:

- Accepts SIP INVITE requests
- Creates LiveKit rooms
- Connects the caller
- Dispatches an AI agent
- Bridges RTP audio

---

# 12. Call Metadata

Metadata accompanies each session.

Typical fields include:

```
Call SID

Call ID

Tenant ID

Phone Number

Caller Number

Direction

Timestamp

Campaign ID

Agent ID
```

Metadata is persisted in PostgreSQL.

---

# 13. DTMF Support

The platform supports DTMF events for:

- IVR navigation
- PIN entry
- Menu selection
- Legacy integrations

DTMF events are forwarded to the AI Runtime when required.

---

# 14. Recording Integration

Call recording follows platform policies.

Flow:

```
Conversation

↓

Recording Service

↓

Supabase Storage

↓

Metadata

↓

PostgreSQL
```

Recording retention follows tenant-specific policies.

---

# 15. Status Callbacks

Twilio sends webhook events for major call lifecycle events.

Examples:

- Call initiated
- Ringing
- Answered
- In progress
- Completed
- Busy
- Failed
- No answer

Backend services use these events to update call state.

---

# 16. Failure Handling

Failure scenarios include:

### SIP Connection Failure

- Retry connection
- Route to backup infrastructure
- Log failure

### LiveKit Unavailable

- Reject new sessions
- Notify monitoring systems

### Backend Unavailable

- Queue events when possible
- Retry webhook delivery

---

# 17. Multi-Tenant Isolation

Each tenant maintains isolated:

- Phone numbers
- SIP routing rules
- AI agents
- Voice settings
- Call records
- Analytics

No tenant can access another tenant's telephony resources.

---

# 18. Security

Security controls include:

- TLS encryption
- Secure SIP credentials
- API authentication
- Tenant isolation
- Audit logging
- Secret rotation
- Access control

---

# 19. Monitoring

Operational metrics include:

- Active calls
- Calls per minute
- Call success rate
- SIP registration status
- Call setup latency
- Average call duration
- Failed call percentage
- Webhook delivery success

---

# 20. Scalability

The architecture supports:

- Multiple SIP trunks
- Geographic redundancy
- High call concurrency
- Horizontal LiveKit scaling
- Multiple AI worker pools

---

# 21. Disaster Recovery

Recovery procedures include:

- Backup SIP routes
- Redundant LiveKit clusters
- Database replication
- Redis high availability
- Automated infrastructure recovery

---

# 22. Design Principles

The Twilio SIP integration follows:

- Standards-based SIP
- Stateless signaling
- Secure communication
- Event-driven processing
- Horizontal scalability
- High availability
- Multi-tenant isolation

---

# 23. Related Documentation

- 02_LIVEKIT_ARCHITECTURE.md
- 03_LIVEKIT_SERVER_DESIGN.md
- 04_LIVEKIT_AGENT_RUNTIME.md
- 06_INBOUND_CALL_ARCHITECTURE.md
- 07_OUTBOUND_CALL_ARCHITECTURE.md
- 09_CALL_SESSION_MANAGEMENT.md
- 19_VOICE_WEBHOOKS.md

---

# 24. Summary

Twilio provides the telephony gateway between the public telephone network and the Voice Agent SaaS Platform.

By combining Twilio Elastic SIP Trunking with LiveKit, the Backend, and the AI Runtime, the platform delivers secure, scalable, and enterprise-grade inbound and outbound voice communications while maintaining complete tenant isolation and seamless integration with AI-driven conversational workflows.