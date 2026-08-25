# HHD gap-register resolution pass — 2026-07-22/23

Suite **30285** (`**NEW** HHD Test Suite`, project 42, `TFTS - System Test`). Before escalating the
HHD deep-audit's ~26 open questions to George (the biggest backlog in the gap register), tried hard to
resolve every one of them from existing evidence first, per George's directive: check the 4 old suites
(5446 primary, 13958 dedup, 5608 smoke, 5505 R1.1) via `TestRailClient.get_cases(42, <id>)`, the
UX/design-note documentation (`HHD Inspection and Validation Design Note.docx`, `Smartcard Use
Matrix.xlsx`), and a broader/deeper `REQS_DIR` re-search — before anything goes to George as
unanswerable.

## Scope

All HHD questions in `proposals/coherence-audit/gap-register.md`: the original **Q16/Q17** conflicts
(near the top of the file, "Cross-case contradictions" section), the standalone **Q58-Q60** (before
the HHD session header), and the **Q34-Q57** batch from the "HHD deep-grounding audit (suite 30285)"
session — 27 questions total covering ~50-plus cases (several questions group multiple cases).

## Method

1. Dumped all 4 old suites' cases (`get_cases(42, <suite>)`) and sections to local JSON for offline
   keyword search (1632/455/42/151 cases respectively) — avoided repeated live API calls per question.
2. Dumped the live HHD suite (30285, 211 cases) similarly, for exact case-body reference.
3. Opened `Smartcard Use Matrix.xlsx` and `HHD Inspection and Validation Design Note.docx` directly via
   `tools/extract_req.py`, and — where a flattened text/pipe-joined table risked mis-mapping columns
   (the same trap the earlier TVM/GV Q10 pass fell into) — re-opened the xlsx with `openpyxl` directly,
   cell-by-cell, to get the real per-column (device/mode) mapping rather than trusting a joined-text row.
4. **New this pass**: searched `REQS_DIR` for `TFTS Requirements Matrix.xlsx`
   (`1_Requirements/TFTS Project Delivery Matrices & VCRMs/`) — a REQ-id index/description sheet
   (~3,230 REQ ids with full requirement text, status, and device applicability) that had never been
   searched by name in any prior pass. This one file resolved more questions than everything else
   combined — see "Most valuable source" below.
5. For every resolvable question: updated the gap-register entry in place (an `A (resolved from
   [source], 2026-07-22): ...` block appended under the original, question left visible for audit
   trail), then re-grounded the affected case(s) via `hhd-gap-resolution.rewrite.json` +
   `hhd-gap-resolution2.rewrite.json`, applied with `tools/apply_rewrite.py --commit` (suite locked via
   `TESTRAIL_WRITE_SUITE_ID=30285`).
6. Re-ran `python -m system_test_ops audit --suite 30285` after each commit; both passes returned
   **CLEAN** (0 blocking findings).

## Most valuable source: `TFTS Requirements Matrix.xlsx`

Flagged mid-task by a sibling POS gap-resolution pass that had just found it. Its "Description" sheet
maps every `REQ-####.#` id to full requirement text, sign-off status, and per-device/per-mode
applicability (HHD (All) / HHD (NIR) / HHD (BRT) etc.) — exactly the traceability layer the earlier
HHD deep-audit pass was missing (that pass could only find FBD-numbered docs, many of which don't cover
HHD at all, which is *why* so many of Q34-Q57 existed). This single file resolved or substantially
resolved: Q35 (PAN masking, REQ-1722.0/1723.0), Q38 (smartcard top-up vs issue, cross-checked against
`Smartcard Use Matrix.xlsx`), Q39 (boarding/alighting stage UI, REQ-0113.3/0142.0 + a whole REQ-08xx.x
series), Q40 (annul reverses the smartcard write, REQ-2836.0), Q41 (default ticket type, REQ-0235.0),
Q42 (advance date is an attribute not a product, REQ-0142.6/0446.0/3094.0), **Q44** (the 9-case Penalty
Warning & Fares section — REQ-0062.0/0062.1, REQ-1449.0/1449.2/1449.3/1449.4, REQ-2255.6,
REQ-3047.0/3048.0/3049.0, REQ-0329.1), Q45 (sign-on/session, REQ-0056.0-3, REQ-0276.0, REQ-0050.3,
REQ-0396.2, REQ-1478.0/0384.1), Q46 (break mode itself, REQ-0305.0/0305.1/0305.2/0360.0/1137.0), Q47
(View Totals/mini-statement, REQ-0299.0/0350.2), Q48 (favourites, REQ-0307.0/0307.1), Q49/Q52 (printer
hardware is integrated per REQ-0819.6, strengthening rather than resolving the doubt), Q51 (Supervisor
override vs authorise direction, REQ-0360.0/0305.2), Q55 (revalidation window, REQ-3488.0), Q56
(printer is integrated not NFC-external, REQ-0819.6/0819.8).

## Old-suite evidence (second most valuable)

