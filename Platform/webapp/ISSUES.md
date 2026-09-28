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

- Side bar menu, when closing it, theres a wierd overlay of text\? its like the paddling left or margin left of the text content just moves outside or rally close to the left side of the screen? should flow well when opening and closing.
- siebar menu would be cool to have icons for buttons that open up the sub menu options? when siebar is closed, compared to open does that make sense?
- think the projects menu option on automation is broken?
- can we deep dive the SIT view only dashboards, and content i think its not really up to do date? real reflection of what we actually have or is it purely based on the sit clone, pull we do?
- Can we change up the dashboard status page, can we mix in like line graphs, pie charts, other cool dashboard stuff into anywhere here? like use the data we have but make it look cooler? anything better we can add to like automation tests written by the tool? data etc
- Add a like confidence in coverage for the suite? maybe make the judgement based off gaps, and tests and specs covered etc? whatever yo uthink can be used, old runs etc or whatever
- what does the sync do? do we need to start adding buffers like visual buffers on most of our stuff to ensure people are not mis led, or are visually understanding
- pipeline info, still annoyingly only has one of the accordions a different colour, each open accordion should change to the purple colour, but be white background when not open
- the piplein info btw is not the flows of the sit automation stuff, i meant we need flow diagrams here to show how our pipelines work? each part of the pipeline will be informative, do this, this happens, this next, blah blah we need one for each pipeline we have
- I think the text and gaps right, are so vague? like no one will ever know what the question actually is, maybe you need to ensure your asking us the question better? like understand the unconfirmed, or gap and write it out in plain english what the gap and unconfirmed issue is, maybe even a button on the page to say AI summarize? and you go through each and write a description or question better for each so they can be asnwered
- can we re-organise our side bar menu options can stuff be moved around better structured, less accordions? maybe dont know have a think and suggest
- the repos? how come we dont have the test sit repo there as well or all the repos related/
- gaps on the knowledge can be a bit more info? bullet pointed? give more info on what you think is missing in the specs? whats maybe hasnt been gien like a doc or something etc?
- 