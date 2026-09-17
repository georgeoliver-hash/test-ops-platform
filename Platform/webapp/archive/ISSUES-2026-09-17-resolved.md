# Test-Ops Console — issues & feedback (v2)

The previous round is archived at `archive/ISSUES-2026-09-resolved.md` — everything in it was
fixed or answered. This is a clean sheet, sectioned to match the app's actual sidebar/page
structure, plus every genuinely open item carried forward from the old file (tightened into
bullets, nothing new invented).

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

## General / onboarding gating

### Overview should only show what's usable pre-setup
**Type:** Change request
**Severity:** annoying
**What happened / what you want:** When there are no credentials, no docs, nothing set up yet, only show Overview-level items, and make Start (and only Start) non-faded/clickable — everything else faded until real.
**Expected:** A genuinely gated first-run state, testable end to end.
**Status:** fixed — already built (found live, not previously known to be done): `GATED_GROUP_IDS = ['navBuild','navAudit','navMaintain']` + `/api/setup-status`, with Start deliberately excluded so onboarding is never blocked. Found and fixed one real bug in it: `.setup-gated` was toggled on the group element but had zero CSS rule, so only individual nav items visually dimmed, not the group label itself — added the missing rule.

### Automation should stay visible even pre-setup
**Type:** UX
**Severity:** nice-to-have
**What happened / what you want:** Automation section shouldn't be hidden by the same gating as above.
**Expected:** Automation visible regardless of setup state.
**Status:** fixed — already built. Automation is its own top-level console tab (`tabAutomation`), entirely separate from `GATED_GROUP_IDS`; never gated.

## General UI/UX (layout, sidebar, branding)

### Arrive logo — bigger again
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Logo was sized up once already (22px→36px) but still wanted bigger, top left.
**Expected:** Larger logo, still fits the sidebar cleanly.
**Status:** fixed — 48px → 60px.

### Sidebar hierarchy — sizing + Overview as an accordion
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** Main sidebar items (Overview, Start, Audit) should be ~3px bigger/bolder than accordion sub-items. Consider making Overview itself an accordion containing Suite Health / Processes / Features / Repo map / Gap register underneath.
**Expected:** Clear visual hierarchy between top-level nav and sub-pages.
**Status:** fixed — already built. Group labels are 16.5px/weight 600, sub-items 13.5px (exactly a 3px step), and Overview is already `<div class="navgroup collapsible open" id="navOverview">` wrapping Suite health/All processes/Features/Repo map/Gap register.

### Settings/Docs placement
**Type:** UX
**Severity:** nice-to-have
**What happened / what you want:** Move Settings/Docs lower, nearer the username — or make clicking the username open a small menu with Docs/Settings in it.
**Expected:** Less top-of-sidebar clutter.
**Status:** fixed — already built. Clicking the username (`userMenuBtn`) opens exactly this popup with Docs/Settings.

### Console title styling
**Type:** UI
**Severity:** nice-to-have
**What happened / what you want:** "Test-ops console" title under the Arrive logo should match the logo's style, or at least be bolder/more distinct.
**Expected:** Title reads as a proper product name, not default text.
**Status:** fixed — bumped 13px/weight 600 → 14.5px/weight 700, solid white instead of the dimmer sidebar-ink tone, for more separation from the nav labels below it.

## Suite Health

### Last-run timestamps per function
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Show blocks with date/time of the last time each function ran (add-feature, audit, suite update, etc.) — not just one generic "last run" line.
**Expected:** Per-function last-run visibility.
**Status:** fixed — new "Recent activity" card on Suite Health, one row per key function (ingest-docs, onboard-suite, add-feature, consolidate, audit, export-automation), each pulling its real last-run status/timestamp from the already-existing generic `/api/pipelines/{id}/last-run` endpoint (previously only ever called for `audit`).

### Manual vs automation coverage %
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Add coverage percentage split (manual vs automated), plus a "blocked" count for new vs old suite.
**Expected:** Real computed %, not a guess.
**Status:** not built — still genuinely blocked. TestRail case ↔ `.robot` test linkage today is free text inside a `Documentation` field (e.g. "TestRail C4099912, suite 30253"), not a structured tag, and isn't consistent across suites. Computing a real % needs that mapping parsed properly first — real prerequisite work, not a quick add.

