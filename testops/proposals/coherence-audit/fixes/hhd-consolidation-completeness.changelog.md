# HHD consolidation-COMPLETENESS audit — 2026-07-23

Suite **30285** (`**NEW** HHD Test Suite`, project 42). Question answered: did consolidating ~2,087
main-scope old cases (suites 5446 primary, 13958 dedup, plus 5608 smoke/42 and 5505 R1.1/151) down to
211 active cases in 30285 **remove genuinely distinct required coverage**, not just redundancy? Builds
on today's earlier gap-resolution pass (which already surfaced Q38's smartcard top-up conflict and
Q42's "Advance ticket" question, both now resolved) — this pass is a fresh, systematic family-by-family
completeness sweep, the first one run on HHD (unlike POS/ETM, which already had one).

## Method
Pulled all 4 old suites full (`TestRailClient.get_cases(42, <id>)` + `get_sections`) and the live 30285
suite full, to local JSON for offline grouping (avoided repeated live calls). Grouped by the family
taxonomy in `proposals/hhd-suite-restructure/structure.md` (Sign On/Session, Sales, Card Payment,
Smartcards & ABT, Top-Ups, Smartcard Inspection, Barcodes, Revenue Inspection, Annulment & Reversal,
Penalty, Ticket Formats/Waybill, Metro/Ulsterbus Products, Non-Functional). For each family, cross-tabbed
old-suite distinct members (product names, format numbers, decline reasons, role×method combinations)
against the live suite's cases and their `custom_expected` text, checking specifically for a "Data
variations:" line where a case represents multiple old-suite members.

**Priority directive followed:** George specifically flagged Sign On / role-based access as the family
most likely to have lost a genuinely distinct role×method combination in the fold from ~42 role×sign-on
cases (across the 4 old suites) down to ~14 live cases. That matrix was walked in full first (see Q61/Q62
below) before moving to the other families.

## Families reviewed

