# HHD deep-grounding audit — consolidated changelog

Suite **30285** (`**NEW** HHD Test Suite`, project 42, `TFTS - System Test`). Full, per-case,
citation-grounded walk of **every one of the 211 live cases** against the real FBD/REQ source
documents (`REQS_DIR`), per George's 2026-07-21 directive: do the actual thing this tool exists for
— not another coherence/wording pass, but cross-examine every claim against the specs. This is a
separate, deeper pass than the 2026-07-17 coherence audit (`hhd.findings.md`, 6 findings) and the
2026-07-21 terse-wording pass (`hhd-terse-rewrite.changelog.md`, 26 cases): those checked internal
consistency and wording; this pass checked **every factual claim's actual source**.

## Method

Batched across 6 parallel sub-agents by section (36/43/44/39/29/20 cases), each independently:
read `CLAUDE.md` + `docs/gherkin-standard.md` + `docs/test-practices.md` in full, then for every case
in its batch: listed every factual claim, checked the existing Refs citation actually supports it
(opened the real spec via `tools/extract_req.py`, not just trusted an existing ref), corrected/added
citations where thin or wrong, marked `**GAP**`/`**UNCONFIRMED**` in place of any unsupported claim
(never invented), and applied the terse-wording standard to anything touched for grounding. The
2 known unresolved conflicts (Q16 C4103831/C4103883, Q17 C4103835/C4103982) were explicitly
protected — no batch touched them.

