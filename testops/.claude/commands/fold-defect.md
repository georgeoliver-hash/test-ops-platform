---
description: Fold a found/fixed defect into the suite — into the owning case (preferred) or a dedicated regression case. Usage: /fold-defect <project> <suite-id> <defect-id> "<summary>"
argument-hint: <project> <suite-id> <defect-id> "<summary>"
---

Pin a defect so it can't silently return. Arguments: `$ARGUMENTS` (`$1` = project, `$2` = suite id,
`$3` = defect id e.g. TIBU-#### / 3xxxxx / a JIRA key, `$4` = short summary). Governing rule:
`docs/test-practices.md` rubric step 4 — **never one case per bug as a reflex.**

**If `$1`, `$2`, `$3`, or `$4` is missing, stop and ask before doing anything else** — per
`CLAUDE.md`'s hard rule on confirming an ambiguous target: which project/device, which suite, what's
the defect id, and a one-line summary of what it is (if not obvious from the id alone).

1. `python -m system_test_ops cases --project $1 --suite $2` and find the case(s) that own the
   behaviour the defect touches. (Enrich the defect's intent from JIRA via the Atlassian MCP if it's
   reachable there.)
2. **Decide:**
   - **Scenario already exercised** → **fold**: add a short regression step/assertion to the owning
     case if the fix changed observable behaviour, and add `$3` to that case's **Refs**. No new case.
   - **No case covers the scenario** → write **one** dedicated case in the `Regression` section with
     `$3` in Refs.
3. Set `TESTRAIL_WRITE_SUITE_ID=$2`; apply via a `*.cases.yaml` (`match: <owning title>` to update in
   place, or a new Regression case). `push --commit [--update]`.
4. Record the decision in `proposals/<device>-suite-restructure/regression-register.md`
   (defect → FOLD owning-case / NEW). Done when `audit --suite $2` is CLEAN.
