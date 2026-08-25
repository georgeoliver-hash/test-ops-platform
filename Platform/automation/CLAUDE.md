# automation-tests — Project memory for Claude

This is George's system test automation framework for Arrive transit/parking devices (Flowbird-lineage). Read this file at the start of every session before doing anything else.

## What this codebase is for

End-to-end system tests across **multiple projects**, each with a fleet of **heterogeneous devices**. A typical test:

1. Drives a device UI (Android app or web) to perform an action — e.g. operator sign-on, top-up, transaction.
2. Verifies the side effect on the **back-office system (BOS)** — typically an audit event with the right shape and timing.

This is **not** unit tests, **not** load tests. The framework's reason to exist is verifying that device behaviour and BOS state agree.

## Domain glossary

| Term  | Meaning |
|-------|---------|
| ETMS  | Electronic Ticket Machine System |
| POS   | Point of Sale terminal |
| TVM   | Ticket Vending Machine |
| GV    | Gate Validator |
| PV    | Platform Validator |
| BV    | Bus Validator (onboard card-tap device) |
| HHD   | Handheld Device |
| BOS   | Back Office System (audit / reporting) |
| GTFS  | General Transit Feed Specification (shared schedule data) |
| project | A customer deployment (e.g. Translink) owning a fleet of devices |

## Hierarchy

```
project (e.g. translink)
  └── device (e.g. translink-tvm-01)
        ├── os: linux | android
        ├── ui: web | android_app | none
        ├── transport: ssh | adb
        └── build: variant + version
```

A **test** declares which `(project, device_type)` combinations it applies to via Robot Framework tags. The runner picks the right transport + UI driver from the device registry.

## Layout

