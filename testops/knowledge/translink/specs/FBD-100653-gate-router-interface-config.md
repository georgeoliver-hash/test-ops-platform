# FBD-100653 — TFTS Gate Router & Interface Configuration (distilled)

**Source:** `TFTS Gate Router and Interface Config V1.00` (17 Apr 2024, C. Warnes). Distilled testable
config facts only — raw spec (with screenshots + secrets) held locally, not committed.
_(Doc's internal number reads FBD-100522; filed under FBD-100653. Credentials/passwords in the source
are deliberately omitted here.)_

## Scope / context
- Config of the **per-lane MicroTik router** and the **TGS SkyLane (CO140787_Belfast) interface
  board** at gate install/commissioning. Managed via the **WinBox** tool from a Windows laptop.
- Two goals: (1) **port-forward** so authorised staff reach the gate interface web service from the
  corporate network — a **temporary stop-gap** until GV head software + CloudFare/Station Manager flow
  control are available (needed for the initial **York Street** install); (2) give each lane a
  **known static WAN IP**.

## Network topology / addressing (testable)
- Router default LAN IP **192.168.88.1/24**, DHCP on. Laptop into one of the **4 LAN ports** (not the
  Internet/WAN port); either DHCP or static **192.168.88.199**.
- After Quick-Set the router LAN moves to the **192.168.0.x** family → re-set laptop to
  **192.168.0.199** to reconnect.
- **SkyLane interface board = 192.168.0.200**; its **Ethernet Port 1 (eth0) gateway must be set to
  192.168.0.1** (required for port-forwarding to work).
- **WAN/Internet** per lane: **Mode = Router, Address Acquisition = Static**, with IP/Netmask/Gateway
  from the **per-lane install spreadsheet** (Translink IT provides; unique per lane/location).

## Router changes
- **Quick Set:** set WAN static (above), LAN per screenshot, and **set a router admin password**
  (default is blank — a security risk; a single shared password is used across all lanes). Passwords
  are in the source doc — **not reproduced here**.
- **Port forwarding (IP → Firewall → NAT):** add a NAT rule redirecting **WAN IP : port 80 → gate
  interface board : port 80**, so staff browse to the router WAN IP to reach the lane interface.
  (Router itself is managed over **SSH**, has no web UI, so port 80 is free to forward.)

## Suite implications (GV / gates — commissioning/config)
- This is a **field-config/commissioning** doc, not device functional behaviour — most is
  human-procedure, low automated-test value. Testable/checkable items:
  - Each lane has a **unique static WAN IP** per the install spreadsheet; SkyLane at **.200** with
    gateway **.0.1**; **port-80 NAT** rule present → gate interface reachable from the corporate LAN.
  - Router admin password **is set** (not blank) — a **security check**.
- Flag as **transitional**: direct gate-interface flow control is a **stop-gap**; the target is
  **CloudFare / Station Manager** control once GV head software lands. Do not build long-lived cases
  around the web-interface port-forward path.
- The **shared router password across all lanes** is a security posture worth raising with the team
  (single credential, hard-coded in the guide).
