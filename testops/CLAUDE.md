# CLAUDE.md — system-test-ops

Project memory for Claude. **Start every session here.**

## First message of a new session — greet, don't wait to be asked

If this looks like a fresh session in this repo (no prior context, nothing established yet) and the
user's first message doesn't already name a specific task, **run the `/start` flow proactively**
rather than waiting for them to type `/start` themselves. Someone who's just cloned this repo often
doesn't know that command exists yet — the point of `/start` is to be the front door, so make it
behave like one: say hello, briefly say what this tool does, run the readiness preflight
(`python -m system_test_ops doctor`), and offer the short numbered menu (get set up / build a new
suite / audit coverage / etc. — see `/start`'s own routing table). If their first message already
states a clear task ("audit POS coverage against release X"), skip the greeting and just confirm the
target per the rule below, then go — don't force everyone through a menu they didn't ask for.

## What this repo is for

A shared, version-controlled **AI test-ops team** for the system-test department. It answers two
recurring questions about a device/project test suite held in **TestRail** (written in **Gherkin**):

1. **Coverage (before a run)** — given a JIRA **fix version** (user stories, new features, bug
   fixes), does the TestRail suite cover it? What is **missing / partial / stale**?
2. **Run history (across the last N runs)** — which cases are **always-failing** (candidate
   invalid/outdated), **never-executed**, **flaky**, **recently-regressed**, or **orphaned**? What
   should we **add / edit / remove / reorganise**?

The output is a decision-ready report plus **ready-to-paste Gherkin drafts**. The whole department
pushes/pulls this repo so that, over time, every suite is written to **one Gherkin standard** and
common (cross-project) cases are identical — only genuinely bespoke cases differ.

## Hard rules

- **Confirm the target before acting on an ambiguous request — ask, don't assume.** If a request
  names an action (audit, push, edit cases, check coverage, write a new suite) but doesn't make the
  **device/suite/project/JIRA target** explicit, and it isn't already unambiguous from context (the
  last suite worked in this session, a case id that pins a device), **ask which one** before running
  anything — especially before any write. Never silently rely on whatever `TESTRAIL_WRITE_SUITE_ID`
  happens to be set to in `.env` as if it were the user's intent; that value is leftover state from
  whoever/whatever used this repo last, not a stated instruction. Get confirmed, then proceed without
  re-asking for the rest of that piece of work.
- **Refuse to push into a suite with a live run, unless explicitly overridden.** `push --commit`
  checks for in-progress runs against the target suite first and refuses (listing them) unless
  `--allow-active-runs` is passed — editing cases mid-run can desync that run's results from what a
  tester is looking at right now. Raised as a governance requirement in the 2026-08-07 showcase demo.
- **Read anywhere; write ONLY to the configured new suite.** `system_test_ops/testrail/client.py`
  is read-only (no write endpoints). Writes live solely in the guarded `testrail/writer.py` and go
  **only** to `TESTRAIL_WRITE_SUITE_ID` (the new suite). Every write verifies its target section is
  in that suite; the `push` command is **dry-run unless `--commit`**. Source/old suites and every
  other suite remain strictly read-only. If `TESTRAIL_WRITE_SUITE_ID` is unset, writes are disabled.
- **The old suite is sacrosanct. Copy out, never change.** For Translink POS the source suite is
  **`AA-POS Acceptance Test`** (read-only reference) and the target is **`GG - POS - Claude Suite`**
  (where everything is built). When reusing a pre-existing case, the proposal must say **copy it into
  the new suite** — never move, edit-in-place, or delete from the old suite. All proposed actions
  land in the new suite only.
- **CLI owns data, agents own judgment.** Deterministic, reproducible data (TestRail cases, run
  results) is produced by the Python CLI as JSON. Agents read that JSON baseline and add
  classification/recommendations — they never re-fetch or invent raw data. (Same split as the
  sibling `log-intelligence` repo: `findings.json` → `report.agent.md`.)
- **Cite evidence.** Every coverage classification cites a TestRail **case id** and a JIRA **issue
  key**; every run-health finding cites a **run id**. No claim without a reference.
- **Never invent device behaviour. Mark gaps; do not fill them.** Every action, value, screen name,
  and capability in a case MUST trace to a source requirement (a cited FBD/spec) or a real test body.
  If a detail is **not** in the source, you may **not** substitute a plausible-sounding one to make the
  case read better or feel complete. Instead write an explicit, visible marker at the exact spot —
  `**GAP** — <what is unknown> — not in requirements; confirm on the live system before running` — and
  leave the rest of the case honest about the unknown. A case that says "we don't know this yet" is
  correct; a fluent case built on invented functionality is a defect. **A change request being written
  in a spec does NOT mean the feature is live** — if it is specified but unverified on the real system,
  mark it `**UNCONFIRMED**`, never assert it works. This is a hard rule: prefer visible gaps over
  invisible invention, always.
