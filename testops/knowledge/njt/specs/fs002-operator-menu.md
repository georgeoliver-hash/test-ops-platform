# NJT FS002 — 5.4 Operator Menu (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` (Flowbird America Inc / an
Arrive Company), section 5.4 "Operator Menu" (Cancel Ticket, Hold, Pay Leave, Passenger Count, Driver
Totals, Dump, End of Trip + End of Run, Relief, Device Settings, Paper Status, Driver Break,
Supervisor/Audit Reports, Accept Next Bill, Clear Bill Jam). Distilled testable facts only — full spec
held locally in `njt-requirements/`, not committed. This note covers lines 3362–5019 of the extracted
text only; adjoining sections (5.3, 5.5 Other Functions) are covered elsewhere.

## Entry into the Operator Menu
- Pressing the **'F' key** displays the Operator menu; driver selects the desired action.
- If more options exist than fit one screen, **next/previous page** buttons appear.
- Driver returns to the ticket-issue screen via **'F' key or cancel key**. (NJT_FRFRP_FS002 p.34)

## Cancel Ticket (5.4.1)
- **Only available in Full Service mode.** (Implies unavailable in Exact Fare mode — **GAP**: not
  explicitly stated for Exact Fare; confirm.)
- Driver can cancel the **last paper product issued**. Selecting it shows the **annulment menu**
  (available transactions to cancel) → select transaction → FR shows transaction details → select
  "cancel" to cancel the transaction.
- Eligibility criteria (configurable, default values given):
  - Only the **last 1 paper transaction** can be cancelled (**OBV transactions are not selectable**).
  - Transactions can only be annulled **within 10 minutes of issue**.
- On confirmation: cancellation is audited, a **cancelled ticket receipt is printed (GR-12)**, audible +
  visual confirmation shown to driver, and a **cancelled transaction audit record sent to CloudFare**
  (GR-3, FRT-1). **If connected**, FR also sends a transaction detail message to the **Clever Device**
  (GR-10). (NJT_FRFRP_FS002 p.34)

## Hold (5.4.2)
- **Exact Fare service only** (GR-10, FM-1).
- Selecting Hold sends a message to the Farebox initiating the Farebox **'Hold'** facility, which
  **resets the Farebox's automatic dump timeout value back to 60 seconds.** (NJT_FRFRP_FS002 p.34)

## Pay Leave (5.4.3)
- For routes where the passenger pays on leaving the bus; passenger is treated as having boarded at
  the **first zone of the trip** (the default boarding zone set at trip sign-on).
- Selecting 'Pay Leave' displays the **Pay Leave ticket issue screen**, with zones set from the
  **default boarding zone to the current boarding zone**, and displays the fare due. (**GAP** — exact
  meaning of "zones set to the default boarding zone to the current boarding zone" is ambiguous in the
  source phrasing — confirm whether this denotes a zone range or a specific pair.)
- Driver must **set rider class and transaction type** before selecting the Pay Leave function.
- Driver can **issue the product** or **select cancel** to return to the ticket-issue screen; after
  issuing, FR returns to the ticket-issue screen. (NJT_FRFRP_FS002 p.34–35)

## Passenger Count (5.4.4)
- "The passenger count is now included on the driver totals screen." (**GAP** — the spec gives no
  further detail on Passenger Count as a distinct menu item; unclear whether 5.4.4 is a standalone
  menu entry/screen or purely a note that the count now surfaces inside Driver Totals — confirm with
  engineer / check live menu for a separate "Passenger Count" entry.) (NJT_FRFRP_FS002 p.35)

## Driver Totals (5.4.5)
- Selecting "Driver's Totals" shows totals **since signing on to the FR**: current **run** details
  and current **trip** details.
- Driver exits via **cancel key**; FR returns to the ticket-issue screen.
- For each totals option (run and trip) FR displays:
  - Number of gross tickets accepted + receipts issued
  - Gross cash taken
  - Number of cancelled tickets accepted + receipts issued
  - Amount of cancelled cash
  - Number of net receipts issued
  - Net cash taken
  - Net number of tickets accepted
- **Trip details only**, additionally displays:
  - **Passenger count** (number of boardings since start of trip). (NJT_FRFRP_FS002 p.35)

## Dump (5.4.6)
- **Exact Fare service only** (GR-10, FM-1).
- Sends a message to the Farebox instructing it to **'dump' any unused funds**, resetting available
  funds to zero.
- **If connected**, FR sends a transaction detail message to the **Clever Device** (GR-10).
  (NJT_FRFRP_FS002 p.36)

