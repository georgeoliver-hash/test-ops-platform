# ETM automation backlog

Ranked backlog of Translink **ETM** (WinCE, `translink-etm-inf211-01`) automation candidates,
mapped case-by-case to the device-side surface each one asserts. Source cases live in the
`system-test-ops` repo (TestRail suite **30254**, `proposals/etm-suite-restructure/*.cases.yaml`);
the UX screens + design notes are in `system-test-ops/knowledge/flows/etm/`.

## The constraint that shapes everything

The ETM is **headless and SFTP-only — no shell, no automatable UI**. We cannot *drive* it. So every
ETM test is the **verification half** of a case: a human (or a BOS-side push) performs the `WHEN`,
and automation asserts the `THEN` against device-side file/event state. This is exactly what the
framework exists to do — confirm device behaviour and recorded state agree.

## Assertion surfaces (what we can read over SFTP)

| Surface | Path (V6 slot) | Used for |
|---|---|---|
| Event log | `…\SRSService\Data\DeviceEvents.json` | most behavioural side-effects (see codes below) |
| Event catalogue | `…\SRSService\Configuration\EventsConfig.json` | the set of emittable codes |
| Device config | `GFTS\State\Params\DM\DMParameters.json` | config/software/fare-mode changes (22 values) |
| Session state | `GFTS\State\CurrentState.json` | idle vs in-session (`{"State":"Idle"}`) |
| Audit outbox | `GFTS\BOSRecords\` | audit records pending shipment (ephemeral — shipped+deleted) |

**Event codes confirmed from the cached V6 snapshot** (`DeviceEvents.json`, components & sample
codes): `TicketPrinter` (102 "Print started", 110 "Printer OK", 111 "Printer Offline"),
`Power Management` (1307 "Power loss"), `SmartcardService` (40041, 40042), `TransactionService`
(40125), `NETWORK` (812), `Device` (901 "Device Suspending", 921), `Device Manager` (503).
Codes for sign-on / sign-off / annul are **not yet observed** — the Tier-A capture session below
records them live (the snapshot only carried 11 historical rows).

> Baseline rule: `Id` is an event-**type** code, not a row index, so a "new" event is one whose
> `EventDate` is newer than everything already present. All tests baseline on `EventDate`.

## Tier A — automate now (operator triggers at the device; we assert the event)

| # | TestRail case | Assertion | Confidence | Test |
|---|---|---|---|---|
| 1 | Ticket Issue — issue a single ticket | new `TicketPrinter` (102/110) + `TransactionService` (40125) since baseline | High | `test_etm_ticket_issue_audit.py` (built) |
| 2 | Driver Sign Off | `CurrentState.json`→`Idle` + new sign-off audit event | Med | capture stub |
| 3 | Ticket Issue — annul last ticket | new `TransactionService` annul event + annulment-receipt print | Med | capture stub |
| 4 | Smoke — smartcard validates on tap | new `SmartcardService` (40041/40042) | Med | capture stub |
| 5 | Driver Sign On — Manual, first use | state leaves `Idle` + start-of-shift audit event | Med | capture stub |
| 6 | Smoke — ABT contactless tap | new `SmartcardService` / open-payment (50001) | Med-low | capture stub |

Capture stubs live in `projects/translink/tests/smoke/test_etm_live_event_capture.py` — runnable,
opt-in via `ETM_LIVE_ACTION=1`. Each run dumps **all** new events since baseline, so the session
hardens every predicate from "a new event of component X" to the exact `(Id, component, message)`.

## Tier B — clean & deterministic, but the trigger is BOS-side

| # | TestRail case | Assertion | Note |
|---|---|---|---|
| 7 | Download configuration files | diff `DMParameters.json` before/after | cleanest diff test; needs a CloudFare config push |
| 8 | Software distribution & fare-mode transition | `softwareVersion`/fare-mode flips at activation | needs a distribution |
| 9 | Upload audit files / Force comms | `BOSRecords/` drains to empty + `NETWORK` (812) | outbox is ephemeral — poll tight |

## Tier C — observable but destructive or slow (later)

- **Power interruption — minor vs major** → `Power Management` (1307); needs a real power pull → `@destructive`.
- **Auto sign-off** → like sign-off, but wait out the configured timeout.
- **Comms lock after configured period** → state + `NETWORK` events; needs hours of no-comms.

## Tier D — NOT automatable on this device (stays manual)

The ~280 **HMI screen-validation** cases, PIN masking with `*`, error-bar-for-2-seconds,
basket-tracker-visible, etc. — pure visual checks with no file side-effect and no readable UI. (On
the POS these would automate via `ui_dump`; on the headless ETM they do not.)

## Suggested first capture session (~15 min at the device)

1. **#1 ticket issue** (built) — confirms the loop end-to-end.
2. **#5 sign-on** then **#2 sign-off** — one signed session captures both + the audit/session codes.
3. **#3 annul** — issue then annul to capture the annul event.
4. **#4 smartcard tap** — capture the `SmartcardService` validation code.

After the session: tighten each capture test's predicate to the observed code, move it out of the
opt-in gate, and (where useful) promote the precise event into `framework/wince/events.py` constants.
