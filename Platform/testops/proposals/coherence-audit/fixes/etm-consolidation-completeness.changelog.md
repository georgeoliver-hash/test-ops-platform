# ETM consolidation-completeness audit — suite 30254 (2026-07-23)

**Mandate:** did consolidating `AA-ETM-Acceptance Test` (4943, 936 cases / 146 sections, read-only)
down to the new `**NEW** ETM-Acceptance Suite` (30254) silently drop any genuinely distinct required
coverage — a card type, entitlement, decline reason, product variant, or behaviour branch — rather
than legitimately folding it into a data-variation line? This is a fresh pass, on top of the
2026-06-11/12 function-granularity audit (`proposals/function-granularity-audit.md`) and the
2026-07-17/21/22 coherence/terse/deep-grounding passes (`proposals/coherence-audit/fixes/etm*`),
which had already restored several dropped families (Fare-Paying Smartcard, Faulty Smartpass/
Dependants receipts — see `proposals/etm-suite-restructure/unfold.cases.yaml` and
`smartcard-products.cases.yaml`).

## Data pulled fresh this session

- `TestRailClient.get_cases(42, 4943)` — **936 cases, 146 sections** (old, untouched).
- `TestRailClient.get_cases(42, 30254)` — **524 cases, 56 sections** (new) → **454 active** excluding
  `ZZ - To Delete` (70), before this session's additions; **456 active** after.
- `get_sections` for both suites, to build full section paths per case (old title-only groupings can
  be misleading — e.g. "Glider Transfers" turned out to hold mis-filed PV cases, not ETM cases).

## Method

Grouped both suites by full section path, cross-referenced top-level and second-level section counts
old vs new to find suspicious drops, then read full case bodies (preface/preconds/steps/expected) for
every family investigated in depth — not just titles — before deciding covered / folded / gap.

## Family-by-family accounting

### 1. Sign On & Session — Driver/Supervisor/Technician × method × mode (PRIORITY — George's specific concern)

Old: 19 Driver-sign-on cases + 4 Supervisor-sign-on + 3 Technician-sign-on = 26, plus Supervisor/
Technician sign-off and menu-function cases. New: `Functional / Sign On & Session / Driver` (10),
`/Supervisor` (5), `/Technician` (3).

**Supervisor sign-on (4/4) and Technician sign-on (3/3): fully covered, 1:1**, each old case (Manual,
Smartcard, Lock Out, Unlock) has its own new case (C4100525–528, C4100530–532).

