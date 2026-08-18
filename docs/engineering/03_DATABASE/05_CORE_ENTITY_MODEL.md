# Core Entity Model

**Document ID:** DB-CORE-005  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the core entity model for the AI Voice Agent SaaS platform.

Core entities represent the foundational objects shared across the entire platform.

These entities establish relationships between:

- Organizations
- Users
- Workspaces
- AI agents
- Voice infrastructure
- Conversations
- Knowledge systems
- Billing
- Audit systems

The core entity model provides the foundation for all other database domains.

---

# 2. Entity Architecture

High-level relationship:

                Platform

                   |

             Organization

                   |

             Workspace

                   |

    +--------------+--------------+

    |              |              |

  Users          Agents        Integrations

                   |

                Voice

                   |

             Conversations

                   |

          Knowledge / Memory

                   |

              Analytics

---

# 3. Core Entity Principles

## 3.1 Every Business Entity Requires

Standard fields:

```sql
id UUID PRIMARY KEY

tenant_id UUID

created_at TIMESTAMPTZ

updated_at TIMESTAMPTZ

deleted_at TIMESTAMPTZ
3.2 Entity Ownership

Every customer-owned entity must have:

tenant_id

Example:

agent.agents

voice.call_sessions

knowledge.documents
4. Core Entity List

The platform core entities:

Entity	Schema	Purpose
Organization	tenant	Customer company
Workspace	tenant	Operational environment
User	identity	Platform user
Membership	identity	User access relationship
Agent	agent	AI assistant
Phone Number	voice	Telephony identity
Call Session	voice	Voice interaction
Conversation	conversation	AI interaction
Knowledge Base	knowledge	AI knowledge source
Integration	integration	External system
Subscription	billing	Commercial relationship
5. Organization Entity

Table:

tenant.organizations

Purpose:

Represents a SaaS customer.

Example:

Acme Healthcare

XYZ Plumbing

ABC Support Center
Attributes
Column	Type	Description
id	UUID	Organization ID
name	TEXT	Display name
slug	TEXT	Unique identifier
status	TEXT	Active state
created_at	TIMESTAMP	Creation time

Example:

CREATE TABLE tenant.organizations
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

name TEXT NOT NULL,

slug TEXT UNIQUE NOT NULL,

status TEXT DEFAULT 'active',

created_at TIMESTAMPTZ DEFAULT now()
);
6. Workspace Entity

Table:

tenant.workspaces

Purpose:

Represents an isolated operating environment.

Examples:

Production

Sales Team

Customer Support

Testing

Relationship:

Organization

     |

 Workspace

7. User Entity

Table:

identity.users

Purpose:

Represents platform users.

Users can:

Configure agents
Manage calls
View analytics
Manage billing

Relationship:

User

 |

Membership

 |

Organization

8. Membership Entity

Table:

identity.memberships

Purpose:

Connects users with organizations.

Example:

John

belongs to

Acme Healthcare

Role:

Admin

9. Agent Entity

Table:

agent.agents

Purpose:

Represents an AI voice agent.

Examples:

Receptionist Agent
Sales Agent
Booking Agent
Support Agent
Medical Assistant

Relationship:

Organization

      |

    Agent

      |

 Agent Version

      |

 Runtime Configuration

10. Phone Number Entity

Table:

voice.phone_numbers

Purpose:

Represents assigned telephony numbers.

Examples:

+1 555 555 1234

+44 20 XXXX XXXX


Relationship:

Tenant

 |

Phone Number

 |

Call Routing

11. Call Session Entity

Table:

voice.call_sessions

Purpose:

Represents a voice call lifecycle.

Lifecycle:

Incoming Call

      |

Call Session Created

      |

Agent Assigned

      |

Conversation Started

      |

Call Completed


Important fields:

call_sid

provider

direction

status

started_at

ended_at

duration
12. Conversation Entity

Table:

conversation.conversations

Purpose:

Stores AI interactions.

Relationship:

Call Session

      |

 Conversation

      |

 Messages


Contains:

User messages
AI responses
Tool calls
Events
Summaries
13. Knowledge Base Entity

Table:

knowledge.knowledge_bases

Purpose:

Stores tenant AI knowledge sources.

Examples:

Product manuals

FAQs

Company policies

Training documents


Relationship:

Knowledge Base

      |

Documents

      |

Chunks

      |

Embeddings

14. Integration Entity

Table:

integration.connections

Purpose:

Stores external system connections.

Examples:

CRM
Calendar
ERP
Ticketing systems

Relationship:

Tenant

 |

Integration

 |

External Provider

15. Subscription Entity

Table:

billing.subscriptions

Purpose:

Represents customer billing state.

Relationship:

Organization

      |

Subscription

      |

Plan

16. Entity Relationship Overview
tenant.organizations

        |

        +----------------+

        |                |

 tenant.workspaces   identity.memberships

                         |

                    identity.users


        |

   agent.agents

        |

 voice.call_sessions

        |

conversation.conversations

        |

knowledge.knowledge_bases


17. Common Entity Lifecycle

All entities follow:

Create

 |

Active

 |

Updated

 |

Archived

 |

Deleted

18. Audit Requirements

Core entities must support:

Creation tracking
Modification tracking
User attribution
Historical records

Required fields:

created_by

updated_by

created_at

updated_at

19. Data Ownership Matrix
Entity	Owner
Organization	Tenant Service
Users	Identity Service
Agents	Agent Service
Calls	Voice Service
Conversations	Conversation Service
Knowledge	RAG Service
Billing	Billing Service
20. Future Extensions

Potential entities:

marketplace_agents

agent_templates

workflow_templates

evaluation_runs

ai_models

21. Related Documents

Next:

06_USER_IDENTITY_SCHEMA.md

07_AGENT_SCHEMA.md

08_AGENT_RUNTIME_SCHEMA.md
End of Document