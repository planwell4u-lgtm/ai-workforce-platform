# AI Workforce Platform

The repository implements the approved V2 AI Workforce Platform architecture.

## Current stage

The first local vertical slice is complete and available for review. It includes protected Support and Sales chat, Front Desk route administration, controlled routing, and the local verification workflow. See the project-status record for delivery evidence and remaining roadmap choices.

## Local workspace pages

After starting the local frontend, open:

- `/` — Planwell landing page and workspace navigation
- `/support` — protected Support chat, controlled voice test, and support routing
- `/sales` — protected Sales chat and consent-based lead request
- `/front-desk-admin` — permission-bound, test-only Front Desk route administration

The Support, Sales, and Front Desk pages require their appropriate Auth0 sign-in permissions. The Front Desk page does not configure live telephone or external handoff providers.

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
