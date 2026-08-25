# ABT/BOS suite (30279) — card/credential-variant completeness sweep, 2026-07-23

**Follow-up, narrower pass** to today's general `abt-consolidation-completeness.changelog.md` audit,
modelled on the real miss just found in the PV suite: 13 old-suite card-SCHEME cases (Visa Debit/
Credit, Mastercard Debit/Credit, Maestro) folded into one new case that only said "Visa, Mastercard,
mobile wallet" — silently dropping the Debit/Credit distinction and Maestro. George's directive:
*"anywhere with smartcard, EMV tapping on any device... we should stick with all the validations we
do with different cards, types etc... each variant being tested to ensure we cover all scenarios of
card types... this should be gospel to any device."*

**Question asked:** in the BOS/back-office suite, is card-scheme/product enumeration silently thin
anywhere it should be complete — Declined Taps report (already fixed today), EMV Summary report, Card
Reference File, Smartrack card-data, ABT capping per-scheme, and the Card Verification (AVR/pre-auth/
issuer-liability) family?

## Method

1. Pulled old suite 14441 fully (1,766 cases) and new suite 30279 fully (496 cases, excluding
   `ZZ_DELETE_REVIEW`) fresh this session.
2. Grepped both suites for scheme vocabulary (Visa/Mastercard/Maestro/Amex/Diners/scheme/card type)
   and read every hit's full case body (`custom_preface`/`preconds`/`steps_seperated`/`expected`) via
   `TestRailClient.get_case`, not just titles.
3. For every family where the old suite split cases by scheme, checked whether the new suite's
   consolidated case still names every scheme, and whether it's consistent across title/preconditions/
   steps/expected (not just mentioned once in a summary line while the rest of the case is silent).
4. Cross-referenced `PSPEC-0015` (CloudFare ABT Product Spec) and the `TFTS Requirements Matrix.xlsx`
   for the governing requirements, to confirm each scheme distinction is a real, signed-off/Deployed
   requirement — not just an old-suite title artefact.

## Families checked

- **Card Verification (AVR / Pre-Authorisation / Issuer Liability Threshold)** — real gap, fixed.
- **EMV Summary Report** — real gap, fixed.
- **Retail Debt Report** — real gap, fixed (plus 3 unpinned scheme-handling regressions).
- **Debt Recovery — automated scheme recovery** — inconsistency + thin cadence detail, fixed.
- **Journeys by Card Scheme Report** — checked, no gap (old suite's own body never named a scheme
  breakdown despite the title — nothing to restore).
- **Smartrack Scheme Liability Report / Display Card Data by Card Type** — checked; Smartrack "Card
  Type" is the Translink travel-product taxonomy (SmartPass/Daylink/etc.), not the EMV bank-scheme
  axis — different concept, no gap on this axis. Report-name completeness for Smartrack was already
  resolved in an earlier pass (Q29).
- **Card Reference File, Deny List / BIN List** — re-checked at the scheme level; no additional gap
  beyond what today's earlier consolidation-completeness pass already covers (device-axis, not
  scheme-axis, for Card Reference File; no per-scheme Deny/BIN List old-suite cases exist to be lost).
- **ABT capping per-scheme** — swept; capping rules are configured per fare/zone, not per card scheme,
  in both old and new suites — no scheme dimension to check here.
- **BOS-side BIN-range/Amex/Diners acceptance list** — swept; zero hits in the old suite outside
  device-level (PV/ETM/POS) EMV kernel cases, which are out of this suite's scope (BIN-range
  acceptance is a device concern, not back-office).

## Findings and fixes

### 1. Card Verification family — Maestro silently dropped from 3 of 4 cases

Old suite `ABT / Processing Taps / Card Verification` had 9 real behavioural cases (excl. the
`NOT IN SCOPE` UKCA-trigger-limit template, C2665814) testing AVR/pre-authorisation/issuer-liability
per scheme, each backed by its own signed-off requirement:
- **REQ-3354** Issuer Liability Threshold — tested 3x: Visa (C2665815), MasterCard (C2665816),
  **Maestro (C2665817)**.
- **REQ-3359** AVR — Visa only (C2665818) — confirmed correct scope; PSPEC-0015 §4.6 (para
  ~10543-10547) states AVR is a **Visa-only** mechanism, so no Mastercard/Maestro AVR case ever
  existed or should.
