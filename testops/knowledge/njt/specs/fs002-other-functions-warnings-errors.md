# FS002 — Other Functions & FR Operation Warnings/Errors (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf` — sections **5.5 Other
Functions** and **5.6 FR Operation Warnings and Errors** (source text lines 5020–6356). Distilled
testable facts only — full spec held locally, not committed. Requirement tags (`GR-10`, `GR-3`,
`FRT-1`, `FF-2`, `GR-12`, `CR...`) are cited verbatim from the source where present next to a rule.

## 5.5.1 Spotter Display (GR-10)
- FR sends a **12-character string** to a bus-mounted Spotter Display over **RS485**, for every
  successful transaction (including cancel). (p.39)
- Standard transaction string: **passenger count (3 chars) `<space>` class (3 chars) `<space>`
  transaction type (4 chars)** — e.g. `023 SEN CASH`. (p.39)
- **MyTix transactions:** the space between class and transaction type is replaced with `*`
  (asterisk). (p.39)
- **PayGo and FarePay transactions:** the space between class and transaction type is replaced with
  `*`, AND the transaction type field is forced to literal `CARD` (e.g. `*CARD`). (p.39)
- **Cancel transaction:** passenger count (3 chars) `<space>` `Cancel` — e.g. `022 Cancel` (padded).
  (p.39)
- **Empty transaction string case** (e.g. "non payment pass"): only the passenger count is sent,
  rest of the 12-char field blank — e.g. `025` + trailing spaces. (p.39)
- Passenger count rules: zeroed at start of each trip; incremented per transaction; **NOT**
  incremented for override / override-transfer transactions; decremented on ticket cancellation,
  **except** cancelling an override or override-transfer transaction (no decrement). (p.39)
- **GAP** — exact spec of "class" 3-character codes (beyond `SEN` example) not given in this range;
  confirm the full code table before asserting exact string content in a case.

## 5.5.2 Sum Function
- Available **only in Full Service mode**. Lets the driver confirm a running total with the
  passenger before any receipts print. (p.39)
- Flow: driver enters product parameters for the first product, presses **S (sum) key**; repeats
  entry + sum key for further products as required. Transaction count and combined fare total show
  in the product-details area of the ticket-issue screen. (p.40)
- On pressing **ISSUE**, all summed products are issued in sequence. (p.40)
- Each transaction in the sum is recorded **separately**. (p.40)
- Only the **last** ticket in the sum sequence can be cancelled. (p.40)
- **Maximum of 10 transactions** within a single Sum function use. (p.40)
- **GAP** — behaviour if the driver attempts an 11th sum entry (reject / error message / silently
  capped) is not stated in this range; confirm on the live system.

## 5.5.3 Paper Loading
- Sequence: driver opens lid → removes old roll → inserts new roll → closes lid → FR **prompts a
  test print** → test print is conducted → on successful test-ticket print, FR returns to whatever
  state it was in when the roll was inserted. (p.40)
- **GAP** — behaviour if the test print itself fails (e.g. still jams/mis-feeds) is not covered in
  this range; confirm before writing a negative-path case.

## 5.5.4 Bus Inspection (GR-10, GR-3, FRT-1, GR-12)
- Driver selects the Bus Inspection feature and is prompted to enter a **6-digit police operator
  ID**. (p.40)
- **Valid entry (≤6 digits):** an event is sent to CloudFare (GR-3, FRT-1), a Police Inspection
  record is sent to the **Clever Device** (GR-10), and — if the option is set — a receipt is printed
  (GR-12); FR then returns to the ticket-issue screen. (p.40–41)
- **Invalid entry (>6 digits):** FR issues an **error beep**, the entry prompt remains on screen to
  allow re-entry of a valid number. (p.41)
- Driver can **exit the prompt via the Clear key**. (p.41)
- **GAP** — no stated behaviour for a non-numeric / empty submission distinct from ">6 digits"; and
  no stated content/format of the printed receipt. Confirm before authoring exact assertions.

## 5.5.5 Colour of the Day (FF-2)
- FR shows a **3-character text string** on the ticket-selection screen representing the colour that
  valid rail barcoded flash passes must display that day. (p.41)
- The Colour-of-the-Day calendar is sent to the FR from the back office; FR uses it to populate the
  display **at duty sign-on**. (p.41)
- FR applies the colour by **calendar day** — it will **update the colour display at midnight** if
  the FR is currently in service (i.e. mid-shift rollover, not just at next sign-on). (p.41)
