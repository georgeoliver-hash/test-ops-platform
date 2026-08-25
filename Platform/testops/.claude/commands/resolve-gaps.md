# /resolve-gaps — turn test gaps into answers (or into design findings)

Use this whenever authoring or auditing has produced `**GAP**` / `**UNCONFIRMED**` markers, or after a
coherence/grounding audit. It is the **required** companion to the no-gap-filling rule: gaps are never
fabricated shut and never silently dropped — they are resolved through a Q&A loop with the engineer.

## Why this step exists
These are tests for devices whose behaviour is *specified*. If a detail isn't grounded, the honest move
is to **ask the person running the tool** — they usually know it, can find it, or confirm it on the live
system. And a gap that **no one** can answer is not a nuisance: it means the tests have found a hole in
the **requirement or the system design itself**. That is one of the most valuable things this tool
produces — surface it, don't bury it.

## Procedure
1. **Collect.** Gather every `GAP`/`UNCONFIRMED` marker (and audit `needs-confirmation` findings) into a
   `gap-register.md` under the relevant `proposals/**/` folder. One row per gap: the affected case id(s),
   the **question**, a category (SURFACE / LIVE? / VALUE / CONFLICT / BUG?), and blank `A:` + `source:`.
2. **Ask.** Put the batch to the engineer — grouped by area, most-blocking first. Use `AskUserQuestion`
   for the few that gate large families; leave the rest as a checklist they fill in. Never guess on their
   behalf.
3. **Apply.** For each answer: re-write the affected case(s) to state the grounded behaviour and **cite
   the source** (spec section / "confirmed on live system" / colleague). Record durable facts in
   `knowledge/` so future audits ground against them. Then re-run `audit` on the suite.
4. **Escalate.** Any question left unanswered → mark the case `**UNCONFIRMED**` (do not assert it) and
   record it as a **POSSIBLE DESIGN/SPEC BUG** for the Jira writeup, with the exact ambiguity. This closes
   the loop even when the answer doesn't exist yet.

## Output
- Updated `gap-register.md` (answered + escalated).
- Re-grounded cases (cited) pushed via the normal `push` flow.
- New/updated `knowledge/` facts.
- A short list of design/spec findings to raise.

**Never** fill a gap to make a case read better. A visible gap routed through this loop is the correct
state; invented functionality that reads fluently is a defect.
