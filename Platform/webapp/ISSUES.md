# Test-Ops Console — issues & feedback (v5)

Previous rounds, fully resolved/answered, archived at:
- `archive/ISSUES-2026-09-resolved.md`
- `archive/ISSUES-2026-09-17-resolved.md`
- `archive/ISSUES-2026-09-21-resolved.md`
- `archive/ISSUES-2026-09-28-resolved.md`

**How to use:** just drop raw bullet points below, whatever's quickest — no template needed.
I'll read them, work out what each one actually means, fix or answer what I can, and write it
up properly myself (with a real Status line) when I pick the file up.

---

## Carried forward, not yet resolved

- **Run-status conflation: "failed" vs "waiting on you"** — a run whose overall `status` is
  `waiting_human` can actually be sitting on a **failed** CLI step several steps past the last
  human gate (real example: run `a45a020d`, onboard-suite/Translink-POS — summary described a
  succeeded step 2 steps back while the actual stopping point, `push_area[FBD-100293-product-
  group-usage]`, had failed). Anyone reading the run card looks for a confirmation button that
  isn't there. Run-level status needs to distinguish these two states.
- **Raw traceback shown in the run card for failed CLI steps** — a `cli`-kind step failure
  renders the full Python traceback with no human-readable summary line above it. Fine for
  debugging, not fine as the primary thing a non-engineer reads. Worth a one-line "what broke"
  synthesis above the raw stderr.
- **No signal on whether a failed step is worth a plain Retry vs needs a real fix** — the
  `FBD-100293` YAML failure above turned out to be a real bug (fixed 2026-09-28 — see archived
  round), but a different failure on the same suite genuinely was transient/stale. Today there's
  no way to tell from the UI which kind you're looking at before you retry.
- **Silent, near-instant agent-step failures** — an **agent**-kind step (`cross_tab`, run
  `84d39936`) failed in under a second with `output: "(the agent returned no output)"` — no
  error, no partial output, nothing to diagnose from. Whatever captures the agent's result before
  writing `failed` has a real gap here.
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
- **4 pre-existing blocking `then-compound-genuine` audit findings on Translink/POS suite
  30253** (C4109983, C4109984, C4109989, C4110000) — flagged by the 2026-09-28 push's suite-wide
  conformance audit, unrelated to that push itself. Not split yet — want these done next?
- **`system-test-ops` working tree has uncommitted content** (multiple `knowledge/translink/
  specs/*.md` modified/deleted/added, plus the in-progress `proposals/Translink-POS-suite-
  restructure/` folder) — looks like output from more than one earlier pipeline run never got
  committed. Real content, not a code bug — flag before anything gets committed/pushed on top of
  it without a look first.

---

