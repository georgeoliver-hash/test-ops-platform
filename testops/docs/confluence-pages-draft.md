# Confluence pages — paste-ready drafts
# (I don't have write_confluence permission — org admin needs to grant it, or paste these yourself.)
# Each "## PAGE:" marks where one Confluence page starts.

## PAGE: Setup & Installation

### One-time setup, a few minutes

This tool is a shared GitHub repo. Nothing lives on one person's machine — clone it, and everything
(agents, commands, docs, knowledge) comes with it.

**1. Clone the repo**
```
git clone https://github.com/georgeoliver-hash/system-test-ops.git
cd system-test-ops
```

**2. Install Python dependencies**
```
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e .[dev]
```
Requires Python 3.11+.

**3. Connect TestRail** — copy `.env.example` to `.env` and fill in:
```
TESTRAIL_URL=...
TESTRAIL_USER=your-email@arrive.com
TESTRAIL_API_KEY=...            (My Settings -> API Keys in TestRail)
TESTRAIL_PROJECT_ID=42
TESTRAIL_WRITE_SUITE_ID=        (leave unset until you're ready to write)
```
⚠️ **Never commit `.env`.** It's gitignored, but never paste its contents anywhere — it carries a live API key.

⚠️ **`TESTRAIL_WRITE_SUITE_ID` is the only suite this tool can ever write to.** Everything else —
including every "old" suite — is permanently read-only by design; there's no write endpoint in the
code for anything else. Set this to whichever suite you're actively working on, and confirm it
matches before every push.

**4. Connect JIRA** (only needed for release/coverage work) — via the Atlassian (Rovo) MCP connector
in Claude Code; each person connects their own account (`/mcp`, then authorize Atlassian). Read
access is enough.

**5. Check you're ready**
```
python -m system_test_ops doctor
```
Confirms Python, venv, dependencies, `.env`, and TestRail connectivity in one go. JIRA/Atlassian
can't be checked from the CLI — it tells you to verify that one manually.

**Onboarding a brand new device or project** — read `docs/new-work-setup.md` first, specifically
"What you must provide first" (the old suite, requirements, UX flows, defect history). This tool is
**project-agnostic by design** — no code change is needed for a new device/project, only a new
folder under `knowledge/`.

---

## PAGE: About / How It Works

### What problem this solves

Two recurring questions about a device/project test suite in TestRail:
1. **Coverage (before a run)** — given a JIRA release, or real UX documentation, does the suite
   cover it? What's missing / partial / stale?
2. **Run history (after runs)** — which cases are always-failing, never-run, flaky,
   recently-regressed, or orphaned? What should be added / edited / removed?

The output is always a decision-ready report plus ready-to-paste (or already-pushed) Gherkin cases —
never just a chat answer that disappears.

### The core design principle: CLI owns data, agents own judgment

A deterministic, read-only Python CLI pulls real facts from TestRail/JIRA as JSON. Claude agents read
that JSON and add classification/recommendations on top — they never re-fetch or invent raw data.
This is why every finding is traceable back to a real case id, a real JIRA key, or a real run id —
never an unverifiable claim.

### The write guardrail

The TestRail client is **read-only by construction** — there is no code path that can create/edit/
delete on any suite except the one named in `TESTRAIL_WRITE_SUITE_ID`. Every write also verifies its
target section actually belongs to that suite before touching anything. The old/source suite is
permanently safe — you can only ever copy out of it, never edit it in place.

### The Gherkin standard

Every case, on every device, reads the same way:
```
Title: <Feature> — <observable behaviour>
Given <starting state>
When <the one action under test>
Then <the observable outcome>
  And <a BOS/back-office audit event, if the feature produces one>
```
1–3 steps per case (more only when a step genuinely needs it) — no compound "Then A and B", no
citations baked into the wording (those live in the Refs field / gap register only), no hard-coded
secrets/routes/PINs.

### The "never invent" rule

If a detail isn't in the source (a spec, a UX doc, a real case), it does not get guessed to make a
case read better. It gets an explicit `**GAP**` or `**UNCONFIRMED**` marker, and the exact open
question is logged to `gap-register.md` for a human to answer. A case that says "we don't know this
yet" is correct; a fluent case built on invented behaviour is a defect. As of today there are **87
open, unanswered questions** logged across the whole department this way — that's the tool being
honest about the limits of the source material, not a shortfall in the work.

### Where results actually land
| Location | What's there |
|---|---|
| TestRail | The live suite — cases written straight there, only to the nominated write-suite |
| `proposals/` | Draft case specs (YAML), reviewable/diffable before or as they're pushed |
| `reports/` | Generated, dated audit/coverage evidence (local only, not committed) |
| `knowledge/` | Distilled, cited notes per project/device — reused by every future session |

---

## PAGE: Demos

### What to actually show

The tool is meant to be **run for real, live**, against something genuinely current — not a
pre-picked, rehearsed example — because that's the actual point: it works against real, moving data,
not a canned demo.