### Manual-edit-only "observed changes" scoping
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** "Observed changes since last audit" should only reflect manual TestRail edits by humans, not this tool's own pushes.
**Expected:** Diff excludes the tool's own writes.
**Status:** not built — still genuinely blocked. Needs either TestRail's `updated_by`/`updated_on` per case (only on `get_case`, not the bulk snapshot call `build-stats` uses today) or this tool tagging its own pushes so they can be excluded from the diff.

### Review/approve manual edits inline
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** A way to review flagged manual edits and tick "okay, that's fine."
**Expected:** Depends on the manual-vs-automated distinction above existing first.
**Status:** not built — depends on the item above; nothing to review/tick yet.

### Docs ingest status card
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Show doc name, ingested pass/fail, last ingested date/time — reflecting that docs get reduced into knowledge files, not just stored raw.
**Expected:** Real per-doc ingest status.
**Status:** partial — the new "Recent activity" card (above) now gives a real suite-level "last ingested" timestamp + pass/fail via `ingest-docs`'s last-run. Per-*document* status (which specific file passed/failed) still isn't tracked anywhere — `tools/ingest_docs.py` prints a kept/failed count but the console doesn't parse or store it per filename. Real follow-up if you want it broken down per doc, not just per run.

## Start

### "Already set up" green state
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** When a user has credentials + full setup done, show a tick + a highlighted "you're all set" state on the page instead of leaving it looking incomplete.
**Expected:** Clear visual confirmation setup is done.
**Status:** fixed — the Start pipeline's detail page now shows a green "✓ fully set up" card (real `/api/setup-status` check, same data the sidebar gating already uses) whenever credentials + suite target + docs are all configured for the current target.

## Onboard suite

### Clarify scope — first-build only?
**Type:** Q+A
**Severity:** nice-to-have
**What happened / what you want:** Confirm onboard-suite is mainly for a suite's very first build.
**Expected:** A clear one-line answer on the page itself.
**Status:** answered — yes, and it already says so on the page: "Builds (or rebuilds) a suite for a device from scratch, checking real sources first" (`PIPELINE_PLAIN['onboard-suite']`), shown above the technical description on every onboard-suite view.

### "Already Done" badge
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** If a suite has already been onboarded (docs ingested, knowledge cited, suite built), show a highlighted "Already Done — `<suite name>`" state instead of the plain run button.
**Expected:** Visual signal that re-running isn't needed.
**Status:** fixed — generalized to every runnable pipeline, not just onboard-suite: any pipeline detail page now shows a green "✓ Already done — last succeeded `<date>`" card when its most recent real run for the current target succeeded, via the same last-run endpoint above.

## New-suite-from-docs

### Overlap with onboard-suite / suggested ordering
**Type:** UX
**Severity:** nice-to-have
**What happened / what you want:** Clarify how this differs from onboard-suite; suggested real flow order is: setup/credentials → docs ingested → target old+new suite → onboard-suite/build. If a user is targeting an *existing* suite, rebuild/onboard-suite steps likely aren't needed — warn "you're targeting an existing suite, no need for this."
**Expected:** Clear sequencing + warnings when a step doesn't apply to the current target mode.
**Status:** partial — the sequencing half is fixed: `ingest-docs` moved into the Start group (see below), so the sidebar now reads Start (setup + ingest-docs) → Build (target-dependent steps), matching your suggested order. The "existing suite, no warning needed" half is still not built — see the item directly below, same real blocker.

### Existing-suite mode needs its own toolset
**Type:** Change request
**Severity:** annoying
**What happened / what you want:** Existing suites probably only need add-feature / consolidate / export-automation — plus a way to review which existing cases are automatable and estimate effort.
**Expected:** A distinct "working suite" path, separate from fresh-build onboarding.
**Status:** not built — needs your decision, not mine to make silently (same governance point raised in the archived predecessor file). Today's `fresh_build` flag only distinguishes "no old suite to reference" from "has one"; it doesn't model a genuinely separate "just work in this existing suite, skip onboarding" mode. Building that is a real, scoped feature — flag if you want it prioritized.

## ingest-docs

### Fold under Start?
**Type:** UX
**Severity:** nice-to-have
**What happened / what you want:** Consider moving ingest-docs under the Start accordion, since it's a before-anything-else step for a new project.
**Expected:** A decision either way, reflected in the sidebar grouping.
**Status:** fixed — moved from Build into Start in the sidebar. It doesn't touch TestRail or need a suite target, so it belongs with `start` (the one group never setup-gated), not behind the credentials/suite gate. The Processes-tab grouping already had it under "How to get started" — now consistent everywhere.

