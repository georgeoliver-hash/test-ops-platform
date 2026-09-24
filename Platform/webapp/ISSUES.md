# Test-Ops Console — issues & feedback (v4)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`

**How to use:** just drop raw bullet points below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## Carried forward, not yet resolved

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
  doesn't model a genuine "just work in this existing suite, skip onboarding" mode. Flag if you
  want it prioritized.
- **Test provenance — manual vs. Claude-written** — no reliable signal today (Claude's commits
  land under George's own git identity) — would need this tool tagging its own generated files.
- **Features layout — named conceptual-area taxonomy** (Communication/Signing on/Ticket
  purchasing) doesn't exist as a field in `Platform/model/features.py` today. Needs a real
  curated `area` field added (data-modelling decision) — flag if you want it scoped for real.
- **Gap Register sync → re-audit/re-edit pipeline** — needs the same pipeline-execution-from-
  console plumbing every disabled "Run" button is already waiting on.
- ~~`human_setup` step's real `actions:` list isn't rendered~~ — **fixed** (round 3): `renderStep`
  now renders a real "Things to do" bullet list from `s.actions`.

---

General:
- on the sidebar, with Test-Ops, Automation, can we add two more pills buttons underneath so you have 4 like a 2 by 2 - Test-Ops, Automation, Project, Reports
- Project, Reports (can be empty spaces for now, for future phases way in the future.
**Status:** fixed — `.console-tabs` is a real 2x2 grid now; Project/Reports render as disabled `.placeholder` pills with a "soon" tag rather than hidden, so the intended shape is visible without pretending they're built.
- I think you have taken the wording of like lower case, or upper-case titles, words as gosepl from me, can we just make it globally a thing that its written in proper english? maybe like titles or stuff your grabbing from resources, data can be a spitting image of what it says but one the tool everything should be like proper english, Aa type way? not AA or aa or Aaaa Adddd but like a sentence is Aueue djhdhd ksjss you know? 
**Status:** fixed, scoped correctly — applies only to labels the TOOL generates (the pipeline-name fallback in `pipelineDisplayName`, via new `titleCaseWords()`), never to real data it merely displays (file names, TestRail project names, device ids) — those stay a spitting image of the source, per your own distinction.
- Gap Register title menu option to be Gaps
**Status:** fixed — sidebar group renamed "Gaps".
- Make Gaps a button the same as the other accordions right? and the like Project gaps, Device gaps, Commans Gaps, Bespoke gaps should be accordion options that open to the filtered tab on the pag right. 
**Status:** fixed — Gaps is now a real collapsible accordion (same as Build/Audit/Maintain), with Project/Device/Common/Bespoke gaps as its 4 sub-items; each jumps straight to the Gaps page with that scope already active.
- Make the text font size of menu options a bit smaller, clunky on the sidebar at the moment.
**Status:** fixed — `.navitem` 13.5px → 12.5px, group labels 16.5px → 14px, tightened sidebar padding generally.
- need more prominent arrows for the accordions on these menu options.
**Status:** fixed — chevrons 10-12px → 15px, bold, brighter (near-white) so open/close state reads at a glance.
- Change suite health to Status
**Status:** fixed — sidebar label only; the real view id (`health`) and page internals are untouched.
- Processes & Flows to Pipelines
**Status:** fixed — see the flagged naming collision noted below ("Tools to Pipelines").
- Knowledge & Features Files to Knowledge
**Status:** fixed — sidebar label and page `<h1>` both renamed.
- Repo structure & Map to Repos
**Status:** fixed — sidebar label and page `<h1>` both renamed.
- Get started to /Start
**Status:** fixed — `GROUP_DISPLAY_NAME.Start` is now "Start" (was "Get Started").
- check setup to Setup
**Status:** fixed — `PIPELINE_DISPLAY_NAME.start` is now "Setup" (was "Check setup").
- Leave Ingest docs
**Status:** left alone, as asked — no rename.
- Tools to Pipelines
**Status:** fixed — the naming collision this caused (flagged above originally) is now resolved: Build group stays "Pipelines"; the Dashboards nav item (`renderProcessesTab`) is "Pipeline Info" instead, page `<h1>` matches.
- New suite onboarding to Onboarding
**Status:** fixed — `PIPELINE_DISPLAY_NAME['onboard-suite']` is now "Onboarding".
- Onboard new JIRA to JIRA
**Status:** fixed — `PIPELINE_DISPLAY_NAME['add-feature']` is now "JIRA".
- Check Duplication to Duplication
**Status:** fixed — `PIPELINE_DISPLAY_NAME.consolidate` is now "Duplication".
- Automation Hand off to (move to Automation instead) - change name to Pull cases
**Status:** fixed — `export-automation` removed from the Test-Ops Build group; renamed "Pull cases"; real nav button added under the Automation tab's new "Cases" group, which jumps to the exact same real pipeline-run screen (decided with George: reuse the existing run UI rather than build a second one inside Automation).
- Write automated test cases (move to automation instead) - change name to Write
**Status:** fixed — same as above: `write-automation` moved out of Build, renamed "Write", real button under Automation's "Cases" group.
- Audit to stay as Audit
**Status:** confirmed, no change — `GROUP_DISPLAY_NAME.Audit` was already "Audit".
- Audit coverage vs release change to JIRA Coverage
**Status:** fixed — `PIPELINE_DISPLAY_NAME['audit-coverage']` is now "JIRA Coverage".
- Audit flow maps to Flow Maps
**Status:** fixed — `PIPELINE_DISPLAY_NAME['audit-flows']` is now "Flow Maps".
- Audit syntax to Gherkin
**Status:** fixed — `PIPELINE_DISPLAY_NAME.audit` is now "Gherkin".
- Maintenance to change to Testrail
**Status:** fixed — the `maintain` pipeline itself (had no display-name override before, fell back to its slash-command) is now labelled "Testrail".
- defect steps to case - Defects
**Status:** fixed — `PIPELINE_DISPLAY_NAME['fold-defect']` is now "Defects".
- Review latest run comments to Review runs
**Status:** fixed — `PIPELINE_DISPLAY_NAME['review-runs']` is now "Review runs".
- Maintain to Health
**Status:** fixed — `GROUP_DISPLAY_NAME.Maintain` is now "Health" (was "Maintenance") — this is the sidebar GROUP; the separate `maintain` PIPELINE inside it is the "Testrail" rename just above. Two different things sharing similar wording in your notes, resolved as two separate renames, not a conflict.
- Resolve gaps to Push gaps
**Status:** fixed — `PIPELINE_DISPLAY_NAME['resolve-gaps']` is now "Push gaps".
- Aurtomation should be the following below:
- title test automation SIT to just be SIT
**Status:** fixed — Automation tab's first group label is now "SIT (view only)".
- Dashboard sta the same, and test written, keywords to be the same, screen flows to be the same
**Status:** confirmed, no change — those 4 labels were already exactly that.
- Should we now have a Pull cases and write cases as mentioned above to move to this side of the platform
**Status:** fixed — see "Automation Hand off"/"Write automated test cases" above.
- Maybe a Projects options with accordion sub options
- sub options to be the Projects we have done so far, and the stuff related in a dashboard i.e. tess written, keywords area - all of which can be opened and closed to make the page not so big.
**Status:** fixed — real "Projects" accordion added under Automation, sub-items pulled live from `/api/automation/tests`' own `projects` list (not fabricated), each opening the dashboard pre-filtered to that project.
- changed my mind thing the arrive logo and title of the console to be aligned left same as the options. need the whole sibebar a bit tidier, the titles and sub titles text font size better easier to read
**Status:** fixed — logo-row is a left-aligned flex row again (was centred-stacked from the previous round); logo shrunk 60px→34px, tool-name 14.5px→13px, nav item/group font sizes tightened as above.
- we need a hamburger menu i think so we can open and close the sidebar?
**Status:** fixed — ☰ button in the topbar toggles `.sidebar-collapsed` on the shell, sliding the sidebar fully out of view and back.
- There was bug where the target you were selecting, after doing like a onboarding or refreshing it would sanp to a default translink target - but this si a bug, cause it should always be the last selected your doing right. not snap to a default
**Status:** fixed, real bug confirmed — `window.CURRENT_TARGET` was a hardcoded literal with nothing ever reading or writing it; every reload silently reset to Translink/POS. Now persisted to `localStorage` on every "Approve & apply target" and restored on load, before the first render.

Change target
- Project drop down? is this taking from real data? we need to ensure like archived or ones that dont exist are not pulling in as well? just ones actually on the database and have proper work done
**Status:** answered, real gap flagged — yes, real data: `projectsWithMappings()` unions SIT's real taxonomy with whatever's actually in the `suite_mappings` store, nothing invented. "Archived/doesn't exist" filtering is NOT built — there's no `archived` concept anywhere in `suite_mappings` today; adding one is a real, separate data-modelling decision (what marks a project archived, who sets it), flag if you want it scoped.
- device is a good drop-down to have - it should maybe onyl show the specific devices related to the project though right if i change project and they only have etm then thats the only option
**Status:** confirmed already working — `devicesForProject()` already does exactly this and was unaffected by this round's changes; picking a project always refilters Device to just that project's real devices.
- Model / build not sure how useful this actually is tbh with you? please help me if this is helping you with anything? or if this is even needed
**Status:** answered directly, then removed — checked every reference: it fed nothing but its own breadcrumb text, no pipeline or API call ever read it. Removed the field, the `selModel`/`refreshModels` code, and the model segment from the target chip.
- Need to have a better structure layout of this pop up.
**Status:** fixed — modal body is a real 2-column grid now (was a single stacked column), wider (below).
- So if the project doesnt exist we need a add project button really, so they can just add a Name, and then this is then added to the projectdrop-down - should at this point when you give project a name, maybe you should at this point select a top level testrail project? so that this project name is always got a parent level testrail project space selected yes?
- then when you do not have a documented pair for this new project, then you can press add this pair, you no longer would need to see new project name fields, or choose top level testrail project, you would only have the old and new suite fields right with dropdowns of the suites in the project?
**Status:** fixed — new "Add project" button opens the form in a distinct mode: project name + TestRail-project picker only, nothing else. The ordinary "Add/edit this pair" button (for a project that already has ≥1 pair) now auto-reuses that project's already-known TestRail project id (`projectTestrailId()`) and hides the picker entirely, showing it reused instead of re-asking — exactly the "no longer need to choose top level testrail project" ask, just old/new suite fields.
- Ticking fresh build is good, for like new new new projects so a complete startup and we just wannt create a new suite target with no old reference still.
**Status:** confirmed, no change — this already works as described; not touched.
- we should shorten the text everywhere though, no need to bulk our the jargan text explanations, like the not configured text and fresh build text - make it simpler - like Start up, no old suite to reference?
**Status:** fixed — "Not configured"/paragraph → "Not set up yet / No suite pair for X/Y — add it below."; "Fresh build — no old suite to reference (building purely from documentation)" → "Fresh build — no old suite"; suite readout labels "Old (read-only source)"/"New (write target)" → "Old"/"New".
- General tidy up on pop up as the above is all changed, better UI experience.
**Status:** fixed as part of the above — grid layout, shortened copy, Model/build removed, Add project flow.
- The responsive of this is bad, if your on laptop, the whole target pop up can go beyond screen - maybe the layout needs to be re-thought so it fits more width of the screen like 65% and longer - wider so can fit more on a screen width> make sense
**Status:** fixed — modal max-width is now `min(920px, 65vw)` (was a fixed 460px), with a narrower-screen fallback under 760px.

Dashboard suite health (name will change i know, this is just for reference)
- what is the fixture data? what does sync actually do, just refreshes for any changes? does this use AI, can it be code not AI
**Status:** answered — 100% code, zero AI. Only Translink/POS has a captured real TestRail snapshot (2026-08-07) standing in for live data; every other project/device shows an honest "no fixture" warning rather than faking numbers. "↻ Sync" re-runs the exact same real fetch calls the page does on load (build-stats, run-health, gaps, docs, last-audit, comparison, run comments, activity) — not a fake spinner.

Processes and flows:
- how to get started is highlighted, but when you highlight or click once set up, it doesnt highlight and remove highglight from how t oget started 
**Status:** fixed, real bug — "How to get started" was a hardcoded `featured: true`, never re-evaluated. `renderProcessesTab` now checks the real `/api/setup-status` for the current target: featured stays on "How to get started" while not ready, and moves to "Once set up" once it is.
- all accordions should reflect the same as the titles and options on the sidebar right, to give insight on everything the console has to offer and pipeplines etc
**Status:** confirmed already true, not re-built — Processes & Flows already reads pipeline data live from `/api/pipelines`/`/api/pipelines/{id}` (same source the sidebar's Build/Audit/Maintain groups read), and pipeline labels now use the exact same `PIPELINE_DISPLAY_NAME` map as the sidebar after this round's renames, so the two are already consistent by construction.
- does flows need updating, i feel like theres very little flows for everthing + when im targeting the Translink POS this should make the flows, and other parts of the console default to the info for that device and project only? ofcourse they can see other devices and info too
**Status:** partially fixed, one real gap flagged — Flows tab now also defaults to the current target's DEVICE (it already defaulted to the project; device wasn't matched before). "Very little flows for everything" is a real, separate data gap — screen-flow graphs come from SIT's own `screenflow_map.jsonc` per device, and how many devices have one isn't something this console generates, only displays; not fabricated to look fuller.

Knowledge and features files:
- change layout completely
- I think it maybe best to have a list of all the project and device etc thats filtered down, in one big list not seperated by feature - but instead have a column that shows the feature its relation to, this way you can ascend, descend the columns, can search phases or notes, maybe even a better way to group, or filter out specific areas of the device and bundle features together, jsut a better way to view this page entirely would be good.
**Status:** fixed, real rebuild — replaced the grouped-by-feature (or grouped-by-device) card layout entirely with one flat table: every variant is a row, a real Feature column shows what it belongs to, every column header is clickable to sort (ascending/descending, toggles on repeat click), and the existing project/device/search/common-bespoke filters all still apply to the same flat list. The old "Group by Feature/Device type" toggle is gone — there's nothing left to group, it's one list now.
- Gaps found should just be called Gaps
**Status:** fixed — tab label and page `<h2>` both renamed "Gaps" (the Features-tab-local one; the sidebar Gap Register page's own rename is covered separately below).
- This should list out in a neater way each seperate like not cited area or something rather than one big description
**Status:** fixed as a side effect of the flat-table rebuild — each row's expanded detail now shows the feature's own description alongside that specific variant's note, separately, rather than one shared paragraph sitting above a whole group of variants.

Repo and strcuture & map:
- think we need to re-think this area, accordions are good but dont understand the pill look, like when you open a accordion the inside content should be in the same pill div area right, and is this even match all the repos we have? and updates? maybe need to refresh or re-sync this area to grab the latest
**Status:** fixed — folder-tree content inside each accordion now sits inside a real pill-styled box (`.repo-tree-pillbox`, same purple-tinted pill look used elsewhere), not a bare nested list. Added an explicit "↻ Re-sync" button — genuinely re-fetches `/api/repo-map`, which itself already regenerates live from real docstrings/frontmatter on every call (confirmed: not a cached snapshot, covers both repos already).
- Thinking we just have accordions for top level repos - then just literally shot spitting image of a tree of files exactly like the repo would look, folders, files etc.
**Status:** confirmed already built this way — `buildFileTreeHTML` already renders a real nested folder/file tree per top-level section, client-side, from each file's real path; not changed structurally this round, just re-skinned into the pillbox above.

Gap register
- remember the questions here should only relate to the current targeted project, can see njt/etm questions on bespoke gaps for POS translink? 
**Status:** fixed — real backend change (`app.py` `get_gap_register`): `scope=bespoke` now ALSO narrows to the current `project` when one is given, same as project/device scopes (only stays repo-wide with no project set at all). This deliberately overrides the original 2026-09-18 design note in the code, which called repo-wide bespoke correct on purpose — you've now asked for the opposite, and that's the real, current answer. New test: `test_gap_register_scope_bespoke_narrows_to_project_when_one_is_given`.
- No need for the answer log form fields bit now if you just click and can asnwer - the bottom bit or logs should be a seperate tab in this place next to the Gaps
**Status:** fixed — page renamed "Gaps", split into two real tabs: "Gaps" (the marker table, click-a-row-to-answer, unchanged mechanism) and "Log". The old quick-add form fields at the bottom are gone entirely — answering only ever happens via the click-a-row modal now.
- within this page should show the answers logged, date and time it was logged and asnwered, date and time of last sync or resolve gaps, what calrifications requested and when, conflicts with spec stuff etc
**Status:** fixed — the new Log tab shows: last resolve-gaps run for this target (real status + timestamp, via the existing `/api/pipelines/resolve-gaps/last-run`), then three real sections (Answers / Clarifications requested / Conflicts with spec), each entry dated and attributed, exactly as already stored — nothing new fabricated, just surfaced together instead of stacked under one quick-add form.

Get started:
-  NJT/ETM is fully set up — credentials, a suite target, and docs/knowledge are all configured. Nothing left to do here. this wording is wrong, should just be your account or credentials are set up etc, doesnt matter about docs/knowledge right for getting started?
**Status:** fixed, agreed — the message now checks only `credentials_configured && suite_configured` (dropped `docs_configured`) and reads "...is set up — credentials and a suite target are configured." Docs/knowledge is still correctly required for the SEPARATE Build/Audit/Maintain gate (same `/api/setup-status` call, different field) — only this one over-scoped message was wrong.
- ingest docs, what is the docs_path - can this be better calrified? do we ever wanna be given the ability to change this, should this just show as a text string not in a field to edit.
**Status:** already fixed last round (2026-09-21) — `docs_path` is read-only, pre-filled from the real resolved target folder, can't be typed into. Carrying the confirmation forward since you asked again.

New suite onboarding:
- flow data path what is the point of this? is this the JSON flows? we need a better way to gain UI understanding cause we can give you docs HMI docs, and use the flows in SIT not everyone will gt JSON flows of the UI designs unfortunately as this will always be different
**Status:** answered + inline help added — yes, it's the Overflow UX flow-data JSON export, feeding `mine_flows`. Added real inline help text on the field itself explaining it's optional and skipped cleanly with no export. The deeper point — that HMI docs + SIT's own flows should be enough without ever requiring an Overflow JSON — is already true structurally (the field is optional, `mine_flows` skips cleanly, `onboard-suite` doesn't block on it), so no code change was needed there, just the missing explanation.
- any part of this pipeline or steps can be removed as uneccessary or reduced to code instead? even if we split AI area to code and AI is good.
**Status:** flagged, not decided — this is a real pipeline-design/architecture question (which of `onboard-suite`'s agent steps could become deterministic code), not a UI change, and not mine to decide unilaterally. Worth a dedicated look at `onboard-suite.yaml` step-by-step if you want to scope it.

Onboard new JIRA
- so this is the same for docs path, flows path and everything, this area where you can write into a field, should have more info, like what, why and how do we put the write data in these fields to help you. like do we put the tibu or whatever here? or the release? etc would be cool to be able to search JIRA dropdown instead fo what you need, filter down via grabbed data from JIRA or would that clog it too much Maybe
**Status:** fixed (inline help) + decided (with George): added real inline help text to `add-feature`'s `feature_or_jira_key` field ("A JIRA key like PROJ-123 (pulled live from JIRA), or just a plain description..."). Decision on the searchable-dropdown idea: inline help only for now, no new backend/MCP search work — can revisit if the plain-text field turns out to genuinely clog things up in practice.
- does this pipeline actually work?
**Status:** answered — yes. `add-feature` is fully wired end-to-end: real `python -m system_test_ops push --file ... --commit`, a real `audit` gate (`must_be: clean_of_blocking`), no stubs anywhere in the chain.

Check duplication:
- (nothing written yet — nothing to action)

GLOBALLY - when you open a accordion, it should close the other accordion you have open i.e. sibe bar menu or processes and flows, and other areas too
**Status:** fixed for sidebar nav groups (Dashboards/Gaps/Start/Build/Audit/Maintain — opening one now closes any other open one) and for stage-group accordions (Processes & Flows' stages, Knowledge's old grouped view before its rebuild, Repo map's sections) — both via a shared "close siblings within this root" helper. Deliberately NOT applied to the repo-map's nested FOLDER tree (multiple folders open at once is normal, expected file-browser behaviour — forcing single-open there would actively hurt usability) or to individual step "what it does" accordions (each step's detail is independent info, not mutually exclusive like a menu). Flag if you actually wanted those included too.
- We should add fake loading percentages or bars when you running a pipeline? woudl look cool just like an estimated time it should take and add a loading bar to fill in that time or something, and buffers, and loading, and little areas where some more like visual reference to no we are still doing something, not just waiting.
**Status:** decided (with George), NOT built as a fake bar — a fabricated % or ETA for a duration this app genuinely doesn't know would be the one place that breaks its own "never invent what isn't real" rule that runs through everything else in this console. Built the honest version instead: a small pulsing "still working" animation (three dots) next to any currently-running step, and on the overall "Running…" message — visually alive, without inventing a number.

Coverage runs — multiple JIRAs, and per-pipeline run history (raised in chat, not dropped into this file first — recorded here anyway so the history stays complete):
- need a way to run coverage against a fix version/release on JIRA, OR bugs/epics — sometimes multiple JIRAs at once, not just one — needs to be a real thing you set before running any JIRA-related pipeline.
**Status:** fixed — `fix_version` (audit-coverage) and `feature_or_jira_key` (add-feature) are now a real repeatable chip input (add one, see it as a removable chip, add another) instead of a single text box. Submits as one comma-joined string, unchanged wire format. The real JQL step each field feeds (`pull_jira_scope`/`understand_feature`) now explicitly builds `fixVersion in (...)`/`key in (...)` when given more than one — updated the real pipeline YAML notes in `system-test-ops`, not just the UI. `add-feature`'s dual JIRA-key-or-plain-description behaviour is preserved, just not both at once in the same run.
- have we actually done everything on my issues.md?
**Status:** answered directly in chat — yes, every prior bullet had a real Status line; only the explicitly-flagged architectural/data-modelling items remain open (see "Carried forward" at the top of this file).
- ingest docs page needs an overview of the current documents uploaded for the target area.
**Status:** fixed — this data already existed (the separate Docs settings page's own table) but wasn't surfaced ON the ingest-docs pipeline page itself. Added a "Currently uploaded for X/Y" panel there, reusing the same real `/api/docs` data.
- maybe each pipeline needs a log tab to keep any info of previous runs, data, uploads — and specifically for JIRA pipelines, overviews of current JIRAs being selected/reviewed, and a log of previous date/time of specific JIRAs already reviewed against.
**Status:** fixed, real backend addition — `pipeline_runs` gained a genuine `extra_inputs` column (JSON, e.g. which fix_version/JIRA key(s) a run was actually given), a new `store.get_runs()` query, and a new `/api/pipelines/{id}/runs` endpoint. Every pipeline-detail page now has a real "Log" tab alongside "Details" showing past runs for the current target — when, status, what it was given (JIRA values shown per-run where recorded), and its summary. Runs from before this change genuinely have no `extra_inputs` recorded — shown honestly as "not recorded", never backfilled or guessed.
- can we have a drop-down select for review runs instead of the latest 15 runs on the project space currently targeted?
**Status:** fixed — `review-runs`' real `last_n` input (already existed in the YAML, default 10) was rendering as a plain free-text number box; now a real dropdown (5/10/15/25/50).

Doc-sorting + intent field (raised in chat while doing a real Translink doc-sort by device, not dropped into this file first — recorded here anyway so the history stays complete):
- maybe sometimes we need prompt fields on pipelines so users can also give a prompt to you about what there expecting to do with stuff you know.
**Status:** fixed — every pipeline-detail page now has a real, always-present "What are you trying to achieve with this run? (optional)" textarea, not tied to any pipeline's own declared `inputs:` list. Rides the existing `extra_inputs` plumbing (`data-extra-input="intent"`), so it needed no new submission wiring and already shows up in a run's Log tab for free, same as `fix_version`/`docs_path`. On the runner side, when supplied it's appended to whatever prompt an agent step builds, explicitly framed as *"context for your judgment calls on this step — weigh it, but the step's own instructions above still govern what you actually do"* — deliberately not phrased as a command that could override the step's real job. Omitting it (the default, and every pre-existing run) changes nothing. Real tests added (`test_run_intent_appended_to_agent_prompt`, `test_run_intent_omitted_when_not_supplied`, `test_run_intent_persisted_and_visible_on_run_record`), full suite passes (171/171).
