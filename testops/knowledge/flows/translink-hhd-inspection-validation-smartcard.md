# Flow: Translink HHD — Inspection & Validation V2 (Smartcard)

- Source: `knowledge/flows/translink-hhd-full-transcription-v17.3.7.md`, board "9. Inspection &
  Validation V2" (Screens/Decision Points/Annotations/Connections lists under that heading).
  Transcribed/structured 2026-08-05.
- Project: translink   Device: HHD   Feature: smartcard inspection & validation (mode switch, card
  read, passback, pre-validation, previously-validated/transfer-period checks, penalty
  fare/warning, and the discount/concession re-sell path an Invalid card can route into)
- Transcription confidence: **medium** — the raw board reuses identical decision labels
  (`Glider/Rail?`, `Does the direction of travel match the current route?`, `Back to Sales
  screen.` / `Back to 'Sales' screen.`) from multiple different entry points with different
  outgoing edges each time. This file preserves that structure by giving each reused instance its
  own diagram node (suffixed `2`/`3`) rather than merging them into one node with all edges —
  see Notes/unknowns.
- **Revenue Inspection** (the square-button EMV/BOS function) is a genuinely separate feature area
  of the same board — see `translink-hhd-inspection-validation-revenue.md`.

## Diagram
```mermaid
flowchart TD
  SI_DV["2.0 Sales Screen - Inspection - Device View"]
  SI_RAIL_DV["2.0.6 Sales Screen - Rail- Inspection - Device View"]
  SV_RAIL_DV["2.0.6 Sales Screen - Rail- Validation - Device View"]
  PRESENT_SC["8.4 Present Smart Card"]

  SI_DV -->|swipe Inspection to change mode| D_MODE{"HHD remains in inspection mode"}
  SI_RAIL_DV -->|swipe Inspection to engage Validation mode| SV_RAIL_DV
  SV_RAIL_DV -->|swipe Validation to engage Inspection mode| SI_RAIL_DV

  SI_DV -->|presents a smartcard| D_READABLE{"Smartcard Readable?"}
  SI_RAIL_DV -->|presents a smartcard| D_READABLE
  SV_RAIL_DV -->|presents a smartcard| D_READABLE
  PRESENT_SC -->|presents smartcard| D_READABLE

  D_READABLE -->|No / not readable| ERR_RW["3.3 Error - Read/Write Fail"]
  D_READABLE -->|No| CRIT_ERR["2.5.4.1 Critical Error"]
  D_READABLE -->|Yes| D_PASSBACK_CFG{"Is passback configured?"}
  D_READABLE -->|Yes| D_VALIDTOPUP{"Valid top-up card?"}

  ERR_RW -->|Retry| D_GOBACKPREV{"Go back to previous screen."}
  ERR_RW -->|'Faulty Smartpass'| D_TOPUPPRINT{"Go to 'Top Up Receipt Print' flow."}
  ERR_RW -->|Cancel| D_BACKSALES{"Back to Sales screen."}
  D_TOPUPPRINT -->|print flow complete| D_BACKSALES

  D_PASSBACK_CFG -->|No| D_PREVALID{"Passed pre-validation checks?"}
  D_PASSBACK_CFG -->|No| D_VALID{"Smartcard Valid?"}
  D_PASSBACK_CFG -->|Yes| D_PASSBACK_PERIOD{"Smartcard Last Used within passback period?"}
  D_PASSBACK_PERIOD -->|No| D_PREVALID
  D_PASSBACK_PERIOD -->|No| D_VALID
  D_PASSBACK_PERIOD -->|Yes| ERR_PASSBACK["2.5.4.2 Error - Passback"]
  ERR_PASSBACK --> D_BACKSALES

  D_PREVALID -->|Yes| D_PREV_VALIDATED{"Has the smartcard been previously validated?"}
  D_PREVALID -->|No| ERR_GENERIC["3.3.1 Error"]

  D_PREV_VALIDATED -->|No| INVALID["3.2 Inspection - Invalid"]
  D_PREV_VALIDATED -->|Yes| D_TRANSFER{"Is 'Last Use' within the transfer period? (less than 90 minutes)"}

  D_TRANSFER -->|Yes: within period| D_DIRECTION_A{"Does the direction of travel match the current route?"}
  D_TRANSFER -->|No: outside period| D_DIRECTION_B{"Does the direction of travel match the current route?"}
  D_DIRECTION_A -->|Yes| VALID["3.1 Inspection - Valid"]
  D_DIRECTION_A -->|No| INVALID
  D_DIRECTION_B -->|Yes| INV_WARN["3.2.1 Inspection - Invalid - Warning"]
  D_DIRECTION_B -->|No| INVALID

  VALID --> D_BACKSALES
  VALID -->|selects 'Not Valid'| ERR_GENERIC

  INVALID -->|taps 'Validate'| D_GLIDERRAIL{"Glider/Rail?"}
  INVALID -->|selects 'Penalty Fare'| ERR_GENERIC
  INV_WARN -->|taps 'Validate'| D_GLIDERRAIL
  INV_WARN -->|selects 'Penalty Fare'| ERR_GENERIC

  ERR_GENERIC -->|taps/selects 'Penalty Warning' — ticket prints| D_PENWARNPRINT{"Go to Penalty Warning print flow."}
  ERR_GENERIC -->|taps 'Penalty Fare'| D_PENFARE3RD{"A third party app opens. A Penalty Fare ticket also prints."}
  ERR_GENERIC -->|selects 'Penalty Fare'| D_USERPENFARE{"User chooses to issue a penalty fare and third party app opens. A Penalty Fare ticket also prints."}
  ERR_GENERIC --> D_BACKSALES
  D_PENWARNPRINT -->|print flow complete| D_BACKSALES
  D_PENFARE3RD --> D_BACKSALES
  D_USERPENFARE --> D_BACKSALES

  D_VALID -->|Yes: valid| D_TYPE_COMM{"Smartcard Type Commercial/Staff/EA?"}
  D_VALID -->|No: Travel is prohibited| ERR_GENERIC
  D_VALID -->|No: No travel remaining| NOTRAVEL["3.2.3 Smartcard Not Valid - No Travel Remaining"]
  NOTRAVEL -->|taps 'Top-Up'| TOPUP_SELECT["4.2.2 Top Up - iLink - Select Product"]
  NOTRAVEL -->|Cancel| D_BACKSALES

  TOPUP_SELECT -->|iLink product selected| NOWARRANT["2.4.0.1 Payment Area - No Warrant"]
  NOWARRANT -->|selects a Cash value| REPRESENT_SC["4.4 Represent Smartcard"]
  NOWARRANT -->|taps 'Card' button| D_CARDPAY{"See Card Payment flow."}
  D_CARDPAY -->|successful card payment| REPRESENT_SC
  REPRESENT_SC --> D_READABLE

  D_VALIDTOPUP -->|No| CRIT_ERR_INVALID["4.1.2 Critical Error - Invalid Card"]
  D_VALIDTOPUP -->|Yes| PRINT_CASH["8.5 Printing Receipt - Cash"]
  CRIT_ERR_INVALID -->|taps 'Cancel'| D_PAYCARDUSED{"Payment card used?"}
  CRIT_ERR_INVALID -->|taps 'Retry'| D_REPRESENT_BACK{"Back to 'Represent Smartcard' screen."}
  CRIT_ERR -->|taps 'Cancel'| D_PAYCARDUSED
  CRIT_ERR -->|taps 'Retry'| D_REPRESENT_BACK
  D_PAYCARDUSED -->|No| D_BACKSALES
  D_PAYCARDUSED -->|Yes| VOID_TXN["4.6 Voiding Last Card Transaction"]
  VOID_TXN --> D_CARDPAYPRINT{"Go to the 'Card Payment Receipt Print' flow."}

  PRINT_CASH --> D_ABLEPRINT{"Able to print?"}
  D_ABLEPRINT -->|No| PRINT_FAILED["7.2 Print Failed"]
  D_ABLEPRINT -->|Yes| TXN_COMPLETE["2.4.3.1 Transaction complete"]
  PRINT_FAILED -->|'Continue Without Printing'| VAL_OK["3.2.2 Successful Validation"]
  TXN_COMPLETE -->|3s timeout| VAL_OK
  VAL_OK --> VAL_SUCCESS["2.6.7 Validation - Success"]
  VAL_SUCCESS --> D_BACKSALES

  D_GLIDERRAIL -->|Rail| PRESENT_SC
  D_GLIDERRAIL -->|Glider — no explicit condition text, by elimination| D_TYPE_COMM
  D_TYPE_COMM -->|Yes| D_GLIDERRAIL2{"Glider/Rail?"}
  D_TYPE_COMM -->|No — no explicit condition text, by elimination| D_TYPE_DISC{"Smartcard Type Discounted Fare Validation?"}
  D_TYPE_DISC -->|Yes| D_HALFFARE{"Half-Fare?"}
  D_TYPE_DISC -->|No — no explicit condition text, by elimination| D_TYPE_CONCESSION{"Smartcard Type Concession Fare Validation"}
  D_HALFFARE -->|Yes| D_GLIDERRAIL2
  D_HALFFARE -->|No| D_YLINK{"yLink Validation?"}
  D_YLINK -->|Yes| D_GLIDERRAIL2
  D_YLINK -->|No| DISC_RAIL["2.6.1 Discount - Sales mode - Rail"]
  D_TYPE_CONCESSION -->|Concession Fare Validation| D_GLIDERRAIL3{"Glider/Rail?"}

  D_GLIDERRAIL2 -->|Rail| DISC_RAIL
  D_GLIDERRAIL2 -->|Glider| DISC_YLINK["2.6 Discount - Sales mode (yLink)"]
  D_GLIDERRAIL2 -->|Rail| VAL_SUCCESS
  D_GLIDERRAIL2 -->|Glider| CONCESSION["2.6.5 Concessionary Card - Sales mode"]
  D_GLIDERRAIL3 -->|Rail| CONCESSION_RAIL["2.6.5.1 Concessionary Card - Sales mode - Rail"]
  D_GLIDERRAIL3 -->|Glider| CONCESSION

  DISC_YLINK --> DISC_YLINK_ALIGHT["2.6.0.1 Discount - Sales mode - Alighting Selected (yLink)"]
  DISC_YLINK_ALIGHT --> DISC_SUMMARY["2.6.2 Discount - Summary (yLink)"]
  DISC_RAIL --> DISC_SUMMARY
  DISC_RAIL --> DISC_RAIL_SELECT["2.6.1 - Discount - Sales mode - Select Product - Rail - yLink"]
  DISC_RAIL_SELECT --> DISC_RAIL
  DISC_SUMMARY --> PAY_AREA["2.4 Payment Area"]
  DISC_SUMMARY --> PAY_GLIDER["2.4 Payment Area (Glider)"]

  CONCESSION --> D_READABLE
  CONCESSION_RAIL --> D_CROSSBORDER{"Cross Border?"}
  D_CROSSBORDER -->|No| D_NOOTHERTICKET{"If no other Ticket Types are available the HHD will remain on the current screen"}
  D_CROSSBORDER -->|Yes| CONCESSION_XB_SELECT["2.6.1 - Discount - Sales mode - Select Product - SeniorXB"]
  CONCESSION_XB_SELECT -->|selects a Ticket Type| CONCESSION_RAIL
  CONCESSION_RAIL --> REPRESENT_SC

  PAY_AREA -->|taps 'Card' button| D_CARDPAY
  PAY_AREA -->|cash preset / correct amount / Warrant| D_CASHPAYPRINT{"Go to relevant 'Cash / Payment Card Print Flow' flow."}
  PAY_GLIDER -->|taps 'Card' button| D_CARDPAY
  PAY_GLIDER -->|cash preset / correct amount / Warrant| REPRESENT_SC
```

