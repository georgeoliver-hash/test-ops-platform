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

- Run health is this like the recent runs? test runs being run by people or just your own tests for the tool itself?
  **Status:** answered — real. `run_ids: [21978, 21742, 21495, 19352, 19087, 19074]` in the fixture are genuine TestRail run ids, pulled via `system_test_ops runs --project --suite --last 10` (a read-only TestRail API call) — actual executions of the actual suite, not anything this tool ran itself. Added a line to the Run health card saying this explicitly.
- why do we have a removed bit when we cant actually delete? we only mark as delete right? maybe this should reflect the amount marked for deletion.
  **Status:** answered + fixed — "removed" doesn't mean "marked for deletion" (there's no such flag; TestRail here has no soft-delete concept exposed to this tool). It means: a case id that existed in the *last* build-stats snapshot but is missing from the suite *now* (`system_test_ops/snapshots.py`: `removed = old_ids - new_ids`). Since the API genuinely can't delete, this only shows non-zero if a case was removed by hand in the TestRail UI, or moved to a different suite. Relabelled the stat tile to "removed since snapshot" and added the same case ids to the delta table (which previously only listed Added/Edited, dropping Removed silently — a real inconsistency, now fixed) plus an explanatory line.
- 799 is alot of cases you sure this is right for POS?
  **Status:** confirmed real, not a bug — pulled from the actual live suite (id 30253, `**NEW** POS-Acceptance Suite`), captured 2026-09-07T08:13:26Z, straight from the fixture file (`pos-build-stats.json`). Not a guess or a stale number.
- should have a like last audited date, last time gaps were resolved, last time audit coverage was checked, last time any 'build' feature was Run
  **Status:** real gap, not built — checked `system-test-ops/reports/**` (gitignored, local-only) for something to surface honestly: dated folders exist per suite (e.g. `reports/tfts-system-test/30254/2026-08-07/`), but the filenames inside aren't standardised across sessions (`flow-coverage.md`, `alignment-audit.md`, `cases.md` all appear, not a fixed set) — auto-classifying those into "last audit" vs "last gap-resolve" would mean guessing at what a human-named file actually was, which I'm not willing to do. The honest path: this becomes trackable for real once pipeline "Run" buttons are actually wired (a real event to timestamp), or if you want, I can add a manual "log this as done" button in the meantime — flag which you'd prefer.
- gap register questions showing 5 is obselete, just the number of gap questions visible, and where to find them - (probably should be able to answer these questions for this specific project, targeted area in the gap register bit, with free typing 9but then this would need AI wouldnt it?) maybe code can push the free typed answers to the related question? and then on a audit or audit coverage review again then its countered into that
  **Status:** the "5" bug is fixed — it was a literal hardcoded string ("showing 5") unrelated to what was actually shown; now reads the real count. Added a "See all →" link straight to the full Gap Register page. Your bigger idea (answer a gap inline, have it flow back into the next audit) is real and matches how `resolve-gaps` already works in system-test-ops (turns GAP/UNCONFIRMED markers into cited facts via a human Q&A loop) — but that loop runs as a Claude Code agent pipeline, not through this API, so wiring "type an answer in the console" through to it is exactly the same pipeline-execution wiring the disabled "Run" buttons are waiting on. Not built yet; flagging as the same underlying blocker, not a separate one.
- dont know what data currency is, or case delta is it actually data worth showing probably not.
  **Status:** fixed — renamed "Data currency" → "Where this data comes from" and reworded its bullets in plain terms (what each number is, not just a timestamp). Kept "case delta" (renamed the card copy, not removed) since it's the real added/edited/removed breakdown, just poorly labelled before — the underlying data is genuinely useful, the name wasn't.
- and OLD vs NEW suite data compairson would be cool? like coverage, or total number of cases, or give me some suggestions
  **Status:** good idea, not built — suggestions: (1) total case count old vs new (cheap, just two `cases --suite` pulls), (2) how many old-suite cases have been copied into the new suite yet vs how many remain (needs a Refs/title-match heuristic, already exists in some proposals/*.changelog.md), (3) coverage-shape diff (sections/case-types present in old but missing in new). (1) is buildable now from data we already pull; (2)/(3) need the same coverage-analyst-style matching `audit-coverage` already does. Say which you want first.
- maybe the last time documents were uploaded for this device, project and the name of these docs in a list would be cool to see.
  **Status:** fixed — Suite Health now has a "Docs on file for `<project>/<device>`" card, real data from `/api/docs`, with a link through to the full Docs page.
- links to relevant places like, gap register, uploaded docs, feature files for this targeted area
  **Status:** fixed (partial) — added real "See all →"/"Manage →" links from Suite Health to Gap register and Docs. Didn't add a Features link since Features isn't project/device-scoped the same way (it's the common-vs-bespoke view across all projects) — flag if you want a filtered jump-in anyway.

## Overview — All processes

- lets make the keys the same background colour as on the accordions so easier to know what is what.
  **Status:** fixed — each step-detail key label (Command, Agent, Gate, etc.) is now tinted to match the same colour system as the kind pills above it (AI=purple, code=teal, gate=indigo, human=grey) — same colour means the same thing everywhere on the page now, not just on the top badge.
- when opening a process, flow i.e. start - have a description of what start is, not AI or code based, or scripts just say /start is the beginning, its where you first interact with the platform and your PC requirements, set up is done (not liek that but on the lines of that get me? do that for all)
  **Status:** fixed for all 14 real pipelines — added a plain-English one-liner per pipeline (shown on both the Processes & flows list and the pipeline detail page, above the technical description, never replacing it). `start`'s: *"The front door — checks your setup is ready, asks what you want to do, and points you to the right process."* Every gloss is a simplification of that pipeline's real `description:` field — nothing new asserted.
- accordions for each like bit preflight, fix-ready-items there good, but there not actually like informative, they just add extra confusion of more scrip names, more technical names, we need to basically explain in baby terms what this part of the process is doing, how it does it, what is uses. in a short descriptive way
  **Status:** fixed — every step accordion now opens with a plain-language line before the technical detail (Command/Agent/etc, still there for anyone who wants it). Sourced only from real, cited docs: CLI subcommand glosses come verbatim from system-test-ops CLAUDE.md's own "CLI quick reference" table; agent-step glosses come from the same file's "The team" table. Nothing invented — if a step's kind/command/agent isn't one of those documented ones, no plain line is shown rather than guessing at one.
- not every process or flow is actually on the side bar? this can be confusing as it looks like there is more features to the processes than available to use, maybe split them into functions and behind the scene processes or something. easier to differentiate
  **Status:** confirmed and fixed — you were right, this was a real bug. `start` exists in the real pipeline index (`/start` slash command and all) but wasn't in any of the Build/Audit/Maintain groups, so it silently never appeared in the sidebar even though the other 13 pipelines all did. Added a new "Start" group above Build. Checked the full index against the groups this time — all 14 are now accounted for, one group each.

## Overview — Features

## Overview — Repo map

## Overview — Gap register

## Build group (onboard-suite, new-suite-from-docs, ingest-docs, add-feature, consolidate, export-automation)

## Audit group (audit-coverage, audit-flows, audit, resolve-gaps)

## Maintain group (fold-defect, review-runs, maintain)

## Target switcher (Change target modal)

## General UI/UX (layout, colours, responsiveness, anything cross-cutting)
