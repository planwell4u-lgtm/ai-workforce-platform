# Local Runtime Restart and Verification Runbook

**Status:** Verified local procedure
**Scope:** Backend, frontend, local LiveKit sandbox, and the safe staging check

## Prerequisites

- Docker Desktop is installed and running.
- `.env` exists locally and has the required Auth0, Supabase, FAQ, and support
  tenant settings.
- `PGSSLMODE=require` is present in `.env` for the Supabase PostgreSQL pooler.
- Auth0 allows `http://localhost:8765/callback` for the interactive staging
  verifier.

## Start the local runtime

From the repository root, start the verified local LiveKit sandbox if it is not
already running:

```powershell
docker start ai-workforce-livekit-sandbox
```

Load the local configuration into the current PowerShell session before
starting the backend. This avoids putting credentials in source code or command
history.

```powershell
Get-Content .env | ForEach-Object {
  $line = $_.Trim()
  if ($line -and -not $line.StartsWith('#')) {
    $separator = $line.IndexOf('=')
    if ($separator -gt 0) {
      Set-Item -Path "Env:$($line.Substring(0, $separator).Trim())" -Value $line.Substring($separator + 1).Trim()
    }
  }
}
uv run --no-sync python -m ai_workforce_backend.server
```

In a second terminal, start the frontend:

```powershell
Set-Location apps/frontend
npx vinext dev
```

The frontend is available at `http://localhost:3000`; backend health is at
`http://localhost:8080/healthz`.

## Verify local readiness

Run the non-authenticated preflight from the repository root:

```powershell
uv run --no-sync python scripts/check_local_runtime.py
```

It checks only backend health and frontend runtime configuration. It does not
send user data or access a token.

## Run the protected staging check

Use a separate terminal with the local environment variables loaded. The
runner opens Auth0 sign-in, performs one approved FAQ request, and writes a
non-secret result file.

```powershell
uv run --no-sync python scripts/run_staging_ticket_flow.py `
  --client-id $env:AUTH0_CLIENT_ID `
  --result-file "$env:TEMP\ai-workforce-staging-check.json"
```

Complete sign-in and consent in the browser. A successful result contains the
approved FAQ answer and non-secret correlation references; it never records an
access token.

## Stop and recover

- Stop the frontend and backend with `Ctrl+C` in their respective terminals.
- Stop an active browser voice session before signing out or closing the page;
  confirm the UI says the microphone is no longer shared.
- Keep the LiveKit sandbox running for local development, or stop it with
  `docker stop ai-workforce-livekit-sandbox` when it is no longer needed.

If backend startup cannot connect to Supabase, verify `PGSSLMODE=require` is
present in `.env`, then restart the backend. Do not replace the configured
Supabase URL with a local database without an approved migration and recovery
plan.
