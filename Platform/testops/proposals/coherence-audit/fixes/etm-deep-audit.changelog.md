# ETM deep spec-grounding audit — suite 30254 (2026-07-22)

**Suite:** 30254 (`**NEW** ETM-Acceptance Suite`, project 42 `tfts-system-test`)
**Mandate:** George's whole-department directive — cross-examine every live case against the real
FBD/PSPEC specs (not just internal coherence), fold in the terse-wording standard, no corners cut.
**Status:** 6 cases corrected and pushed to TestRail; 2 new gaps logged; re-audit CLEAN.

## What this pass built on

This suite already had two full passes before today:
- **2026-07-17 coherence + grounding audit** (`etm-1.findings.md` + `etm-2.findings.md`) — read all
  455 then-active cases (139 Functional + 23 Non-Functional + 7 Regression + 6 Smoke + 280 HMI,
  sampled) for internal coherence AND spec grounding against the FBD library, citing FBD-100662,
  FBD-100658, FBD-100335 etc. per case. 13 findings raised (2 High, 2 Medium/CONFLICT, 9 Low/
  needs-confirmation).
- **2026-07-21 capability fixes** — 3 of those findings (C4100586, C4100587, C4100588) resolved via
  George's live-system Q&A (gap-register Q7, Q19).
- **2026-07-21 terse-wording pass** (`etm-terse-rewrite.*`) — reread all 455 active cases for
  inline-citation/prose bloat; 2 cases fixed (same C4100586/587, provenance moved to Refs).

**This pass's job**, per today's directive, was the part not yet done: **take the remaining open
findings from the 2026-07-17 audit and actually check them against the full spec text** (not just
flag them), resolve what's resolvable, and gap-register what isn't — plus a fresh full-suite sweep
for the specific wrong-fact patterns George flagged live today.

## Fresh pull

`TestRailClient.get_cases(42, 30254)` → `proposals/coherence-audit/fixes/etm-suite-30254-raw-2026-07-22.json`
(524 cases, 50 sections). **454 active** (non-`ZZ`) + **70** in `ZZ - To Delete (review then bin)`
(one more than the 69 counted on 2026-07-21 — `C4100588` was condemned that day and is now correctly
in the ZZ bin). ZZ section not touched, per standing instruction.

## Full-suite fact sweep (all 454 active cases)

Regex/keyword swept every active case's title+preface+preconds+steps+expected for the four
just-confirmed ETM facts, to make sure nothing beyond the 3 cases already fixed on 2026-07-21 still
assumes the wrong version:

| Fact | Pattern | Hits | Verdict |
|---|---|---:|---|
| No customer tap-off on Metro/Ulsterbus | "alighting-only tap", "tap-off", "boarding-and-alighting pair" | 2 (C4100586, C4100587) | Both are the **already-corrected** cases (ETM-calculated / driver-selected alighting) — matched only because they still say "alighting". No other case affected. |
| Flat/fixed fare is Metro-only | "fixed fare" | 0 | Clean — the one stale case (C4100588) is already in the ZZ bin. |
| ETM has a customer-facing passenger display | "passenger display" | 2 (C4100645, C4100946) | Both consistent with the confirmed-real peripheral; no doubt language remaining. |
| Fare-paying/e-purse smartcard is real | "fare-paying", "stored-value", "e-purse" | 3 (C4102566, C4102567, C4102568) | All consistent with the confirmed-real product. |

**Result: no case beyond the 3 already fixed on 2026-07-21 assumes any wrong version of these four
facts.**

## Resolving the 8 previously-open findings (etm-1/etm-2)

