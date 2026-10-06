# Test-Ops Console — issues & feedback (v7)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`
- `archive/ISSUES-2026-09-28-resolved.md`
- `archive/ISSUES-2026-09-28-b-resolved.md`

**How to use:** just drop raw bullet points below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## Built/fixed this round (2026-09-28, fourth pass) — real, re-verified against live code

- **Start merged into Pipelines, for real this time** — I'd previously mis-scoped this as "Start
  already contains Setup+Ingest as one group" and left it alone; the actual ask was to eliminate
  Start as its own section entirely and fold Setup/Ingest Docs/Scheduled scan into Pipelines. Done
  now — no separate "Start" heading anywhere. Real constraint respected: these 3 pipelines were
  deliberately exempt from the setup-completion gate (you need them precisely because setup isn't
  done yet); moving them into the same DOM group as gated pipelines could have silently broken
  that. Fixed via per-pipeline-id exemption (`NEVER_GATED_PIPELINE_IDS`), verified with a real
  headless-browser test forcing an unconfigured target: Setup/Ingest Docs stayed clickable,
  Onboarding correctly stayed locked.
- **Sidebar accordions removed, always-expanded flat list** — every sidebar nav section
  (Dashboards/Pipelines/Audit/Health/Projects) is now a plain heading with everything underneath
  always visible, no click-to-open, no chevron — matching how "SIT (view only)"/"Cases" already
  worked.
- **Sidebar collapse overlap bug, root-caused for real** — the hamburger toggle was animating
  `grid-template-columns` (unreliable across browsers, worse with a `position:sticky` sidebar);
  even after an earlier attempted fix, the sidebar still rendered at a stray 32px (its own
  padding) instead of 0 when collapsed, so main content overlapped it. Fixed by removing the
  animation and forcing explicit `width:0` in the collapsed state. Measured with real bounding
  boxes via headless browser: sidebar now hits exactly 0px, zero overlap.
