# Threat Model

Threat model definition and mitigations for application assets.

## Core Assets
- User Credentials (Passwords, API Keys).
- Conversation Data & PII.
- Integration Credentials (LLM Provider API Keys).

## Mitigations

| Threat | Target Asset | Mitigation Strategy |
| :--- | :--- | :--- |
| SQL Injection | DB / User Data | Use ORM parameterization exclusively |
| Token Theft | JWT Session | Short expiration, secure HTTP-only cookies |
| Data Breach | LLM API Keys | Envelope encryption with AWS KMS / HashiCorp Vault |
