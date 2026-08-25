# HHD deep-audit — Batch F (Non-Functional + Smoke)

Suite 30285, sections: Power & Battery, Printer, Comms / SaaS / Heartbeat, Network, Security, Timings,
Smoke. 20 cases (4103991–4104010). Full grounding pass against real FBD/REQ sources (not the earlier
coherence/terse-wording-only pass).

**Headline finding:** 14 of the 20 cases (everything outside Heartbeat) carried a stock citation —
mostly `FBD-100373` (Refund on POS), occasionally `FBD-100359`/`FBD-100651` — that does not discuss the
claim in the case at all. `FBD-100373` in particular is about POS refund/annulment rules and never
mentions battery, printer, panic button, OS upgrade, sign-on, or waybill; for the annulment case
(4104008) that spec actively says refund ≠ annulment, so the citation had it backwards. Corrected all
of these against the real `TFTS Requirements Matrix.xlsx` (`REQ-####`) and, where the topic matched, the
correct FBD.

| Case | Title | Verdict | Citation now | Note |
|---|---|---|---|---|
| 4103991 | Power & Battery — session recovers after power loss | corrected | REQ-0105.0, REQ-0105.1 | Session-recovery + <3min timing grounded; "resolved without duplication" claim not evidenced — marked UNCONFIRMED, logged as a gap. |
| 4103992 | Power & Battery — sign on after battery replacement | corrected | REQ-0105.0, REQ-0105.1 | Citation-only fix; case text already matches (PIN re-entry, <3 min). |
| 4103993 | Power & Battery — low-battery warning | corrected | REQ-1389.1, REQ-1389.3 | Citation-only fix. |
| 4103994 | Printer — partial print reported | corrected | REQ-1741.0 | Citation-only fix; old ref (FBD-100167, barcodes) was topically wrong. |
| 4103995 | Printer — HHD pairs to printer via NFC | **flagged-gap** | REQ-0819.6, FBD-100320 (context, do not confirm) | No spec anywhere describes an external/NFC-paired printer; HHD has an *integrated* thermal printer (REQ-0819.6). The only documented pairing is HHD↔M020 payment terminal over **Bluetooth** (FBD-100320), not NFC, and not a printer. Likely mechanism mix-up — GAP raised. |
| 4103996 | Heartbeat — 15-min call-in when signed off | verified-clean-with-citation | FBD-100266 | Matches distilled notes and spec exactly; no change. |
| 4103997 | Heartbeat — StaffList resets Hours Since Last Comm | verified-clean-with-citation | FBD-100266 | Matches spec exactly; no change. |
| 4103998 | Comms — sustained outage takes HHD offline | corrected | REQ-2576.0 | FBD-100359 explicitly says cellular devices (HHD) are *unaffected* by a Translink-network outage — only listed Ethernet devices go comms-locked. Reworded precondition to "the HHD's own network connection is lost" instead of implying a Translink-network outage; re-cited to a device-agnostic lockout requirement. |
| 4103999 | Comms — queued transactions delivered on restore | corrected | FBD-100359, REQ-2576.0 | Precondition reworded to match the 4103998 fix; the RabbitMQ queue-and-deliver mechanism itself is back-office-side/device-agnostic so FBD-100359 still applies. |
| 4104000 | Network — view connectivity type & strength | corrected | REQ-2854.0 | Citation-only fix; old ref (FBD-100359) is an architecture doc with no device-UI content. |
| 4104001 | Security — panic button raises alert | corrected | REQ-0437.0 | Citation-only fix; matches spec (3x press → immediate BO event → alert email) at the case's declarative altitude. |
| 4104002 | Security — HHD upgrades OS 7 to OS 8 | **flagged-gap** | REQ-0569.0, REQ-1618.0 | General OS/firmware-update-distribution capability is evidenced (TMS-managed, HHD is Android); the specific "OS 7 → OS 8" version pairing appears nowhere in the requirements library — marked GAP rather than asserted, logged for confirmation. |
| 4104003 | Timings — smartcard validation within expected time | corrected | REQ-3364.0, REQ-3365.0 | Citation-only fix; old ref (FBD-100651, Glider TOO) was out of scope. Case correctly avoids a hard-coded value (assumed-configured-value pattern). |
| 4104004 | Timings — barcode read to beep within 1s | corrected | FBD-100167, REQ-3132.0 | Old ref was actually correct (distilled note already cites this "≤1s" fact) — added REQ-3132.0 as a cleaner, more direct source. |
| 4104005 | Smoke — sign on reaches main menu | corrected | REQ-0050.0 | Citation-only fix. |
| 4104006 | Smoke — cash paper ticket sale | corrected | REQ-0163.4 | Citation-only fix. "Adult Single" product confirmed in HHD NIR Products config; £2.30 fare is a configured value, not separately verified — treated as example pricing, not blocked. |
| 4104007 | Smoke — card sale on M020 | corrected | FBD-100320, REQ-0163.4 | Dropped the wrong FBD-100373; kept the already-correct FBD-100320 (Bluetooth pairing) and added REQ-0163.4. |
| 4104008 | Smoke — annul a just-sold ticket | corrected | REQ-0300.0, REQ-0300.1 | Old ref (FBD-100373, Refund on POS) actively contradicts this case — that spec says refund ≠ annulment. Corrected to the real annulment requirements. |
| 4104009 | Smoke — valid smartcard validates | corrected | REQ-0871.0 | Citation-only fix; old ref (FBD-100651, Glider TOO) is PV/HHD-inspection-only scope, not general Multi-Journey validation. |
| 4104010 | Smoke — sign off and print waybill | corrected | REQ-0329.0, REQ-0329.1 | Citation-only fix. |

## Totals
- **verified-clean-with-citation:** 2 (4103996, 4103997 — both Heartbeat, already correctly grounded on FBD-100266)
- **corrected:** 16 (mostly wrong-topic `refs`; two also had preconditions reworded for accuracy — 4103998/4103999)
- **flagged-gap:** 2 (4103995 printer/NFC pairing mechanism; 4104002 OS 7→OS 8 specific version claim)

## Spec surprises worth flagging to the orchestrator
1. **`FBD-100373` (Refund on POS) was used as a near-default filler citation** across Power & Battery,
   Security (panic button), and every Smoke case — none of which it covers, and for annulment it's
   actively contradictory (refund ≠ annulment per that spec's own text). This pattern suggests whoever
   authored this batch's `refs` field didn't check individual citations — worth a targeted look at
   whether other batches share the same filler-ref pattern.
2. **No dedicated HHD hardware/security spec exists in the requirements library** (unlike POS, which has
   FBD-100183). All grounding for battery, printer, panic button, and OS-upgrade claims had to come from
   individual `REQ-####` rows in `TFTS Requirements Matrix.xlsx`, not a cohesive FBD document — this is
   likely why the original authors defaulted to a wrong-but-plausible-sounding FBD number instead.
3. **HHD is a cellular device, not one of the Ethernet devices FBD-100359 discusses** going
   comms-locked during a Translink-network outage — the spec says cellular devices are unaffected. Two
   comms cases (4103998/4103999) had preconditions that read as if HHD suffers the Ethernet-device
   outage behaviour; reworded to the device's own connection being down, which is a real and distinct
   scenario the spec doesn't contradict.

## Files
- `proposals/coherence-audit/fixes/hhd-deep-audit-batchF.rewrite.json`
- `proposals/coherence-audit/fixes/hhd-deep-audit-batchF.changelog.md` (this file)
- `proposals/coherence-audit/fixes/hhd-deep-audit-batchF.gaps.md`
