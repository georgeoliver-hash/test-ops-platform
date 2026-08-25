# FBD-100304 — TFTS System Diagram Roadmap (distilled)

**Source:** `TFTS System Diagram Roadmap (FBD-100304) V3.00` (11 May 2023, S. James).
Distilled testable facts only — raw spec (diagram-only) held locally in `dev/translink-requirements/`, not committed.
"Living document, subject to change." Use for topology/CR sequencing context, not hard assertions.

## What it is
A set of full-system architecture diagrams, one per project phase, showing components, hosting boundaries and data paths. Useful as the **map** that ties the other specs together (which device talks to what, and when each capability lands).

## Phase roadmap (device/capability sequencing)
- **Existing Baseline** — on-prem CloudFare; Way6S ETM, Axio4S PV live.
- **Project 1b — CloudFare SaaS** — back office migrates to AWS (see FBD-100359); ADFS→KeyCloak; NTP/time-sync servers added; self-registration.
- **Project 2c — Ulsterbus ETM & Metro POS Rollout** — **Way6 POS** and Way6S ETM in scope; VIX RTPI/DAIP for ETM.
- **Project 3 — TVM, PV and HHD Upgrades** — TVM/PV/HHD device upgrades.
- **Project 4 — ABT Tag-On/Tag-Off, BV, GV and POS** — **Axio4 BV** (on-bus, Ethernet to ETM), **Axio4 GV** + Gate Hardware, POS ABT payments; full ABT tap-on/tap-off.

## Key components & hosting boundaries
- **AWS (post-SaaS):** CloudFare Web / Internal Services / Gateway (External Device) Services, **TMS**, **KeyCloak**, CloudFare/ABT DB cluster, Message Broker Service, ABT Modules (Operator + Passenger Web Portals).
- **Translink network (on-prem):** MERIT + MERIT SQL, SmarTrack + SmarTrack SQL, **RabbitMQ (CloudAMQP)**, Data Warehouse, SSIS, PayComplete/Agresso, Legacy Application Server.
- **3rd-party / external:** Corethree (barcode/mLink), Chipside, PayPoint / i-movo, NMI (payments), VIX (RTPI/DAIP), ServiceNow (Customer Support/incidents), Power BI, Card Bureau.
- **Time sync:** devices/servers sync to **NTP servers** — Amazon Time Sync (AWS), a **Translink/UK time server**, and Google (Flowbird users).

## Device → back-office data paths (recurring across phases)
- Devices send **Device Messages / Transactions, ABT Lists, Software & Config** via **TMS** (fares/topology/config down; logon/logoff/stage-change/transaction events up via Gateway Services in near-real-time).
- **Cellular** devices connect direct to AWS; **Ethernet** devices route via the Translink network firewall (cross-ref FBD-100359 offline behaviour).
- **ABT taps** → ABT Broker/Modules → Message Broker → RabbitMQ → MERIT / SmarTrack / Data Warehouse.
- **Barcode Validation (HHD)**, **Penalty Fares (HHD)**, **Collect Tickets (TVM/Kiosk)**, **Change/Payments (TVM/Kiosk)** shown as distinct device flows.
- **On-bus:** Way6S ETM ↔ Axio4 BV Ethernet link; ETM → VIX for RTPI (cellular).

## Suite implications (BOS/ABT suite 30279 + device config)
- This is a **context/traceability map, not a source of new device rules** — no standalone assertions. Use it to:
  - Confirm the **device inventory per phase** (which device types + capabilities are in the build under test) so suite scope matches the delivered project.
  - Establish **end-to-end path expectations** for BOS audit checks (device → Gateway → RabbitMQ → MERIT/SmarTrack/DWH; ABT tap → CloudFare Portal).
  - Sequence **CR/feature dependencies** — e.g. BV/GV/tap-on-tap-off cases belong to Project 4; SaaS/KeyCloak behaviour to Project 1b.
  - Cross-check **hosting boundaries** for the offline/failover cases in FBD-100359 (Ethernet-via-Translink vs cellular-direct-to-AWS).
