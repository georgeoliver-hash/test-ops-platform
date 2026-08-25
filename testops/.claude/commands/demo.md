---
description: Live-demo mode — quick readiness check, find a real current Translink JIRA target, run a real audit against it, present it cleanly for someone else to talk over. Usage /demo
argument-hint: (no arguments — I'll find a target and confirm with you)
---

You are running a **live demo** in front of an audience (managers, QA, testers). George is doing
the talking; your job is to produce one genuine, current, decision-ready result fast, with minimal
text on screen, so he has something real to point at. This is NOT `/start` — skip the onboarding
narration, setup checks, and doc-dumping. Assume the environment already works.

## 1. One-line readiness confirmation (5 seconds, not a report)

Run `python -m system_test_ops doctor` silently and just say: **"Connected — TestRail and JIRA are
live."** If anything is actually broken, say so plainly and stop (don't debug live in front of the
room) — suggest falling back to a pre-made artifact instead.

## 2. Find a real, current target — don't use a pre-picked one

Search live for something genuinely current, not a case prepared earlier this session. **`TIBU` is a
shared, multi-customer JIRA project — most of its recent activity is NOT Translink** (Rouen, Amiens,
Monaco, Avignon and others all file under the same project key). Filter for Translink explicitly,
don't just take "most recently updated."

Use the Atlassian (Rovo) MCP against `flowbird.atlassian.net`, project `TIBU`. Try, in order, until
you get a usable shortlist of 3–5, **all confirmed Translink**:

1. **A recent Translink fix version** (most reliable — Translink releases are named `TL_<device>_x.x.x`
   or `TL <Device> vx.x.x`) — `searchJiraIssuesUsingJql`: `project = TIBU AND fixVersion is not EMPTY
   ORDER BY updated DESC`, then filter the returned `fixVersions` client-side for names starting
   `TL` / containing "Translink", prefer one tied to a device this repo already covers
   (POS/ETM/PV/TVM/HHD/GV).
2. **A recent QA-passed / ready-for-release Translink bug** — `project = TIBU AND status in ("Ready
   for Release", "Done") AND (summary ~ "POS" OR summary ~ "ETM" OR summary ~ "TVM" OR summary ~ "HHD"
   OR summary ~ "GV" OR summary ~ "PV" OR summary ~ "Translink") ORDER BY updated DESC` — read each
   result's summary/fixVersion to confirm it's actually Translink before offering it, don't trust the
   text match alone.
3. **Epics** are a weak signal here — most current epics belong to other customers. Only use one if
   its summary explicitly says Translink/TL and nothing better turned up from 1–2.

Present the shortlist in one short line each (key + summary), ask George to pick one (or pick the
most compelling yourself and say which and why — recency + relevance to a built suite). Do not spend
more than one exchange on this.

## 3. Run the real thing against it

Match the pick to the right existing command and run it for real:

- **Fix version or epic** → `/audit-coverage <project> <fix-version-or-epic-key>` (the real
  coverage-analyst/run-historian pipeline — this takes a couple of minutes; tell George it's running
  and let him keep talking while it works).
- **A single bug** → the `/fold-defect` procedure: check existing coverage first, then either fold or
  author one new case, `push --commit`, confirm the audit stays clean. (Do NOT reuse `TIBU-29756` /
  `C4105016` — that one's already been pushed. Pick whatever's actually current.)

## 4. Present the result for talking over, not reading

However it turns out — covered, partial, missing, stale, or a freshly-authored case — summarize in
**at most 5 lines**: what was checked, the verdict, and the one most interesting finding (a gap, a
contradiction, a fresh case created). Do not paste the full report. Point to the report path /
new case id and stop talking — let George take it from there.

## Guardrails

Same as everywhere else in this repo: read-only except `TESTRAIL_WRITE_SUITE_ID`, no invented
coverage, cite everything, conformance audit must stay clean after any write.
