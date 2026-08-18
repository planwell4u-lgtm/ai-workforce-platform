# ADR 003: Repository Pattern

## Context
Decoupling database access logic from business logic (services and controllers) makes testing easier and ensures consistency.

## Decision
All database access will go through a Repository layer, avoiding direct ORM model calls in the service layer.

## Consequences
- Cleaner separation of concerns.
- Consistent patterns for handling transactions and multi-tenant scoping.
