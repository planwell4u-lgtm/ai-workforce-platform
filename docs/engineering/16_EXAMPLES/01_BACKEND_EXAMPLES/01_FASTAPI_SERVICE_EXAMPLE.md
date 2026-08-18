# 01 Fastapi Service Example
# FastAPI Service Example

## 1. Overview

This document provides a production-oriented example of implementing a backend service using **FastAPI** for the Voice Agent SaaS platform.

The example demonstrates recommended backend patterns including:

- Project structure
- API routing
- Dependency injection
- Configuration management
- Database integration
- Service layer design
- Error handling
- Logging
- Testing considerations

This example acts as a golden reference for backend developers.

---

# 2. Technology Stack

Example service uses:

| Component | Technology |
|---|---|
| Language | Python 3.13+ |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Migration | Alembic |
| Cache | Redis |
| Logging | Structured Logging |
| Testing | Pytest |

---

# 3. Service Example

Example service:


Agent Management Service


Responsibilities:

- Create AI agents
- Retrieve agent configuration
- Update agent settings
- Validate tenant ownership

---

# 4. Recommended Project Structure


agent-service/

├── app/
│
├── api/
│ ├── routes/
│ │ └── agents.py
│ └── dependencies.py
│
├── core/
│ ├── config.py
│ ├── security.py
│ └── logging.py
│
├── models/
│ └── agent.py
│
├── schemas/
│ └── agent.py
│
├── services/
│ └── agent_service.py
│
├── repositories/
│ └── agent_repository.py
│
├── database/
│ ├── session.py
│ └── migrations/
│
├── tests/
│
└── main.py


---

# 5. Application Entry Point

`main.py`

```python
from fastapi import FastAPI

from app.api.routes import agents
from app.core.logging import configure_logging


configure_logging()

app = FastAPI(
    title="Agent Service",
    version="1.0.0"
)


app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["Agents"]
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
6. Configuration Management

core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str
    REDIS_URL: str

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
7. Database Model Example

models/agent.py

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Agent(Base):

    __tablename__ = "agents"

    id = Column(
        String,
        primary_key=True
    )

    tenant_id = Column(
        String,
        nullable=False
    )

    name = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="active"
    )
8. API Schema Example

schemas/agent.py

from pydantic import BaseModel


class AgentCreate(BaseModel):

    name: str


class AgentResponse(BaseModel):

    id: str
    name: str
    status: str

    model_config = {
        "from_attributes": True
    }
9. Repository Layer

repositories/agent_repository.py

from sqlalchemy.orm import Session

from app.models.agent import Agent


class AgentRepository:


    def create(
        self,
        db: Session,
        agent: Agent
    ):

        db.add(agent)
        db.commit()
        db.refresh(agent)

        return agent


    def get_by_id(
        self,
        db: Session,
        agent_id: str
    ):

        return (
            db.query(Agent)
            .filter(
                Agent.id == agent_id
            )
            .first()
        )
10. Service Layer

services/agent_service.py

from app.models.agent import Agent


class AgentService:


    def __init__(
        self,
        repository
    ):
        self.repository = repository


    def create_agent(
        self,
        db,
        tenant_id,
        name
    ):

        agent = Agent(
            tenant_id=tenant_id,
            name=name
        )

        return self.repository.create(
            db,
            agent
        )
11. API Route Example

api/routes/agents.py

from fastapi import APIRouter
from fastapi import Depends

from app.schemas.agent import AgentCreate
from app.schemas.agent import AgentResponse


router = APIRouter()


@router.post(
    "/",
    response_model=AgentResponse
)
async def create_agent(
    request: AgentCreate
):

    agent = {
        "id": "agent_123",
        "name": request.name,
        "status": "active"
    }

    return agent
12. Dependency Injection Pattern

FastAPI dependencies should provide:

Database sessions
Authentication context
Tenant context
Permissions
External clients

Example:

from fastapi import Depends


async def get_current_tenant():

    return {
        "tenant_id": "tenant_123"
    }
13. Multi-Tenant Enforcement

Every request must validate tenant ownership.

Example:

Request
   |
Authentication
   |
Tenant Resolution
   |
Authorization Check
   |
Service Layer
   |
Database Query

Database queries must always include:

WHERE tenant_id = current_tenant_id
14. Error Handling

Recommended pattern:

from fastapi import HTTPException


if agent is None:

    raise HTTPException(
        status_code=404,
        detail="Agent not found"
    )

Production services should also include:

Error codes
Structured error responses
Correlation IDs
15. Logging Example
import logging


logger = logging.getLogger(__name__)


logger.info(
    "agent_created",
    extra={
        "tenant_id": tenant_id,
        "agent_id": agent.id
    }
)

Logs must include:

Request ID
Tenant ID
User ID
Service name
Operation name
16. Health Endpoints

Every service should expose:

Liveness

Checks process availability.

GET /health/live
Readiness

Checks dependencies.

GET /health/ready

Example:

{
  "database": "healthy",
  "redis": "healthy",
  "status": "ready"
}
17. Testing Example

Example:

def test_create_agent():

    response = client.post(
        "/api/v1/agents",
        json={
            "name": "Support Agent"
        }
    )

    assert response.status_code == 200

Required tests:

Unit tests
API tests
Integration tests
Database tests
18. Production Requirements

A production FastAPI service must include:

Security
Authentication
Authorization
Input validation
Rate limiting
Reliability
Retries
Timeouts
Circuit breakers
Observability
Metrics
Logs
Traces
Deployment
Docker image
Kubernetes manifests
CI/CD pipeline
19. Golden Rules

Backend services must:

Keep business logic outside API routes
Use dependency injection
Separate layers clearly
Validate tenant boundaries
Use async where required
Provide observability
Be independently deployable
20. Conclusion

This FastAPI example represents the recommended backend implementation pattern for the Voice Agent SaaS platform.

All backend services should follow this architecture style to maintain:

Consistency
Scalability
Maintainability
Production reliability