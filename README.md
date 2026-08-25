# test-ops-platform

Sandbox for the merge target: **`flowbird-group/sit`** gets a new **`Platform/`** folder nesting
system-test-ops, test-automation-sit, and the shared schema together. Team's aligned on the
direction (2026-08-25); this repo is where it gets built and proven **before** that merge happens
— nothing here touches the real `sit` repo yet.

The `Platform/` folder in this repo IS the eventual merge payload — same relative layout it'll have
once it's nested inside `sit/`. Everything else at this repo's root (`sit-mirror/`,
`tools/sync_sit_mirror.py`, `docs/sync-policy.md`) is sandbox-only scaffolding that goes away once
`Platform/model/` can read SIT's real files directly, in the same repo, instead of a mirror.

See the **AI Boundary Map** artifact for the full reasoning/phased plan.

## What's here

```
test-ops-platform/
├── Platform/                  <- THE MERGE PAYLOAD — drops into sit/Platform/ as-is
│   ├── model/                 <- shared schema: devices.py + functions.py are real & working
│   ├── testops/               <- system-test-ops, copied as-is (no behaviour change yet)
│   ├── automation/             <- test-automation-sit, copied as-is (builds/ + firmware artifacts
│   │                              excluded — reference JSON/code only, see below)
│   ├── tools/model_demo.py    <- proves model/ holds real data end-to-end
│   ├── tests/test_model.py    <- same thing, as a regression suite (6 passing)
│   ├── ai_steps.yaml          <- the AI boundary declaration — 5 named steps, real fallbacks
│   └── pyproject.toml         <- self-contained: this folder alone is a working Python project
├── sit-mirror/                <- SANDBOX ONLY — one-way mirror, see docs/sync-policy.md
├── tools/sync_sit_mirror.py   <- SANDBOX ONLY — refreshes sit-mirror/
└── docs/sync-policy.md        <- SANDBOX ONLY — the one-way-mirror rule
```

`model/devices.py` and `model/functions.py` resolve their source root via `SIT_SCHEMA_ROOT` (env
var) or default to `sit-mirror/`. Post-merge, that default becomes SIT's real
`Resources/Common/ConfigSets/` and `Resources/Devices/` directly — one line changes, nothing else.

`Platform/automation/` had its `builds/` (579MB of SD-card firmware dumps), `artifacts/pkn_sw`,
run logs, and ramdisk images excluded on copy — those are reference data pulled from real devices,
not code, and don't belong in git history. The JSON reference files that matter for schema work
(`pos_apk_metadata.json`, `bsp_inventory.json`, etc.) are kept.

## Quickstart

```
python -m venv .venv
./.venv/Scripts/pip install -e "./Platform[dev]"     # or: pip install pydantic pytest
python tools/sync_sit_mirror.py --sit-path ../sit
./.venv/Scripts/python Platform/tools/model_demo.py
./.venv/Scripts/python -m pytest Platform/tests/
```

## Where this came from

Built following the phased plan in the AI Boundary Map artifact (2026-08-24/25). Phase 0 (scaffold)
and the first real slice of Phase 1 (`model/devices.py` + `model/functions.py`, proven against a
live `sit` checkout — 267 real function keywords, 8 Translink device-type groups) are done.
Restructured 2026-08-25 into the `Platform/` layout once the merge-into-`sit` direction was
confirmed, and `test-automation-sit` was pulled in alongside `testops/` for the same reason.

Not yet started: `model/flows.py` (needs `discover_screenflow.py`'s real output shape read first),
the `ai_steps.yaml` `--no-ai` CLI wiring, and both codegen generators. Not yet decided: exactly when
`Platform/` actually moves into a `sit` branch, and who reviews that PR.
