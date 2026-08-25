# system-test-ops

One AI-driven process for the whole system-test lifecycle — **maintain** the TestRail suites,
**check coverage** against JIRA releases and requirement specs, and **hand off** the automatable
cases — for any device/project (POS, ETM, PV, TVM, BV, GV, HHD). Driven through **Claude Code**.

## New here? One word.

Open this folder in Claude Code and type **`/start`**. It runs a readiness check, tells you exactly
what it still needs from you, and routes you to the right workflow.

- **3-minute orientation:** [ONBOARDING.md](ONBOARDING.md)
- **What the whole tool does (the big picture):** [docs/overview.md](docs/overview.md)
- **Full command menu + when to use each:** [docs/using-claude.md](docs/using-claude.md)

## The one rule that explains everything

**Read anywhere; write only to the one new suite you nominate** (`TESTRAIL_WRITE_SUITE_ID`). Your
old/source suite is never edited or deleted — Claude copies out of it into a fresh target suite, and
you do the few TestRail UI moves the API can't. Every push auto-runs the **conformance audit**; a
change isn't done until it's CLEAN.

## The command menu (type in Claude Code)

```
/start                              front door: readiness preflight + intake + routing
/onboard-suite <project> <device>   initial build/restructure of a suite
/consolidate   <project> <suite>    fold over-fragmented cases
/add-feature / /fold-defect         add coverage for a story / pin a fixed defect
/audit-coverage <project> <fixver>  covered / partial / missing / stale vs a JIRA release
/audit-flows <project> <device> <suite>  same, but vs real UX flow-maps instead of a JIRA release
/review-runs    <project> <suite>   run-history health
/maintain       <project> <suite>   routine upkeep (run-history + audit + consolidation, one pass)
/ingest-docs    <project> <path>    distil requirement docs into cited knowledge/<project>/specs
/audit / /export-automation
```

Every command above asks for its project/device/suite/release if you don't give it — it never
assumes or falls back on whatever was configured last.

## FAQ

**Do I need to remember all these commands?** No — type `/start` (or just say hello) and Claude walks
you through it.

**What if I don't have UX flows, only a JIRA release?** Use `/audit-coverage` instead of
`/audit-flows` — it only needs a fix version, not transcribed flow-maps.

**What if my UX source is Figma, not Overflow?** There's no ingestion path for that today — only
Overflow exports (via the Claude Chrome extension transcription process) can become a flow-map. Say
so when asked and Claude will tell you plainly rather than pretending it can read it.

**Can I break the old suite by running this?** No — the client has no write endpoint for anything
except the one suite you set in `TESTRAIL_WRITE_SUITE_ID`. Every other suite, including the old one,
is permanently read-only by construction, not just convention.

**What if the suite I'm pushing to has a run in progress right now?** `push --commit` checks for
this and refuses, listing the run(s), unless you pass `--allow-active-runs`. Editing cases mid-run
can desync that run's results from what a tester is currently looking at.

**How do I know a change is actually finished?** `python -m system_test_ops audit --suite <id>` must
report CLEAN of blocking findings. `push --commit` runs this automatically; if it's not CLEAN, the
work isn't done yet.

**Something looks wrong / a spec doesn't make sense — what happens?** It gets logged as an explicit
question in `proposals/coherence-audit/gap-register.md`, cited by case id, and left for a human to
answer — never guessed at to make a case read better.

**Can the automated-test side be generated from this automatically?** Not yet — that's on the
roadmap, not built. Today a person reads a marked case and writes the automation by hand, citing the
case id back (see `docs/automation-handoff.md`).

## Layout

- `system_test_ops/` — deterministic Python core (read-only TestRail client, guarded writer, audit).
- `.claude/agents` + `.claude/commands` — the AI team and the workflow menu.
- `knowledge/` — human-curated + distilled per-project facts (`knowledge/<project>/…`). No code is
  project-specific.
- `docs/` — the standard, practices, setup, overview.
- `proposals/` — per-suite working artifacts + reviews (see `proposals/README.md`).
- `reports/`, `.venv/`, `.env`, raw requirement docs — **gitignored / local only**, never committed.

Conventions Claude loads every session: [CLAUDE.md](CLAUDE.md).
