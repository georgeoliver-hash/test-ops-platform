# System Test Ops — one AI tool for the whole system-test lifecycle

*One tool, driven through Claude Code. You pick which steps to run from a menu — from maintaining
the TestRail suite, to generating and running the automated tests for the cases marked automatable,
to validating that those tests actually worked. No tribal knowledge, one Gherkin standard, one
traceability key (the TestRail case id) tying it all together.*

> **The idea in one line:** everything a system tester does — design, maintain, automate, verify —
> is one process with selectable steps, not a scatter of separate tools. If a case is marked
> **automatable**, the tool can write the automated test for it *there and then*; if you'd rather
> just maintain the suite, run only that step. **You choose.**

---

## 1. The process menu — pick what you run

Every capability below is one step in the **same** tool. Run one, run several, or run the whole
chain. Status shows what's live today vs. on the roadmap.

| # | Step | What it does | Status |
|---|---|---|---|
| 1 | **Build / restructure a suite** | Audit a legacy TestRail suite, cross-tab, design a clean structure, author cases to one Gherkin standard, push to the new suite | ✅ Live |
| 2 | **Consolidate** | Fold over-fragmented flow-step / variation cases into single flow tests | ✅ Live |
| 3 | **Coverage vs a JIRA release** | Given a fix version, classify covered / partial / missing / stale + draft the gaps | ✅ Live |
| 4 | **Fold a defect** | Pin a fixed bug into the case that owns the behaviour, linked via Refs | ✅ Live |
| 5 | **Conformance audit** | Lint every case against the Gherkin standard; gates "done" | ✅ Live |
| 6 | **Enrich + estimate + mark automatable** | Set per-case **priority** (risk-based), a **manual-execution time estimate** (mins to run by hand) and an **automation-authoring estimate** (effort to script it), plus a 3-tier **Automatable** marker (Yes / Partial / No) | ✅ Live |
| 7 | **Generate the automated test** | For an automatable case, write the pytest test (ADB/Appium for devices, Playwright for portals), tagged with the case id | 🔜 Roadmap — the direction this unification enables |
| 8 | **Run the automated tests** | Execute on the real device / back-office portal; reconcile results back to the case id | ✅ Live (in the automation layer, being folded into the one menu) |
| 9 | **Validate the run** | Read the run output + device logs to confirm the automated test genuinely passed (not a false green) and explain any failure | 🔜 Roadmap (optional validation step) |

You don't have to run them in order. Common picks:
- *"Just tidy the suite"* → steps 1–2, 5.
- *"Prep for a release"* → step 3.
- *"We fixed a bug"* → step 4.
- *"Take this suite all the way to automated"* → steps 1 → 6 → 7 → 8 → 9.

### What powers those steps — the documents you feed in

The maintenance steps (1–5) are **audit-first**: the tool grounds every decision in the real source
material you give it, not guesswork. It reads and cross-references:

