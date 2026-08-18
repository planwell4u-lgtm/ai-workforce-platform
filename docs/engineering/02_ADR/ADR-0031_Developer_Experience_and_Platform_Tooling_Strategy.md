# ADR-0031: Developer Experience and Platform Tooling Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Developer Experience and Platform Tooling Strategy  
**ADR Number:** ADR-0031  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will implement a developer experience (DX) strategy focused on making development, testing, deployment, and extension of the platform efficient and consistent.

The developer platform will provide:

- Standard development environments
- Local platform setup
- Shared tooling
- Documentation systems
- SDKs
- Development automation
- Testing utilities
- Internal platform libraries


Architecture:


                Developer


                     |


          Developer Platform Layer


                     |

| | | |

Tools SDKs Docs Automation

| | | |

          Platform Services


---

# 2. Context


The Voice Agent SaaS Platform contains many engineering domains:



Frontend

Backend

AI Runtime

Voice Infrastructure

RAG Pipeline

Database

Infrastructure

Security

Operations



Without a strong developer experience, the platform becomes difficult to maintain as the engineering team grows.

---

# 3. Problem Statement


The platform must enable developers to:


## Build Quickly


Developers need reliable local environments.


---

## Understand Systems


Complex architecture requires clear documentation.


---

## Test Safely


Changes must be validated before production.


---

## Extend Easily


New features should follow standard patterns.


---

# 4. Developer Experience Goals


The strategy provides:


## Consistency


All developers use standard workflows.


---

## Productivity


Reduce repetitive tasks.


---

## Quality


Encourage best engineering practices.


---

## Scalability


Support larger engineering teams.


---

# 5. Options Considered


---

# Option 1: Individual Developer Setup


Approach:



Each Developer

Creates Own Environment



## Advantages


- Flexible


## Disadvantages


- Environment differences
- More debugging


## Decision

Rejected.


---

# Option 2: Documentation Only


Approach:



Developer Guide

    |

Manual Setup



## Advantages


- Simple


## Disadvantages


- Setup errors
- Slow onboarding


## Decision

Rejected.


---

# Option 3: Standard Developer Platform


Approach:



Standard Tools

Automation

Documentation



## Advantages


- Faster onboarding
- Better consistency
- Easier scaling


## Decision

Accepted.


---

# 6. Final Developer Platform Architecture


             Developer


                 |


          Development Tools


                 |

| | | |

Local Dev CLI Tools SDKs Documentation

| | | |

         Platform Environment


---

# 7. Development Environment Strategy


The platform provides:


## Frontend Environment


Technology:



Next.js

React

TypeScript

Tailwind



---

## Backend Environment


Technology:



Python

FastAPI

PostgreSQL

Redis



---

## AI Runtime Environment


Technology:



LangChain

LangGraph

LiveKit Agents

Model Providers



---

# 8. Local Development Strategy


Developers should run:



Frontend

Backend

Database

Redis

Voice Services

AI Workers



Using:


- Docker
- Compose environments
- Local configuration templates


---

# 9. Developer Tooling


Required tools:


## Source Control



Git

GitHub/Git Platform



---

## Package Management


Frontend:



pnpm



Backend:



Python package manager



---

## Containers



Docker

Docker Compose



---

## Infrastructure



Terraform

Kubernetes Tools



---

# 10. Internal SDK Strategy


The platform provides reusable libraries.


Examples:



Authentication SDK

Tenant SDK

Agent SDK

Voice SDK

Event SDK



Benefits:


- Consistency
- Faster development
- Reduced duplication


---

# 11. Documentation Strategy


Documentation includes:


## Architecture Docs


Examples:


- System architecture
- Service boundaries
- Data models


---

## API Documentation


Includes:


- OpenAPI specifications
- Examples
- Authentication details


---

## Developer Guides


Includes:


- Setup instructions
- Coding standards
- Deployment guides


---

# 12. CLI Platform Tools


Future platform CLI:


Example:



voice-agent create

voice-agent deploy

voice-agent test

voice-agent logs



Capabilities:


- Create agents
- Validate configuration
- Manage environments


---

# 13. Testing Developer Experience


Developers receive:


- Local test tools
- Mock services
- Sample agents
- Test data


---

# 14. Golden Examples Strategy


Maintain reference implementations:


Examples:



Reception Agent Example

Sales Agent Example

Booking Agent Example

RAG Example

Tool Integration Example



---

# 15. Development Standards


All projects follow:


## Code Standards


- Formatting
- Linting
- Type checking


---

## Architecture Standards


- Service boundaries
- API contracts
- Documentation requirements


---

## Security Standards


- Secret handling
- Access control


---

# 16. Developer Onboarding


New developers should complete:



Environment Setup

    |

Run Platform Locally

    |

Understand Architecture

    |

Deploy Example Service

    |

Create Feature



---

# 17. Platform Engineering Principles


## Principle 1


Automate repetitive work.


---

## Principle 2


Provide self-service tools.


---

## Principle 3


Document decisions.


---

## Principle 4


Prefer reusable components.


---

## Principle 5


Maintain developer productivity.


---

# 18. Implementation Rules


## Rule 1

Every service requires documentation.


---

## Rule 2

Local development must be reproducible.


---

## Rule 3

Common functionality should become shared tooling.


---

## Rule 4

Developers should not manually perform repetitive operations.


---

## Rule 5

Architecture decisions must be documented.


---

# 19. Consequences


## Positive Consequences


- Faster development
- Easier onboarding
- Higher code quality
- Better collaboration


---

## Negative Consequences


- Initial tooling investment
- Maintenance requirements
- More standards to follow


---

# 20. Future Evolution


Future capabilities:


- Internal developer portal
- Automated environment creation
- AI coding assistants
- Platform marketplace
- Self-service extension development


Major changes require new ADRs.


---

# 21. Related Documents


Architecture:


- 04_Component_Architecture.md
- 05_Service_Boundaries.md
- 15_Deployment_Architecture.md


Related ADRs:


- ADR-0028_Platform_Extensibility_Strategy.md
- ADR-0020_CI_CD_Strategy.md
- ADR-0021_Testing_Strategy.md


---

# Final Statement


The Voice Agent SaaS Platform will provide a strong developer experience through standardized tools, automation, documentation, and reusable platform capabilities.

This enables:

- Faster engineering velocity
- Easier platform growth
- Higher development quality
- Long-term maintainability