**Driver sign-on: read all 19 old cases' full bodies against the 10 new cases' full bodies.**
- Manual/Smartcard first-use, first-use-with-defects, lock-out, topology-per-route, not-communicating
  (this old case is actually about the MOTD/Word-&-Colour lookup **timeout** fallback, not general
  CloudFare comms — confirmed folded into C4100510's "or its Unavailable fallback after the 5-second
  timeout" steps): **covered**.
- Invalid Duty Number, Invalid Journey Number: **folded as explicit steps inside C4100510** ("an
  invalid duty is rejected... the invalid journey number is rejected") — correctly a data variation,
  not a dropped case.
- Subsequent-use with/without on-board safety check, and overridden: **folded into C4100513** via an
  explicit variation clause ("skipped when already satisfied on board, or presented/overridden per
  configuration") — the override branch is named, not silently dropped. Correct.
- Abandon before route selection / after Duty entry: **folded into C4100521**, both outcomes (no
  shift vs End-of-Shift + Waybill) explicitly named. Correct.
- Correct topology — Metro: **generalised into C4100523** ("Run against Metro and Ulsterbus
  configurations") — the intended use of TestRail Configurations, not a drop.
- **GAP FOUND — Duty Number Back / Back Button at Route Entry / Abandon Sign-Off (old C1521874,
  C1521889, C2543141):** the old suite's "P-key sign-off prompt is available at every sign-on screen
  and can itself be **cancelled (L6)**, resuming at the exact screen it was raised from" branch is
  **not tested anywhere** in the new suite. C4100521 only exercises the two **confirm** outcomes
  (abandon before/after route selection); the **cancel-the-abandon** branch — a genuine negative/
  boundary path per `docs/test-practices.md`'s "positive, negative and boundary coverage" principle —
  was dropped. **Fixed** (see below).
  - **GAP FOUND — Journey screen pagination (old C1547359):** the Journey Selection screen's
    dynamic behaviour (more than 5 journeys available for a duty pages via arrow up/down, with the
    journey closest to current time highlighted) is a distinct interactive behaviour, not a static
    screen-content check — HMI Screen Validation only covers static rendering of `01.5.0 Journey
    Selection` / `01.5.1 Journey Number`, not the paging/highlight logic. **Not represented anywhere**
    in the new suite. **Fixed** (see below).
  - Journey Confirmation content/back (old C1547361): the screen-content part (journey time/number/
    direction/first stage) is HMI-covered (`01.6.0 Route Summary`); the back-to-journey-entry
    navigation is the same cancel/resume mechanic as the abandon-cancel gap above — covered by the
    same new case's "resumes at the exact screen" assertion (worked example includes the
    Journey Number screen).
- **Minor — Smartcard + first-use-with-defects combination (old C2481159):** C4100512 (the defects
  case) doesn't name the sign-on method in its precondition, so the smartcard variant wasn't named
  anywhere (mechanism is identical once authenticated — a data variation, not a distinct behaviour).
  **Fixed** — added `Data variations: Manual or Smartcard sign-on.`

**Verdict: 2 genuine gaps found and fixed (new cases), 1 minor labelling gap fixed (data-variation
line added). Everything else in this family — the one George specifically flagged — was already
correctly consolidated with variations properly named.**

### 2. Ticket Issue — per-product Adult/Child/Basket matrix

Old: ~109 cases (Metro Single, Day Return, iLink Single, Month Return, Jobseeker, Gateway, Warrant
Return, Metro Day/Evening/Family, Bus Rambler, Family & Friends, Park & Ride, ME Rugby Day; each ×
Adult/Child × Issue/Annulment/Basket-Issue/Basket-Annulment) + Easibus (9 stage sub-variants) +
Change Receipts + printer-interrupt (4). New: `Functional / Ticket Issue` (5) + `/Promo Menu` (2) +
`Functional / Basket Mode` (4).

Read all 7 live case bodies in full. **Every product is explicitly named** in a `Data variations:`
line — C4100550 lists Metro Single/Day Return/Month Return/iLink Single/Gateway/Jobseeker/Warrant
Return/ME Rugby Day; C4100558 lists Bus Rambler/Metro Day-Evening-Family Day/Family & Friends Day/
Park & Ride/ME Rugby Day; C4100555 lists all 8 Easibus stage options. Basket issue/annulment/limits/
tracker are generic-mechanism cases (Basket Mode section) — correct, since the basket mechanic is
identical regardless of which product is in the basket. Annulment refusal reasons (boarding-stage-
changed, MJ-validated, pass-validated, concession-pass) are named explicitly in C4100551. Change
Receipt is folded into C4100550 ("prints a change receipt when change is due") — same mechanism,
not product-specific. **Verdict: correctly consolidated, no gap.**

### 3. Smartcards & ABT — product × mode cross-tab (28-behaviour plan)

Already the subject of a dedicated prior audit (`smartcards-abt-crosstab.md`, 337 old cases → ~28
behaviour cases) and the 2026-06-12 function-granularity un-fold (Fare-Paying Smartcard, Faulty
Smartpass/Dependants receipts, per-product validation cases in `smartcard-products.cases.yaml`).
Spot-checked the per-product validation cases (60+, Senior, ROI Senior, Blind, War Pensioner,
Half-Fare, Free, Staff/Spouse/Dependants/Retired/External, EA Bus/Rail, DayLink, Belfast Visitor,
iLink, aLink, yLink, 24+, Metro/Town Service Travelcard) — each is its own case with the invalid/
expired/hotlisted branch and the CloudFare/MERIT/SmartTrack verification steps already baked in.
Old suite's `Invalid Cards?` section (17 product-specific "invalid card presented" cases) maps onto
these same per-product cases' rejection branch — confirmed not a separate drop. **Verdict: already
remediated by prior passes; this session's spot-check found no further gap.**

### 4. Barcodes

Old: 22 cases across Single Use Online (8 failure reasons: decrypt-fail, visual-confirm-not-passed,
already-validated-offline, invalid-product, expired), Single Use Offline (over-limit, invalid-
product), Multiple Use (passback, incorrect-zone, wrong-dates, wrong-travel-method), mLink (expired),
Printing, Legacy. New: `Functional / Barcode Scanning` (6). Read all 6 in full — **every failure
reason is named explicitly** as a `Data variations:` line on C4100622 (online) and C4100625
(multiple-use); offline over-limit/invalid and mLink-expired are named in-line in C4100624/C4100626;
legacy barcodes are named in C4100628. Barcode Reference Entry (old: 4 cases, single/multiple ×
valid/invalid) → C4100627 covers both types + invalid generically (same mechanism). **Verdict:
correctly consolidated, no gap.**

### 5. Driver Menu & Options

Old ~30 across Annulments, Driver Break, Currency, Driver Options (Other Devices, Last Ticket,
Totals, Soft Reboot, Reboot Card Reader, Report Faulty Reader, Display Settings, Paper Status, Word &
Colour, Messages), Open Tickets, Barcode Reference Entry, Inspector, Start New Journey. New:
`Functional / Driver Menu & Options` (14). Annulments and Open Tickets are homed under `Ticket Issue`
in the new structure (organisational move, not a drop — confirmed covered per family #2 above).
"Start New Journey" confirmed present (C4100549). Driver Menu access/navigation (C4100595) explicitly
tests the 'C'/Go Back navigation — this family's back-navigation coverage is intact, which sharpens
the confidence that the Sign-On family's back-navigation gap (family #1) is a genuine, isolated drop
rather than a suite-wide pattern. **Verdict: correctly consolidated, no gap found in this pass.**

### 6. Invalid Cards? / card-technology dimension

Old section held two things conflated under one heading: (a) per-product "invalid card presented"
cases — already covered per family #3; (b) card-**technology** cases (MIFARE Classic 1K, MIFARE
Classic EV1, 8-digit PSN range) — a genuinely distinct dimension (chip/format, not product
eligibility). New suite's C4100655 covers MIFARE Classic 1K/EV1 but **did not name the PSN-range
case (old C2439098)** anywhere. **Fixed** — added `Data variations: 8-digit PSN range.` to C4100655.
Also confirmed: `Restart - Break Mode / In Service Within/Outside Recovery Period` (old, 4 cases) →
fully covered by C4100636 (power-loss recovery within/outside the recovery period, including break
mode). `Interface With Other On-Vehicle Third Party Equipment` → covered by C4100657.

### 7. Exploratory Tests / Timing Tests, Non-Functional testing

Old: 17 stopwatch-benchmark cases (Idle→FLU manual/card, per-product basket print timings, annul
timing) + 2 (smartcard/EMV timings). New: `Non-Functional / System and Performance` includes
C4100656 (smartcard/EMV transaction timings, explicitly carrying forward old C2448294's
"potentially untestable" caveat). The per-scenario stopwatch benchmarks are generalised into a single
"acceptable timing" check — the underlying flows (FLU navigation, basket printing, annulment) are
separately functionally tested elsewhere; only the specific numeric per-scenario benchmark is
consolidated. Treated as a legitimate equivalence-class consolidation (test-practices rubric #2), not
a functional-coverage drop, and out of this audit's priority scope per the task brief (HMI/NFR timing
is lower-risk, sample not exhaustive).

### 8. Glider Transfers

Old "Glider Transfers" section (3 cases) is titled `PV: cEMV Card Transfer — …` — these are **PV
(Person Validator) device cases mis-filed under the ETM suite**, not ETM behaviour. ETM's own
Transfers coverage lives in `Functional / Smartcards / Transfers` (4 cases; already spec-verified
against FBD-100271 in the 2026-07-22 deep-audit pass, findings C4103556/C4103553/C4103554).
**Verdict: correctly excluded (wrong device, not an ETM drop).**

### 9. HMI Screen Validation (280 cases)

Sampled per the task brief's explicit lower-priority allowance (not re-verified exhaustively this
pass) — consistent with the 2026-07-17/21/22 passes, which sampled representatively across Driver
Menu, FLU, Numeric Entry, Power Management, Printer & Travel Mode, Promo Menu, Sign On, Smartcards,
Supervisor Menu, Technician Menu and found the template coherent by construction.

### 10. Supervisor/Technician Functions

Old Supervisor Functions (8: Serial Numbers, Software Versions, Config Data Versions view/print,
Historic Waybills, Force Comms ×3, Soft Reboot) and Technician Functions (13, similar + Device
Settings + Paper Status) → new Supervisor Menu (5) / Technician Menu (8). The three "view and print
X versions" cases fold legitimately into one "view and print versions" case per role (same UI
mechanism, different data field) — correct. Technician's own "Paper Status" case is not separately
represented (only Driver Menu's paper-status case exists) — judged a legitimate consolidation (same
screen/mechanism regardless of which menu it's opened from), not pursued as a gap given no evidence
the content differs by role.

## Applied changes

1. **New case C4104125** — "Driver Sign On — abandoning is cancellable and resumes at the same
   screen" (`Functional / Sign On & Session / Driver`). Refs: old suite 4943 C1521889, C2543141.
2. **New case C4104126** — "Driver Sign On — Journey screen pages more than 5 journeys with the
   closest highlighted" (same section). Refs: old suite 4943 C1547359.
3. **Reworded C4100512** — added `Data variations: Manual or Smartcard sign-on.` Refs: old suite
   4943 C2481159.
4. **Reworded C4100655** — added `Data variations: 8-digit PSN range.` Refs: old suite 4943 C2439098.

Files: `proposals/coherence-audit/fixes/etm-completeness-signon.cases.yaml` (the 2 new cases, pushed
via `push --commit`), `proposals/coherence-audit/fixes/etm-completeness-signon-minor.rewrite.json`
(the 2 rewords, applied via `tools/apply_rewrite.py --commit`).

## Re-audit result

`python -m system_test_ops audit --suite 30254` after all commits:

```
        0  mojibake
        8  title-no-emdash (advisory)
       68  title-too-long (advisory)
        0  preface-empty / preface-bad-preamble
        0  preconds-empty / preconds-no-given
        0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
        0  then-compound-genuine
        0  expected-empty / expected-starts-then
        0  has-tags
  audited 456 cases: CLEAN; 76 advisory.
```

**CLEAN of blocking findings** (456 active cases, up from 454 before this session's 2 additions; 76
advisory title-style items, unchanged in kind from prior passes, out of this audit's scope).

## Summary

- **Families reviewed:** 10 (Sign On & Session — priority deep dive; Ticket Issue; Smartcards & ABT;
  Barcodes; Driver Menu & Options; Invalid Cards/card-technology; Exploratory/Timing; Glider
  Transfers; HMI sampled; Supervisor/Technician Functions).
- **Genuine gaps found and fixed:** 2 new cases (abandon-cancel-resume; Journey-screen pagination),
  both in Sign On & Session — the family George specifically flagged.
- **Minor labelling gaps fixed:** 2 (Manual/Smartcard defects variation on C4100512; PSN-range
  variation on C4100655).
- **Confirmed correctly consolidated (no case needed):** Ticket Issue, Smartcards/ABT, Barcodes,
  Driver Menu & Options, Restart/recovery-period, Third-party equipment, Timing/NFR, Glider (wrong
  device, correctly excluded).
- **Not exhaustively re-verified this pass (by design, per task brief):** HMI Screen Validation (280
  cases, sampled only, consistent with prior passes).
- **Audit:** CLEAN of blocking findings after all commits.
