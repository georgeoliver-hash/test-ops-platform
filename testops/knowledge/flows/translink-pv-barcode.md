# Flow: Translink PV — Platform Validator-Barcode

- Source: Overflow project "Translink Validators 3.1.7" (https://overflow.io/s/9LR2K30N/), board
  "4. Platform Validator-Barcode". Transcribed verbatim via the Claude Chrome extension, board text
  captured 2026-08-05. Raw source:
  `knowledge/flows/translink-validators-gv-pv-bv-full-transcription-v3.1.7.md`.
- Project: translink   Device: PV   Feature: card/barcode present-and-validate flow (boot,
  commissioning, device faults, ABT EMV, legacy smartcard, operator/technician card, barcode)
- Transcription confidence: **high** — verbatim, not summarized. Two ambiguities in the raw
  connections are flagged below rather than resolved by guessing.
- **Board note**: despite the board title "Platform Validator-Barcode", this board's screens/
  decisions cover the PV's full card-or-barcode presentment path — device power-on/commissioning,
  device-fault handling, ABT EMV smartcard, legacy smartcard (including operator/technician card),
  and barcode validation all share this one board and one entry screen ("1.0.1 Present SmartCard or
  Barcode"), so it is kept as a single flow-map file per the source board boundary (same precedent as
  the ETM Supervisor Menu file bundling several sub-areas under one menu).
- Per the board's own annotation: "The following flow for the Platform Validator differs from the
  Gate Validator flow in that Passback validations are not considered a Failure response."

## Diagram
```mermaid
flowchart TD
  POWERON{Device is powered on}
  LOADING[0.0 Loading]
  COMMISSIONED{Is device commissioned and fully operational?}
  PLINTHCOMM{Is Validator/Plinth Commissioned?}
  NOTINSERVICE[1.2.1 Machine Not in Service]
  PRESENT[1.0.1 Present SmartCard or Barcode]
  FAULTOCCURRED{A device fault has occurred}
  NOTICKETS[1.1.0 Present SmartCard no Tickets]
  NOSMARTCARD[1.1.1 Present Ticket no SmartCard]
  REBOOTATTEMPT{Device reboots in an attempt to recover the reader}
  FAULTFIXED{Fault is corrected}

  POWERON --> LOADING
  LOADING --> COMMISSIONED
  COMMISSIONED -->|Yes| PRESENT
  COMMISSIONED -->|No| PLINTHCOMM
  PLINTHCOMM -->|No| NOTINSERVICE
  PLINTHCOMM -->|Yes| NOTINSERVICE

  PRESENT --> FAULTOCCURRED
  FAULTOCCURRED -->|Barcode Reader has become unavailable| NOTICKETS
  FAULTOCCURRED -->|Smartcard Reader has become unavailable| NOSMARTCARD
  FAULTOCCURRED -->|Both readers become unavailable, or other non-powerloss fault| NOTINSERVICE
  NOTICKETS --> FAULTFIXED
  NOSMARTCARD --> FAULTFIXED
  NOTINSERVICE --> FAULTFIXED
  NOSMARTCARD --> REBOOTATTEMPT
  NOTINSERVICE --> REBOOTATTEMPT
  REBOOTATTEMPT --> LOADING
  FAULTFIXED --> PRESENT

  PRESENTED{Smartcard or Barcode is presented to reader}
  CARDREADABLE{Is presented card readable?}
  BCREADABLE{Barcode: Is barcode readable?}
  ABTERROR[1.6.3 ABT Error reading card]
  CARDTYPE{Is the presented smartcard a Legacy miFare or ABT EMV?}
  UNABLEVALIDATE[1.3.16 Unable to Validate]

  PRESENT --> PRESENTED
  PRESENTED --> CARDREADABLE
  PRESENTED --> BCREADABLE
  CARDREADABLE -->|Yes| CARDTYPE
  CARDREADABLE -->|No| ABTERROR
  BCREADABLE -->|Yes, implied| BCROUTE
  BCREADABLE -->|No, implied| UNABLEVALIDATE

  %% ABT EMV branch
  ABTAID{ABT: Valid AID?}
  ABTEXP{ABT: Card is Expired?}
  ABTODA{ABT: ODA Valid?}
  ABTBIN{ABT: Is PAN on BIN list?}
  ABTDENYLIST{ABT: PAN on Deny List?}
  ABTPB{ABT: Has PAN been used within Passback Period?}
  ABTDENY[1.6.2 ABT deny list/negative list]
  ABTTAGOK[1.6.1.1 ABT Tag successful]
  PBNOENTRY[1.6.6 Passback - No Entry]

  CARDTYPE -->|ABT| ABTAID
  ABTAID -->|Yes VISA/Mastercard/Maestro| ABTEXP
  ABTAID -->|No Amex etc| ABTDENY
  ABTEXP -->|No| ABTODA
  ABTEXP -->|Yes| ABTDENY
  ABTODA -->|Valid| ABTBIN
  ABTODA -->|No| ABTDENY
  ABTBIN -->|No| ABTDENYLIST
  ABTBIN -->|Yes| ABTDENY
  ABTDENYLIST -->|No| ABTPB
  ABTDENYLIST -->|Yes| ABTDENY
  ABTPB -->|No| ABTTAGOK
  ABTPB -->|Yes| PBNOENTRY

  %% Legacy smartcard branch
  SCOPERATOR{Smartcard: Is smartcard an operator card?}
  OPMATCH{Does Operator ID match a Technician ID in Stafflist?}
  TECHMENU[[See "Technician Menu" board for Technician Sign-on]]
  DEVICENORESPOND{Device will not respond}
  SCBLOCKED{Smartcard: Is card blocked?}
  SCACTIONLIST{Smartcard: Is card on the Actionlist?}
  HOTLISTED[1.6.4 ABT Hot listed card]
  SCLOCVALID{Smartcard: Is smartcard product valid for current location?}
  NOTVALIDLOC[1.3.7 Not Valid At This Location]
  SCTIMEVALID{Smartcard: Is smartcard valid at current time/date?}
  INVALIDTIME[1.3.8 Invalid Time Of Day]
  SCEXPIRED{Smartcard: Is smartcard expired?}
  PRODEXPIRED[1.3.9 Product Expired]
  SCPBPERIOD{Smartcard: Is smartcard within Passback period?}
  PBJOURNEYS[1.4.3 Passback Journeys Left]
  PBDAYS[1.4.4 Passback Days Left]
  SCTRANSFER{Smartcard: Is smartcard within transfer period?}
  TAGSUCCESS[1.5.0 Tag successful]
  SCRECORDUPDATED{Smartcard: Was Smartcard validation record successfully updated?}
  REPRESENT[1.3.1 Represent Card]

  CARDTYPE -->|Smartcard| SCOPERATOR
  SCOPERATOR -->|Yes| OPMATCH
  SCOPERATOR -->|No| SCBLOCKED
  OPMATCH -->|Yes| TECHMENU
  OPMATCH -->|No| DEVICENORESPOND
  SCBLOCKED -->|No| SCACTIONLIST
  SCBLOCKED -->|Yes| HOTLISTED
  SCACTIONLIST -->|No| SCLOCVALID
  SCACTIONLIST -->|Yes| HOTLISTED
  SCLOCVALID -->|Yes| SCTIMEVALID
  SCLOCVALID -->|No| NOTVALIDLOC
  SCTIMEVALID -->|Yes| SCEXPIRED
  SCTIMEVALID -->|No| INVALIDTIME
  SCEXPIRED -->|No| SCPBPERIOD
  SCEXPIRED -->|Yes| PRODEXPIRED
  SCPBPERIOD -->|No| SCTRANSFER
  SCPBPERIOD -->|Yes| PBJOURNEYS
  SCPBPERIOD -->|unlabeled, same decision| PBDAYS
  SCTRANSFER -->|Yes| TAGSUCCESS
  SCTRANSFER -->|No| SCRECORDUPDATED
  SCRECORDUPDATED -->|Yes| TAGSUCCESS
  SCRECORDUPDATED -->|No| REPRESENT

  %% Barcode branch
  BCROUTE{Barcode: Is barcode valid on current route/service?}
  BCDATETIME{Barcode: Is barcode valid at current date/time}
  BCLOC{Barcode: Is barcode valid at current location?}
  BCEXP{Barcode: Is barcode expired?}
  BCPB{Barcode: Has Barcode been used within Passback Period?}
  BCFAILSERVICE[1.7.99.2 Barcode Validation Fail - Service]
  BCFAILTIME[1.7.99.3 Barcode Validation Fail - Time]
  BCFAILLOC[1.7.99.4 Barcode Validation Fail - Location]
  BCFAILEXP[1.7.99.5 Barcode Validation Fail - Expired]
  BCFAILPB[1.7.99.6 Barcode Validation Fail - Passback PV]
  BCSUCCESS[1.7.1.1 Barcode Validation Successful - Adult]

  BCROUTE -->|Yes, implied| BCDATETIME
  BCROUTE -->|No, implied| BCFAILSERVICE
  BCDATETIME -->|Yes, implied| BCLOC
  BCDATETIME -->|No, implied| BCFAILTIME
  BCLOC -->|Yes, implied| BCEXP
  BCLOC -->|No, implied| BCFAILLOC
  BCEXP -->|No, implied| BCPB
  BCEXP -->|Yes, implied| BCFAILEXP
  BCPB -->|No| BCSUCCESS
  BCPB -->|Yes| BCFAILPB
```

## Paths (each path = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Device powered on → Loading → commissioned & fully operational → Present SmartCard or Barcode | boot | — | 4105408 |
| 2 | Device powered on → Loading → NOT commissioned → Is Validator/Plinth Commissioned? (No) → Machine Not in Service | boot/commissioning | — | 4102430 |
| 3 | Device powered on → Loading → NOT commissioned → Is Validator/Plinth Commissioned? (Yes) → Machine Not in Service | boot/commissioning | @destructive | GAP — see proposals/coherence-audit/gap-register.md |
| 4 | Present SmartCard or Barcode → device fault: Barcode Reader unavailable → Present SmartCard no Tickets → fault corrected → Present SmartCard or Barcode | device-fault | @destructive | 4104109 |
| 5 | Present SmartCard or Barcode → device fault: Smartcard Reader unavailable → Present Ticket no SmartCard → fault corrected → Present SmartCard or Barcode | device-fault | @destructive | 4104109 |
| 6 | Present SmartCard or Barcode → device fault: Smartcard Reader unavailable → Present Ticket no SmartCard → reboot attempt → Loading | device-fault | @destructive | 4105409 |
| 7 | Present SmartCard or Barcode → device fault: both readers unavailable / other non-powerloss fault → Machine Not in Service → fault corrected → Present SmartCard or Barcode | device-fault | @destructive | 4105410 |
| 8 | Present SmartCard or Barcode → device fault: both readers unavailable / other non-powerloss fault → Machine Not in Service → reboot attempt → Loading | device-fault | @destructive | 4105411 |
| 9 | Smartcard or Barcode presented → card not readable → ABT Error reading card | card-present | @destructive | 4101039 |
| 10 | Smartcard or Barcode presented → barcode not readable → Unable to Validate | card-present | @destructive | 4101029 |
| 11 | Card readable → Legacy miFare or ABT EMV? → ABT → Valid AID (VISA/Mastercard/Maestro) → not expired → ODA Valid → PAN not on BIN list → PAN not on Deny List → not used within Passback Period → ABT Tag successful | abt-emv | — | 4101000, 4101038 |
| 12 | ABT path → Valid AID? No (Amex etc) → ABT deny list/negative list | abt-emv | @destructive | 4101000, 4101038 |
| 13 | ABT path → Valid AID Yes → Card is Expired? Yes → ABT deny list/negative list | abt-emv | @destructive | 4101000, 4101038 |
| 14 | ABT path → ODA Valid? No → ABT deny list/negative list | abt-emv | @destructive | 4101000, 4101038 |
| 15 | ABT path → Is PAN on BIN list? Yes → ABT deny list/negative list | abt-emv | @destructive | 4101000, 4101038 |
| 16 | ABT path → PAN on Deny List? Yes → ABT deny list/negative list | abt-emv | @destructive | 4101000, 4101038 |
| 17 | ABT path → Has PAN been used within Passback Period? Yes → Passback - No Entry | abt-emv | — | 4101088, 4101041 |
| 18 | Card readable → Legacy miFare or ABT EMV? → Smartcard → not an operator card → not blocked → not on Actionlist → product valid for location → valid at time/date → not expired → not within Passback period → within transfer period → Tag successful | smartcard | — | 4103566, 4101007 |
| 19 | Smartcard → not operator card → not blocked → not on Actionlist → product valid → valid at time → not expired → not within Passback → NOT within transfer period → validation record successfully updated Yes → Tag successful | smartcard | — | 4103567 |
| 20 | Smartcard → …→ NOT within transfer period → validation record successfully updated No → Represent Card | smartcard | @destructive | 4100992, 4101028 |
| 21 | Smartcard → is operator card → Operator ID matches Technician ID in Stafflist Yes → routes to Technician Menu board (Technician Sign-on) | smartcard/operator | — | 4101011, 4101076 |
| 22 | Smartcard → is operator card → Operator ID does NOT match Technician ID in Stafflist → Device will not respond | smartcard/operator | @destructive | 4105412 |
| 23 | Smartcard → not operator card → card blocked Yes → ABT Hot listed card | smartcard | @destructive | 4100992, 4101040 |
| 24 | Smartcard → not operator card → not blocked → on Actionlist Yes → ABT Hot listed card | smartcard | @destructive | 4100992, 4101040 |
| 25 | Smartcard → …→ product NOT valid for current location → Not Valid At This Location | smartcard | @destructive | 4100984, 4104446, 4104448, 4104450, 4104451, 4104453, 4104455, 4104457, 4104438, 4104440, 4104442, 4104444, 4100987 |
| 26 | Smartcard → …→ NOT valid at current time/date → Invalid Time Of Day | smartcard | @destructive | 4100991, 4104469 |
| 27 | Smartcard → …→ expired Yes → Product Expired | smartcard | @destructive | 4100981, 4104467 |
| 28 | Smartcard → …→ within Passback period Yes → Passback Journeys Left | smartcard | — | 4100993, 4101009 |
| 29 | Smartcard → …→ within Passback period (same decision, unlabeled branch) → Passback Days Left | smartcard | — | 4100993 |
| 30 | Barcode readable → valid on current route/service → valid at current date/time → valid at current location → not expired → not used within Passback Period → Barcode Validation Successful - Adult | barcode | — | 4101006, 4104489, 4104503, 4103560, 4102428 |
| 31 | Barcode → NOT valid on current route/service → Barcode Validation Fail - Service | barcode | @destructive | 4101043 |
| 32 | Barcode → valid on route → NOT valid at current date/time → Barcode Validation Fail - Time | barcode | @destructive | 4101044 |
| 33 | Barcode → valid on route → valid at date/time → NOT valid at current location → Barcode Validation Fail - Location | barcode | @destructive | 4101045 |
| 34 | Barcode → …→ expired Yes → Barcode Validation Fail - Expired | barcode | @destructive | 4103561 |
| 35 | Barcode → …→ not expired → used within Passback Period Yes → Barcode Validation Fail - Passback PV (per board note, PV treats this as a Passback response, not the same as a Gate Validator Failure) | barcode | — | 4101047 |

## Screen states (Given/Then anchors)
- **1.0.1 Present SmartCard or Barcode** — the PV's normal idle/ready screen; entry point for every
  card-or-barcode presentment, and the screen returned to once a device fault is corrected.
- **0.0 Loading** — shown at power-on and again after a reboot-recovery attempt, before the
  commissioning check runs.
- **1.2.1 Machine Not in Service** — shown when the plinth/validator is not commissioned, and also
  when both readers become unavailable or another non-powerloss fault occurs. Per the annotation, an
  uncommissioned device typically has an unprogrammed Plinth-ID, so the Status Bar's Device ID /
  Sub Location / Location fields may be blank until a Technician signs in and programs them.
- **1.1.0 Present SmartCard no Tickets** — shown when the Barcode Reader specifically becomes
  unavailable (smartcard reading still possible).
- **1.1.1 Present Ticket no SmartCard** — shown when the Smartcard Reader specifically becomes
  unavailable (barcode reading still possible).
- **1.6.1.1 ABT Tag successful** — can show an additional line of text; for NIR/Rail PVs this states
  "Northern Ireland Travel Only" (a distinct "- Rail" variant of this screen is referenced in the
  source but has no separate connections listed).
- **1.6.3 ABT Error reading card** — reached when a presented card is not readable, before the
  Legacy-miFare/ABT-EMV split; title says "ABT" but the trigger ("Is presented card readable?") is
  upstream of the ABT/Legacy branch — see Notes/unknowns.
- **1.6.2 ABT deny list/negative list** — the shared failure screen for every ABT EMV rejection reason
  (bad AID, expired, ODA invalid, BIN-listed, deny-listed).
- **1.6.6 Passback - No Entry** — ABT EMV Passback-period rejection.
- **1.4.3 Passback Journeys Left / 1.4.4 Passback Days Left** — legacy smartcard Passback-period
  screens; per the board's own note, Passback on the PV is not treated as a Failure response (unlike
  the Gate Validator).
