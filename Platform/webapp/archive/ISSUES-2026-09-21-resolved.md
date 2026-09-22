# Test-Ops Console — issues & feedback (v3, archived 2026-09-21)

Everything below was fixed, answered, or explicitly flagged as a real, honest gap during this
round. Superseded by a clean ISSUES.md (v4) — see there for what's still open.

---

## Questions still to do (carried over, not yet resolved)

- **Manual vs. automation coverage %** — blocked on real prerequisite work: TestRail case ↔
  `.robot` test linkage is free-text today (inside a `Documentation` field), not a structured
  tag, and inconsistent across suites. Needs that parsed properly first.
- **Manual-edit-only "observed changes" scoping** — needs either TestRail's `updated_by`/
  `updated_on` per case (not available on the bulk snapshot call `build-stats` uses today), or
  this tool tagging its own pushes so they can be excluded from the diff.
- **Review/approve manual edits inline** — depends on the item above existing first; nothing to
  review/tick yet.
- **Docs ingest status — per-document breakdown** — suite-level last-ingested + pass/fail is
  real now; which *specific file* passed/failed within a run still isn't tracked anywhere.
- **Existing-suite mode needs its own toolset** — real governance decision, not mine to make
  silently: today's `fresh_build` flag only distinguishes "no old suite" from "has one," it
  doesn't model a genuine "just work in this existing suite, skip onboarding" mode (which would
  also let New-suite-from-docs show a real "you're targeting an existing suite, skip this"
  warning). Flag if you want it prioritized.
- **Test provenance — manual vs. Claude-written** — repo/folder/project is already shown per
  test. Whether a test was hand-written vs. generated has no reliable signal to build from today
  (Claude's commits land under George's own git identity) — would need this tool tagging its own
  generated files at write time.

---

## General / branding

### Logo + title centred, stacked
**Status:** fixed — `.logo-row` is now a centred flex column (logo, then title beneath, both centre-aligned).

### Sidebar parent groups as pills/tabs, clearer open/close arrows
**Status:** fixed — group headers now render as a soft rounded background block (pill-like), darkening further on hover/open, with a slightly bigger chevron.

### Full renaming pass
**Status:** fixed — display-only renames via `GROUP_DISPLAY_NAME`/`PIPELINE_DISPLAY_NAME` lookups; real ids untouched, old id shown in parens. Two ambiguities flagged and resolved by picking the first-stated version ("Start"→"Get Started" group / "Check setup" pipeline; "Maintain"→"Maintenance").

### Audit flows — what is it actually auditing?
**Status:** answered — compares `knowledge/flows/{project}-{device}-*.md` (transcribed Overflow UX exports) against the live TestRail suite. Not an uploaded doc, not the same as SIT's `screenflow_map.jsonc` graphs. Made explicit in the pipeline's own gloss.

### Gap Register promoted to its own top-level menu, Project/Device/Common/Bespoke split
**Status:** fixed — own top-level sidebar group; 4-way split as tabs on one page, backed by a real `scope` param on `/api/gap-register` + `_infer_gap_device`. Tested.

### Device GAPs must stay correctly scoped when switching device within a project
**Status:** fixed and tested — `scope=project` stable across device switch; `scope=device` requires both to match.

### Remove new-suite-from-docs from all menus
**Status:** fixed — removed from sidebar, Processes stage grouping, and the "Ungrouped" fallback. Pipeline YAML/backend untouched.

### resolve-gaps: button in Gap Register + moved to Maintain
**Status:** fixed — moved to Maintain/Maintenance; added direct "Resolve gaps →" button on the Gap Register page.

## Suite Health

### Title-row meta as pills, not a paragraph
**Status:** fixed on Suite Health and Gap Register (real meta facts to pill-ify). NOT applied to Processes & Flows/Features/Repo map/Docs — their subtitles are genuine sentences, not facts; flag if you want those cut down into pills anyway.

### Sync button, Arrive colours
**Status:** fixed — "↻ Sync" button re-runs every real live fetch the page does on load.

### Tighten dashboard spacing
**Status:** fixed — global CSS, all pages.

## Processes & Flows

### "How to get started" styled Arrive purple, numbered pills
**Status:** fixed — `stage-featured` class, numbered circular pills reflecting run order.

### Keep processes/flows up to date as the real process evolves
**Status:** answered — already live from `/api/pipelines` → real `.claude/pipelines/*.yaml`. A genuinely new pipeline file still needs adding to `PIPELINE_STAGES`/`GROUPS` or it shows as "Ungrouped."

## Features (now "Knowledge & Feature Files")

### Layout rethink — tree by device/structure
**Status:** partial, real gap flagged — "Group by: Feature / Device type" toggle added (real `device_type` data). The specific named taxonomy (Communication/Signing on/Ticket purchasing) doesn't exist as a field in `Platform/model/features.py` — would need a real curated `area` field, a data-modelling decision, not built. Flag if you want it scoped.

### Common/Bespoke filter toggle
**Status:** fixed — "All / Common only / Bespoke only" segmented toggle.

### Gaps-found filter (superseded)
**Status:** not built — correctly superseded by Gap Register's own tabs.

## Repo map (now "Repo structure & map")

### GitHub-style expandable folder browser
**Status:** fixed — client-side nested tree (`buildFileTreeHTML`), no backend change needed.

## Gap register

### Click a gap → modal with answer form
**Status:** fixed — modal with full text, inferred project/device, inline answer form.

### Sync button: push answered gaps into a re-audit/re-edit pipeline
**Status:** not built, flagged honestly — needs the same pipeline-execution-from-console plumbing every disabled "Run" button is already waiting on.

---

## Start

- Global accordion line order (plain language → files touched → command → tech detail → rest).
  **Status:** fixed, global — `renderStep`'s detail-line order rewritten; applies to every pipeline.
- Rename `preflight`/`fix_ready_items`/`human_setup`.
  **Status:** fixed, all three — new `STEP_DISPLAY_NAME` map, real ids kept in parens.
- List what's required of the human after the check, or mark complete/checked.
  **Status:** flagged, not built — `human_setup`'s real `actions:` list isn't rendered at all today (only `note:` is). Small follow-up, not done since it was implied not asked outright.
- What do `intake`/`route` actually do?
  **Status:** fixed, both — explicit plain-language overrides added from their real `collects:`/`note:` fields; `intake`'s `collects:` also now rendered directly as "Asks you for."

## Ingest Docs

- Global cancel buttons on pipeline runs.
  **Status:** fixed, global — backend (`runner.cancel_run` + `/api/pipelines/runs/{id}/cancel`) already existed, just had no UI button. Added "Cancel run", shown while `running`/`waiting_human`.
- Should `docs_path` be editable?
  **Status:** fixed per George's own suggestion — now read-only, pre-filled from the real resolved target folder; locked with a warning if no target's set yet.

## Onboard suite

- Author area / push area should go one-by-one with a review point between, plus a highlighted warning on Approve & Push.
  **Status:** fixed, real bug found — `author_area`/`push_area` were running as "draft every area, then push every area," not one-by-one. Rewrote `_flatten_steps` (`runner.py`) to interleave consecutive same-`loop:` steps per area; new regression test added. Also added a highlighted warning banner under every Approve & Push gate (in addition to the existing confirm() dialog).
- What is `flow_data_path` for?
  **Status:** answered — optional Overflow UX flow-data JSON export path, feeds `mine_flows`; blank is fine and handled cleanly for from-scratch builds.