**The `/demo` command** does this automatically:
1. A 5-second readiness check (TestRail + JIRA connectivity).
2. Searches JIRA live for a **genuinely current Translink item** — this matters more than it sounds:
   the shared `TIBU` JIRA project is used by several other customers (Perth, SRUP, RTMS, Edinburgh
   Trams) under the same project key, so "most recently updated" alone returns mostly noise. The
   command filters specifically for Translink fix-versions (`TL_...`) before presenting anything.
3. Runs the real coverage/defect-fold check against whatever's picked.
4. Summarises the result in under 5 lines — covered / partial / missing / stale, or a freshly
   authored case — and stops talking, so the presenter can take it from there.

### A real rehearsed example (2026-08-06)

**TIBU-31521** — "POS - Rail POS Top-Up Options Missing for Multi-Journey and Travelcard Products"
(QA TEST, fix version TL_POS_2.0.0). Checking existing coverage found real functional cases for
topping up each affected product — but every one of them is filed under a mode-specific section
(Ulsterbus/Top Up, Metro/Top Up) and tagged to that single mode. The bug specifically describes
attempting the top-up **from Rail POS** — a cross-mode interaction not covered by anything tagged to
run under Rail. Honest classification: **partial** — the product's top-up is tested under its native
mode, but not the exact cross-mode scenario the bug describes. That's a much stronger demo moment
than a flat "covered" or "missing" — it shows the tool reasoning about *why*, not just returning a
label.

### If pre-recording rather than running live

Running the actual commands in a few terminals ahead of time and showing the real transcripts is a
legitimate substitute for a live run when time is short — it's still 100% real output, just not
real-time. Suggested sequence: `doctor` + a suite `audit` (proves connectivity/conformance) → a fresh
`/audit-flows` or `/audit-coverage` run (the actual "how coverage gets checked" moment) → the
TIBU-31521-style fold-defect check (a real, explained finding) → `git log` scrolled to show the
day's actual commit volume → the roadmap artifact as the closing "whole shape of it" view.

---

## PAGE: Commands & Audits Reference

### The 9 abilities — pick one, or run several in sequence

| Command | What it does |
|---|---|
| `/onboard-suite` | Build a whole new suite from an old one — clean structure, every case authored fresh |
| `/audit-coverage` | Coverage vs a JIRA fix version — covered / partial / missing / stale |
| `/audit-flows` | Coverage vs real UX flow-maps (Overflow-transcribed) — every path classified & authored |
| `/consolidate` | Fold over-fragmented cases into single flow tests |
| `/add-feature` | Add a feature/story — extends the flows it touches rather than bolting on new cases |
| `/fold-defect` | Pin a found/fixed bug into its owning case, or author one new regression case |
| `/review-runs` | Run-history health — always-failing / never-run / flaky / regressed, from real data |
| `/maintain` | Routine upkeep — run-history + audit + consolidation check, one pass |
| `/audit` | The conformance gate — runs automatically after every one of the above; this is the definition of done |

### The conformance audit, in detail

Not optional — `push --commit` runs it automatically on every push. Checks (all must be zero to be
"CLEAN"): mojibake/encoding corruption, empty or malformed preface/preconditions/steps/expected,
steps not starting with When, a genuine compound Then (two distinct outcomes bundled into one line),
missing tags. Two title-format checks are advisory only (sometimes intentionally broken, e.g. Screen
Validation titles that must mirror exact UI screen names).

### CLI quick reference
```
python -m system_test_ops doctor                     # readiness check
python -m system_test_ops check                      # validate creds, list projects
python -m system_test_ops discover-fields --project <id> --sample-case <id>   # required for a new project
python -m system_test_ops cases --suite <suite_id>    # pull a live suite -> cases.json
python -m system_test_ops runs --project <id> --suite <suite_id> --last 10    # -> run-health.json
python -m system_test_ops push --file <spec>.cases.yaml [--commit] [--update] # write to the ONE nominated suite
python -m system_test_ops audit [--suite <id>]        # read-only conformance lint, any suite, any time
```

### Real, current status (checked live, 2026-08-06/07)

| Suite | Cases | Conformance | Estimate populated | Notes |
|---|---:|---|---:|---|
| ETM (30254) | 615 | CLEAN | 459/615 | mode tags still old format |
| POS (30253) | 799 | CLEAN | 530/799 | mode tags fully renamed |
| HHD (30285) | 482 | CLEAN | 211/482 | mode tags still old format |
| TVM (30284) | 436 | CLEAN | 201/436 | mode tags still old format |
| GV (30286) | 125 | CLEAN | 96/125 | mode tags still old format |
| PV (30255) | 197 | CLEAN | 133/197 | mode tags still old format |
| ABT (30279) | 633 | CLEAN | 496/633 | not a device-mode suite |
| BOS (30287) | 191 | CLEAN | 175/191 | not a device-mode suite |

All 8 suites are conformance-clean right now. Every Translink device's UX flow-map coverage is
complete except 3 known, logged gaps: ETM's Startup board and POS's Welcome Page board were never
transcribed into a flow-map, and Bus Validator (BV) has zero structured coverage at all (57+ screens,
untouched). "Automatable Y/P/N" is **not** actually stored on any live case today — it's computed
fresh by a report each time it runs, never persisted to TestRail (there's nowhere in the current
case template for it to live yet).

