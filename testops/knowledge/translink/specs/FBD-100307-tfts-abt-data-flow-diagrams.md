# FBD-100307 — TFTS ABT Data Flow Diagrams (distilled)

**Source:** `CloudFare - ABT Data Flow Specification (FBD-100307) V7.01` (18 Apr 2023, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Diagram-led spec; the **triggers/criteria text** around each data-flow diagram is the testable part
(sequence diagrams themselves are in the source `.docx`/`.pdf` only). Related: FBD-100389 (scenarios),
FBD-100658 (audit fields), FBD-100698 (fares-engine calls).

## Tap / media model
- ABT media: **cEMV** (bank card, phone, watch) or **issued ABT smartcard**.
- Transaction types: **Tap On Only (TOO)**, **Model 1 (KFT — Known Fare Transaction)**, **Tap On Tap Off (TOTO)**.
  - TOO: single tap; device stores furthest possible travel (within zone) + fare; back office prices it.
  - Model 1 (KFT): a ticket is bought on-device with cEMV but **payment is deferred**; back office does authorisation + settlement.
  - TOTO: tap-on + tap-off compiled into one journey; **missing tap-off → 'Maximum' fare** per business rules.

## cEMV TOO — success vs failure (assertable criteria)
- **Success (all must hold):** location enabled for TOO; a **future alighting stop enabled for TOO** exists; a valid fare exists for boarding/alighting; card readable; valid scheme; not expired; **passed ODA**; not on **BIN blocking list**; not on **Deny list**; **outside passback**. → travel permitted; txn stored for collection.
- **Failure Mode 1 — card unreadable at all:** no response (device never saw a card).
- **Failure Mode 2 — card-level reject:** not read properly / invalid scheme / expired / ODA fail / on BIN list / on Deny list / within passback. → travel not permitted; **txn + declined reason stored**.
- **Failure Mode 3 — topology/fare reject:** route not enabled for TOO / boarding not in ABT TOO zone / no future stop in ABT TOO zone / no valid fare. → **card reader not even enabled** (no passenger response).
- Audited TOO transaction records: Type=TOO, **Boarding** = tap location, **Alighting** = last stop on route within the ABT TOO zone, **Fare** = flat fare from the ABT-TOO-product rule (fares engine), **Zone** = ABT TOO Zone Id, **Declined Reason** on Mode-2 failure.

## Key thresholds & timings (high-value assertions)
- **Late tap:** accepted if < **14 days** after original tap date (treated as **late tap**); ≥ 14 days → **expired tap**. (Matches FBD-100389 S3.)
- **Capping rules cannot take effect the same business day** — earliest is the **next business day**.
- **Deny list:** ABT regenerates a **Full list (max 100,000 entries)** and a **Delta** every **15 min**; devices pull full ≥ once/day and delta every 15 min → a newly added token can take **just under 30 min** to start being denied.
- **BIN blocking list:** up to **2,500 BINs**, Flowbird-managed; devices refresh ≥ once/day.
- **Debt recovery / re-authorisation** removes a card from the deny list; three triggers: **web-initiated**, **automated** (scheme rules), **tap-initiated** (tap by an already-denied card → near-real-time attempt; if the online auth approves, card removed **within 15 min**). Automated re-auth also attempts to collect the original transaction value.
- **Refunds:** operator marks ≤ transaction value, supervisor authorises; sent to **NMI**; **only one refund per transaction**; **refunds are NOT sent to MERIT**.

## To MERIT (both TOO and Model 1)
- Data forwarded uses the **original tap date/time**, **Fare paid** (may be zero), **Full Fare cost** (uncapped), service, boarding/alighting, Product Type/Class (the ABT TOO product), **Payment method = OpenPayment** (TOO) / **Card** (Model 1).
- **Model 1 txn is sent to MERIT regardless of whether ABT payment later succeeds.** Debt-recovery/re-auth outcomes send **no** data to MERIT.

## Suite implications (this note is the backbone for the ABT/BOS suite, 30279)
- Encode the **three TOO failure modes** as distinct cases — especially **Mode 3 (reader disabled, no response)** vs **Mode 2 (declined reason stored)**; a common conflation.
- Assert the **timing/threshold constants**: 14-day late/expired boundary, next-business-day capping activation, 100k deny-list cap, ~30-min deny propagation, 15-min tap-initiated removal, 2,500-BIN cap. These are gaps most device suites never check.
- Cover **TOTO missing-tap-off → Maximum fare**, and **Model 1 KFT deferred settlement** (txn to MERIT even if payment fails).
- Assert **MERIT payload**: original tap date/time, Fare paid vs Full Fare cost, payment method **OpenPayment** (TOO) vs **Card** (Model 1); and that **refunds/debt-recovery never reach MERIT**.
- Diagrams (sequence flows) live only in the source doc — for detailed step ordering, point testers to the `.docx`/`.pdf` in `dev/translink-requirements/`; do not reconstruct from memory.