| Input you provide | What it is | Powers which steps |
|---|---|---|
| **Old / source TestRail suite** | The existing cases to mine, consolidate, de-duplicate | Build (1), Consolidate (2) |
| **Requirement specs / spreadsheets** (REQ-####, fare/capping references, **test trackers** like the UB-TOO tap tracker) | The rules the device/back-office must obey — fares, caps, limits, expected charges, worked examples | Build (1), Coverage (3), Audit (5) |
| **UX / design documents + flow exports** (Overflow flows + flow-data JSON, screen images) | The behaviour spec — screens, branches, preconditions, thresholds, error handling | Build (1), Consolidate (2), Coverage (3) |
| **Defect / bug trackers** (TIBU / TODEV, regression sheets) | Every fixed bug, to pin as regression coverage | Fold defect (4), Build (1) |
| **JIRA fix version** | The release scope to test against | Coverage (3) |
| **Device brief / glossary** | On-screen wording, operating modes, payment methods, terminology | Build (1), all authoring |

Drop flows/briefs under `knowledge/`, or just point the tool at a spreadsheet or doc — the more you
give, the less it guesses. *(Worked example: today's ABT capping cases were authored and
coverage-checked straight from the **UB-TOO tap tracker** spreadsheet + the fare reference — real
routes, stops and fares flowed from the document into the cases.)*

## 2. How one case flows through the tool

```
  Requirements / JIRA / defects / UX flows
                    │
                    ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  ONE TOOL (Claude Code)                                          │
   │                                                                 │
   │  [1-5] design & maintain ──▶ case lives in TestRail (case id)   │
   │              │                                                  │
   │  [6] mark automatable ──────▶ Yes / Partial / No                │
   │              │ (if Yes/Partial and you choose to)               │
   │  [7] generate automated test ─▶ pytest test  @case("C…")        │
   │              │                                                  │
   │  [8] run on device / portal ──▶ result reconciled to case id    │
   │              │                                                  │
   │  [9] validate via logs ───────▶ confirmed pass / explained fail │
   └───────────────────────────────────────────────────────────────┘
                    │
                    ▼
     TestRail case ⇄ automated test ⇄ run result  (all keyed by the case id)
```

The **TestRail case id is the spine** — a case designed in step 1 is automated in step 7 under that
id, run in step 8 against that id, and validated in step 9. Nothing is orphaned, and any step can be
the one you run today.

> **Honest note on today's shape:** steps 1–6 and 8 exist now (8 currently lives in a connected
> automation layer). Steps 7 and 9 — auto-*writing* the test from the marker, and log-based
> validation — are the new capabilities this "one tool" direction is built to add. This page
> showcases the whole tool; treat 🔜 items as roadmap, not yet delivered.

## 3. The one rule that governs the suite side

> **Read anywhere; write only to the one new suite you nominate.**

Your old/source suite is **never** edited or deleted. The tool copies out of it into a fresh target
suite (set once as `TESTRAIL_WRITE_SUITE_ID`); every write is verified to target that suite alone.
Reorganising (moving/binning sections) is done by **you** in the TestRail UI, because this instance's
API can't move or delete — the tool flags exactly which cases to bin.

## 4. Who does what (the honest split)

A few steps are genuinely yours and can't be automated — secrets, interactive sign-in, creating a
suite, grabbing design data, network/device access, domain sign-off. Everything else, the tool does.

| You do (once, up front) | The tool does |
|---|---|
| Install Python 3.11+, Claude Code, Git (+ ADB/Appium/Playwright for automation) | Create the venv, install dependencies |
| Put TestRail creds in `.env` (secret) | Verify connectivity, discover the case schema |
| **Create the new/target suite** in TestRail, set `TESTRAIL_WRITE_SUITE_ID` | Audit, design, build, push the cases |
| Connect the Atlassian (JIRA) MCP via `/mcp` | Coverage analysis, defect folding, Gherkin drafting |
| Stand up device / back-office access for automation | Generate + run the automated tests, assert the BOS cross-check, reconcile by case id |
| The few TestRail UI moves/bins the API can't | Flag exactly which cases to bin |

## 5. Prerequisites & access

### 5.1 Tools
| Tool | Why | Notes |
|---|---|---|
| **Python 3.11+** | Runs the CLI and the pytest automation | 3.11+ |
| **Claude Code** | The one interface you drive it all through | Desktop or CLI |
| **Git / GitHub Desktop** | Clone, raise PRs | GH Desktop fine without Git on PATH |
| **ADB / Appium / Playwright** | *(automation steps)* drive devices + web portals | Appium/ADB for POS/ETM/PV/BV; Playwright for ABT/BOS portals |

### 5.2 TestRail
- **Internal-only** — you must be on the office network / **VPN** (the host is an internal address,
  e.g. `10.120.54.19`, and it changes occasionally — if it stops resolving, check the current IP).
- **Auth:** no API keys on this instance, so **email + AD password** in `.env` (an API-key instance
  would use a key from *My Settings → API Keys*).