Merge steps (this session): validated all 6 batches' `*.rewrite.json` for parse errors and cross-batch
ID collisions (none found), dry-ran the combined 134-entry rewrite, applied via
`tools/apply_rewrite.py --commit`, re-ran `audit --suite 30285` (surfaced 1 new blocking
`then-compound-genuine` finding on C4103991, fixed and reapplied), merged all 6 batches' `*.gaps.md`
files into `proposals/coherence-audit/gap-register.md` as **Q34–Q60** (27 new questions, numbered and
cited back into each affected case's Refs field), and re-audited to confirm CLEAN.

## Coverage

**All 211 cases inspected. 0 not-reached.**

| Outcome | Count | Notes |
|---|---:|---|
| **Verified-clean-with-citation** | 72 | Existing claims checked against the real spec and confirmed correct; some got a firmer/corrected citation with no behaviour change. |
| **Corrected** | 87 | Citation wrong/thin/off-topic (see "Systemic citation problems" below) and/or wording tightened for grounding; behaviour claims not invented, only re-sourced or marked. |
| **Flagged-gap** | 48 | A claim has no supporting source anywhere in the requirements library; marked `**GAP**`/`**UNCONFIRMED**` in place and routed to `gap-register.md` as Q34–Q60 (27 questions covering these 48 cases; several questions cover a multi-case group). |
| **Left alone — known conflict, human-owned** | 4 | C4103831, C4103835 (Q16), C4103883 (Q16), C4103982 (Q17) — untouched, per the task's explicit instruction not to resolve these unilaterally. |
| **Not reached** | 0 | — |

Totals sum to 211.

## Systemic citation problems found (not isolated typos — patterns across whole sections)

These recurred across multiple batches independently, which is itself informative — the original suite
build appears to have assigned several refs by **topic-keyword association** rather than opening and
reading the cited document:

1. **FBD-100373 (Refund on POS) cited on ~20 sale/decline/timeout/annul/waybill cases that aren't about
   refunds** — the doc is refund-process-only and in several places (e.g. REQ-1630.0) *explicitly
   excludes HHD from refunds*, so citing it on an HHD annulment/waybill/decline case is actively
   misleading, not just unsupported. Corrected across batches A, B, D, F.
2. **FBD-100383 (Operator Hierarchy) used as a catch-all for sign-on/lockout/duty/break/printer-pairing
   cases** — it is purely the CloudFare location/config-inheritance tree; a direct full-text search for
   "sign on", "PIN", "duty", "lockout", "Device Locked" returns zero hits. Affects most of Sign On &
   Session, half of Operator, and several Supervisor/Technician cases (batches C, D).
3. **FBD-100207 (Fare Stage to Stop) cited for HHD boarding/alighting UI on 11 cases** — the document
   explicitly documents this model for ETM/POS/TVM only and never adds an HHD section, despite
   otherwise being exhaustive per device. Kept as the closest analogy citation but flagged (Q39), not
   asserted as confirmed (batch B).
4. **FBD-100336 (Fares List File Export) cited for on-device UI behaviour** (basket defaults, ticket
   numbering, cash change) — it's a pure back-office CloudFare export feature with no device behaviour
   at all, per its own knowledge note (batch B).
5. **FBD-100716 (Revenue Inspection Device) cited on a 9-case "Penalty Warning & Fares" section**
   describing a manual operator-issued penalty ticket/whitelist/waybill workflow — the actual document
   only describes a **fully automated** back-office cEMV "Standard Fare" charge at End-of-Day, no
   operator action, no ticket, no whitelist. This is the most significant single finding of the whole
   pass (see below) (batch C).
6. **FBD-100651 (Glider cEMV Tap-On-Only) cited on all 7 "Smartcard Inspection" cases** — wrong spec
   entirely (it's the unrelated Glider bank-card TOO flow); corrected to the actual smartcard-inspection
   sources (Smartcard Use Matrix, HHD Inspection & Validation Design Note) (batch E).
7. **FBD-100341/FBD-100276/FBD-100266/FBD-100260/FBD-100342 used as catch-all citations** for on-device
   Operator Menu features (View Totals, mini-statement, Status, favourites) they never describe —
   these are back-office/API/reporting specs, not device-UX docs (batch C).

## Most significant findings (behaviour-level, not just citation hygiene)

- **Q44 — "Penalty Warning & Fares" section (9 cases) may test invented functionality.** No spec
  anywhere in the local library describes a manual, operator-triggered penalty-fare/warning function
  with a printed ticket, a whitelist, or a waybill entry. The only real mechanism found (FBD-100716) is
  a fully automated back-office charge with zero operator interaction. Flagged `POSSIBLE DESIGN/SPEC
  BUG or suite invention` — an entire section may need rewriting to the real cEMV inspection flow once
  an engineer confirms there's no separate legacy manual function.
- **Q38 — new conflict found: C4103829/C4103830 (HHD smartcard top-up) vs C4103832 (HHD cannot issue
  smartcards, in the same suite).** FBD-100261 states smartcard issue+recharge is POS-only — the same
  document already correctly grounds C4103832 elsewhere in this suite. Flagged, not resolved.
- **Q53 — C4103970 "Old Barcode Redemption (BRS) on Glider" upgraded from suspicion to confirmed gap.**
  Exhaustive search (filename + full text) found zero trace of a "BRS" concept anywhere in the library;
  FBD-100483 states outright Glider HHD does not use single-use functionality.
  Two of the 2026-07-17 coherence-audit's original 6 findings (C4103828/C4103833–4103835 "ABT Tap"
  section-overlap, and C4103842 title/body mismatch) were re-confirmed still open during this pass but
  left as structural/wording notes, not re-litigated (out of scope for a citation-grounding pass).
- **Q45/Q46/Q49/Q52 — HHD lacks its own sign-on, break-mode, and printer-pairing source documents.**
  Multiple cases (16 total) rely on cross-device analogy (the POS Overflow sign-on flow) or partial
  hardware-capability inference (Bluetooth+barcode scanning exists, so a printer-pairing flow is
  plausible) with no HHD-specific design doc to confirm the exact mechanism.
- **Q39 — HHD's boarding/alighting stage-selection UI (11 cases) has no HHD-specific spec section**,
  only the ETM/POS/TVM sections of FBD-100207; kept as best-available analogy, flagged for confirmation.
- Reassuring counterpoint: the **Revenue Inspection (cEMV/RID)** section (batch E) and the
  **Single-Use Barcode (NIR)** section (batch D) were both excellently grounded already — every event
  code, message string, and numeric threshold checked out verbatim against FBD-100716/FBD-100483 with
  no corrections needed.

## Gap register

**27 new questions (Q34–Q60)** appended to `proposals/coherence-audit/gap-register.md`, covering all
48 flagged-gap cases (several questions group multiple cases sharing one root question, e.g. Q39 covers
11 cases, Q44 covers 9). Every affected case's Refs field was updated to cite its specific `gap-register
Q<n>` (not just the bare word "gap-register" some batches originally used) so the question is traceable
from the case itself. None of Q34–Q60 are answered yet — batched for George, same as the existing
open Q2/Q10/Q21b.

The two protected pre-existing conflicts (Q16, Q17) remain open and untouched, as instructed.

## Files

- Per-batch rewrite/changelog/gaps: `proposals/coherence-audit/fixes/hhd-deep-audit-batch{A..F}.rewrite.json`,
  `.changelog.md`, `.gaps.md` (kept for detailed per-case audit trail).
- This consolidated changelog: `proposals/coherence-audit/fixes/hhd-deep-audit.changelog.md`.
- Gap register additions: `proposals/coherence-audit/gap-register.md` (Q34–Q60).
- Report: `reports/translink/hhd/2026-07-21/deep-audit.md`.
- A follow-up fix (`then-compound-genuine` on C4103991) applied via
  `scripts/_fix_4103991.rewrite.json`, and the gap-register Q-numbering pass via
  `scripts/_gap_refs_number.rewrite.json` (both one-off, not batch-specific).

## Audit result

```
audited 211 cases: CLEAN; 43 advisory.
```

0 blocking findings. The 43 advisory `title-too-long` items are pre-existing (unrelated to this pass,
titles were not in scope for rewording here).