## export-automation

### Surface last export in Test Automation tab
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** export-automation's output should be visible in the Test Automation tab with a last-exported date/time, so someone knows there's a backlog ready to write tests from.
**Expected:** Cross-link from export-automation into Test Automation.
**Status:** fixed — Automation dashboard now shows a real export-automation card (current target's last run, status, summary) with direct links to re-run it and to **write-automation** (see next section — this surfaced a bigger find).

## Test Automation (dashboard / Keyword / Screen flows / Automation tab)

### Dashboard filters
**Type:** Change request
**Severity:** annoying
**What happened / what you want:** Add filter options (project, device, or all) to the Test Automation dashboard.
**Expected:** Filterable dashboard.
**Status:** fixed — project/device dropdowns added to the Dashboard page. Also found and fixed a real bug while wiring this: `/api/automation/tests`' `summary` was always computed from the *unfiltered* suite list even when `project`/`device_type` query params were passed, so a filtered view would have silently kept showing global totals. Regression test added (`test_automation_tests_summary_reflects_the_project_device_filter`).

### Provenance per test
**Type:** Change request
**Severity:** nice-to-have
**What happened / what you want:** Show which repo/folder/project a test lives in, and whether it was written manually vs. generated and pushed by Claude.
**Expected:** Provenance column/tag per test.
**Status:** partial, real gap on the other half — repo/folder/project is already shown (`source_file`, project, device tags on every suite card). Manual-vs-Claude-written is **not built and has no reliable signal to build it from**: Claude's own commits in these repos land under George's own git identity (checked this session's own commits), so `git blame`/author can't distinguish the two. Would need this tool tagging its own generated files at write time — real follow-up, not a quick add.

### Keyword scope confirmation
**Type:** Q+A
**Severity:** nice-to-have
**What happened / what you want:** Confirm keywords are always device-specific, never project-specific.
**Expected:** One-line confirmation on the page.
**Status:** answered — confirmed by reading the model directly: `FunctionKeyword` (`Platform/model/functions.py`) only ever carries `device_family` (POS/ETM/Common/Validators/...) — there is no `project` field anywhere in this data. Keywords are device-scoped only, never project-specific.

### Screen flows — completeness + "keys" explainer
**Type:** Q+A
**Severity:** nice-to-have
**What happened / what you want:** Is there more to the flows than what's shown? What are "keys" for?
**Expected:** Either more flow data surfaced, or an explanation of current scope + a tooltip/gloss for "keys."
**Status:** answered + fixed — the page already honestly states exactly how much was discovered ("N screens, M transitions") with the real source file cited, so what's shown *is* the full known scope for that device — nothing held back. Added a real tooltip on the "Keys" column header explaining what it is: the physical/virtual device key(s) that fire that transition, read straight from SIT's own `screenflow_map.jsonc`.

### Run + write automation from exported cases
**Type:** Change request
**Severity:** blocker
**What happened / what you want:** A way to actually run the exported automatable cases and start writing tests from them — e.g. a list of exported cases where you pick which ones to write up next.
**Expected:** Exported backlog is actionable, not just a static list.
**Status:** fixed — bigger find than expected: this already exists as a real, fully-wired pipeline (`write-automation.yaml` — confirm real device facts → `test-author` agent writes `.robot` tests tagged with real TestRail case ids in `test-automation-sit` → human-gated commit+push), with existing passing tests (`test_write_automation_*` in `test_app.py`). It just had **no way to reach it** — missing from every sidebar/nav group. Added it to the Build group, the Processes-tab "Once set up" stage, and linked directly from the new export-automation card ("Write automation from this backlog →").

---

**Test status:** `python -m pytest Platform/webapp/ -q` → 108 passed (was 107; added one regression test for the dashboard-filter summary bug).

*Dropped from the old sheet as stale, not carried forward:* "STUFF TO do" (getting Gareth set up
to onboard NJT) — this actually happened for real (2026-09-16/17 live onboarding run). If new
follow-ups come out of that work, log them fresh above under the relevant section.

*Still genuinely open, needing your input/decision rather than more code:* the "existing suite"
mode toggle (New-suite-from-docs section), and whether to invest in the manual-vs-automated
coverage % (needs `.robot`↔TestRail-id parsing built properly first). Everything else above is
either fixed or was already built and just needed confirming/surfacing.
