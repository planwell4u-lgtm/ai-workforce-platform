# Database Restore Runbook

Steps for performing manual restoration of the database from backup snapshots.

## Prerequisite

Identify target backup ID or date-time snapshot in AWS RDS / Cloud dashboard.

## Restoration Steps

1. **Stop Application Traffic:** Scale down application deployment replicas to `0` to prevent write attempts.
2. **Launch Restore:** Initiate restore command using cloud provider console or CLI tool.
3. **Verify Integrity:** Connect to restored instance locally and run verification checks on tables.
4. **Update Connection String:** Point application environment variables to new DB instance.
5. **Resume Traffic:** Scale deployment replicas back to active state.