## Paths (each = one candidate scenario)
| # | Path | Feature | Tags | Covered by |
|---|------|---------|------|------------|
| 1 | Sales Screen (Inspection) → swipe → HHD remains in inspection mode | inspection-validation | — | 4105196 |
| 2 | Sales Screen Rail (Inspection) → swipe → Rail (Validation) → swipe back → Rail (Inspection) | inspection-validation | — | 4105197 |
| 3 | Present smartcard → not readable → Error Read/Write Fail → Retry → previous screen | inspection-validation | @destructive | C4103825 |
| 4 | Present smartcard → not readable → Error Read/Write Fail → 'Faulty Smartpass' → Top Up Receipt Print flow → Sales screen | inspection-validation | @destructive | 4105198 |
| 5 | Present smartcard → readable → passback configured → last used within passback period → Error - Passback → Sales screen | inspection-validation | @destructive | C4103827 |
| 6 | Present smartcard → readable → (no passback / passback OK) → pre-validation fails → 3.3.1 Error | inspection-validation | @destructive | 4105199 |
| 7 | Pre-validation passes → not previously validated → Inspection - Invalid | inspection-validation | — | 4105200 |
| 8 | Pre-validation passes → previously validated → within 90-min transfer period → direction matches → Inspection - Valid → Back to Sales | inspection-validation | — | C4103971 |
| 9 | Pre-validation passes → previously validated → within 90-min transfer period → direction does NOT match → Inspection - Invalid | inspection-validation | @destructive | 4105201 |
| 10 | Pre-validation passes → previously validated → outside 90-min transfer period → direction matches → Inspection - Invalid - Warning | inspection-validation | @destructive | FRAGMENTED — see consolidation-audit.md |
| 11 | Pre-validation passes → previously validated → outside 90-min transfer period → direction does NOT match → Inspection - Invalid | inspection-validation | @destructive | 4105202 |
| 12 | Inspection - Valid → selects 'Not Valid' → 3.3.1 Error | inspection-validation | @destructive | 4105203 |
| 13 | Inspection - Invalid / Invalid - Warning → taps 'Validate' → Glider/Rail? → Present Smart Card (Rail) or fare-type routing (Glider) | inspection-validation | — | 4105204 |
| 14 | 3.3.1 Error → 'Penalty Warning' → ticket prints → Penalty Warning print flow → Back to Sales | inspection-validation | @destructive | C4103894 |
| 15 | 3.3.1 Error → 'Penalty Fare' → third-party app opens → Penalty Fare ticket prints → Back to Sales | inspection-validation | @destructive | C4103896 |
| 16 | Smartcard Valid (Validation flow) → No, travel prohibited → 3.3.1 Error | inspection-validation | @destructive | 4105205 |
| 17 | Smartcard Valid (Validation flow) → No, no travel remaining → Not Valid - No Travel Remaining → 'Top-Up' → iLink product → No Warrant Payment Area → Cash/Card → Represent Smartcard | inspection-validation | — | FRAGMENTED — see consolidation-audit.md |
| 18 | Valid top-up card? → No → Critical Error - Invalid Card → Retry / Cancel | inspection-validation | @destructive | 4105206 |
| 19 | Valid top-up card? → Yes → Printing Receipt - Cash → Able to print? Yes → Transaction complete → Successful Validation → Validation - Success | inspection-validation | — | C4103800(-analog Top-Up cases) |
| 20 | Able to print? → No → Print Failed → Continue Without Printing → Successful Validation | inspection-validation | @destructive | FRAGMENTED — see consolidation-audit.md |
| 21 | Smartcard Valid (Validation flow) → Yes → fare-type chain (Commercial/Staff/EA → Discounted Fare → Half-Fare → yLink) → Glider/Rail? → Discount - Sales mode - Rail or (yLink) | inspection-validation | — | 4105207 |
| 22 | Fare-type chain → Concession Fare Validation → Glider/Rail? → Concessionary Card - Sales mode (Glider) or - Rail | inspection-validation | — | 4105208 |
| 23 | Concessionary Card - Sales mode - Rail → Cross Border? Yes → Select Product - SeniorXB → select Ticket Type → back to Concessionary Card - Sales mode - Rail → Represent Smartcard | inspection-validation | — | 4105209 |
| 24 | Concessionary Card - Sales mode - Rail → Cross Border? No → "no other Ticket Types available, remains on current screen" | inspection-validation | @destructive | 4105210 |
| 25 | Discount - Sales mode (yLink) → Alighting Selected → Discount - Summary → Payment Area (Glider) or Payment Area | inspection-validation | — | 4105211 |
| 26 | Payment Area / Payment Area (Glider) → 'Card' button → See Card Payment flow → successful payment → Represent Smartcard | inspection-validation | — | 4105212 |
| 27 | Payment Area / Payment Area (Glider) → cash preset/Warrant → Cash/Payment Card Print flow, or Represent Smartcard (Glider) | inspection-validation | — | 4105213 |
| 28 | Critical Error (2.5.4.1) → Cancel → Payment card used? → Yes → Voiding Last Card Transaction → Card Payment Receipt Print flow | inspection-validation | @destructive | 4105214 |