| Family | Old-suite basis | Verdict |
|---|---|---|
| **Sign On & Session (Operator/Supervisor/Technician role×method)** | 42 cases, 4 suites | **2 genuine gaps found and fixed** (Q61, Q62) — see below. Everything else in the matrix (ID entry, smartcard, invalid credentials, duty number, Message/Word&Colour of the Day, NIR/Metro topology, route selection, sign-off incl. forced-by-docking, auto sign-off, break-mode resume, battery-replace sign-on, Technician/Supervisor sign-on/off) confirmed present. |
| **Ticket Formats & Waybill** | ~55 numbered format/layout cases | **Fully covered** — every NIR Layout (1–20) and Glider Format (1–16 incl. sub-letters) traced to an explicit Data-variations line in C4103939–C4103950, including the easy-to-miss NIR Layout 20 / Glider Format 15 Mini-Statement (folded correctly into C4103917's Expected text). Model example of correct consolidation. |
| **Card Payment (M020) + decline reasons** | ~20 cases incl. declined/expired/blocked/timeout | **Fully covered** — pairing, TID/TK, terminal group, device swap, chip-and-PIN/contactless/wallet, three decline reasons (declined/expired/blocked), EMV timeout, cancel-before/after-card, comms resume, PAN masking, PRN format, on-charge sale, plus the two NIR-only reference-number-station cases. |
| **Annulment & Reversal (no refund)** | ~20+ cases across 4 suites | Mostly covered (cash/card ticket, cash/card top-up, nothing-to-annul, sign-off annul, M020 reversal, unique-ref annul, no-refund x2). **One gap found**: "24+" discount product annul (old C1706672/C2598723) not named anywhere — added as a Data-variation with a GAP marker (Q64, no REQ id confirmed). |
| **Smartcards & ABT (product validation)** | ~100 "Validate <Product>" cases, 32 named product sections in 5446 | **Gap found and fixed** (Q63) — representative cases existed but carried no "Data variations:" enumeration. Added, citing ~30 REQ ids confirmed live for HHD via `Smartcard Use Matrix.xlsx` + `TFTS Requirements Matrix.xlsx`. 2 product names flagged rather than asserted (iLink NW — GAP; Metro/Joint TaxSmart — UNCONFIRMED/archived REQ). |
| **Smartcard Top-Ups** | ~25 cases across product families | **Gap found and fixed** (Q63, same root cause) — C4103879 said "across products" with no named list; added Data-variations line (Multi-Journey, Period Pass/DayLink, BVP, Metro Travelcard, iLink) with REQ-id Refs. |
| **Smartcard Inspection** | ~58 cases, product-family sections (Concession/Half-Fare/Staff/EA/Discounted-Youth/Adult-Child colour) | **Gap found and fixed** (Q63, same root cause) — added a Data-variations line to C4103971 naming the product families the representative cases stand in for. |
| **Metro/Ulsterbus Products** | Glider R1.1 tree (Multi-Journey/DayLink/Travelcard/Town Service) | **Gap found and fixed** (Q63, same root cause) — C4103875/C4103876 named no specific product; added DayLink/Multi-Journey/Travelcard (Metro) and Multi-Journey (Ulsterbus) as Data-variations. Town Service was already its own two cases (C4103877/C4103878) — correct, since it has genuinely distinct boundary behaviour (zone-limited pricing), not just a data variation. |
| **Single-Use Barcodes (CR094) / Multi-Use Barcodes / Old Barcode Redemption (BRS)** | ~247 cases incl. TIBU regression buckets | **No new gaps found this pass** — the existing coherence audit (`hhd.findings.md`) already flagged C4103970 (BRS on Glider) as needs-confirmation; not re-litigated. State-machine coverage (200/400/500, AES/TripleDES, 17-comma decrypt, offline sweep, events 1412/1416) traced fully to the live 11-case Single-Use section; Multi-Use's 8 cases cover the validation-outcome/passback/expiry/audit matrix. Deep TIBU-by-TIBU reconciliation not repeated here — out of scope for this pass, flagged for a future dedicated barcode-regression audit if needed. |
| **Revenue Inspection (cEMV/RID)** | ~30 cases (RID list lifecycle, events 5008–5013) | **Fully covered**, per the existing coherence audit's assessment — Inspection-Mode enablement, all 5 decline events (5009–5012), success (5008), timeout, cannot-annul, and the full/delta/EoD RID-list lifecycle are all present. Confirmed a Supervisor-not-just-Operator inspection eligibility question (Q65) but the old source (C4068377) is too thin (unstructured, `None` body) to ground a dedicated case on — logged, not authored. |
| **Penalty Warning & Fares** | 9 cases | Already confirmed real (not invented) by today's earlier gap-resolution pass (Q44); re-checked against the live 8-case section — consistent, no new gap. |
| **Sales — Paper Tickets (incl. Cross-Border, Basket, Group)** | ~90 cases | Reviewed at a high level — Ticket Issue (default type/stage/change/warrant/advance-date/barcode), Basket, Group, Cross-Border (ROI alighting/boarding, Euro cash, cross-border layout) all present with sensible Data-variation grouping (period product, Bus Rambler, 3 Day Select). No gap found. |

## Fixes applied

**Two new cases (Sign On, from the priority-directive matrix walk):**
- **C4104127** — "Sign On — an incorrect Supervisor PIN leaves a PIN-locked HHD locked" (`Functional /
  Supervisor`). Negative counterpart to the existing C4103926 (Supervisor unlocks a PIN-locked HHD).
  Grounded on 5446 C2759053/C2759057/C2735568 + 13958 C2598944 (4 old cases, 2 suites, all consistent).
  Refs `REQ-0099.1`.
- **C4104128** — "Sign On — device resets to Inspector Mode after a full sign-off" (`Functional / Sign
  On & Session`). Distinct trigger/outcome from the existing break-mode-resume case (C4103913): a full
  sign-off/sign-on defaults to Inspector Mode; a break preserves the pre-break mode. Grounded on 5446
  C3509566/C3509644, carries an explicit `**UNCONFIRMED**` marker (no REQ/FBD distinguishing the two
  triggers was found this pass). Refs `FBD-100651`.

**Eight cases updated with Data-variations + REQ-id Refs (product-catalogue completeness):**
C4103820, C4103822, C4103826 (Smartcards & ABT — Validate), C4103840 (Annulment — 24+, GAP-flagged),
C4103879 (Top-Ups), C4103875, C4103876 (Metro/Ulsterbus Products), C4103971 (Smartcard Inspection).
Product-family grounding: `Smartcard Use Matrix.xlsx` (Smartcard Validation / Smartcard Topups sheets —
HHD is the merged E:F columns = Glider/NIR) + `TFTS Requirements Matrix.xlsx` "Description" sheet
(REQ-0837–0919 series, REQ-2025/2026, REQ-2461/2463/2618/2633/2070/2065, REQ-3473/3475/3478/3480).
Two product names explicitly NOT asserted (flagged instead): **iLink NW** (no distinct REQ — only a
generic iLink + NW zone flag per FBD-100250) and **Metro TaxSmart / Joint TaxSmart** (REQ found but
tagged `#ARCHIVE#` — needs an engineer call on live status).

**Gap register:** `proposals/coherence-audit/gap-register.md`, new session "HHD consolidation-
COMPLETENESS audit" — Q61 (resolved-by-fix), Q62 (resolved-by-fix, UNCONFIRMED), Q63 (resolved-by-fix,
product enumeration), Q64 (open — 24+ product, GAP), Q65 (open — Supervisor inspection eligibility, GAP,
not authored, source too thin).

## Files
- `proposals/coherence-audit/fixes/hhd-completeness-audit.rewrite.json` — 8 case updates (Data-variations
  + Refs), applied via `tools/apply_rewrite.py --commit`.
- `proposals/coherence-audit/fixes/hhd-signon-completeness.cases.yaml` — 2 new cases, applied via
  `python -m system_test_ops push --commit`.
- `proposals/coherence-audit/gap-register.md` — Q61–Q65.
- Report: `reports/tfts-system-test/new-hhd-test-suite/2026-07-23/alignment-audit.md` (post-commit
  re-audit).

## Audit result
```
audited 210 cases: CLEAN; 43 advisory.
```
0 blocking findings after both commits (8 updated + 2 new = 213 live-title rows, 3 pre-existing
`ZZ_DELETE_REVIEW` condemned cases excluded from the 210 count, same as the prior gap-resolution pass).
The 43 advisory `title-too-long` findings are pre-existing and unrelated to this pass.
