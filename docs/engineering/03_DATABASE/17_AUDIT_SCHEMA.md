# Audit Schema

**Document ID:** DB-AUDIT-017  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for audit logging, compliance tracking, security monitoring, and change history in the AI Voice Agent SaaS platform.

The audit domain provides complete visibility into:

- User actions
- System changes
- Configuration modifications
- Security events
- Data access
- Administrative operations

The audit system supports:

- Compliance requirements
- Security investigations
- Customer transparency
- Operational debugging

---

# 2. Audit Architecture

High-level model:


User Action

 |

Application Service

 |

Audit Event Generator

 |

Audit Storage

 |

Security Monitoring

 |

Compliance Reports


---

# 3. Audit Design Principles

## 3.1 Immutable Records

Audit records must be:

- Append-only
- Never modified
- Never deleted without policy approval

---

## 3.2 Complete Traceability

Every important action should answer:

- Who performed it?
- What changed?
- When did it happen?
- Where did it originate?
- What was affected?

---

## 3.3 Tenant Isolation

Audit data belongs to tenants.

Required:

```sql
tenant_id UUID NOT NULL
4. Audit Schema

Schema:

audit
5. Audit Tables Overview
audit.events

audit.change_history

audit.login_events

audit.security_events

audit.data_access_logs

audit.api_requests

audit.admin_actions

audit.retention_policies

6. Audit Events

Table:

audit.events

Purpose:

Central audit event store.

Examples:

USER_CREATED

AGENT_UPDATED

CALL_ACCESSED

DOCUMENT_DELETED

BILLING_CHANGED


Structure:

CREATE TABLE audit.events
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    actor_id UUID,

    actor_type TEXT,

    action TEXT NOT NULL,

    resource_type TEXT,

    resource_id UUID,

    metadata JSONB,

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Actor Types

Supported:

user

administrator

service

agent

system

integration
8. Audit Event Lifecycle
Action Occurs

      |

Capture Event

      |

Store Audit Record

      |

Monitor

      |

Report

9. Change History

Table:

audit.change_history

Purpose:

Tracks changes to important entities.

Examples:

Agent Prompt Changed

Billing Plan Updated

User Permission Modified

Knowledge Document Updated


Structure:

CREATE TABLE audit.change_history
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

resource_type TEXT NOT NULL,

resource_id UUID NOT NULL,

old_value JSONB,

new_value JSONB,

changed_by UUID,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Change Tracking Model

Example:

Before:

{
 "voice":"old_voice"
}

After:

{
 "voice":"new_voice"
}
11. Login Audit Events

Table:

audit.login_events

Purpose:

Tracks authentication activity.

Examples:

Successful Login

Failed Login

Password Reset

MFA Challenge

Session Expired


Structure:

CREATE TABLE audit.login_events
(
id UUID PRIMARY KEY,

tenant_id UUID,

user_id UUID,

event_type TEXT,

ip_address TEXT,

user_agent TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Security Events

Table:

audit.security_events

Purpose:

Tracks security-related activities.

Examples:

Suspicious Login

Permission Violation

API Abuse

Credential Rotation


Structure:

CREATE TABLE audit.security_events
(
id UUID PRIMARY KEY,

tenant_id UUID,

severity TEXT,

event_type TEXT,

details JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
13. Data Access Logs

Table:

audit.data_access_logs

Purpose:

Tracks sensitive data access.

Examples:

Customer Transcript Viewed

Recording Downloaded

Invoice Exported

Document Accessed


Structure:

CREATE TABLE audit.data_access_logs
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

actor_id UUID,

resource_type TEXT,

resource_id UUID,

access_type TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
14. API Request Audit

Table:

audit.api_requests

Purpose:

Tracks API activity.

Stored:

Endpoint
Method
User
Response status
Latency
Request ID

Structure:

CREATE TABLE audit.api_requests
(
id UUID PRIMARY KEY,

tenant_id UUID,

request_id TEXT,

endpoint TEXT,

method TEXT,

status_code INTEGER,

latency_ms INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
15. Administrative Actions

Table:

audit.admin_actions

Purpose:

Tracks privileged operations.

Examples:

Tenant Suspension

User Role Change

Billing Override

System Configuration Change


Structure:

CREATE TABLE audit.admin_actions
(
id UUID PRIMARY KEY,

tenant_id UUID,

admin_id UUID,

action TEXT,

reason TEXT,

metadata JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Audit Integration Points

Audit events originate from:

Authentication Service

        |

Agent Service

        |

Voice Service

        |

Knowledge Service

        |

Billing Service

        |

Integration Service

17. Audit Event Example

Example:

User Updated Agent Prompt

Actor:

admin@example.com


Resource:

Agent ABC


Action:

UPDATE_PROMPT


Timestamp:

2026-07-24 10:30 UTC

18. Compliance Support

Supports:

SOC 2
ISO 27001
GDPR audit requirements
Enterprise security reviews
19. Retention Policies

Table:

audit.retention_policies

Purpose:

Controls data lifecycle.

Example:

Security Logs:

7 years


API Logs:

1 year


Debug Logs:

30 days


Structure:

CREATE TABLE audit.retention_policies
(
id UUID PRIMARY KEY,

data_type TEXT,

retention_days INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
20. Performance Requirements

High-volume tables:

Table	Growth
events	Very High
api_requests	Very High
data_access_logs	High
21. Partitioning Strategy

Large tables:

audit.events

audit.api_requests

audit.login_events

Partition by:

created_at
22. Index Requirements

Tenant lookup:

CREATE INDEX idx_audit_tenant
ON audit.events(tenant_id);

Resource lookup:

CREATE INDEX idx_audit_resource
ON audit.events(resource_id);

Time search:

CREATE INDEX idx_audit_time
ON audit.events(created_at);
23. Security Requirements

Required:

Append-only permissions
Restricted access
Encryption at rest
Sensitive data masking
Compliance monitoring
24. Future Extensions

Possible additions:

audit.risk_scores

audit.policy_violations

audit.security_alerts

audit.compliance_reports

audit.user_behavior_analysis

25. Related Documents

Next:

18_NOTIFICATION_SCHEMA.md

19_SEARCH_SCHEMA.md

20_CONFIGURATION_SCHEMA.md
End of Document