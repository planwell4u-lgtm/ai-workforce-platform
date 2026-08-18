# ADR-0036: Human-in-the-Loop and Agent Escalation Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Human-in-the-Loop and Agent Escalation Strategy  
**ADR Number:** ADR-0036  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will implement a Human-in-the-Loop (HITL) architecture that allows AI agents to seamlessly transfer conversations to human operators when required.

AI agents will remain the primary automation layer, while humans provide support for:

- Complex situations
- Sensitive conversations
- Customer requests requiring judgment
- Failed automation scenarios
- Business-specific exceptions


Architecture:


                Customer


                   |


             Voice Channel


                   |


             AI Agent


                   |


      Decision: Continue or Escalate


             /              \


            /                \


    AI Resolution        Human Agent


            \                /


             \              /


          Conversation Complete

---

# 2. Context


AI agents can automate many business conversations, but some situations require human involvement.


Examples:



Customer Complaint

Complex Support Issue

High Value Sales Opportunity

Sensitive Medical Question

Payment Problem

Customer Request


A production AI platform must provide controlled escalation instead of forcing every conversation through automation.

---

# 3. Problem Statement


The platform must support:


## Intelligent Escalation


Determine when AI should request human help.


---

## Smooth Transfer


Customers should not repeat information.


---

## Human Context


Human agents need conversation history.


---

## Business Control


Companies need customizable escalation rules.


---

# 4. Goals


The strategy provides:


## Better Customer Experience


Customers receive human assistance when necessary.


---

## Higher Automation Rate


AI handles simple tasks independently.


---

## Operational Control


Businesses define escalation policies.


---

## Reduced AI Failures


Critical situations receive human support.

---

# 5. Options Considered


---

# Option 1: AI Only


Architecture:



Customer

|

AI Agent

|

Completion


## Advantages

- Maximum automation


## Disadvantages

- Poor handling of exceptions
- Customer frustration


## Decision

Rejected.


---

# Option 2: Always Human Transfer


Architecture:



Customer

|

Human Agent


## Advantages

- Simple


## Disadvantages

- Expensive
- Low automation


## Decision

Rejected.


---

# Option 3: AI First with Human Escalation


Architecture:



Customer

|

AI Agent

|

Human When Needed


## Advantages

- Best balance
- Scalable
- Better experience


## Decision

Accepted.


---

# 6. Final HITL Architecture


             Conversation


                  |


          AI Decision Engine


                  |

| | |

Continue Escalate Transfer

| | |

AI Workflow Human Queue Human Agent

                  |


          Conversation Context

---

# 7. Escalation Triggers


Escalation can happen because of:


---

# 7.1 Customer Request


Example:



"I want to speak with a person"


---

# 7.2 AI Confidence


When confidence is low:



Unknown Question

Poor Retrieval

Unclear Intent


---

# 7.3 Business Rules


Examples:



High Value Customer

Refund Request

Complaint

Medical Concern


---

# 7.4 Workflow Failure


Examples:



Tool Failure

Integration Error

Unable To Complete Task


---

# 7.5 Safety Requirements


Examples:



Sensitive Information

Compliance Requirement

Risky Situation


---

# 8. Escalation Decision Model


The AI runtime evaluates:



Intent

Confidence

Business Rules

Customer Profile

Conversation History

Agent Policy


---

# 9. Human Transfer Process


Transfer flow:



Escalation Decision

    |

Create Transfer Request

    |

Find Available Agent

    |

Provide Context

    |

Transfer Conversation

    |

Human Resolution


---

# 10. Conversation Context Transfer


Human agents receive:


## Customer Information


- Name
- Contact details
- Account information


---

## Conversation History


- Previous messages
- Customer intent
- Agent actions


---

## AI Summary


Example:



Customer wants appointment change.

AI verified account.

Calendar tool failed.

Human assistance required.


---

# 11. Human Agent Interface


The platform should provide:


## Live Conversation View


Shows:


- Transcript
- Customer information
- AI status


---

## Agent Controls


Allows:


- Take over conversation
- Send messages
- End conversation


---

## AI Assistance


Provides:


- Suggested responses
- Knowledge lookup
- Customer history


---

# 12. Human Queue Management


Queue considers:


- Priority
- Customer value
- Language
- Department
- Availability


---

# 13. Agent Permission Model


Human operators require:


- Tenant access
- Role permissions
- Department permissions


Example:



Support Agent

Sales Agent

Supervisor

Administrator


---

# 14. AI-to-Human Handoff Types


Supported modes:


## Warm Transfer


AI introduces human:



"Connecting you with Sarah from support."


---

## Silent Transfer


Human joins without interruption.


---

## Callback Request


Human contacts customer later.


---

# 15. Human-to-AI Return


After human interaction:


The conversation may return to AI for:


- Follow-up messages
- Confirmation
- Reminders


---

# 16. Escalation Analytics


Track:


- Escalation rate
- Escalation reasons
- Resolution time
- Human workload
- AI failure patterns


---

# 17. Improvement Feedback Loop


Human escalations become improvement data:



Escalated Conversation

    |

Analysis

    |

Agent Improvement

    |

New Version


---

# 18. Security Considerations


Protect:


- Customer data
- Conversation history
- Human access


Controls:


- Authentication
- Authorization
- Audit logging


---

# 19. Implementation Rules


## Rule 1

Every production agent must define escalation behavior.


---

## Rule 2

Human transfers must preserve context.


---

## Rule 3

Escalation decisions must be observable.


---

## Rule 4

Human access requires permissions.


---

## Rule 5

Escalated conversations should improve future agents.


---

# 20. Consequences


## Positive Consequences


- Better customer experience
- Higher trust
- Safer AI deployment
- Reduced automation failures


---

## Negative Consequences


- Requires human operations
- More workflow complexity
- Additional UI requirements


---

# 21. Future Evolution


Future capabilities:


- AI supervisor agents
- Automatic agent coaching
- Predictive escalation
- AI-assisted human operators
- Multi-agent collaboration


Major changes require new ADRs.


---

# 22. Related Documents


Architecture:


- 09_Voice_Call_Flow.md
- 10_AI_Runtime_Architecture.md
- 13_Agent_Architecture.md
- 19_Service_Communication.md


Related ADRs:


- ADR-0034_AI_Agent_Evaluation_and_Quality_Assurance_Strategy.md
- ADR-0035_AI_Cost_Management_and_Token_Optimization_Strategy.md
- ADR-0029_Product_Tenant_Customization_Strategy.md


---

# Final Statement


The Voice Agent SaaS Platform will implement Human-in-the-Loop escalation as a core capability, combining AI automation with human expertise.

This enables:

- Reliable customer interactions
- Enterprise-ready operations
- Safer AI adoption
- Continuous agent improvement