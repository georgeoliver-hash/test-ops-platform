# `/start` — worked example (the front-door experience)

A reference walkthrough of what a teammate sees when they open this repo in Claude Code and type
**`/start`**. Use it to explain the onboarding flow without needing a live screen-share. `/start` is
the welcome desk: it runs the readiness preflight, translates it into a plain to-do, takes a short
intake, then routes to the right workflow. (Definition: `.claude/commands/start.md`.)

---

## What `/start` does, in three moves

1. **Readiness preflight** — runs `python -m system_test_ops doctor` (read-only) and buckets every
   finding into **READY / CLAUDE CAN HANDLE / NEEDS YOU / CHECK MANUALLY**.
2. **Intake** — asks only what's still needed: what you want to do, which project + device, the old
   and new suite ids, and what grounding material you have.
3. **Route** — hands off to the right command (`/onboard-suite`, `/consolidate`, `/audit-coverage`, …)
   and the audit-first build process takes over.

---

## Example A — a fully set-up machine (all green)

> **Welcome to System Test Ops 👋** Let me check you're ready before we build anything.
>
> I ran the readiness preflight — plain-English version:
>
> **All set:** Python ✅, virtual env ✅, dependencies ✅, `.env` with your TestRail creds ✅,
> **TestRail reachable — 43 projects visible** ✅, git ✅.
>
> **One optional check:** the JIRA (Atlassian) connection can't be auto-detected. You only need it for
> coverage / feature / defect work — for a pure suite rebuild you can skip it. To enable it, run
> `/mcp` and connect the Atlassian server.
>
> **Verdict: all green — ready to work.** What are we doing?
> 1. Rebuild / restructure a suite · 2. Add a feature · 3. Fold a defect · 4. Coverage audit for a
> release · 5. Run-history review · 6. Routine maintenance
>
> Tell me **which project + device**, the **old (source) suite** and the **new/target suite**, and
> **what grounding material you have** (old suite, UX flows + flow-data JSON, requirement
> spreadsheets, defect tracker, device brief). The more you bring, the less I guess.

---

## Example B — a brand-new teammate (nothing set up yet)

This is the flow that shows the tool front-loading the human-only steps so nothing ambushes you
mid-build:

> **Before we can build, here's your short to-do (these can't be automated):**
>
> 1. **TestRail credentials** — copy `.env.example` → `.env` and add your email + AD password
>    (secrets, so you paste them, not me).
> 2. **Create the new/target suite in the TestRail UI**, then set `TESTRAIL_WRITE_SUITE_ID` to its id
>    — this is the *only* suite I'll write to; your old suite stays read-only.
> 3. **On the VPN?** TestRail is internal-only — if it's unreachable, connect the VPN.
> 4. *(If you need JIRA)* run `/mcp` and connect Atlassian.
>
> **I'll handle the rest now:** create the `.venv`, install dependencies. Come back to `/start` once
> those four are done and we'll go.

The irreducible human set — secrets, interactive sign-in, creating a suite, network/VPN access,
domain sign-off — cannot be automated. `/start` makes them explicit and up front; everything else
the tool does.

---

## Then: routing to the real work

Once green, say what you want in plain English and `/start` routes it:

| You say… | It runs |
|---|---|
| "rebuild the POS suite" | `/onboard-suite translink pos <old> <new>` |
| "consolidate the PV suite" | `/consolidate translink 30255` |
| "we fixed bug TIBU-#####" | `/fold-defect translink <suite> TIBU-##### "<summary>"` |
| "does the suite cover release X?" | `/audit-coverage translink <fix-version>` |
| "hand the automatable cases over" | `/export-automation translink <suite>` |

From there the audit-first process in `docs/test-practices.md` takes over: audit the old suite →
cross-tab shared vs mode → design the structure → author cases → push (which auto-runs the
conformance audit) → hand you the few TestRail UI moves the API can't do.

---

*See also: `ONBOARDING.md` (the 3-minute orientation), `docs/using-claude.md` (the full command
menu), `docs/overview.md` (the one-tool process overview).*
