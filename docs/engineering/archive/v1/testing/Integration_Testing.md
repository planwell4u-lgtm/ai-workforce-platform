# Integration Testing

Guidelines for writing and running integration tests.

## Purpose

Validate interaction interfaces between application modules, databases, message queues, and external APIs.

## Tooling & Environment

- **Docker Compose:** Spun up dynamically in CI/CD to provide realistic dependency environments (e.g., PostgreSQL, Redis).
- **Test Database:** Ensure database migrations are run against clean test schemas before executing tests.
- **Cleanup:** Drop schemas or truncate tables after each integration test suite to prevent side-effects.
