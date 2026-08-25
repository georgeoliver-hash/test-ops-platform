---
description: Audit a TestRail suite's coverage of a JIRA fix version (covered/partial/missing/stale) and draft the gaps. Usage: /audit-coverage <project> <fix-version> [suite]
argument-hint: <project> <fix-version> [suite]
---

Run a coverage audit. Arguments: `$ARGUMENTS`
(positional: `$1` = project, `$2` = fix version, `$3` = suite — default the suite to the project's
primary device suite, e.g. `POS` for translink, if `$3` is omitted).

**If `$1` (project) or `$2` (fix version) is missing, stop and ask before doing anything else** — per
`CLAUDE.md`'s hard rule on confirming an ambiguous target. Don't guess a project, don't assume the
"last suite worked in," don't default off `TESTRAIL_WRITE_SUITE_ID`. Ask plainly:
- Which project/device? (e.g. Translink POS, Translink ETM)
- Which JIRA fix version should this audit against? (offer to look up live current ones for that
  project if the user doesn't have one in mind — `fixVersion is not EMPTY ORDER BY updated DESC`,
  filtered to that project's real naming convention, same caution as `/demo` about shared JIRA
  project keys serving multiple unrelated customers)
- Which suite, if it's not obvious from the project (multiple devices under one project)?

Once confirmed, proceed without re-asking for the rest of this run.

Act as the **test-lead** agent (`.claude/agents/test-lead.md`). Follow its coverage-audit playbook:

1. Read `CLAUDE.md`, `knowledge/projects/$1.md`, and the relevant `knowledge/devices/*.md`.
2. Produce the deterministic baselines (read-only):
   - `python -m system_test_ops cases --project $1 --suite <suite>`
   - `python -m system_test_ops runs  --project $1 --suite <suite> --last 10`
   If the CLI errors on credentials, stop and point the user at `docs/getting-started.md`.
3. Pull the `$2` fix-version scope from JIRA via the Atlassian MCP (resolve the project key from the
   knowledge file or `getVisibleJiraProjects`, then `searchJiraIssuesUsingJql`
   `fixVersion = "$2" AND project = <KEY>`).
4. Dispatch **coverage-analyst** and **run-historian** in parallel (hand each the relevant JSON path
   + the scope list).
5. Dispatch **gherkin-author** for the missing/partial/stale items, then **standards-keeper** to
   review the drafts.
6. Consolidate into `reports/$1/<suite>/<date>/coverage.md` exactly as test-lead specifies (verdict,
   scope table, ADD/EDIT/REMOVE/REORGANISE recommendations with citations, run-health section, links
   to `cases.json` / `run-health.json` / `case-drafts.md`).

Finish by printing the report path and a 3-line summary (covered/partial/missing/stale counts +
biggest risk). Remember: read-only against TestRail — propose, don't write.
