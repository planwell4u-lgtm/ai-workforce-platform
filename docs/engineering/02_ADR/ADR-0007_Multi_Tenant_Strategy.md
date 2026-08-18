# ADR-0007: Multi-Tenant Architecture Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Multi-Tenant Architecture Strategy  
**ADR Number:** ADR-0007  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will use a shared infrastructure multi-tenant architecture with strict logical tenant isolation.

The approved strategy is:

| Area | Decision |
|---|---|
| Application architecture | Multi-tenant SaaS platform |
| Database strategy | Shared PostgreSQL database |
| Tenant isolation | tenant_id based isolation + security policies |
| Authentication | Tenant-aware identity management |
| Authorization | Role-based access control |
| Storage isolation | Tenant-scoped object storage paths |
| AI isolation | Tenant-aware agents, memory, and knowledge |
| Voice isolation | Tenant-owned phone numbers and agents |


The platform will support multiple businesses operating independently on the same platform.

---

# 2. Context

The Voice Agent SaaS Platform is designed as a Software-as-a-Service product.

Multiple businesses will use the same platform to create and operate AI voice agents.

Examples:


Medical Clinic

Real Estate Company

Restaurant

Software Company

Home Service Provider


Each customer requires:

- Separate users
- Separate agents
- Separate phone numbers
- Separate knowledge bases
- Separate conversations
- Separate billing
- Separate analytics


The architecture must provide isolation while maintaining operational simplicity.

---

# 3. Problem Statement

The platform must solve:


## Data Isolation

Tenant data must never leak between customers.


Examples:

Tenant A must not access:

- Tenant B agents
- Tenant B calls
- Tenant B documents
- Tenant B customers


---

## Operational Scalability

The system must support:

- Hundreds of tenants
- Thousands of agents
- Millions of calls


---

## Development Simplicity

The early platform must avoid unnecessary infrastructure complexity.

---

## Future Enterprise Requirements

The architecture must allow:

- Enterprise isolation
- Dedicated deployments
- Regional deployments


---

# 4. Multi-Tenant Requirements


The platform requires:


## Tenant Identity

Every resource must belong to a tenant.

Examples:


Agent

Call

Conversation

Document

Memory

User

Integration



---

## Tenant Context Propagation

Every request must carry tenant context.


Example:



User Request

    |

Authentication

    |

Tenant Identification

    |

Authorization

    |

Business Logic



---

## Tenant-Aware Services

All services must understand:

- Current tenant
- User permissions
- Resource ownership


---

# 5. Options Considered


---

# Option 1: Separate Database Per Tenant


Architecture:



Tenant A

Database A

Tenant B

Database B

Tenant C

Database C



## Advantages

- Strong isolation
- Easy tenant backup
- Enterprise friendly


## Disadvantages

- Operational complexity
- Difficult migrations
- Higher infrastructure cost
- Harder analytics


## Decision

Rejected for initial platform.


---

# Option 2: Shared Database, Shared Schema


Architecture:



PostgreSQL

users

agents

calls

documents

tenant_id column



## Advantages

- Simple operations
- Easy migrations
- Efficient infrastructure
- Good SaaS model


## Disadvantages

- Requires strong isolation controls


## Decision

Accepted.


---

# Option 3: Shared Database, Separate Schema Per Tenant


Architecture:



Tenant A Schema

Tenant B Schema

Tenant C Schema



## Advantages

- Better separation


## Disadvantages

- Schema management complexity
- Difficult migrations
- Poor scaling


## Decision

Rejected initially.


---

# 6. Final Multi-Tenant Architecture


The platform will use:


             SaaS Platform


                   |


          Tenant Context


                   |


    --------------------------------


    |              |               |


 Agents        Calls          Knowledge


    |              |               |


    --------------------------------


                   |


             PostgreSQL


              tenant_id


---

# 7. Tenant Model


A tenant represents a customer organization.


Example:



Tenant

|

Users

|

Agents

|

Phone Numbers

|

Knowledge

|

Calls

|

Billing



---

# 8. Tenant Database Strategy


All tenant-owned tables require:



tenant_id



Example:



agents

id

tenant_id

name

configuration

created_at



---

# 9. Tenant Isolation Rules


Mandatory rules:


## Rule 1

