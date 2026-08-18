# Agent Runtime Schema

**Document ID:** DB-RUNTIME-008  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database design for the AI Agent Runtime system.

The runtime domain manages the execution state of AI agents while they are actively processing tasks, conversations, and workflows.

The runtime layer is responsible for:

- Active agent sessions
- Runtime state
- Execution context
- Tool executions
- Agent events
- State persistence
- Memory synchronization
- Workflow coordination

The runtime schema is separate from the agent configuration schema.

---

# 2. Agent Runtime Architecture

High-level architecture:

             Agent Definition

                    |

             Agent Deployment

                    |

              Agent Runtime

                    |

    +---------------+---------------+

    |               |               |

Runtime State   Tool Calls     Events

                    |

             Conversation Layer

---

# 3. Runtime Design Principles

## 3.1 Configuration vs Execution Separation

Agent schema:

Stores:

- What the agent is
- How it behaves
- Which tools it has

Runtime schema:

Stores:

- What the agent is doing now
- Current state
- Execution history

---

## 3.2 Short-Lived and Persistent State

Runtime data is divided into:


Ephemeral State

Persistent State


---

Ephemeral:

- Current execution state
- Active context
- Temporary variables

Stored in:

- Redis
- Memory cache

---

Persistent:

- Sessions
- Events
- Tool executions
- State checkpoints

Stored in:

- PostgreSQL

---

# 4. Runtime Schema

Schema:


agent_runtime


---

# 5. Runtime Tables Overview


agent_runtime.sessions

agent_runtime.execution_contexts

agent_runtime.state_snapshots

agent_runtime.events

agent_runtime.tool_executions

agent_runtime.workflow_runs

agent_runtime.checkpoints


---

# 6. Agent Runtime Session

Table:


agent_runtime.sessions


Purpose:

Represents one running instance of an AI agent.

Examples:


Phone Call Agent Session

Chat Agent Session

Workflow Agent Session


---

Structure:

```sql
CREATE TABLE agent_runtime.sessions
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    agent_id UUID NOT NULL,

    status TEXT NOT NULL,

    started_at TIMESTAMPTZ DEFAULT now(),

    ended_at TIMESTAMPTZ
);
7. Runtime Session Lifecycle
Created

 |

Initializing

 |

Running

 |

Waiting

 |

Completed

 |

Failed

8. Runtime Status Values

Supported:

initializing

active

paused

completed

failed

terminated
9. Execution Context

Table:

agent_runtime.execution_contexts

Purpose:

Stores the current working context.

Contains:

User information
Conversation state
Variables
Tool results
Runtime metadata

Example:

{
 "customer_name":"John",
 "intent":"booking",
 "appointment_date":"2026-07-25"
}

Database:

context JSONB
10. Runtime State Model

Agent state example:

START

 |

IDENTIFY_USER

 |

UNDERSTAND_REQUEST

 |

CALL_TOOL

 |

RESPOND

 |

END


Stored as:

state_snapshots
11. State Snapshots

Table:

agent_runtime.state_snapshots

Purpose:

Stores recoverable runtime states.

Example:

CREATE TABLE agent_runtime.state_snapshots
(
id UUID PRIMARY KEY,

session_id UUID NOT NULL,

state_name TEXT NOT NULL,

state_data JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
12. LangGraph Integration

The runtime schema supports LangGraph execution.

Mapping:

LangGraph State

        |

State Snapshot

        |

PostgreSQL Persistence


Stores:

Current node
Previous nodes
State data
Execution history
13. Runtime Events

Table:

agent_runtime.events

Purpose:

Stores runtime activity.

Examples:

Agent Started

LLM Called

Tool Executed

Memory Retrieved

Human Transfer

Agent Completed


Structure:

CREATE TABLE agent_runtime.events
(
id UUID PRIMARY KEY,

session_id UUID NOT NULL,

event_type TEXT NOT NULL,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
14. Event Types

Examples:

Event	Description
agent_started	Runtime initialized
llm_request	Model invocation
llm_response	Model output
tool_called	Tool execution
memory_loaded	Memory retrieval
error	Runtime failure
completed	Session finished
15. Tool Execution Tracking

Table:

agent_runtime.tool_executions

Purpose:

Tracks every external action.

Examples:

Calendar Lookup

CRM Search

Email Sending

Database Query


Structure:

CREATE TABLE agent_runtime.tool_executions
(
id UUID PRIMARY KEY,

session_id UUID NOT NULL,

tool_name TEXT NOT NULL,

input JSONB,

output JSONB,

status TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Tool Execution Lifecycle
Requested

 |

Running

 |

Completed

 |

Failed

17. Workflow Runtime

Table:

agent_runtime.workflow_runs

Purpose:

Tracks automation execution.

Examples:

Lead Qualification Workflow

Appointment Booking Workflow

Customer Support Workflow

18. Runtime Checkpoints

Table:

agent_runtime.checkpoints

Purpose:

Enables recovery.

Used for:

Agent crashes
Network failures
Long-running tasks

Example:

Call Interrupted

       |

Load Checkpoint

       |

Resume Agent

19. Runtime Data Flow
Incoming Request

        |

Create Runtime Session

        |

Load Agent Version

        |

Initialize Context

        |

Execute Graph

        |

Store Events

        |

Update State

        |

Complete

20. Runtime Storage Strategy
PostgreSQL

Stores:

Sessions
Events
Checkpoints
History
Redis

Stores:

Active state
Temporary context
Low latency data

Architecture:

Agent Runtime

       |

+--------------+

|              |

Redis       PostgreSQL

Fast        Persistent

21. Multi-Tenant Rules

All runtime tables require:

tenant_id UUID NOT NULL

RLS enabled:

agent_runtime.*
22. Performance Requirements

High-volume tables:

agent_runtime.events

agent_runtime.tool_executions

agent_runtime.state_snapshots


Required:

Indexing
Partitioning strategy
Retention policy
23. Index Requirements

Session lookup:

CREATE INDEX idx_runtime_sessions_agent
ON agent_runtime.sessions(agent_id);

Event lookup:

CREATE INDEX idx_runtime_events_session
ON agent_runtime.events(session_id);
24. Data Retention

Runtime events:

30-180 days

Long-term analytics:

Move to:

analytics schema
25. Security Requirements

Required:

Tenant isolation
Sensitive data filtering
Audit logging
Encrypted secrets
Tool authorization
26. Future Extensions

Possible additions:

agent_runtime.agent_traces

agent_runtime.reasoning_logs

agent_runtime.evaluations

agent_runtime.performance_metrics

agent_runtime.replay_sessions

27. Related Documents

Next:

09_VOICE_CALL_SCHEMA.md

10_CONVERSATION_SCHEMA.md

11_KNOWLEDGE_SCHEMA.md
End of Document