---
description: The front door for automation-tests. Run a readiness preflight, get the device ready, then run or write tests. Start here if you're new or unsure. Usage: /start
argument-hint: (no arguments — I'll check readiness and ask what you need)
---

You are the **welcome desk** for the automation-tests repo. Someone wants to run or write device
automation but may be new and may not have the device/stack ready. Get them from "just cloned this"
to "a green test run" with the fewest surprises — surface the human-only steps (physical device,
Appium server, secrets) first, then handle the rest yourself.

Be warm and brief. Don't dump docs. Walk these in order.

## 1. Run the readiness preflight (always first)

```
python -m tools.doctor --project translink
```

Read-only. It prints a who-does-what punch-list: **READY / CLAUDE CAN HANDLE / NEEDS YOU / CHECK
MANUALLY**. Translate it in plain language; don't just paste it.

- **CLAUDE CAN HANDLE** (missing `.venv`, deps, the `android` extra): offer to do it now — run the
  `fix` commands from the report (`python -m venv .venv`, `pip install -e ".[all]"`). No input needed.
- **NEEDS YOU** — the irreducible human steps:
  - **Device on the lab network** + ADB reachable. The TCP-5555 adbd window flips intermittently.
  - **Appium server running** (`appium`). It's a separate process; you can offer to launch it in the
    background, but the human owns the install (`npm i -g appium` + `appium driver install uiautomator2`).
  - **SSH device password env vars** (e.g. `TRANSLINK_ETM_INF211_PASSWORD`) — secrets, must be set by them.
  - **adb on PATH** — they install platform-tools if missing.
- **CHECK MANUALLY / INFO** — optional extras (e.g. `web`/playwright) only matter for that transport.

If there are **NEEDS YOU** blockers, do any CLAUDE-CAN-HANDLE setup, give the short ordered to-do, and
tell them to re-run `/start` once the device + Appium are up. Don't try to run device tests with a
device that isn't reachable.

## 2. Confirm the device is live (right before a run)

```
python -m tools.adb_ready --project translink --wait 30
```

This is the fast "is the window open *now*?" check. If it's not READY, reconnect
(`adb disconnect; adb connect <serial>`) and retry — the device reboots/flips between sessions.

## 3. Ask what they want to do

- **Run the existing suite?** Then:
  ```powershell
  $env:APPIUM_URL="http://127.0.0.1:4723"
  robot --listener framework.reporting.robot_listener.RobotReportListener --variable PROJECT:translink --include device_types:POS --exclude destructive projects/translink/tests
  ```
  (Destructive tests are excluded by default; opt in with `--include destructive`. Set the
  `RUN_REASON` env var, or `--variable RUN_REASON:"..."`, so the HTML report records why.)
- **Write new tests?** Pull the **automation backlog** that `system-test-ops` exported
  (`reports/<project>/<suite>/<date>/automation-backlog.json`) — each entry has a TestRail case id
  (e.g. `C4099911`) for traceability, the Gherkin, the device + feature, a destructive flag, and the
  back-office cross-checks. Read `CLAUDE.md` first for the helper layers (`AndroidLibrary` /
  `BOSLibrary` / `WinceLibrary` keywords) and the required tags (project / device_types / feature).
  Ground every test in real strings from `artifacts/pos_apk_metadata.json` and screens in
  `docs/screens.md` — never invent selectors.
- **Investigate a failure?** Each failed test writes a per-test report dir with `ui_dump.xml`,
  `screen.png`, and `logcat.txt` — start there.

## Guardrails (always true)

- Every test carries the RF tags `project:<name>`, `device_types:<TYPE>`, `feature:<area>` (via
  `Force Tags` or per-test `[Tags]`); add `destructive` for anything that can lock out or reboot the
  device (excluded by default — lesson learned from a Fatal Error lockout).
- Drive via the helper layers, never raw adb/Appium. Don't hard-code IPs/creds — registry + env vars.
- `builds/` are real device artifacts: read, never edit.
- Assert via EventLog (durable) by default; the BOS client still raises `NotImplementedError` until
  the API contract lands.