Every tenant resource must contain tenant ownership.


---

## Rule 2

Every query must filter by tenant context.


Example:


Incorrect:


SELECT *
FROM agents;



Correct:


SELECT *
FROM agents
WHERE tenant_id = current_tenant;



---

## Rule 3

Services cannot access another tenant's data.


---

## Rule 4

Background jobs must preserve tenant context.


---

# 10. Authentication and Tenant Identification


Authentication flow:



User Login

  |

Identity Provider

  |

JWT Token

  |

Tenant Context

  |

Authorization Check

  |

Application Access



---

# 11. Authorization Model


The platform uses:


## Role Based Access Control (RBAC)


Example roles:



Owner

Admin

Manager

Agent Manager

Viewer



---

# 12. Tenant Resource Ownership


Examples:


## Agents


Owned by:


Tenant



---

## Phone Numbers


Owned by:


Tenant



---

## Knowledge


Owned by:


Tenant



---

## Conversations


Owned by:


Tenant



---

# 13. AI Tenant Isolation


AI systems must respect tenant boundaries.


Includes:


## Agent Isolation

Each tenant has independent:

- Agent configurations
- Prompts
- Workflows


---

## Memory Isolation

Tenant memories must never mix.


---

## RAG Isolation

Knowledge retrieval must always filter:



tenant_id



---

# 14. Voice Tenant Isolation


Voice layer must isolate:


- Phone numbers
- Call records
- Recordings
- Transcripts


Flow:



Incoming Call

  |

Phone Number Lookup

  |

Tenant Identification

  |

Agent Assignment

  |

AI Runtime



---

# 15. Storage Isolation


Object storage structure:



bucket

|

tenant_id

|

documents

|

recordings



Example:



tenant_001/recordings/call123.wav

tenant_002/documents/manual.pdf



---

# 16. API Tenant Isolation


All APIs must:


- Validate tenant ownership
- Validate permissions
- Reject unauthorized access


Example:



GET /api/agents/{id}



Must verify:



agent belongs to current tenant



---

# 17. Background Processing


Background jobs must include:



tenant_id

job_id

user_id



Examples:


- Document processing
- Call analysis
- AI evaluation


---

# 18. Billing Isolation


Usage tracking must be tenant-based.


Track:


- Minutes consumed
- AI tokens
- Storage usage
- Agent executions


---

# 19. Observability Isolation


Logs and metrics should include:



tenant_id

request_id

call_id

agent_id



This enables:

- Debugging
- Usage reporting
- Support operations


---

# 20. Security Considerations


Required controls:


- Row Level Security where appropriate
- Authorization middleware
- Tenant validation
- Audit logs
- Encryption
- Access monitoring


---

# 21. Consequences


## Positive Consequences


- Simple SaaS architecture
- Lower operational cost
- Easier migrations
- Faster development
- Good scalability


---

## Negative Consequences


- Requires strict engineering discipline
- Isolation mistakes can create security issues
- Large tenants may need future separation


---

# 22. Future Evolution


The platform can evolve toward:


## Enterprise Isolation


Dedicated databases for large customers.


---

## Regional Deployment


Separate deployments by geography.


---

## Hybrid Model


Combination:



Small Customers

Shared Database

Large Customers

Dedicated Infrastructure



Any change requires a new ADR.


---

# 23. Implementation Rules


## Rule 1

Tenant isolation is mandatory.


---

## Rule 2

No service may bypass tenant validation.


---

## Rule 3

All tenant-owned data requires ownership metadata.


---

## Rule 4

AI systems must enforce tenant boundaries.


---

## Rule 5

Logs must include tenant context.


---

# 24. Related Documents


Architecture:

- 06_Multi_Tenant_Architecture.md
- 05_Service_Boundaries.md
- 14_Security_Architecture.md
- ADR-0003_Database_Architecture.md


Implementation:

- Authentication Design
- Authorization Model
- Database Schema
- API Security Standards


---

# Final Statement


The Voice Agent SaaS Platform will use a shared infrastructure multi-tenant architecture with strong logical isolation.

This approach provides:

- SaaS scalability
- Operational simplicity
- Security boundaries
- AI isolation
- Future enterprise expansion capability

while avoiding unnecessary complexity during initial platform development.