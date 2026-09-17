# Test-Ops Console — issues & feedback (v3)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`

**How to use:** drop a new entry under whichever section you're testing, using this template.
I'll read this file directly, fix what I can, and mark items `Status: fixed`/`answered` with a
one-line note (and commit, once committed).

```
### Short title
**Type:** Bug / UX / UI / Change request
**Severity:** blocker / annoying / nice-to-have / Q+A
**What happened / what you want:** ...
**Expected:** ...
**Status:** open
```

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
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Arrive logo and "Test-Ops Console" title centred at the top, one after the other, not left-aligned in a row.
**Status:** fixed — `.logo-row` is now a centred flex column (logo, then title beneath, both centre-aligned).

### Sidebar parent groups as pills/tabs, clearer open/close arrows
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Parent-level sidebar options (e.g. Overview) should look like pills/tabs with clearer accordion arrows.
**Status:** fixed — group headers now render as a soft rounded background block (pill-like), darkening further on hover/open, with a slightly bigger chevron.

### Full renaming pass
**Type:** UX
**Severity:** nice-to-have
**What happened / what you want:** Rename sidebar groups, pipeline items, and page titles per the full list given (Dashboards, Processes & Flows, Knowledge & Feature Files, Repo structure & map, Get Started, Tools, New Suite Onboarding, Onboard New JIRA, Check Duplication, Automation Hand Off, Write Automated Test Cases, Audit Coverage vs Release, Audit flow maps, Audit Syntax, Defect Steps to Case, Review latest run comments, etc).
**Status:** fixed — display-only renames via `GROUP_DISPLAY_NAME`/`PIPELINE_DISPLAY_NAME` lookups; every real pipeline `id`, slash command, and system-test-ops YAML id is untouched, only the shown label changed (old id shown in parenthesis next to the new name so nothing's hidden). Two real ambiguities found and resolved by picking the first-stated version, flagged rather than silently guessed:
  - "Start" — you wrote both "Start to be changed to Get Started" (the sidebar GROUP) and, as a sub-bullet, "Change Start to Check setup" — read as: group = "Get Started", the `start` pipeline itself within it = "Check setup". If that's not what you meant, say so.
  - "Maintain" — you wrote "Maintenance" in one note and "Health Check" in another, unrelated one. Went with **Maintenance** (matches the Processes tab's existing stage title of the same name). Flag if you actually wanted "Health Check".

### Audit flows — what is it actually auditing?
**Type:** Q+A
**Severity:** nice-to-have
**What happened / what you want:** "What is it auditing? A uploaded doc? Or the SIT flows?"
**Status:** answered — neither, exactly. Per `audit-flows.yaml`'s real inputs, it compares `knowledge/flows/{project}-{device}-*.md` (UX flow maps transcribed from Overflow exports) against the live TestRail suite. That's NOT a doc you upload on the Docs page, and NOT the same thing as SIT's own `screenflow_map.jsonc` graphs shown under Automation → Screen flows — three genuinely different things that share the word "flow." Made this explicit in the pipeline's own plain-language gloss so it's answered on the page itself, not just here.

### Gap Register promoted to its own top-level menu, Project/Device/Common/Bespoke split
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Gap Register as a whole parent sidebar item, reworked with Project GAPs / Device GAPs / Common GAPs / Bespoke GAPs views.
**Status:** fixed, one real design call made: it's now its own top-level sidebar group (no longer nested under Dashboards) — but the 4-way split is implemented as **tabs on one page**, not 4 separate sidebar entries, since they're 4 lenses on the same underlying marker set rather than 4 different destinations. `/api/gap-register` gained a real `scope` param (`project`/`device`/`common`/`bespoke`) backed by a new, honest path-hint device-inference function (`_infer_gap_device`, same style as the existing project one) — tested (`test_gap_register_scope_*` in test_app.py, 4 new passing tests).

### Device GAPs must stay correctly scoped when switching device within a project
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Switching target from Translink/POS to Translink/ETM should leave Project GAPs unchanged but change Device GAPs.
**Status:** fixed and tested — `scope=project` ignores device entirely (stable across a device switch); `scope=device` requires both project AND device to match. `test_gap_register_scope_project_ignores_device_and_stays_stable` proves the stability claim directly against real fixture data, not an assertion of intent.

### Remove new-suite-from-docs from all menus
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** "No need really... just get rid of entirely."
**Status:** fixed — removed from the sidebar Build group, the Processes tab's "How to get started" stage, and its own "Ungrouped" fallback bucket (all three checked, since it would've silently reappeared in the fallback otherwise). The pipeline YAML/backend itself is untouched — only navigation stopped surfacing it.

### resolve-gaps: button in Gap Register + moved to Maintain
**Type:** Change request
**Severity:** nice-to-have
**Status:** fixed — moved from the Audit group into Maintain/Maintenance in both the sidebar and the Processes tab's stage grouping, and added a direct "Resolve gaps →" button on the Gap Register page itself.

## Suite Health

### Title-row meta as pills, not a paragraph
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Keep page titles as they are, but move the meta line (warnings, generated date, etc.) into small pills to the right of the title — global pattern, all pages.
**Status:** fixed on Suite Health and Gap Register (both have real "meta" facts — suite name, generated date, fixture warning, total marker count — to put in pills). NOT applied to Processes & Flows / Features / Repo map / Docs: their subtitle lines are genuine descriptive sentences, not meta-facts, so forcing them into pills would mean inventing fake "facts" to fill pill shapes rather than a real global rollout. Flag if you want those subtitles cut down into pill-shaped facts anyway — that's a content decision, not just styling.

### Sync button, Arrive colours
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** A button to re-sync old vs new comparison, run comments, recent activity — Arrive brand colours.
**Status:** fixed — "↻ Sync" button (purple, `--p1`) next to the title pills; re-runs the exact same live fetches the page does on load (build-stats, run-health, gaps, docs, last-audit, suite comparison, run comments, recent activity) — a real refresh, not a fake spinner.

### Tighten dashboard spacing
**Type:** UI
**Severity:** nice-to-have
**Status:** fixed — reduced `.card` padding/margin and `.stat-row` gap slightly across the whole app (global CSS, not Suite-Health-only, since the same components are reused everywhere).

## Processes & Flows

### "How to get started" styled Arrive purple, numbered pills
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Parent accordion in Arrive purple; sub-items as numbered pills (1st/2nd/3rd) instead of today's style.
**Status:** fixed — `stage-featured` class applied only to that one stage (others unchanged): purple header background, and each pipeline row gets a numbered circular pill (1, 2, 3…) reflecting run order.

### Keep processes/flows up to date as the real process evolves
**Type:** Q+A
**Severity:** nice-to-have
**Status:** answered — this is already how it works structurally: the page reads pipeline data live from `/api/pipelines` (which itself reads system-test-ops' real `.claude/pipelines/*.yaml` on every request) rather than a cached/hand-written list, so a real pipeline change shows up here automatically. No code change needed for that part; what WOULD need action is if you add a genuinely new pipeline file — it needs adding to `PIPELINE_STAGES`/`GROUPS` or it'll surface as "Ungrouped" instead of vanishing (same lesson as `start` and `write-automation` earlier).

## Features (now "Knowledge & Feature Files")

### Layout rethink — tree by device/structure
**Type:** Change request
**Severity:** annoying
**What happened / what you want:** Move away from flat pills+cards toward a tree mirroring device flows/TestRail suite structure (e.g. Communication, Signing on, Ticket purchasing as broad areas, features nested underneath).
**Status:** partial, real gap flagged honestly — added a "Group by: Feature / Device type" toggle that gives a genuine expandable tree (device type → features → variants), because `device_type` is real, already-cited data that does mirror how suites are actually organised (`etm-suite-restructure` etc). The SPECIFIC conceptual-area taxonomy you named (Communication/Signing on/Ticket purchasing) does **not** exist as a field anywhere in `Platform/model/features.py` today — `Feature` only has `key`/`name`/`description`, no broader category. Building that means either adding a real, curated `area` field to the feature registry (a data-modelling decision, not a UI one) or fabricating category names nobody's confirmed, which breaks the no-gap-fabrication rule this whole app runs on. Flag if you want to scope adding that field for real.

### Common/Bespoke filter toggle
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Toggle tabs for Common / Bespoke / device-only / project-only.
**Status:** fixed — "All / Common only / Bespoke only" segmented toggle added alongside the existing project/device filters (which already covered the "device only, project only" half).

### Gaps-found filter (superseded)
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** You noted this might not be needed once Gap Register got its own menu section.
**Status:** not built — correctly superseded. Gap Register's own Project/Device/Common/Bespoke tabs (above) cover this need directly; no separate filter added here to avoid building the same thing twice.

## Repo map (now "Repo structure & map")

### GitHub-style expandable folder browser
**Type:** Change request
**Severity:** nice-to-have
**Status:** fixed — genuinely feasible with existing data, no backend change needed (every file's real path already carries its folder structure). Built a client-side nested tree (`buildFileTreeHTML`): click a folder to expand it, files listed with their real GitHub links inside.

## Gap register

### Click a gap → modal with answer form
**Type:** Change request
**Severity:** nice-to-have
**Status:** fixed — clicking any row in the marker table opens a modal with the full text, inferred project/device, and an inline answer form (question/answer/type/device), posting to the same real `/api/gap-answers` the page-bottom form already used.

### Sync button: push answered gaps into a re-audit/re-edit pipeline
**Type:** Change request
**Severity:** annoying
**What happened / what you want:** A sync button so answered gaps flow into steps-needed/tests-written, via re-auditing and editing existing cases.
**Status:** not built, flagged honestly rather than faked — this is genuinely more than a UI change. `resolve-gaps` (the real pipeline) already exists and does turn GAP/UNCONFIRMED markers into cited facts, but wiring "answered in the console" through to "a pipeline run actually re-audits/edits the case" needs the same pipeline-execution-from-the-console plumbing every disabled "Run" button elsewhere is already waiting on — not something to fake with a spinner here. Real follow-up once that plumbing lands.

---
*(Below this line is where you'd left off typing — kept exactly as you left it.)*

Start
- (global) - the accordions with like code, human, ai - i dolike how you have it a little bit, but maybe a bit more user human language freindly - like a what it does, just langaueg, then a files it touches, with the more heavy file, tech wording, then the command, and report it produces. do this globally for all - needs more like info for each step.
- change preflight to check setup
- fix ready itmes to running installs
- human_setup to Things for you to do
-- here we should also list the things required by human after the check is done right? or just complete, or checked if done.
- what the fuck does the intake bit do here? 
- what does route do here? (hence my reasoning for more info on each one)

Ingest Docs
- Maybe we need globally cancel buttons on the functions, pipelines right as i do not need to continue or do anything with ingest docs anymore should be done, but still there.
- docs path bit does it need to be visible? like why do we get the choice to change path that will just break things right? maybe display the path its going to but not actually allow to change? what do you think here

Onbaord suite
- the author area, and push area i think do one by one, so author area, then approve and push after - so you can review after each one get me? maybe we need to indicate on the bit where it says approve and push, warning highlighted, check this doc pathway once happy, approve and push
- the flow data_path what is this for again? why do we need it

Add feature
- 