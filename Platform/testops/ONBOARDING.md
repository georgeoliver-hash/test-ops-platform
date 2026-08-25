# Start here — onboarding (read this first, ~3 minutes)

You've cloned **system-test-ops**: a shared, version-controlled AI test-ops team for the system-test
department. It rebuilds and maintains TestRail suites (written in Gherkin), audits coverage against
JIRA releases, and hands automatable cases to the `automation-tests` repo. Everything runs through
**Claude Code** in this folder.

You don't need to memorise the process. **Open this repo in Claude Code and type `/start`** — Claude
runs a readiness check, tells you exactly what (if anything) it still needs from you, and then drives
the work. This page just sets expectations first.

## The one rule that explains everything

**Read anywhere; write only to the one new suite you nominate.** Your old/source suite is never
edited or deleted — Claude copies out of it into a fresh target suite (`TESTRAIL_WRITE_SUITE_ID`).
Reorganising (moving/binning) is done by you in the TestRail UI, because this TestRail instance's API
can't move or delete. Claude builds; you do the few clicks the API can't.

## Who does what (the honest split)

Some steps are genuinely yours and **cannot be automated** — secrets, interactive sign-in, creating a
suite, grabbing design data, network/device access, and domain sign-off. The point of `/start` is to
surface these **up front** so they don't ambush you mid-build. Everything else, Claude does.

| You do (once, up front) | Claude does (for you) |
|---|---|
| Install Python 3.11+ (and Claude Code) | Create the `.venv`, `pip install -e ".[dev]"` |
| Put TestRail creds in `.env` (secret) | Verify connectivity, list projects, discover case schema |
| **Create the new/target suite** in the TestRail UI, set `TESTRAIL_WRITE_SUITE_ID` | Audit the old suite, cross-tab, design structure, build cases, push |
| Connect the Atlassian (JIRA) MCP via `/mcp` (interactive OAuth) | Pull fix-version scope, classify coverage, draft Gherkin |
| Provide grounding material (below) | Mine flows, fold defects, run the conformance audit, export the automation backlog |
| The few TestRail UI moves/bins the API can't | Flag exactly which cases to bin and build the `ZZ - To Delete` section for you |

## What to bring (the more, the better the result)

Claude is **audit-first**: it proves what's shared/covered from real evidence rather than guessing
from names. The quality of the help is capped by what you give it. Bring as many as exist:

- **The old TestRail suite** (source) + the new/target suite — the baseline to mine and consolidate.
- **Requirements / specs** (e.g. `REQ-####`) — to judge covered vs stale.
- **UX / design flows** — the behaviour spec (preconditions, thresholds, error handling). For
  Overflow (no API/MCP), the best path is the **Claude Chrome extension**: open the flow in your
  browser with the extension installed, ask it to transcribe every board verbatim (screen names,
  annotations, decision points, connections — not a summary), and paste the result into
  `knowledge/flows/` as a raw `.md` file. Scales far better than screenshots for a large, densely
  annotated diagram. A plain PDF/PNG export works too if you'd rather. See
  `knowledge/flows/README.md` for the exact ask and the template Claude transcribes it into.
- **Defect / bug history** (e.g. the TIBU tracker) — to pin every fixed bug as regression coverage.
- **A device brief** — on-screen wording, operating modes, payment methods, terminology.
- **Links** — dashboards, share links, ticket boards.

Missing several? That's fine to *start a conversation* — just say so, and Claude scopes its confidence
down instead of inventing coverage. A full **build** really wants the old suite + flows + defect history.

## The 60-second path

1. Open this folder in Claude Code (`claude` in the repo root).
2. Type **`/start`**. Claude runs `python -m system_test_ops doctor` and gives you a who-does-what
   punch-list — it'll offer to do its own setup (venv, deps) and tell you your few to-dos.
3. Clear any **NEEDS YOU** items (creds, create the target suite, connect JIRA MCP if needed).
4. Tell Claude what you want (build / consolidate / add-feature / fold-defect / coverage / maintain)
   and which project + device + suites.
5. Claude routes to the right command and the audit-first process takes over.

## Where the detail lives (you don't have to read these — Claude does)

- **`docs/getting-started.md`** — the exact one-time setup commands (venv, `.env`, `/mcp`).
- **`docs/using-claude.md`** — the full command menu and when to use each.
- **`docs/new-work-setup.md`** — the repeatable playbook for a new project / device / suite.
- **`docs/test-practices.md`** — the governing mindset (audit-first, consolidation, the conformance gate).
- **`docs/gherkin-standard.md`** — how a case is written.
- **`CLAUDE.md`** — the conventions Claude loads automatically every session.

Anytime you're unsure, just run **`/start`** again, or run `python -m system_test_ops doctor` yourself
to re-check readiness.
