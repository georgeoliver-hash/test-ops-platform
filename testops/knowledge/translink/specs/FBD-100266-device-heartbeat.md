# FBD-100266 — Device Heartbeat Functionality & Reporting (distilled)

**Source:** `Device Heartbeat Functionality & Reporting (FBD-100266) V3.00` (20 Nov 2020, S. James).
Distilled testable facts only — raw spec held locally, not committed.
Drivers: REQ-0503.0 (regular operational-state reporting) + CONOPS N14.x.

## Scope — which devices
- **All device types** call in to CloudFare (ETM, POS, TVM, HHD, and validators). Heartbeat is a
  back-office/CloudFare reporting feature, not device-specific new behaviour.
- Reporting/monitoring surface is **CloudFare** (Comms Monitor + Asset Manager + Dashboard).

## Heartbeat mechanism — the agreed solution (Method 2)
- **Chosen mechanism = reuse the existing Staff List Refresh check.** Every device already performs a
  **Staff List Refresh check every 15 minutes** regardless of state (signed in, docked, undocked,
  signed out, locked). Method 1 (dedicated Device Status heartbeat messages) was **rejected** on
  performance grounds.
- The staff-list call-in is the heartbeat: it happens **whether or not the device is signed on** and
  **without any ticket transaction**.
- **Not configurable by Translink** — the 15-minute period is fixed (a known deviation from the
  original "configurable by Translink" requirement).
- Historical reference periods (non-binding): attended devices (ETM) ~daily; unattended devices
  (TVM) ~every 2 hours. The delivered solution supersedes these with the 15-min staff-list cadence.

## CloudFare reporting rules (testable)
- New Comms Monitor message type **`StaffList`**. Receiving one updates the **Last Communication**
  time and **resets Hours-Since-Last-Communication to zero**; it flows into Asset Manager and the
  Devices Last Seen report.
- Comms Monitor column changed from **"Days Since Last Communication" → "Hours Since Last
  Communication"**; user can free-type a number of hours to filter devices not seen in ≥ N hours.
- "Last Communication" is updated by **any** standard message (transaction or event) **or** a staff
  list request.
- New **Dashboard tile**: configurable by **device type(s)** and by **hours since last comms**, where
  hours is restricted to the fixed set **{1, 3, 6, 12, 24, 48, 72}**. Tile columns: Device ID, Device
  Type, Location, Device Category, Hours Since Last Communication; **sorted low→high**.
- Dashboard tile shows **only unblocked devices** (devices blocked for repair/lost are excluded).
- Clicking a device (in tile or Comms Monitor) opens its **Asset Manager** page.

## Suite implications (ABT-BOS / all devices)
- Assert **every device type** updates CloudFare Last Communication at least every **15 min** via the
  staff-list check, **even when signed out / no sales** — this is the core heartbeat assertion.
- Assert a `StaffList` message **resets Hours-Since-Last-Communication to 0** and updates Asset
  Manager + Devices Last Seen.
- Assert the Dashboard tile honours the **fixed hours set {1,3,6,12,24,48,72}**, filters by device
  type, sorts low→high, and **hides blocked devices**.
- Negative: a **blocked** device must **not** appear in the tile even if overdue.
- Note the **known limitation** for coverage classification: period is **not Translink-configurable**
  (do not write a case expecting configurability).