## Screen states (Given/Then anchors)
- **2.0 Sales Screen - Inspection - Device View / 2.0.6 Sales Screen - Rail- Inspection - Device
  View / 2.0.6 Sales Screen - Rail- Validation - Device View** — the "V2"/"Device View" screens;
  swiping toggles Inspection↔Validation mode; presenting a smartcard from any of them starts the
  `Smartcard Readable?` decision.
- **3.1 Inspection - Valid** — reached only when previously-validated AND direction-of-travel
  matches; offers 'Not Valid' override → 3.3.1 Error.
- **3.2 Inspection - Invalid** — reached from: not-previously-validated, OR direction mismatch (in
  either the within- or outside-transfer-period branch). Offers 'Validate' (→ Glider/Rail? fare
  routing) and 'Penalty Fare' (→ 3.3.1 Error).
- **3.2.1 Inspection - Invalid - Warning** — reached only from the outside-transfer-period branch
  when direction matches. Same two actions as 3.2 Invalid.
- **3.2.3 Smartcard Not Valid - No Travel Remaining** — offers 'Top-Up' (routes into the iLink top-up
  purchase flow) or Cancel.
- **3.3.1 Error** — the shared error/penalty screen: 'Penalty Warning' (ticket prints, then routes
  back to Sales), 'Penalty Fare' (opens third-party app + prints ticket), or Back to Sales. Error
  message text per annotation: "Product Expired / Pass Expired / No Journeys Left / No Balance
  Left / Hotlisted Card / Visual Rejection".