- **1.5.0 Tag successful** — legacy smartcard success screen, reached either directly (within
  transfer period) or after the validation record update succeeds.
- **1.3.1 Represent Card** — shown if the smartcard validation record fails to update.
- **1.7.1.1 Barcode Validation Successful - Adult** — barcode success screen. Annotation: for
  barcodes with an expiry time between 00:00 and 04:00, the PV must display the previous day as the
  expiry date on this (MUB) screen.
- **1.7.99.2 / .3 / .4 / .5 / .6 Barcode Validation Fail - Service / Time / Location / Expired /
  Passback PV** — barcode rejection screens, one per failed decision in the barcode chain.
- **1.3.16 Unable to Validate** — shown when the barcode itself is not readable.

## Notes / unknowns
- TODO: confirm the "Is Validator/Plinth Commissioned?" decision — the raw transcription lists both
  its **Yes** and **No** branches routing to the same "1.2.1 Machine Not in Service" screen (lines
  975–976 of the raw transcription). This may be a transcription artifact in the Overflow source
  rather than genuine device behaviour; flag for engineer confirmation before treating "Yes →
  Machine Not in Service" as a real path.
- TODO: confirm the "Smartcard Is smartcard within Passback period?" decision's second outgoing
  connection to "1.4.4 Passback Days Left" — the raw source gives this connection no branch label
  (unlike the labelled "Yes → 1.4.3 Passback Journeys Left"), so it's unclear whether Passback Days
  Left is a second Yes-branch outcome (e.g. day-pass vs journey-pass product) or something else.
