# Start here — onboarding (read this first, ~3 minutes)

You've cloned **automation-tests**: the system-test automation framework for Arrive transit/parking
devices (Flowbird lineage). It drives a real device's UI (Android POS via ADB/Appium, or a WinCE ETM
via SSH/SFTP) and verifies the side effects — EventLog rows, on-device audit ledger, and (later) the
back-office system. It runs in Claude Code, and tests are written from the **automation backlog** the
sibling `system-test-ops` repo exports from TestRail.

You don't need to memorise the setup. **Open this repo in Claude Code and type `/start`** — Claude
runs a readiness check, tells you exactly what it still needs from you, and gets you to a green run.
This page sets expectations first.

## The thing that makes this repo different: it needs real hardware

Unlike a pure software project, a test run touches a **physical device on the lab network**. That
means a few steps are irreducibly yours — they can't be automated away:

| You do (some are one-time, some per-session) | Claude does (for you) |
|---|---|
| Install Python 3.11+, Node + Appium, `adb` (platform-tools) | Create the `.venv`, `pip install -e ".[all]"` |
| Put the device on the lab network / VPN; keep ADB's TCP window open | Run the test suite, capture UI dumps + logcat on failure |
| Start the Appium server (`appium`) | Drive the POS via the Navigator/AndroidShell helpers |
| Set SSH device passwords as env vars (secret) | Write new tests from the automation backlog, mark destructive ones |
| Decide which cases are worth automating vs leaving to a human eye | Generate the Jira-ready run report + defects |

The point of `/start` (and `python -m tools.doctor`) is to surface those **up front** so they don't
ambush you mid-run.

## Readiness, in two commands

- **`python -m tools.doctor`** — the broad preflight: Python/venv/deps, `adb` on PATH, Appium CLI +
  **server reachable**, the project's `devices.yaml` loads, SSH device secrets present. Add
  `--device` to also probe whether the device's ADB window is open right now. Grouped into
  **READY / CLAUDE CAN HANDLE / NEEDS YOU / CHECK MANUALLY**.
- **`python -m tools.adb_ready --project translink --wait 30`** — the fast, run-time check: *is the
  device reachable this very moment?* The TCP-5555 adbd window flips intermittently, so run this
  right before kicking off a suite.

## The 60-second path

1. Open this folder in Claude Code (`claude` in the repo root).
2. Type **`/start`** (or run `python -m tools.doctor`). Clear the **NEEDS YOU** items:
   - Device on the network; `adb connect <serial>`.
   - Appium server running (`appium`).
   - Any SSH device password env vars set.
3. `python -m tools.adb_ready --project translink --wait 30` until it says READY.
4. Run the suite:
   ```powershell
   $env:APPIUM_URL="http://127.0.0.1:4723"
   robot --variable PROJECT:translink --include device_types:POS --exclude destructive projects/translink/tests
   ```
   Destructive tests (lockout/reboot) are excluded by default — opt in with `--include destructive`.
5. Want new coverage? Ask Claude to write tests from the **automation backlog** that `system-test-ops`
   exports (`reports/<project>/<suite>/<date>/automation-backlog.json`) — each entry carries its
   TestRail case id (e.g. `C4099911`) for traceability.

## Where the detail lives (Claude reads these automatically)

- **`CLAUDE.md`** — the conventions, helper layers (AndroidShell / EventLog / Navigator / POSStrings),
  the markers every test needs, and the run-reporting setup. Loaded every session.
- **`docs/architecture.md`** — deeper design notes.
- The **automation handoff contract** is documented in the `system-test-ops` repo
  (`docs/automation-handoff.md`) — that's the source of the backlog this repo consumes.

Unsure at any point? Run **`python -m tools.doctor`** again, or just type **`/start`**.