---

## PAGE: Automation

### Two separate repos, deliberately not merged

- **`system-test-ops`** (this tool) — TestRail/JIRA case authoring, built project-agnostic on purpose.
- **`dev/sit`** (`flowbird-group/sit`, Robot Framework) — the **official** device-automation suite,
  owned by the automation team (Mat/Tayo/Persistent), with its own CI/PR review.

Different tech stack, different owners, different governance — merging them would blur
system-test-ops' project-agnostic design and move SIT's live work under different ownership without
its owners' say. Kept separate; connected by a documented citation pattern instead.

### The pattern that already works (confirmed live, SIT branch `feature/pos-device-family`, PR #52)

A SIT `.robot` test cites its source TestRail case directly:
```
[Documentation]    C4099922. GIVEN the TMS-configured failed-attempt threshold, WHEN the
...                operator enters incorrect credentials that many times, THEN the device
...                locks... Refs: TIBU-22672, TIBU-22003.
[Tags]    testrailid=C4099922    destructive    Regression
[Setup]    Skip    GAP: needs the confirmed TMS-configured lockout threshold... see [Documentation]
```
Case id cited, Given/When/Then mirrored verbatim, `destructive` carried over, and — critically — the
same "don't invent it" discipline carries into automation: an unconfirmed value gets `Skip` +
`GAP:`, not a fabricated passing test.

### Real status per device (checked directly in the SIT repo, not assumed)

- **ETM** — genuinely working. A real NJT/Way6 driver console, proven against live device hardware
  (192.168.3.11).
- **POS** — 24 test files exist, matching almost exactly the areas covered in TestRail (Sign On,
  FLU, Printing, Audit, Status, Options). But every UI-driving keyword is `Fail Not Implemented` —
  there is no generic Android screen-driving layer built for any Android device yet in that repo.
  These would fail immediately if run today.
- **Jenkins CI** exists (4 pipelines) but runs an older, separate `PilotTests` source tree for
  deployment validation — not wired to the current `Tests/POS`/`Tests/ETM` folders at all.
- **`TestRailListener`** (would push automated results back into TestRail) exists as code but is
  wired into nothing — no pipeline invokes it. Also has hardcoded plaintext credentials in the file —
  flagged to whoever owns that repo, not fixed here.

### An important discovery: working POS automation already exists elsewhere, unused

A separate, independent repo — `dev/automation-tests` — already solved the exact problem SIT's POS
layer is stubbed on. It has **real, working ADB + Appium driving code**: a genuine `Navigator.sign_on()`
that taps fields, types credentials, and asserts on real UI state, verified against a live device
(`192.168.3.151:5555`), including a test that asserts a real `state.changed` EventLog entry after an
actual driven sign-on. A `POS-handover/` package already exists specifically to bridge this into SIT,
but its own README says SIT's Library/registry layer is incompatible with the code as-is — likely why
SIT re-stubbed POS from scratch instead of reusing it. This code had **no git history at all** (real
loss risk) until it was committed locally on 2026-08-07 as a safety measure — it is not yet pushed to
a permanent remote.

### What's genuinely not built anywhere yet

Auto-generating a script from a TestRail case (every example above was hand-written by a person
reading a case), a results dashboard, and CI that runs manual and automated tests side by side. Named
honestly, no committed date on any of it.

---

## PAGE: Skills

### The 5 specialists

| Agent | Job |
|---|---|
| `test-lead` | Orchestrator — entry point for every command, dispatches the others in parallel, produces one decision-ready report |
| `coverage-analyst` | Maps a JIRA release or a UX flow-map against real TestRail cases — classifies covered / partial / missing / stale / fragmented |
| `run-historian` | Reads real run-health data — flags always-failing / never-run / flaky / regressed / orphaned cases |
| `gherkin-author` | Drafts/edits cases to the shared standard — only ever writes to `proposals/`, never straight to TestRail |
| `standards-keeper` | Owns the Gherkin standard itself — reviews drafts and existing cases for syntax/cross-project drift |

### The skills that make any of the above trustworthy, not just fast

- **Full-document reading** — reads whole specs/UX transcriptions, not a skim, then writes small,
  cited notes into `knowledge/` so the next session doesn't have to re-read the source from scratch.
- **Reads real run comments** — pulls actual TestRail run results and tester comments (why a case
  was marked Invalid) and grounds a fix in that, not just the case's own text.
- **Asks, doesn't guess** — the single most load-bearing discipline in the whole tool. Every
  unconfirmed detail becomes a logged question in `gap-register.md`, cited by case id, and waits for
  a real answer instead of inventing one. Currently 87 open questions on record, across every device.
- **Flow-map-driven UX coverage** — Overflow (design tool) exports get transcribed verbatim, then
  structured into a Mermaid diagram + a table of candidate paths per screen-flow. Each path becomes a
  literal coverage checklist row, cross-referenced against the live suite until every row is either a
  real case id or an explicit logged reason it isn't yet.
