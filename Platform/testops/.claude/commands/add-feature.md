---
description: Add coverage for a new feature/story, updating the flows it touches rather than bolting on isolated cases. Usage: /add-feature <project> <suite-id> "<feature or JIRA key>"
argument-hint: <project> <suite-id> "<feature or JIRA key>"
---

Add coverage for a new feature. Arguments: `$ARGUMENTS` (`$1` = project, `$2` = suite id, `$3` =
feature description or JIRA key). Act as **test-lead**; governing rule `docs/test-practices.md`.

**If `$1`, `$2`, or `$3` is missing, stop and ask before doing anything else** — per `CLAUDE.md`'s
hard rule on confirming an ambiguous target: which project/device, which suite, and what's the
feature (a JIRA key, or a plain description if there isn't one yet)?

1. **Understand the feature.** Pull the story/scope from JIRA via the Atlassian MCP if `$3` is a key;
   read any updated UX flow / requirements. A new feature often **changes existing flows**, not just
   adds a standalone one.
2. `python -m system_test_ops cases --project $1 --suite $2` to see what exists.
3. **Apply the rubric:** does an existing flow test now need extra steps (feature changes its path)?
   Prefer **extending the owning flow test**. Only add a **new** case for a genuinely distinct new
   behaviour/risk, placed in the area that owns it; ride values/variants as data-variation lines.
4. If the feature adds **new screens**, add them to the `HMI Screen Validation` section (one per
   screen) as well as into the functional flow that uses them.
5. Set `TESTRAIL_WRITE_SUITE_ID=$2`; author/extend via `*.cases.yaml` (`match:` to update existing).
   `push --commit [--update]`. Link the story via Refs.
6. Done when `audit --suite $2` is CLEAN and the impacted flow tests reflect the new behaviour.
   Note any old cases the feature **supersedes** for retirement (`ZZ_DELETE_REVIEW`).