| Case | 2026-07-17 finding | This pass | Outcome |
|---|---|---|---|
| C4103547 | Rail-Sub tap audit fields — needs-confirmation (gated feature) | Q20 (2026-07-21) already confirmed rail-sub gating is correct as written, no case change needed. Re-checked the TransportationType/paymentType/revenue assertions against **FBD-100335 v3.00 §Rail Substitution para 155** ("ensure ABT taps are sent to the back office with a transport mode of 'Rail Sub'") — supported. | **Verified-clean-with-citation.** Refs already correct (FBD-100335, FBD-100658, FBD-100662); no field change. |
| C4103548 | Rail-Sub PJT-ignored/MJT clause — the added "MJT still applied" wording had no cited source | Read **FBD-100335 v3.00 para 159** in full: *"Note that the Maximum Journey Time still applies to these journeys however."* Directly confirms the clause. | **Verified-clean-with-citation.** No field change — the claim was correct, just previously uncited at paragraph level; now confirmed. |
| C4100550 | "the change receipt can be annulled" tacked onto a ticket-issue case, not exercised by any step | Confirmed C4100551 ("Ticket Issue — annulment") is the dedicated case for this behaviour (same section, section 887016) | **Corrected** — dropped the annul clause from Step1's expected result and the case-level Expected; annulment stays owned by C4100551 only. |
| C4100545 | "the alighting-stage key toggles currency" — unsourced key-mapping claim | Searched the requirements library for "currency"/"Euro" — 0 relevant hits. No spec documents this key mapping. | **Corrected + gap logged (Q26).** Applied the gherkin-standard "Unknown how" pattern: names the outcome (switch currency to Euro and back), defers the exact control to the tester, `**GAP**` marker in place of the invented key claim. |
| C4100950 | Generic "CloudFare activity log... corresponding event" bolted onto a print-speed case; no concrete target time | Pulled **FBD-100358 v4.00's full event-type list** (§3.2.1–3.2.18: Transaction ×2, Transaction Annulment, Start/End of Shift, Start/End of Journey, Event, Stop Arrival/Departure, Operator Event, Device Status, Device Registration, Inspection, Defect, Driver Break, Peripheral Device, Software Version) — none is a print-speed/hardware-performance metric. | **Corrected** — dropped the CloudFare step (not a real event); replaced the unstated numeric target with the "Unknown configured value" pattern (assumed-knowledge precondition) instead of a guessed figure. |
| C4100949 | Same generic CloudFare step bolted onto a sustained-performance case | Same FBD-100358 event-list check — no performance/response-time event exists. | **Corrected** — dropped the CloudFare step. Step1 (the actual behaviour) unchanged. |
| C4100945 | Deny/BIN-list + FEIG + "Open Payments" terminology unconfirmed; same generic CloudFare step | Searched the requirements library for "FEIG" and "Open Payments" — 0 hits. Found `Deny List Tile Options.docx` (a design-options doc) confirming a general deny/negative-list-download concept only. FBD-100358's event list has nothing for a deny-list update either. | **Corrected + gap logged (Q25).** `**GAP**` marker added to the preface for the FEIG/Open Payments terms; dropped the ungrounded CloudFare step; left the defect-linked download/update behaviour as-is (not itself disproven). |
| C4100944 | "the corresponding event" left unnamed for a sequence-ID/power-loss case | FBD-100358 §3.2.12 "Device Status" is the only event type in the full list covering a device power/restart condition. | **Corrected** — named the event as "Device Status" (FBD-100358 §3.2.12) instead of the vague "the corresponding event." |

## Additional risk-weighted spot-check (citations not previously flagged)

Per the mandate ("don't assume a citation existing means it was verified"), sampled and independently
re-checked 3 further FBD-cited cases against the full spec text (not previously flagged by any prior
pass), covering a different feature area (Transfer) and a different spec (FBD-100271):

- **C4103556** ("a transfer audits WTS SmartTransfer while a journey audits WTS SmartUse") — confirmed
  against FBD-100271 v5.00 paras 160–161, 166–167 (WTS SmartUse on failed-transfer check, WTS
  SmartTransfer on a valid transfer). **Supported.**
