# On-Call Operations

## 1. Overview

On-Call Operations defines the responsibilities, processes, and procedures for engineers responsible for maintaining production reliability outside normal development workflows.

The Voice Agent SaaS platform requires reliable on-call coverage because production systems operate continuously across:

* API services
* AI agent runtime
* Voice infrastructure
* Database systems
* Background workers
* Cloud infrastructure
* External integrations

The objective of on-call operations is to ensure:

* Fast incident response
* Clear ownership
* Reliable service recovery
* Effective escalation
* Continuous platform availability

---

# 2. On-Call Objectives

On-call operations focus on:

* Detecting production issues quickly
* Responding to alerts
* Restoring service availability
* Performing initial troubleshooting
* Escalating when required
* Documenting operational knowledge

---

# 3. On-Call Responsibilities

## Primary On-Call Engineer

The primary engineer is responsible for:

* Monitoring alerts
* Acknowledging incidents
* Performing initial investigation
* Coordinating immediate response
* Escalating when necessary

## Secondary On-Call Engineer

The secondary engineer provides:

* Backup support
* Additional technical expertise
* Incident assistance
* Coverage when primary is unavailable

## Service Owner

Responsible for:

* Long-term fixes
* Reliability improvements
* Architecture decisions
* Runbook maintenance

---

# 4. On-Call Coverage Model

The platform follows a rotating coverage model.

Example:

```text
Week 1
Primary Engineer
        |
        v
Secondary Engineer

Week 2
Next Rotation
        |
        v
Updated Ownership
```

Coverage must define:

* Rotation schedule
* Handoff process
* Contact information
* Escalation path

---

# 5. On-Call Readiness

Before accepting on-call responsibility, engineers must understand:

* System architecture
* Monitoring dashboards
* Alert definitions
* Operational runbooks
* Incident procedures
* Escalation policies

Required access:

* Monitoring systems
* Logging systems
* Deployment systems
* Infrastructure tools
* Incident communication channels

---

# 6. Alert Response Process

When an alert triggers:

```text
Alert Received
       |
       v
Acknowledge Alert
       |
       v
Validate Impact
       |
       v
Investigate
       |
       v
Mitigate
       |
       v
Resolve
       |
       v
Document
```

---

# 7. Alert Handling Procedure

## Step 1 — Acknowledge

The engineer should:

* Confirm alert receipt
* Record ownership
* Prevent duplicate response

---

## Step 2 — Validate

Determine:

* Is the alert real?
* What services are affected?
* What customers are impacted?
* What is the severity?

---

## Step 3 — Investigate

Review:

* Logs
* Metrics
* Traces
* Recent changes
* Dependencies

---

## Step 4 — Resolve

Actions may include:

* Restart services
* Roll back deployments
* Adjust configuration
* Scale resources
* Activate failover procedures

---

# 8. On-Call for Voice Platform

Voice incidents require priority handling because they directly affect customer conversations.

Monitor:

* Call connection success
* Call latency
* Audio quality
* SIP failures
* LiveKit availability
* Agent assignment failures

Common actions:

* Verify telephony provider status
* Check media infrastructure
* Review call events
* Restart voice workers
* Escalate provider issues

---

# 9. On-Call for AI Runtime

Monitor:

* Agent availability
* Response latency
* Model failures
* Tool execution errors
* Memory service health
* RAG retrieval failures

Common actions:

* Review runtime logs
* Check model provider status
* Disable faulty configuration
* Restart runtime workers

---

# 10. On-Call for Database Systems

Monitor:

* Connection usage
* Query latency
* Storage capacity
* Backup status
* Replication health

Common actions:

* Identify slow queries
* Review locks
* Check migrations
* Restore service connectivity

---

# 11. Handoff Process

A proper handoff must include:

```text
Current Incidents:

Active Alerts:

Recent Changes:

Known Issues:

Pending Actions:

Important Notes:
```

The incoming engineer must confirm ownership.

---

# 12. Escalation During On-Call

Escalate when:

* Incident severity increases
* Resolution is unclear
* Security impact exists
* Data integrity is affected
* Multiple systems fail

Escalation path:

```text
Primary On-Call
        |
        v
Secondary On-Call
        |
        v
Service Owner
        |
        v
Engineering Leadership
```

---

# 13. On-Call Metrics

Track:

## Response Time

Time between alert creation and acknowledgement.

## Resolution Time

Time required to restore service.

## Alert Quality

Measures:

* False positives
* Missing alerts
* Alert usefulness

## Incident Frequency

Number of incidents handled over time.

---

# 14. Improving On-Call Operations

Continuous improvements include:

* Better alerting
* Improved automation
* Updated runbooks
* Reduced manual recovery steps
* Better system design

---

# 15. Related Documents

* SRE Guidelines
* Incident Management
* Major Incident Response
* Escalation Policy
* Operational Runbooks
* Monitoring Architecture