- **GAP** — the actual colour/day mapping table and the 3-character code values are not in this
  range; needed to assert specific display strings.

## 5.5.6 Disable Receipt Printing
- A **route attribute** can disable receipt printing; when set, the FR prints **no receipts**. (p.41)
- **Exception:** fare media for a transaction (transfer, CTT, or CRT) is **always** printed even with
  receipts disabled. (p.41)

## 5.5.7 Fare Mode
- Fare mode for a route (**Exact** or **Full Service**) is determined by a **route attribute**.
  (p.41)
- **GAP** — no detail here on how/where the attribute is configured or on operator-visible indication
  of current mode outside of farebox-failure fallback (see 5.6.6); cross-check against other spec
  sections if asserting mode-display behaviour generally.

## 5.5.8 GPS
- The Infigo 4 FR has an internal GPS module; current latitude/longitude is recorded in
  **transaction and event records** sent to CloudFare (FRT-1). (p.41)
- **GAP** — no stated behaviour for GPS unavailable/no-fix (blank field? last-known? error flag?);
  confirm before asserting a specific value in that case.

## 5.5.9 AutoLog off
- FR automatically logs off the current driver after **no activity for a configurable period**,
  initially set to **120 minutes** — purpose: prevent unauthorised access if a driver leaves the bus
  without logging off. (p.41)
- At timeout, FR displays a **warning screen for 10 seconds** with an **audio warning** that logoff
  is imminent, and the driver may **cancel the operation** during that window. (p.41)
- **GAP** — exact wording of the warning screen, and confirmation of what actually happens if the
  driver does *not* cancel (implied: forced logoff to what screen/state) are not stated in this
  range; confirm before asserting post-logoff screen state.

---

## 5.6 FR Operation Warnings and Errors

### 5.6.1 Memory Low
- Error message displayed when **90%** of audit-data storage memory is used. (p.42)
- Driver clears the message by **pressing any key**. (p.42)

### 5.6.2 Memory Full
- Error message displayed when **100%** of audit-data storage memory is used. (p.42)
- FR **enters "Out of Service"** functional state. (p.42)
- Recovery: after a **successful communications session** uploads the unsent data, FR **returns to
  the idle screen** (automatically, not via a keypress). (p.42)

### 5.6.3 Paper Low
- Error message displayed when calculated remaining paper is below a **configurable threshold** of
  tickets. (p.42)
- Driver clears the message by **pressing any key**. (p.42)
- **GAP** — default/typical threshold value not stated in this range.

### 5.6.4 Paper Out
- "Paper Out" error message displayed when the roll has run out. (p.42)
- Operator **must load a new roll** before any further transactions can be processed. (p.42)
- If the FR is idle with no paper loaded, **only special users** can log in to the machine (regular
  driver login blocked). (p.42)
- **GAP** — "special users" is not defined in this range (role/permission level); confirm against
  user-role knowledge before writing the login-restriction case.

### 5.6.5 Paper Jam
- Paper-jam error message displayed on detection. (p.42)
- Operator must **release the jam and press Enter** before ticket issuing can continue. (p.42)

### 5.6.6 Farebox Failure (GR-10)
- Applies **Exact mode only**. A Farebox Failure occurs when either (a) communications with the
  Farebox is lost, or (b) the Farebox reports a fault/degraded condition to the FR. (p.43)

#### 5.6.6.1 Communication loss
- Triggered if FR gets **no reply from the Farebox for 10 consecutive polls**. (p.43)
- FR then **briefly pauses communications** to let the Farebox recover; during this pause it
  displays **"standby"** and **blocks all actions**. (p.43)
- After the pause, FR **restarts polling**:
  - If comms restore **within 2 seconds** → normal operation resumes. (p.43)
  - If comms do **not** restore within 2 seconds → treated as a **farebox disconnection**; FR
    **reverts to 'Full Service' mode**, and a message is shown to the driver alerting that the
    operational mode has changed. (p.43)
- If **10 consecutive NAKs** are detected, this **also initiates 'standby mode'** (same as the no-reply
  case above), with the same restore/lost outcomes. (p.43)
- Events sent to CloudFare (GR-3, FRT-1): on **Standby occurring**, on **comms loss occurring**, and
  if **6 consecutive NAKs** have been received from the Farebox. (p.43)
- **GAP** — exact wording/format of the driver-facing "mode changed" message, and the precise
  relationship between the "6 consecutive NAKs" event trigger and the "10 consecutive NAKs → standby"
  trigger (i.e. is the 6-NAK event a separate, earlier warning?) is not fully disambiguated in this
  range; confirm before writing a strict sequencing assertion.

