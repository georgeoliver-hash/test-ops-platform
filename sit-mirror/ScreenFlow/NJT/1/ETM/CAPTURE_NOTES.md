# NJT ETM — device capture notes (ground-truthed from 192.168.3.11)

Captured live from the NJT ETM (Way6s, armv7l/Debian 12) over SSH + CDP. This records
what was gathered and what still needs the device to complete.

## Enabling CDP (prerequisite for UI capture / TSS UI driving)
The NJT Way6s runs its driver console in QtWebEngine via `flb_launcher`, and by default
**remote-debugging is off**. It is enabled per-device the same way the Axio/CWT profiles
do it — in `/opt/pap-sdk-config/devices/way6x.cfg`:

```
setEnvVar("QTWEBENGINE_REMOTE_DEBUGGING", "0.0.0.0:9000")
```

then `systemctl restart pap-sdk-app.service`. CDP then serves on **port 9000** (not 9222).
→ For the SIT deploy, the NJT recipe needs a CDP-enable step (the Way6s analogue of the
Axio `WebengineCmd`), and the TSS adaptor should use **CdpPort 9000**.
(A backup of the original profile is at `way6x.cfg.sitbak` on the device.)

## Screens captured
`translate_screen_data` strips the leading slash (PR #13), so template `Attributes.Name` is
un-slashed. Captured: **ScreenSaver**, **Idle** (see Templates/). Volatile clock/date/day
element text uses **`REGEX:`** patterns — `Comparitors` matches template text literally unless
it starts with `REGEX:`.

## Screenflow build plan (UPDATE 2026-08-11: key/text entry now WORKS — supersedes both
## the original "use JS_Navigate" note AND the uinput-blocked correction below)
**This section is stale as of 2026-07-21 (see below) — kept for history.** The
`/dev/uinput`-blocked CDP key-injection path described here was never fixed; instead a
**JS-injection workaround** was found and is now the proven, validated mechanism (see
`Resources/Devices/ETM/Utility/Platforms/ETMNjtInteractionUtility.robot`, `ETM: Njt: Sign On
Fresh` — validated end-to-end with real creds 9999/1234 on 2026-07-21, still current):
- Buttons/keys → `dispatch key event on device` (a synthetic `window.dispatchEvent(new
  KeyboardEvent(...))`, i.e. a JS-level keydown+keyup, NOT CDP `Input.dispatchKeyEvent`) —
  this reaches the app's real global-keydown-handler input path and does **not** need
  `/dev/uinput` at all.
- Text/number entry → `set device input value` (native `HTMLInputElement` value setter +
  `input`/`change` events, targeted by 0-based index into the page's `input,textarea` list —
  index 0 = staff ID, index 1 = PIN) — synthetic keydowns alone don't type characters, so
  this covers what key-dispatch can't.
- Screen identity → `get device web route` (`location.href`), not the layout-based
  `Attributes.Name`.
Both primitives go over the SAME `/UI/Evaluate` TSS endpoint (CDP `Runtime.evaluate`) that
`/UI/Layout` already uses on the same CDP tab — so no new adaptor/channel was needed, just a
different script.

**Original (now-corrected) analysis, 2026-07-21:** the Way6s driver console is a
**key-driven state machine** (Expo / React-Native-Web + a global keydown handler), *not* a
URL/history-routed app, so `JS_Navigate` (pushState/PopState) doesn't drive it. At the time,
CDP's native `Input.dispatchKeyEvent` path (`UI_Key` → `press_keys()`) was believed permanently
blocked without `/dev/uinput`, and `UI_Click`/`UI_ClickAt` (CDP mouse events) were the only
confirmed-working input. That CDP-key-is-blocked conclusion is now superseded by the
JS-injection workaround above — mouse clicks still work too, but key/text entry no longer
needs them.

**`screenflow_map.jsonc`/`NavigationActions.py` status:** two new action types —
`JS_KeyPress` and `JS_SetInputValue` — were added to `NavigationActions.py` (mirroring
`JS_Navigate`'s `/UI/Evaluate` pattern and calling the exact same scripts as
`dispatch_key_event`/`set_input_value` in `DeviceUI.py`) so a `screenflow_map.jsonc` can now
drive this proven mechanism directly, instead of only the hand-written
`ETMNjtInteractionUtility.robot` keyword layer. `screenflow_map.jsonc` has been extended
through `SignOn`/`TripSetup` using these. Everything from `TripSetup` onward into per-field
screens / FLU / ticket issue is still a logic+HMI-spec-derived DRAFT, not live-verified — see
the `TODO(on-device)` markers in `screenflow_map.jsonc` for exactly what's confirmed vs. drafted.

## Credentials & trip-setup line IDs (source: Slack `team-njt-etm-dev`)
Real working creds for the NJT test back office — now in `DeviceStaff.json` (selected by role):

| Persona | StaffNumber | Pin | Role (Id) |
|---|---|---|---|
| Operator | 9999 | 1234 | Operator_ETM (2) |
| Operator 2 | 1000 | 1000 | Operator_ETM (2) |
| Supervisor | 8888 | 8888 | Supervisor_ETM (5) |
| Admin | 7777 | 7777 | Technician_ETM (12) — *Admin→Technician mapping assumed; confirm* |

No Inspector (7) or 6-digit staff cred supplied yet — those personas are omitted until real
creds exist (a non-authenticating placeholder would only mislead).

**Trip-setup Line IDs (valid on the test estate):** `308, 318, 321, 346, 351`
(any one usable; stored as `LineId` / `LineIdAlternatives` presets in `screenflow_map.jsonc`).

## Encrypted on-device configs (how to read them)
Some `…/gfts/config/*.json` are encrypted (confirmed binary: `authentication.stafflist.json`;
others like `topology.config.json`, `appsettings.json`, `store.json`). Encryption is **.NET
DPAPI `ProtectedData`** — `services/System.Security.Cryptography.ProtectedData.dll` +
`services/libKeyEncryption.so` (arm/arm64 native). **Caveat:** a plaintext JSON file that
starts with a UTF-8 BOM (e.g. `locationservice.parameters.json`, `.homelocations.json`,
`identityservice.config.json`) is *not* encrypted — it just isn't `{`-prefixed; those read fine.

To extract the info, in order of preference:
1. **Don't** — the source of truth is the back office. The stafflist is served plaintext from
   `StaffListUri` (`…/OVRAPI{0}/distribution/staff…`); staff creds come from there (that is
   exactly what the Slack creds are). Populate `DeviceStaff.json` from back-office knowledge,
   not by decrypting the device cache.
2. Most config we care about is **already plaintext** on-device (backofficeagent, authentication.config,
   configurationservice, locationservice.config, logger, farebox, printer, remotecommand) —
   read directly (this is what the deploy recipe downloads + patches).
3. Only if you must read an encrypted file off-device: run a small .NET helper **on the device**
   that calls `ProtectedData.Unprotect` via the shipped dll/`libKeyEncryption.so` (same
   machine/entropy scope). Undocumented and fragile — avoid unless there's no back-office source.

## Home locations / CommsGroups (from driver-console `gfts-field-config.json`)
The device is assigned **IRB (Ironbound)**; the full selectable set is:

| Code | Description | Code | Description |
|------|-------------|------|-------------|
| KRN | Kearney Point | ORD | Oradell |
| IRB | Ironbound | WYN | Wayne |
| BIG | Big Tree | WWD | Westwood |
| HLT | Hilton | EHT | Egg Harbor |
| HOW | Howell | HAM | Hamilton |
| ORG | Orange | NEP | Neptune |
| FAR | Fairview | NWT | Newton Avenue |
| GRN | Greenville | WTP | Washington Twp |
| MRK | Market Street | HCK | Hackensack |
| MED | Meadowlands | NBK | New Brunswick |
| MOR | Morris | SLM | Salem |

## Live endpoints (STE40 / UK Test Env 1) — SIT repoint map
For SIT these all repoint to the BOSEmulator; IdP + RemoteEndpoint blank.

| Config field | Live value | SIT |
|---|---|---|
| `backofficeagentservice.BOSUri` | `https://device-uktest-nj-env1.albedo-gen.co.uk` | → BOSEmulator |
| `authentication.StaffListUri` | `…/OVRAPI{0}/distribution/staff{versionTimestamp}` | → BOS, keep the `OVRAPI{0}…{versionTimestamp}` shape |
| `configurationservice.ManifestUri` | `…/manifest/v1/?deviceType=ETM&deviceId={deviceId}` | → TMS/BOS |
| `locationservice.HomeLocationsListUri` | `…/info/homelocations` | → BOS |
| `remotecommand.BOSConnection` | `…/command/` | → BOS (note: `/command/`, lowercase, trailing slash — the field **does** exist) |
| `backofficeagentservice.IdentityProviderUri` | `https://auth-uktest-nj-env1.albedo-gen.co.uk/auth/realms/NJTransitDevices` | `""` (no Keycloak) |
| `logger.service.RemoteLoggingConfig.RemoteEndpoint` | `https://devicelogmanager-uktest-nj-env1.albedo-gen.co.uk/logging/` | `""` |

## Device facts
- Serial (identityservice.serialnum): `TA-000004`  ·  Operator id: `1`
- Location params (live): HomeLocation `IRB`, MountingPointId `003`, StopId `9400ZZEDAIR`
- Packages: `gfts-config-njt-driverconsole-ste40`, `gfts-database-njt`, `gfts-product-{gfts,features,update}`,
  `platform-sdk-settings-armhf`, `pap-sdk-app`, `njt-driver-console-web-app` — config + DBs ship in
  those packages (installed on-device), **not** loose in the build artifact.
- Fare/Topology SQLite DBs present (`FareProducts.sqlite`, `FaresTopology.sqlite`) — potential test-data source.
