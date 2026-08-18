# Unit Testing

Guidelines and best practices for writing unit tests.

## Frameworks & Tools

- **Backend:** `testing` package (Go) / `jest` (JavaScript/TypeScript) / `pytest` (Python)
- **Frontend:** `jest` + `@testing-library/react` (or equivalent framework tools)

## Writing Clean Unit Tests

- **Isolate:** Mock external network and database calls.
- **AAA Pattern:** Structure tests using *Arrange, Act, Assert*.
- **Naming Conventions:** Use clear, descriptive test names, e.g., `TestUserLogin_Success` or `describe('User Login validation')`.