- **REQ-3360** Pre-Authorisation (Mastercard) — 2 scenarios: first daily use (C2665819), first use
  after Deny List removal (C2665820).
- **REQ-3361** Pre-Authorisation (**Maestro**) — a **separate, distinct, signed-off requirement**
  (not a Mastercard sub-case) — same 2 scenarios: first daily use (C2665821), first use after Deny
  List removal (C2665822).

New suite has 4 consolidated cases. Reading full bodies found:
- **C4102937** (Issuer Liability Threshold) — precondition said "Visa or Mastercard" — Maestro
  dropped from the setup even though the case's own Expected summary already promised "Visa,
  MasterCard and Maestro" (an internal inconsistency, not just a gap).
- **C4102938** (AVR — Visa) — correctly Visa-only. No fix needed.
- **C4102939** (first daily use pre-auth) — title/preconditions/steps named only Mastercard; Maestro
  appeared *only* in the Expected summary line ("MasterCard or Maestro") — inconsistent, and REQ-3361
  wasn't in Refs at all.
- **C4102940** (first use after Deny List removal pre-auth) — **worse**: Maestro was absent
  *everywhere* — title, preface, preconditions, steps, and expected all said "Mastercard" only. No
  trace of REQ-3361/Maestro anywhere in this case.

**Fix:** broadened preconditions/preface/expected on C4102937/4102939/4102940 to name every scheme
consistently, retitled C4102939 to name both schemes, and added a `Data variations:` line to each
citing the specific REQ id(s) and old-suite case id(s). C4102938 left untouched (correctly scoped).

### 2. EMV Summary Report — scheme split and report content lost in consolidation

Old suite's 3 cases (C2665801/C2817603/C2879324, REQ-2662.1 "Deployed") all explicitly specify the
report "displays Open Payment details (**split between Visa, MasterCard and Maestro**)", named export
formats (PDF/XLS/CSV), 5 KPI headings, and per-row detail (Decline Reason, BIN range, Issuer,
Quantity, Value, Decline Percentage). New suite's consolidated **C4102894** had none of this — a
generic 3-line stub ("the report is generated / displayed / can be exported") with the scheme split
named nowhere.

**Fix:** restored the Visa/MasterCard/Maestro split into the step body and a `Data variations:` line,
plus the export-format and KPI/row-detail content, grounded directly on the 3 old-suite bodies (now
fully cited in Refs alongside REQ-2662.1/3457/3491). The case's pre-existing `**UNCONFIRMED**`
preface (report existence not named in the 7 governing reporting specs) was **left untouched** — a
separate, already-flagged question this pass does not resolve.

### 3. Retail Debt Report — scheme breakdown dropped + 3 regressions never pinned

Old suite's C2880099 (already cited in the new case's Refs) explicitly specifies the Retail Debt
Summary must show "Value and percentage of debt from **Visa** Cards" and "Value and percentage of
debt from **Maestro and MasterCard's**" — a genuine per-scheme breakdown. New suite's **C4102908**
was the same generic 3-line stub as the EMV Summary Report, with no scheme mentioned at all.

Worse: this exact report has **3 real, unpinned scheme-handling regression bugs** in the old suite
that were never linked via Refs to the new case:
- **CA-13549** — Retail Debt Report displays `NaN` in the Visa and Mastercard debt cells.
- **TODEV-15538** — Maestro retail debts are not counted in the Retail Debt Summary section.
- **TODEV-11567** — unrecovered Maestro debt after 3 failed attempts is not displayed under Total
  Unrecovered Debt.

**Fix:** restored the Visa/Mastercard/Maestro breakdown (value + percentage each) and row-detail
columns as a `Data variations:` line, and pinned all 3 regressions via Refs (`CA-13549`,
`TODEV-15538`, `TODEV-11567`) per the gherkin-standard's regression-pinning rule. `**UNCONFIRMED**`
existence preface left untouched, same reasoning as above.

### 4. Debt Recovery — automated scheme recovery — inconsistent wording + thin cadence detail