- **Create the target suite yourself** in the UI first (the API can't create suites) and set its id.
- The API can't move / delete / attach — those stay manual UI actions.

### 5.3 JIRA (coverage / defect steps)
Via the **Atlassian (Rovo) MCP**, connected per-user with `/mcp`. Read works once connected; issue
**write** may be admin-gated (the tool drafts issues to paste until then).

### 5.4 Device & back-office access (automation steps)
ADB/Appium reachability to the target device (usually via the test router), and a read-capable
back-office login/test env to verify the cross-check (CloudFare / MERIT / SmartTrack) and drive the
ABT/BOS **web portals** with Playwright.

### 5.5 `.env` (secrets — never committed)
```
TESTRAIL_URL=http://<testrail-host>/testrail      # internal (IP can change)
TESTRAIL_USER=you@arrive.com
TESTRAIL_API_KEY=<api key OR your AD password>
TESTRAIL_PROJECT_ID=<project id>                   # e.g. TFTS - System Test
TESTRAIL_WRITE_SUITE_ID=<new suite id>             # writes go ONLY here
```

### 5.6 Verify
Run **`/start`** (or `python -m system_test_ops doctor`) — checks Python, venv, deps, every `.env`
var, live TestRail, Git and the JIRA MCP, and tells you exactly what's left.
> *Gotcha:* "TestRail unreachable" usually means the VPN isn't really up, or the instance IP changed.

## 6. What you bring (the more, the better)

The tool is **audit-first** — it proves what's shared/covered from real evidence, not names. Bring:
the **old suite** + target suite; **requirements/specs**; **UX flows + flow-data JSON**;
**defect history** (TIBU/TODEV trackers); a **device brief**; and **links**.

## 7. Structure & Gherkin, in brief

Suites are **test-type-first** (Smoke / Functional / Non-Functional / Regression); features under
Functional; mode subsections only where behaviour truly diverges; per-screen HMI validation is its
own layer; functional cases are **flow-based**. Every case: a one-line title, preconditions (with a
**concrete worked example** where it helps a tester — e.g. real route + boarding→alighting stage +
fare), at least one When→Then step, a short prose Expected, and a back-office audit-event assertion
where one genuinely fires. Tags (project / device / feature / mode) are carried natively by TestRail.

## 8. Where it is today

| Suite | TestRail id | Cases | State |
|---|---|---|---|
| Translink **POS** | 30253 | 601 | Built, consolidated, audit-clean, mode-tagged |
| Translink **ETM** | 30254 | 516 | Built, consolidated, audit-clean, mode-tagged |
| Translink **PV** | 30255 | 185 | Built, consolidated, audit-clean, mode-tagged |
| Translink **TVM** | 30284 | 317 | Built, consolidated, audit-clean, mode-tagged |
| Translink **HHD** | 30285 | 335 | Built, consolidated, audit-clean, mode-tagged |
| Translink **GV** | 30286 | 111 | Built, consolidated, audit-clean, mode-tagged |
| **ABT** | 30279 | 297 | Built, consolidated; 45 pre-existing findings open (backlog, not new work) |
| **BOS** | 30287 | 191 | Built, consolidated; 48 pre-existing findings open (backlog, not new work) |

*(Counts and audit state as of 2026-08-03, `python -m system_test_ops audit --suite <id>`. "Mode-tagged"
= every case carries a `MODE-*` Refs tag so a run can be filtered to one operating mode without
re-running mode-irrelevant cases — see `proposals/*/mode-coverage.md` per suite.)*

- **Automation (step 8):** wired today — the 3-tier `Automatable` marker drives the automated tests
  (ADB/Appium for devices, Playwright for the ABT/BOS portals), each linked back to its case id.
- **Next (steps 7 & 9):** fold test *generation* and log-based *validation* into the same menu so the
  whole lifecycle runs from one tool.

---

*Deeper detail lives in the repo (the tool reads it for you): `ONBOARDING.md`, `docs/using-claude.md`,
`docs/new-work-setup.md`, `docs/test-practices.md`, `docs/gherkin-standard.md`,
`docs/automation-handoff.md`, `CLAUDE.md`.*
