# Production Incident Response Runbook

Standard operating procedures for managing active production outages.

## Severity Levels

- **SEV 1 (Critical):** Core system unavailable (e.g. users cannot log in).
- **SEV 2 (Major):** Critical subsystem failure with no workaround (e.g. billing failures).
- **SEV 3 (Minor):** Non-blocking bugs or minor performance degradation.

## Response Checklist

1. **Acknowledge & Triage:** Confirm receipt of alert in paging tool.
2. **Declare Incident:** Open a Slack war room channel (#incident-YYYY-MM-DD-title) and assign roles (Incident Commander, Communications Lead).
3. **Mitigate:** Apply hotfix, restart services, or roll back deployment.
4. **Post-Mortem:** Schedule root cause analysis (RCA) meeting within 48 hours.