## End of Trip (5.4.7)
- Ends the current service trip and lets the driver log in to the next trip.
- Selecting the option shows a **confirmation screen**. Driver may:
  - **Cancel** → FR returns to the ticket-issue screen (no end-of-trip action taken).
  - **Confirm** → FR ends the trip, **prints a trip report receipt (GR-12)**, sends the **end of trip
    message to the Clever Device (GR-10)**, and sends an **end of trip record to CloudFare (GR-3,
    FRT-1)**.
- After confirming, FR shows an indication it is **waiting for a response from the IVN** with
  Suggested Trip Details for the next trip.
  - FR **suspends normal Farebox polling for up to 1000 ms** to allow the IVN time to respond.
  - IVN responds within this window **or not at all**.
  - If the Suggested Trip Details message is **not received within 1 second** of the end-of-trip
    message, FR **sends an event to CloudFare** (GR-3, FRT-1).
  - When received, FR **auto pre-fills** trip sign-on fields with suggested data, up to the **first
    `00` value found after the message subtype field**; data after that `00` is **not used**.
  - Driver then completes sign-on manually for any remaining fields.
  - If **no Suggested Trip Details message arrives within 1 second**, OR the message contains **no
    useful data (all fields zero)**, the driver may **enter trip details manually**.
  - If the **"reassignment alert" flag** is set in the Suggested Trip Details message, FR displays a
    **"reassignment received"** message that the **driver must acknowledge** before continuing sign-on.
    (See referenced document [4] for more detail — **GAP**: external doc, not in this excerpt.)
    (NJT_FRFRP_FS002 p.35–37)

### End of Run (5.4.7.1)
- At any point during the End of Trip process, the operator can press **F** to initiate **End of
  Run**.
- Driver must **confirm** the End of Run action, or **cancel** back to the trip sign-on screen.
- Selecting **"ISSUE"** initiates the End of Run procedure: an **end of run report is produced**, FR
  sends an **end of shift record to CloudFare** (GR-3, FRT-1) and an **End of Run message to the
  Clever Device** (GR-10). (NJT_FRFRP_FS002 p.37)

## Relief (5.4.8)
- Driver is prompted to confirm a Relief is required. Selecting **"ISSUE"** initiates the Relief
  procedure: a **relief report is produced**, FR **signs off the current driver**, sends an **end of
  shift record to CloudFare** (GR-3, FRT-1), and sends an **operator relief message to the Clever
  Device** (GR-10). (**GAP** — no explicit "cancel" path described for Relief, unlike End of Trip/End
  of Run; confirm whether cancel is available here too.) (NJT_FRFRP_FS002 p.37)

## Device Settings (5.4.9)
- Lets the driver change **screen brightness** and **volume level** of the Fare Register and of the
  Farebox (GR-10, FM-1). Options presented:
  - Increment/decrement FR backlight level
  - Increment/decrement FR volume level
  - Restore default FR brightness / default FR volume
  - Increment/decrement Farebox backlight level
  - Increment/decrement Farebox volume level
  - (**GAP** — no explicit "restore default" option listed for Farebox brightness/volume, only for FR;
    confirm whether Farebox has a restore-default control too.) (NJT_FRFRP_FS002 p.37)

## Paper Status (5.4.10)
- Shows the **approximate number of tickets** that can be produced from the remaining paper roll.
- Screen **stays displayed until the driver clears it by pressing any key**, then FR returns to the
  **driver menu**. (NJT_FRFRP_FS002 p.38)

## Driver Break (5.4.11)
- Lets the driver temporarily leave the bus with the FR secured.
- On confirming: FR enters **driver break mode**; sends **enter driver break record to CloudFare**
  (GR-3, FRT-1) and an **enter driver break message to the Clever Device** (GR-10); **if connected**,
  the **Farebox is put out of service** (GR-10).
- To resume: driver enters **PIN** and presses **ISSUE**; FR returns to **ticket issue mode**; sends a
  **return-from-break record to CloudFare** (GR-3, FRT-1) and a **return from break message to the
  Clever Device** (GR-10); **if connected**, Farebox is put **back in service** (GR-10).
- If the driver fails to return and another driver needs the bus, an option to **force a sign-off for
  the original driver** is available. (**GAP** — spec doesn't state who can invoke force-sign-off
  (supervisor/audit only? any driver PIN?), nor what audit trail it produces — confirm.)
  (NJT_FRFRP_FS002 p.38)

## Supervisor / Audit Reports (5.4.12)
- Provides supervisors/auditors a **status receipt while the bus is in service**.
- Operator selects **supervisor** or **audit**:
  - Supervisor → prompts for **super ID**.
  - Audit → prompts for **audit ID**.
