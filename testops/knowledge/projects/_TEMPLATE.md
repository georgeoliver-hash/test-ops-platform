# Project: <Name>

Copy this file to `knowledge/projects/<project>.md` and fill it in. Human-curated facts the agents
load before reasoning about this project — the source of truth for things the TestRail/JIRA data
doesn't make obvious. Mark anything unknown as `TODO`; agents must treat unknowns as unknown, never
guess.

## Inputs provided (audit-first — list what you have; gaps = lower confidence)
- Old suite/cases: `<TestRail access? suite ids?>` · Requirements/specs: `<docs/links?>`
- UX/design flows + flow-data JSON: `<in knowledge/flows/?>` · Defect history: `<tracker + section?>`
- Device brief / terminology: `<source?>` · Links: `<dashboards/boards/design?>`

## TestRail
- **Project:** `<TestRail project name>` — **id `<n>`** (set `TESTRAIL_PROJECT_ID=<n>` in `.env`).
- **Case schema (`defaults:` for push):** run `discover-fields --project <n> --sample-case <id>`
  and paste the suggested block here (template_id + required custom fields — project-specific).
- **Suites:**
  - **`<old suite name>`** — id `<n>`. SOURCE, **read-only**. Never modify/delete; only copy out.
  - **`<new suite name>`** — id `<n>`. TARGET. All new/copied/rewritten cases land here.

## Operating modes / configurations  (delete if the device has none)
- Modes: `<e.g. NIR, Ulsterbus, Metro>`. Most behaviour is identical → write once as `@mode(all)`,
  run via TestRail Configurations. List the areas that genuinely **diverge** per mode here.

## Requirements & defects (traceability)
- **Requirement refs:** prefix `<e.g. REQ->` — the primary coverage signal (in the case Refs field).
- **Defect tracker:** prefix `<e.g. TIBU->` — where past bugs live; pin each fixed bug via Refs.
- **Where the bug backlog lives:** `<e.g. a "Confirmation Tests" section / defect-linked cases>`.

## Devices in scope
- `<DEVICE>` — see `knowledge/devices/<device>.md`.

## What "covered" means here
- `<project-specific definition — e.g. a bug is covered only when a case would catch the regression>`.

## Cross-references
- `<links to sibling automation repos, specs, design files, dashboards>`.
