# Notification Schema

**Document ID:** DB-NOTIFICATION-019  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the notification and communication delivery system used by the AI Voice Agent SaaS platform.

The notification subsystem manages communication between the platform, tenants, users, customers, and external messaging providers.

The system supports:

- Email notifications
- SMS notifications
- Voice notifications
- Push notifications
- In-app notifications
- Webhook notifications
- Notification templates
- Delivery tracking
- Retry handling

---

# 2. Notification Architecture

High-level model:

             System Event

                  |

         Notification Service

                  |

      Notification Processing

                  |

    +-------------+-------------+

    |             |             |

  Email          SMS          Push

    |             |             |

Providers Providers Mobile Apps

                  |

          Delivery Tracking

---

# 3. Notification Design Principles

## 3.1 Event Driven

Notifications are generated from platform events.

Examples:


Call Completed

Appointment Created

Payment Failed

Agent Escalation

Password Reset


---

## 3.2 Provider Independent

The system supports multiple providers.

Examples:

- SMTP
- SendGrid
- Twilio
- AWS SNS
- Firebase
- Custom providers

---

## 3.3 Reliable Delivery

The system provides:

- Retry mechanisms
- Failure tracking
- Delivery status
- Provider fallback

---

# 4. Notification Schema

Schema:


notification


---

# 5. Notification Tables Overview


notification.templates

notification.channels

notification.notifications

notification.recipients

notification.deliveries

notification.provider_configs

notification.events

notification.preferences

notification.retry_queue


---

# 6. Notification Templates

Table:


notification.templates


Purpose:

Stores reusable notification content.

Examples:


Appointment Confirmation

Payment Receipt

Password Reset

Call Summary


---

Structure:

```sql
CREATE TABLE notification.templates
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID,

    name TEXT NOT NULL,

    channel TEXT NOT NULL,

    subject TEXT,

    content TEXT,

    variables JSONB,

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Notification Channels

Supported channels:

Channel	Purpose
email	Email messages
sms	Text messages
voice	Voice calls
push	Mobile notifications
webhook	External events
in_app	Application alerts
8. Notifications

Table:

notification.notifications

Purpose:

Main notification records.

Structure:

CREATE TABLE notification.notifications
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

template_id UUID,

event_type TEXT,

status TEXT,

priority TEXT DEFAULT 'normal',

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Notification Lifecycle
Created

   |

Queued

   |

Processing

   |

Sent

   |

Delivered

   |

Failed

10. Notification Recipients

Table:

notification.recipients

Purpose:

Stores notification targets.

Structure:

CREATE TABLE notification.recipients
(
id UUID PRIMARY KEY,

notification_id UUID NOT NULL,

user_id UUID,

destination TEXT,

recipient_type TEXT
);
11. Delivery Tracking

Table:

notification.deliveries

Purpose:

Tracks provider delivery status.

Example:

SMS Sent

      |

Twilio Accepted

      |

Delivered


Structure:

CREATE TABLE notification.deliveries
(
id UUID PRIMARY KEY,

notification_id UUID NOT NULL,

provider TEXT,

provider_message_id TEXT,

status TEXT,

response JSONB,

sent_at TIMESTAMPTZ,

delivered_at TIMESTAMPTZ
);
12. Delivery Status

Supported:

queued

processing

sent

delivered

failed

bounced

expired

13. Provider Configuration

Table:

notification.provider_configs

Purpose:

Stores provider connection information.

Sensitive credentials should reference:

Secret Manager
Vault
Cloud Secrets

Structure:

CREATE TABLE notification.provider_configs
(
id UUID PRIMARY KEY,

tenant_id UUID,

provider TEXT,

configuration JSONB,

status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Notification Events

Table:

notification.events

Purpose:

Stores triggering events.

Examples:

CALL_COMPLETED

PAYMENT_SUCCESS

USER_CREATED

WORKFLOW_COMPLETED


Structure:

CREATE TABLE notification.events
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

event_type TEXT,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
15. User Notification Preferences

Table:

notification.preferences

Purpose:

Controls user communication preferences.

Examples:

Receive SMS alerts

Receive email reports

Disable marketing messages


Structure:

CREATE TABLE notification.preferences
(
id UUID PRIMARY KEY,

user_id UUID NOT NULL,

channel TEXT,

enabled BOOLEAN DEFAULT true,

updated_at TIMESTAMPTZ DEFAULT now()
);
16. Retry Queue

Table:

notification.retry_queue

Purpose:

Handles failed deliveries.

Structure:

CREATE TABLE notification.retry_queue
(
id UUID PRIMARY KEY,

delivery_id UUID NOT NULL,

attempt_count INTEGER DEFAULT 0,

next_retry_at TIMESTAMPTZ,

status TEXT
);
17. Voice Agent Integration

Example:

Customer Call Completed

        |

Generate Call Summary

        |

Notification Event

        |

Send Email/SMS

        |

Track Delivery

18. Workflow Integration

Example:

Workflow Step

      |

Send Notification Action

      |

Notification Service

      |

Provider

19. Multi-Tenant Requirements

Tenant-owned tables:

notification.notifications

notification.events

notification.templates

notification.provider_configs


Require:

tenant_id UUID NOT NULL
20. Performance Requirements

High-volume tables:

Table	Growth
notifications	Very High
deliveries	Very High
events	High
retry_queue	Medium
21. Index Requirements

Tenant lookup:

CREATE INDEX idx_notification_tenant

ON notification.notifications(tenant_id);

Delivery lookup:

CREATE INDEX idx_delivery_notification

ON notification.deliveries(notification_id);

Retry processing:

CREATE INDEX idx_retry_queue

ON notification.retry_queue(status,next_retry_at);
22. Security Requirements

Required:

Provider credential protection
Message privacy
Tenant isolation
Delivery audit history
Access control
23. Future Extensions

Possible additions:

notification.ai_generated_messages

notification.notification_rules

notification.sms_templates

notification.email_campaigns

notification.communication_preferences

notification.delivery_analytics

24. Related Documents

Previous:

18_AUDIT_SCHEMA.md

Next:

20_SEARCH_SCHEMA.md

21_CONFIGURATION_SCHEMA.md
End of Document