# Flow: Translink POS — Operator Menu: Options (everything except Annulment)

- Source: `knowledge/flows/translink-pos-full-transcription-v4.0.3.md`, board "10. 9.0 Operator" —
  everything except Annulment. Transcribed/structured 2026-08-05. Raw transcription itself was via
  the Claude Chrome extension, 2026-08-04, from Overflow (v4.0.3).
- Project: translink   Device: POS   Feature: operator menu (sign off, break mode, totals, operator
  information/device management, excess tickets)
- Split note: see `translink-pos-operator-annulment.md` for the annulment sub-flow (Annul Rail/Misc
  Tickets, Annul Previous Ticket bus/rail, Card Top-Up/Card Issue annulment) — split out from this
  file the same way ETM's Driver Menu board was split into `-options` and `-annulment`.
- Transcription confidence: **high** for screens/connections present in the source; **medium** on a
  few decision nodes whose Overflow export gave a raw UUID instead of readable text (see Notes).

## Diagram
```mermaid
flowchart TD
  MAINSCR["Main Screen / FLU (Bus, Rail, Ulsterbus)"]
  MAINSCR -->|press 'Wayfarer' button| MENU[9.0 Operator Menu]

  MENU -->|Sign Off| SIGNOFF[9.1.3 Operator Menu/SignOff]
  MENU -->|Break Mode| BREAKMODE[9.1.5 Operator Menu/BreakMode]
  MENU -->|Totals| TOTALS[9.1.2 Operator Menu/Totals]
  MENU -->|Operator Options / Operator Information| OPINFO[9.1.6 Operator Menu/Operator Information]
  MENU -->|Excess Tickets| EXCESS[9.1.8 Operator Menu - Excess Tickets]

  SIGNOFF -->|Cancel| SIGNOFFCANCELQ{Operator can go back to Operator Menu pressing Cancel.}
  SIGNOFFCANCELQ --> MENU
  SIGNOFF --> PRINTQ{Is the device able to print waybill?}
  PRINTQ -->|Yes| IDLE[1.0 Idle Screen]
  PRINTQ -->|No| SOPRINTERR[9.4.2 Operator Menu/SignOff Printer Error]
  SOPRINTERR --> IDLE

  BREAKMODE -->|Cancel| BREAKCANCELQ{Operator can go back to Operator Menu pressing Cancel.}
  BREAKCANCELQ --> MENU
  BREAKMODE --> DRIVERBREAK[9.2.3 Idle Screen - Driver on Break]
  DRIVERBREAK -->|"on break for configured amount of time" (unlabeled decision node)| BREAKTIMEOUT{"?"}
  BREAKTIMEOUT --> DRIVERBREAK
  DRIVERBREAK -->|sign back in| PINENTRY[1.1.3 Sign On - PIN Entry]
  PINENTRY -->|operator enters PIN| PINENTRY4[1.1.4 Sign On - PIN Entry - 4*]
  PINENTRY4 --> PLEASEWAIT[1.2.2 Please Wait...]
  PLEASEWAIT --> SIGNOKQ{Sign On Succesful?}
  SIGNOKQ -->|No, wrong ID/PIN| SIGNERR[1.3.1 Sign On - Incorrect Details]
  SIGNERR -->|3s timeout or Enter| PINENTRY
  SIGNOKQ -->|Yes| MAINSELECTED[2.2 Main Screen-Rail selected]

  OPINFO -->|Back| OPINFOBACKQ{Operator can go back to Operator Menu pressing Back.}
  OPINFOBACKQ --> MENU
  OPINFO --> CONSOLE[9.3.1 Operator Menu/ConsoleSettings]
  OPINFO --> WCDQ{Are Word and Colour of the Day available?}
  WCDQ -->|Yes| WCD[9.4.4 Operator - Word and Colour of the Day]
  WCDQ -->|No| WCDU[9.5.2 Word and Colour of the Day - Unavailable]
  OPINFO --> MOTDQ{Is Message of the Day available?}
  MOTDQ -->|Yes| MOTD[9.2.4 Operator - Message of the Day]
  MOTDQ -->|No| MOTDU[9.4.3 Message of the Day - Unavailable]
  OPINFO --> SOFTREBOOTC[11.1.2 Soft Reboot - Confirm]
  SOFTREBOOTC --> SOFTREBOOTW[11.1.2 Soft Reboot - Please Wait...]
  SOFTREBOOTW --> DRIVERBREAK
  SOFTREBOOTC --> OPINFO
  OPINFO --> TICKHIST[9.4.5 Operator Menu/Operator Options/Ticket History]
  TICKHIST --> TICKET[9.5.3 Operator Menu/Operator Options/Ticket History/Ticket]
  TICKET --> TICKHIST
  TICKHIST -->|Back| OPINFO
  OPINFO --> PAPERSTATUS[11.2.5 Technician/PaperStatus]
  OPINFO --> FAULTYQ{Device already reported as faulty?}
  FAULTYQ -->|No| REPORTFAULTY[9.6 Operator Menu/Report Faulty Device]
  FAULTYQ -->|Yes| ALREADYFAULTY[9.6.3 Faulty Device Already Reported]
  ALREADYFAULTY -->|go back to Operator Menu, icon already shown| FAULTYINFO[9.6.1 Operator Menu/Operator Information - Faulty Device]
  REPORTFAULTY -->|press Confirm| FAULTYINFO
  FAULTYINFO -->|navigate back to Main Screen| ULSTERFAULTY[9.6.2 Main Screen-Ulsterbus selected - Faulty Device]

  EXCESS --> EXCESSENTER[9.2.7 Operator Menu - Exccess Tickets- Enter Value]
  EXCESSENTER -->|Cancel| EXCESS
  EXCESSENTER -->|operator enters value| EXCESSVAL[9.2.8 Operator Menu - Exccess Tickets- Value Entered]
  EXCESSVAL -->|operator enters invalid value| EXCESSEXCEEDED[9.4.6 Operator Menu - Exccess Tickets- Value Exceeded]
  EXCESSVAL --> EXCESSISSUE["POS issues ticket and operator will return to Operator Menu"]
  EXCESSISSUE --> MENU
```

