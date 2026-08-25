# Gap Register & Q&A — NJT Fare Register (Non-Functional Requirements)

**Purpose.** Every gap is a question, not a silent marker. See CLAUDE.md's "gaps trigger a Q&A loop" rule.

---

**Q1 · GAP · Security / environmental / reliability-MTBF NFR categories have no source and no cases** — OPEN

`knowledge/njt/specs/ss003-fare-register-nfrs.md` confirms SS003 (`NJT_FRFRP_SS003 Fare Register Non
Functional Requirements.pdf`) defines only three NFR topic groups — System Initialization & Offline
Resilience, Cloud Synchronization & Configuration Management, and Driver Operations — and explicitly
has no security, environmental (temperature/humidity/vibration), or reliability/MTBF sections.

Cross-checking against the 14 existing TestRail "Non Functional Requirements" cases
(`reports/uk-bus-projects/njt-farebox-and-register-replacement/2026-08-13/area-cases/nfr.md`): none of
the 14 claim to test security, environmental, or reliability/MTBF behaviour — all 14 map cleanly onto
SS003's three defined groups. So there is no existing case wrongly grounded against SS003 in this
category. But that also means **these three NFR categories currently have zero TestRail coverage** in
the "Non Functional Requirements" section, and SS003 states the formal baseline NFRs actually live in
the FDR (Final Design Review) documentation, not in this doc.

Question for the engineer: does the FDR (or another spec) define security / environmental /
reliability-MTBF NFRs for the Fare Register? If so, please point us at it so cases can be grounded and
drafted; if genuinely out of scope for this device/contract, please confirm so we can record that
explicitly rather than leave it an open unknown.

A:

source: `knowledge/njt/specs/ss003-fare-register-nfrs.md`.

---

**Q2 · FINDING · Existing cases don't reflect SS003's non-contractual "Target" disclaimer** — OPEN

SS003 §1 / Performance Disclaimer (p.4) states every metric in Section 2 is a non-binding engineering
design goal ("Target"), provided for informational/planning purposes, and that missing one does **not**
constitute a breach of contract. None of the 14 existing "Non Functional Requirements" cases
(C4105015, C4105017–C4105029) reference this disclaimer in their Expected result — each currently reads
as a hard pass/fail figure with no framing.

Question for the engineer: should the existing 14 cases be updated (in a future authoring pass — not
altered by this task, per the "old suite copy-not-edit" posture extended here) to state the disclaimer
in their Expected result, so a missed target reads as "investigate, don't fail the release" rather than
an implied contractual breach? The 3 newly drafted soak/fleet-scale cases in `nfr.cases.yaml` already
carry this framing as the template for any such rewrite.

A:

source: `knowledge/njt/specs/ss003-fare-register-nfrs.md` (Performance Disclaimer summary, p.4).

---

**Q3 · FINDING · Three NFRs are only "Partial" against SS003's own testability caveats** — OPEN

Per `knowledge/njt/specs/ss003-fare-register-nfrs.md`, three checkpoints are explicitly flagged in the
source knowledge note as not fully verifiable via a single-run functional case: offline storage
capacity (5 days, C4105017), fleet-wide config update rollout (6h, C4105021), and fleet-wide software
update rollout (24h, C4105023). The existing cases test these as simple same-run/single-rig checks,
which is a reasonable smoke test but does not verify the actual soak/fleet-scale target.

Question for the engineer: is there an existing soak-test rig or fleet-scale test bed (or fleet
telemetry from a live pilot rollout) that could execute the 3 supplementary cases drafted in
`nfr.cases.yaml` (System Initialization & Offline Resilience / Cloud Synchronization & Configuration
Management sections)? If no such rig exists yet, should these be logged as a test-infrastructure gap
rather than executed cases for now?

A:

source: `knowledge/njt/specs/ss003-fare-register-nfrs.md`; `proposals/njt-fr-suite-restructure/findings-nfr.md`.

---
