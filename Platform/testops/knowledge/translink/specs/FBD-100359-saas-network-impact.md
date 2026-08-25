# FBD-100359 — CloudFare SaaS Network Impact (distilled)

**Source:** `TFTS CloudFare SaaS Network Impact (FBD-100359) V1.02` (15 Sep 2021, C. Warnes).
Distilled testable facts only — raw spec + network diagrams held locally in `dev/translink-requirements/`, not committed.
Mostly architecture/bandwidth context; testable behaviour is the **offline-mode / failover** rules below.

## What moves to AWS (post-SaaS, release 2.0→2.1)
- Migrated to **AWS**: CloudFare Web, CloudFare Internal Services, Gateway Services (External Device Services), **TMS** (Linux server), **KeyCloak** auth, CloudFare/ABT **DB cluster**, Message Broker Service.
- Stays **on-premise (Translink network)**: **MERIT** + **SmarTrack** (and their SQL DBs), **RabbitMQ**, **PayComplete/Scancoin**, **SSIS**, **Data Warehouse DB**, Card Bureau. **Power BI** sits outside both networks but queries the on-prem Data Warehouse.
- Availability target: **CloudFare SaaS 99.98%** monthly (excludes planned maintenance).

## Auth & release rules
- Auth moves from on-prem **ADFS → KeyCloak** (Azure ADFS) in AWS; Translink no longer maintains its own ADFS for CloudFare/ABT (cross-ref FBD-100342).
- Devices must be updated to use **DNS** (same DNS server) so the server switchover needs **no re-commissioning**.
- Releases are **sequential and incremental** (v1.1, v1.2, v2.0, v2.1…); **no skipping/jumping releases**. Cluster deploys are **zero-loss-of-service**.

## Connectivity behaviour — the testable core
- **Cellular** devices connect directly to AWS (TMS, Gateway Services, KeyCloak) — **independent of the Translink network**.
- **Ethernet** devices (Way6 POS, T1 Dock, Retail Kiosk, **Platform & Gate Validators**) are assumed routed **through the Translink network** to reach AWS.
- **Soft-failure principle:** most Translink-network outages cause a soft failure — functions still run but data may be stale/inaccurate; queued data delivers via RabbitMQ once the network is restored.
- **Hard failure (devices):** on a sustained Translink-network outage, **Ethernet devices operate offline, and after a significant period may enter a communication-locked, out-of-service state.** Same result whether the fault is external or internal (they route through Translink either way). Cellular devices are unaffected.

## Service behaviour during a Translink-network issue
- **MERIT / DWH:** no near-real-time updates (transactions, passenger journeys, schedule) reach MERIT DB; queued in RabbitMQ and delivered on restore. Web MERIT unavailable; existing data still reportable via WTS UI/MERIT. Full denial → no MERIT reporting; **ABT transactions still reportable via the AWS-hosted CloudFare Web Portal.**
- **SmarTrack:** no near-real-time updates; changes (e.g. hot-listing a card) not reflected to device services until restore; Card Bureau cannot reach SmarTrack.
- **PayComplete/Scancoin:** operators can still pay-in; MERIT not updated so shorts/overs reports inaccurate until restore.
- **Power BI:** depends on on-prem Data Warehouse — any Translink-network access issue (internal or external) blocks report generation.

## Suite implications (BOS/ABT suite 30279 + device config)
- **Offline-mode device cases** are the key deliverable: pull the Translink network, assert Ethernet devices (POS/PV/GV/Kiosk/T1 Dock) go offline and eventually enter the **communication-locked out-of-service** state; assert **cellular devices keep working**.
- **Recovery/queue** case: transactions generated during outage are queued and **delivered to MERIT/SmarTrack via RabbitMQ on restore** (no data loss) — a good end-to-end BOS audit check.
- **Auth** case: device/portal auth via KeyCloak (not ADFS); DNS-based server switchover requires no re-commission.
- SmarTrack hot-list change not reflected on device during outage; **ABT still reportable via CloudFare Web Portal** when MERIT is unreachable.
- Bandwidth/firewall detail is context only — no device/BOS assertions.
