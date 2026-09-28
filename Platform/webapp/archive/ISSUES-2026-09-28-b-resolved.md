# Test-Ops Console — issues & feedback (v5, archived 2026-09-28 round 2)

Everything below was fixed, answered, or explicitly flagged/scoped during this round.
Superseded by a clean ISSUES.md (v6) — see there for what's still open, including the
naming/IA questions this round surfaced.

---

## Big batch (51 raw bullets dropped in one go, 2026-09-28) — processed in full

- Side bar menu, when closing it, theres a wierd overlay of text — margin/padding spilling to the left edge.
**Status:** fixed, real bug — grid items default to `min-width: auto`, so `.shell.sidebar-collapsed{grid-template-columns:0 1fr}` never actually shrank `.sidebar` to 0 width; its unbreakable content just sat at the edge, looking like an overlay. Added `min-width: 0` to `.sidebar` so it can genuinely collapse and its existing `overflow: hidden` can do its job.
- siebar menu would be cool to have icons for buttons that open up the sub menu options?
**Status:** not built — real, reasonable ask, but a real design pass (which icon per nav item, collapsed-state-only or always) rather than a one-line fix. Flag if you want it scoped for real.
- think the projects menu option on automation is broken?
**Status:** investigated, no code bug found — `/api/automation/tests` returns real projects (`bos, common, njt, nta, translink`); the accordion/click wiring (`populateAutomationProjectsNav`) is structurally correct and persists across tab switches (nav content is built once, just hidden/shown). `bos`/`common` showing up alongside `njt`/`nta`/`translink` matches the real repo structure — `test-automation-sit/projects/bos/` has its own `devices.yaml`/`tests/`, same shape as the customer projects — not a fabricated entry. If something specific still feels broken (nothing happens on click, wrong dashboard shown), tell me exactly what you saw and I'll dig further with that repro.
- can we deep dive the SIT view only dashboards... is it really up to date or purely based on the sit clone/pull?
**Status:** answered + fixed, confirmed real — yes, `sit-mirror/` (backing the Keywords and Screen flows views specifically) is a one-way, point-in-time copy via `tools/sync_sit_mirror.py`, never a live connection. Checked: it was genuinely **20 days stale** (last touched 2026-09-08). Dashboard/Tests written are unaffected — those read the live `test-automation-sit` repo directly, not the mirror. Added a real "last synced" banner (✓ if <7 days, ⚠ if older) on the two mirror-backed views, sourced from the mirror folder's own real filesystem mtime via a new `/api/sit-mirror/status` endpoint — never a fabricated "up to date."
- dashboard status page — line graphs, pie charts, cooler dashboard stuff?
**Status:** not built — real data-visualization feature, needs a design pass (what to chart, what "cooler" means concretely). Flag if you want this scoped; the dataviz skill is available when we get there.
- confidence in coverage for the suite, based on gaps/tests/specs covered?
**Status:** not built — real feature, needs a scoring-model decision (what inputs, what weighting) before it can be built honestly rather than as an arbitrary number. Flag if you want it scoped.
- what does sync do, do we need visual buffers so people aren't misled?
**Status:** answered previously (100% code, zero AI; ↻ Sync re-runs the exact same real fetch calls the page does on load) — still true. The "visual buffer" ask is already partly addressed by the pulsing "still working" dots on running pipeline steps (built 2026-09-24). If you want buffers somewhere specific beyond that, name the exact spot.
- pipeline info accordion — only one has a different colour, should be purple-when-open/white-when-closed for all.
**Status:** fixed, real bug — there was no `.stage-group.open .stage-header` rule at all; only the hardcoded "featured" (How to get started) stage was ever purple, permanently, regardless of open/closed state — exactly the "only one is a different colour" you saw. Added the missing open-state purple rule for every accordion.
- pipeline info — we need flow diagrams of how pipelines work, not SIT flows.
**Status:** partially addressed this round (see the new generic "How to run this" card below, which covers "what does each step do, in order, in plain steps"), but an actual **visual diagram** of a pipeline's mechanics is a separate, bigger ask, not built. Flag if you still want real flowchart-style diagrams — would use the diagramming skill.
- gaps/unconfirmed text is too vague — write it out in plain English, maybe an AI-summarize button.
**Status:** not built — real, good feature. Flag to scope (per-marker rewrite vs. a one-click batch "AI summarize" pass over the whole register).
- reorganise the sidebar, less accordions?
**Status:** folds into the naming/IA discussion below — see the questions.
- the repos view — where's the test-automation-sit repo?
**Status:** fixed, real gap — Repo Map only ever covered `system-test-ops` + `test-ops-platform`; `test-automation-sit` (this team's own Robot Framework suites — NOT `flowbird-group/sit`, which stays excluded per this tool's own docstring, "not ours to inventory") was missing entirely, despite the Automation tab already reading from it. Added two new real sections (written test suites + scripts), excluding `reference/` the same way `model/automation_tests.py` already does for its own dashboard counts.
- knowledge gaps could use more info — bullet-pointed, what's missing, what doc would help.
**Status:** not built — real enhancement. Flag to scope (this overlaps with the "gaps too vague" ask above — likely one piece of work, not two).
- log tab summaries are too long, ground them down to a couple of sentences.
**Status:** fixed — an agent step's `summary` can genuinely run to paragraphs (its full free-text output); the Log tab cell now truncates display to ~180 chars with an ellipsis, full text still available on hover (native tooltip). The underlying data isn't touched, just this table's display of it.
- new pipeline: generate a test summary report from existing templates/examples.
**Status:** not built — real, scoped feature, but needs grounding in your actual template(s)/example report(s) first (per this whole app's own no-invention rule — I won't guess a report shape). Point me at the real template/examples and I'll scope a real pipeline.
- rename the JIRA/"Release" pipeline to reflect it takes anything from JIRA, not just releases.
**Status:** folds into the naming/IA discussion below.
- maybe get rid of Start entirely, merge into Setup + Ingest Docs in one accordion?
**Status:** folds into the naming/IA discussion below.
- docs_path shouldn't be an editable field — just show it near the title like the dashboard pills.
**Status:** fixed — `docs_path` removed entirely from the editable-inputs list (it was always system-resolved, never actually typeable in practice); now shown as a real pill (green dot = resolved, amber = not yet) right under the page title, next to the pipeline description.
- only_file — can this be a dropdown of recently uploaded files, clearly labelled optional?
**Status:** fixed — new `/api/docs/folder-files` endpoint lists the real, actually-present convertible files in the resolved docs folder (capped at 300, placeholder/0-byte stubs excluded same as the existing file-count logic). `only_file` is now a dropdown of those real files, clearly labelled "(optional...)", with a "Type a path manually…" fallback for anything the listing missed.
- currently-uploaded docs list — can this be an accordion (open/close)?
**Status:** fixed — wrapped in a real collapsible accordion, count shown in the header.
- put the "waiting on you" bit under each step on the left, not just in a separate column.
**Status:** investigated, partially already true, full merge deferred — the live run panel already puts the Continue/Approve button directly under its matching step (right-hand `pipelineStepList` column). The literal ask — merging that into the SAME column as the static "what it does" descriptions on the left — is a bigger layout refactor of the live-polling architecture a lot of today's other fixes depend on; flagged rather than rushed through at the end of an already very large session. Real candidate for a focused pass on its own.
- is "Pipelines" the right word for that accordion? tools/functions/abilities?
**Status:** folds into the naming/IA discussion below.
- separate Functional docs / Design docs upload areas in Settings; drop flow_data_path from onboarding.
**Status:** not built — real feature, needs a placement decision (Settings vs. a new page) and a definition of exactly what counts as "Design docs" vs. today's `docs_path`. Flag if you want it scoped for real (this is the same underlying ask as "check coverage against design docs" and "upload functional/design separately" further down this list).
- distinguish onboarding vs. update-from-docs so people don't confuse "onboard everything again" — maybe "Re-examine whole suite"?
**Status:** folds into the naming/IA discussion below.
- (the big capability restatement, #91–115): a full re-listing of what the tool should do.
**Status:** read in full and mapped against what's real today (not guessed):
  - Setup/laptop check → **Start** (exists).
  - Ingest zips/multiple folders, select/de-select documents → **not built** — `ingest-docs` handles a whole folder or one file (`only_file`) today, not a zip upload or a multi-select picker. Real, scoped gap — flag to prioritize.
  - Onboard a new suite from newly-uploaded docs → **Onboarding** (`onboard-suite`, exists).
  - Feature/JIRA (any key/URL, bugs/epics/stories/releases) cross-examined against current suite + automation knowledge → **Feature** (`add-feature`, exists) for the suite side; automation-knowledge cross-examination specifically isn't part of it today — real, separate gap if you want that added.
  - Update from docs, select one or multiple newly-uploaded documents against an existing suite → **Update from docs** (`update-suite-from-docs`, built earlier today, exists) — multi-document selection via the new knowledge-files "Use this run" picker also built today.
  - Merge/health-of-structure after edits/resolved gaps → **Merge** (`consolidate`, exists — and its real, blocking bug from a live run today is fixed, see below).
  - Targeted run → **Targeted run** (exists).
  - Generate a test-run report from templates → **not built**, see above.
  - Answer questions/gaps, resolve, update cases → **Resolve** (`resolve-gaps`, exists) + the Gap Register's click-a-row-to-answer UI (exists). The "write it in plain English" quality-of-the-question ask above is real and separate.
  - Short step-by-step guide per pipeline, plain sentences, in an accordion → **built this session** (the new generic "How to run this" card — preconditions, real step-by-step from the actual command doc, where results land, what's next).
  - Coverage against design docs / separate functional+design upload → **not built**, folds into the Functional/Design docs ask above.
  - TestRail standards/Gherkin/English conformance → **Standard** (`audit`, exists).
  - "Health" word vs. merging Audit+Health → folds into the naming/IA discussion below.
  - Review runs/comments/defects/all statuses to answer gaps/update cases → **History** (`review-runs`, exists) — covers run health broadly; full per-status (pass/fail/retest/invalid) breakdown and defect-linking specifically isn't built out yet, real gap if you want it deeper.
  - Automation cases dashboard, keywords/flows view → **Dashboard**, **Keywords**, **Screen flows** (all exist, under Automation's "SIT (view only)" group).
  - Repo-type click-through view of tests written (not bulk detail) → **not built** — today's "Tests written" view is a filterable table, not a click-through tree. Real, scoped gap — flag to prioritize.
  - Pull cases from TestRail / write for automation → **Pull cases**, **Write** (exist, Automation tab's Cases group).
  - Write automation from docs/JIRA without the TestRail pre-step → **Draft** (`draft-automation`, exists).
  - Project info tab (per-project devices/health/gaps/audits/automation) → **Project tab** (exists, built 2026-09-22).
  - Reports tab as real links to generated reports + tool logs/cost → **not built** — Reports is currently an empty placeholder pill (2×2 grid, "soon" tag) with nothing wired. Real, scoped gap — flag to prioritize; the AI-cost data it would need (per-run cost/tokens) already exists (`/api/pipelines/runs/{id}/cost`), just isn't surfaced as its own page yet.
- please review every pipeline/option's naming to match the real scope.
**Status:** folds into the naming/IA discussion below — this is the umbrella version of the several individual rename asks above (Release/JIRA, Start, "Pipelines", Health/Audit, Onboarding-vs-Update-from-docs).

---

## Real bug found and fixed while addressing the above (not from this file — raised live, "another one, leave to the end")

Run failed: `consolidate` (Merge) on Translink/POS, step `execute_folds` failed.
**Status:** fixed, real bug, root-caused (not a Retry-worthy transient) — `execute_folds`'s command hardcoded the literal, never-substituted placeholder `<folded>.cases.yaml` as its push target (unlike `onboard-suite`'s `<area>` token, `<folded>` isn't a real template token anywhere in `runner.py`), AND no step in the pipeline ever actually authored a real `.cases.yaml` from the confirmed fold groups — `find_fold_groups` only ever wrote the audit/proposal `.md`. This step could never have succeeded as written. Fixed: added a real `author_folds` step (gherkin-author, between `confirm_aggressiveness` and `execute_folds`) that authors a real staging `folded.cases.yaml` from the confirmed fold groups, and `execute_folds` now pushes that real file. Also found and fixed the same missing-`{project}-`-prefix bug in `find_fold_groups`' and `fold-defect`'s own `produces:` paths (they wrote to `proposals/POS-suite-restructure/...` instead of the real, established `proposals/Translink-POS-suite-restructure/...` convention every other pipeline uses) — confirmed by the live run's own agent output, which had written to exactly the wrong, prefix-less path. New tests: `test_consolidate_execute_folds_references_a_real_produced_file_not_a_placeholder`, `test_fold_defect_regression_register_path_matches_real_naming_convention`. This is a YAML-only fix (system-test-ops/.claude/pipelines/), picked up live on the next read — no server restart needed for this part; **you can retry the failed run now** (or start a fresh Merge run) and it should get past `execute_folds`.

Full test suite passes (199/199) after this whole round.
