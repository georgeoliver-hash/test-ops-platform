# Test-Ops Console — issues & feedback (v6)

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

## Built this round (2026-09-28, third pass) — real answers, tested, live

- **JIRA pipeline renamed** — `audit-coverage` is now "Cross-Check JIRA" everywhere (nav, detail
  page, cross-references). Confirmed with George.
- **Bulk document selector, real multi-select** — `only_file` is now a real checkbox tree of
  every actual file in the resolved docs folder (select/de-select any number), not a single
  dropdown. `tools/ingest_docs.py --only` now accepts a comma-separated list server-side, same
  day. New tests: `test_only_accepts_multiple_comma_separated_files`,
  `test_only_reports_a_clear_error_when_one_of_several_files_is_missing`.
- **Test-run report pipeline: real groundwork, not the final thing** — new
  `generate-test-run-report` pipeline (pulls a suite's real recent run data, drafts a plain
  honest summary). Its drafting step explicitly says not to invent a layout — waiting on the
  real template/example report(s) George is supplying separately; the step's own note will be
  rewritten to match once that lands.
- **Reports tab correction** — earlier this session I wrongly called this "an empty placeholder
  pill, not wired to anything." False — it already had real generated-reports listing + preview
  + a live build-stats summary. What was actually missing (per "can we not do all of it"): now
  added — a tool-wide **"Tool activity" feed** (every real run, any pipeline/project/device, new
  `/api/runs/recent` + `store.get_recent_runs`) and the **AI-cost widget** (reused as-is from the
  dashboard). All three now sit together on one page.
- **Repo-click-through test viewer, built now** — "Automation tests written" is a real project →
  device → suite-file tree now (same visual pattern as the Repo Map), collapsed by default; a
  suite's case list only renders once you click into it — no more full bulk dump.
- **Gap/unconfirmed text rewritten in plain English, real batch pass** — new `clarify-gaps`
  pipeline + a "Rewrite in plain English" button on the Gaps page, scoped to whatever
  scope/project/device is currently active. Rewrites are cached (keyed by file+line) and merged
  into `/api/gap-register` automatically; it only ever rewords, never answers (that's still
  Resolve/`resolve-gaps`). Grounded strictly in each marker's own existing text.
- **Functional docs / Design docs split, built** — real, separate upload bucket ("Design docs":
  Figma exports, Overflow JSON, screenshots, anything UI/UX-visual) lives in a new Settings
  section, same place as credentials/suite-mappings. `flow_data_path` is gone from Onboarding's
  editable fields entirely — it auto-resolves from the first real `.json` file in that target's
  Design docs folder, same "system-resolved, not hand-typed" treatment `docs_path` already got.
  Existing Functional docs (the original Docs page) are completely untouched — a different,
  unmoved storage path, so nothing already uploaded got silently orphaned.

Backend: 206/206 webapp tests pass, 12/12 pipeline-model tests pass. All of the above is live on
the running server (verified via a real port check, not just a restart command's exit code).

---

## Naming/IA — still waiting on you

- **Start / Setup / Ingest Docs merge** — you said yes, but these are *already* one sidebar
  group today (the `Start` accordion already contains both). Confirm: is the current structure
  actually what you meant, or did you want them combined into one single *page* (not just a
  shared accordion header)?
- **Audit + Health merge** — you said yes. What should the merged group be called, and should
  Audit's 3 pipelines and Health's 6 sit flat under one header or as two visible sub-sections?
- Distinguish Onboarding vs. Update from docs more clearly — e.g. "re-examine whole suite" for a
  full re-onboard vs. today's split.
- The umbrella ask: review every remaining pipeline/option's naming against its real scope, once
  the above are settled.

## Workshop now (per your answer) — dashboard charts + coverage confidence score

Not yet designed — see chat for the actual discussion; recording the real open questions here so
nothing gets lost if we don't finish in one sitting:
- **Dashboard charts**: which numbers actually deserve a chart (case counts over time? gap
  trend? run pass-rate?), and what's the data source for each — a snapshot-over-time view needs
  history that may not exist yet for most projects (only Translink/POS has real captured data).
- **Coverage confidence score**: what should feed it (gaps open, cases stale/never-run, spec
  citations present) and how should it weight them — a single number needs a real, defensible
  formula, not an arbitrary blend.

## Carried forward, not yet resolved

- **Run-status conflation: "failed" vs "waiting on you"** — a run whose overall `status` is
  `waiting_human` can actually be sitting on a **failed** CLI step several steps past the last
  human gate. Run-level status needs to distinguish these two states.
- **No signal on whether a failed step is worth a plain Retry vs needs a real fix**.
- **Silent, near-instant agent-step failures** — an **agent**-kind step can fail in under a
  second with `output: "(the agent returned no output)"` — no error, no partial output.
- **Manual vs. automation coverage %** — blocked on real prerequisite work: TestRail case ↔
  `.robot` test linkage is free-text today, not a structured tag.
- **Manual-edit-only "observed changes" scoping** — needs TestRail's `updated_by`/`updated_on`
  per case, or this tool tagging its own pushes.
- **Review/approve manual edits inline** — depends on the item above existing first.
- **Docs ingest status — per-document breakdown** — which *specific file* passed/failed within a
  run still isn't tracked.
- **Existing-suite mode needs its own toolset** (non-docs-driven "just edit this suite" mode) —
  largely superseded by `update-suite-from-docs` for the docs-driven case.
- **Test provenance — manual vs. Claude-written** — no reliable signal today.
- **Features layout — named conceptual-area taxonomy** doesn't exist as a field yet.
- **Gap Register sync → re-audit/re-edit pipeline** — needs pipeline-execution-from-console
  plumbing every disabled "Run" button is already waiting on.
- **4 pre-existing blocking `then-compound-genuine` audit findings on Translink/POS suite 30253**
  (C4109983, C4109984, C4109989, C4110000) — want these done next?
- **`system-test-ops` working tree has uncommitted content** — flag before anything gets
  committed/pushed on top of it without a look first.
- **Put the "waiting on you" action under each step in the SAME left-hand column as its static
  "what it does" description**, not a separate right-hand column — deferred, it's a layout
  refactor of the live-polling architecture other fixes depend on.
- **Visual flow diagrams of pipeline mechanics** (distinct from the text-based per-step guide) —
  would use the diagramming skill.
- **Sidebar nav icons** per accordion item.
- **JIRA/automation-knowledge cross-examination inside Feature** (`add-feature`) — today it
  cross-examines against the suite only; automation knowledge too is a separate extension.
- **Deeper per-status run review** (pass/fail/retest/invalid breakdown + defect-linking) beyond
  what History (`review-runs`) already covers.

---