- **C4103553** ("the ETM decides transfer vs journey from the ROUTE Transfer Time") — confirmed against
  FBD-100271 para 178 ("The ETM will always use the Route Property to determine the transfer time for
  the route"). **Supported.**
- **C4103554** ("a stop outside the Metro Transfer Zone is charged as a journey") — confirmed against
  FBD-100271 para 195 (Metro Transfer Zone definition, stops-in-zone requirement). **Supported.**

All three verified-clean-with-citation, no changes needed.

## Applied

- Rewrite file: `proposals/coherence-audit/fixes/etm-deep-audit.rewrite.json` (6 records, action
  `reword`).
- Dry-run: `python tools/apply_rewrite.py proposals/coherence-audit/fixes/etm-deep-audit.rewrite.json`
  → `updated: 6, skipped: 0, missing: 0`.
- Commit: same + `--commit` → `updated: 6`.
- Gap register: `proposals/coherence-audit/gap-register.md` — added Q25 (FEIG/Open Payments, C4100945),
  Q26 (FLU currency-switch key, C4100545).

## Re-audit result

`python -m system_test_ops audit --suite 30254`:

```
        0  mojibake
        8  title-no-emdash (advisory)
       66  title-too-long (advisory)
        0  preface-empty / preface-bad-preamble
        0  preconds-empty / preconds-no-given
        0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
        0  then-compound-genuine
        0  expected-empty / expected-starts-then
        0  has-tags
  audited 454 cases: CLEAN; 74 advisory.
```

**CLEAN of blocking findings.** The 74 advisory items are pre-existing title-style items (length /
em-dash), out of this pass's scope.

## Accounting — total / verified / corrected / flagged-gap / sampled-only / not-reached

- **Total active cases:** 454 (out of 524; 70 in `ZZ - To Delete`, correctly untouched).
- **Verified-clean-with-citation (this pass, newly re-checked against full spec text):** 5
  (C4103547, C4103548, C4103556, C4103553, C4103554).
- **Corrected (this pass):** 6 (C4100550, C4100545, C4100950, C4100949, C4100945, C4100944).
- **Flagged-gap (this pass, new questions):** 2 (C4100545 → Q26, C4100945 → Q25) — both already
  reflected as corrections above (GAP marker applied in the same edit that fixed the coherence issue).
- **Full-suite fact sweep (all 454 active):** re-confirmed clean for the 4 live-confirmed ETM facts
  (no customer tap-off, Metro-only flat fare, passenger display exists, fare-paying smartcard real).
- **Carried forward from the 2026-07-17 full pass (not re-derived independently this session):** the
  remaining ~163 of 174 non-HMI Functional/Non-Functional/Regression/Smoke cases were already read
  end-to-end for internal coherence AND spec grounding in `etm-1.findings.md`/`etm-2.findings.md`
  (which cite FBD-100662, FBD-100658, FBD-100335, FBD-100271, FBD-100831, FBD-100358 etc. per case)
  and found clean at that time. This session did not re-open and independently re-derive a fresh
  citation for every one of those ~163 cases from raw spec text — it (a) resolved every item that
  pass had explicitly left open/uncertain (the 8 above), (b) full-suite swept for the 4 specific
  wrong-fact patterns George called out live, and (c) spot-verified 3 additional not-previously-
  flagged citations against raw spec text as a confidence check on the earlier pass's citation
  quality (all 3 passed). **If a fully independent re-derivation of citations for all ~163 remaining
  cases is wanted, that is not done in this session and would need a further pass** — flagging this
  explicitly rather than silently presenting the 2026-07-17 pass's results as if redone today.
- **HMI Screen Validation (280 cases):** sample-verified only, per the task's own allowance — relying
  on the 2026-07-17/07-21 passes' representative sampling (~6 cases spot-checked across Driver Menu,
  Fare Look-Up, Numeric Entry, Power Management, Printer & Travel Mode, Promo Menu, Sign On,
  Smartcards, Supervisor Menu, Technician Menu); not independently re-sampled this session. Explicitly
  **not** a full 280-case deep-check.
