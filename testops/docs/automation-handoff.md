# Automation handoff — system-test-ops → SIT (primary) / automation-tests (secondary)

How the TestRail suites built/maintained here feed the test-automation side. **Two separate repos,
different governance, deliberately not merged** (different tech, different owners, different CI) —
this doc is the contract that lets them stay separate but still speak to each other.

- **`dev/sit`** (`flowbird-group/sit`, Robot Framework) — the **official** automation suite, owned by
  the automation team (Mat/Tayo/Persistent et al). This is the primary consumer today.
- **`dev/automation-tests`** (pytest + ADB/Appium/Playwright) — an earlier exploratory project, now
  **secondary** to SIT (confirmed 2026-07-28). The JSON-backlog mechanism below was originally built
  for this repo and still works for it, but SIT is where real work is happening.

## The pattern that's actually working today (SIT, direct citation — no export step)

This is already live, unprompted, in SIT's `feature/pos-device-family` branch (PR #52) — it needs no
new tooling, just documenting so anyone can repeat it:

1. Open the TestRail case in `system-test-ops` (or its live suite export) for the case you're
   automating.
2. Write the `.robot` test mirroring its Given/When/Then **verbatim**, wording included.
3. Tag it `[Tags]    testrailid=C<case_id>` — this is the traceability link back to TestRail.
4. Carry over `destructive` as a Robot tag, exactly as tagged in the case.
5. If the case (or the underlying device capability) has a `**GAP**`/`**UNCONFIRMED**` marker, or the
   automation itself is blocked (missing UI-driving layer, needs a physical card fixture), **don't
   invent a passing test** — use `[Setup]    Skip    GAP: <reason>` and say why in `[Documentation]`,
   citing the same gap. This mirrors system-test-ops' own "no gap-filling" rule on the automation side.

**Worked example** — `dev/sit/Tests/POS/SignOn/test_signon_lockout.robot` (real, in that repo today):

```robot
*** Test Cases ***
Device Locks After The Configured Number Of Failed Attempts
    [Documentation]    C4099922. GIVEN the TMS-configured failed-attempt threshold, WHEN the
    ...                operator enters incorrect credentials that many times, THEN the device
    ...                locks and shows the Device Locked screen. Refs: TIBU-22672, TIBU-22003.
    ...
    ...                ${LOCKOUT_THRESHOLD} is a placeholder, NOT a confirmed value -- GAP:
    ...                the real TMS-configured threshold for the target environment must be
    ...                confirmed before this is run for real (it is not always 3).
    [Tags]    testrailid=C4099922    destructive    Regression
    [Setup]    Skip    GAP: needs the confirmed TMS-configured lockout threshold for this environment before running for real -- see [Documentation]
    ${LOCKOUT_THRESHOLD}=    Set Variable    ${3}
    Given the operator is signed off
    When the operator attempts to sign on with an unrecognised ID and PIN ${LOCKOUT_THRESHOLD} times
    Then the Device Locked screen should show the following labels
    ...    Device Locked
    ...    Present Supervisor Card
```

That's the whole contract for direct, ad-hoc authoring — no CLI step required. The JSON-backlog
mechanism below is still available (useful for bulk "here's everything automatable in this suite, go"
handoffs), but isn't what's actually driving today's SIT work.

## The bulk-handoff link, in one line (JSON backlog — optional, either repo can consume it)

system-test-ops marks every case **Automatable: Yes/No** (+ a **Cross-check** flag) during
enrichment; `export-automation` emits the `Yes` cases as a **backlog** that either automation repo
can implement from, with each automated test linked back to its **TestRail case id**.

```
TestRail suite  --enrich-->  [Automatable: …] on Expected  --export-->  automation-backlog.json
                                                                              |
                                                    SIT (.robot, testrailid= tag) or
                                                    automation-tests (pytest, @case() marker)
                                                    -- either way, tagged + referencing the case id
```

## Producing the backlog (system-test-ops side)

```
python -m system_test_ops export-automation --suite <suite_id>          # automatable only
python -m system_test_ops export-automation --suite <suite_id> --include-manual
```

