# 08 Call Routing Engine

**Version:** 2.0  
**Status:** Production Architecture  
**Owner:** Voice Platform Engineering

---

# 1. Purpose

This document defines the Call Routing Engine for the Voice Agent SaaS Platform.

The Call Routing Engine is responsible for determining where every incoming or outgoing call should be routed.

Routing decisions consider:

- Tenant
- Phone number
- Business rules
- AI agent configuration
- Customer profile
- Campaign
- Language
- Time zone
- Business hours
- Availability

The routing engine supports both AI-first and human-assisted communication.

---

# 2. Objectives

The routing engine is designed to provide:

- Intelligent call routing
- Multi-tenant isolation
- Dynamic agent selection
- Human escalation
- Geographic routing
- Business-hours routing
- Failover handling
- Horizontal scalability

---

# 3. High-Level Architecture

```
               Incoming Call

                     │

                     ▼

            Call Routing Engine

                     │

     ┌───────────────┼───────────────┐

     ▼               ▼               ▼

 AI Agent       Human Agent      Reject Call

                     │

                     ▼

              LiveKit Session

                     │

                     ▼

               AI Runtime
```

---

# 4. Responsibilities

The routing engine determines:

- Which tenant owns the call
- Which AI agent should answer
- Which workflow should start
- Which language to use
- Which voice model to use
- Whether human escalation is required
- Which outbound campaign owns the call

---

# 5. Routing Inputs

Routing decisions may use:

- Dialed phone number
- Caller number
- Tenant ID
- Campaign ID
- Customer profile
- CRM data
- Business hours
- Time zone
- Preferred language
- Customer history
- Agent availability
- Routing policies

---

# 6. Routing Process

```
Incoming Call

↓

Identify Tenant

↓

Load Routing Policy

↓

Evaluate Rules

↓

Select Destination

↓

Initialize Session

↓

Launch Agent
```

---

# 7. Routing Policies

Each tenant defines one or more routing policies.

Example:

```
Policy

├── Priority

├── Conditions

├── Destination

├── Failover

└── Timeout
```

Policies are evaluated in priority order.

---

# 8. Phone Number Routing

Each phone number maps to a routing configuration.

```
Phone Number

↓

Tenant

↓

Routing Policy

↓

Default Agent
```

Different phone numbers may connect to different departments or AI agents.

---

# 9. AI Agent Selection

Agent selection may consider:

- Department
- Skills
- Language
- Campaign
- Customer segment
- Previous interactions
- Availability
- Load balancing

---

# 10. Language Routing

The engine supports multilingual deployments.

Routing may use:

- Customer preference
- Dialed number
- Geographic region
- Automatic language detection

Example:

```
Spanish

↓

Spanish Agent

↓

Spanish Voice

↓

Spanish Prompt
```

---

# 11. Time-Based Routing

Business rules may vary by time.

Examples:

- Business hours
- Holidays
- Weekends
- Emergency schedules
- After-hours support

---

# 12. Customer-Based Routing

Returning customers may receive personalized routing.

Factors include:

- VIP status
- Account manager
- Previous conversations
- Open support cases
- Subscription tier

---

# 13. Campaign Routing

Outbound calls include campaign context.

Routing determines:

- Assigned AI agent
- Prompt template
- Customer variables
- Workflow
- Retry policy

---

# 14. Human Escalation

Calls may be transferred when:

- Customer requests a human
- AI confidence falls below threshold
- Compliance requires human review
- Emergency detected
- Business rules require escalation

---

# 15. Failover Routing

If the preferred destination is unavailable:

```
Primary Agent

↓

Secondary Agent

↓

Shared Queue

↓

Human Agent

↓

Voicemail
```

---

# 16. Routing Configuration

Example configuration:

```
Routing Profile

├── Tenant

├── Phone Number

├── Default Agent

├── Language

├── Business Hours

├── Failover Rules

├── Transfer Rules

└── Recording Policy
```

---

# 17. Integration Points

The routing engine communicates with:

- Backend Services
- Agent Service
- AI Runtime
- LiveKit
- Twilio
- Memory Service
- RAG Service

---

# 18. Persistence

Routing metadata is stored in PostgreSQL.

Examples:

- Routing profiles
- Policies
- Rule sets
- Call history
- Transfer history

Redis may cache active routing configurations for low-latency lookups.

---

# 19. Events

Examples:

```
ROUTING_STARTED

TENANT_IDENTIFIED

AGENT_SELECTED

CALL_TRANSFERRED

ROUTING_FAILED

ROUTING_COMPLETED
```

---

# 20. Monitoring

Metrics include:

- Routing latency
- Agent utilization
- Transfer rate
- Routing failures
- Business-hours matches
- Failover activations
- Human escalations

---

# 21. Security

Security controls include:

- Tenant isolation
- Policy authorization
- API authentication
- Audit logging
- Configuration validation

---

# 22. Scalability

The routing engine supports:

- Millions of routing decisions
- Stateless execution
- Horizontal scaling
- Cached routing policies
- Distributed processing

---

# 23. Design Principles

The Call Routing Engine follows:

- Configuration over code
- Policy-driven routing
- Event-driven execution
- Stateless services
- Low-latency decisions
- High availability
- Multi-tenant isolation

---

# 24. Related Documentation

- 05_TWILIO_SIP_INTEGRATION.md
- 06_INBOUND_CALL_ARCHITECTURE.md
- 07_OUTBOUND_CALL_ARCHITECTURE.md
- 09_CALL_SESSION_MANAGEMENT.md
- 15_VOICE_AGENT_HANDOFF.md
- 16_HUMAN_TRANSFER_ARCHITECTURE.md

---

# 25. Summary

The Call Routing Engine is the central decision-making component for all voice interactions within the Voice Agent SaaS Platform.

By evaluating tenant configuration, routing policies, customer context, campaign information, language, business rules, and AI agent availability, it ensures that every call reaches the most appropriate destination while maintaining scalability, security, and complete multi-tenant isolation.