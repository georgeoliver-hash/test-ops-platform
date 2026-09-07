# Test-Ops Console — issues & feedback

How to use: drop notes under whichever sidebar item you're testing, using the template
below. I'll read this file directly, fix what I can, and mark items `Status: fixed` with a
one-line note on what changed (and the commit, once committed).

Template for a new entry:

```
### Short title
**Severity:** blocker / annoying / nice-to-have / Q+A
**What happened:** ...
**Expected:** ...
**Status:** open
```

---

//Overview — General UI - Sidebar etc

### Arrive logo
**Severity:** nice-to-have
**What happened:** Logo is really small
**Expected:** Logo to fit the top left nicely
**Status:** fixed — height 22px → 36px, row padding increased. Look and confirm it reads well against the sidebar purple.

### dashboards and content
**Severity:** nice-to-have
**What happened:** Doesn't fit the full space, always a large gap, space to the right of the dashboard content or any content in any tab
**Expected:** Responsive, and fits nicely to width of content area space
**Status:** fixed — `.content` was hard-capped at 1180px; raised to 1600px + `width:100%`. Stat/dashboard grids already flex, so they should now fill wide screens. Flag if it still feels narrow on your monitor.

//Overview - Change target

### Changing target
**Severity:** Q+A
**What happened:** We can select project, device and model, build but how do we know were targeting the right suite? or the right old suite to also gain knowledge from - maybe there is a gap here with how we select the old suite, and the new targeted suite to work in
**Expected:** Users should be warned, and it should be very visible what project, device, model, build is currently pointing to old and new suites - and the ability to change this should be easy but not withut security checks - someone should approve the changed targeted suites maybe me for now my user
**Status:** fixed (first pass) — modal now shows a real "Old (read-only source) / New (write target)" readout, keyed per project+device pair (not a single global suite — each project/device combo gets its own real pair, per your follow-up). Only Translink/POS has a documented pair right now (`AA-POS Acceptance Test` → `GG - POS - Claude Suite`, from system-test-ops' CLAUDE.md); everything else honestly shows "Not configured" rather than guessing. Added a required approval checkbox that must be re-ticked every time (resets on any project/device change) before "Approve & apply target" enables — today you're the sole approver by ticking it; once writes are wired in this becomes a real sign-off gate rather than just a UI nicety. Top-bar chip now also shows both suites once applied.
**Follow-up needed from you:** more real old/new suite pairs for other devices so more combinations stop showing "Not configured" — I don't have those documented anywhere yet, so I won't guess them.

//Overview — Suite health

## Overview — All processes

## Overview — Features

## Overview — Repo map

## Overview — Gap register

## Build group (onboard-suite, new-suite-from-docs, ingest-docs, add-feature, consolidate, export-automation)

## Audit group (audit-coverage, audit-flows, audit, resolve-gaps)

## Maintain group (fold-defect, review-runs, maintain)

## Target switcher (Change target modal)

## General UI/UX (layout, colours, responsiveness, anything cross-cutting)
