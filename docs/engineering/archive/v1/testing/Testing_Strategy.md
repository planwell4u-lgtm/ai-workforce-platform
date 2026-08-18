# Testing Strategy

This document outlines the testing methodologies, frameworks, goals, and standards across the codebase.

## Testing Pyramid

We adhere to the classic testing pyramid structure:
1. **Unit Tests (Base):** Validate individual functions, components, and classes in isolation.
2. **Integration Tests (Middle):** Validate how multiple components/services work together (e.g., API database connections).
3. **End-to-End & Load Tests (Apex):** Ensure system-wide scenarios and high-volume performance meet SLAs.

## Test Standards

- **Coverage Goal:** At least 80% code coverage on core logic.
- **Automation:** Every Pull Request runs tests via CI/CD before merge.
- **Reporting:** Failing tests block the release pipeline.
