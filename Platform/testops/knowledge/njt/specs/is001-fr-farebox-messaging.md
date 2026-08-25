# NJT_FRFRP_IS001 — Fare Register and Farebox Messaging (distilled)

**Source:** `NJT_FRFRP_IS001 Fare Register and Farebox Messaging` (NJ Transit FR/Farebox Replacement
Project, v2, 1 Dec 2025, Arrive). Distilled testable facts only — raw spec held locally in
`C:\SystemTestOps\njt-requirements\_text\`, not committed. Page citations use the "Page N" footer
marker nearest the cited text (`NJT_FRFRP_IS001 p.N`). Related: document [1] "NJT Communications
Protocol Description" (defines the base RS485 protocol, Chapter 2, and the generic
ACK/NAK acknowledgement format this spec extends) — not sighted; if its contents matter for
coverage, treat as a separate ingest.

## Scope — what this interface is (p.4, p.6)
- Describes the RS485 message set exchanged between the **Infigo 4 Fare Register (FR)** and the
  **Fast Fare Farebox**, on the existing NJ TRANSIT bus RS485 protocol (`NJT_FRFRP_IS001` p.4, p.6).
- Bus addressing: **FR = device address 0, Farebox = slave address 1** (p.6).
- All messages share a common frame: `01` (SOM) `10` (slave addr/message type) `LEN` `MSUBTYPE`
  `[data]` `CRC` (p.8 onward, every message).
- Acknowledgement messages (plain ACK `01 16`, and NAK) follow the format in document [1] — not
  redefined here (p.7).

## Message catalogue (p.7)
FR → Farebox (subtype hex): Poll `00`, FB Information request `10`, FR ID Information `11`, Enter
Service `12`, Exit Service `13`, Decrement Funds `20`, Bill Reclassify `21`, Adjust
Backlight/Volume `22`, Hold `23`, Bill Unjam `24`, Unlock Door `30`, Program Farebox ID `31`.
Farebox → FR (subtype hex): FB Status `08` (also serves as the ack in place of the generic
ack — p.20), FB IDs `18`, Increment Funds `28`, Funds Dumped `29`, Bill Rejected `2A`, Farebox
Vaulted `2B` (p.7).

## FR → Farebox messages

- **Poll (`10 00`, p.8):** the FR's routine query. Allowed responses: ACK, NAK, FB Status,
  Increment Funds, Funds Dumped, Bill Rejected, or Farebox Vaulted — i.e. the Farebox can piggyback
  any of its unsolicited event messages onto a poll response rather than a bare ack.
- **FB Information request (`10 10`, p.9):** FR asks for current Farebox + cashbox IDs. Triggered
  by three events: **FR power-on (including after nightly reboot)**, **after FR sends "Program
  Farebox ID"**, or **after the Farebox Status "cashbox" bit transitions 1→0** (cashbox
  re-inserted). Allowed responses: FB IDs or NAK.
- **FR ID Information (`10 11`, p.10):** FR sends its own serial number + version string so the
  Farebox can track which FR it's paired with. Triggered when the FR **detects comms has been
  established** — explicitly including **"after a nightly reboot or comms loss/recovery event"**.
  Allowed responses: ACK, NAK, or FB Status.
- **Enter Service (`10 12`, p.11):** sent when FR is **signed on to an Exact Fare service**; carries
  driver number, route, trip, bus number (all BCD). **Driver number field is 8 digits wide
  (future-proofed) but the system currently only supports 6-digit driver numbers** (footnote,
  p.11). Allowed responses: FB Status or NAK.
- **Exit Service (`10 13`, p.12):** sent when FR **exits revenue service mode** (Exact Fare
  service). No payload beyond subtype. Allowed responses: FB Status or NAK.
- **Decrement Funds (`10 20`, p.13):** sent when the driver issues a product requiring a cash
  value — **not sent for flash pass or OBV validation** (i.e. no-cash-value products bypass this
  message entirely). Carries Product Value and Amount Accepted (cents, BCD). **Product value = 0**
  signals a driver-invoked "dump". Farebox derives a **short-fare "accept"** when Amount Accepted <
  Product Value (sample shows exactly this: accepted $4.00 vs product $4.80). Allowed responses: FB
  Status, ACK, or NAK.
- **Bill Reclassify (`10 21`, p.14):** driver selects "accept next bill" on the FR; instructs the
  Farebox to accept the next presented bill, using the given dollar value **if the value can't be
  read from the bill itself**. Allowed responses: FB Status, ACK, or NAK.
- **Adjust Backlight/Volume (`10 22`, p.15):** driver selects increment/decrement of Farebox
  backlight or volume from the FR. Payload: target (1=Backlight, 2=Volume) and direction
  (1=Increment, 2=Decrement). Allowed responses: FB Status, ACK, or NAK.
- **Hold (`10 23`, p.16):** driver selects "Hold" on the FR; instructs Farebox to **reset its dump
  timeout to 60 seconds (configurable)**. Allowed responses: FB Status, ACK, or NAK.
- **Bill Unjam (`10 24`, p.17):** driver selects "Clear Bill Jam"; instructs Farebox to run its bill
  unjam procedure. Sample sequence shows the Farebox reporting **FB Status with the bill-validator
  "Jammed" bit set**, then — once the unjam completes — a subsequent Poll returns FB Status with the
  bit cleared. Allowed responses: FB Status, ACK, or NAK.
- **Unlock Door (`10 30`, p.18):** a **special user** selects unlock-door on the FR; instructs the
  Farebox to unlock the cashbox access door, carrying a 5-digit unlock code (BCD). Sample sequence
  shows the FB status door-unlocked bit only flips on a **subsequent poll**, not instantaneously in
  the direct response — i.e. door state should be asserted via poll/FB-Status, not assumed from the
  Unlock Door ack alone. Allowed responses: FB Status, ACK, or NAK.
- **Program Farebox ID (`10 31`, p.19):** a **special user** selects the option to program the
  Farebox ID; instructs Farebox to update its stored ID number (6-digit BCD). This is also one of
  the three triggers for a subsequent FB Information request (p.9). Allowed responses: FB Status,
  ACK, or NAK.

## Farebox → FR messages

- **FB Status (`10 08`, p.20–22):** Farebox's state report; **doubles as the acknowledgement**,
  sent instead of a plain ack in normal operation. Three status bytes, each bitmapped:
  - **Coin/Bill status byte** (p.20–21): cashbox coin/bill fill level (≥75% full), coin/bill area
    full, coin validator jammed/offline, bill validator jammed/offline (bits 7→0).
  - **Operating status byte** (p.21): Revenue mode (In/Out of Service), maintenance jumper present,
    currently-probing flag, coin-bypass active, time/date invalid, farebox-number missing,
    operating-parameters missing (bit 0 unused).
  - **FB status byte** (p.22): cashbox door unlocked/open, cashbox removed, top cover opened,
    **door open ≥ 3 minutes** flag (bits 3–0 unused).
  - No response is defined to an FB Status message (it is itself the ack/event, p.22).
- **FB IDs (`10 18`, p.23):** Farebox's reply to an FB Information request; carries 6-digit Farebox
  ID + 6-digit cashbox ID (both BCD). Allowed responses: ACK or NAK.
- **Increment Funds (`10 28`, p.24):** sent when funds are inserted; carries a **Bill/Coin
  indicator** (0x01 coins, 0x10 bills, 0x11 both) and the increment amount in cents **since the
  last increment sent** (i.e. a delta, not a running total). Allowed responses: ACK or NAK.
- **Funds Dumped (`10 29`, p.25):** sent when funds are dumped (Farebox resets its available-funds
  total to $0.00); the FR is expected to **reset its own available-fund tracking to $0.00** in
  response. Allowed responses: ACK or NAK.
- **Bill Rejected (`10 2A`, p.26):** sent when the Farebox rejects an inserted bill; spec notes this
  "may be used by the FR to prompt the driver to use the accept-next-bill function" (i.e. links
  directly to Bill Reclassify, `10 21`, as the expected operator recovery path — a plausible
  scenario/case pairing, not stated as mandatory). Allowed responses: ACK or NAK.
- **Farebox Vaulted (`10 2B`, p.27–28):** sent after the Farebox has been probed and the cashbox
  removed; details cumulative cash counted since the last cashbox replacement, broken out per
  denomination (1¢/5¢/10¢/25¢/$1 coin; $1/$2/$5/$10/$20 bill counts, all HEX) plus a coin-bypass
  indicator. Allowed responses: ACK or NAK.

## Timing / error handling — what the spec does and does NOT define
- No explicit poll interval, timeout value, or retry/backoff count is given anywhere in this
  document for the FR↔Farebox RS485 link.
- **GAP** — no defined behaviour for **sustained non-response from the Farebox to a Poll** (no
  ACK/NAK/FB Status at all) — no escalation, alarm, or fallback state is specified in this document.
  This is the FR↔Farebox link specifically, distinct from the back-office "Comms Locked" functional
  state in FS002 (see cross-reference below) — confirm with the requirements owner whether that
  behaviour is specified elsewhere (e.g. document [1], not sighted) or is genuinely undefined.
- **GAP** — CRC algorithm/width is referenced (`XX XX CRC` on every message) but never specified in
  this document; presumably defined in document [1]. Do not assume a specific CRC variant without
  that source.
- The one explicit "recovery" behaviour defined is **FR ID Information (p.10)**: the FR re-announces
  itself "after a nightly reboot **or comms loss/recovery event**" — this is the closest thing to a
  documented comms-failure hook in this spec, and it is a FR-initiated re-handshake, not a
  Farebox-initiated failure report.
- **GAP** — no message type exists for the Farebox to proactively report "I am not responding" (by
  definition — a completely silent Farebox is only detectable by the FR polling and getting nothing).
  Confirm how the wider system (back-office / driver display) surfaces this to the driver — not
  covered in this document.

## Suite implications
- **Cross-reference, don't duplicate:** `knowledge/njt/specs/fs002-functional-states.md` §3.1.2
  covers **"Comms Locked"** — that is the FR↔**back-office** link going down for a configurable
  period. This document's FR↔**Farebox** RS485 link is a *different* channel with *no* documented
  lock/timeout state. Keep these two "communication loss" concepts separate in case titles/tags —
  do not fold Farebox-poll-silence scenarios into Comms-Locked cases.
- Cover each of the 12 FR→Farebox and 6 Farebox→FR message types as distinct scenarios (message
  sent, expected response set, and — where the spec calls it out — the follow-on state check via a
  subsequent Poll): Unlock Door and Bill Unjam both explicitly need a **follow-up poll** to observe
  the state change, not just the immediate response.
- Cover the **three FB-Information-request triggers** (power-on/nightly reboot, post-Program-Farebox-ID,
  cashbox-bit 1→0 transition) as three separate trigger scenarios, since they're functionally
  distinct paths to the same message.
- Cover **Decrement Funds short-fare ("accept")** — Amount Accepted < Product Value — and the
  **driver "dump" case** (Product Value = 0) as explicit boundary scenarios; confirm exact short-fare
  threshold/UI behaviour isn't assumed beyond what's stated here.
- Cover **FB Status bit-level assertions** for each of the three status bytes (coin/bill fill,
  jam/offline, revenue mode, maintenance jumper, cashbox door/removed/top-cover/door-open-3min) —
  these are the richest source of device-state test points in this spec and are easy to under-cover
  if only the "happy path" FB Status (all-zero, in-service-all-ok) is exercised.
- **Bill Rejected → Bill Reclassify** operator-recovery flow is worth one linking scenario (bill
  rejected, driver invokes accept-next-bill, Farebox subsequently accepts) since the spec explicitly
  suggests this pairing (p.26) even though it isn't mandated.
- Flag the two GAPs above (silent-Farebox timeout/escalation; CRC definition) to the gap register per
  the repo's Q&A-loop rule — they affect whether "Farebox failure" / comms-loss suites for this
  interface can be written with confidence, or must carry visible `GAP` markers until answered.
- **6-digit driver number** system limit (despite an 8-digit wire format) is a concrete boundary case
  worth a dedicated scenario (7/8-digit input rejected or truncated — confirm which, since the spec
  only says "will only support 6 digit", not the failure mode for longer input — mark as a further
  **GAP** if no case currently covers it).
