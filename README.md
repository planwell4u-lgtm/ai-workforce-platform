# AI Workforce Platform

The repository implements the approved V2 AI Workforce Platform architecture.

## Current stage

Engineering Foundation (B0) is complete. This baseline establishes workspace boundaries, safe configuration, automated structural checks, and CI. It intentionally contains no product behavior, provider integration, database access, or credentials. The next task is B1: tenant-aware identity and protected API entry.

## Workspace

```text
apps/             Deployable application entry points
packages/         Narrow shared technical libraries
protocols/        Versioned public API and event contracts
config/           Safe configuration examples and references
infrastructure/   Environment and delivery definitions
tests/            Cross-boundary and end-to-end assurance
scripts/          Local quality and workspace checks
docs/             Approved architecture and delivery records
```

## Local checks

Python 3.12 or later is required. Run the foundation checks with:

```powershell
python -m pip install -e ".[dev]"
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m unittest discover -s tests -v
python scripts/check_workspace.py
python scripts/check_local_runtime.py
```

`check_local_runtime.py` verifies only local backend health and frontend runtime
configuration; it does not send customer data or use an access token. Run
`scripts/run_staging_ticket_flow.py` separately for the interactive,
authenticated staging check.

For the verified startup, recovery, and staging-verification procedure, see
`docs/V2/20_ENGINEERING/LOCAL_RUNTIME_RESTART_AND_VERIFICATION_RUNBOOK.md`.

Do not place secrets in this repository. Copy `config/local.env.example` to `config/local.env` only for local use, then supply values through an approved secret manager when services are introduced.

## Authoritative guidance

- `docs/V2/20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `docs/V2/20_ENGINEERING/02_ENGINEERING_WORKSPACE_AND_MODULE_STRUCTURE.md`
- `docs/V2/00_CONTROL/10_PROJECT_STATUS.md`
