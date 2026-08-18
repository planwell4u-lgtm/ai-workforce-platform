# Integration Schema

**Document ID:** DB-INTEGRATION-014  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for external integrations in the AI Voice Agent SaaS platform.

The integration domain manages connections between the platform and external systems.

Examples:

- CRM systems
- Calendar platforms
- Payment providers
- Messaging systems
- Business applications
- Webhook endpoints
- Custom APIs

The integration layer allows AI agents to securely interact with external services.

---

# 2. Integration Architecture

High-level model:

             Tenant

                |

         Integration Config

                |

      Credential Management

                |

      Integration Provider

                |

    External Application/API

                |

         Agent Runtime

---

# 3. Integration Design Principles

## 3.1 Provider Agnostic

The architecture supports multiple providers.

Examples:


Salesforce

HubSpot

Google Calendar

Microsoft Outlook

Stripe

Custom REST API


---

## 3.2 Secure Credential Handling

Sensitive credentials must:

- Never be stored in plaintext
- Use secret management systems
- Support rotation
- Support revocation

---

## 3.3 Tenant Isolation

Every integration belongs to a tenant.

Required:

```sql
tenant_id UUID NOT NULL
4. Integration Schema

Schema:

integration
5. Integration Tables Overview
integration.providers

integration.connections

integration.credentials

integration.actions

integration.webhooks

integration.events

integration.sync_jobs

integration.sync_logs

6. Integration Providers

Table:

integration.providers

Purpose:

Stores supported external services.

Examples:

Google Calendar

Salesforce

HubSpot

Stripe

Twilio


Structure:

CREATE TABLE integration.providers
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,

    provider_type TEXT NOT NULL,

    version TEXT,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Provider Types

Supported:

Type	Examples
CRM	Salesforce, HubSpot
Calendar	Google Calendar
Communication	Email, SMS
Payment	Stripe
Database	PostgreSQL
Custom	REST APIs
8. Integration Connections

Table:

integration.connections

Purpose:

Represents a tenant's connected external service.

Example:

Acme Company

      |

Google Calendar Connection


Structure:

CREATE TABLE integration.connections
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    provider_id UUID NOT NULL,

    name TEXT NOT NULL,

    status TEXT DEFAULT 'active',

    configuration JSONB,

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
9. Connection Lifecycle
Created

 |

Authentication Pending

 |

Connected

 |

Active

 |

Suspended

 |

Disconnected

10. Credential Storage

Table:

integration.credentials

Purpose:

Stores references to external secrets.

Important:

Actual secrets are stored in:

Hashicorp Vault
AWS Secrets Manager
Google Secret Manager
Kubernetes Secrets

Structure:

CREATE TABLE integration.credentials
(
id UUID PRIMARY KEY,

connection_id UUID NOT NULL,

secret_reference TEXT NOT NULL,

credential_type TEXT NOT NULL,

expires_at TIMESTAMPTZ,

created_at TIMESTAMPTZ DEFAULT now()
);
11. Credential Types

Examples:

oauth2

api_key

bearer_token

basic_auth

service_account

12. Integration Actions

Table:

integration.actions

Purpose:

Defines operations available to AI agents.

Examples:

Create Calendar Event

Search Customer

Create Ticket

Send Email

Process Payment


Structure:

CREATE TABLE integration.actions
(
id UUID PRIMARY KEY,

provider_id UUID NOT NULL,

action_name TEXT NOT NULL,

schema_definition JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
13. Agent Tool Integration

Relationship:

Agent

 |

Tool

 |

Integration Action

 |

External API


Example:

AI Agent

    |

Book Appointment Tool

    |

Google Calendar API

14. Webhook Management

Table:

integration.webhooks

Purpose:

Stores inbound and outbound webhook configurations.

Examples:

Inbound:

Stripe Payment Event

CRM Update Event


Outbound:

Conversation Completed

Lead Created


Structure:

CREATE TABLE integration.webhooks
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

connection_id UUID,

endpoint TEXT,

event_type TEXT,

status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
15. Integration Events

Table:

integration.events

Purpose:

Stores integration activity.

Examples:

API Request Sent

Webhook Received

Sync Completed

Authentication Failed


Structure:

CREATE TABLE integration.events
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

connection_id UUID,

event_type TEXT,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Synchronization Jobs

Table:

integration.sync_jobs

Purpose:

Tracks background synchronization.

Examples:

Sync CRM Contacts

Sync Calendar Events

Import Knowledge Documents


Structure:

CREATE TABLE integration.sync_jobs
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

connection_id UUID NOT NULL,

job_type TEXT,

status TEXT,

started_at TIMESTAMPTZ,

completed_at TIMESTAMPTZ
);
17. Sync Lifecycle
Queued

 |

Running

 |

Completed

 |

Failed

 |

Retry

18. Sync Logs

Table:

integration.sync_logs

Purpose:

Detailed synchronization history.

Stores:

Records processed
Errors
API responses
Retry information
19. Integration Runtime Flow

Example:

AI booking request:

Customer

 |

AI Agent

 |

Tool Call

 |

Integration Action

 |

Calendar API

 |

Result

 |

Agent Response

20. Integration Security

Required:

OAuth token encryption
Secret rotation
Permission validation
API rate limiting
Audit logging
21. Multi-Tenant Requirements

Tenant-owned tables:

integration.connections

integration.credentials

integration.webhooks

integration.events

integration.sync_jobs


Require:

tenant_id UUID NOT NULL
22. Performance Requirements

High-volume tables:

Table	Growth
events	Very High
sync_logs	High
webhook_events	High
23. Index Requirements

Tenant lookup:

CREATE INDEX idx_integration_tenant
ON integration.connections(tenant_id);

Provider lookup:

CREATE INDEX idx_connection_provider
ON integration.connections(provider_id);

Event search:

CREATE INDEX idx_integration_events
ON integration.events(connection_id);
24. Error Handling

Integration failures must track:

Error Type

Error Message

Provider Response

Retry Count

Last Attempt

Resolution Status

25. Future Extensions

Possible additions:

integration.marketplace

integration.custom_connectors

integration.rate_limits

integration.api_usage

integration.workflow_triggers

integration.event_subscriptions

26. Related Documents

Next:

15_BILLING_SCHEMA.md

16_ANALYTICS_SCHEMA.md

17_AUDIT_SCHEMA.md
End of Document