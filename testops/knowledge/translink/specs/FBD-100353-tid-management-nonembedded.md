# FBD-100353 — TID Management, NonEmbedded Payment Devices (distilled)

**Source:** filed under FBD-100353 but the document is `TID Management - Embedded & Non-Embedded
Payment Devices V5.0` (10 Feb 2022 / rev 4.1 content, C. Kiraz). Distilled testable facts only — raw
spec held locally, not committed.

> **This is an OLDER near-duplicate of FBD-100320.** The FBD-100353 folder holds the earlier
> (V4.1/V5.0) revision of the same TID Management document; **FBD-100320 V5.03 supersedes it.**
> Author from **[FBD-100320](FBD-100320-tid-management.md)**; use this note only for the
> non-embedded (HHD/POS) emphasis the folder title implies.

## Non-embedded devices (HHD & POS) — the specifics
- **HHD** and **POS** use the **external Miura M020** payment device (non-embedded).
  - **HHD ↔ M020 = Bluetooth pairing**; **POS ↔ M020 = wired connection**.
  - Pairing is **required during commissioning** (unlike embedded Feig devices).
- NMI Terminal Groups in this (older) revision: **HHD → "HHD"**, **POS → "POS"** (FBD-100320 V5.03
  refines HHD to **"HHD Retailing"** and POS device as **Way6**). Treat FBD-100320 as authoritative.
- Commissioning order for non-embedded: download TID/TK config from TMS (by serial) → **pair** new
  ticketing device with payment device → sync device–payment–TID–TK mapping to NMI → asset sync to
  CloudFare.

## Non-embedded replacement scenarios (testable)
- **Ticketing device (HHD/POS) replaced:** old device disconnects + syncs status to NMI; new device
  downloads its own TID/TK config by serial and **pairs** with a payment device. No restriction on
  pairing the new device with an existing payment device, but the **new device's allocated TID/TK**
  become the in-use credentials.
- **Non-embedded payment device (M020) replaced:** new M020 is paired to the existing ticketing
  device; **TID/TK unchanged**; NMI informed of add-new + remove-old. Repaired (not replaced) M020 =
  no TID/TK change.
- Reallocation constraints identical to FBD-100320: **same NMI Terminal Group only**, **deallocate
  before reallocate**, update TMS for both devices.

## Suite implications (HHD / POS)
- Assert **pairing** is part of HHD/POS commissioning (BT for HHD, wired for POS) and that TID/TK come
  from TMS by serial, **not** manual entry.
- Assert **M020 swap leaves TID/TK unchanged**; ticketing-device swap uses the **new** device's
  credentials.
- **Prefer FBD-100320 V5.03** for authoritative Terminal Group names (HHD Retailing / POS-Way6) and
  the Inspection-MID override — do not double-author cases across both FBD ids.