**C4102852**'s Expected line said "Scheduled **Visa MIT** recovery re-collects..." while the rest of
the case (preface/preconditions/steps) was scheme-neutral ("scheme-driven", "per card-scheme rules")
— an internal inconsistency naming one scheme only in the summary. PSPEC-0015 (para ~11493-11504)
documents that Visa and Mastercard have genuinely different automated-recovery cadences (Visa: six
attempts within 14 days, UK/IntraEU/International; Mastercard: one attempt/day for a month, retried
at 4/14/28 days, and this schedule explicitly also governs **International and Maestro**) — a real,
spec-named scheme difference with no old-suite case to carry it (this is a PSPEC-only fact, not an
old-suite drop), so it had never been named in either suite.

**Fix:** made the Expected line scheme-neutral (matching the rest of the case, since the behaviour is
the same regardless of scheme) and added the cadence difference as a `Data variations:` line, cited
to PSPEC-0015 directly (spec-grounded, not invented).

## Not touched / no gap found

- **C4102938** (AVR — Visa) — correctly Visa-only per PSPEC-0015 §4.6; no other scheme has an AVR
  requirement.
- **Journeys by Card Scheme Report (C4102902)** — old-suite sources (C2813971, C2879330) never
  actually enumerated a scheme breakdown in their bodies despite the title — nothing to restore.
- **Smartrack Scheme Liability Report (C4103166)**, **Display Card Data by Card Type (C2691860's
  family)** — Smartrack "Card Type" means the Translink smartcard product taxonomy, a different axis
  from the EMV bank-card scheme; no gap on the scheme axis. Report-name completeness for Smartrack
  was already resolved in the 2026-07-22 gap-resolution pass (Q29).
- **Card Reference File, Deny List / BIN List** — re-checked at the scheme level specifically; no
  further gap beyond what today's earlier `abt-consolidation-completeness` pass already covers.
- **ABT capping** — configured per fare/zone, not per card scheme; no scheme dimension applies.
- **BOS-side BIN-range/Amex/Diners acceptance** — zero old-suite hits outside device-level (PV/ETM/
  POS) cases, which are correctly out of this back-office suite's scope.

## Fixes applied this pass

Pushed via `tools/apply_rewrite.py proposals/coherence-audit/fixes/abt-card-variant-sweep.rewrite.json --commit`
(dry-run first: `updated: 6 removed(ZZ): 0 skipped: 0 missing: 0`; then `--commit`, identical counts).
6 existing cases reworded (no new cases created, no cases removed):
- **C4102937** — Maestro added to preconditions; Data variations: Visa/Mastercard/Maestro (REQ-3354).
- **C4102939** — retitled to name Mastercard + Maestro; Data variations: REQ-3360/REQ-3361.
- **C4102940** — Maestro added throughout (was previously absent everywhere); Data variations:
  REQ-3360/REQ-3361.
- **C4102894** — EMV Summary Report scheme split + export/KPI/row-detail content restored.
- **C4102908** — Retail Debt Report scheme breakdown restored; 3 regressions pinned via Refs.
- **C4102852** — Expected line made scheme-neutral; scheme cadence Data variations line added.

**One correction mid-pass:** the first push (dry-run + commit) introduced 2 new blocking
`then-compound-genuine` findings on C4102894/C4102908, because the restored step text joined "the
report is generated and displayed, split by scheme..." inline with "and" (a second predicate,
"displayed", chained after "and" — exactly the pattern the auditor flags). Re-split each into
separate `**AND**` lines (one outcome per line, per the gherkin-standard's own rule) and re-pushed;
confirmed clean on the second audit run before finishing.

## Audit result after this pass

`python -m system_test_ops audit --suite 30279 --no-gate`: **391 cases audited, 89 blocking, 208
advisory** — identical to the pre-existing baseline from earlier today
(`abt-consolidation-completeness.changelog.md`). None of the 6 edited case ids (`C4102937`,
`C4102939`, `C4102940`, `C4102894`, `C4102908`, `C4102852`) appear under any blocking rule; the two
report-name cases (`C4102894`/`C4102908`) still appear only under the pre-existing, advisory
`title-no-emdash`/`title-too-long`/`preface-bad-preamble` sections — all carried over unchanged from
before this session (bare report-name titles and the `**UNCONFIRMED**` existence preface, neither
touched by this pass). **This pass's changes added zero net blocking findings.**

## Files touched

- `proposals/coherence-audit/fixes/abt-card-variant-sweep.rewrite.json` (new, pushed live)
- `proposals/coherence-audit/fixes/abt-card-variant-sweep.changelog.md` (new, this file)
- No changes to old suite 14441 (read-only, never touched).
