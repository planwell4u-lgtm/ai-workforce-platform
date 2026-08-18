# Workflow Schema

**Document ID:** DB-WORKFLOW-014  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for the workflow automation engine used by the AI Voice Agent SaaS platform.

The workflow subsystem enables AI agents and business processes to execute multi-step automation sequences.

The workflow engine supports:

- Visual workflow builders
- Event-driven automation
- Agent task orchestration
- Human approval steps
- External integrations
- Conditional branching
- Background jobs
- Workflow execution tracking

---

# 2. Workflow Architecture

High-level workflow model:

            Trigger Event

                 |

          Workflow Definition

                 |

          Workflow Execution

                 |

      +----------+----------+

      |                     |

   Workflow Steps       Conditions

      |

   Actions

      |

External Systems / AI Agents


---

# 3. Workflow Design Principles

## 3.1 Definition vs Execution Separation

Workflow templates are separated from runtime executions.

Example:


Workflow Definition

"Customer Booking Flow"

    |

Workflow Execution

Customer John Booking Request


---

## 3.2 Event Driven Execution

Workflows can start from:

- Voice calls
- Webhooks
- Agent actions
- Scheduled events
- User actions
- Integration events

---

## 3.3 Durable Execution

Workflow state must survive:

- Service restarts
- Network failures
- Worker failures
- Retry operations

---

# 4. Workflow Schema

Schema:


workflow


---

# 5. Workflow Tables Overview


workflow.definitions

workflow.versions

workflow.nodes

workflow.edges

workflow.triggers

workflow.executions

workflow.execution_steps

workflow.jobs

workflow.approvals

workflow.variables

workflow.logs


---

# 6. Workflow Definitions

Table:


workflow.definitions


Purpose:

Stores workflow templates.

Examples:


Appointment Booking

Lead Qualification

Customer Follow-up

Call Escalation


---

Structure:

