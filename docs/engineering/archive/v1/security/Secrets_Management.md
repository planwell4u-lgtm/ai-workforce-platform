# Secrets Management Policy

How credentials and configuration secrets are safely stored and accessed.

## Principles

1. **No Plaintext Secrets:** Secrets must never be committed to version control.
2. **Environment Ingestion:** Ingest secrets as environment variables provided by container orchestration.

## Production Storage

- Production secrets are managed securely using **HashiCorp Vault** or cloud-native secrets managers (e.g. AWS Secrets Manager).
- Access to production secrets requires authentication IAM roles.
