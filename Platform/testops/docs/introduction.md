# Introduction

`system-test-ops` is a small AI team that helps the system-test department keep its **TestRail**
suites honest. It does two jobs and writes its findings to `reports/`.

## The mental model

```
          JIRA fix version                 TestRail suite                 TestRail run history
        (stories/features/bugs)        (Gherkin test cases)            (last N runs of the suite)
                  │                              │                                │
                  └──────────────┬───────────────┘                               │
                                 ▼                                                ▼
                        coverage-analyst                                   run-historian
                 "is the release covered?"                       "which cases are stale/flaky/dead?"
                                 │                                                │
                                 └────────────────────┬───────────────────────────┘
                                                       ▼
                                                  test-lead
                                       consolidates → decision-ready report
                                                       │
                                                       ▼
                                               gherkin-author
                                  drafts missing/edited cases to the standard
                                                       │
                                                       ▼
                                              standards-keeper
                                  checks syntax + cross-project consistency
```

## The two workflows

### 1. Coverage audit (before a run)
You're prepping a fix version — e.g. **Translink POS 5.0.0** with its stories, features and bug
fixes. Run `/audit-coverage translink 5.0.0`. The team reads the fix version from JIRA, reads the
POS suite from TestRail, and tells you for each scope item whether it's **covered / partial /
missing / stale**, citing case IDs and issue keys — plus ready-to-paste Gherkin drafts for the gaps.

### 2. Run-history review (continuous maintenance)
Run `/review-runs translink POS --last 10`. The team looks across the last 10 runs of the suite and
flags cases that are **always-failing** (probably invalid/outdated), **never-executed**, **flaky**,
**recently-regressed**, or **orphaned** — so you can decide what to **add / edit / remove /
reorganise**.

## Two principles that make it trustworthy

- **Read-only.** It never edits your TestRail data. It proposes; you apply.
- **Deterministic data, judgment on top.** A Python CLI fetches reproducible JSON from TestRail;
  the agents reason over that JSON and always cite their evidence (case id, run id, issue key).

## Where things live

- Conventions & the team roster → [`../CLAUDE.md`](../CLAUDE.md)
- How to connect JIRA + TestRail and run your first audit → [`getting-started.md`](getting-started.md)
- How to write a case so it matches everyone else's → [`gherkin-standard.md`](gherkin-standard.md)
