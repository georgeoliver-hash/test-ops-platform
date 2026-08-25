# FBD-100320 — TID Management, Embedded & Non-Embedded Payment Devices (distilled)

**Source:** `TID Management - Embedded & Non-Embedded Payment Devices (FBD-100320) V5.03` (23 Mar
2023, C. Warnes). Distilled testable facts only — raw spec held locally, not committed.
Covers all Flowbird ticketing devices integrating to the **NMI ChipDNA / P2PE** payment solution.
See also FBD-100353 (older near-duplicate) and FBD-100716 (Revenue Inspection MID override).

## What TID/TK are (invariants)
- **TID** (Terminal ID) + **TK** (Transaction Key) are the payment-terminal credentials; issued by
  **NMI** to Flowbird after MID Boarding (boarding must include the payment-card device serial).
- **1-1** relationships throughout: ticketing device ↔ payment device ↔ TID ↔ TK.
- **Each payment device must have a unique TID+TK.** TK validates the unique TID+TK pairing at NMI.
- Credentials are **allocated to the ticketing device** (keyed on its **serial number**) and
  **pre-configured on TMS**; the device downloads its config during commissioning (no manual entry).

## Device matrix (device → payment device → embedded? → pairing? → NMI Terminal Group)
- **ETM** — Feig — Embedded — no pairing — Group **Travel Charge**
- **PV** — Feig — Embedded — no pairing — Group **Travel Charge**
- **GV** — Feig — Embedded — no pairing — Group **Travel Charge**
- **BV** — Feig — Embedded — no pairing — Group **Travel Charge**
- **TVM (Astreo & Retail Kiosk)** — Ingenico — Embedded — no pairing — Group **TVM**
- **HHD** — Miura M020 — External/Non-embedded — **pairing required (Bluetooth)** — Group **HHD Retailing**
- **POS** — Miura M020 — External/Non-embedded — **pairing required (wired)** — Group **POS**

## Allocation / reallocation rules (testable constraints)
- **TID+TK reallocation is allowed only within the SAME NMI Terminal Group.** A TVM TID/TK can never
  be used on an HHD, etc. — **no cross-Terminal-Group use, ever.**
- Before reallocating to a different ticketing device: **deallocate from the current device first**,
  then update TMS config for **both** old and new device (keyed on serial numbers).
- **Payment-device replacement does NOT change the in-use TID/TK** (embedded or non-embedded); the
  ticketing device keeps its allocated credentials. Transactions on a reused device/payment device
  retain the TID/TK stored on the ticketing device.
- **Hardware cannot cross device types even if the same part**: e.g. an ETM's Feig reader cannot be
  moved into a PV — a replaced Feig may only be reused on ETM devices.
- On device replacement/shutdown, device status is synchronised to **NMI**; new device asset data
  synchronised to **CloudFare**. Broken-beyond-repair devices (and their embedded payment device) are
  **removed from the system**; replaced payment devices are reported to NMI as add-new + remove-old.

## Revenue Inspection MID override
- There is a **MID assignment** against TID/TK maintained by NMI, used by default for settlement.
- When a device is in **"Revenue Inspection Mode"**, the **ABT BOS overrides the MID** with a
  distinct **Inspection MID** to settle penalty/excess (Standard Fare) charges — so retail card
  payments (e.g. T1 HHD via M20) always settle under a **separate, distinct MID** from ABT
  inspections. (Cross-ref FBD-100716 for the inspection solution; note that spec supersedes the "M20
  unlikely" caveat here — inspection is delivered on T1 HHD + Miura M020.)

## Suite implications (all payment devices / ABT-BOS)
- Assert the **device→payment→Terminal Group matrix** exactly (esp. Feig/embedded for ETM/PV/GV/BV;
  M020/paired for HHD & POS).
- Assert **uniqueness** (no duplicate TID/TK) and the **within-Terminal-Group-only** reallocation
  rule; negative-test cross-group reuse is rejected.
- Assert **deallocate-before-reallocate** and that TMS updates **both** device configs.
- Assert **payment-device swap leaves TID/TK unchanged** and transactions remain auditable by TID/TK
  in CloudFare/ServiceNow/WebMIS.
- Assert TID/TK arrive **via TMS config by serial number at commissioning** (no manual keying) — for
  HHD/POS this occurs **after** payment-device pairing.
- Assert **Inspection MID override** separates inspection revenue from travel/retail revenue.
