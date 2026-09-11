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





STARTING Fresh

General
- So when no credentials, no docs, nothing set up yet, we should make only overview items, and START the things not faded and clickable. (need a way to test this)
- Auotmation can be visible though too

Test Ops
UI / UX
- Arrive logo bigger again please top left
- Overview, and start, and audit, (main side bar menu options) bolders, tiny bit bigger like 3px bigger than the accordion sub menu options, mayb make overview a accordion to with the suite health, processes, features, repo map, gap register underneth.
- Seetings and docs can be lower down nearer to the george oliver user name. or to be honest can clicking the login username, open up a tab type menu with docs, settings as options.
- Test-ops console title bit below arrive logo, to be in a similar writing or style as the arrive logo if possible? or just bolder, better, different font style to showcase the title of the CMS

Suite Health
- the real build stats run part, report data, is this gonna be showcasing the same way the last date, time a run was done or a audit, suite update or anything was done?
- Would be cool to have there, blocks again that show the date, time of the last function that was done, so add feature, then another one, showcasing all of them? so someone knows the last date, time of a specific functin that was run?
- cases total is good, added is good, edited is good, removed can delete this block i think, unchanged remove this block too, open gap qs is good to keep, can we add blocked for like new vs old, coverage percentage? manual coverage and automation coverage?
  **Status:** fixed (partial) — "removed" and "unchanged" stat blocks removed from the top row. Coverage % (manual vs automation) NOT built: some `.robot` files do reference a TestRail case id in their `Documentation` field (e.g. `test_signon_idle_screen.robot`: "TestRail C4099912, suite 30253") but it's free text, not a structured tag, and it's not there consistently across suites — computing a real automated/total % needs that mapping parsed properly first, flagging as a genuine follow-up rather than a made-up number.
- run health purpose? it should only ever be runs based off the new suite always, flaky dont get? no need for this, pass and fail are good to have, orphaned remove as dont understand. and the breif showcase of the ones visible should just be the failed test cases
  **Status:** fixed — confirmed the run-health fixture already only covers the `**NEW** POS-Acceptance Suite`, never the old one. Removed the "flaky"/"orphaned" stat blocks, kept "runs considered"/"always failing", and the case table now only lists cases with at least one failure (falls back to "No failed cases" text when there are none).
- to the right of run health have a comments bit, so pull in all comments of the recent run, mainly on the failed tickets, and then the actions taken against these.
  **Status:** fixed — run comments now render in a card side-by-side with run health (2-col sub-grid) instead of stacked below it. Also added a real "actions taken" signal: TestRail's own `defects` field on a result (linked bug ids) now shows as a pill next to any comment that has one — pulled live, not invented.
- last audit run is good to have
  **Status:** no change needed.
- open gap questions is good to have but annoyingly you can only show a few, are they the most recent questions? always have most recent first visible on dashboard.
  **Status:** answered — honestly, no. The gap-register fixture (`gaps.json`, 972 markers) is a mechanical grep result: `{file, line, kind, text}`, no timestamp field at all, so there's nothing to sort "most recent" by yet — the order shown is just repo file order. Sorting by recency would need either a `created_at` written at grep time or git blame per line; didn't fabricate an ordering to look like it's sorted when it isn't.
- make the manage, see all buttons on dashboards a 5px bordered shaped button on the top rght of each block bit. 
  **Status:** fixed — added a `.corner-link` style (small bordered pill, absolutely positioned top-right of the card) and applied it to "See all →" (gap register), "Manage →" (docs), and "Run again →" (last audit run).
- Case delta since snapshot, can we give a different name? maybe just observed changed since last audit or something? so this basically should only show, what cases might be deleted, moved, edited, added, MANUALLY - so anything you change doesnt effect this bit, only the manual edits by Users
  **Status:** fixed (partial) — card renamed to "Observed changes since last audit". The MANUAL-only scoping is NOT built: build-stats' diff today just compares case ids between two snapshots, it has no idea whether a change came from a manual TestRail edit vs. a re-export/push from this tool — added an honest caveat line to the card instead of a false claim. Doing this properly needs either TestRail's `updated_by`/`updated_on` per case (only visible via `get_case`, not the bulk snapshot call currently used) or this tool tagging its own pushes so they can be excluded — real follow-up, not done yet.
- maybe the above needs a way to review the manual edits and tick okay, thats fine type thing.
  **Status:** not built — depends on the manual-vs-automated distinction above existing first; there's nothing yet to "tick okay" against.
