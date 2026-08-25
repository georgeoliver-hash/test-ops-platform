# FBD-100720 — Translink ABT Pilot List (distilled)

**Source:** `FBD-100720 Translink ABT Pilot List Specification v1.00` (24 Sep 2025, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100651 (Glider Tap On Only), FBD-100690 (NIR Tap On Tap Off).

## Purpose
Allow **cEMV tap** testing in the **live/production** environment for Glider Tap-On-Only and NIR Tap-On-Tap-Off without opening the system to the general public. The **Pilot List** is a list of **FEIG tokens** that a device with the pilot list enabled will accept; all other cards are rejected.

## Two TMS device settings (under "Open Payments"), per device type
- **`Enable Registration Mode`** (True/False)
- **`Enable Pilot List`** (True/False)
- **`Pilot List File`** (import field for the binary list, distribution phase only)

These are set via **TMS datasets** and deployed per device type.

## Phase 1 — Registration (build the list)
- Dataset: `Enable Registration Mode = True`, `Enable Pilot List = False`. Deploy to registration device(s); wait for dataset update.
- Tap every EMV card to be enrolled. Device captures the card's **FEIG token** (a unique tokenised identifier) into a **pilot registration file** on-device.
- File is uploaded to **CloudFare Device Log Manager as a zip, ONCE PER DAY at the configured End-of-Day time** (not real-time).
- Arrive personnel retrieve the zip from **Device Logging** in CloudFare, extract per-device registration lists, run the **Pilot List Converter tool** (CSV→binary, then binary→CSV) and sample-check the round-trip, then zip **`pilotlist.dat`** (binary only, no folders).

## Phase 2 — Distribution & testing
- Dataset: `Enable Registration Mode = False`, `Enable Pilot List = True`, import the binary into **`Pilot List File`**. Deploy with a **topology that has ABT enabled** for the device (via the **ABT Type route attribute**). Wait for dataset update.
- **Validation behaviour on a tap (device in pilot mode):** device performs the standard cEMV checks, then **additionally** checks the media's FEIG token against the pilot list:
  - **Token on the list →** proceed down the **normal cEMV flow** (success screens + auditing).
  - **Token NOT on the list →** **reject with the standard rejection screen and perform NO auditing.**

## Suite implications (BOS/ABT suite 30279 + device config)
- Core pilot-list cases (on GV/PV/HHD for Glider/NIR ABT):
  - Registration mode ON + pilot list OFF → tapping enrols the FEIG token into the on-device registration file.
  - Registration file uploads **once/day at End-of-Day**, as a zip, to CloudFare Device Logging (assert timing, not real-time).
  - Pilot list ON: **enrolled card → normal success + audit**; **non-enrolled card → standard rejection, NO audit event**. The "no auditing on reject" is the key negative assertion and easy to get wrong.
  - Requires ABT enabled via **ABT Type route attribute** in topology — a precondition to assert.
- Converter-tool round-trip (CSV↔binary sample-check) is an Arrive back-office step — cover as a tooling/process check, not a device case.
- Depends on the underlying tap solutions (FBD-100651 Glider TOO, FBD-100690 NIR TOTO) for the "normal flow" definition.
