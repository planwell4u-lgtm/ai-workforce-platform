# Multi-Tenant Data Model

**Document ID:** DB-MULTI-004  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the multi-tenant data architecture for the AI Voice Agent SaaS platform.

The platform is designed as a Software-as-a-Service (SaaS) system where multiple organizations share the same application infrastructure while maintaining strict data isolation.

The database architecture uses:


Shared PostgreSQL Cluster

Shared Database

Shared Schema

Tenant ID Isolation

Row Level Security


---

# 2. Multi-Tenant Requirements

The platform must support:

- Thousands of customer organizations
- Multiple users per organization
- Multiple AI agents per tenant
- Independent voice configurations
- Separate knowledge bases
- Isolated conversations
- Tenant-specific billing
- Tenant-level analytics

---

# 3. Tenant Isolation Strategy

The selected architecture:

## Shared Database / Shared Schema Model

             PostgreSQL

                  |

    +-------------+-------------+

    |                           |

 Tenant A                    Tenant B

tenant_id = A tenant_id = B

Agents Agents

Calls Calls

Users Users

Knowledge Knowledge


---

# 4. Why Shared Schema Architecture

Advantages:

## Cost Efficient

One database cluster serves many customers.

---

## Easier Operations

Single:

- Backup strategy
- Migration process
- Monitoring system

---

## Scalable

Supports:

- Thousands of tenants
- Automated provisioning
- SaaS growth

---

# 5. Tenant Hierarchy Model

The tenant structure:


Platform

|

Organization

|

Workspace

|

Users

|

Resources


---

# 6. Core Tenant Entities

Main entities:


tenant.organizations

tenant.workspaces

identity.users

identity.memberships


---

# 7. Organization Model

Table:


tenant.organizations


Purpose:

Represents a customer company.

Example:


Acme Plumbing

Healthcare Clinic

Real Estate Agency


---

Example structure:

```sql
CREATE TABLE tenant.organizations
(
    id UUID PRIMARY KEY,

    name TEXT NOT NULL,

    slug TEXT UNIQUE NOT NULL,

    status TEXT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT now()
);
8. Workspace Model

A workspace represents an operational environment.

Examples:

Production Workspace

Testing Workspace

Sales Department

Support Department


Table:

tenant.workspaces

Example:

CREATE TABLE tenant.workspaces
(
    id UUID PRIMARY KEY,

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT now()
);
9. Tenant Ownership Rules

Every business resource must belong to a tenant.

Required:

tenant_id UUID NOT NULL

Examples:

Agents
agent.agents

tenant_id
Calls
voice.call_sessions

tenant_id
Knowledge
knowledge.documents

tenant_id
10. Tenant Context Propagation

Every request must contain tenant context.

Flow:

User Request

      |

Authentication

      |

Resolve Tenant

      |

Set Database Context

      |

Execute Query


Example:

SET app.tenant_id='tenant_uuid';
11. Row Level Security Architecture

All tenant-owned tables use PostgreSQL RLS.

Example:

ALTER TABLE agent.agents
ENABLE ROW LEVEL SECURITY;

Policy:

CREATE POLICY tenant_access_policy
ON agent.agents

USING
(
tenant_id =
current_setting('app.tenant_id')::uuid
);
12. Tenant Data Access Flow
API Request

     |

JWT Token

     |

Tenant Resolver

     |

tenant_id

     |

PostgreSQL Session

     |

RLS Filter

     |

Tenant Data

13. User Membership Model

A user may belong to one or more organizations.

Relationship:

User

 |

Membership

 |

Organization


Tables:

identity.users

identity.memberships

tenant.organizations


Example:

CREATE TABLE identity.memberships
(
id UUID PRIMARY KEY,

user_id UUID NOT NULL,

tenant_id UUID NOT NULL,

role_id UUID NOT NULL

);
14. Tenant Roles

Example roles:

Role	Permissions
Owner	Full access
Admin	Manage resources
Developer	API access
Operator	Daily operations
Viewer	Read only
15. Tenant Resource Ownership

Ownership pattern:

Organization

      |

      +---- Agents

      |

      +---- Phone Numbers

      |

      +---- Conversations

      |

      +---- Knowledge Bases

      |

      +---- Integrations

16. Tenant-Aware API Design

All APIs must include tenant context.

Example:

GET /api/v1/agents

Internally:

SELECT *
FROM agent.agents
WHERE tenant_id = current_tenant;
17. Tenant Data Rules
Rule 1

Never trust client-provided tenant IDs.

Bad:

POST /agents

{
tenant_id:"abc"
}


Correct:

JWT

+

Server-side tenant resolution

Rule 2

Never bypass RLS in application queries.

Rule 3

All background jobs require tenant context.

Example:

Worker

 |

Tenant ID

 |

Database Query

18. Background Processing

AI workloads must preserve tenant boundaries.

Examples:

RAG Processing
Document Upload

 |

Tenant Context

 |

Embedding Worker

 |

Tenant Vector Storage

Call Processing
Incoming Call

 |

Tenant Lookup

 |

Agent Assignment

 |

Conversation Storage

19. Tenant Data Partitioning Strategy

Initial phase:

Single PostgreSQL Cluster


Growth phase:

Partition large tables:

conversation.messages

voice.call_events

knowledge.embeddings


Partition key:

tenant_id

20. Tenant Lifecycle
Creation
Signup

 |

Create Organization

 |

Create Workspace

 |

Create Default Roles

 |

Create Default Settings

Suspension

Actions:

Disable login
Stop API access
Preserve data
Deletion

Process:

Soft Delete

 |

Retention Period

 |

Permanent Removal

21. Tenant Security Controls

Required:

RLS enabled
Tenant-aware logging
API authorization
Encryption
Audit tracking
22. Tenant Performance Considerations

Monitor:

Largest tenants
Query distribution
Storage growth
API usage
Call volume
23. Future Enterprise Isolation

For enterprise customers:

Possible upgrade:

Shared Database

        |

Dedicated Database

        |

Dedicated Infrastructure


Migration path:

Tenant Export

        |

Database Migration

        |

Dedicated Environment

24. Related Documents

Next:

05_CORE_ENTITY_MODEL.md

06_USER_IDENTITY_SCHEMA.md

07_AGENT_SCHEMA.md
End of Document