- **3.3 Error - Read/Write Fail** — 'Retry' (back to previous screen) or 'Faulty Smartpass' (routes
  to Top Up Receipt Print flow) or Cancel (Back to Sales).
- **2.5.4.2 Error - Passback** — reached only when passback is configured AND the card's last use
  is within the passback period.
- **2.5.4.1 Critical Error / 4.1.2 Critical Error - Invalid Card** — both offer Cancel (→ Payment
  card used?) and Retry (→ Back to Represent Smartcard screen).
- **2.6.7 Validation - Success** — end state after a successful validation printing sequence
  (Transaction complete → 3.2.2 Successful Validation → 2.6.7); routes Back to Sales.
- Per annotation: **on validation, a Transaction Record is sent to the back office** (BOS audit
  event — no further detail on payload/fields given in this board).

## Notes / unknowns
- The decision "Glider/Rail?" is transcribed at four distinct points in the source graph (post
  Invalid/Warning 'Validate', post Smartcard-Type-Commercial/Staff/EA, post Half-Fare/yLink, and
  post Smartcard-Type-Concession-Fare-Validation), each with a different outgoing edge set. This
  file gives each instance its own diagram node (`D_GLIDERRAIL`/`2`/`3`) rather than merging them
  into one node with all edges superimposed, to avoid implying reachability that isn't in the
  source. TODO: confirm with the design/Overflow source whether these are genuinely four separate
  decision instances or one reused sub-routine — the raw transcription does not distinguish them.
