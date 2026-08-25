# POS Device Facts — Translink INF212 way6

Consolidated device research pulled from this repo's `CLAUDE.md` (project memory) and the static
artefacts it references. Every fact below cites where in the source repo it comes from, so the
`sit` team can go re-verify against a live unit rather than take this on faith.

---

## 1. Hardware, OS, build

- **SoC / board**: i.MX53, 640×480 display, `way6.std` mainboard (LF10714).
- **Customer code**: **INF212** — Translink, per `linux-bsp.dtalias` line 106 (modem + wifi
  variant of the way6 board).
- **OS**: Android (SELinux disabled, `selinux=0`) with Flowbird/Parkeon init scripts layered on top
  of a standard boot chain: U-Boot → Linux kernel → Android `/init`.
- **Build id**: `POS_1_3_12_22119_v2` (SD-card fingerprint, captured 2026-05-07). Live device build
  as of 2026-06-11 was `1.0.572.20749` (package `pos.STE11`), superseding an earlier
  `1.0.571.25500` — versioning schemes across the two sources aren't 1:1 comparable (SD-card
  fingerprint vs. installed APK versionName), both are recorded so neither gets silently dropped.
- **App package**: `com.flowbird.pos` (the operator-facing UI). Daemons alongside it:
  `com.parkeon.platform`, `com.parkeon.updater`, and `pkn_command_server` (an internal RPC socket,
  not itself test-relevant beyond "is it running").
- **App runtime**: **Xamarin/Mono**. Main activity is `crc648b5ee79715524b27.MainActivity` (the
  `crc64` prefix is Xamarin's mangled-MD5 class-naming scheme). Launch via
  `am start -n com.flowbird.pos/crc648b5ee79715524b27.MainActivity`.
- **SDK levels**: Min SDK 22 / target SDK 33 — a modern Android target despite the aged hardware,
  meaning modern Android framework APIs are available to test tooling.
- Because it's Xamarin, **View IDs in the compiled layout are auto-generated junk** — they are not
  a usable UI selector. The stable selector key is the Xamarin resource *string name*
  (e.g. `Login.button_log_in` → "Log in"), resolved through the APK string catalog (§5) and then
  matched against on-screen text.

Source: `CLAUDE.md` §"POS app shape" and §"Discovered facts — Translink POS (way6 / INF212)".

---

## 2. Package, services, providers

### Services (23 total, `com.parkeon.generic.*`)

Declared in the APK manifest: `audit`, `authentication`, `backofficeagent`, `cardcontrol`,
`configuration`, `events`, `fareproducts`, `fares`, `logger`, `operatorinformation`, `pages`,
`persistentobject`, `platformprint`, `remotecommand`, `smartcard`, `srs`, `state`, `topology`,
`transaction`, plus device-level `identity`/`location`/`powermanagement`/`ui` services.

### Broadcast receivers (`am broadcast` targets for test injection)

`DataRegisterReceiver`, `ShutdownReceiver`, `UsbPaymentDeviceReceiver`, `AdminEnabledReceiver`,
`InstallCompleteReceiver`, `MaintenanceProceduresReceiver`, `PowerBroadcastReceiver`.

### Provider authorities (26 unique, aggregated from the `pkn_sw.zip` static scan into
`artifacts/bsp_inventory.json`)

Key ones:

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

`SystemStateContentProvider` is a multi-authority hub: one Java class fronts `state`, `alarms`,
`accounting`, `register`, `configuration`, plus SharedPreferences + files siblings. Treat it as the
canonical reference for any cross-cutting state assertion.

Architecture notes (from bytecode of `SystemStateContentProvider` + dex string scan):

- **`events` is the only SQL-backed authority** in SystemState; everything else is a key-value
  store fronted by an `IStorage` backend. Three SharedPreferences XML stores exist:
  `content://com.parkeon.systemstate.shared_prefs/{local,sec,volatile}.xml`.
- The provider resolves URI paths to values via `NodeDefinition` objects
  (`com.parkeon.systemstate.schema.*`), bootstrapped at runtime from
  `content://com.parkeon.systemstate.files/schema.xml` — **not packaged statically**, so it can't be
  read purely from the APK.