- Do we need a docs file for translink thought the point was to reduce the docs on the repo? we only ingest docs right then have stored reduced easier readable knowledge files, flows and features? maybe a short breif way of showing the doc name, and pass or fail for ingested properly, last date and time ingested.
  **Status:** not yet answered — no ingest-docs pipeline exists yet (docs today are just uploaded/stored, not processed into knowledge files), so there's nothing real to report a pass/fail or ingested-date on. Will answer properly once that pipeline is built.
- remove where this data comes from
  **Status:** fixed — card removed.
- move old vs new to the top as mentioned above. 
  **Status:** fixed — "Old vs. new suite — case counts" card is now first in the left column, above run health.

All processes
- new-suite-from-dcos? any point in this? being here.. its just ingest-docs amd nboard suite?
  **Status:** answered (repeat of the earlier answer) — yes, it's the doc-driven combo of ingest-docs -> onboard-suite chained together for a from-scratch build. Kept as its own pipeline entry, grouped under "How to get started" below since it's an onboarding path, not a duplicate.
- I really like this page and hows its set up, can we have a two tab thing on this page though, processes (default page) then flows, and on flows what i want to have is more of a like, How to get started accordiong then this has in the tree, /Start ingest docs, set up credentials and connections etc - then like Once your set up accordiong with tree for like onboard suite, consolidate, add feature, fold defect, then like a maintenance accordion tree for audit functions and reviews, maintain, then a like Human led accordion tree, resolve gaps etc. 
  **Status:** fixed — page now has "Processes" (default) / "Flows" tabs. Processes is grouped into 4 accordions covering all 14 real pipelines: "How to get started" (start, ingest-docs, new-suite-from-docs), "Once set up" (onboard-suite, consolidate, add-feature, fold-defect, export-automation), "Maintenance" (audit, audit-coverage, audit-flows, review-runs, maintain), "Human led" (resolve-gaps). export-automation's placement under "Once set up" (not Maintenance/Human led) was a judgement call — flag if you'd rather it sit elsewhere. Flows tab reuses the real SIT screen-flow viewer (same one under Automation) rather than duplicating it.


Features
- Neaten this page up, so have gaps found as a tab on this page so you can easily see the gaps in features found but onyl for the project your targeting, and list it better.
  **Status:** fixed — page now has "Features" (default) / "Gaps found" tabs. Gaps found is scoped to the current target's project (via `window.CURRENT_TARGET`, case-insensitive match against the real `d.gaps` keys — found and fixed a real casing bug here: the API returns lowercase project keys like `translink` but the target object uses `Translink`, so the first version silently showed "no gaps" when there really were 8). Falls back to showing every project's gaps if no target is set, and now shows feature names instead of bare keys.