- Likewise "Does the direction of travel match the current route?" appears twice (post within-90-min
  transfer-period, and post outside-90-min transfer-period) with different destination screens for
  the same Yes/No answer (Valid/Invalid vs Invalid-Warning/Invalid) — kept as two nodes
  (`D_DIRECTION_A`/`B`) for the same reason.
- "Back to Sales screen." and "Back to 'Sales' screen." appear as two textual variants in the raw
  source (with/without single quotes and with a capital S) — treated here as the same terminal
  decision (`D_BACKSALES`); TODO: confirm they are not meant to be distinguishable screens (e.g.
  Glider vs Rail sales screen).
- Two "Glider/Rail?" outgoing edges have no bracketed condition text in the source (`Glider/Rail? →
  Smartcard Type Commercial/Staff/EA?` and the two "Smartcard Type …?" chain edges into the next
  check) — the [Glider]/[No] labels shown in the diagram are inferred **by elimination** against the
  sibling edge that *does* carry a `[Rail]`/`[Yes]` label. TODO: confirm this inference against
  Overflow directly.
- Annotation "Previous screens may be: 2.0 Sales Screen - Inspection / 2.0.6 Sales Screen - Rail -
  Inspection / 2.6.5 Concessionary Card - Sales mode" is present in the source but its anchor
  screen (which screen this annotates) is not stated. TODO: confirm which screen this note attaches
  to (likely 4.4 Represent Smartcard or a Critical Error screen).
