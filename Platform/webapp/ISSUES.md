# Test-Ops Console — issues & feedback

How to use: drop notes under whichever sidebar item you're testing, using the template
below. I'll read this file directly, fix what I can, and mark items `Status: fixed` with a
one-line note on what changed (and the commit, once committed).

Template for a new entry:

```
### Short title
**Severity:** blocker / annoying / nice-to-have / Q+A
**What happened:** ...
**Expected:** ...
**Status:** open
```

---

//Overview — General UI - Sidebar etc

### Arrive logo
**Severity:** nice-to-have
**What happened:** Logo is really small
**Expected:** Logo to fit the top left nicely
**Status:** fixed — height 22px → 36px, row padding increased. Look and confirm it reads well against the sidebar purple.

### dashboards and content
**Severity:** nice-to-have
**What happened:** Doesn't fit the full space, always a large gap, space to the right of the dashboard content or any content in any tab
**Expected:** Responsive, and fits nicely to width of content area space
**Status:** fixed — `.content` was hard-capped at 1180px; raised to 1600px + `width:100%`. Stat/dashboard grids already flex, so they should now fill wide screens. Flag if it still feels narrow on your monitor.

//Overview - Change target

### Changing target
**Severity:** Q+A
**What happened:** We can select project, device and model, build but how do we know were targeting the right suite? or the right old suite to also gain knowledge from - maybe there is a gap here with how we select the old suite, and the new targeted suite to work in
**Expected:** Users should be warned, and it should be very visible what project, device, model, build is currently pointing to old and new suites - and the ability to change this should be easy but not withut security checks - someone should approve the changed targeted suites maybe me for now my user
**Status:** fixed (first pass) — modal now shows a real "Old (read-only source) / New (write target)" readout, keyed per project+device pair (not a single global suite — each project/device combo gets its own real pair, per your follow-up). Only Translink/POS has a documented pair right now (`AA-POS Acceptance Test` → `GG - POS - Claude Suite`, from system-test-ops' CLAUDE.md); everything else honestly shows "Not configured" rather than guessing. Added a required approval checkbox that must be re-ticked every time (resets on any project/device change) before "Approve & apply target" enables — today you're the sole approver by ticking it; once writes are wired in this becomes a real sign-off gate rather than just a UI nicety. Top-bar chip now also shows both suites once applied.
**Follow-up needed from you:** more real old/new suite pairs for other devices so more combinations stop showing "Not configured" — I don't have those documented anywhere yet, so I won't guess them.

- Old suite should probably be optional? --- im just thinking about like scenarios when a user wants to target their existing suite - the test ops flow then would just basically add tests, edit tests within the existing targeted suite, instead of doing an old and new everytime. This way people can just check coverage instead on their existing suite - which means having an old would be obselete? you need and old if you have a brand new suite ofcourse so it has an old suite to reference
  **Status:** needs your decision, not mine to make silently — this changes what "old suite" means, and system-test-ops' CLAUDE.md currently has a hard rule baked in: *"the old suite is sacrosanct — copy out, never change"* (writes go only to `TESTRAIL_WRITE_SUITE_ID`, the new suite; old/source suites are always read-only, full stop). Making "old" optional would mean a genuine second mode — "audit/edit an existing suite in place" vs today's "old=reference, new=build target" — not a UI tweak. My read: this is worth having, but as an explicit **mode toggle** in the target switcher ("Fresh build (old+new)" vs "Working suite (edit in place)"), not a silent option, since the in-place mode drops the "never touch the old suite" safety net entirely. Flag if you want me to build that toggle — I haven't, since it's a governance change, not a bug fix.
- QA - where did you gt all these device models, builds from? i think there all correct. Does this just help with bespoke feature files about a model in the future? ofcourse alot of stuff will be common code, features anyway but just in case the way you reboot a device or do something specific for a model? this is why we have this right?
  **Status:** answered — `/api/taxonomy` (`Platform/model/devices.py`) parses this **live, every request**, straight from the real mirrored `EquipmentTypes.json` per project (the SIT device registry) — nothing hand-typed or cached. And yes, that's exactly the point of the model/device axis: most behaviour is common code/features, but some things are genuinely per-model (reboot sequence, specific hardware quirks, screen text) — the taxonomy is what lets a future bespoke feature/case say "this applies to POS_Way6 specifically" instead of guessing. The Features page's common-vs-bespoke split is the other half of that same idea.
- QA - I thought Gareth had already targeted an old and new suite for ETM NJT? is this not in the repos?
  **Status:** answered, partially good news — a **new/target suite is real and already in heavy use**: `proposals/njt-fr-suite-restructure/*.cases.yaml` all point at suite **30295**, with real findings/gap-register docs alongside it. But I could not find a documented **old/source suite id** anywhere in this repo for NJT FR — no `knowledge/projects/njt.md` exists yet (only `knowledge/njt/specs/*.md`, spec notes), and none of the NJT proposal docs name an old suite number the way ETM/GV/PV/POS do. So: the "new" half is confirmed, the "old" half is a real gap, not something I'm willing to guess at. If you know the old NJT FR suite id/name, tell me and I'll add the pair for real.
- QA i also thought we had already got old and new suites for all translink devices as this is all work we have already done? for translink anyway?
  **Status:** mostly yes, and the console just didn't know about it — I found and seeded 3 more real, unambiguous pairs into the console's store (POS was already there):
  - **ETM:** `AA-ETM-Acceptance Test` → `NEW ETM-Acceptance Suite` (30254) — cite: `knowledge/devices/etm.md:89` + `proposals/etm-suite-restructure/`
  - **GV:** `AA - Gate Validator - Acceptance Test` (14973) → `NEW GV Test Suite` (30286) — cite: `proposals/gv-suite-restructure/old-suite-audit.md:7`
  - **PV:** `AA-Platform Validator Acceptance Test` (10047) → `NEW PV-Acceptance Test Suite` (30255) — cite: `proposals/pv-suite-restructure/build-complete.md:3`

  Two are real gaps, not omissions on my part — both have a confirmed **new** suite but a genuinely ambiguous **old** side (multiple old suites feed the same new one, not a clean 1:1):
  - **TVM** → `NEW TVM Test Suite` (30284), fed by *at least* suites 5602, 6160 (called "the richest source"), Kiosk, Astreo (`proposals/tvm-suite-restructure/old-suite-audit.md`, `cross-tab.md`).
  - **HHD** → `NEW HHD Test Suite` (30285), fed by 4 old suites, 5446 primary + others incl. 5505 (`proposals/hhd-suite-restructure/`).

  I didn't seed these two because picking one "the" old suite would be a guess your engineers already resolved by hand (that's literally what the old-suite-audit docs did) — tell me which old suite id you want treated as "the" reference for each (or if it should genuinely be "multiple, see the audit doc") and I'll add it as a real pair, or extend the schema to support >1 old suite if that's actually the right model.

  Also found but out of scope of the project/device dropdown (not a `KEEP_DEVICE_TYPES` device): **BOS & ABT** has its own real pair too — old suite 14441 → `NEW BOS & ABT Suite` (30279). Flag if you want a way to target that from the console as well.

- **NEW (2026-09-07):** you already have real TestRail credentials configured in `system-test-ops/.env` — Settings now detects that file (read-only peek, never shows the key) and offers a one-click **Import** instead of asking you to retype anything. Also added a **Connections** card in Settings that's honest about scope: TestRail status is real and checkable here; JIRA/Confluence (via the Atlassian Rovo MCP) are connected at the Claude Code/agent layer, invisible to this plain FastAPI backend — the console says so rather than faking a status light for something it can't actually see.


//Overview — Suite health

- 

## Overview — All processes

## Overview — Features

## Overview — Repo map

## Overview — Gap register

## Build group (onboard-suite, new-suite-from-docs, ingest-docs, add-feature, consolidate, export-automation)

## Audit group (audit-coverage, audit-flows, audit, resolve-gaps)

## Maintain group (fold-defect, review-runs, maintain)

## Target switcher (Change target modal)

## General UI/UX (layout, colours, responsiveness, anything cross-cutting)