- **Q16** (expired-card top-up: refuse vs reactivate): suite 5446 (C1688835, C2682243, C2682242/2244/
  2247/2248, C2682255/2256) and dedup suite 13958 (C2598643) all model the same consistent
  reactivation flow across ~9 cases spanning two suites — none model an outright refusal.
- **Q58** (Multi-Journey top-up max journeys): suite 5446 C2678902/C2678944 ("...Journeys Exceed 45")
  state the real maximum is **50 journeys** (45 is a boundary test value used in those cases, not the
  cap itself) — the live case's "45-journey maximum" wording was reworded accordingly.
- **Q59** (expired journeys removed before top-up): suite 5446 C2678904/2905/2946/2947 plus a dedicated
  receipt format (C2725362 primary / C2598962 dedup, "Ticket Format 13C — Smartcard Top-up Expiry
  Receipt") fully confirm this as real, existing behaviour.
- **Q47** (Mini Statement field list): suite 5446 C2759099/C2759103 give the exact on-device field list
  (Card Type, ESN, PSN, Card Ref, Start/End Date, Journeys/Days Left, Usage/Top-Up Date-Time).

## Spec cross-reference (no new document, just reading two already-indexed notes together)

- **Q17** (DeclinedReason=1 vs "Card Declined"+event 5010): `knowledge/translink/specs/
  FBD-100658-abt-audit-specification.md`'s `DeclinedReason` enum (`1`=Card Expired) and
  `knowledge/translink/specs/FBD-100716-revenue-inspection-device.md`'s event 5010 ("Failure – Card
  Expired") describe the *same* M020 card-integrity-check decline from two different audit layers
  (BOS audit record vs on-device event/message) — not a real conflict, just two incomplete partial
  descriptions of one event. No prior pass had cross-referenced these two already-cited docs together.

## Outcome — 27 questions

| Outcome | Questions | Notes |
|---|---|---|
| **Resolved** | Q16, Q17, Q35, Q38, Q40, Q41, Q42, Q44, Q48, Q51, Q55, Q56, Q58, Q59 | 14 questions, ~30 cases re-grounded/corrected, 0 behaviour invented. |
| **Substantially/partially resolved** | Q39 (10/11 cases), Q45 (7/8 cases), Q46 (2/3 cases; 1 condemned), Q47 (2/4 cases) | Core claim grounded; one narrow sub-claim per group stays open. |
| **Strengthened but not resolved** | Q49, Q52 | New contradicting hardware evidence (REQ-0819.6/0819.8: printer is integrated, BT/NFC is for the M020 only) makes both look likely-invented, but not condemned outright — escalated with the new evidence attached rather than unilaterally deleted. |
| **Still open — no source found** | Q34, Q36, Q37, Q43, Q50, Q53, Q54, Q57, Q60 | Genuinely searched (old suites + REQ matrix + REQS_DIR) and came up empty; these stay queued for George. |

**Cases condemned (`ZZ_DELETE_REVIEW`), 3:**
- **C4103831** ("a top-up on an expired card is rejected") — superseded by old-suite evidence; the
  reactivation model (C4103883) is correct instead.
- **C4103977** ("inspection is available in break mode") — its own premise contradicts REQ-0305.0's
  explicit constraint that break mode restricts the touch-screen/keyboard to ID+PIN entry only.
- **C4103995** ("HHD pairs to a printer via NFC") — REQ-0819.6/0819.8 confirm the printer is
  integrated hardware and the HHD's only external-pairing NFC/BT use is the M020 payment device;
  likely a mislabelled duplicate of C4104007.

**Cases updated, 48** (39 in the first rewrite pass + 9 in a follow-up): Refs corrected/added, GAP/
UNCONFIRMED/CONFLICT markers removed where resolved, two cases reworded (C4103855 advance-ticket
attribute vs product; C4103925 renamed + reworded from "authorise" to "override/end"), one case's
config-value wording corrected (C4103881, 45 → the configured maximum/50).

## Files

- `proposals/coherence-audit/fixes/hhd-gap-resolution.rewrite.json` — main rewrite (39 cases + 3
  condemned).
- `proposals/coherence-audit/fixes/hhd-gap-resolution2.rewrite.json` — follow-up Refs-only rewrite (9
  cases: the Q45 sign-on group + Q47's View Totals/Mini-Statement pair).
- Gap-register updates: `proposals/coherence-audit/gap-register.md` (Q16, Q17, Q35, Q38-Q42, Q44-Q49,
  Q51, Q52, Q55, Q56, Q58, Q59 all carry an `A (resolved/partially resolved/strengthened from ..., 2026-
  07-22)` block; unresolved questions unchanged).
- Reports: `reports/tfts-system-test/new-hhd-test-suite/2026-07-22/alignment-audit.md` and
  `.../2026-07-23/alignment-audit.md` (post-commit re-audits, both CLEAN).

## Audit result

```
audited 208 cases: CLEAN; 43 advisory.
```

0 blocking findings both times (after the first 39-case commit and again after the 9-case follow-up).
The 43 advisory `title-too-long` items are pre-existing and unrelated to this pass.
