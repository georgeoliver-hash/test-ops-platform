# FBD-100271 — Legacy Smartcard Transfer Functionality (distilled)

**Source:** `Legacy Smartcard Transfer Functionality (FBD-100271) V5.00` (12 Jun 2023, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Covers two transfer mechanisms: **Multi-Journey transfers** (Metro/Ulsterbus MJ cards) and **Rail Smartcard transfers** (iLink/aLink/Staff/EA on rail).

## The core rule
On first successful validation the card is written with **time of validation + direction of travel**. On re-validation, if it falls inside the transfer window the device records a **transfer (no journey deducted / no second fare)** instead of a journey. Two separate CloudFare/Merit product types back this: **WTS SmartUse** (normal journey) vs **WTS SmartTransfer** (transfer) — linked by matching **Field ID + Group ID** search properties.

## Multi-Journey transfers (REQ-3280.0 + CR027)
- Applies to **ETM (all), PV (all), HHD (all)** — but the **Glider HHD does NOT validate MJ cards** (it only inspects them; if unvalidated + operator opts in, it validates normally). So transfer logic effectively lives on **ETM + Glider PV**.
- **ETM uses the ROUTE 'Transfer Time' property; PV uses the PRODUCT 'Transfer Time' property.** Other devices ignore both.
- **ETM checks (all must pass for a transfer):** route Transfer Time > 0; current stop is inside the **Metro Transfer Zone**; `now ≤ LastValidated + TransferTime`; and — if route **'Transfer Direction of Travel Enabled'** (Boolean, default **true**) — previous direction = current route direction.
- **PV checks:** product Transfer Time > 0; within `LastValidated + TransferTime`; previous direction = the halt's commissioned direction (PV always considers direction).
- Any check fails → **journey deducted**, card updated, **WTS SmartUse** transaction audited. All pass → **no journey deducted**, Transaction Reference Number incremented, **WTS SmartTransfer** transaction audited → CloudFare → MERIT/SmarTrack.
- Trigger = a **business rule** on transfer-enabled smartcard products (currently Metro + Ulsterbus MJ), wired via **'Rapid Issue Sequence Id'**.

## Rail Smartcard transfers (REQ-3470.0 / 3488–3490)
- Applies to **Rail HHD (NIR), GV, PV (NIR)** — all use the **PRODUCT 'Transfer Time'** property.
- Smartcards in scope: **iLink** (all 5 types), **Belfast Visitor Pass** (= iLink product), **aLink**, **Staff & Spouse** (incl. retired/external), and **new EA Pupil/FE** smartcards.
- **Checks:** product Transfer Time > 0; route **Vehicle Type = 'Train'** (Rail; Glider routes = 'Bus'); `now` within `LastValidated + TransferTime`. Pass → **WTS SmartTransfer**; fail → **WTS SmartUse**.
- **Passback always applies and is prioritised over the transfer timer**; the transfer countdown **must be configured longer than the passback time**. **Transfer Time = 0 → no transfers**, everything counts as a journey.

## Config summary (for BOS-setup audits)
- Route level: `Transfer Time` (minutes, 0 = off), `Transfer Direction of Travel Enabled` (bool, default true); Vehicle Type = Train/Bus.
- Product level (WTS SmartUse): `Transfer Time`, `Rapid Issue Sequence Id`.
- **Metro Transfer Zone**: a zone with **ID > 256** (to avoid iLink-zone clashes) listing all stops where MJ transfers apply; granularity is Translink's choice.
- MJ Field ID → card type table: `01`–`06` Metro MJ (City/Extended/Inner × Adult/Child), `09` Ulsterbus MJ Adult, `10` Ulsterbus MJ Child.

## Suite implications
- Cover the **transfer-vs-journey decision** on each device with the right property source: **ETM = route property**, **PV/GV/Rail HHD = product property** — a common misconfiguration risk.
- Cover the **window boundary** (`LastValidated + TransferTime`): just-inside = transfer, just-outside = journey; and **TransferTime = 0** = always journey.
- Cover **direction of travel**: MJ with direction enabled (same dir = transfer, opposite = journey) vs PV always-directional; and the **Metro Transfer Zone** membership check on ETM (in-zone = eligible, out-of-zone = journey).
- Cover **passback prioritised over transfer** (re-tap inside passback window → passback wins, not a transfer).
- Assert the **audit split**: transfer → **WTS SmartTransfer** class (separate Merit/DWH class), journey → **WTS SmartUse**, and TRN reference increment on transfer.
- **Glider HHD MJ non-validation** is a distinct negative case (inspect-only, no journey deduction unless operator opts to validate an unvalidated card).
- Rail transfer scope is exactly iLink/BVP/aLink/Staff+Spouse/EA — do not extend to other cards without spec support.
