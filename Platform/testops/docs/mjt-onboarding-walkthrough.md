# Onboarding MJT — a literal step-by-step walkthrough

Written for whoever's picking up MJT first (currently Gareth). This is the concrete "do this, then
this" version of `new-work-setup.md` — read that file for the *why*; this one is the *exact steps*.

## 0. Before you touch Claude — create the empty suite

The API can't create a TestRail suite. Do this yourself first:
1. In TestRail, create a new suite for MJT (empty is fine).
2. Note its suite id — you'll need it as `TESTRAIL_WRITE_SUITE_ID`.

## 1. One-time setup

1. Clone both repos:
   - `github.com/georgeoliver-hash/system-test-ops`
   - `github.com/georgeoliver-hash/test-automation-sit`
2. Open `system-test-ops` in Claude Code. Just say hello, or ask a question — you don't need to
   remember any command. It'll run a readiness check and tell you exactly what's still missing
   (TestRail credentials in `.env`, connecting the JIRA/Atlassian MCP via `/mcp`).
3. Put `TESTRAIL_WRITE_SUITE_ID` (the suite id from step 0) in `.env` once you have it.

## 2. Gather materials — before you start the real conversation

Bring as many of these as exist for MJT. You don't need all of them, but the more you bring, the
less Claude has to ask you mid-build, and the better-grounded the result.

| Material | What to actually bring |
|---|---|
| **Old TestRail suite** (if MJT has one already) | Just tell Claude the suite name/id — it pulls it live, you don't need to export anything |
| **Requirements / specs** | Whatever exists as documents — PDFs, Word docs, wiki/Confluence pages, spec sheets |
| **UX flows** | See the dedicated section below — this is the one that needs a bit of prep work |
| **Defect / bug history** | Where it's tracked (a JIRA project key, or another tracker) and roughly how far back matters |
| **Stories / features / releases** | A JIRA epic key or fix-version, if MJT has one set up in JIRA |
| **Device brief** | Anything on-screen wording, operating modes, payment methods, terminology — even rough notes |

### UX flows specifically — if it's a mindmap, not Overflow

The transcription tooling that exists today (the Claude Chrome extension) was built for **Overflow**
exports. There's no equivalent automated path for a mindmap tool yet. Do this instead:

1. Check if your mindmap tool can **export to plain text or an outline format** (XMind, MindMeister,
   Miro, and most others usually can, under an Export menu). If so, that's the fastest path — hand
   the exported text straight to Claude.
2. If it can't export cleanly, take **screenshots of each branch** and ask Claude to transcribe it
   **verbatim** — exact node names, the order, every branch/connection — not a summary. This is the
   same principle as the Overflow method, just done by hand instead of the extension.
3. Either way, the result becomes a raw `.md` file under `knowledge/flows/`. From there Claude
   structures it into the same Mermaid-diagram + paths-table shape used for every other device — the
   mindmap's shape doesn't matter once it's transcribed; what matters is that nothing was summarised
   or guessed at in the transcription step itself.

## 3. The actual conversation with Claude, in order

1. Say what you're doing: *"I'm onboarding MJT as a new project. I want to build a new suite."*
   Claude will ask which project/device/suites if it isn't already obvious — that's expected, answer
   it rather than it guessing.
2. Hand over materials **as you mention them**, not all in one dump — e.g. "here are the specs"
   (point at the files or paste them), "here's the UX flow transcription" (the `.md` from step 2),
   "the old suite id is X" if one exists.
3. Claude runs the audit-first build (this is `/onboard-suite` under the hood): pulls the old suite
   if there is one, works out what's shared vs. MJT-specific, proposes a structure, and drafts cases
   grounded in what you gave it. If anything's ambiguous, it will **stop and ask you** rather than
   guess — that's a deliberate rule, not a bug.
4. Genuinely unconfirmable things (a spec that doesn't say, a UX flow with a gap) get logged as an
   open question in `proposals/coherence-audit/gap-register.md`, not invented. Expect a few of these
   on a first pass — that's normal and correct, not a sign something went wrong.
5. Once cases are pushed, the **conformance audit** must come back clean — Claude runs this
   automatically after every push. If it's not clean, the work isn't finished yet.
6. **Time estimates** are set per-case as cases are authored — nothing extra to do for this.
7. **Automation** is a separate, later step. Once the suite exists and has real cases, the
   `test-automation-sit` repo picks up from there — see that repo's own `docs/automation-handoff.md`
   for how a test cites a case back. Don't try to do this in the same pass as the initial build.

## What "done" looks like for the first pass

- A new, structured MJT suite in TestRail, built from whatever real materials existed — not guessed.
- Conformance audit: CLEAN.
- A short list of open questions in `gap-register.md` for anything genuinely unconfirmable from the
  source material — normal, not a failure.
- Nothing touched in any suite except the one MJT suite you created in step 0.
