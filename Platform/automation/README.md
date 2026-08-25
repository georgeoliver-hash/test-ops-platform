# automation-tests

System test automation for Arrive transit/parking devices.

_Repo verified live on GitHub — 2026-08-07. Local folder renamed to match (test-automation-sit) — 2026-08-10._

## New here? Start with one word

Open this folder in Claude Code and type **`/start`**. It runs a readiness check
(`python -m tools.doctor`), tells you what the device/stack still needs, and gets you to a green run.
The 3-minute orientation is in **[ONBOARDING.md](ONBOARDING.md)**.

## Quick start

```powershell
# Install (with all optional deps)
pip install -e ".[all]"

# List discoverable projects
python -m tools.list_projects

# Inventory build artifacts
python -m tools.scan_builds

# Health-check every device in every project
python -m tools.device_health

# Run a project's full suite
robot --variable PROJECT:translink --exclude destructive projects/translink/tests

# Run only auth tests for the active project
robot --variable PROJECT:translink --include feature:auth --exclude destructive projects/translink/tests

# Run a single suite by file
robot --variable PROJECT:translink projects/translink/tests/signon/test_operator_signon.robot
```

## Where things live

- `framework/` — generic infrastructure (transport, UI drivers, BOS client).
- `projects/_common/` — tests shared across projects.
- `projects/<name>/` — project-specific tests + `devices.yaml` registry.
- `builds/` — read-only build artifacts from real devices.
- `tools/` — operational scripts.
- `.claude/agents/` — Claude Code subagents for the test team.
- `docs/architecture.md` — deeper design notes.

See **CLAUDE.md** for the full project model and conventions.