- Features is its own tab and default tab, like how this is done.
  **Status:** interpreted as "within the Features page, Features itself should be the default tab" (done — it's the first/active tab, Gaps found is the second). If you actually meant "make Features the whole app's default landing page instead of Suite Health," flag it — that's a bigger, different change and I didn't want to guess and silently switch everyone's home page.
- Cited source (repo) 
  **Status:** still genuinely unclear what's being asked — a Citation's `source_ref` is sometimes a real repo file path (e.g. `knowledge/flows/...` in system-test-ops), sometimes a TestRail case id (`C4099911`, no repo), sometimes a spec paragraph (`FBD-100167 para 12`, a document, not a repo file). There's no single "which repo" answer that applies to all three kinds without fabricating one for the ones that aren't files. Please clarify what you want shown here and I'll build it for real.
- Is there any structure to the features, i fear this page will get soooo long with eventually every projects features, just trying to think of a better way to see the features files, knowledge files. 
  **Status:** fixed — each feature is now a collapsed accordion (reusing the same `.stage-group` pattern as Processes), so the page shows N feature headers, not N full tables, until you click one open. Auto-opens matching features when a filter/search is active.
- Maybe only show the features as default for the targeted project, device? as filtered, but people can click and change this to view others.
  **Status:** fixed — project/device dropdowns now default-select the current target (Translink/POS etc.) instead of "All", still fully changeable.
- How do we differentiate the common features vs bespoke? nothing on the features shows this, maybe the common should be common and include all devices its ocmmon for and variants etc, then bespoke is more of a project and device type view, maybe the colour of the cited source is slightly different for common than bespoke. 
  **Status:** fixed (partial) — added a real "Scope" column and recoloured the cited-source pill: a variant_name counts as Common if 2+ different real projects share that exact name for the same feature, otherwise Bespoke. Honest finding: on the current real seed data, this comes back 0 Common / 15 Bespoke — every project currently names its variant differently even for conceptually shared behaviour, so nothing is flagged common yet. That's a real fact about the data, not a bug — if you want cross-project reuse to actually register as "common," the seed data itself needs matching variant_name values across projects.
- Defo ways to improve this, to show common and bespoke features, feature files and cited source knowledge - way to stop it from being a massive long page, accordions, or blocks or info, dont know have a think.
  **Status:** fixed — see the accordion + Scope-column answers above; combined they're the page-length + common/bespoke fix in one.

Repo map
- Does the files need cleaning up? 
  **Status:** not assessed — this is a judgement call about a sibling repo's file layout, not something I'll silently act on. Didn't find anything obviously dead while working through this page, but I wasn't looking for that specifically. Ask me to actually audit for unused/stale files if you want a real answer here.
- make this accordions i think too
  **Status:** fixed — same collapsible `.stage-group` pattern as Processes/Features, one accordion per section, first one open by default.
- Add breif description to the main accordion too so like scripts -- blah blah what is it, what are these files - and how are they used
  **Status:** fixed — added a one-line plain-English gloss under each of the 6 section headers (deterministic core, scripts, agents, commands, this console's model/, this console's own scripts) explaining what the files in that group are and how the pipelines use them.
- Can we link files to the repo? and are they not now on the test platform repo? or is that just purely for this dashboard front end
  **Status:** fixed + answered — every filename is now a real link to its actual GitHub source. Answering the actual question: no, it's not all one repo — the repo map spans two real separate repos (`system-test-ops` on its `main` branch, `test-ops-platform` on its `master` branch), which is exactly why the section titles are prefixed with the repo name. The dashboard's own `Platform/model|tools` files are in test-ops-platform; everything else (the actual CLI, TestRail client, Claude agents/commands the pipelines run) lives in system-test-ops, not in this dashboard's repo.

Gap Register
- This should only be questions for the specific project and device yes> not all gap questions
- so need a way to make sure were tagging the question with what device, suite, document, if it is common then great but bespoke questions just for specific target.
- I would have prefered to select a gap question and then have a pop up with the form to reply, to answer it
- Can we not have pagination to view all of the gap questions or is that too much?
- What if we need to get you to clarify a little more on what your asking? maybe we need a way to reply and say can you give me more info on this gap question? what like area, what device, what functionality area or feature or any info on it more to help us answer would be great,
- This should be logged as well somewhere so all questions and answers are there - just because its good for us to show project managers that documentation may have gaps compared to the device now, and functionality now.
- You know like a tab on this page that shows like answers that conflict with specification and functionality or something, and like logs.

start
- When the user is all set up and has credentials, and set up everything - then can this just have a Tick byt the /start menu option, and a complete highlighted green on the page somewhere to suggest no need for this to be done by this user.

Onboard suite
- Is this function only mainly for like the very first time a suite has been made and needs building from scratch?
- If the user has done this or a suite has been build, onboarded, and the documents have been used, cited knowledge features to build a new suite and its basically all done, then maybe this should have a complete highlight on it or something different like a highlighted bit that says - Already Done - with suite name or something?

New-suite from docs
- Is this not the same as onboard suite?
- We probably should ingest docs, then onboard a new suite everything time first before allowing anything else, as we should have start, crednetials, languages and tools set up, then documents provided, ingested, then target old and new suite, then onboard suite, build new suite from all info. 
- If user is targeting existing then the rebuild and onboard suite, and stuff probably isnt needed right? we should probably label places that arent needed with a warning like - your targeting a existing suite no need for this
- existing suites probably only relly need add feature, consolidate, export automation (reminds me we probably need a way for existing suites to review cases for which is automatable, and give estimates to on existing suites

ingest-docs
- should this just be under a start accordion instead? something to be done for the project before anything else really so have stuff to write from etc

export automation
- this should export into the automation tab somewhere - so that it is visible to have a last date and time of the export so that on that side someone can run a write test automation from it basically. 


Test automation
- dashboard is cool - we need filter options though so you can put filters for project, device, or all 
- do we need more info on the tests written, like what repo folder there in, what projects, written manually pulled from repo or ones written by claude sent to repo type thing

Keyword
- looks good, assume keywords then are device specific never project specific? good to keep this way if that is the case

screen flows
- is there more screens to the flows?
- whats keys for?

Automation
- We need a way to run the exported cases and start writing them
- Maybe a list of the cases exported and then you can choose which ones you want to be written up?






STUFF TO do
- We want to use the tool to get NJT suite fully covered, and automation tests written
- Gareth will preferably need his own local or server hosted platform tool to do this on
- How can we get set up for this? what is the things we need to fix, change do to make this possible for gareth to start running the flows, and adding docs, and building suites, and audits and everything.