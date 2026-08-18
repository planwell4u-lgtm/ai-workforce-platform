# ADR-0017: Memory Architecture Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Memory Architecture Strategy  
**ADR Number:** ADR-0017  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will implement a multi-layer memory architecture to provide AI agents with short-term conversational context and long-term business knowledge.

The approved memory architecture uses:


| Memory Type | Technology | Purpose |
|---|---|---|
| Short-Term Memory | Redis | Active conversation state |
| Long-Term Memory | PostgreSQL | Persistent business memory |
| Semantic Memory | PostgreSQL + pgvector | Similarity-based retrieval |
| Session Memory | Agent Runtime State | Current execution context |
| Knowledge Memory | RAG System | Document-based knowledge |


The memory architecture follows:



Conversation

  |

Short-Term Memory

  |

AI Runtime

  |

Long-Term Memory

  |

RAG Knowledge System



---

# 2. Context


AI agents require memory to maintain useful conversations.


Without memory:



User:

"I want to book an appointment"

Agent:

"What appointment?"



With memory:



User:

"I want to book an appointment"

Agent:

"Sure, what date would you prefer?"



The platform requires memory for:


- Conversations
- Customer preferences
- Business context
- Historical interactions
- Knowledge retrieval


---

# 3. Problem Statement


The platform must solve:


## Conversation Continuity


Agents need awareness of previous messages.


---

## Customer Understanding


Agents should remember:


- Customer details
- Previous requests
- Preferences


---

## Business Knowledge


Agents need access to:


- Documents
- Policies
- FAQs
- Procedures


---

## Multi-Tenant Isolation


Memory must never cross tenants.


Example:



Tenant A Memory

    X

Tenant B Memory



---

# 4. Memory Architecture Goals


The memory system must provide:


## Fast Access


Active conversations require millisecond retrieval.


---

## Persistent Storage


Important information must survive sessions.


---

## Semantic Retrieval


Agents should find relevant information by meaning.


---

## Privacy Control


Customers control:


- Retention
- Deletion
- Access


---

# 5. Options Considered


---

# Option 1: Store Everything in Database


Architecture:



PostgreSQL

|

All Memory



## Advantages


- Simple


## Disadvantages


- Slow for active conversations
- Poor real-time performance


## Decision

Rejected.


---

# Option 2: Store Everything in Vector Database


Architecture:



Vector Database

   |

All Memory



## Advantages


- Good semantic search


## Disadvantages


- Poor transactional data handling
- Difficult business queries


## Decision

Rejected.


---

# Option 3: Multi-Layer Memory Architecture


Architecture:



Redis

PostgreSQL

pgvector

RAG



## Advantages


- Fast
- Flexible
- Production ready


## Decision

Accepted.


---

# 6. Final Memory Architecture


              AI Agent


                 |


          Memory Manager


                 |


   ----------------------------


   |             |            |

Session Long-Term Semantic

Redis PostgreSQL pgvector

                 |


          Knowledge System


---

# 7. Short-Term Memory


## Purpose


Maintain active conversations.


Technology:



Redis



---

## Stores


Examples:



Current conversation

Current workflow state

Temporary variables

Active call context



---

## Lifecycle


Created:



Conversation Started



Updated:



Every interaction



Removed:



Session Completed



---

# 8. Long-Term Memory


## Purpose


Store persistent information.


Technology:



PostgreSQL



---

## Examples


Customer information:



Name

Preferences

Previous interactions

Business history



---

# 9. Semantic Memory


## Purpose


Enable meaning-based retrieval.


Technology:



PostgreSQL + pgvector



---

## Examples


User asks:



"What did we discuss last month?"



System retrieves:



Similar previous conversations



---

# 10. Memory Data Model


Example:



memory

|

id

tenant_id

customer_id

agent_id

memory_type

content

embedding

created_at

updated_at



---

# 11. Memory Flow


When user speaks:



User Message

  |

Memory Retrieval

  |

Relevant Context

  |

AI Runtime

  |

LLM

  |

Response

  |

Memory Update



---

# 12. Memory Manager Service


A dedicated Memory Manager controls:


## Storage


Where memory is stored.


---

## Retrieval


What information is loaded.


---

## Policies


What can be remembered.


---

## Retention


How long information exists.


---

# 13. Memory Policies


Each agent defines:


## What To Store


Examples:


- Customer preferences
- Important facts
- Business information


---

## What Not To Store


Examples:


- Sensitive temporary data
- Unnecessary conversation details


---

## Retention Period


Examples:



30 days

1 year

Permanent



---

# 14. Multi-Tenant Memory Isolation


Every memory record requires:



tenant_id



Example:



Tenant A

Customer Memory

Tenant B

Customer Memory



These must remain isolated.


---

# 15. Agent Memory Strategy


Different agents use different memory policies.


Example:


## Reception Agent


Stores:


- Customer identity
- Previous appointments


---

## Sales Agent


Stores:


- Customer interests
- Buying stage


---

## Support Agent


Stores:


- Previous issues
- Solutions provided


---

# 16. RAG Relationship


Memory and RAG serve different purposes.


## Memory


Answers:


"What do we know about this user?"


---

## RAG


Answers:


"What does the company know?"


---

Example:


Memory:



Customer prefers morning appointments



RAG:



Company appointment policy



---

# 17. Security Requirements


Memory requires:


- Tenant isolation
- Encryption
- Access controls
- Audit logging
- Retention enforcement


---

# 18. Performance Requirements


The system should optimize:


## Retrieval Speed


Fast access for active calls.


---

## Context Size


Avoid sending unnecessary data to LLM.


---

## Memory Ranking


Return most relevant information.


---

# 19. Implementation Rules


## Rule 1

Never mix tenant memory.


---

## Rule 2

Memory requires explicit policies.


---

## Rule 3

Do not store unnecessary information.


---

## Rule 4

All memory access must be observable.


---

## Rule 5

Memory retrieval must respect permissions.


---

# 20. Consequences


## Positive Consequences


- Better conversations
- Personalized agents
- Improved customer experience
- More intelligent automation


---

## Negative Consequences


- Additional storage complexity
- Privacy responsibilities
- Memory management overhead


---

# 21. Future Evolution


Future capabilities:


- Adaptive memory
- User-controlled memory
- AI memory summarization
- Memory analytics
- Cross-channel memory


Major changes require new ADRs.


---

# 22. Related Documents


Architecture:


- 12_Memory_Architecture.md
- 11_RAG_Architecture.md
- 10_AI_Runtime_Architecture.md


Related ADRs:


- ADR-0005_AI_Runtime_Architecture.md
- ADR-0006_RAG_Vector_Storage_Strategy.md
- ADR-0016_Agent_Platform_Strategy.md


---

# Final Statement


The Voice Agent SaaS Platform will implement a multi-layer memory architecture using Redis, PostgreSQL, pgvector, and RAG integration.

This provides:

- Real-time conversational memory
- Persistent customer context
- Semantic knowledge retrieval
- Secure multi-tenant AI experiences