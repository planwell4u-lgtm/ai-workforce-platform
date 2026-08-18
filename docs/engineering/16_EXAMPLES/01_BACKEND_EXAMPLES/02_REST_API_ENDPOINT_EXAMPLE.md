# 02 Rest Api Endpoint Example
# Database Repository Pattern

Version: 2.0

---

# 1. Overview

This document defines the standard Repository Pattern used throughout the Voice Agent SaaS backend.

The repository layer is responsible for abstracting data access from business logic. Services interact with repositories instead of directly accessing the database, ensuring:

- Separation of concerns
- Testability
- Maintainability
- Consistent database access
- Easier migration to new storage technologies

---

# 2. Architecture

```
API Route
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
SQLAlchemy ORM
    │
    ▼
PostgreSQL
```

---

# 3. Responsibilities

Repositories should:

- Execute database queries
- Map ORM models
- Handle pagination
- Support filtering
- Support sorting
- Execute transactions when required
- Return domain objects

Repositories should NOT:

- Perform business logic
- Call external APIs
- Validate permissions
- Send notifications
- Perform authentication

---

# 4. Directory Structure

```
app/

repositories/

    base_repository.py

    agent_repository.py

    user_repository.py

    tenant_repository.py

    conversation_repository.py

    memory_repository.py

    knowledge_repository.py

    call_repository.py
```

---

# 5. Base Repository Example

```python
from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model
    ):
        self.model = model

    def get(
        self,
        db: Session,
        object_id: str
    ):

        return (
            db.query(self.model)
            .filter(
                self.model.id == object_id
            )
            .first()
        )

    def list(
        self,
        db: Session
    ):

        return db.query(self.model).all()

    def create(
        self,
        db: Session,
        obj
    ):

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def delete(
        self,
        db: Session,
        obj
    ):

        db.delete(obj)
        db.commit()
```

---

# 6. Agent Repository Example

```python
from sqlalchemy.orm import Session

from app.models.agent import Agent

from .base_repository import BaseRepository


class AgentRepository(
    BaseRepository[Agent]
):

    def __init__(self):

        super().__init__(Agent)

    def get_by_name(
        self,
        db: Session,
        tenant_id: str,
        name: str
    ):

        return (
            db.query(Agent)
            .filter(
                Agent.tenant_id == tenant_id,
                Agent.name == name
            )
            .first()
        )

    def list_active(
        self,
        db: Session,
        tenant_id: str
    ):

        return (
            db.query(Agent)
            .filter(
                Agent.tenant_id == tenant_id,
                Agent.status == "active"
            )
            .all()
        )
```

---

# 7. Tenant Isolation

Every repository query must enforce tenant isolation.

Example:

```python
.filter(
    Agent.tenant_id == tenant_id
)
```

Never execute queries without tenant filtering unless accessing global system data.

---

# 8. Pagination

Repositories should implement pagination.

Example:

```python
query.offset(offset).limit(limit)
```

Recommended defaults:

- Default page size: 25
- Maximum page size: 100

---

# 9. Filtering

Repositories should support optional filters.

Example:

```python
if status:

    query = query.filter(
        Agent.status == status
    )

if category:

    query = query.filter(
        Agent.category == category
    )
```

---

# 10. Sorting

Allow controlled sorting.

Example:

```python
query.order_by(
    Agent.created_at.desc()
)
```

Never allow arbitrary SQL sorting directly from user input.

---

# 11. Transactions

Simple CRUD operations may commit immediately.

Complex workflows should use explicit transaction management.

Example:

```python
with db.begin():

    repository.create(...)

    repository.update(...)

    repository.insert_log(...)
```

---

# 12. Error Handling

Repositories should:

- Raise database exceptions
- Avoid HTTP exceptions
- Avoid business-specific exceptions

Service layer translates repository exceptions into business errors.

---

# 13. Performance Guidelines

Repositories should:

- Use indexes
- Avoid N+1 queries
- Use eager loading where appropriate
- Limit returned columns
- Paginate large datasets
- Batch updates when possible

---

# 14. Async Repository Pattern

For asynchronous services:

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def get(
    self,
    db: AsyncSession,
    object_id: str
):

    result = await db.execute(...)

    return result.scalar_one_or_none()
```

Use async repositories consistently throughout async services.

---

# 15. Testing

Repository tests should verify:

- CRUD operations
- Tenant isolation
- Filtering
- Sorting
- Pagination
- Transactions
- Constraint handling

Tests should run against a dedicated test database.

---

# 16. Best Practices

Always:

- Keep repositories focused on persistence
- Reuse shared repository methods
- Keep SQL centralized
- Return ORM/domain objects consistently
- Document custom queries

Avoid:

- Business logic in repositories
- HTTP-specific code
- Authentication logic
- Long transaction scopes
- Duplicate query implementations

---

# 17. Summary

The Repository Pattern provides a clean separation between business logic and data access. By standardizing repository implementations across the Voice Agent SaaS platform, the backend remains modular, testable, secure, and easier to maintain as the system scales.