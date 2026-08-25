# Flow: Translink HHD — Technician-Exclusive Setup (Payment Terminal, Printer Firmware, Home Location, Penalty Fare App)

- Source: `knowledge/flows/translink-hhd-full-transcription-v17.3.7.md`, board "6. Supervisor /
  Technician Functionality" (lines 1481-1727). Transcribed 2026-08-05.
- Project: translink   Device: HHD   Feature: technician-only device setup (Payment Terminal
  configuration, Printer Firmware, Home Location / Back Office transfer, Configure Penalty Fare
  Application)
- Transcription confidence: **high** — verbatim, not summarized.
- **Split note**: part of board "6. Supervisor / Technician Functionality"; these four items are
  reached only from Technician Mode (1.9), never from Supervisor Menu — unlike Versioning/Connect
  Printer/Pair with Payment Device, which the source explicitly delegates to the Supervisor Menu
  flow. See `translink-hhd-supervisor-technician-menus.md` for the Technician Mode entry point.

## Diagram
```mermaid
flowchart TD
  TECHMENU["1.9 Technician Mode (see menus flow-map)"]

  TECHMENU -->|Payment Terminal| PT1["13.1 Payment Terminal - Blank"]
  PT1 -->|user taps 'Terminal ID' field| PT2["13.2 Payment Terminal - Terminal ID Selected"]
  PT2 -->|user inputs ID using numerical pad and taps tick| PT3["13.3 Payment Terminal - Terminal ID Entered"]
  PT3 -->|user inputs Transaction Key and taps off alphanumeric keypad| PT4["13.4 Payment Terminal - Transaction Key Entered"]
  PT4 -->|user taps 'Continue' button| PT5["13.5 Payment Terminal - Details Saved"]
  PT5 -->|green tick or timeout of 2 seconds| BACKTECH["Back to 'Technician Menu'"]

  TECHMENU -->|Apply Printer Firmware| PF1["14 Printer Firmware - Applying"]
  PF1 --> PF2["14.1 Printer Firmware - Applied"]
  PF2 -->|green tick or timeout of 2 seconds| BACKTECH

  TECHMENU -->|Home Location| BO1["15 Transferring Data to Back Office"]
  BO1 --> BOQ{"Is the Back Office available?"}
  BOQ -->|Yes| HOME1["21 Set Home Location"]
  BOQ -->|No| BO2["15.1 Back Office Not Available"]
  BO2 -->|2 second timeout| BACKTECH
  HOME1 -->|user taps a different Home Location| HOME2["21.1 - Setting Home Location"]
  HOME2 -->|New Home Location is set| HOME3["21.2 New Home Location"]
  HOME3 -->|green tick or timeout of 2 seconds| BACKTECH

  TECHMENU -->|Configure Penalty Fare Application| THIRDPARTY["Opens third party app"]
```

## Paths (each = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|---|---|---|---|
| 1 | Technician Mode → Payment Terminal → Blank → Terminal ID field → Terminal ID Selected → input ID+tick → Terminal ID Entered → input Transaction Key → Transaction Key Entered → Continue → Details Saved → back to Technician Menu | technician-setup | — | C4103934 |
| 2 | Technician Mode → Apply Printer Firmware → Printer Firmware - Applying → Printer Firmware - Applied → back to Technician Menu | technician-setup | — | 4105294 |
| 3 | Technician Mode → Home Location → Transferring Data to Back Office → Back Office **available** → Set Home Location → select a different Home Location → Setting Home Location → new location set → New Home Location → back to Technician Menu | technician-setup | — | C4103933 |
| 4 | Technician Mode → Home Location → Transferring Data to Back Office → Back Office **not available** → Back Office Not Available → 2s timeout → back to Technician Menu | technician-setup | @destructive | 4105295 |
| 5 | Technician Mode → Configure Penalty Fare Application → opens third-party app (no further HHD screens captured) | technician-setup | — | 4105296 |

## Screen states (Given/Then anchors)
- **Payment Terminal setup is a fixed 5-step sequence** (Blank → Terminal ID Selected → Terminal ID
  Entered → Transaction Key Entered → Details Saved) with no branching captured in the source; the
  final "Details Saved" screen returns to the Technician Menu on green tick or a 2-second timeout.
- **Printer Firmware apply is a 2-step sequence** (Applying → Applied) with no failure/error branch
  captured in the source.
- **Home Location depends on Back Office availability** — "Is the Back Office available?" gates
  whether the flow proceeds to "Set Home Location" (Yes) or dead-ends at "Back Office Not
  Available" with a 2-second timeout back to the Technician Menu (No).
- **Configure Penalty Fare Application leaves the HHD app** — the only captured behaviour is the
  decision "Opens third party app"; no in-app screens follow it in this board.

## Notes / unknowns
- No error/failure branch is captured for Payment Terminal or Printer Firmware in the raw
  transcription (only the happy path through to "Back to 'Technician Menu'") — TODO: confirm with
  the requirements owner or in Overflow directly whether a failure path exists for either flow
  before treating "success only" as complete coverage.
- "Configure Penalty Fare Application" has no in-app screens beyond the decision "Opens third
  party app" in this board — TODO: confirm whether the third-party app's own screens are
  out-of-scope for this flow-map (likely, since it's a separate application) or whether there is a
  return-to-HHD screen not captured here.
