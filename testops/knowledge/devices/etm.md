# Device: ETM (Electronic Ticket Machine)

Facts a `gherkin-author` may rely on when drafting ETM cases, so drafts are grounded rather than
invented. Seeded from the old `AA-ETM-Acceptance Test` suite (4943) recon + the `automation-tests`
Translink ETM area. **Audit-first:** confirm shared-vs-mode behaviour from evidence, never guess.

## What it is

- **Driver-operated, onboard bus Electronic Ticket Machine.** Translink variant: **INF211, Windows
  CE (WinCE)** — not Android. Mounted on the bus; the driver signs on at the start of a shift.
- Comms with the back office is via **CloudFare** (same naming as POS). Activity/shift/defect data
  is audited up to CloudFare.
- Transport for automation is **SFTP-only, no shell** — asserts run against SD-card JSON state
  (`DeviceEvents.json`, GTFS State files). See `automation-tests` `framework/wince/`. (Relevant to
  *how* we automate, not to the manual Gherkin behaviour.)

## Actors (maps to `custom_actors` / `@feature` framing)

- **Driver** (primary), **Supervisor**, **Technician**. (No "Operator" — that's the POS term.)

## Feature areas (use as `@feature` tags)

`auth` (driver/supervisor/technician sign on/off), `flu` (fare look-up), `ticket-issue` (paper
tickets), `smartcards` (smartcard + ABT tap), `driver-menu` (options/annulments/totals/messages),
`supervisor`, `technician`, `barcodes`, `paper` (paper/printer management), `power` (power
interrupt / saving), `revenue-limit`, `location` (GPS / manual stage), `hmi` (screen validation),
`system` (BOS comms / time change / commissioning).

## Operating modes

- ETM serves **Metro** and **Ulsterbus** products (Glider transfers also appear). Unlike POS there is
  **no NIR/rail mode on the ETM** — it's a bus device. Most behaviour is shared; mode-specific
  divergence shows up in **smartcard products** (Metro City/Inner/Extended Zone Multi-Journey vs
  Ulsterbus Multi-Journey / Town Service Travelcard) and **ticket products**. **Confirm the exact
  shared-vs-mode split from the old-suite product×mode audit before authoring — do not assume.**

## Known behaviours to write against (grounded in old suite C1519256 + section tree)

- **Driver sign-on (manual, first use)** is a long flow:
  `Enter → Staff ID (4–6 digits) → PIN (masked with '*') → authenticate against authorised-user list
  → First-Use Safety Check → Any Defects → Duty number → Route variant → Journey number → Route
  Summary → Message of the Day → Word & Colours of the Day → FLU screen.` Start of shift is audited;
  staff activity, shift details and defect record are identifiable in CloudFare.
- Sign-on variants in the old suite: Manual First Use / Subsequent Use (with & without Safety Check) /
  with Defects / "Not Communicating With CloudFare". Supervisor and Technician have their own sign-on.
- **Smartcards & ABT:** contactless tap (Visa / Mastercard / Mobile Wallet), declined taps, hotlisted
  cards, concessionary passes (EA Smartpass Bus/Rail Pupil & Further Education, Free Smartpass, Half
  Fare Smartpass, Staff Pass), commercial products (Daylink, Belfast Visitor Pass, Multi-Journey,
  Travelcard, iLink zones 1–4 + NW, aLink, yLink), and **inter-device** multi-journey usage.
- **Barcodes:** single-use online/offline, multiple-use, mLink, legacy, printing, reference entry.
- **Power interrupt** and **paper/printer management** are first-class areas (printer interrupts
  during ticket issue, firmware update, paper status).
- **Revenue Limit** — a cash/revenue ceiling behaviour George called out as an Overflow flow
  (confirm the exact rule from flow annotations once the flow-data JSON arrives).

## Audit / BOS

- Device-side activity audits up through **CloudFare**. Only assert audit outcomes you can name from
  the old-suite wording or flow annotations — do not invent event names.

## TestRail push defaults (confirmed from live sample case C1519256)

```yaml
defaults:
  template_id: 1
  custom_autoconfirmation: false
  custom_devtypes: [25]      # 25 == ETM in this instance (POS is [5]); the option-list ordinals
                             # are display-only — trust the value mirrored from a real ETM case.
  custom_revstatus: 2        # In Review
```
The fields `discover-fields` marks REQUIRED (`custom_qualproc`, `custom_bdcreqdocs`,
`custom_automation_script`) are **`None` on real accepted ETM cases**, so they are not enforced for
this template — do not set them.

## House format (old suite already close to our standard)

`**Given** / **AND**` preconditions, `**WHEN** / **THEN** / **AND**` steps, `custom_preface` = a
"To confirm …" objective sentence, `custom_expected` = a short outcome. This maps onto
`docs/gherkin-standard.md` with minimal rewording.

## Terminology to keep consistent

"sign on" / "sign off", "Driver", "Supervisor", "Technician", "duty number", "route variant",
"Message of the Day", "Word & Colours of the Day", "FLU", "CloudFare". Match on-screen strings
exactly when asserting labels.

## Source of truth

- Old suite **`AA-ETM-Acceptance Test`** (id 4943, read-only) — behaviour gospel.
- `C:\Users\GeorgeOliver\dev\automation-tests\` `framework/wince/` + `projects/translink/tests/` for
  the automated ETM tests (DeviceEvents.json / DMParameters reality).