- **Gaps trigger a Q&A loop with the engineer — a required step, not optional.** A `GAP`/`UNCONFIRMED`
  marker is not the end state: log it to a **gap register** (`proposals/**/gap-register.md`) as a
  *question* and put the batch to the engineer, who usually knows the answer or can find it. Their
  answer is cited back into the case (now grounded) and into `knowledge/`. **A gap that nobody can
  answer is itself a finding** — the tests have exposed a hole in the requirement or the system design;
  flag it `POSSIBLE DESIGN/SPEC BUG` and raise it (Jira). Never quietly fabricate to close a gap, and
  never silently drop it — always route it through the Q&A loop. See `.claude/commands/resolve-gaps.md`.
- **No project names in `system_test_ops/`.** Project/device specifics live in `knowledge/`. Keep
  the Python package project-agnostic.
- **Secrets via `.env` only**, referenced by name. Never commit `.env` or paste an API key.

## The Gherkin standard (summary — full spec in `docs/gherkin-standard.md`)

Every case has a one-line **title**, a **tag line**, and a **Given/When/Then** body:

```
Title: <Feature> — <observable behaviour>
Tags: @project(<name|common>) @device(<POS|TVM|BV|ETMS|GV|PV|HHD>) @feature(<area>)

Given <the device/system is in this state>
  And <additional precondition>
When <the operator/system does this>
Then <this observable outcome>
  And <this BOS audit event / EventLog entry, if applicable>
```

The tag scheme mirrors `automation-tests`' three pytest markers — **project / device / feature** —
so a "common" case reads identically across projects. Bespoke cases carry a specific `@project`.

## Repo map

- `system_test_ops/` — deterministic Python core (CLI). `testrail/` (read-only client), `runs/`
  (history aggregation), `coverage/` (normalisation), `models/` (Pydantic), `reporting/` (renderers).
- `.claude/agents/` — the team (see below). `.claude/commands/` — the team workflow menu:
  **`/start`** (the front door — readiness preflight + intake + routing, for anyone new or unsure),
  `/onboard-suite` (initial build), `/consolidate` (fold over-fragmented cases), `/add-feature`,
  `/fold-defect`, `/maintain`, `/audit`, `/audit-coverage`, `/review-runs`, `/export-automation`
  (hand the automatable cases to the `automation-tests` repo — see `docs/automation-handoff.md`). See
  **`docs/using-claude.md`** for the teammate quick-start + when to use which command.
- **`ONBOARDING.md`** (repo root) — the 3-minute first-run orientation (who-does-what split + what to
  bring). The first thing a newcomer should open; `/start` operationalises it.
- `knowledge/` — human-curated, per-project/-device facts (NOT code). Includes `knowledge/flows/` —
  user flows exported from Overflow (PDF) and transcribed to Mermaid + a path list; each path is a
  candidate scenario, so the flow doubles as a coverage checklist. See `knowledge/flows/README.md`.
- `docs/` — `introduction.md`, `getting-started.md`, `gherkin-standard.md`.
- `reports/` — generated output (gitignored): `reports/<project>/<suite>/<date>/`.

## The team (`.claude/agents/`)

| Agent | Role |
|-------|------|
| `test-lead` | Orchestrator. Entry point for both commands; dispatches the specialists in parallel; consolidates one decision-ready report; asks `gherkin-author` to draft gaps. |
| `coverage-analyst` | Maps a JIRA fix-version scope ↔ TestRail cases; classifies covered / partial / missing / stale. |
| `run-historian` | Reads `run-health.json`; flags always-failing / never-run / flaky / regressed / orphaned cases. |
| `gherkin-author` | Drafts/edits cases in the standard, written to `reports/.../case-drafts.md` (never to TestRail). |
| `standards-keeper` | Owns `docs/gherkin-standard.md`; reviews drafts + existing cases for syntax + cross-project drift. |

## Data sources

- **TestRail** — Python client + API key in `.env` (no TestRail MCP exists). Read-only.
- **JIRA** — the **Atlassian (Rovo) MCP**, at the agent layer. Each teammate connects their own.
- **Requirement specs — full docs stay LOCAL, never committed.** The authoritative requirement library
  (e.g. the Flowbird TFTS docs) is confidential and large, so it lives in each engineer's local folder
  and is read on demand via **`tools/extract_req.py`** (point it at the library with `REQS_DIR` or
  `--dir`). Ground on the **full docs** — the `knowledge/**/*.md` notes are **cited pointers** into them
  (every fact tagged `FBD-xxxxx para N`), NOT a lossy replacement. This keeps the GitHub clone lean
  (tooling + cited notes only), grounding full-fidelity, and confidential content off the repo. A note
  that can't cite a paragraph is a `GAP`, not a fact. New project: drop its library locally, index it
  with `extract_req.py`, build cited notes.

