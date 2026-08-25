# POS Test Intent — 26 Tests, by Feature Area

For each of the 26 POS-tagged `.robot` test files in `projects/translink/tests/` (confirmed via
`grep "device_types:POS"` — ETM-only files like `test_etm_*.robot` and
`provisioning/test_etm_dm_parameters.robot` are excluded, they're a different device type). This is
the part that should survive the move to `sit` — re-implement the *intent* described here against
`sit`'s own Bindings/Utility layer, using `raw-repo-export/` only to check exact implementation
detail if needed.

Legend for **Evidence source**: `EventLog` (durable content-provider row), `Local ledger` (ephemeral
`Audit/BOSRecords/*.evt` outbox file), `UI text` (on-screen string match via `POSStrings`/Appium),
`APK/registry version` (installed package versionName vs. `DatasetParameters`/registry), `None (stub)`
(test currently `Skip`s — documents intent without asserting anything yet).

---

## transactions

### `projects/translink/tests/transactions/test_basket_add_and_clear.robot`
**Test**: `Basket Clear Resets Count`. Verifies that clearing the basket removes all items —
concretely, after tapping the Clear Basket button, the per-item "Delete" control (visible while an
item is in the basket) must no longer be on screen. This matters because a basket that doesn't
truly empty on Clear would let a stale item slip through to payment. **Caveat**: the test currently
assumes the device is pre-signed-on and skips actually adding an item first (both are open TODOs in
the pytest-era carryover) — so as written it only proves Clear doesn't error, not that it empties a
populated basket. **Evidence source**: UI text (basket-view label/button visibility).

### `projects/translink/tests/transactions/test_annulment.robot`
Two tests. `Nothing To Annul When No Recent Ticket` verifies that on a fresh device with no prior
transaction, entering the annul-last-ticket flow shows "No Ticket to Annul" rather than a bogus
total — i.e. the negative path is handled distinctly from the happy path. `Annul Confirmation
Screen Shows Total` (intent: after a real transaction, the annul-confirmation screen shows the
transaction's total and time) is currently a stub — `Skip`ped because there's no way yet to seed a
prior transaction into the day's register from a test. **Evidence source**: UI text
(`Annulment.NothingToAnnul` / `AnnulmentConfirmation.Title` + `Annulment.Total`); second test
None (stub).

### `projects/translink/tests/transactions/test_advance_ticket_date.robot`
Two tests. `Advance Ticket Screen Renders` verifies the Advance Ticket date-entry screen shows its
title, date-input label, and "select date of travel" prompt — i.e. the screen loads with all its
static chrome. `Advance Ticket Accepts Future Date` verifies a valid future date typed in
`DD/MM/YY` format is accepted by the input control; this one has an open TODO — it locates the
input by tapping the hint text (Xamarin auto-generates the actual view id) and types the date, but
does **not** yet assert the date was actually accepted post-entry (that assertion is a TODO pending
a way to read the input's resulting `@text`). **Evidence source**: UI text (screen title/labels);
second test is UI-text driven but incomplete on the actual accept-assertion.

### `projects/translink/tests/transactions/test_abt_topup.robot`
Two tests, both currently stubs. `Topup Title Present On Smartcard Menu` (intent: with a smartcard
present, the operator menu offers a "Top Up" option) and `Successful Topup Emits Resource Changed`
(intent: a successful top-up should emit a `resource.changed` EventLog row for the balance update
plus a `state.changed` row for the transaction) both `Skip` because there's no way yet to simulate
smartcard presentation (needs either a hardware card-reader fixture or an injected event into the
`com.parkeon.generic.smartcard` service). **Evidence source (intended)**: UI text for the menu
option; `EventLog` (`resource.changed` + `state.changed`) for the top-up transaction. **Current
state**: None (stub) — no live assertion yet.

### `projects/translink/tests/transactions/test_basket_confirm_payment.robot`
Two tests. `Payment Method Button Present` (templated over Cash/BankCard/Warrant) verifies all
three payment-method buttons render on the basket-confirmation screen — this guards against a
build regression silently dropping a payment option. `Cash Payment Emits Transaction Event`
verifies that tapping Cash produces *some* new EventLog row — the test doesn't yet know the exact
`eventType` a cash transaction uses, so it takes a baseline index on both `state.changed` and
`resource.changed` and asserts at least one of the two advanced past baseline after the tap; this
is intentionally loose pending a live run to pin the real schema. Both tests carry an open TODO to
first navigate through sign-on → add product → confirm before landing on this screen — as written
they assume the harness is already there. **Evidence source**: UI text (button presence);
`EventLog` (`state.changed`/`resource.changed`, loosely).

---

## status

### `projects/translink/tests/status/test_paper_status_panel.robot`
Two tests. `Paper Status Panel Renders Labels` verifies the paper-status screen's five static
labels (ticket roll length, paper percentage remaining, average tickets remaining, paper low
threshold, reverse-paper-feed control) all render — a build-verification check that the printer
health surface hasn't lost a field. `Paper Low Threshold Matches Dataset` is a stub: intent is that
the numeric value shown next to "Paper Low Threshold" on-device matches
`DatasetParameters.lowPaperLengthMetres` (10 in the current build) — skipped because the value sits
in a sibling view set programmatically by Xamarin, and adjacent-value extraction from a
`uiautomator` dump isn't implemented yet. **Evidence source**: UI text (label presence); intended
second-test evidence is UI text + `DatasetParameters.json` cross-check (currently None/stub).

### `projects/translink/tests/status/test_smartcard_status_panel.robot`
**Test**: `Smartcard Status Panel Renders Labels`. Verifies all 11 static field labels on the
smartcard-status panel render (card reference, card type, ESN, PSN, validity start/expiry dates,
days/journeys remaining, last top-up, last usage, and the mini-statement entry point). This is a
label-shape assertion only — it doesn't drive an actual card presentation, just confirms the panel's
expected fields are all present so a future test (once card simulation exists) has somewhere to
read real values from. **Evidence source**: UI text.

### `projects/translink/tests/status/test_other_devices_panel.robot`
**Test**: `Other Devices Panel Renders Column Headers`. Verifies the fleet-visibility panel (shows
sibling devices in the same `CommsGroupId`) renders its "Device" and "Status" column headers. Body
rows are populated at runtime from a BOS query and aren't asserted here — this is purely "the panel
itself loads with its expected structure," a TODO exists to check populated rows once a live device
with a populated fleet is available. **Evidence source**: UI text.

### `projects/translink/tests/status/test_device_status_panel.robot`
Two tests. `Device Status Screen Lists Printer And Card Reader` verifies the peripherals-health
panel shows both the "Printer" and "Card Reader" rows (these map to the
`pknUsbPrinter`/`dallas`/`pknBixolonUsbSerialLcd` peripheral daemons) — i.e. the panel that
operators/support use to see subsystem health hasn't lost either row. `State Changed Rows Have
Source Field` is a schema-integrity check independent of any screen: it pulls the 10 most recent
`state.changed` EventLog rows and asserts every one has a non-empty `source` field shaped like a
dotted Java package name — this guards against a platform regression where the `source` column
silently goes blank, which would break any test that filters/attributes events by source.
**Evidence source**: UI text (panel labels); `EventLog` (schema/column integrity check).

---

## printing

### `projects/translink/tests/printing/test_print_receipt.robot`
Two tests. `Print Receipt Button Appears After Card Payment` (intent: the card-payment success
screen offers a "Print Receipt" action) is a stub — `Skip`ped pending a deterministic way to seed a
completed card transaction. `Low Paper Alarm Surfaces In Eventlog` verifies that when paper runs
low, an `alarms.changed` EventLog row fires and its payload references paper in some form; this is
written as a "sniff test" — it inspects the most recent 20 `alarms.changed` rows for anything
paper-related and only asserts real content if a paper alarm is actually present (it skips
gracefully otherwise, since it can only run meaningfully under a genuinely low-paper condition).
**Evidence source**: UI text (first test, currently stub); `EventLog` (`alarms.changed`) for the
low-paper alarm.

---

## signon

### `projects/translink/tests/signon/test_operator_signon.robot`
Three tests (TestRail refs implicit via the sibling `signon.resource` Given/When/Then keywords).
`Signon Screen Shows Id And Pin Labels` verifies the sign-on screen's static ID and PIN field
labels render before any credentials are entered. `Invalid Signon Shows Failure Dialog` verifies
that signing on with wrong credentials (`0000`/`9999`) surfaces the "Sign On Failed" dialog rather
than silently doing nothing or crashing — **this test is tagged `destructive`**: repeated bad
credentials trip a Fatal Error lockout on the real POS requiring a manual power cycle to clear, so
it's excluded from default runs and must be opted into deliberately. `Successful Signon Emits State
Changed` verifies that a valid sign-on produces a `state.changed` EventLog row. **Known false-pass
risk, carry this forward**: the platform emits a `state.changed` roughly every 30 seconds as a
side-effect of NTP clock sync, which also carries a non-empty payload — so the current
`require_payload=True` check can pass without a genuine sign-on ever happening. Needs tightening
(e.g. to the specific operator/session payload shape) once a real signed-on payload has been
captured on a live device. **Evidence source**: UI text (first two tests); `EventLog`
(`state.changed`, third test — currently under-specified, see caveat).

### `projects/translink/tests/signon/test_operator_signoff.robot`
Two tests (TestRail refs `C4100370`, `C4099929`). `Signoff Returns To Idle Screen` verifies that
after signing off, the device returns to the idle/sign-on screen (checked via any of "Press Any Key
to Continue" / "Present card" / "Sign On" appearing). `Signoff Emits State Changed Event` verifies
sign-off produces a `state.changed` EventLog row within 30 seconds — this one does **not** carry
the same false-pass risk noted above since it explicitly waits for a *new* event past a
just-taken baseline rather than accepting any payload-bearing row. **Evidence source**: UI text
(first test); `EventLog` (`state.changed`, second test).

### `projects/translink/tests/signon/test_automatic_signoff.robot`
**Test**: `Automatic Signoff After Inactivity` (TestRail ref `C4099933`). Verifies the device
auto-signs-off after being idle for the `automaticLogOff` duration configured in
`DatasetParameters.json` (10 seconds on the current build) — reads the real dataset value rather
than hard-coding it, sleeps for that duration plus a 5-second safety margin with zero UI
interaction, then asserts the device is back on the idle/sign-on screen. Skips itself if the
configured timeout is implausibly long (>120s) to avoid a runaway test. This is a direct behavioural
verification of one of the 14 `DatasetParameters` fields, not just a build-verification string
compare. **Evidence source**: UI text, cross-checked against `DatasetParameters.json`.

---

## options

### `projects/translink/tests/options/test_volume_brightness_settings.robot`
Two tests. `Volume Brightness Panel Renders Labels` verifies the four static controls (Volume
title, Brightness title, "+" / "-" step controls) render on the settings panel. `Volume Brightness
Defaults Match Dataset` is a stub: intent is that the current slider positions match
`DatasetParameters.audioLevelDefault` (4) and `.brightnessLevelDefault` (5) on a freshly-booted
device — skipped because the slider's current value isn't set in the static layout XML and hasn't
been located in a live `uiautomator` dump yet. **Evidence source**: UI text (first test); intended
second-test evidence is UI text + `DatasetParameters.json` cross-check (currently None/stub).

### `projects/translink/tests/options/test_operator_options.robot`
Two tests (TestRail refs `C4099937`, `C4099942`). `Cancel Soft Reboot Stays On Options Screen`
verifies that dismissing (ESC, falling back to BACK) the Soft Reboot confirmation dialog leaves the
device on the Operator Options screen **without actually rebooting** — an important negative-path
check since an accidental reboot on cancel would be a serious regression. `Ticket History Screen
Loads` verifies that navigating Operator Options → Ticket History opens a screen with its title and
all three column headers (Product Name, Date and Time, Price). Both tests navigate via the physical
MENU key → "Operator Menu" → "Operator Options", a helper keyword shared between them.
**Evidence source**: UI text (screen navigation state + labels).

### `projects/translink/tests/options/test_operator_break.robot`
Two tests (TestRail refs `C4099939`, `C4099940`). `Enter Break Mode Shows On Break` verifies that
tapping "Operator Break" from the Operator Menu puts the device into break mode, surfaced via
either the "On break" status indicator or the "Break End Sign On" re-authentication prompt.
`Leave Break Mode Returns To Main` verifies that re-entering the same operator credentials from
break mode returns the device to the normal signed-on main screen (checked via any of "Rail FLU" /
"Rail" / "Ulsterbus" / "Basket" / "Operator Menu" reappearing). Together these cover the full
break-mode round trip an operator would use on a real shift. **Evidence source**: UI text.

---

## provisioning

### `projects/translink/tests/provisioning/test_dataset_parameters.robot`
Three tests — the build-verification anchor for the whole `DatasetParameters` config surface.
`Dataset Parameters Has All Expected Keys` is a pure-data sanity check (no device connection
needed) asserting the authored JSON carries all 14 keys the rest of the suite relies on — a guard
against silent build-pipeline schema drift breaking every other test that reads a dataset value.
`Pos Package Version Matches Dataset Software Version` cross-checks the installed
`com.flowbird.pos` versionName against `DatasetParameters.softwareVersion` — the cleanest available
build-verification check since `package_version` is a stable platform API, whereas the other 13
values are runtime-behaviour assertions that belong in their own feature tests (idle timeout,
EMV-disabled build, etc.) rather than being compared as strings here. `Registry Build Version
Matches Dataset Software Version` cross-checks the project's `devices.yaml` registry version
against the same dataset value, guarding against the registry silently drifting out of sync with
what's actually on the device. **Evidence source**: `DatasetParameters.json` (data-only); APK/
registry version (both device-facing tests).

---

## flu (Fare Look-Up)

### `projects/translink/tests/flu/test_rail_flu.robot`
Six tests (TestRail refs `C4099970`, `C4099972`, `C4099974`, `C4099976`, `C4099978`, `C4099979`,
`C4099987`) covering the Rail FLU screen in NIR (rail) mode — the core fare-selection flow for this
customer's live configuration. `Rail Flu Grid Renders All Section Labels` verifies all four section
headers (Ticket Types, Alighting Stations, Boarding Stations, Passenger Types) render on the grid.
`Rail Flu C Key Returns To Main Screen` verifies the physical "C" key (universal back/cancel on the
way6 keypad) returns from the FLU grid to the main menu. `Rail Flu Ticket Types Section Is
Populated` verifies tapping Ticket Types shows at least one dynamically-loaded product (sourced
from BOS/GTFS at runtime) without hard-coding product names, since available products vary by BOS
config — this is effectively a live BOS/GTFS connectivity smoke check disguised as a UI test.
`Rail Flu Passenger Types Section Opens` verifies the passenger-type picker opens and shows its own
heading. `Rail Flu Advance Ticket Screen Opens` verifies tapping Advance Ticket from the grid (via
Ticket Types first if needed) opens the date-entry screen with its title and prompt visible.
`Rail Flu Station Selection Shows Boarding List` verifies tapping Boarding Stations activates a
station-selection context (loaded from BOS/GTFS) without asserting specific station names. **Evidence
source**: UI text throughout; several tests double as informal checks that the BOS/GTFS data feed
behind the FLU grid is actually populating.

### `projects/translink/tests/flu/test_nir_main_screen.robot`
**Test**: `Nir Main Screen Is Rail Only` (TestRail ref `C4099975`). Verifies that after sign-on in
NIR (rail) mode, the main screen does **not** show the "Bus" or "Day Tours" buttons — confirming
mode-based UI gating actually hides the options that don't apply to this customer configuration.
This test is also what establishes (and is relied on by) the fact that the lab POS is in NIR mode,
which is why the sibling Bus FLU tests below skip gracefully rather than fail. **Evidence source**:
UI text (absence check).

### `projects/translink/tests/flu/test_bus_flu.robot`
Three tests (TestRail refs `C4100374`, `C4100375`, `C4100376`, `C4100377`, `C4100378`) documenting
the Ulsterbus/Metro-mode FLU flow, which is **not reachable on the current lab device** (it's
provisioned NIR/Rail-only) — every test here calls a shared `Try Open Bus FLU` helper that returns
`False` (rather than failing) when the Bus/Ulsterbus button is absent, and the test then
`Skip`s with an explanation. `Bus Flu Route Entry Screen Opens` documents that the Bus button should
open a numeric route-entry screen showing "Enter Route". `Bus Flu Star Key Cycles Boarding Stage`
documents that the "*" key should cycle a boarding-stage/fare-type override on that screen.
`Bus Flu Misc Opens Miscellaneous Products` is the one test in this file that **can** run regardless
of mode (Misc is available across modes) — it verifies tapping "Misc" from the main menu opens the
Miscellaneous Products screen. **Evidence source**: UI text; two of three tests are currently
None (stub, mode-gated) on this specific unit, one (Misc) runs live.

---

## pos (smoke)

### `projects/translink/tests/pos/test_pos_app_installed.robot`
**Test**: `Flowbird Pos App Installed`. Verifies `com.flowbird.pos` is installed at all, and that
its versionName contains the build version pinned in the device registry — a basic smoke/build
gate that should run before anything else, since every other functional test assumes the app is
present and at roughly the expected build. **Evidence source**: APK/registry version.

### `projects/translink/tests/pos/test_pkn_daemon_running.robot`
**Test**: `Pkn Command Server Running`. Verifies the `pkn_command_server` daemon process is running
— without it the on-device internal RPC channel is dead, which would silently break functionality
that depends on it even though the main UI app might still appear to work. Another basic
smoke/health gate. **Evidence source**: process-running check (`Is Process Running`, not
UI/EventLog).

---

## display

### `projects/translink/tests/display/test_clock.robot`
**Test**: `Clock Displays 24 Hour Time` (TestRail ref `C4100373`). Verifies the on-screen clock
renders in 24-hour `HH:MM` format (regex-matched against all visible text) rather than 12-hour
with AM/PM — a locale/format-correctness check relevant to the UK deployment. **Evidence source**:
UI text (regex pattern match).

---

## audit

### `projects/translink/tests/audit/test_eventlog_state_changes.robot`
Two tests. `Eventlog Has Recent State Changes` verifies the `EventLog` content provider is
reachable and returns rows for `state.changed` that carry a populated `eventIndex` — a basic
provider-health check underlying every other EventLog-based assertion in the suite. `Eventlog
Indices Are Monotonic` verifies that rows returned sorted by `eventIndex DESC` actually come back in
strictly descending order — protects every test that takes a "baseline index, then wait for
something past it" pattern (used throughout signon/transactions) from silently breaking if the
provider's sort order ever regresses. **Evidence source**: `EventLog`.

### `projects/translink/tests/audit/test_eventlog_baseline.robot`
**Test**: `State Changed Arrives Within 60s`. Verifies the platform emits at least one
`state.changed` event per minute under normal idle conditions (attributed to NTP/network-watchdog
side effects) — if no new event shows up within 60 seconds, something is wrong with the platform's
event pipeline generally (not specific to any one feature). This is effectively a platform
heartbeat/liveness check, useful as an early-warning canary before trusting any other EventLog
assertion in a run. **Evidence source**: `EventLog` (`state.changed`).

### `projects/translink/tests/audit/test_audit_ledger_present.robot`
Two tests. `Audit Ledger Path Resolves` verifies the on-device `Audit/BOSRecords` ledger path
resolves to a real filesystem path after discovery — a basic reachability check for the ledger
mechanism itself. `Newest Audit Record Is Parseable` verifies that if any `.evt` records are
currently present in the ledger, the newest one parses successfully and carries a `_filename` key —
guards against a change to the on-device audit-record format silently breaking every test that
falls back to the local ledger when EventLog isn't sufficient. Because the ledger is an ephemeral
outbox (records get deleted once shipped to BOS), this test skips gracefully when the ledger is
empty rather than failing. **Evidence source**: Local ledger (`Audit/BOSRecords/*.evt`).