- **"You're on an existing suite / a fresh build, this isn't needed" warning — built.** You'd
  asked for this across at least 4 separate rounds; it kept getting flagged as carried-forward
  instead of built. Any step whose `when:` only applies to a fresh build or an existing suite now
  shows a real "not needed for this target" pill, computed from whether your current target has an
  old suite configured (the same signal `runner.py`'s own `_is_fresh_build` uses at run time).
  **Found while building this:** the database never actually persisted the `fresh_build` flag at
  all (real, separate bug — not yet fixed, see carried-forward).
- **Two pipelines had zero visible nav button anywhere** — `refresh-automation-tier` and
  `scheduled-scan` existed and worked but were unreachable from any menu. Both now wired in
  (Automation tab's Cases group, and Pipelines respectively). Only `new-suite-from-docs` remains
  deliberately hidden (documented, real reason: 136-step/65-agent-call cost for Translink).
- **Gap-register rewrite: fast per-marker option added.** The full `clarify-gaps` batch pipeline
  re-greps the whole repo and can be slow over a large scope; each gap's own detail popup now has
  a "Rewrite in plain English" button that does just that one marker, fast, writing into the same
  shared cache the table already reads.
- **Log/activity summaries: real click-to-expand**, replacing a fragile hover-tooltip, on both the
  pipeline Log tab and the Reports tab's activity feed.
- **Test-run report pipeline properly grounded** — read both real files you dropped in Downloads
  (the Arrive-branded template + a real filled Translink example), copied them to a local,
  gitignored folder (same treatment as your other confidential specs — never committed), and
  wrote a real structure doc (`docs/test-run-report-template.md` in system-test-ops) citing the
  actual section order and table shapes from both, including the real behaviour of omitting empty
  sections rather than padding them. The drafting step now follows that exactly.
- **The 4 "carried forward" blocking audit findings on suite 30253 are actually already fixed** —
  checked directly just now: suite 30253 audits CLEAN, 0 blocking findings. They were part of the
  same 12-case batch fixed earlier this session; I'd just never removed the stale line from this
  file. Corrected here, not carried forward any more.

Also fixed earlier the same day (still live, re-verified): JIRA pipeline rename ("Cross-Check
JIRA"), multi-select document picker for `only_file`, Reports tab's tool-activity+AI-cost
additions, Automation "Tests written" repo-tree view, Functional/Design docs split, `flow_data_path`
auto-resolution, SIT-mirror staleness banner, `test-automation-sit` added to the Repo Map, the
`consolidate`/`fold-defect` missing-file-placeholder bug, and the step-by-step guide's jargon-strip
+ list-numbering bug + accordion.

Backend: 209/209 webapp tests pass. Everything above verified against the actual running server —
not just claimed.

---

## Real gap found and fixed (correction to what I first reported)

- **`fresh_build` had no real database column** — flagged last round as a live user-facing bug (the
  edit form's checkbox "will always show unchecked on reopen"). That specific claim was wrong; I
  hadn't checked the frontend before writing it. The edit form already derives the same fact a
  different, equally-reliable way (`!old_suite` — old_suite is only ever empty when fresh_build was
  true, enforced by validation), so the checkbox always round-tripped correctly in practice. The
  underlying gap was real, though: no actual column existed, so nothing else could ever read this
  fact directly. Fixed properly — a real `fresh_build` column, migration, and both directions
  (`upsert_suite_mapping`/`list_suite_mappings`) wired through. New test:
  `test_fresh_build_flag_actually_persists_as_its_own_column`.

## Naming/IA — resolved this round

- **Audit + Health merged into "Checks"**, flat list (your answer) — all 11 pipelines (Audit's 4 +
  Health's 7) under one heading, no sub-sections. Verified live.
- **Onboarding renamed to "Build suite"** — clearer against Update from docs; every cross-reference
  string updated too (Update from docs, Feature, ingest-docs' "what's next" text, etc.), not just
  the sidebar label. Verified live.

## Naming/IA — still open

- The umbrella ask: review every remaining pipeline/option's naming against its real scope, now
  that the bigger structural moves (Start merge, Checks merge, Build suite rename) are settled.

## Built this round — dashboard charts + coverage confidence score

Per your answers (live snapshot now, all 4 charts, all 3 confidence inputs):
- **Suite health breakdown chart** and **Gaps by device chart** — real inline SVG bar charts on
  the Health page, built from the same real run-health/gap-register data the tables above them
  already showed as raw numbers. Status colors reserved for real status meaning, never reused for
  identity.
- **Coverage confidence score — built, all 3 inputs you picked, equally weighted.** Real numbers,
  not fabricated: 41.4% of suite 30253's 944 cases carry a real spec citation (`refs` field);
  99.4% aren't behind an open GAP/UNCONFIRMED marker (6 open, scoped to Translink/POS); 2.9% are
  referenced from an actual `.robot` test (regex-matched `C\d{6,7}` case ids in real, non-reference
  Documentation fields — 27 of 944 suite cases matched). Confidence = 48%. **Correction to my own
  earlier note in this file**: I'd previously called "manual vs. automation coverage" blocked —
  wrong, TestRail case ids are already mechanically extractable from `.robot` files today, no new
  prerequisite work needed. Shown as a breakdown table, never a bare number, and the automation
  number is shown honestly low (2.9%), not spun. Same fixture convention as build-stats/run-health
  (POS/Translink only — the one target with real captured data); new `/api/confidence-score`
  endpoint, new test, verified live via headless browser on the real running server.

## Built this round (low-priority items + flow diagrams)

- **Sidebar nav icons + icon-only collapsed rail, built together** — you clarified these were
  linked ("this means the side bar should stay slightly visible with icons only when closed
  right"). Every nav item now has a real, meaningful icon (not decorative); collapsed state is a
  genuine 56px icon-only rail, not fully hidden — verified live: sidebar hits exactly 56px, main
  content starts at 56px (no overlap), icons stay visible, labels/headings/chevrons hide.
- **Visual flow diagrams of pipeline mechanics — built.** You were right that this needed no new
  data: real inline SVG per pipeline, one node per real step in real order, colored by real kind
  (same CODE/AI/GATE/HUMAN palette the pills already use), a dashed connector + "if `<condition>`"
  label wherever a step's own real `when:` gates it, a loop badge wherever `loop:` fans it out.
  Never a fabricated branch. New collapsed-by-default accordion on every pipeline detail page.
  Verified live (Feature/add-feature): 6 real step nodes, correctly connected, zero errors.

## Carried forward, not yet resolved

- **Run-status conflation: "failed" vs "waiting on you"** — a run whose overall `status` is
  `waiting_human` can actually be sitting on a **failed** CLI step several steps past the last
  human gate.
- **No signal on whether a failed step is worth a plain Retry vs needs a real fix**.
- **Silent, near-instant agent-step failures** — no error, no partial output.
- **Manual-edit-only "observed changes" scoping**, and **review/approve manual edits inline**.
- **Docs ingest status — per-document breakdown** within a run.
- **Existing-suite mode's own toolset** (non-docs-driven "just edit this suite" mode) — largely
  superseded by `update-suite-from-docs` for the docs-driven case; the "no need for this" warning
  built this round covers part of the original ask too.
- **Test provenance — manual vs. Claude-written** — no reliable signal today.
- **Features layout — named conceptual-area taxonomy** doesn't exist as a field yet.
- **Gap Register sync → re-audit/re-edit pipeline** — needs pipeline-execution-from-console
  plumbing every disabled "Run" button is already waiting on.
- **`system-test-ops` working tree has uncommitted content** — flag before anything gets
  committed/pushed on top of it without a look first.
- **Put the "waiting on you" action under each step in the SAME left-hand column as its static
  description**, not a separate right-hand column — deferred, real layout refactor.
- **JIRA/automation-knowledge cross-examination inside Feature** (`add-feature`) — today it
  cross-examines against the suite only.
- **Deeper per-status run review** (pass/fail/retest/invalid breakdown + defect-linking).

---

## Built this round — blocking bug fix + Gap register rebuild (2026-09-29)

- **BLOCKING bug fixed: stale converted-doc cache.** `ingest_docs.py` only ever added/
  overwrote `_text/*.txt`, never removed one whose source doc no longer exists in `--src`
  -- so replacing your POS library with 3 new files still left the *old* 131-file library's
  converted text sitting there forever, and the relevance check scored all of it. Now a
  full (non-`--only`) run reconciles `_text/` to exactly match the current `--src`. Verified
  against your real data: your `_text/` folder went from 131 files to the real 3; relevance
  check now correctly runs against just those 3, "All relevant. Nothing flagged."
- **Gap register rebuilt** — single flat list, current project+device only, no more
  project/common/bespoke tabs. Two real bugs found and fixed along the way:
  - **Confirmed the cross-device leak was real** ("Im pretty sure the gaps related to all
    things translink... even though im targeted POS") — the old default scope showed every
    device mixed together. Verified live: Translink/POS and Translink/ETM now return
    genuinely different, correctly-scoped totals.
  - **Found while adding the live "Refresh" button**: the gap-register CLI's scan doesn't
    exclude archived/superseded folders, so archiving Translink POS's old knowledge notes
    into `_archive/<timestamp>/` earlier this session made 82 *stale* markers from those
    archived files suddenly count as current open gaps. Fixed at the source
    (`system_test_ops gap-register`), not papered over in the console.
  - **"Rewrite in plain English" removed** (both the per-gap and whole-scope buttons) —
    replaced with a real **"Explain more"** button that asks the Ask box's live grounded
    agent about that specific marker, rather than just rewording its existing text.
  - **Real "↻ Refresh against new docs" button** — runs the actual gap-register CLI live
    (cheap, read-only, ~1-3s), not a re-fetch of a frozen fixture.
  - Rows now have a visible **"Open →"** button, not just an implicit whole-row click.
  - Verified live end-to-end: real refresh dropped the repo-wide count 1354→1272 (removing
    exactly the 82 archived-folder markers), POS-scoped 37→23, correctly excluding stale
    content throughout.
- Small terseness pass: Change Target's git-status messages shortened (per your "make all
  descriptive text briefer, no fluff" ask) — full sweep of every page's descriptive text is
  still queued below, this was just the one you named directly.

**Not yet started this round** (queued next, in order): pipeline-info page simplification +
separate Flows section, docs/ingest single-upload overhaul, Dashboards→Admin rename,
Knowledge page removal, the dashboard-staleness-after-remap bug, the green setup-status
banner overclaiming a live check it never ran, removing the guardrail/rule pills
(`no_gap_fabrication` etc.) app-wide, and the rest of the raw batch below.

---

## Built this round — the rest of the "smash it out" batch (2026-09-29, continued)

Real, itemized status against every bullet below — you asked me to re-check this multiple
times against the live app, not just claim it, and I found real problems doing that (listed
under "Found and fixed mid-round").

**Done, verified live:**
- Dashboards → Admin (sidebar label).
- Knowledge page removed entirely — nav item, `renderFeatures`, `/api/features`, and its
  test all deleted (nothing else in the app depended on it — checked first). Your stated
  reason ("eats tokens keeping it up to date") was actually wrong — it was a static,
  manually-curated seed file, no AI cost — but the page had no real use either way, so
  removed as asked.
- Rule/guardrail pills (`no_gap_fabrication` etc.) removed everywhere — per-step Rule/
  Guardrails lines, the pipeline-level guardrail chip row, and the CODE/AI/GATE/HUMAN "key"
  legend blocks (2 of them) all gone.
- Flow diagrams **out of every individual pipeline page** — moved into a "Flows" tab inside
  "How to's" (nee Pipeline Info), which **replaces** (not duplicates) the old tab there —
  that old tab was a pure duplicate of Automation → Flows (literally the same function),
  so nothing was lost, just de-duplicated.
- "How to's" → Processes tab: no more accordion, no more "How to get started"/"Once set
  up"/"Maintenance" lifecycle grouping — now reuses the exact same Build/Checks grouping the
  sidebar itself uses, so it can't drift from what the sidebar shows. A row no longer
  expands into a step list; click it and you're on that pipeline's real detail page.
- Pipeline detail page's "How to run this": accordion gone, dropped the "Before you
  start"/"Where results land"/"What's next" clutter sections, kept just the real
  step-by-step guide, always visible (the guide's own prose itself is unchanged — that's a
  content-authoring task per pipeline, not a template fix, flagged separately below).
- "What's next" line kept, but as one small line under the description, not its own section.
- Gap register: single list, current project+device only, "Explain more" (real, via the Ask
  box) instead of "Rewrite in plain English", real live Refresh button, visible "Open →" per
  row. (Built last round, re-verified still correct this round.)
- Green "already done" pill for a per-pipeline last-run — was a full-width card, now a small
  pill.
- Green "fully set up" banner — now runs a real live connection check before ever showing
  green; shows an honest amber "saved locally, not verified live" state otherwise.
- Change Target's git-status messages shortened.

**Found and fixed mid-round** (real regressions/bugs from THIS round's own work, caught by
re-checking against the live app per your ask, not just re-reading the code):
- **Regression**: rewriting the Processes tab dropped the "hide certain pipelines" exclusion
  entirely — `new-suite-from-docs` (deliberately hidden, real reason: 136 steps/65 agent
  calls for Translink) reappeared, and 4 Automation-tab pipelines that already have their
  own nav buttons started showing again in a stray "Ungrouped" bucket. Fixed: exclusion
  restored, verified live — "How to's" now shows exactly the same 19 pipelines as before,
  zero stray "Ungrouped" section.
- **Real CSS bug, caught via an actual screenshot, not just a code read**: the new
  "STALE suite mismatch" banner (built last round) visually fell apart — `.fixture-note`'s
  base CSS is `display:inline-flex` (built for short one-line pill badges); a longer
  message with embedded `<b>` tags got each tag treated as its own flex item, fragmenting
  the sentence into a broken multi-column layout instead of normal prose. Fixed with a
  `display:block` override; re-screenshotted, now reads as one normal paragraph.
- Misread my own earlier build: initially added a brand-new **top-level "Pipeline Flows"
  nav item**, misreading "flows in pipeline info" as wanting a new nav section. Caught it,
  reverted, and did what you actually asked — flow diagrams live *inside* the existing
  Pipeline Info/"How to's" page's own tab bar, not a new sidebar entry.
- Confirmed live: the STALE banner is genuinely firing correctly right now — you've
  re-pointed Translink/POS to a new real suite ("Agentic Translink POS", 30607) as part of
  your own parallel re-onboarding work, and the banner correctly flags every fixture-backed
  number on the page as stale for that new suite. Also confirmed a Gaps-page row citing
  `knowledge/translink/specs/FBD-100183-pos-hardware.md` is NOT stale data leaking through —
  that file was genuinely re-distilled today (real, different content from the archived
  version), so the refresh correctly picked up your fresh work, not old content.

**Explicitly not done yet** (real, sizeable items still queued, in rough priority order):
- Docs/ingest single-upload overhaul (drop the docs-source picker, one upload method, a
  last-ingested timestamp instead) — the confirmed shape from earlier, not yet built.
- Bulk delete on the docs page; archive-instead-of-delete for docs; "where did my docs go"
  scoped to only show after a successful ingest; a docs-count overview widget.
- Change Target modal's popup overflow (goes beyond screen top/bottom when editing a pair).
- Sidebar collapsed-rail icon padding + scrollbar styling.
- Design docs in Settings — still needed now that specs are the flow/design source? (open
  question, not investigated).
- Scheduled checks — against a centralised doc location, or just internal uploads? (open
  question, not investigated).
- Sub-title text wrapping at ~40% width instead of using more space near the Run button.
- Log summaries as a popup, not an accordion.
- Bigger pipeline-page layout change (pills/prompt left-right, steps/results side-by-side).
- Results shown as a plain-English pass/fail summary with an expandable multi-issue list.
- Human-check steps given real, specific guidance on what to actually check (currently just
  "waiting on you" with no direction).
- POS suite naming/ID drift check against TestRail (not investigated).
- The per-pipeline walkthrough guides' own prose is still fairly dense in places — the
  container is no longer an accordion, but shortening the actual authored text per pipeline
  is separate follow-up work, not done this round.

Backend: 214/214 tests pass. Every item marked "done" above was verified against the actual
running server (headless-browser DOM checks + 2 real screenshots), not just claimed.

---

## Built this round — working through the queue (2026-09-30)

- **Change Target modal overflow — real bug fixed.** The modal had no max-height/scroll at
  all, so a long form (e.g. "Add project") could extend off-screen with no way to reach
  Save/Cancel. Fixed generically for every modal using this class (header/footer stay
  fixed, only the body scrolls). Verified live at a small 1200×600 viewport — modal now
  fits, Apply button stays visible.
- **Sidebar collapsed-rail padding + scrollbar** — bumped the collapsed rail 56px→62px so
  the extra padding is real breathing room, not just squeezing the icons smaller. Nav-list
  scrollbar themed to blend into the dark sidebar (thin, translucent white) instead of the
  default light-grey OS scrollbar.
- **Pipeline-page sub-title wrapping — real bug fixed.** The description column had no
  flex-grow and the paragraph itself had a hardcoded `max-width:64ch`, so it wrapped early
  even with a wide empty gap before the Run button. Fixed: the column now actually fills
  available width up to the button.
- **Log summaries now open in a real popup**, not click-to-expand-in-place (which just
  crammed the full text into the same ~300px-wide table cell it was truncated in).
- **Docs page rebuilt**: a real overview (docs on file, last uploaded, last ingest-docs run
  — no separate call needed, derived from data already fetched); the hard-delete "Remove"
  button is gone, replaced by checkboxes + one "Archive selected" bulk action reusing the
  exact same never-delete archive machinery the knowledge-archive card already used;
  "Where did my docs go?" now only shows once Ingest Docs has actually succeeded for this
  target, with a direct link to run it otherwise.
- **Two open questions, answered with real evidence, not just opinion:**
  - **Design docs — still needed, not redundant.** `flow_data_path` feeds a genuinely
    different, structured Overflow-JSON screen/annotation extraction
    (`tools/extract_overflow_annotations.py`) that prose knowledge/specs notes can't
    provide. Nothing has superseded its role in `onboard-suite`.
  - **Scheduled checks check the centralised synced folder**, not just internal uploads —
    confirmed via `runner.start_scheduled_scan` → `store.resolve_ingest_docs_source`, the
    exact same resolution manual Ingest itself uses (synced folder first, uploads bucket
    only as a fallback).
- **POS suite naming — real live "Check names" feature built**, not just a one-off answer.
  Confirmed right now there's no drift (both old suite 9317 and new suite 30607's stored
  names exactly match TestRail), but built the actual live check George asked for
  ("ensure the naming is correct... or refresh if been changed") rather than leaving it as
  a point-in-time answer that goes stale: a new `/api/suite-name-drift` endpoint (one cheap
  `list-suites` API call, not a full case download) plus a "Check names" button per row on
  Settings' suite-mappings table, verified live against real TestRail data.

**Found in passing, not fixed (separate, pre-existing issue, noted for later):** historical
run summaries stored in the database have mangled characters (mojibake) in a few places —
spotted in a real screenshot of the Reports tab's activity feed. Same general class of bug
as the connection-check encoding fix from two rounds ago, but in a different code path
(likely `_run_agent_step`/`_run_cli_step`'s own subprocess calls not pinning
`encoding="utf-8"`) — needs its own investigation, not touched this round.

Backend: 216/216 tests pass. Every item above verified against the real running server —
live curl calls, headless-browser DOM checks, and real screenshots at both normal and
constrained viewport sizes.

---

## Corrections — two real misses from the last round, fixed properly (2026-09-30)

You were right on both counts:

- **"How to run this" — genuinely rewritten this time.** The earlier fix only removed the
  clutter sections around it; the guide text itself was still the full `.claude/commands/
  *.md` prose (written for an AI agent to execute, not a person skimming a page). Now a
  real, curated, terse rewrite — one short plain-English sentence per real numbered step,
  same exact style as Docs Upload's numbered list, for all 16 pipelines that have a real
  command doc. Grounded in and traceable to that doc's own real steps, nothing invented.
- **Flow diagrams + step pills — brought back, redesigned per your sketch.** You shared a
  hand-drawn wireframe: pill-shaped step nodes in wrapping rows at the top of each
  pipeline's own page, then a two-column layout below (how-to + step pills + live run
  progress on the left; prompt + results on the right). Built exactly that:
  - New compact pill-row flow diagram, colored by kind (CODE/AI/GATE/HUMAN), wrapping onto
    further rows for pipelines with more steps — verified live on `onboard-suite` (14
    steps): wraps correctly onto a second row, arrows connect correctly across the wrap.
  - The static step-pill list (kind pill + step id + description) is back, now always
    visible in its own "Steps" card, not deleted.
  - Real two-column grid: left = how-to guide → Steps card → live Run progress card; right
    = pipeline inputs → Prompt field → Results card. The heavier box-and-arrow diagram (with
    conditions/loop badges) is still available via "More detail on this flow →", in the How
    to's page's own Flows tab, for anyone who wants it.
  - Small polish caught while rebuilding: the live run-progress card was ALSO titled "Steps"
    — same heading as the new static card sitting right above it, reading as duplicated.
    Renamed to "Run progress". Also dropped a redundant duplicate description line that
    became more noticeable once the page got cleaner.

**Flagged again, not yet fixed:** the mojibake (mangled character) bug in stored run
output/summaries — now seen twice, in two different places (Reports tab activity feed,
and an `onboard-suite` run's failure message shown in this round's own screenshots). Real,
recurring, needs its own investigation — likely the same subprocess-encoding class of bug
already fixed for the connection-check, in a different code path that writes run
summaries/output to the database.

Backend: 216/216 tests pass. Verified live via real screenshots (not just DOM checks) on
`ingest-docs`, `add-feature`, and `onboard-suite` (the wrap-testing case).

---

## Built this round — persistent console panel + layout removals (2026-09-30)

- **Removed:** the "More detail on this flow" link under each pipeline's pill diagram, the
  whole "Flows" tab in How to's (was a second, heavier version of the same diagram — pure
  redundancy once the pill row existed), and the "UX flow data" status card on Build suite.
  The underlying Design-docs capability is untouched — just this page's own status card
  about it is gone. `renderFlowDiagram` (the box+arrow SVG) and its remaining wiring
  (`PIPELINE_FLOW_PRESELECT`, `data-goto-flow`, `data-goto-settings-design`) removed as
  fully-orphaned dead code, not just hidden.
- **Real persistent console panel, built like you asked** — a genuine VS Code/PyCharm-style
  docked panel: `position:fixed` to the viewport (not the scrolling content), open by
  default, collapsible, sitting above the sidebar's real width at both expanded and
  collapsed states. Run progress + Results now live inside it — same real elements/ids
  every run/poll/cancel/resume function already used, just relocated, so none of that logic
  needed to change. Verified live: scrolling the page 400px did not move the panel at all;
  a real resumed run (`onboard-suite`, genuinely `waiting_human`) renders correctly inside
  it, including its live "Continue" button.
- **"Steps" vs "Run progress" — no more duplicate-looking cards.** They're genuinely
  different things (the static step list vs. the live per-run status), now labeled as such.
- **Two-column layout no longer forces equal-width gaps** — was a rigid CSS grid
  (`1fr 1fr`) stretching both sides to the same width regardless of actual content; now
  flex-wrap with a sane minimum, so a short card doesn't get stretched and a tall one
  doesn't get squeezed — they only sit side by side when there's genuinely room.
- Dropped a stray duplicate description line (PIPELINE_PLAIN vs. `detail.description`
  showing near-identical text back to back) while it was in front of me.

**Flagged a third time now, still not fixed:** the mojibake bug in stored run output —
seen again in this round's own `onboard-suite` screenshot. Real, recurring, needs its own
dedicated investigation pass.

Backend: 216/216 tests pass. Verified live: scroll-independence, toggle behaviour, real
run content rendering correctly inside the relocated panel, wrap behaviour on a 14-step
pipeline (`onboard-suite`).

---

## Built this round — How to's list rows get an accordion + a real link (2026-09-30)

Each row in the Processes list now does both things you asked: clicking the row header
toggles an inline accordion showing the exact same curated 1-2-3 terse step guide the
pipeline's own page shows (never a second, separately-drifting copy), and a real
"Open pipeline →" link inside that accordion takes you to the actual detail page. Verified
live: toggled Setup's row open, saw its real 3-step guide inline, clicked through, landed
on the real Setup pipeline page.

Backend: 216/216 tests pass (no backend touched this round — pure frontend).

---




NEW::

(actually - lets make it simpler, lets remove flows from pipeline info entriely, 

- Flow diagrams to be inside the flows in pieline info not inside each pipeline sorry. Remove from pipelines and remove how flows currently look in pipeline info - make it so that we have a simple easy way to navigate through each pipeline and see it in a flow diagram
- Pipeline info lets change how it looks make it simpler. (processes) lets just have no accordion showing the actual steps here, just a 1-3 sentence description of what this process, pipeline does, then the flows will show the actual flow and steps of each one. 
- I think remove the accordions with like how to get started, lets just structure it the same as the menu side bar? yes. only the pipelines have flows, and like ai, human, code etc. but the rest can just be a simple 1-3 sentence description of what it is - this is basicalyl going to be - all info on each part of the tool, and a flow diagram of the pipelines on the flows. 
- Everywhere do we really need those like key pills? they dont help with anything, you know AI / judgement with purple dot, not need, i like the ones alongside the tool name, with number there good.

- Change menu dashboards name to Admin
- The status dashboard needs to be like wrapped? so no gaps, if one dashboard has more content or less, then it should all be pushed to fit alognside each other right? well or underneath basically no gaps
- POS TL suite name new one, is GG - POS - Claude Suite but on testrail it is something else? do we need to ensure the naming is correct for the ID or refresh if been changed


As i go through the process:

- Adding a new pair, after deleting the pair for Translink POS - the dashboard stays the same? suppose this always stays the same for data in the past - even with an archive or the knowledge and doing a fresh doc update type thing?
- Maybe we need a way to bulk delete files on the docs page - as im removing all docs for it before ingesting and uploading new ones
- I like how easy to read the upload docs step by step is for the upload button lovely, take note as this is the neat and tidy step by step i like when i ask for these things
- If i can remove docs, why do i need to archive? should we ust have one option really? archive probably safer more secure right? to just do that instead of removing the doc
- where did my docs go, should only really be relevant once i have done ingest-docs right and maybe on that page when ingest docs has been successful.
- Requirement docs, check for changes descriptive text needs updatng, please make all descriptive text for each function everywhere be so much breifer, pin pioint and to the point no fluff
- remove this text Target list has local changes not yet committed — commit system-test-ops/knowledge/suite_targets.yaml so others can see any target you added. from change target
- a OVERVIEW OF THE amount of docs currently being used, newly uploaded for the targeted project, device would be good though to give you insight oh i need to upload or oh theres loads of info better go check it.
- dont like when you open up edit this pair of add project, remove pair it makes the pop up go beyond the top and bottom of the screen and hard to view, do we need a better way to display? maybe a 2nd pop up above the current pop up but slightly up and to the right so you can see both pop ups? so we can add, edit pairs etc. otherwise really hard to use the change target pop up when it goes beyond the screen dimensions
- do we need design docs in the settings anymore? now we are using the specs as a flow, design area? with the specs now. 
- I dont like the scroll bar on the CMS sidebar menu panel? can we blend the colours of it? or find a way to make this easier? when you close the side bar menu and you can see the icons, there quite squeezed in, the paddlign left and right needs to be a tiny tiny bit bigger, so that even the arrive logo is still not so squeezed including
-  Dashboard defo still shows the other suite targeted not the now newer one for Translink POS
- I think we can remove the knowledge page entriely? as its all files inside the repo anyway right. will eat up tokens trying to keep it up to date all the time when the knowledge is in the files, you dont need this page for anything do you?
- Change pipeline info name to How to's
- The scheduled checks are run again a centralised location of docs or just the internal uploaded docs?
- rewrite the gap in plain english is annoying right? as it forgets about the gap after a long time, so for future maybe we need to ensure the plain english is written from gaps alreayd, then we can just remove the re-write option on this page. And tbh we probably dont need all the device, common, bespoke gaps either just one list for the currently selected project, device
- be good to have a not re-write english button when clicking on a gap, but more of a - can you explain more button so you get more info or something?
- Im pretty sure the gaps related to all things translink? or there is a bug when opening a gap and it shows translink ETM? even though im targeted POS
- We should only show gaps for that project and device, and we need to be able to re-check these gaps against new specs uploaded, so a refresh button (or resolve? well not resovle thats comments and answers right, we need a way to after uploading more docs and gaining more knowledge do that asesment right if now gaps are resolved by the new docs?
- The gaps need a select button on them? so people can see they can be selected.
- Get rid of the flow diagrams on all pipeline pages
- how to run this is sooooo big and so uneccessary, again i like the docs upload one, so easy to read, one tiny sentence per number of step? and doesnt need to be accordion.
- can we make the green banners a small pill when a project, device has a successful pipeline already run.
- My csettings arent fully configured though right, may have been checked on claude code but not on the tool so maybe the green banner shouldnt be green and more of a warning the tool doesnt se the check being done.
- The title, and sub title text, are good, but the sub title descriptive text on every page seems to be wrapping at like 40% of the page? we could fill it out a bit more and be like 40px away from the button "run" this may free up more visual space for more to be seen.
- Log summaries should open in a pop up not an accordion as wanna fit it all on a summary pop up.
- thinking a change of layout for the pipeline pages, i want the code, ai, human pills steps to be on the left, then the what your trying to achieve field for a prompt on the right side by side with it, then i want the steps when your running the tool to show on the left under the pil lsteps and side by side with the results on the right side of it. 
- We need to make our results better right, I reckon it could be a bit more of plain english quick to the point sumary of the result, failed or passed. obvi the raw output is good to open up. But sometimes you might hit multiple issues right? we should pill these out in a bullet point list so you can open each result if multiple.
- Ingest docs is alot of crappy jargon areas. which documents changed is pointless? think i wanted to just have a quick way to upload a new doc straight to the ingest docs not pick old docs to go through. maybe we dont need this. 
- Maybe we only need one method of uploading docs. and i think the which docs should this run read is annoyingly bad in terms of how we structure this. Maybe we just need a timestamp on the target at the top with like Last doc check / run / ingest or something? that states and reminds users this is the last time docs were updated for this target, so if that was 2 months ago but they know new docsu pdated 2 weeks ago then yes maybe i should re-ingest the docs or check them. I dont know just seems silly to have upload docs in multiple areas, and clunky to have to change which docs to run against? which to choose? when its spec truth of source for the device and project never really changes only maybe updated to it, which will come with the scheduled checks and re-ingesting right? let me know your thoughts here
- we should be ingesting new docs, or the docs uploaded right against the synced folder confused here?
- check relevant went against 131 converted docs even though i removed them all and have uploaded 3 files now? so somethings broken there.
- These human checks, there slghtly annoying because were not actually doing anything? we have no direction most of the time on what we should check? sync_check waiting on me? what am i checking? this is the things we need to relay to the humans using the tool
- running a ingest docs but pretty sure its not doing it right against the newly uploaded docs, again were defo a bit embaressingly bad at how wweve thought this doc structure, like we need better smooth process to upload doc,s ingest them, keep the knowledge, but if i change the docs, remove them, upload the same ones, upload differetn ones, upload one more doc to go on top all this should be smooth
- BLOCKED HERE due to this, need to ingest the new POS docs
- all the puills like no_gap_fabrication not needed, just remove, dont care about these anywehre.
- NEW (George, 2026-09-30): if a doc genuinely covers multiple devices for one project (e.g. Translink-Device-Endpoints-STE12.docx, spans ETM/HHD/PV/GV/POS), and it's later uploaded again for a different device target, ingest-docs has no memory it was already distilled -- convert + distil both re-run from scratch on the same file, real AI cost + risk of drift from the notes already sitting in knowledge/{project}/specs/. Needs a "already distilled this exact file/version for this project?" check before distil runs, not a re-run every time. Confirmed real (checked tools/ingest_docs.py directly -- no hash/dedup memory across runs at all, only within-one-run version-family de-dupe).
- 
  **Status (2026-10-06): fixed in `system-test-ops/tools/ingest_docs.py`.** Convert now hashes each source file (SHA-256 of the content, any folder or device), keeps `_ingest_manifest.json`, and writes `_text/_to_distil.json` listing only new or changed docs; docs already distilled at that exact content are converted but skipped by distil. New pipeline step `mark_distilled` stamps them after distil. `--force` re-distils on purpose. Tested on a scratch folder: same file from another device folder skipped, edited file re-queued. Not yet run through the console on the real POS docs.

- **NEW (George, 2026-10-06): revamp the automation dashboard toggle area into a live, visual runs view; and bulk out Reports.** Not started. Wants:
  - a visual way to see runs, pipelines in progress, passes and fails as they come in; a live running log of the pipeline; easy to see which test is running right now and whether it passed or failed, all pulling through in real time;
  - how many tests are in a run, the schedule time, and the ability to change the schedule from the tool;
  - set up a targeted run by choosing the tags to include;
  - end goal: used company-wide (projects, testers, automation) to see stats, data and runs in real time;
  - same for Reports: keep adding many quick, narrowed-down reports and dashboards for most of what the tool and automation do.
  - Depends on: sit's results ingestion (see the SIT results dashboard plan; results upload is off in sit today). Single-user local console today, so "company-wide" is the shared-service jump flagged earlier (credentials store + uploads need the multi-user redesign first).

- **Status (2026-10-06):** removed the "Uncommitted local target changes" text from Change target. Audit of the rest of this list against the code: most items are built; still open are human-check guidance, ingest-docs simplification (needs a decision), better results (plain-English verdict + a pill per issue), gap re-check against new specs, Design docs in Settings (needs a decision), pipeline-page 2x2 layout (needs a decision), stale-dashboard approach (needs a decision).