## TestRail instance constraints (learned the hard way — don't rediscover by failing)

This deployment's API is **add / update only** for case management:
- **No `move_cases_to_section` / `move_section`** (404 "Unknown method") — you **cannot move or
  re-parent** cases/sections via API. Reorg = a human drags sections in the **TestRail UI**.
- **No `add_attachment_to_case`** (404) — you **cannot attach images** via API. Screen-validation
  cases carry the Overflow link + image filename in the preface instead.
- **Delete is not available to all accounts** — do not rely on it; treat old suites as read-only and
  bin via the UI.
- **`update_section` ignores `parent_id`** — it can rename a section but not re-home it.
- So the safe model: **build in the repo (YAML) → `push` (idempotent, new-suite-only) → a human does
  any moves/bins in the UI.** Set the per-project `defaults:` via `discover-fields` (case templates
  and required custom fields differ per project — e.g. POS uses `template_id: 1`,
  `custom_steps_seperated`, `custom_devtypes: [5]`; another project will differ).

## This repo is self-contained
A fresh session (any engineer) should read, in order: **this file → `docs/test-practices.md`
(audit-first + conformance audit) → `docs/new-work-setup.md` (what to provide + per-project setup) →
the relevant `knowledge/` files**. That is enough to work safely without any prior chat history.

**Definition of done (every authoring session, every engineer):** after pushing cases, the target
suite's `audit` must be **CLEAN of blocking findings** (advisory title items may remain if reviewed
and intentional). `push --commit` runs the audit for you; treat a non-clean result as unfinished
work. This applies to everyone, all the time — including the first time someone picks up the repo.

## CLI quick reference

```
python -m system_test_ops doctor                                           # readiness preflight: env/creds/connectivity (the engine behind /start)
python -m system_test_ops check                                            # validate creds, list projects
python -m system_test_ops discover-fields --project <id> --sample-case <id># REQUIRED per new project: prints the push `defaults:` block
python -m system_test_ops cases --suite <suite_id>                         # -> cases.json
python -m system_test_ops runs  --project <id> --suite <suite_id> --last 10 # -> run-health.json
python -m system_test_ops push  --file <area>.cases.yaml [--commit] [--update]  # write to the NEW suite only
python -m system_test_ops audit [--suite <id>]                             # read-only: lint a suite vs the Gherkin standard
```

**The conformance audit is part of the standard process — not optional.** `push --commit`
automatically runs `audit` on the target suite and prints a per-rule read-out, so no authoring ever
lands without a conformance check. **Blocking** findings (mojibake, missing objective/preconds,
malformed When/Then, genuine compound THEN, stray tags) must be fixed before a PR; the two **title**
checks are advisory (sometimes intentionally broken — e.g. Screen Validation titles mirror exact UI
screen names). Run `python -m system_test_ops audit` any time; it exits non-zero on blocking
findings (so it can gate a PR/CI), or pass `--no-gate`. Full spec: `docs/test-practices.md`
("Conformance audit"). The rule the auditor encodes — genuine compound THEN vs benign noun list —
is defined in `docs/gherkin-standard.md`.

**Encoding rule (learned the hard way):** never rewrite the `*.cases.yaml` specs with PowerShell
`Set-Content`/`Out-File` — they re-encode UTF-8 as cp1252 and mangle em-dashes/quotes into mojibake,
which then breaks `push`'s title-`match` and silently creates duplicate cases. Edit specs only with
the editor tools or Python with explicit `encoding="utf-8"`. `tools/audit_suite.py` flags residual
mojibake; rerun it after any bulk edit.

**Onboarding a new device/project:** first read `docs/new-work-setup.md` — especially "What you must
provide first" (old suite, requirements, UX flows + flow-data JSON, defect history, links). The
agents are audit-first: missing inputs = guessing = hindered suites.

## Governing docs (read before making coverage decisions)

- **`docs/test-practices.md`** — the mindset for every add/edit/merge/fold/leave decision
  (risk-based, minimal sufficient coverage, no duplication, traceability). The "do we need a new
  test?" rubric lives here. **This rules everything.**
- **`docs/gherkin-standard.md`** — how to write a case.
- **`docs/new-work-setup.md`** — the repeatable playbook for a new project / device / suite / bug
  backlog. This repo is a **company-wide product**: any engineer, any device, any project.

## Conventions when extending

- **Reusable by design.** Everything project-specific is a file under `knowledge/` — copy
  `knowledge/projects/_TEMPLATE.md` and `knowledge/devices/_TEMPLATE.md` for new work. **No code
  change** is needed for a new project or device.
- Keep the deterministic/agent split: if you're tempted to make an agent call the TestRail API
  directly, add it to the CLI instead and have the agent read the JSON.