- Entered ID is **validated against the staff list**:
  - Valid → FR **prints a supervisor or audit report accordingly (GR-12)**.
  - Invalid → **an error is shown**. (**GAP** — no detail on error content/audit event for a failed ID
    entry; confirm whether a failed attempt is logged to CloudFare.) (NJT_FRFRP_FS002 p.38)

## Accept Next Bill (5.4.13)
- **Exact Fare service only.**
- Used when the Farebox cannot identify a bill (e.g. heavily worn note) — driver invokes Accept Next
  Bill to instruct the Farebox to **accept the next presented bill** (GR-10, FM-1).
- Driver selects the **denomination** of the note from a list. Denominations configurable as a subset;
  for **initial deployment**: **$1, $2, $5, $10, $20**.
- The selected denomination is used by the Farebox **only if it cannot determine the bill's value
  itself** — otherwise the Farebox accepts the next bill as **whatever denomination it detects**.
- Selecting this option sends **an Event to CloudFare** (GR-3, FRT-1). (NJT_FRFRP_FS002 p.38–39)

## Clear Bill Jam (5.4.14)
- **Exact Fare service only.**
- Sends a **'clear bill jam' command to the Farebox** (GR-10, JCB-4, FM-1). (**GAP** — no audit/event
  to CloudFare is stated for this action, unlike Accept Next Bill; confirm whether an event is expected
  here too, or whether the absence is intentional.) (NJT_FRFRP_FS002 p.39)

## Suite implications (to action in the FR operator-menu audit)
- **Cancel Ticket**: cover Full-Service-only availability (and confirm/negative-test Exact Fare mode
  per the GAP above); last-1-paper-transaction-only eligibility; OBV transactions excluded; 10-minute
  annulment window boundary (just-inside / just-outside); GR-12 receipt print; CloudFare audit record;
  conditional Clever Device message when connected.
- **Hold**: cover Exact-Fare-only gating; Farebox dump-timeout reset to 60s; confirm menu item is
  absent/disabled in Full Service.
- **Pay Leave**: cover zone range set on entry (once GAP resolved), fare-due display, rider
  class/transaction type mandatory pre-selection, issue vs cancel paths, return to ticket-issue screen.
- **Passenger Count**: cover whichever surface the resolved GAP points to (standalone menu screen vs.
  folded into Driver Totals) — do not test a screen that doesn't exist.
- **Driver Totals**: cover full field list for both Run and Trip views, Trip-only passenger count,
  cancel-key exit back to ticket issue screen.
- **Dump**: cover Exact-Fare-only gating, funds reset to zero, conditional Clever Device message.
- **End of Trip**: cover confirm vs cancel branch; GR-12 trip report print; CloudFare + Clever Device
  messages on confirm; the 1000ms poll-suspend and 1-second IVN timeout-to-event path; suggested-data
  pre-fill truncation at first `00` after message subtype; manual-entry fallback (no response / all-zero
  data); reassignment-alert acknowledgement gate.
- **End of Run**: cover F-key entry mid End-of-Trip flow, confirm vs cancel, end-of-run report,
  CloudFare end-of-shift record, Clever Device End of Run message.
- **Relief**: cover confirm/ISSUE path, relief report, driver sign-off, CloudFare end-of-shift record,
  Clever Device relief message; confirm/resolve the missing-cancel-path GAP.
- **Device Settings**: cover all five listed adjustments (FR backlight/volume inc/dec, FR
  restore-defaults, Farebox backlight/volume inc/dec) and confirm/resolve whether Farebox has its own
  restore-default control.
- **Paper Status**: cover display of remaining-roll ticket estimate and any-key dismissal back to
  driver menu.
- **Driver Break**: cover enter-break (CloudFare + Clever Device messages, Farebox out-of-service if
  connected), PIN+ISSUE resume (CloudFare + Clever Device messages, Farebox back in service), and the
  force-sign-off path once the GAP (who may invoke it, what's audited) is resolved.
- **Supervisor/Audit Reports**: cover both ID types, valid-ID report print (GR-12) for each of
  supervisor/audit, and the invalid-ID error path (plus resolve whether it's audited).
- **Accept Next Bill**: cover Exact-Fare-only gating, the $1/$2/$5/$10/$20 denomination list (and
  configurable subset behaviour if testable), the "Farebox already detected value" precedence rule,
  and the CloudFare Event.
- **Clear Bill Jam**: cover Exact-Fare-only gating and the Farebox command; resolve the missing-audit
  GAP before deciding whether to assert a CloudFare event.