#### 5.6.6.2 Communication Restore
- After a comms loss is registered, FR **automatically retries**: polls the Farebox for **2 seconds,
  once per minute**. (p.43)
- If the Farebox responds, the system **reverts back to Exact fare mode**. (p.43)

#### 5.6.6.3 Farebox Fault
- FR **reverts to 'Full Service' mode** if the Farebox reports it is in a state where it **cannot
  count all money** — e.g. a coin/bill receiver error, or the Farebox has been put into **"coin
  bypass"** mode. (p.43)
- On fault detection: an **Event is sent to CloudFare** (GR-3, FRT-1) and a **Fault Message is sent to
  the IVN**. (p.44)
- **GAP** — no stated recovery path back from Farebox Fault to Exact mode (contrast with
  Communication Restore's explicit auto-retry poll); confirm whether fault-recovery is automatic,
  requires a farebox reset event, or requires manual/driver action.

## Suite implications
- **Spotter Display string composition** — cover each of the 4 string variants: standard
  (`ccc SEN CASH`-style), MyTix (`*` separator), PayGo/FarePay (`*` + forced `CARD`), Cancel
  (`Cancel` literal), and empty-transaction (count-only). Also cover passenger-count
  increment/decrement rules incl. the override/override-transfer exceptions (no increment on issue,
  no decrement on cancel).
- **Sum Function** — cover: Full-Service-mode gating (not available in Exact mode), sum-key flow
  building up to 10 products, running total display, ISSUE fires all in sequence, only-last-cancelable
  rule, and the 10-transaction cap (boundary case at 10 and the gap on the 11th attempt — flag as
  open question).
- **Paper loading** — cover the full lid-open → new roll → lid-close → test-print prompt → return-to-
  prior-state happy path; flag the failed-test-print recovery as a gap to resolve.
- **Bus Inspection** — cover valid-ID happy path (CloudFare event + Clever Device record + optional
  receipt + return to ticket-issue) and invalid->6-digit path (error beep, prompt persists, Clear-key
  exit). Flag receipt-content and non-numeric-input handling as gaps.
- **Colour of the Day** — cover display populated at sign-on AND the mid-shift **midnight rollover**
  while in service — this second behaviour is easy to miss/under-test. Flag the colour/day mapping
  table as a gap needed for concrete value assertions.
- **Disable Receipt Printing** — cover the route-attribute-off case plus the transfer/CTT/CRT
  always-prints exception explicitly (don't let a blanket "no receipts" case wrongly assert those are
  suppressed too).
- **Fare Mode** — cover route-attribute-driven Exact vs Full Service selection at the "static
  configuration" level; deeper mode-transition behaviour is covered under Farebox Failure below.
- **GPS** — cover that lat/long appears on transaction and event records sent to CloudFare; flag
  no-fix/unavailable handling as a gap.
- **AutoLog off** — cover the 120-minute default idle timeout, the 10-second warn+audio window, and
  the cancel-the-logoff path. Flag the "what happens post-timeout if not cancelled" screen/state as a
  gap.
- **Memory Low / Full** — cover the 90% warning (any-key clear) and the 100% Out-of-Service state
  distinctly, including Full's automatic return-to-idle only after a successful comms upload (not a
  keypress) — a common suite-writing mistake is to treat both as any-key-cleared.
- **Paper Low / Out / Jam** — cover threshold warning (any-key clear), Out blocking further
  transactions and restricting idle-mode login to "special users" (flag role definition as a gap),
  and Jam requiring physical release + Enter before continuing.
- **Farebox Failure / Communication loss** — this is the densest area and highest-risk for missing
  coverage: cover (a) 10-consecutive-no-reply → standby display + action lockout; (b) 2-second
  recovery → resume normal; (c) failure to recover in 2s → Full Service fallback + driver-alert
  message; (d) 10-consecutive-NAK path into standby with the same two outcomes; (e) CloudFare events
  for standby, comms-loss, and 6-consecutive-NAKs (flag the 6-vs-10 NAK relationship as a gap to
  resolve before asserting exact event sequencing).
- **Communication Restore** — cover the background 2-second-per-minute repoll and revert-to-Exact-
  mode on success.
- **Farebox Fault** — cover Full-Service fallback on "cannot count all money" (coin/bill error or
  coin-bypass mode), CloudFare event + IVN fault message on detection; flag the missing
  fault-recovery path back to Exact mode as a gap requiring engineer input.