- Reads: `getStorage(authority)` → `IStorage`; `retrieveValue(node, cursor)` /
  `retrieveValues(node, selection, cursor)`. Writes: `setValues(ContentValues, selection)`,
  `delete()`, `insert()`, `deleteNode()`, logged as `'%s' -> '%s'`.
- **Unresolved from static analysis**: whether provider URIs are segment-style
  (`content://AUTHORITY/system/foo`) or query-style (`content://AUTHORITY/?path=/system/foo`) — the
  literal strings live in dex metadata (static-final fields) rather than bytecode. Must be probed
  against a real device.

Source: `CLAUDE.md` §"POS app shape", §"Parkeon BSP inventory". Raw data: `bsp_inventory.json`,
`SystemStateContentProvider.json`, `ConfigurationHelper*.json` (not copied into this package —
large/internal; ask George if needed).

### EventLog — the SQL schema (verified from `EventLogProvider` bytecode)

```
events(
  eventIndex  INTEGER PRIMARY KEY AUTOINCREMENT,
  source      TEXT,
  eventType   TEXT,
  timestamp   INTEGER,
  message     TEXT,
  payload     TEXT DEFAULT '{}'   -- JSON
)
```

Known event types observed/expected: `state.changed`, `system.time.change`,
`system.startup.done`, `alarms.changed`, `resource.changed`, `journal.configuration.changed`,
`journal.startup`, `maintenance.labels.bug_report.{collect,generate}.done`.

Content URI: `content://com.parkeon.data.eventLog/<type>` (queried over ADB `content query`).
`eventIndex` is monotonic and rows persist (no outbox race) — this is the **preferred** assertion
path over the audit ledger below.

Audit lifecycle observed: action → EventLog row inserted → `.evt` file written to outbox → shipped
to BOS → `.evt` deleted. Assert against EventLog (durable) by default; the on-device `.evt` outbox
is a fallback only for events EventLog doesn't expose.

Source: `CLAUDE.md` §"ADB-first testing" (`EventLog` helper description).

---

## 3. DatasetParameters.json — the 14 device-behaviour fields

