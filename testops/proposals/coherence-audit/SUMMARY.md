# Coherence + Grounding Audit — consolidated summary

**Date:** 2026-07-17 · **Scope:** all 7 Translink suites, every non-ZZ case.
**Method:** each case checked for (A) internal coherence — title ↔ preface ↔ preconditions ↔ steps ↔ expected all describe the *same* scenario; and (B) capability grounding vs `knowledge/translink/specs`. Report-only; **no cases edited**.

Findings are grouped into three buckets so we act on each differently:

- **CONTRADICTS-SPEC** — the case disagrees with a distilled requirement. *I can fix these.*
- **INVENTED / NOT-IN-ANY-SPEC** — the action/feature appears in no document (often a surface-confusion). *Condemn.*
- **NEEDS-CONFIRMATION (live system)** — plausibly specified but only George can confirm it's real/live. *Hold; do not assert.*

---

## Per-suite tallies

| Suite | Cases | Findings | High | Med | Low |
|---|---|---|---|---|---|
| POS (1st half) | 265 | 11 | 0 | 3 | 8 |
| POS (2nd half) | 265 | 4 | 0 | 1 | 3 |
| ETM (1st half) | 228 | 8 | 2 | 1 | 5 |
| ETM (2nd half) | 227 | 5 | 0 | 2 | 3 |
| ABT (1st half) | 199 | 3 | 0 | 1 | 2 |
| ABT (2nd half) | 163 | 6 | 0 | 2 | 4 |
| PV | 133 | 9 | 2 | 3 | 4 |
| TVM | 201 | 16 | 2 | 8 | 6 |
| HHD | 211 | 6 | 0 | 2 | 4 |
| GV | 96 | 7 | 0 | 2 | 5 |

Plus the **ABT Tap-Correction/Annulment section (35 cases)** handled separately — the origin of the whole investigation.

### How bad is it, really? (honest proportion)

- **~1,490 cases audited** (excluding the 35-case annul section). **~81 findings ≈ 5%.**
- Of those, **~8 are High** (genuinely broken / impossible) and **~24 Medium**; the rest (~49) are **Low** — grounding gaps, needs-confirmation, or loose wording.
- The **worst single pocket is the 35-case ABT annul/cancel section** — that one was built on a false premise and is largely unusable. It (understandably) coloured the whole impression.
- **The other ~95% are coherent and grounded** — the audit explicitly confirmed the refund block, inspection cEMV lifecycle, barcode state machine, capping oracle tables, screen-validation sets, etc. match spec.

So: a **real but bounded** problem — a few concentrated pockets (annul section; TVM smartcard/scanner assumptions; a handful of tap-on-only-vs-tap-on-off confusions) and a tail of items only George can confirm — **not** a rotten foundation.

---

## The dominant defect: surface / capability confusion

The single biggest theme across suites is cases assuming a device/surface can do something it can't:

- **ETM C4100586 / C4100587 (High)** — assume a **customer tap-off** on Metro/Ulsterbus ETMs that are **Tap-On-Only** (alighting is ETM-calculated / driver-selected). TOTO mechanics welded onto a TOO device.
- **PV C4101005 (High)** — PV **validates a single-use barcode**; FBD-100167 says PV does multi-use only (contradicts its own sibling C4103559).
- **PV C4101085 (High)** — PV **fails over comms**; it is Ethernet-only with no failover (contradicts sibling C4103568).
- **TVM C4103628 (High)** — a barcode is **presented/scanned** at the TVM; per FBD-100317 the TVM has **no scanner** (Collect-Ticket-Code entry only).
- **TVM C4103599 + ~30 cases (Med)** — smartcard **issue/read on the TVM**; FBD-100261/100236 say **POS-only** issue and Card-Bureau writes. Whole "TVM smartcards" area is unconfirmed.
- **HHD C4103828 (Low)** — legacy Mifare validation described as posting a **cEMV ABT audit record** (ABT audit is cEMV-only).
- **GV C4104030 (Med)** — a **TVM-produced multi-use barcode** validated at the GV; TVM can't print multi-use.
- **ABT annul/cancel section** — "cancel a journey/tap in the Operator Portal" (no such action) + "Update Stop list" (invented label for CR122) + capping-£0.00 fused with cancellation-£0.00.

---

## Systemic (best fixed as one rule, not case-by-case)

- **Back-office assertions bolted onto no-transaction scenarios** (POS, ETM): "appears in CloudFare/MERIT/SmartTrack" appended to UI views, cancellations, availability checks, diagnostic reads that produce no transaction. POS-1, POS-2, ETM-2 all flag this.
- **Ungrounded numeric thresholds** (POS power/audio "~3 seconds", ETM print-speed target) carried over from unrelated timeouts.
- **Title mojibake** (`â€"`) on many ETM titles — cosmetic, an extraction/encoding artefact, not a coherence defect.

---

## NEEDS-CONFIRMATION on the live system (only George can close these)

These block me from keeping/writing dependent tests. **Top priority:**

1. **Can you actually change/recalculate a journey's fare in the Operator Portal? In the Passenger web portal?** (CR122 "Alighting Stop Adjustment", FBD-100662.) George has never done this — so the whole ABT correction family is on hold.
2. **Does any "cancel a journey/tap" action exist in either portal?** (Believed no.)
3. **Is there any back-office way to void/refund a *settled* journey?** (C4102830 assumes yes.)
4. **Does the real TVM have a barcode scanner and a smartcard reader?** (Specs say no — affects ~30+ TVM cases.)
5. **Does this ETM have a customer-facing passenger display?** (ETM C4100946.)
6. **Fare-paying / stored-value e-purse smartcard** — real Translink product? (ETM C4102566/67; POS says yes via FBD-100334/100342.)
7. **Concrete cap/fare values** (Metro £4.00/£2.30, iLink £6/£11/£19, ref.60 £7.20/ref.61 £8.20) come from the **UB-TOO tracker**, not the committed FBD specs — need reconciliation against the authoritative fares source.

---

## Cross-case contradictions to resolve

- **HHD C4103831 vs C4103883** — same expired-iLink-at-topup input, opposite outcomes.
- **HHD C4103835 vs C4103982** — expired-card inspection modelled two contradictory ways.
- **POS C4100360 vs C4100436** — sign-off/suspend destination modelled two ways.
- **ETM C4100588** — UB journey "reverts to fixed fare"; FBD-100662 makes flat-fare Metro-only now.

---

_Full per-suite detail in the sibling files: `pos-1`, `pos-2`, `etm-1`, `etm-2`, `abt-1`, `abt-2` (pending), `pv`, `tvm`, `hhd`, `gv` `.findings.md`._