## Paths (each = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|---|---|---|---|
| 1 | Operator Menu → Sign Off → confirm → waybill prints → Idle Screen | operator-menu | @destructive | C4099929 |
| 2 | Operator Menu → Sign Off → confirm → **printer error** → SignOff Printer Error → Idle Screen | operator-menu | @destructive | 4105119 |
| 3 | Operator Menu → Sign Off → Cancel → back to Operator Menu | operator-menu | — | 4105120 |
| 4 | Operator Menu → Break Mode → confirm → Driver on Break → sign back in (PIN entry) → success → Main Screen | operator-menu | @destructive | FRAGMENTED — see consolidation-audit.md |
| 5 | Driver on Break → sign back in with wrong ID/PIN → Incorrect Details → retry | operator-menu | @destructive | C4099921 |
| 6 | Operator Menu → Break Mode → Cancel → back to Operator Menu | operator-menu | — | 4105121 |
| 7 | Driver on Break for the configured amount of time → some further state change (decision node text not captured in export) | operator-menu | @destructive | 4105122 |
| 8 | Operator Menu → Totals → list displayed, available for printing | operator-menu | — | C4099945 |
| 9 | Operator Menu → Operator Information → Console Settings | operator-menu | — | 4105123 |
| 10 | Operator Information → Word and Colour of the Day **available** → shown | operator-menu | — | 4105124 |
| 11 | Operator Information → Word and Colour of the Day **unavailable** → Unavailable screen | operator-menu | @destructive | 4105125 |
| 12 | Operator Information → Message of the Day **available** → shown | operator-menu | — | 4105126 |
| 13 | Operator Information → Message of the Day **unavailable** → Unavailable screen | operator-menu | @destructive | 4105127 |
| 14 | Operator Information → Soft Reboot → confirm → Please Wait → lands on **Driver on Break** | operator-menu | @destructive | C4099956 |
| 15 | Operator Information → Ticket History → select ticket → Ticket detail → Back → Ticket History | operator-menu | — | C4099942 |
| 16 | Ticket History → Back → Operator Information | operator-menu | — | 4105128 |
| 17 | Operator Information → Paper Status | operator-menu | — | C4099959, C4100384 |
| 18 | Operator Information → Report Faulty Device, **not previously reported** → confirm → Faulty Device info screen → navigate to Main Screen shows Faulty Device icon | operator-menu | @destructive | 4105129 |
| 19 | Operator Information → Report Faulty Device, **already reported** → "Already Reported" → back to Faulty Device info | operator-menu | @destructive | 4105130 |
| 20 | Operator Information → Back → Operator Menu | operator-menu | — | 4105131 |
| 21 | Operator Menu → Excess Tickets → Enter Value → valid value → ticket issued → back to Operator Menu | operator-menu | — | C4099946 |
| 22 | Operator Menu → Excess Tickets → Enter Value → invalid/over-limit value → Value Exceeded error | operator-menu | @destructive | 4105132 |
| 23 | Operator Menu → Excess Tickets → Enter Value → Cancel → back to Excess Tickets | operator-menu | — | 4105133 |

