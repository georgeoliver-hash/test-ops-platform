---
description: Audit an existing suite for over-fragmentation and fold flow-step / variation cases into single flow tests. Usage: /consolidate <project> <suite-id>
argument-hint: <project> <suite-id>
---

Run a **consolidation pass** on an existing suite. Arguments: `$ARGUMENTS` (`$1` = project, `$2` =
suite id). Act as **test-lead**; the governing rule is `docs/test-practices.md` →
"Structure by flow/risk, not by screen (the consolidation lens)".

1. Pull the inventory: `python -m system_test_ops cases --project $1 --suite $2`.
2. **Audit for over-fragmentation.** Per functional area, identify groups of cases that are really:
   - **steps of one sequential flow** (e.g. sign-on → route → journey → confirm), or
   - **variations of one behaviour** (per product / passenger type / payment method / source device).
   Leave alone: genuinely distinct **scenarios/branches** (error paths, lockouts, abandons),
   **mode-specific** divergence, and the **per-screen HMI** layer (that stays one-per-screen).
   Write the plan to `proposals/<device>-suite-restructure/consolidation-audit.md` with before→after
   counts per area and the fold groups.
3. **Confirm the aggressiveness** with the user (full / obvious-only) before touching anything — this
   is a judgement call and folding too hard makes failures hard to localise.
4. **Execute:**
   - Set `TESTRAIL_WRITE_SUITE_ID=$2`. For each fold group pick ONE keeper; enrich its steps to walk
     the absorbed behaviour. If renaming the keeper, use `match: <current title>` + the new `title:`.
   - Push the keepers (`push --commit --update`); fix any compound-THEN the audit flags; re-push.
   - **Retire** the absorbed cases: rename them `ZZ_DELETE_REVIEW - <title> (folded)` and create a
     `ZZ - To Delete (review then bin)` section as the human's move-target.
   - **Encoding trap:** build retire/rename specs with the editor or a Python FILE — never a
     PowerShell heredoc (it mangles em-dashes so `match` misses and you CREATE duplicates instead of
     renaming). If duplicates appear, recover with a file-based script like `tools/fix_consolidation.py`.
5. **Done when** `python -m system_test_ops audit --suite $2` is CLEAN and the functional count has
   dropped with coverage intact. Report before→after counts + the human's UI bin list.
