# Agent Schema

**Document ID:** DB-AGENT-007  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database schema for AI agents in the Voice Agent SaaS platform.

The agent domain manages the complete lifecycle of AI voice agents:

- Agent creation
- Agent configuration
- Prompt management
- Model selection
- Tool assignment
- Deployment
- Versioning
- Runtime configuration

An agent represents an intelligent autonomous system capable of handling voice conversations, executing workflows, using tools, retrieving knowledge, and maintaining memory.

---

# 2. Agent Architecture

High-level model:

             Tenant

                |

              Agent

                |

      +---------+---------+

      |                   |

 Agent Version        Configuration

      |

 Runtime Deployment

      |

 Voice Conversation

      |

 AI Execution

---

# 3. Agent Design Principles

## 3.1 Version Everything

Agent configurations are immutable after deployment.

Changes create new versions.

Example:


Agent v1

Customer Support Agent

    |

Agent v2

Updated Prompt + New Tools


---

## 3.2 Separate Definition From Runtime

Agent configuration:


agent schema


Runtime execution:


agent_runtime schema


---

## 3.3 Tenant Ownership

Every agent belongs to a tenant.

Required:

```sql
tenant_id UUID NOT NULL
4. Agent Schema

Schema:

agent
5. Agent Tables Overview
agent.agents

agent.agent_versions

agent.agent_configs

agent.agent_prompts

agent.agent_models

agent.agent_tools

agent.agent_variables

agent.agent_deployments

agent.agent_tags

6. Agents Table

Table:

agent.agents

Purpose:

Stores the main AI agent entity.

Example:

CREATE TABLE agent.agents
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    status TEXT DEFAULT 'draft',

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
7. Agent States

Supported states:

draft

testing

active

paused

archived

deleted
8. Agent Version Model

Table:

agent.agent_versions

Purpose:

Maintains agent configuration history.

Relationship:

Agent

 |

Version 1

Version 2

Version 3


Example:

CREATE TABLE agent.agent_versions
(
id UUID PRIMARY KEY,

agent_id UUID NOT NULL,

version_number INTEGER NOT NULL,

status TEXT NOT NULL,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Agent Version Lifecycle
Draft

 |

Review

 |

Testing

 |

Published

 |

Production

10. Agent Configuration

Table:

agent.agent_configs

Purpose:

Stores configurable behavior.

Examples:

Greeting message
Personality
Response style
Language
Call behavior

Example:

{
 "language":"en-US",
 "tone":"professional",
 "interruptions":true
}

Database:

config JSONB
11. Prompt Management

Table:

agent.agent_prompts

Purpose:

Stores system instructions.

Examples:

You are a customer support assistant.

You answer questions politely.

You collect customer information.


Structure:

CREATE TABLE agent.agent_prompts
(
id UUID PRIMARY KEY,

agent_version_id UUID NOT NULL,

prompt_type TEXT NOT NULL,

content TEXT NOT NULL

);
12. Prompt Types

Supported:

Type	Purpose
system	Main behavior
greeting	Opening message
fallback	Error handling
escalation	Human transfer
13. Model Configuration

Table:

agent.agent_models

Purpose:

Defines AI models.

Examples:

OpenAI GPT model

Anthropic model

Local Ollama model


Structure:

model_provider

model_name

temperature

max_tokens

configuration JSONB

14. Tool Assignment

Table:

agent.agent_tools

Purpose:

Defines available tools.

Examples:

Calendar Booking

CRM Lookup

Database Search

Email Sending

Payment Processing


Relationship:

Agent

 |

Tools


Example:

CREATE TABLE agent.agent_tools
(
id UUID PRIMARY KEY,

agent_id UUID NOT NULL,

tool_name TEXT NOT NULL

);
15. Agent Variables

Table:

agent.agent_variables

Purpose:

Runtime configurable values.

Examples:

company_name

support_phone

business_hours

location


Example:

{
 "company_name":"Acme Plumbing",
 "timezone":"America/New_York"
}
16. Agent Deployment Model

Table:

agent.agent_deployments

Purpose:

Controls production activation.

Relationship:

Agent

 |

Deployment

 |

Runtime Environment


Fields:

agent_id

version_id

environment

status

deployed_at

17. Deployment Environments

Supported:

development

staging

production
18. Agent Tags

Table:

agent.agent_tags

Purpose:

Classification.

Examples:

sales

support

healthcare

booking

19. Agent Runtime Relationship

Runtime flow:

Incoming Call

      |

Tenant Lookup

      |

Agent Selection

      |

Load Agent Version

      |

Load Configuration

      |

Start Runtime

20. Agent Loading Process
Agent ID

 |

Fetch Deployment

 |

Fetch Version

 |

Fetch Prompt

 |

Fetch Tools

 |

Fetch Model

 |

Initialize Runtime

21. Agent Security Rules

Required:

Tenant isolation
Version validation
Permission checks
Audit logging
22. Agent Performance Considerations

Frequently accessed data:

Active deployments
Current prompts
Model configuration
Tool definitions

Recommended caching:

Redis

+

Application Cache

23. Index Requirements

Required indexes:

CREATE INDEX idx_agents_tenant
ON agent.agents(tenant_id);

Version lookup:

CREATE INDEX idx_agent_versions
ON agent.agent_versions(agent_id);

Deployment lookup:

CREATE INDEX idx_agent_deployment
ON agent.agent_deployments(agent_id,status);
24. Agent Data Flow
Dashboard

 |

Create Agent

 |

Store Configuration

 |

Publish Version

 |

Deploy Agent

 |

Receive Calls

 |

Execute AI Runtime

25. Future Extensions

Possible additions:

agent.templates

agent.evaluations

agent.guardrails

agent.skills

agent.voice_profiles

agent.agent_marketplace

26. Related Documents

Next:

08_AGENT_RUNTIME_SCHEMA.md

09_VOICE_CALL_SCHEMA.md

10_CONVERSATION_SCHEMA.md
End of Document