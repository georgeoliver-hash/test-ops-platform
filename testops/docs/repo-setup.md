# Repo setup & the shared-knowledge workflow

How to publish system-test-ops to your GitHub repo, how teammates use it, and how their
knowledge updates flow back to everyone. **The repo is the source of truth; TestRail is the
render target** — the repo holds the case *specs* and *knowledge*, and `push --commit` renders
them into a TestRail suite.

## What is (and isn't) committed

| Committed (travels to everyone) | Local only (never committed) |
|---|---|
| Python core, `.claude/` agents + commands, `docs/` | `.env` (secrets — each person sets their own) |
| `knowledge/` curated facts (projects, devices, flow **annotations**) | `reports/` (generated output) |
| `proposals/**/*.cases.yaml` (the case specs) | raw assets: `*.xlsx`/flow images/`overflow_data.json` (shared store) |
| `docs`, `CONTRIBUTING.md`, `ONBOARDING.md` | `.venv/`, caches |

The `.gitignore` already enforces this — including excluding the ABT spreadsheet (it holds real test
card PANs). Raw assets live in a **shared store** (SharePoint/Teams/network drive), not git.

## 1. First push (one-time, you)

1. **Install Git** (Git for Windows, or GitHub Desktop for a GUI).
2. From the repo root:
   ```
   git init
   git remote add origin <your-github-repo-url>
   git add .
   git status          # ← VERIFY: no .env and no *.xlsx appear. If they do, STOP.
   git commit -m "system-test-ops: AI test-ops toolkit + Translink BOS/ABT/POS/ETM/PV suites"
   git branch -M main
   git push -u origin main
   ```
3. Keep the repo **private** (internal TestRail/JIRA URLs, real fare data, test PANs).

## 2. How a teammate uses it

1. `git clone <repo>` and open the folder in Claude Code.
2. Type **`/start`** — the readiness preflight tells them what to set up.
3. They create their own `.env` (TestRail key) and connect their own JIRA MCP (`/mcp`).
4. They grab any raw assets (flow exports, spreadsheets) from the shared store into `knowledge/`.
5. They drive the work with the commands (`/onboard-suite`, `/consolidate`, `/add-feature`,
   `/fold-defect`, `/maintain`, `/audit`, `/export-automation`).

Each engineer's Claude works in **their own clone** with **their own credentials**. Claude's
personal memory does **not** travel between people — only the repo does. That's why hard-won facts
live in `knowledge/` (in the repo), not just in memory.

## 3. The update-and-push-back loop (the collaboration model)

When a teammate's work updates knowledge or case specs, this is how it gets back to everyone:

```
git pull                      # start from latest main
git checkout -b add-hhd-suite # a branch for the work
   … Claude edits knowledge/**, proposals/**/*.cases.yaml, docs/** …
   … python -m system_test_ops audit   → must be CLEAN of blocking (the gate) …
git add -A
git commit -m "HHD: add knowledge + onboarding suite specs"
git push -u origin add-hhd-suite
   → open a Pull Request on GitHub → review → merge to main
git checkout main && git pull  # everyone syncs with `git pull`
```

Key points:
- **Claude can do the git steps** (branch, commit, push, open PR) once Git is installed — ask it to
  "commit this and open a PR". Or use GitHub Desktop by hand.
- **What flows back** = text files: `knowledge/` facts, `proposals/*.cases.yaml`, `docs/`, agents,
  commands. These are diff-able and review-able.
- **TestRail is updated separately** by `push --commit` (which renders the committed specs into the
  suite). Two people building different suites don't collide in git — they touch different
  `proposals/` files and different TestRail suites.
- **The conformance audit is the PR gate** (`CONTRIBUTING.md`): a change isn't done until
  `python -m system_test_ops audit` is CLEAN of blocking findings. `audit --gate` exits non-zero, so
  it can gate CI too.
- **Merge conflicts** are rare because work is partitioned by knowledge/proposal file; when they
  happen they're plain-text and resolved normally.

## Summary of the two "pushes" (don't confuse them)
- **`git push`** — shares your repo changes (specs, knowledge, docs) with colleagues.
- **`python -m system_test_ops push --commit`** — renders case specs into the TestRail suite.
