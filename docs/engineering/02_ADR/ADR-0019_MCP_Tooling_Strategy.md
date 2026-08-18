# ADR-0019: MCP Tooling Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Model Context Protocol (MCP) Tooling Strategy  
**ADR Number:** ADR-0019  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will adopt the Model Context Protocol (MCP) as a standardized method for connecting AI agents with external tools, applications, knowledge systems, and business capabilities.

The MCP architecture will provide a controlled tool ecosystem for AI agents.


The approved strategy:


| Capability | Decision |
|---|---|
| Tool communication | MCP-compatible protocol |
| Tool discovery | MCP servers |
| Tool execution | AI Runtime controlled |
| Permissions | Tenant-aware authorization |
| Security | Explicit tool access policies |
| Tool management | Centralized registry |
| Observability | Complete tool execution tracking |


Architecture:



AI Agent

|

AI Runtime

|

MCP Client

|

MCP Servers

|

External Capabilities



---

# 2. Context


AI agents become powerful when they can perform actions.


Examples:


Reception Agent:


- Search customer records
- Check appointments
- Create bookings


Sales Agent:


- Create CRM leads
- Send emails
- Schedule meetings


Support Agent:


- Search documentation
- Create tickets
- Update customer records


Without a standardized tool system, every integration becomes custom development.


---

# 3. Problem Statement


The platform must solve:


## Tool Scalability


The number of tools will grow:



Calendar

CRM

Email

Database

Knowledge

Payments

ERP

Custom APIs



---

## Tool Security


Agents must not have unlimited access.


Example:


A sales agent should not access:



Billing Administration



---

## Provider Independence


Tools should be replaceable.


Example:


CRM:



Salesforce

HubSpot

Custom CRM



---

## AI Compatibility


Tools should work across different AI models.


---

# 4. MCP Architecture Goals


The MCP strategy provides:


## Standardization


Common interface for tools.


---

## Discoverability


Agents can discover available capabilities.


---

## Security


Tools require permissions.


---

## Reusability


One tool can support many agents.


---

# 5. Options Considered


---

# Option 1: Custom Tool Framework


Architecture:



Agent

|

Custom APIs

|

Services



## Advantages


- Full control


## Disadvantages


- Reinventing infrastructure
- Poor interoperability


## Decision

Rejected.


---

# Option 2: Direct API Access From Agents


Architecture:



Agent

|

External API



## Advantages


- Simple implementation


## Disadvantages


- Security risk
- Tight coupling
- Difficult management


## Decision

Rejected.


---

# Option 3: MCP-Based Tool Architecture


Architecture:



Agent

|

MCP Client

|

MCP Server

|

Capability



## Advantages


- Standardized
- Secure
- Extensible


## Decision

Accepted.


---

# 6. Final MCP Architecture


             AI Agent


                |


          AI Runtime


                |


          MCP Client


                |


    -------------------------


    |          |            |


CRM MCP   Calendar MCP   Data MCP


    |          |            |


    -------------------------


          External Systems


---

# 7. MCP Components


The platform contains:


---

# 7.1 MCP Client


Responsibilities:


- Connect to MCP servers
- Discover tools
- Execute approved actions


Location:



AI Runtime



---

# 7.2 MCP Server


Responsibilities:


- Expose tools
- Validate requests
- Execute actions


Examples:



Calendar MCP Server

CRM MCP Server

Knowledge MCP Server



---

# 7.3 Tool Registry


Stores:



Tool Name

Description

Permissions

Required Roles

Available Agents

Version



---

# 8. Tool Execution Flow



User Request

  |

AI Agent

  |

Tool Decision

  |

Permission Check

  |

MCP Client

  |

MCP Server

  |

External System

  |

Result

  |

Agent Response



---

# 9. Tool Permission Model


Every tool requires:


## Identity


Who is executing?


---

## Tenant


Which business owns the action?


---

## Agent Permission


Which agents can use it?


---

## User Permission


Does the user allow this action?


---

# 10. Example MCP Tools


---

# Calendar MCP


Capabilities:



Check Availability

Create Appointment

Cancel Appointment



Used by:


- Reception Agent
- Appointment Booking Agent


---

# CRM MCP


Capabilities:



Create Lead

Update Contact

Search Customer



Used by:


- Sales Agent
- Lead Qualification Agent


---

# Knowledge MCP


Capabilities:



Search Documents

Retrieve Information

Update Knowledge



Used by:


- Support Agent
- Reception Agent


---

# Database MCP


Capabilities:



Query Approved Data

Retrieve Records

Execute Safe Operations



---

# 11. MCP Security Strategy


Security controls:


## Authentication


MCP servers require identity validation.


---

## Authorization


Tools require permission checks.


---

## Data Filtering


Results must respect:



tenant_id

user permissions

agent permissions



---

## Audit Logging


Record:



Tool Used

Agent

User

Tenant

Input

Output

Timestamp



---

# 12. MCP and RAG Integration


MCP can expose knowledge capabilities.


Example:



Agent

|

Knowledge MCP

|

RAG System

|

Vector Search

|

Documents



---

# 13. MCP and Memory Integration


Agents may access memory through controlled tools.


Example:



Agent

|

Memory MCP

|

Memory Service

|

Redis/PostgreSQL



---

# 14. MCP Version Management


Tools require versioning.


Example:



Calendar MCP v1

Calendar MCP v2



Old versions remain supported when required.


---

# 15. MCP Observability


Track:


## Tool Performance


- Execution time
- Failures
- Latency


---

## Business Usage


- Most used tools
- Successful actions


---

## Security


- Unauthorized attempts
- Permission failures


---

# 16. Implementation Rules


## Rule 1

Agents never directly access external systems.


---

## Rule 2

Every tool requires permissions.


---

## Rule 3

Every tool execution must be logged.


---

## Rule 4

Tools must be tenant aware.


---

## Rule 5

Tool versions must be managed.


---

# 17. Consequences


## Positive Consequences


- Standard AI integration model
- Safer agent actions
- Faster integration development
- Reusable capabilities


---

## Negative Consequences


- Additional infrastructure
- Requires MCP governance
- Tool management complexity


---

# 18. Future Evolution


Future capabilities:


- MCP marketplace
- Community tools
- Automated tool generation
- Agent-to-agent MCP communication
- Enterprise MCP ecosystem


Major changes require new ADRs.


---

# 19. Related Documents


Architecture:


- 17_Integration_Architecture.md
- 10_AI_Runtime_Architecture.md
- 13_Agent_Architecture.md


Related ADRs:


- ADR-0016_Agent_Platform_Strategy.md
- ADR-0018_Integration_Strategy.md


---

# Final Statement


The Voice Agent SaaS Platform will adopt MCP as the standard tool connectivity layer for AI agents.

This enables:

- Secure AI tool execution
- Reusable integrations
- Provider flexibility
- Enterprise-ready agent capabilities