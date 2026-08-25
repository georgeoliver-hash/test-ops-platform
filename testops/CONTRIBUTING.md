# Team workflow — sharing this via a repository

## The mental model (this is the bit that prevents people overriding each other)

There are **two layers**, and they're kept in sync deliberately:

1. **The repo = the source of truth.** The YAML case specs (`proposals/.../*.cases.yaml`), the agents,
   docs, and `knowledge/` live in git. **Git never silently overwrites** — when two people change the
   same lines it raises a *conflict* and a human resolves it in a Pull Request. Branches + PRs are how
   "everything gets merged together" safely.
2. **TestRail = a render target.** The live suite (`GG - POS - Claude Suite`) is **not** in git and has
   **no branches**. You don't hand-edit it and hope; you **push the *merged* repo specs to it**. So the
   merge happens in git first, and TestRail receives the agreed result.

> Golden rule: **changes are made in the repo (branch → PR → merge), then pushed to TestRail from
> `main`.** Don't make competing edits directly in the TestRail UI — if you do, fold them back into the
> YAML so the repo stays authoritative (otherwise the repo and the live suite drift apart).

## One-time setup
The repo already lives on GitHub — nothing to create, just join it:
1. **Install git** (if not already): `winget install Git.Git`, or via IT.
2. **Clone it**: `git clone https://github.com/georgeoliver-hash/system-test-ops.git`.
3. Create your **own `.env`** (copy `.env.example`, fill in your TestRail creds). **`.env` is
   gitignored and must never be committed** — it holds your password/API key.
4. Run `/start` in Claude Code (or `python -m system_test_ops doctor`) to check you're set up.

## Everyday workflow (per change)
```
git pull                      # get latest main
git checkout -b <your-change> # e.g. tvm-sign-on, pos-topup-fixes
# ...edit the YAML specs / knowledge / docs...
git commit -m "..."           # commit your work
git push -u origin <branch>   # push the BRANCH (not main)
# open a Pull Request -> review (standards-keeper + a human) -> merge to main
```
- **Branches isolate your work** — your changes can't clobber anyone else's until reviewed/merged.
- **PR review** is the quality gate (the `standards-keeper` checks the standard; a human approves).
- Conflicts (rare, since cases are per-area files) are resolved in the PR — nothing is lost.

### The conformance audit is a required gate (everyone, every change)
Before a PR is ready, the suite's standard-conformance audit must be **CLEAN of blocking findings**:
```
python -m system_test_ops audit --suite <id>   # read-only; exits non-zero on blocking findings
```
`push --commit` runs this automatically, but run it explicitly after manual TestRail UI edits too. It
writes `reports/<project>/<suite>/<date>/alignment-audit.md`. Blocking findings (mojibake, missing
objective/preconditions, malformed When/Then, genuine compound THEN, stray tags) **must be fixed
before merge**; the two title checks are advisory. Because it exits non-zero, it can gate a CI/PR
check — wire it in once the remote is set up. This is the same for the first person who picks up the
repo as for everyone after: a suite isn't done until its audit is clean.

## Pushing the merged result to TestRail
- Only push to TestRail **from up-to-date `main`**, after the PR is merged.
- **One coordinated push per suite at a time** (or split by area/owner) — TestRail has no branches, so
  two people pushing the same suite simultaneously is the only real clash risk. Agree who owns a suite.
- The `push` command is **idempotent** (skips/updates by title, per section) and **writes only the
  configured new suite** — so re-running from `main` safely reconciles TestRail to the repo.

## Avoiding "someone overrode my work"
- **In the repo:** branches + PRs. Git merges text and stops on conflicts — your merged work stays as
  the base; others branch off it. Nothing is silently overwritten.
- **In TestRail:** per-suite/area ownership + push-from-main-only. Don't hand-edit the same cases two
  people at once; fold any UI tidies back into the YAML.

## Large assets (kept OUT of git)
The flow **images (~193 MB)** and `overflow_data.json` (~9 MB) are gitignored — too heavy for a shared
repo. Keep them in a shared store (SharePoint / network drive / Overflow itself). What **is** committed
is the **derived text**: `flow-annotations.md`, the transcribed flow maps, and the case specs — all
diff/merge-friendly. (If the team wants the raw assets versioned, use **Git LFS** instead.)

## New device/project
Read `docs/new-work-setup.md` first — especially **"What you must provide first"** — then run
`discover-fields` for the project's case schema. Audit-first: missing inputs = guessing = hindered suites.
