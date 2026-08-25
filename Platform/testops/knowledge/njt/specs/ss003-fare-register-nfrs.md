# NJT_FRFRP_SS003 — Fare Register Non-Functional Requirements (distilled)

**Source:** `NJT_FRFRP_SS003 Fare Register Non Functional Requirements.pdf` (v1, 6 Jul 2026, Author: Arrive).
Distilled testable facts only — raw spec held locally in `C:\SystemTestOps\njt-requirements\_text\`, not committed.
Related: NJ TRANSIT RFP0000064 - Attachment C (Oct 1 2024) — the referenced, related document (SS003 §1.3).

## Status of these requirements — read before auditing
**Non-contractual "Target" values.** SS003 §1 / Performance Disclaimer (p.4) states every metric in
Section 2 is a **non-binding engineering design goal**, provided to fill gaps not covered by the
primary contract, for **informational/planning purposes only**. All formal baseline requirements
reside strictly in the **Final Design Review (FDR)** documentation — not in this doc. Every row in
the source tables is classified `Target`, and failure to hit a target metric is explicitly stated to
**not** constitute a breach of contract or performance failure (SS003 p.4). This framing matters for
the audit: a TestRail case that treats one of these numbers as a hard pass/fail contractual gate is
overstating its own authority — the case should say "Target" and cite SS003, not imply an SLA.

The document defines only three topic groups (§2.1–§2.3); no security, environmental, MTBF/reliability,
or capacity-beyond-storage sections exist in this spec. **GAP** — those NFR categories are not covered
by SS003 at all; if the TestRail "Non Functional Requirements" section has cases claiming to test
security/environmental/reliability, they must cite a different source document or be flagged as
ungrounded.

## 2.1 System Initialization & Offline Resilience (SS003 p.5)
- **Fare Register start-up time** — Target: **4 minutes** from applying power to the Fare Register
  being fully operational (in the required operating mode).
- **Offline transaction data storage capacity** — Target: minimum of **5 days** of standard
  operational transaction logs and events stored locally **without data loss**.

## 2.2 Cloud Synchronization & Configuration Management (SS003 p.5–6)
All items in this group are explicitly qualified: "Subject to communications infrastructure being
available" (and, for updates, "devices being in a state where they can apply updates") — SS003 p.5–6.
- **Send data to CloudFare** — Target: **10 seconds** after a transaction/event is logged on the Fare
  Register.
- **Apply a remote command** — Target: **5 seconds** after the user triggers the command, to when the
  Fare Register processes it.
- **All devices receiving and activating a configuration update** — Target: **6 hours** after
  distributing a configuration update from CloudFare, for all Fare Registers to apply it.
- **A single device receiving and activating a configuration update** — Target: **1 hour** after
  distribution, for one Fare Register to apply it.
- **All devices receiving and activating a software update** — Target: **24 hours** after
  distributing a software update from CloudFare, for all Fare Registers to apply it.
- **A single device receiving and activating a software update** — Target: **1.5 hours** after
  distribution, for one Fare Register to apply it.

## 2.3 Driver Operations (SS003 p.7)
- **Fare Register sign on (Start of Run)** — Target: **3 seconds** from confirming trip details to
  the Start-of-Run report being printed **and** the Fare Register in Ticket Issue mode.
- **Fare Register sign off (End of Run)** — Target: **5 seconds** from confirming end of run to the
  End-of-Run report being printed **and** the Fare Register in the idle screen.
- **Fare Register sign on (Start of trip)** — Target: **3 seconds** from confirming trip details to
  the Fare Register in Ticket Issue mode.
- **Fare Register sign off (End of trip)** — Target: **5 seconds** from confirming end of run to the
  end-of-trip report being printed **and** the Fare Register displaying the next-trip screen.
- **Print a ticket/receipt (not including 2nd parts)** — Target: **2.5 seconds** after issuing the
  product, to the receipt/ticket being printed.

## Suite implications
13 distinct, individually testable NFRs were catalogued (all timing-based Target metrics; none in
this document are pure hardware/MTBF/environmental specs, so none are ruled out as functionally
untestable — but see caveats below). One coverage checkpoint per NFR:

1. **Start-up time ≤ 4 min** (SS003 p.5) — power-on to fully operational in required mode.
2. **Offline storage ≥ 5 days, no data loss** (SS003 p.5) — needs a sustained/soak-test case (or a
   documented data-volume-per-day proxy); flag as high-effort, not a quick functional check.
3. **CloudFare send latency ≤ 10s** (SS003 p.5) — requires comms available; note the qualifier as an
   explicit precondition in the case.
4. **Remote command apply latency ≤ 5s** (SS003 p.5) — same comms-available precondition.
5. **Fleet-wide config update activation ≤ 6h** (SS003 p.6) — fleet-scale test; likely only feasible
   at a controlled multi-device test bed, not per-device functional testing.
6. **Single-device config update activation ≤ 1h** (SS003 p.6) — comms-available precondition.
7. **Fleet-wide software update activation ≤ 24h** (SS003 p.6) — fleet-scale, same caveat as #5.
8. **Single-device software update activation ≤ 1.5h** (SS003 p.6) — comms-available precondition.
9. **Sign-on (Start of Run) ≤ 3s + report printed + Ticket Issue mode** (SS003 p.7).
10. **Sign-off (End of Run) ≤ 5s + report printed + idle screen** (SS003 p.7).
11. **Sign-on (Start of trip) ≤ 3s + Ticket Issue mode** (SS003 p.7).
12. **Sign-off (End of trip) ≤ 5s + report printed + next-trip screen** (SS003 p.7).
13. **Ticket/receipt print ≤ 2.5s (excl. 2nd parts)** (SS003 p.7).

**Cross-cutting note for every case above:** cite the SS003 "Target" / non-contractual disclaimer
(p.4) in the case preface or comments so the case cannot be read as asserting a contractual SLA.

**Not testable via a single functional/system test case, or out of scope for this document:**
- Fleet-wide items (#5, #7) are testable only as fleet/soak tests, not standard functional cases —
  flag for a dedicated performance/ops test rig rather than the standard suite pattern.
- The 5-day offline storage capacity (#2) needs either a multi-day soak or an audited proxy
  calculation (bytes/transaction × expected daily volume) — a same-day functional case cannot fully
  verify this; note as **partial coverage possible** only.
- Security, environmental (temperature/humidity/vibration), and reliability/MTBF NFRs are **not
  present in SS003 at all** — **GAP**: if the TestRail suite's 14 "Non Functional Requirements" cases
  include any of these categories, they are not grounded in this source document; either locate the
  correct source spec for them or flag as ungrounded/ **UNCONFIRMED** pending the engineer's input via
  the gap register.