The SD card carries `state/params/DM/DatasetParameters.json` (dual-format with
`DatasetParameters.xml` as the authored source), authored via the Flowbird
`api.cloudfare.co.uk/versions/<DisplayVersion>` Atom feed. These are **application-level**, not
platform-level, config values — each one is a test-relevant assertion in its own right (e.g. "after
`automaticLogOff` ms idle, the device must auto-sign-off"; "`enableEmv=false` in this build").

Live values captured from the current INF212 build (see also `reference/dataset_parameters_live.json`
for a raw captured sample):

| Field | Value | Test-relevant meaning |
|---|---|---|
| `softwareVersion` | `1.3.12.22119` | Cross-checked against installed APK `versionName` and the `devices.yaml` registry version |
| `automaticLogOff` | `10000` (ms) | Idle timeout before auto sign-off |
| `screenSaverTimeout` | `300` | Idle timeout before screensaver |
| `powerInterrupt` | `100` | — |
| `audioLevelDefault` | `4` | Expected default volume slider position |
| `brightnessLevelDefault` | `5` | Expected default brightness slider position |
| `maxRevenueWithoutComms` | `2000` | Revenue cap while offline from BOS |
| `conversionValue` | `0` | — |
| `decimalPrecision` | `0` | — |
| `lowPaperLengthMetres` | `10` | Expected threshold shown on the paper-status panel |
| `slipsPaperJam` | `5` | — |
| `numberDaysAutonomyWithoutFullSynchronisation` | `7` | — |
| `merchantReceipt` | `true` | — |
| `enableEmv` | `false` | EMV must be disabled on this build |

Source: `CLAUDE.md` §"Translink device defaults — DatasetParameters.json". Raw file:
`reference/dataset_parameters_live.json` (small — a live-captured sample, not the full canonical
JSON, which lives under `builds/External-SD/` in the parent repo and was not copied into this
package).

---

## 4. BOS endpoint and identity provider

- **BOS base URL (UK test env 5)**: `https://device-uktest-tl-env5.albedo-gen.co.uk`
- **Identity provider**: Keycloak realm **`TranslinkDevices`** at
  `https://auth-uktest-tl-env4.albedo-gen.co.uk/auth/realms/TranslinkDevices/`
- **Device identity sent to BOS**: `DeviceId=POS`, `DeviceType=POS_WAY6`, `CommsGroupId=PKN`
- **On-device audit ledger**: `Audit/BOSRecords` (mirrored to `1:Audit/BOSRecords`) — every audit
  record is persisted locally before being posted to BOS, giving a second (ephemeral, outbox-style)
  assertion path over ADB when the BOS round-trip is slow/unavailable. Full path on-device:
  `/sdcard/Android/data/com.flowbird.pos/files/Audit/BOSRecords/<seq>.evt`.
- **BOS audit API is NOT confirmed** — `BOSClient.get_audit_events` in this repo deliberately
  raises `NotImplementedError`. Don't build a `sit` assertion against a live BOS audit-event
  round-trip until that contract is verified; assert via EventLog or the local ledger instead.

Source: `CLAUDE.md` §"Discovered facts — Translink POS (way6 / INF212)", §"ADB-first testing".
`devices.yaml` (`raw-repo-export/projects/translink/devices.yaml`) mirrors these same values in the
device registry entry `translink-pos-inf212-01`.

---

## 5. Screen catalog and APK string catalog

- **Screen catalog**: `docs/screens.md` (copied here as `reference/screens.md`) — **109 application
  layouts**, each listing the `@string` references it declares statically. Generated by
  `tools/generate_screens_doc.py` from `pos_apk_metadata.json` + `pos_apk_layouts.json`. Use it to
  find which screen owns a given UI element.
  - Caveat: only **~44 of the 109 layouts** declare strings statically in the layout XML — the rest
    set their text from C#/Xamarin code at runtime. A layout missing from a string's screen list
    does *not* mean that screen is textless; it means the mapping can't be derived statically.
- **APK string catalog**: `artifacts/pos_apk_metadata.json` (copied here as
  `reference/pos_apk_metadata.json`) — **1,311 strings** indexed by symbolic resource name (e.g.
  `Login.button_log_in` → `"Log in"`). This is the mechanism this repo's `POSStrings` helper uses to
  resolve a stable selector name to the on-screen text to search for, since Xamarin view IDs aren't
  usable directly. Regenerable from a fresh APK via
  `python tools/extract_apk_metadata.py <apk> -o <json>`.

Source: `CLAUDE.md` §"POS app shape" (screens.md bullet), §"ADB-first testing" (`POSStrings`
description).

---

## 6. Physical keypad → Android keycode map

Verified via `getevent` against the physical way6 keypad on 2026-06-12 (recorded in `devices.yaml`
metadata, not independently re-derivable from the APK):

| Key | Android keycode |
|---|---|
| L1–L5 | `131`–`135` (`KEY_F1`–`KEY_F5`) |
| R1–R5 | `136`–`140` (`KEY_F6`–`KEY_F10`) |
| MENU | `142` (`KEY_F12`) — opens the settings/Operator menu |
| UP / DOWN / LEFT / RIGHT | `19` / `20` / `21` / `22` |
| ENTER | `66` |
| ESC | `111` (`KEY_ESC`) |
| CLEAR ("C" key) | `67` (`KEY_BACKSPACE`) — universal back/cancel |
| PLUS / MINUS / STAR | `157` / `156` / `155` |

Source: `raw-repo-export/projects/translink/devices.yaml` (`metadata.keypad_keycodes`).

---

## 7. Operational identity / credentials used in testing

- **Operator id**: `300051`, **operator PIN**: `1234` — seeded in `devices.yaml` metadata, used to
  drive sign-on across nearly every functional test.
- **Live device transport**: ADB over `192.168.3.151:5555` (lab router ethernet); this is
  environment-specific to George's lab and won't carry over to wherever `sit`'s POS unit lives.
- **Observed live mode**: the lab POS is provisioned in **NIR (Rail) mode** — Bus/Ulsterbus FLU
  screens are unreachable from standard sign-on on this specific unit (confirmed by
  `Nir Main Screen Is Rail Only`, which asserts the "Bus" and "Day Tours" buttons are absent). If
  `sit`'s unit is provisioned differently, this assumption needs revisiting.

Source: `CLAUDE.md` §"Current status", `devices.yaml`.
