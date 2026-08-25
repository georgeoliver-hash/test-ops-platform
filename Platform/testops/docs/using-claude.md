# Using Claude on system-test-ops (for the team)

This repo **is** the department's AI test-ops process: the methodology, the agents, the deterministic
CLI, and a set of slash commands — all version-controlled. Clone it, open it in Claude Code, and you
drive the same audit-first, consolidation-minded workflow everyone else does. No tribal knowledge.

## One-time setup
1. **Clone** the repo and open the folder in Claude Code (`claude` in the repo root).
2. **Python env:** `python -m venv .venv` → activate → `pip install -e .[dev]`.
3. **Secrets:** copy `.env.example`/`.env` and set `TESTRAIL_URL`, `TESTRAIL_USER`,
   `TESTRAIL_API_KEY` (or AD password on instances without API keys), `TESTRAIL_PROJECT_ID`. Set
   `TESTRAIL_WRITE_SUITE_ID` to the **new** suite you're building — writes go ONLY there; everything
   else is read-only. `.env` is gitignored — never commit it.
4. **JIRA (optional, for coverage/feature work):** run `/mcp` and connect the Atlassian (Rovo) MCP
   with your own account.
5. Verify: `python -m system_test_ops doctor` gives a full readiness read-out (or `check` just lists
   the projects you can see). Or simpler — open the repo in Claude Code and type **`/start`**, which
   runs the preflight for you and tells you what's left.

## What to read first (Claude reads these automatically; you can too)
`CLAUDE.md` → `docs/test-practices.md` (the governing mindset: audit-first, the "do we need a new
test?" rubric, **structure by flow not by screen**, the conformance gate) → `docs/new-work-setup.md`
(what to provide for a new device) → the relevant `knowledge/` files. This is enough to work safely
with no prior chat history.

## The command menu — just type these in Claude Code
| Command | What it does |
|---|---|
| `/start` | **The front door** — runs the readiness preflight, takes a short intake, and routes you to the right command. Start here if you're new or unsure. |
| `/onboard-suite <project> <device> [old] [new]` | **Initial build** of a restructured suite (the big one): audit-first → cross-tab → structure → build area-by-area → conformance-clean. |
| `/consolidate <project> <suite>` | Audit an existing suite for over-fragmentation and **fold** flow-step/variation cases into single flow tests (HMI per-screen stays). |
| `/add-feature <project> <suite> "<feature/JIRA key>"` | Add coverage for a **new feature/story**, extending the flows it changes rather than bolting on isolated cases. |
| `/fold-defect <project> <suite> <defect-id> "<summary>"` | **Pin a found/fixed bug** — fold into the owning case (preferred) or a dedicated regression case, linked via Refs. |
| `/maintain <project> <suite>` | Periodic upkeep: run-history (retire dead/flaky), conformance audit, consolidation sanity check. |
| `/audit <project> <suite>` | Read-only **conformance audit** vs the Gherkin standard, with fixes explained. |
| `/audit-coverage <project> <fix-version> [suite]` | Does the suite cover a JIRA fix version? covered/partial/missing/stale + drafts. |
| `/review-runs <project> <suite>` | Run-history health analysis on its own. |

You can also just **talk to Claude** ("rebuild the TVM suite", "consolidate POS", "we found bug X,
pin it") — the commands are the well-trodden paths, not the only way in.

## How effort scales (set expectations)
- **Initial build** = the longest task (full audit + restructure of hundreds of old cases). `/onboard-suite`.
- **New feature** = moderate — may change existing flows, not just add. `/add-feature`.
- **Bugs found** = light — usually fold into an existing case + a Ref, or one regression case. `/fold-defect`.
- **Routine** = `/maintain` periodically so the suite stays lean (it should shrink as often as it grows).

## Non-negotiables (the guardrails are in the tooling, but know them)
- **Audit-first** — never change a suite before an evidence-based audit (cross-tab to prove shared
  vs mode-specific; don't guess from names).
- **Read-only / propose-first against TestRail** — writes go only to `TESTRAIL_WRITE_SUITE_ID`; old
  suites are copied out of, never edited or deleted from. Reorg moves/bins are done by a human in the
  TestRail UI (this instance's API can't move/delete) — Claude flags cases `ZZ_DELETE_REVIEW` and
  builds a `ZZ - To Delete` section for you.
- **Conformance audit is the definition of done** — `push --commit` runs it automatically; a change
  isn't done until it's CLEAN of blocking findings.
- **Never** generate `*.cases.yaml` via PowerShell `Set-Content`/`Out-File` or a heredoc piped to
  Python — they mangle UTF-8 punctuation, which breaks title-matching and creates duplicate cases.
- **Everything is reviewable** — proposals land under `proposals/`, reports under `reports/`, and
  changes go through a PR so every project converges on the same conventions.
