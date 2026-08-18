# Schema Organization

**Document ID:** DB-SCHEMA-003  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the PostgreSQL schema organization strategy for the AI Voice Agent SaaS platform.

The database is organized into logical schemas based on business capabilities rather than technical layers.

The schema structure supports:

- Multi-tenant SaaS architecture
- Domain ownership
- Independent service development
- Security isolation
- Easier database scaling
- Clear data boundaries

---

# 2. Schema Architecture Principles

The database follows these principles:

## 2.1 Domain Ownership

Each schema represents a business domain.

Example:


agent schema

Owns:

AI agent definitions
Agent configurations
Agent versions

---

## 2.2 Controlled Data Access

Services should only access schemas they own.

Example:


Voice Service

Allowed:
voice.*
conversation.*

Restricted:
billing.*
identity.*


---

## 2.3 Avoid Cross-Domain Coupling

Schemas communicate through:

- Foreign keys
- Service APIs
- Events

Avoid:


agent.agents
directly modifying
billing.invoices


---

# 3. Complete Schema Map

Production PostgreSQL layout:


PostgreSQL Cluster

|
+------------------------------------------------+
|
+-- core
|
+-- tenant
|
+-- identity
|
+-- agent
|
+-- voice
|
+-- conversation
|
+-- knowledge
|
+-- memory
|
+-- workflow
|
+-- integration
|
+-- billing
|
+-- analytics
|
+-- audit


---

# 4. Core Schema

Schema:


core


Purpose:

Platform-wide shared functionality.

---

## Tables


core.settings

core.feature_flags

core.system_configs

core.countries

core.languages

core.timezones


---

## Responsibilities

Contains:

- Global configuration
- Reference data
- Platform settings

Does not contain:

- Customer data
- Application entities

---

# 5. Tenant Schema

Schema:


tenant


Purpose:

Customer organization management.

---

## Tables


tenant.organizations

tenant.workspaces

tenant.tenant_settings

tenant.domains

tenant.subscription_links


---

## Example Entity

Organization:


Organization

|

id
name
industry
created_at

---

# 6. Identity Schema

Schema:


identity


Purpose:

Authentication and authorization.

---

## Tables


identity.users

identity.roles

identity.permissions

identity.user_roles

identity.sessions

identity.api_keys

identity.oauth_accounts


---

## Responsibilities

Handles:

- Login
- User access
- Permissions
- Authentication providers

---

# 7. Agent Schema

Schema:


agent


Purpose:

AI agent lifecycle management.

---

## Tables


agent.agents

agent.agent_versions

agent.agent_prompts

agent.agent_models

agent.agent_tools

agent.agent_variables

agent.agent_deployments


---

## Example Relationship


Agent

|

Agent Version

|

Prompt

|

Tools


---

# 8. Voice Schema

Schema:


voice


Purpose:

Telephony infrastructure.

---

## Tables


voice.phone_numbers

voice.providers

voice.sip_connections

voice.call_sessions

voice.call_routes

voice.recordings

voice.transfers


---

## External Systems

Integrates with:

- Twilio
- LiveKit
- SIP providers
- Voice providers

---

# 9. Conversation Schema

Schema:


conversation


Purpose:

Stores interaction history.

---

## Tables


conversation.conversations

conversation.messages

conversation.transcripts

conversation.events

conversation.participants

conversation.summaries


---

## Data Flow


Phone Call

|

Voice Session

|

Conversation

|

Messages

|

Transcript

|

Summary


---

# 10. Knowledge Schema

Schema:


knowledge


Purpose:

AI knowledge management and RAG.

---

## Tables


knowledge.knowledge_bases

knowledge.documents

knowledge.document_chunks

knowledge.embeddings

knowledge.retrieval_logs


---

## RAG Pipeline


Document

|

Chunking

|

Embedding Generation

|

Vector Storage

|

Similarity Search

|

LLM Context


---

# 11. Memory Schema

Schema:


memory


Purpose:

AI memory storage.

---

## Tables


memory.user_memories

memory.agent_memories

memory.conversation_memory

memory.memory_embeddings


---

## Memory Types

| Type | Purpose |
|-|-|
| Short-term | Current conversation |
| Long-term | User preferences |
| Agent | Agent knowledge |
| Session | Runtime context |

---

# 12. Workflow Schema

Schema:


workflow


Purpose:

Agent automation and orchestration.

---

## Tables


workflow.workflows

workflow.workflow_versions

workflow.nodes

workflow.executions

workflow.tasks

workflow.execution_logs


---

# 13. Integration Schema

Schema:


integration


Purpose:

External system connections.

---

## Tables


integration.connections

integration.credentials

integration.webhooks

integration.events

integration.sync_jobs


---

## Supported Integrations

Examples:

- CRM systems
- Calendars
- Payment systems
- Messaging platforms

---

# 14. Billing Schema

Schema:


billing


Purpose:

SaaS monetization.

---

## Tables


billing.plans

billing.subscriptions

billing.usage_events

billing.invoices

billing.payments


---

# 15. Analytics Schema

Schema:


analytics


Purpose:

Reporting and business intelligence.

---

## Tables


analytics.call_metrics

analytics.agent_metrics

analytics.tenant_metrics

analytics.daily_usage


---

# 16. Audit Schema

Schema:


audit


Purpose:

Security and compliance tracking.

---

## Tables


audit.audit_logs

audit.security_events

audit.data_changes

audit.access_logs


---

# 17. Schema Dependency Map

             core

              |

           tenant

              |

    +---------+---------+

    |                   |

identity              agent

                        |

                      voice

                        |

                conversation

                        |

      +-----------------+----------------+

      |                                  |

  knowledge                         memory


                        |

                    workflow


                        |

                  integration


                        |

                     billing


                        |

                   analytics


                        |

                       audit

---

# 18. Cross Schema Rules

## Rule 1

Tenant schema is the ownership root.

Most business tables reference:


tenant.organizations.id


---

## Rule 2

Identity references tenant.

Example:


identity.users

tenant_id


---

## Rule 3

Agents belong to tenants.

Example:


agent.agents

tenant_id


---

## Rule 4

Calls belong to tenants and agents.

Example:


voice.call_sessions

tenant_id

agent_id


---

# 19. Schema Permissions

Recommended PostgreSQL roles:


schema_owner

service_role

readonly_role

migration_role


---

Example:


agent_service

CAN:

SELECT agent.*

INSERT agent.*

UPDATE agent.*


Cannot:


DROP schema

CREATE extensions

Modify billing


---

# 20. Schema Migration Strategy

Each schema owns its migrations.

Example:


migrations/

|
+-- core/

+-- tenant/

+-- identity/

+-- agent/

+-- voice/


---

# 21. Future Schema Expansion

Possible future domains:


compliance

marketplace

ai_training

experiments

notifications

support


---

# 22. Related Documents

Next:


04_MULTI_TENANT_DATA_MODEL.md

05_CORE_ENTITY_MODEL.md

06_USER_IDENTITY_SCHEMA.md


---

# End of Document