- **Not reached:** the 70 `ZZ - To Delete` cases (out of scope by standing convention — pending human
  bin-review, never edited).

## Most significant findings

1. Two cases (C4100950, C4100949 — both Regression) asserted a CloudFare Activity Log event for a
   claim (print speed, sustained-use response time) that **has no corresponding event type** in the
   full FBD-100358 spec — a genuine over-assertion beyond what the back office can actually audit, not
   just a wording nit.
2. C4100545's premise — a specific key (the alighting-stage key) toggles currency — has **zero
   supporting text** anywhere in the requirements library; it was pure invention of a mechanism dressed
   up as fact. Corrected to the "Unknown how" pattern rather than removed, since the underlying £/€
   screen capability is real.
3. C4100550 was quietly asserting a second behaviour (annullability) that belongs to a different,
   already-existing case (C4100551) — a small but real duplication/conflation the terse-wording pass
   would not have caught (it isn't a citation/prose problem, it's a coherence one).

## Addendum (2026-07-22) — gap-register Q25/Q26 resolved before escalation to George

George's standing directive: exhaust the old suite, Overflow/UX flow annotations, and a broader spec
re-search before putting any GAP/UNCONFIRMED question to him. Both ETM questions left open by this
pass (Q25, Q26 above) turned out to be answerable from evidence already available — neither needed to
reach George.

**Q25 (C4100945, FEIG/Open Payments terminology).** Pulled old suite 4943 via
`TestRailClient.get_cases(42, 4943)` and searched case titles for "feig"/"open payment"/"bin
list"/"deny list". Found **C2547104** ("302090 - Open Payments Service - Deny or BIN List Updates
while FEIG is doing Comms Call") — tied to the exact same defect number (302090) the live case cites —
plus **C2536476**/**C2543245** ("301106 - Deny List is not Downloaded to Device" / "Deny List
Downloads Daily"), tied to defect 301106, also cited by the live case. The old suite's own section
title is literally "Open Payments Service" for this defect pair, using "FEIG" and "Deny/BIN list"
exactly as the live case does. This is direct old-suite test evidence for the identical defects, not a
spec — but per the department's evidence hierarchy (old suite counts as prior test evidence), it
resolves the terminology question.

**Q26 (C4100545, currency-switch key).** Re-read `knowledge/flows/etm-flow-annotations.md` — both the
"FLU" and "FLU 2.0 Navigation" Overflow boards independently state that pressing the Alighting Stage
key a second time toggles the sale currency to Euro, and a third time toggles back to Pounds. Then
pulled old suite 4943's **C2471550** ("7.0.4 Main Screen - Currency is Euro") — an old, real test of
the same screen — whose preface states the identical mechanism verbatim (predating this session, drawn
from an earlier Overflow export, noting Euro functionality wasn't fully delivered until R2.1). Two
independent sources (the current Overflow UX design and the old suite's own prior test) agree exactly,
so the GAP is resolved as fact rather than left as "unknown how."

**Applied:** `proposals/coherence-audit/fixes/etm-gap-resolution.rewrite.json` (2 records, action
`reword`) — dry-run then `--commit` against suite 30254. C4100545's GAP marker removed and the
Alighting Stage key asserted as the currency-toggle control (two-press → Euro, third press → Pounds).
C4100945's GAP marker removed; FEIG/Open Payments terminology now asserted as confirmed, citing the
old-suite case ids in Refs. Re-audit (`system_test_ops audit --suite 30254`): **CLEAN**, 454 cases, 74
pre-existing advisory (title-length/em-dash) findings unchanged, 0 blocking.

**Result:** both open ETM gap-register questions from this suite are now resolved from existing
evidence (old suite + UX flow annotations) — no ETM question needed escalation to George this round.