- Annotation: "'Penalty Fare' option may be disabled if the Penalty Fare App is not available, the
  printer is disconnected or the Smartcard product is valid for free travel" — a precondition on
  3.3.1 Error's 'Penalty Fare' button, not itself a screen/connection.
- Annotation: "Warrant is used for paper tickets only, not top-ups. They will appear on Waybills and
  are available on Rail only" — governs the 2.4.0.1 Payment Area - No Warrant screen's Warrant
  option; not shown as its own diagram branch since no connection for it was transcribed beyond the
  Cash/Card options already mapped.
- Annotation on card-payment receipt printing ("N.B. '£Price change' header will only show if cash
  was the payment method… this will be 1 of 2 for print due to additional receipts for card
  payment. Print will still go through same checks seen in Print flows.") and "For a card payment,
  there will be a check to see if you also want to print the customer receipt as seen in the
  'Payment Card Print' flow" both describe the Card Payment Receipt Print sub-flow referenced from
  `D_CARDPAYPRINT`/`D_CASHPAYPRINT`, which is itself out of scope for this board (not expanded here
  — TODO: confirm against the dedicated Payment Card Print flow board/file if one exists).
- Annotation: "Other cards will display the tick and then [PRODUCT NAME] Validated below the tick.
  See 'Validation Successful' screen on the Rail flow for reference" — describes 2.6.7
  Validation - Success screen content; the referenced "Rail flow" reference screen is not itself in
  this board.
- Annotation on product options for Dependants Pass/Senior/Blind/War Pensioner/60+/ROI Senior
  (single only for local travel ≤ station 61; XB single/day return/1-month return for cross-border
  travel > station 61) governs the Cross Border?/SeniorXB Select Product screens.
- "Top-up is iLink only. Validation includes iLink, Staff, Spouse, Retired, External and aLink" is a
  stated scope note on the smartcard-type chain (Commercial/Staff/EA → Discounted → Concession) —
  no separate "Spouse"/"Retired"/"External"/"aLink" decision node was transcribed for this board,
  so those types are presumably folded into the existing type-decision screens. TODO: confirm
  whether Spouse/Retired/External/aLink route through the existing Commercial/Staff/EA or
  Discounted-Fare decisions, or are missing from this board's transcription.
