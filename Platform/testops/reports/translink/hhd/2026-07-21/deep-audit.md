# HHD deep spec-grounding audit — suite 30285

**Date:** 2026-07-21/22 · **Project:** 42 (TFTS - System Test) · **Suite:** 30285 (`**NEW** HHD Test
Suite`) · **Scope:** all 211 live cases.

## Verdict

**CLEAN** (0 blocking conformance findings, 43 pre-existing advisory title-length items). All 211
cases inspected and cross-examined against the real FBD/REQ specs (`REQS_DIR`) — not a repeat of the
lighter 2026-07-17 coherence pass or the 2026-07-21 terse-wording pass, but the full citation-grounded
check George asked for. 87 cases corrected, 48 flagged as genuine gaps (routed to the gap register as
27 new questions, Q34–Q60), 72 verified clean with a checked citation, and 4 left untouched as
already-known, human-owned conflicts. Nothing was invented to fill a gap; every unsupported claim is
marked visibly in-case.

## Totals

| | Count |
|---|---:|
| Total live cases | 211 |
| Verified-clean-with-citation | 72 |
| Corrected (citation and/or wording) | 87 |
| Flagged-gap (GAP/UNCONFIRMED marker added, gap-register question raised) | 48 |
| Left alone — known conflict, human-owned (Q16, Q17) | 4 |
| Not reached | 0 |

## By section

| Section | Cases | Clean | Corrected | Gap | Conflict |
|---|---:|---:|---:|---:|---:|
| Card Payment (M020) + Ref-Number Stations | 20 | 5 | 11 | 4 | 0 |
| Smartcards & ABT | 16 | 6 | 5 | 3 | 2 |
| Annulment & Reversal | 11 | 5 | 5 | 1 | 0 |
| Sales – Ticket Issue / Basket / Group / Visual / Cross-Border / Metro & Ulsterbus | 32 | 8 | 21 | 3 | 0 |
| Top-Ups | 14 | 6 | 5 | 3 | 0 |
| Penalty Warning & Fares | 8 | 0 | 0 | 8 | 0 |
| Sign On & Session | 13 | 4 | 1 | 8 | 0 |
| Operator | 9 | 3 | 1 | 5 | 0 |
| Supervisor | 9 | 6 | 1 | 2 | 0 |
| Technician | 7 | 4 | 2 | 1 | 0 |
| Ticket Formats & Waybill | 12 | 3 | 9 | 0 | 0 |
| Single-Use Barcodes (NIR) | 11 | 11 | 0 | 0 | 0 |
| Multi-Use Barcodes + Old Barcode Redemption (BRS) | 9 | 5 | 3 | 1 | 0 |
| Smartcard Inspection | 7 | 0 | 3 | 4 | 0 |
| Revenue Inspection (cEMV/RID) | 13 | 12 | 0 | 0 | 1 |
| Non-Functional (Power/Printer/Comms/Network/Security/Timings) | 14 | 1 | 11 | 2 | 0 |
| Smoke | 6 | 3 | 3 | 0 | 0 |

(Row counts are per-agent classification; a few cases carry both a citation correction and a gap
marker, tie-broken to the more significant outcome for this table — the case-level truth is in the
per-batch changelogs.)

## Top findings

1. **Systemic wrong-spec citations, not isolated typos.** Several off-topic FBDs were used as
   catch-all references across whole sections — most notably **FBD-100373 (Refund on POS)** on ~20
   non-refund cases (it explicitly excludes HHD from refunds, so the citation was actively backwards
   in places), **FBD-100383 (Operator Hierarchy)** on most Sign On/Operator/Supervisor cases (it's a
   CloudFare config-tree doc with zero sign-on content), and **FBD-100651** on all 7 Smartcard
   Inspection cases (the wrong Glider cEMV spec entirely). All corrected to real, content-verified
   sources.
2. **The whole "Penalty Warning & Fares" section (9 cases) may test invented functionality**
   (gap-register Q44). The only real mechanism documented anywhere (FBD-100716) is a fully automated
   back-office cEMV charge with no operator action, ticket, whitelist, or waybill — nothing in the
   library supports the manual operator-driven flow these 9 cases assume. Flagged as a possible
   design/spec bug or suite invention; needs an engineer's call before any rewrite.
3. **A new conflict, found while grounding (not previously known): C4103829/C4103830 vs C4103832**
   (gap-register Q38) — the suite claims both that HHD can top up smartcards and, elsewhere, that HHD
   cannot issue smartcards, citing the same document (FBD-100261) for both. Flagged, not resolved.
4. **C4103970's "legacy BRS redemption on Glider" upgraded from suspicion to confirmed gap**
   (gap-register Q53) — exhaustive search found no trace of a BRS concept anywhere in the requirements
   library, and the relevant specs say Glider HHD does not use single-use functionality at all.
5. **HHD lacks its own sign-on/break-mode/printer-pairing source documents** — 16+ cases currently rely
   on cross-device analogy (POS's Overflow sign-on flow) or partial hardware-capability inference,
   with no HHD-specific design doc to confirm exact screens/mechanisms.
6. Two sections were already excellently grounded with no corrections needed: **Revenue Inspection
   (cEMV/RID)** and **Single-Use Barcodes (NIR)** — every event code, message string, and threshold
   checked out verbatim against FBD-100716 / FBD-100483.

## Known unresolved conflicts (untouched, per instruction)

- **Q16** — C4103831 vs C4103883 (expired Adult iLink at top-up: refuses vs reactivates).
- **Q17** — C4103835 vs C4103982 (expired-card inspection: audit `DeclinedReason=1` vs M020 "Card
  Declined" pre-tap).

Neither spec search this session turned up a definitive answer for either — both need George's
live-system confirmation, as previously determined.

## Gap register

27 new questions (**Q34–Q60**) appended to `proposals/coherence-audit/gap-register.md`, covering the
48 flagged-gap cases. Every affected case's Refs field cites its specific `gap-register Q<n>`. None
answered yet.

## Not reached

None. All 211 cases were inspected; 0 remain outstanding from this pass.

## Files

- Changelog (full accounting): `proposals/coherence-audit/fixes/hhd-deep-audit.changelog.md`
- Per-batch detail: `proposals/coherence-audit/fixes/hhd-deep-audit-batch{A..F}.{rewrite.json,changelog.md,gaps.md}`
- Gap register: `proposals/coherence-audit/gap-register.md` (Q34–Q60)
- This report: `reports/translink/hhd/2026-07-21/deep-audit.md`

## Audit gate

```
audited 211 cases: CLEAN; 43 advisory.
```