## Screen states (Given/Then anchors)
- **Sign Off print behaviour**: "POS will print a waybill if confirmed. Shift and day totals will
  appear on the waybill." — mirrors the same "was printing successful?" pattern used elsewhere in
  the suite (see ETM Supervisor Menu equivalent).
- **Break Mode confirmation required**: "Pressing 'Break Mode' will show user another screen that
  will require confirmation, before actually going into break mode." Same pattern for Sign Off:
  "Pressing 'Sign Off' will show user another screen that will require confirmation, before actually
  signing off."
- **Driver on Break re-entry reuses the Sign On flow** (PIN Entry → Please Wait → Sign On
  Succesful? decision) — the same screens as board "1.0 Sign On"; this file only shows the
  connection point, not the full Sign On board detail.
- **Excess Ticket child flow**: annotation states "The child flow will be the same as the Adult
  Excess Ticket flow" — i.e. no separate child-specific diagram exists in this board.
- **Faulty device reporting**: per annotation, "Reporting a faulty device means the Payment Device
  will no longer be available to use. An event will be sent to CloudFare to notify back end users of
  a Faulty Device." (spelling "CloudFare" is verbatim from the source annotation — not corrected.)
  "If there is a faulty device, the Faulty Device icon is shown in the header."
- **Operator Information submenu items** (Console Settings, Word/Colour of the Day, Message of the
  Day, Soft Reboot, Ticket History, Paper Status, Report Faulty Device) all hang off "9.1.6 Operator
  Menu/Operator Information" and each returns to it (or to Operator Menu directly) via Back/Cancel.
- A **Metro-specific variant** of the Operator Menu exists — "9.0 Operator Menu/Metro" (annotation:
  "Example of Metro POS Operator Menu.") and "9.1.6.1 Operator Menu/Operator Information/Metro" — but
  no explicit connection lines into/out of either were captured in the source transcription.

## Notes / unknowns
- TODO: confirm the exact behaviour/label of the decision node following "9.2.3 Idle Screen - Driver
  on Break" for the break-timeout condition — the Overflow export yielded a raw UUID node id
  (`7fb3f170-c492-4fce-a357-26dd28167e9d` → `9.2.3 Idle Screen - Driver on Break`, and a second UUID
  `ac96d55d-fb06-40ce-abe1-104d8446f9ba` → `9.2.3 Idle Screen - Driver on Break`) rather than a
  readable decision label. Two annotations exist nearby that may or may not both apply here: "If on
  break for a configured amount of time, the user will be signed out" and "If on break for a
  configured amount of time, the POS will be put in suspend mode" — unclear which (or both, for
  different conditions) governs this transition; do not assume either without confirming live.
- TODO: confirm how the Metro-mode variants of the Operator Menu ("9.0 Operator Menu/Metro") and
  Operator Information ("9.1.6.1 Operator Menu/Operator Information/Metro") differ in behaviour from
  the standard screens — the source only supplies the screen names/example annotations, no
  connections.
- "9.3.1 Operator Menu/ConsoleSettings" has no further child screens/connections captured within this
  board — TODO: confirm whether Console Settings' own sub-flow is detailed elsewhere (e.g. under
  Technician/Administrator boards) or is out of scope here.
- "11.2.5 Technician/PaperStatus" and "11.1.2 Soft Reboot - Confirm/Please Wait..." are shared screens
  also reachable from the Technician board (per their `11.x` numbering) — this board only shows the
  Operator-menu entry point into them, not their full detail.
- GAP: no screen/annotation in this board states what happens if Sign Off is attempted while there
  are un-annulled/unresolved transactions, or interacts with the annulment flows in
  `translink-pos-operator-annulment.md` — not something to guess at.
