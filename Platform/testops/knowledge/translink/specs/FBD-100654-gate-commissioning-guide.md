# FBD-100654 — TFTS Gate System Commissioning Guide (distilled)

**Source:** `FBD-100654 TFTS Gate System Commissioning Guide V1.02` (21 Aug 2024, C. Warnes).
Distilled testable facts only — raw spec (screenshots + credentials) held locally, not committed.
_(Doc's internal number reads FBD-100523; filed under FBD-100654. Login credentials in the source are
deliberately omitted here.)_

## Gate lane architecture (testable component model)
A commissioned lane = **physical gate** (glass + motors + plinths) + **SkyLane TGS interface board**
(drives obstacles + pictograms) + **two GV heads** + **per-lane MicroTik router** (isolates the lane
LAN, connects GV heads to CloudFare via the corporate network).
- **Primary GV head = Entry / unpaid / insecure side**; **Secondary GV head = Exit / paid / secure
  side**. GV heads + interface board talk to each other through the MicroTik router.
- GV heads run **Android** (Axio4 base image `blankAxio4_1105_dtalias`).

## Commissioning steps (durable facts)
1. **Rewire GV green connector:** remove ferrules from the Ethernet twisted pairs on **pins 11-14**
   (they compromise the connection) — cut, re-strip to 10 mm copper, reinsert in the same pins.
2. **SkyLane interface firmware → HF03** (enables the front-most plinth sensors). **Two variants —
   Standard vs Wide (disabled-access) gate — must not be confused.** Login to SkyLane at
   **192.168.0.200**; if version already shows HF03, skip.
3. **Router + interface config** — as **FBD-100653**: WinBox, static WAN per per-lane spreadsheet,
   LAN → 192.168.0.x, set admin password, **port-80 NAT**, SkyLane **eth0 gateway = 192.168.0.1**.
4. **One-wire chip programming (per GV head):** each green connector has a **one-wire chip** storing
   basic peripheral data the GV software needs to load. As-delivered chips are **unprogrammed**, so
   the GV app won't boot / Technician Mode is unavailable → boot an **intermediate 4 GB microSD image**
   (`Intermediate_GV_Commissioning_Image.bin`, written with **ImageUSB**, not Win32DiskImager; needs
   an **external USB card reader**) to reach **Maintenance Mode** and set the minimal parameters:
   **homeLocation = "RA"**, **zoneNo = "128"**. (Boot-mode switch must be **down** to boot from SD.)
5. **Load live GV software:** burn `blankAxio4_1105_dtalias` to **2× 4 GB microSD** (partitions
   `sdcard`/`boot`/`recovery`); copy the **primary** app zip (`pkn_sw.zip` from
   `…gv.TFTS-Live.primary`) to the **P** card's `sdcard` partition and the **secondary** app zip to
   the **S** card. **Primary and secondary images are distinct — do not swap.** First boot self-extracts
   (~20 min); operator must tap **Allow** on 3 Android permission prompts; gate then enters **service**.
6. **Set location** via **Technician card → Location Settings → Change**: Home Location, Stop Location,
   Zone Number, Install Point ID, ID — per the **per-location install spreadsheet** (Google Sheets).
- App version at time of writing **4.0.3.25990** (Google Drive holds only one primary + one secondary
  version at a time — always take the current pair).

## Suite implications (GV / gates — commissioning)
- Primarily a **field procedure** (manual, screenshot-driven, low automated-test value). Useful
  **post-commissioning verification** checks:
  - Both GV heads boot into **service**; **primary=entry/unpaid**, **secondary=exit/paid** roles are
    correct (not swapped).
  - **SkyLane firmware = HF03** and the **correct width variant** (Standard vs Wide) is installed.
  - Minimal one-wire params (**homeLocation, zoneNo**) and the Technician **Location Settings**
    (Home/Stop Location, Zone, Install Point ID, ID) match the install spreadsheet for that lane.
  - Router/interface addressing per **FBD-100653** (SkyLane .200, gateway .0.1, port-80 NAT).
- **Gaps / risks to flag:** manual **primary/secondary image** and **Std/Wide firmware** swaps are
  error-prone (assert role/variant post-commission); commissioning still depends on an **intermediate
  SD image + Maintenance Mode** because one-wire chips ship unprogrammed; **hard-coded credentials**
  in the guide (SkyLane logins, Maintenance user/pass "1"/"1") are a security concern to raise.