```sql
CREATE TABLE workflow.definitions
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    name TEXT NOT NULL,

    description TEXT,

    status TEXT DEFAULT 'draft',

    created_by UUID,

    created_at TIMESTAMPTZ DEFAULT now(),

    updated_at TIMESTAMPTZ DEFAULT now()
);
7. Workflow Lifecycle
Draft

 |

Testing

 |

Published

 |

Active

 |

Archived

8. Workflow Versions

Table:

workflow.versions

Purpose:

Maintains workflow history.

Example:

Booking Workflow v1

        |

Booking Workflow v2


Structure:

CREATE TABLE workflow.versions
(
id UUID PRIMARY KEY,

workflow_id UUID NOT NULL,

version_number INTEGER NOT NULL,

definition JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
9. Workflow Nodes

Table:

workflow.nodes

Purpose:

Stores workflow execution components.

Node examples:

Start Node

AI Agent Node

Condition Node

API Node

Human Approval Node

End Node


Structure:

CREATE TABLE workflow.nodes
(
id UUID PRIMARY KEY,

workflow_version_id UUID NOT NULL,

node_type TEXT NOT NULL,

configuration JSONB,

position JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Workflow Node Types

Supported:

Node Type	Purpose
trigger	Start workflow
agent	Execute AI agent
action	Call external tool
condition	Branch logic
approval	Human decision
delay	Wait operation
webhook	External event
end	Complete workflow
11. Workflow Edges

Table:

workflow.edges

Purpose:

Defines connections between nodes.

Example:

Node A

 |

Node B

 |

Node C


Structure:

CREATE TABLE workflow.edges
(
id UUID PRIMARY KEY,

workflow_version_id UUID NOT NULL,

source_node_id UUID NOT NULL,

target_node_id UUID NOT NULL,

condition JSONB
);
12. Workflow Triggers

Table:

workflow.triggers

Purpose:

Defines workflow start events.

Examples:

Incoming Call

Customer Created

Payment Received

Webhook Received

Schedule Trigger


Structure:

CREATE TABLE workflow.triggers
(
id UUID PRIMARY KEY,

workflow_id UUID NOT NULL,

trigger_type TEXT NOT NULL,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
13. Workflow Execution

Table:

workflow.executions

Purpose:

Stores workflow runtime instances.

Example:

Workflow:

Appointment Booking


Execution:

Customer #123 Booking


Structure:

CREATE TABLE workflow.executions
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

workflow_id UUID NOT NULL,

status TEXT,

input JSONB,

output JSONB,

started_at TIMESTAMPTZ,

completed_at TIMESTAMPTZ
);
14. Execution Status
pending

running

waiting

completed

failed

cancelled

15. Execution Steps

Table:

workflow.execution_steps

Purpose:

Tracks individual node execution.

Structure:

CREATE TABLE workflow.execution_steps
(
id UUID PRIMARY KEY,

execution_id UUID NOT NULL,

node_id UUID NOT NULL,

status TEXT,

input JSONB,

output JSONB,

error JSONB,

started_at TIMESTAMPTZ,

completed_at TIMESTAMPTZ
);
16. Workflow Jobs

Table:

workflow.jobs

Purpose:

Background execution queue.

Examples:

Send Email

Call API

Process Document

Retry Failed Step


Structure:

CREATE TABLE workflow.jobs
(
id UUID PRIMARY KEY,

execution_id UUID NOT NULL,

job_type TEXT,

status TEXT,

scheduled_at TIMESTAMPTZ,

completed_at TIMESTAMPTZ
);
17. Human Approval Workflow

Table:

workflow.approvals

Purpose:

Supports human-in-the-loop operations.

Examples:

Approve Refund

Approve Escalation

Verify Customer


Structure:

CREATE TABLE workflow.approvals
(
id UUID PRIMARY KEY,

execution_step_id UUID NOT NULL,

assigned_user_id UUID,

status TEXT,

decision JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
18. Workflow Variables

Table:

workflow.variables

Purpose:

Stores execution state variables.

Example:

{
 "customer_name":"John",
 "appointment_date":"2026-07-30"
}

Structure:

CREATE TABLE workflow.variables
(
id UUID PRIMARY KEY,

execution_id UUID NOT NULL,

variable_name TEXT,

value JSONB
);
19. Workflow Logs

Table:

workflow.logs

Purpose:

Stores workflow execution history.

Events:

WORKFLOW_STARTED

NODE_COMPLETED

NODE_FAILED

WORKFLOW_COMPLETED


Structure:

CREATE TABLE workflow.logs
(
id UUID PRIMARY KEY,

execution_id UUID NOT NULL,

event_type TEXT,

details JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
20. Agent Runtime Integration

Workflow execution with AI agents:

Customer Request

        |

Agent Runtime

        |

Workflow Engine

        |

AI Agent Node

        |

Tools / Integrations

        |

Response

21. Voice Platform Integration

Example:

Incoming call workflow:

Inbound Call

     |

Identify Customer

     |

Run Agent

     |

Check Availability

     |

Book Appointment

     |

Confirm Call

22. Multi-Tenant Requirements

Tenant-owned tables:

workflow.definitions

workflow.executions

workflow.jobs

workflow.logs


Require:

tenant_id UUID NOT NULL
23. Performance Requirements

High-volume tables:

Table	Growth
executions	Very High
execution_steps	Very High
logs	Very High
jobs	High
24. Index Requirements

Tenant lookup:

CREATE INDEX idx_workflow_tenant
ON workflow.executions(tenant_id);

Execution search:

CREATE INDEX idx_execution_steps
ON workflow.execution_steps(execution_id);

Job queue:

CREATE INDEX idx_workflow_jobs_status
ON workflow.jobs(status, scheduled_at);
25. Security Requirements

Required:

Tenant isolation
Workflow permission control
Execution audit trail
Secret protection
Approval authorization
26. Future Extensions

Possible additions:

workflow.templates

workflow.marketplace

workflow.ai_generation

workflow.optimization

workflow.analytics

workflow.simulations

27. Related Documents

Previous:

12_RAG_SCHEMA.md

13_MEMORY_SCHEMA.md

Next:

15_INTEGRATION_SCHEMA.md

16_BILLING_SCHEMA.md

17_ANALYTICS_SCHEMA.md

18_AUDIT_SCHEMA.md
End of Document