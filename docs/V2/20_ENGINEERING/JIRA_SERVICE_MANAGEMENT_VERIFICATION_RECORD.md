# Jira Service Management Verification Record

**Date:** 2026-08-16  
**Status:** Verified

## Configured Boundary

- Jira Cloud site: `workforai.atlassian.net`
- Cloud ID: `1f6e234e-2b80-4958-9f4a-80d52248a2a5`
- Service desk ID: `67`
- Request type ID: `69`
- Dedicated service account assigned the Service Desk Team role.
- Scoped service-account token uses only `read:jira-user`, `read:servicedesk-request`, and `write:servicedesk-request`.

## Verification

- A read-only request-type permission check succeeded through Atlassian's API gateway.
- A labeled staging verification request was created successfully: `CS-2`.

## Follow-up

- Close `CS-2` after visual confirmation in Jira.
- Implement the Jira adapter in the running backend before enabling customer-facing ticket creation.
- Keep the API token only in ignored local/deployment secret configuration.