Writes (read-only — nothing is mutated in TestRail):
- `reports/<project>/<suite>/<date>/automation-backlog.json` — machine-readable handoff
- `reports/<project>/<suite>/<date>/automation-backlog.md` — human view, grouped by priority

`reports/` is gitignored (generated). The automation repo should **run the CLI** to get a fresh
backlog rather than rely on a committed copy — the marker is re-judged whenever cases change.

## Consuming the backlog (either automation repo)

Each entry:

```json
{
  "ref": "C4099911", "case_id": 4099911,
  "title": "Sign On — incorrect credentials",
  "section_path": ["Functional", "Sign On & Session", "Failures & Lockout"],
  "feature": "Failures & Lockout", "device": "POS",
  "priority": "High", "estimate": "6m",
  "automatable": true, "cross_check": ["CloudFare"], "destructive": false,
  "refs": "REQ-0050,TIBU-22671",
  "gherkin": { "given": "…", "steps": [{"when": "…", "then": "…"}], "expected": "…" }
}
```

Rules:
1. **Traceability — reference the case id.** Put `ref` (e.g. `C4099911`) in the test so a run result
   maps back to its TestRail case — in SIT this is `[Tags]    testrailid=C4099911` (see the worked
   example above); in `automation-tests` a `@case("C4099911")` marker or equivalent. This is what
   lets a TestRail run be reconciled either way.
2. **Markers.** Mirror `device` and `feature` as tags in whichever repo's own convention (SIT:
   `Test Tags    C=POS    feature=SignOn`; automation-tests: pytest markers). Where `destructive:
   true`, tag it as destructive in that repo's convention too — those are deselected by default (a
   destructive test can lock out the device).
3. **Cross-check is part of the assertion.** `cross_check` lists the back-office systems the case
   asserts the event reaches (CloudFare / MERIT / SmartTrack). The automated test isn't "done" until
   it verifies the event actually landed there, not just the on-device outcome.
4. **Priority = order.** Work High → Normal → Low. `estimate` is the manual execution time (a rough
   sense of complexity).
5. **The marker is a starting point.** `automatable` is a system-test-ops judgement. If the
   automation engineer disagrees for a specific case (e.g. a card tap can be driven by a hardware
   rig, or a "Yes" turns out to need an oracle that doesn't exist), override it — and tell
   system-test-ops so the marker is corrected at source (re-run `tools/enrich_cases.py`).

## What "Automatable" means (three tiers — Appium available on POS, 2026-06-11)

The `automation` field is one of:
- **`yes`** — fully software-automatable via Appium/ADB: sign-on PIN entry, navigation, fare look-up,
  menus, config, force-comms, version pages, lockout logic, comms resilience. No physical artifact.
- **`partial`** — the **UI flow is automatable**, but a step needs a **hardware fixture or human
  eye**: presenting/tapping a smartcard or contactless card, scanning a barcode, printing/receipt,
  cash, MIFARE/DESFire. Automate the flow; stub or fixture the physical step.
- **`no`** — leave to a human / rig: per-screen HMI visual checks, performance/timing, power
  interruption + reboot recovery, brightness/audio/LED, DST, firmware/FEIG OTA.

The backlog includes **`yes` + `partial`** by default (`automatable: true`); `no` is excluded unless
you pass `--include-manual`. Tackle `yes` first, then `partial` as fixtures come online.

The tiers are a system-test-ops judgement (rule 5: override per case and tell us). To re-tune the
boundaries, edit the `TIER_NONE` / `TIER_PARTIAL` rules in `tools/enrich_cases.py`, re-enrich, and
re-export — the backlog follows.

## Keeping it in sync

- Cases change here → re-run `enrich_cases.py` (sets the marker) → re-run `export-automation`.
- Never hand-edit the backlog; it is generated. Edit the marker at source (enrichment) instead.
- Reverse direction (writing automation status back into TestRail) is **not** wired up — project 42's
  template doesn't persist a custom automation field, and the API can't move/attach. If/when an
  automation status field is enabled, add it to `enrich_cases.py`.
