# Getting started

This walks a brand-new teammate from zero to a first coverage audit. ~15 minutes.

## 0. Prerequisites

- **Claude Code** installed and signed in.
- **Python 3.11+**.
- A **TestRail** login and a **JIRA** (Atlassian Cloud) login for your org.
- This repo cloned somewhere local, e.g. `C:\Users\<you>\dev\system-test-ops`.
- **Chrome, with the Claude extension installed** — the preferred way to capture UX/design flows
  (Overflow etc.) is having that extension transcribe them verbatim, straight from the browser. Not
  needed for coverage/run-history work, only for bringing in new UX flow material — see
  `knowledge/flows/README.md`.

## 1. Install the Python core

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

(macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`.)

## 2. Connect TestRail (read-only API key)

TestRail has no MCP, so we read it with an API key.

1. In TestRail: **My Settings → API Keys → Add Key**. Copy the key.
2. In the repo, copy the template and fill it in:
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env`:
   ```
   TESTRAIL_URL=https://yourcompany.testrail.io
   TESTRAIL_USER=you@arrive.com
   TESTRAIL_API_KEY=<the key you just copied>
   ```
   `.env` is gitignored — your key never gets committed.
3. Verify connectivity:
   ```powershell
   python -m system_test_ops check
   ```
   You should see `OK — connected to TestRail.` and a list of projects with their numeric IDs.
   Note the project ID you care about (you can also set `TESTRAIL_PROJECT_ID` in `.env`).

## 3. Connect JIRA (Atlassian MCP)

JIRA is read through the **Atlassian (Rovo) MCP** — each person connects their own account.

1. In Claude Code, run `/mcp`.
2. Choose the **Atlassian** server and complete the browser sign-in. You should see
   `Authentication successful. Connected to ... Atlassian ...`.
3. That's it — the agents can now read fix versions and issues as you.

> Why MCP for JIRA but an API key for TestRail? JIRA already has a first-class MCP, so we use it
> (no token to manage). TestRail doesn't, so we use its API key. Both stay read-only.

## 4. Export a baseline (proves the plumbing)

```powershell
python -m system_test_ops cases --project translink --suite POS
python -m system_test_ops runs  --project translink --suite POS --last 10
```

These write JSON + markdown into `reports/<project>/<suite>/<date>/`. Open `cases.md` and
`run-health.md` to confirm you're seeing real data.

## 5. Run your first audit

In Claude Code:

```
/audit-coverage translink 5.0.0
```

The `test-lead` agent will pull the 5.0.0 fix version from JIRA, read the POS suite, and write a
coverage report (covered / partial / missing / stale) plus Gherkin drafts for the gaps into
`reports/translink/POS/<date>/`.

To review run history instead:

```
/review-runs translink POS --last 10
```

## 6. Read the standard before you write cases

All proposed cases follow [`gherkin-standard.md`](gherkin-standard.md). Skim it once — it's what
keeps every project's suite looking the same.

## 7. Know the conformance gate (you'll meet it on every change)

Authoring isn't finished until the suite passes the standard-conformance audit:

```powershell
python -m system_test_ops audit --suite <id>   # read-only; defaults to TESTRAIL_WRITE_SUITE_ID
```

It checks every case against the standard and writes `reports/<project>/<suite>/<date>/
alignment-audit.md`. **Blocking** findings must be **0** before you open a PR; the two title checks
are advisory. `push --commit` runs this for you automatically, and the command exits non-zero on
blocking findings so it can gate CI/PRs. This applies to everyone, all the time — see
[`test-practices.md`](test-practices.md) "Conformance audit". (And never rewrite the
`*.cases.yaml` specs with PowerShell `Set-Content`/`Out-File` — it corrupts encoding and creates
duplicate cases.)

## Onboarding a new project / device / suite

The steps above get *you* connected. To bring a **new project, device, or suite** into the repo
(including importing an old suite and its past-bug backlog), follow the repeatable playbook in
**[new-work-setup.md](new-work-setup.md)** — copy the `knowledge/projects/_TEMPLATE.md` and
`knowledge/devices/_TEMPLATE.md`, capture the flows, pull what exists, and design the new suite using
**[test-practices.md](test-practices.md)**. No code changes are ever needed for a new project.

## Troubleshooting

- **`config error: Missing TestRail credentials`** — you haven't created `.env`, or a value is
  blank. Re-check step 2.
- **`project '…' not found`** — run `python -m system_test_ops check` to see exact project names/IDs.
- **JIRA agent can't see the fix version** — re-run `/mcp` and confirm the Atlassian server shows as
  connected; make sure your JIRA account can see that project's releases.