- TODO: confirm why "1.6.3 ABT Error reading card" is reached from the generic "Is presented card
  readable? [No]" decision, which sits upstream of the Legacy-miFare/ABT-EMV split — the screen name
  implies ABT-specific handling but the trigger is not ABT-specific in the raw connections.
- "1.6.1.1 ABT Tag successful - Rail" is listed as a distinct screen in the board's Screens list but
  has no explicit connection of its own in the raw transcription; treated here as the NIR/Rail
  variant of "1.6.1.1 ABT Tag successful" referenced in the annotations, not a separately reachable
  node.
- "Does Operator ID match a Technician ID in Stafflist? [Yes]" routes to "See 'Technician Menu'
  board for Technician Sign-on" — this is a cross-board pointer, not a screen; the actual Technician
  Sign-on flow is transcribed separately in board 5 ("Technician Menu - Platform Validator"), not in
  this file.
- "Device will not respond" (Operator ID does not match any Technician ID) has no further outgoing
  connection in the raw transcription — treated as a terminal/dead-end state here; TODO: confirm
  there is genuinely no recovery path shown on this board.
- The barcode-chain decisions ("Is barcode valid on current route/service?", "…at current date/
  time", "…at current location?", "…expired?", "…used within Passback Period?") have unlabeled
  connections in the raw source rather than explicit Yes/No branch text; the pass-through vs.
  fail-screen direction was inferred from which screen each edge points to (fail screens are named
  for the specific check), and is marked "implied" in the Diagram above rather than presented as a
  literal transcribed label.
