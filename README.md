# test-ops-platform

Sandbox platform for the system-test-ops / SIT / test-automation-sit build proposal — see the
**AI Boundary Map** artifact for the full reasoning and phased plan. This repo is where that
proposal actually gets built and proven, before any of it goes near `flowbird-group/sit` or
`system-test-ops` for real.

## What's here

- **`model/`** — shared, tool-agnostic schema. `devices.py` and `functions.py` are real and
  working: they parse `sit-mirror/` directly (device taxonomy + function-keyword vocabulary).
  `flows.py` and `provenance.py` are stubs — see their docstrings for what's still open.
- **`sit-mirror/`** — a **one-way, read-only** mirror of two things from `flowbird-group/sit`
  (`EquipmentTypes.json` + `Bindings/*.robot`). Never hand-edited — see `docs/sync-policy.md`.
  Refresh with `python tools/sync_sit_mirror.py --sit-path <path-to-a-local-sit-checkout>`.
- **`testops/`** — a copy of `system-test-ops` as it stood on 2026-08-24/25 (no behaviour changes
  yet — Phase 3/4 will wire its pipelines to read `model/` instead of re-deriving facts).
- **`ai_steps.yaml`** — the AI boundary declaration: every model call this platform makes, by
  name, with a real deterministic fallback. If a model call isn't listed here, it shouldn't exist.
- **`tools/model_demo.py`** — run this after any `sit-mirror/` sync to prove `model/` still holds
  real data end-to-end. `tests/test_model.py` is the same thing as a regression suite.

## Quickstart

```
python -m venv .venv
./.venv/Scripts/pip install -e ".[dev]"     # or: pip install pydantic pytest
python tools/sync_sit_mirror.py --sit-path ../sit
python tools/model_demo.py
python -m pytest tests/
```

## Where this came from

Built following the phased plan in the AI Boundary Map artifact (2026-08-24/25). Phase 0
(scaffold) and the first real slice of Phase 1 (`model/devices.py` + `model/functions.py`,
proven against a live `sit` checkout — 267 real function keywords, 8 Translink device-type
groups) are done as of this commit. Not yet started: `model/flows.py` (needs
`discover_screenflow.py`'s real output shape read first), the `ai_steps.yaml` `--no-ai` CLI
wiring, and both codegen generators.