- `framework/` — generic, project-agnostic infrastructure. **Never reference a project name here.**
  - `framework/robot/` — the Robot Framework Library layer (`DeviceLibrary`, `AndroidLibrary`,
    `BOSLibrary`, `WinceLibrary`, `BuildDataLibrary`) — thin keyword wrappers over the plain-Python
    classes below them (`framework/transport`, `framework/android`, `framework/bos`, `framework/wince`,
    `framework/ui`, `framework/registry` — none of these are RF-specific, they're reused as-is).
  - `framework/reporting/robot_listener.py` — the RF Listener v3 that produces the Jira-ready
    `report.md`/`defects.json`/`index.html` per run (see "Run reporting" below).
- `resources/` — `.resource` files: `resources/common.resource` (shared Library imports + the
  `Collect Test Artefacts` teardown keyword every suite uses) plus per-project domain-level
  Given/When/Then resources, e.g. `resources/translink/signon.resource`.
- `projects/_common/` — tests that apply to most projects. Tagged `project:common`.
- `projects/<name>/` — project-specific `.robot` tests + the device registry (`devices.yaml`) for that project.
- `builds/` — read-only build artifacts pulled from real device SD cards. Reference only — do not edit.
- `tools/` — operational scripts (build inventory, device health, project listing).
- `.claude/agents/` — custom subagents for test authoring, maintenance, framework changes, etc.
- `docs/architecture.md` — deeper design notes and diagram.

## Conventions

- **Runner: Robot Framework** (`robotframework>=7.0`). Tests are `.robot` files under `projects/<name>/tests/`.
  Python only lives in `framework/` (the Library layer + the reused transport/UI/BOS/registry code) — no
  pytest anywhere in this repo.
- **Tags:** every test carries the RF-tag equivalents of the old pytest markers, either via `Force Tags` in
  the suite's `*** Settings ***` (when every test in the file shares them) or per-`[Tags]` on individual tests:
  - `project:<name>` (or `project:common`)
  - `device_types:<TYPE>` — uppercase from the canonical set; a test can carry more than one
  - `feature:<area>` — e.g. `auth`, `transactions`, `printing`, `sync`
  - `destructive` on any test that puts the device into a state requiring manual recovery (power cycle,
    supervisor unlock). `--exclude destructive` is the default run posture — opt in via `--include destructive`.
    Lesson learned 2026-05-21 when `test_invalid_signon_shows_failure_dialog` triggered a Fatal Error
    lockout on the live POS; the RF equivalent (`Invalid Signon Shows Failure Dialog`) still carries the
    same `destructive` tag.
- **Device selection:** RF has no dynamic per-device parametrization (pytest's old `metafunc.parametrize`).
  A suite targets exactly one device: `${DEVICE_ID}` (`--variable DEVICE_ID:...` or the `DEVICE_ID` env var)
  if set, else the first device in the project matching the suite's `${DEVICE_TYPES}` variable (a
  comma-separated list declared in each suite's `*** Variables ***` table).
- **Selecting tests:**
  - Bulk regression: `robot --variable PROJECT:translink --exclude destructive projects/translink/tests`
  - One feature: `robot --variable PROJECT:translink --include feature:auth --exclude destructive projects/translink/tests`
  - One suite: `robot --variable PROJECT:translink projects/translink/tests/signon/test_operator_signon.robot`
  - One test case: add `--test "Signon Screen Shows Id And Pin Labels"`
- **Device registry is config, not code.** New devices go in `projects/<name>/devices.yaml`. Code changes only when the *schema* changes.
- **Transport and UI are abstractions.** Tests call `DeviceLibrary`/`AndroidLibrary` keywords (`Run On Device`, `Tap Text`, `Sign On`, ...), never raw paramiko/Appium/Playwright — same rule as before, just keyword-shaped instead of fixture-shaped.
- **BOS assertions go through `BOSLibrary`.** `Expect BOS Audit Event    event=...    device_id=...    within_seconds=...` so retries and time tolerances live in one place.
- **Don't hard-code IPs, ports, or creds.** Registry + `.env`. Secrets via env vars referenced by name in `devices.yaml`, never committed.
- **Don't add backwards-compat shims.** This is pre-release; refactor freely.
- **Given/When/Then reads literally.** RF strips `Given`/`When`/`And`/`But`/`Then` before keyword lookup, so a domain-level resource keyword (e.g. in `resources/translink/signon.resource`) can be written once and used with whichever BDD prefix a test step needs — this is also how a test case maps onto the Gherkin `system-test-ops` exports per TestRail case.

## ADB-first testing (current focus, BOS deferred)

While the BOS API contract is still pending, tests drive and assert via **ADB only**. Helper layers:

- **`AndroidShell`** (`framework/android/shell.py`) — wrappers over ADB shell: `getprop`, `package_version`, `is_package_installed`, `is_process_running`, `tap/swipe/key/text`, `find_by_text`, `tap_text`, `screenshot`, `ui_dump`, `start_activity`, `force_stop`, `current_activity`. Uses `/data/local/tmp` for scratch files (not `/sdcard` — that path is missing on the way6 Android 5.1 build). RF keywords: `Getprop`, `Package Version`, `Is Package Installed`, `Is Process Running`, `Tap`/`Swipe`/`Send Key`/`Input Text`, `Tap Text`, `Take Screenshot`, `Get UI Dump`, `Start Activity`, `Force Stop App`, `Get Current Activity` (all in `AndroidLibrary`).
- **`EventLog`** (`framework/android/eventlog.py`) — reads `content://com.parkeon.data.eventLog/<type>` over ADB content query. **Preferred** for assertions: events have monotonic `eventIndex` and persist (no outbox race). API: `query`, `latest`, `latest_index`, `since(after_index=...)`, `wait_for(predicate=..., baseline_index=...)`, `list_event_types`. Known types: `state.changed`, `system.time.change`, `system.startup.done`, `alarms.changed`, `resource.changed`, `journal.configuration.changed`, `journal.startup`, `maintenance.labels.bug_report.{collect,generate}.done`. **Schema** (verified from `EventLogProvider` in `2_SystemState`): `events(eventIndex INT PK AUTOINC, source TEXT, eventType TEXT, timestamp INT, message TEXT, payload TEXT='{}')` — `payload` is JSON. `EventLogRow` has typed accessors `event_index`, `source`, `event_type`, `timestamp`, `message`, `payload_json`. RF keywords: `Latest Event Index`, `Events Since`, `Wait For Event` (with `require_payload=True/False`, the RF stand-in for an arbitrary predicate), `List Event Types`, plus `Get Event Log` as an escape hatch (`Call Method` for anything not wrapped, e.g. `.latest(type, limit=N)`).
- **`Configuration`** (`framework/android/configuration.py`) — reads/writes `content://com.parkeon.data.configuration<path>` (path-based key/value tree). API: `get(path)`, `set(path, value)`. Known paths from `artifacts/common.xml`: `/system/debug/mode`, `/system/time/timezone`, `/system/network/modem/*`, `/pknUsbPrinter/printing/speed`, etc. URI format (segment vs query-arg) not yet confirmed — `get()` tries both. RF keywords: `Get Configuration Value`, `Set Configuration Value`.
- **`POSStrings`** (`framework/android/strings.py`) — symbolic-name → UI-text resolver loaded from `artifacts/pos_apk_metadata.json`. The POS app is **Xamarin/Mono** so view-IDs are auto-generated junk; resource names like `Login.button_log_in` are the stable selector key. Tests target UI via `Lookup POS String    Login.button_log_in` → "Log in" then `Tap Text    Log in`. 1,311 strings indexed.
- **`LocalAuditLedger`** (`framework/bos/local_audit.py`) — reads `/sdcard/Android/data/com.flowbird.pos/files/Audit/BOSRecords/<seq>.evt`. **Outbox**: the BOS agent deletes files after successful shipment, so files are ephemeral (sub-second). `expect()` polls at 200 ms. Use this only when an EventLog assertion isn't sufficient. RF keywords (`BOSLibrary`): `List Local Audit Records`, `Newest Local Audit Record`, `Expect Local Audit Record`, `Get Local Audit Ledger`.
- **`load_dataset_parameters`** (`framework/build/dataset_parameters.py`) — loads the canonical `state/params/DM/DatasetParameters.json` from `builds/External-SD/` and returns the 14 string-typed device-behaviour values (`softwareVersion`, `automaticLogOff`, `enableEmv`, etc.). Tests use this as the expected-value source for build-verification assertions. RF keyword: `Get Dataset Parameters` (`BuildDataLibrary`, no device connection needed). The WinCE analogue is `Get ETM DM Parameters` (`WinceLibrary`).

## POS app shape (`com.flowbird.pos`)

Static analysis from `tools/extract_apk_metadata.py` against the POS APK in `pkn_sw.zip`:

- **Xamarin/Mono app** — main activity is `crc648b5ee79715524b27.MainActivity` (the `crc64`-prefixed class name is Xamarin's mangled MD5). Launch with `am start -n com.flowbird.pos/crc648b5ee79715524b27.MainActivity`.
- **23 `com.parkeon.generic.*` services** declared: audit, authentication, backofficeagent, cardcontrol, configuration, events, fareproducts, fares, logger, operatorinformation, pages, persistentobject, platformprint, remotecommand, smartcard, srs, state, topology, transaction, plus device-level identity/location/powermanagement/ui.
- **Receivers we can `am broadcast` to** for tests: `DataRegisterReceiver`, `ShutdownReceiver`, `UsbPaymentDeviceReceiver`, `AdminEnabledReceiver`, `InstallCompleteReceiver`, `MaintenanceProceduresReceiver`, `PowerBroadcastReceiver`.
- **Min SDK 22 / target SDK 33** — modern Android target, framework APIs available.
- Full metadata: `artifacts/pos_apk_metadata.json` (regenerable with `python tools/extract_apk_metadata.py <apk> -o <json>`).
- **Screen catalog**: `docs/screens.md` — 109 application layouts with the `@string` references each one declares. Generated by `tools/generate_screens_doc.py` from `pos_apk_metadata.json` + `pos_apk_layouts.json`. Use this to find which screen contains a given UI element. Note: only ~44 layouts declare strings statically; the rest set text from C#/Xamarin code at runtime, so a missing entry doesn't mean an empty screen.

Audit lifecycle observed: action → EventLog row inserted → `.evt` written to outbox → shipped to BOS → `.evt` deleted. Tests should assert against EventLog (durable) by default; the `.evt` outbox is a fallback for events the EventLog doesn't expose.

Avoid `Expect BOS Audit Event` until the API contract is confirmed — `BOSClient.get_audit_events` raises `NotImplementedError` by design.

## Working with this codebase — which subagent to use

| Task | Subagent |
|---|---|
| Add a new test | `test-author` |
| Investigate a failing test | `test-maintainer` |
| New transport, UI driver, or cross-cutting refactor | `framework-architect` |
| Reconcile `builds/` against device registries | `device-inventory` |
| Design / refine BOS audit assertions for a feature | `bos-auditor` |

Definitions live in `.claude/agents/*.md`.

## Parkeon BSP inventory (from `pkn_sw.zip` static scan)

Aggregated by `tools/scan_apk_providers.py` → `artifacts/bsp_inventory.json`. 26 unique provider authorities across the bundle. Key ones:

| Authority | Class | Owner APK |
|---|---|---|
| `com.parkeon.data.eventLog` | `com.parkeon.systemstate.events.EventLogProvider` | `2_SystemState` |
| `com.parkeon.data.configuration` | `com.parkeon.systemstate.SystemStateContentProvider` | `2_SystemState` |
| `com.parkeon.data.state` | `SystemStateContentProvider` | `2_SystemState` |
| `com.parkeon.data.alarms` | `SystemStateContentProvider` | `2_SystemState` |
| `com.parkeon.data.accounting` | `SystemStateContentProvider` | `2_SystemState` |
| `com.parkeon.data.register` | `SystemStateContentProvider` | `2_SystemState` |
| `com.parkeon.data.environment` | `com.parkeon.data.EnvironmentProvider` | `com.parkeon.platform` |
| `com.parkeon.data.translations` | `TranslationProvider` | `com.parkeon.base` |
| `com.parkeon.data.dallas` | `DallasContentProvider` | `com.parkeon.periphs.dallas` |
| `com.parkeon.security.keystore` | `KeyStoreProvider` | `com.parkeon.base` |
| `com.parkeon.services.commands` | `CommandSchedulerProvider` | `com.parkeon.base` |

`SystemStateContentProvider` is a multi-authority hub — one Java class handles `state`, `alarms`, `accounting`, `register`, `configuration`, plus shared_prefs + files siblings. Treat it as the canonical reference for cross-cutting state assertions.

Architecture (from bytecode of `SystemStateContentProvider` + dex string scan):

- **`events` is the ONLY SQL-backed authority** in SystemState. The rest are key-value stores fronted by `IStorage` backends. Three SharedPreferences XML stores: `content://com.parkeon.systemstate.shared_prefs/{local,sec,volatile}.xml`.
- The provider uses **`NodeDefinition`** objects (in `com.parkeon.systemstate.schema.*`) to resolve URI paths to values. Schema is bootstrapped from `content://com.parkeon.systemstate.files/schema.xml` at runtime, not packaged.
- Reads: `getStorage(authority)` returns the `IStorage` for an authority; `retrieveValue(node, cursor)` and `retrieveValues(node, selection, cursor)` populate the result Cursor.
- Writes: `setValues(ContentValues, selection)`; `delete()`; `insert()`; `deleteNode()`. Logged with `'%s' -> '%s'`.
- The exact URI form for paths (segment-style `content://AUTHORITY/system/foo` vs query-style `content://AUTHORITY/?path=/system/foo`) cannot be resolved purely from static analysis — the relevant strings are in static-final fields stored as dex metadata rather than bytecode. Probe both on first real-device access.

## Translink device defaults — `DatasetParameters.json`

The SD card carries `state/params/DM/DatasetParameters.json` — 14 application-level (not platform-level) device-behaviour config values authored via the Flowbird `api.cloudfare.co.uk/versions/<DisplayVersion>` Atom feed. The current INF212 build values are:

```json
{
  "softwareVersion": "1.3.12.22119",
  "automaticLogOff": "10000",
  "screenSaverTimeout": "300",
  "powerInterrupt": "100",
  "audioLevelDefault": "4",
  "brightnessLevelDefault": "5",
  "maxRevenueWithoutComms": "2000",
  "conversionValue": "0",
  "decimalPrecision": "0",
  "lowPaperLengthMetres": "10",
  "slipsPaperJam": "5",
  "numberDaysAutonomyWithoutFullSynchronisation": "7",
  "merchantReceipt": "true",
  "enableEmv": "false"
}
```

These are *test-relevant assertions*: e.g. "after 10000ms idle, the device must auto-logoff" or "EMV must be disabled in this build". The dual-format XML (`state/params/DM/DatasetParameters.xml`) is the authored source.

## Discovered facts — Translink POS (way6 / INF212)

Pulled from `builds/External-SD/` on 2026-05-07. Treat these as authoritative until contradicted by a fresher device.

- **Hardware:** i.MX53 SoC, 640×480 display, way6.std mainboard (LF10714). Customer code **INF212** per `linux-bsp.dtalias` line 106 — Translink with modem + wifi.
- **OS:** Android (selinux=0) with Flowbird/Parkeon init scripts. Boot chain: U-Boot → Linux kernel → Android `/init`. Build `POS_1_3_12_22119_v2`.
- **App package:** `com.flowbird.pos` (UI). Daemons: `com.parkeon.platform`, `com.parkeon.updater`, `pkn_command_server` (internal RPC socket — irrelevant to tests).
- **BOS endpoint (UK test env 5):** `https://device-uktest-tl-env5.albedo-gen.co.uk`
- **Identity provider:** Keycloak realm `TranslinkDevices` at `https://auth-uktest-tl-env4.albedo-gen.co.uk/auth/realms/TranslinkDevices/`
- **Device identity sent to BOS:** `DeviceId=POS`, `DeviceType=POS_WAY6`, `CommsGroupId=PKN`
- **On-device audit ledger:** `Audit/BOSRecords` (mirrored to `1:Audit/BOSRecords`). The device persists every audit record locally before posting — gives us a **second** assertion path in tests (read the ledger over ADB) when BOS round-trip is slow or down.

The `tools/inspect_device_build.py` tool emits this fingerprint as JSON for any SD root. Run it whenever a new build lands.

## Run reporting (Jira-ready)

Every `robot` invocation with `--listener framework.reporting.robot_listener.RobotReportListener`
(wire this into your run command, e.g. `robot --listener framework.reporting.robot_listener.RobotReportListener ...`)
produces a fresh run directory at `artifacts/runs/<UTC-timestamp>/` containing:

- `index.html` — **self-contained HTML run report**: run date/time, **why it was run** (the
  `RUN_REASON` env var or `--variable RUN_REASON:...`), project, full run command, pass/fail/skip
  counts, a colour-coded results table (failures first, each linking to its `report.md`), and a
  **JIRA-style defect block per failed/errored test** with evidence linked. No external deps, opens
  anywhere. Renderer: `framework/reporting/html.py` (unchanged from the pytest era).
- `index.md` — session summary table (status, test name, duration) sorted by failures-first.
- `defects.json` — every failed test as a JIRA-ready defect (`projectKey`, `issueTypeName=Bug`,
  `summary`, `description` in JIRA wiki markup, `labels`, `priority`, `_evidence_files`). Shaped for
  the Atlassian MCP `createJiraIssue` tool — the "generate file, then offer to push" flow.
  `projectKey` comes from `$JIRA_PROJECT_KEY` (blank if unset, never guessed). Builder:
  `framework/reporting/defect.py` (unchanged).
- `<encoded-testname>/report.md` — per-test Jira-ready writeup: status, duration, repro command,
  environment fingerprint (project, device id/type/os, transport target, build version), traceback /
  skip reason, attached log files, notes.
- `<encoded-testname>/defect.md` — **only for failed tests**: a copy/paste defect raise for the
  manual JIRA workflow.
- `<encoded-testname>/logcat.txt` / `ui_dump.xml` / `screen.png` — pulled by `Collect Device Logs` /
  `Capture UI State On Failure` (`DeviceLibrary`), called from each suite's `Collect Test Artefacts`
  Test Teardown (see `resources/common.resource`).
- `<encoded-testname>/journal.txt` — pulled via `journalctl -n 500 --no-pager` (falls back to
  `dmesg | tail -n 500`) for SSH transports.

RF's own `output.xml`/`report.html`/`log.html` are produced natively alongside this, for whatever
company-wide RF tooling consumes them — the listener doesn't replace those, it adds the Jira-paste
workflow on top.

**Listener** lives at `framework/reporting/robot_listener.py` (`RobotReportListener`, RF Listener v3
— `start_test`/`end_test`/`close`). It sets `${REPORT_DIR}` as a test variable in `start_test` so
`Collect Device Logs`/`Capture UI State On Failure` know where to write, then `end_test` picks up
whatever landed in that directory as report attachments. `TestReport`/`build_defect`/
`render_run_html` themselves (`report.py`/`defect.py`/`html.py`) are unchanged from the pytest era —
only the listener glue is new.

**Per-test logcat isolation:** `Clear Device Logs` (Test Setup, `DeviceLibrary`) runs `logcat -c` at
the start of every test for ADB devices, so each test's `Collect Test Artefacts` teardown
(`logcat -d -t 500`) captures only its own window rather than an overlapping rolling-tail slice.
Best-effort; never fails the test.

Tests that don't add their own notes still get the writeup + log pull automatically via
`Collect Test Artefacts` in `resources/common.resource` — no extra code required per test.

## Onboarding & readiness (the front door)

New to the repo or unsure if the stack is ready? Type **`/start`** in Claude Code (`.claude/commands/
start.md`) — it runs the preflight, surfaces the human-only steps, and routes you to a run. The
3-minute orientation is **`ONBOARDING.md`** (repo root). Two readiness commands:

- **`python -m tools.doctor [--project <name>] [--device]`** — broad preflight: Python/venv/deps,
  `adb` on PATH, `robot` on PATH, Appium CLI + **server reachable**, `devices.yaml` loads,
  **`robot --dryrun` over the project's suites** (resolves every keyword/tag with no device touched
  — replaces the old pytest-collection check), SSH secrets present. `--device` also probes whether
  the ADB window is open now. Grouped READY / CLAUDE-CAN-HANDLE / NEEDS-YOU / CHECK-MANUALLY;
  `--gate` exits non-zero on outstanding human items. ASCII-only output.
- **`python -m tools.adb_ready ...`** (below) — the fast, run-time "is the device reachable *now*?"

## ADB readiness preflight

The device's TCP-5555 listener flips intermittently. Before running the suite, check it's online:

```
python -m tools.adb_ready --project translink           # instant check
python -m tools.adb_ready --project translink --wait 30 # poll for up to 30s
python -m tools.adb_ready 192.168.3.151:5555            # single serial
```

Exit codes: `0` ready, `1` not ready, `2` bad invocation, `3` adb not on PATH. The deeper `tools/first_connect.py` probe is for one-time device fingerprinting — `adb_ready` is the fast pre-run check.

`ADBTransportImpl.wait_until_device(timeout=..., poll_interval=...)` is the underlying primitive — re-issues `adb connect` each poll, returns the final state without raising. `_adb` now converts subprocess timeouts into `CommandResult(exit_code=-1, stderr="timeout...")` so callers don't have to wrap subprocess errors.

## Current status (last updated 2026-07-10)

- **Migrated off pytest onto Robot Framework** (2026-07-10): pytest is no longer a runtime dependency
  at all. `framework/fixtures.py`, the root `conftest.py`, project `conftest.py` files, and
  `framework/reporting/plugin.py` are deleted. All 36 `test_*.py` files became `test_*.robot` files
  in the same directories (67 RF test cases total, 66 with `--exclude destructive`). New Library
  layer: `framework/robot/{device_library,android_library,bos_library,wince_library,build_data_library}.py`.
  New listener: `framework/reporting/robot_listener.py`. See `resources/common.resource` and
  `resources/translink/signon.resource` for the suite-Settings boilerplate and Given/When/Then
  keyword pattern respectively. Full-repo `robot --dryrun` is clean.
- **ADB transport LIVE** — POS at `192.168.3.151:5555` connected over lab router ethernet. Run `python -m tools.adb_ready --project translink --wait 30` before each session; device occasionally needs reconnect after reboot (`adb disconnect; adb connect 192.168.3.151:5555`).
- **Appium 3.5.0 + UiAutomator2 7.6.1** installed (via npm). Server at `http://127.0.0.1:4723`. Required for `AndroidLibrary`'s Appium-backed keywords — set `APPIUM_URL` env var before running.
- **Pydantic model fix (2026-06-22):** `Device.metadata` widened from `dict[str, str]` to `dict[str, Any]` to accommodate nested `keypad_keycodes` dict in `devices.yaml`.
- **operator_id "300051"** (not 300050 as earlier noted), **operator_pin "1234"** — seeded in `devices.yaml` metadata.
- **Live build:** `1.0.572.20749` (INF212 way6 / Android 5.1.1). POS in NIR (Rail) mode — Bus/Ulsterbus FLU not reachable from standard sign-on. Bus FLU tests skip gracefully when 'Bus' button absent.
- **Signon false-pass TODO:** `Successful Signon Emits State Changed` (`test_operator_signon.robot`) — the NTP `state.changed` can satisfy `require_payload=True` without a real sign-on. Tighten once a live signed-on payload is captured (TODO in `resources/translink/signon.resource`).
- **BOS audit endpoint** still raises `NotImplementedError` — deferred; assert via EventLog (durable) until API contract confirmed.
- **Not yet done:** a live device run (not just `--dryrun`) of the migrated suites hasn't happened —
  do that before treating any individual suite as trustworthy, and update `system-test-ops`'s
  `docs/automation-handoff.md` to describe referencing TestRail case ids via an RF tag/
  `[Documentation]` line instead of a pytest marker (no JSON schema change needed).
- Schedulers (cron'd subagents) parked until Jenkins trigger is wired.

## Things to ask before doing

- Adding a new project? Confirm device list + BOS endpoint with George — don't invent.
- Hard-coding a value that varies per device or per project — push it into the registry instead.
- Touching `builds/` — those are real artifacts. Read, don't edit.
- Changing a marker name or registry schema — that's a framework change; use `framework-architect`.
