# Twilio Outage Failover Runbook

Action plan for when SMS or communication channels fail due to Twilio platform outages.

## Indicators

- High notification delivery failure rates on dashboards.
- Direct status alerts from Twilio API status feeds.

## Action Steps

1. **Verify Status:** Check [status.twilio.com](https://status.twilio.com).
2. **Switch Provider:** If downtime is expected to exceed 30 minutes:
   - Update API keys to target the secondary provider (e.g. MessageBird / AWS SNS) via configuration variables.
3. **Notify Users:** Broadcast status updates on login screen warning of potential SMS OTP delays.
