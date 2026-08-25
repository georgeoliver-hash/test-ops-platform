# POS consolidation-completeness audit — suite 30253, 2026-07-23

**Question this pass answers:** did consolidating `AA-POS Acceptance Test` (9317, 2193 cases) down
to `GG - POS - Claude Suite` (30253, ~530 active cases) silently drop any genuinely distinct
required coverage — a card type, entitlement, decline reason, or product variant the system
actually needs tested — rather than removing true duplication? This is a fresh pass, separate from
and deeper-grounded than the 2026-06-11/12 `function-granularity-audit.md` (whose over-folding
findings were checked for completion, not assumed complete).

**Method.** Pulled both suites live via `TestRailClient.get_cases(42, …)` (raw, full body fields —
not the `cases` CLI's normalised baseline, which truncates new-suite bodies to preconditions only
for this suite's template). Old suite 9317: 2193 cases across 369 sections. New suite 30253: 628
cases (530 active, excluding `ZZ_DELETE_*`/`Delete`). Grouped the old suite by product/card-type/
role/mode family, cross-checked each family's distinct members against the new suite's cases and
their "Data variations:" / preface / precondition text — a member is missing only if nothing in the
new suite names it anywhere, even generically.

**George's specific instruction mid-task:** make Sign On/Session the first and most thorough family
— walk the full role (Operator/Supervisor/Technician/Administrator) × method (manual/smartcard) ×
mode (NIR/Ulsterbus/Metro) matrix and confirm every combination with genuinely distinct behaviour is
represented, not just folded under one label. Done first, below.

---

## Families reviewed (7)

### 1. Sign On & Session — thorough role×method×mode walk (priority family)

**Old suite matrix** (39 cases across NIR/Ulsterbus/Metro × Operator/Supervisor/Technician/
Administrator): Manual, Smartcard, Sign Off per role/mode, plus failure-path cases (Invalid
Credentials, Device Locked, Unlock Device) scattered across NIR-Operator, Ulsterbus-Supervisor and
Metro-Operator (not every role×mode — the old suite itself never duplicated the lockout mechanism
per combination), and a Metro-only "Sign On Messages Unavailable" case. NIR has no functional
Administrator sign-on section at all (old-suite's own asymmetry, not something the rebuild caused).

**New suite:** one generic `Sign On — by role (manual and smartcard)` (C4099913, `run for each
role`), one generic `Sign Off — by role` (C4099929), and single generalised cases for the failure
paths (`incorrect credentials` C4099921, `device locks` C4099922, `unlock with Supervisor card`
C4099923, `Communication Locked` C4099924, MOTD/W&C `Message and Word & Colour of the Day` C4099925)
plus dedicated Sign-Off-mechanism cases (`automatic (inactivity)` C4099933, `forced by power cycle`
C4099934) and `Sign On — audit events` (C4099935).

**Verdict on the failure-path folding: correctly consolidated.** The old suite's own case text for
Invalid Credentials / Device Locked / Unlock Device is near-identical regardless of which role/mode
it happened to be authored under (same "Maximum invalid Login attempts value is 3" / "Device Locked
screen is displayed" wording) — this is one universal device mechanism, not a role- or mode-specific
behaviour, so one generic case is the right level (equivalence partitioning, `test-practices.md`).

**Genuine gap found: Metro Operator's sign-on landing screen differs from NIR/Ulsterbus, and this
was dropped from the new suite entirely — including its regression pin.**
- Old suite evidence: Ulsterbus/NIR `Operator sign on - Manual/Smartcard` → expected `"Main Screen -
  Rail is displayed"` (C2691785/86, C2668237/2669055). Metro `Operator sign on - Manual/Smartcard` →
  expected `"Present Smartcard screen is displayed"` (C2691787/C2691788) — a materially different
  observable outcome, not just a data value.
- Confirmed by a real regression case: **TIBU-19559** `"POS: Signing on to Metro Home Location
  displays the incorrect Screen"` (C3560171, old suite `Confirmation Tests / 1.2.1`) — repro steps
  sign on to a Metro home location; expected result is explicitly `"POS should Display 7.1.2 Metro
  Smartcard/Please Present Smartcard Screen"`; the bug was that it showed `"2.2 Main Screen"`
  instead. This is exactly the Metro-vs-NIR/Ulsterbus landing-screen distinction, pinned by a real
  defect — and per `gherkin-standard.md`'s regression-pinning rule, a fixed defect must stay caught
  by a case with the defect linked via Refs.
- The new suite's C4099913 asserted the outcome generically as "the menu for their role is displayed"
  for every mode, with no mention of the Metro variant, and **TIBU-19559 was not referenced anywhere
  in suite 30253** (checked every case's `refs` for "19559" — zero hits). This is a silently-dropped
  distinct mode behaviour plus an un-pinned regression, not mere duplication removed.
- **Fix applied** (C4099913, `pos-completeness.rewrite.json`, `--commit`): both the manual-entry and
  smartcard THEN lines now read `"...the menu for their role is displayed (Metro Operator: the
  Please Present Smartcard screen, not a menu)"`; the Expected-result prose states the Metro
  exception and explicitly says "run... for each of NIR/Ulsterbus/Metro"; `TIBU-19559` added to
  Refs alongside the existing REQ-0050/0056/0276/2821/3013 citations. Kept as one case (not split
  into a `@mode(Metro)` case) — only the terminal screen differs, not the steps, so the standard's
  "don't fork a whole flow when one screen differs" rule applies; the mode-conditional note inside
  the Then line + the Refs pin is the right-sized fix.
- Everything else in the Sign On/Session family (roles, methods, both Sign Off mechanisms, MOTD/W&C
  fallbacks, audit events) is fully and correctly covered — no other gaps found in this family.

### 2. Faulty Card / Fare-Paying Smartcard — confirmed already fixed (not re-broken)
The 2026-06-11/12 `function-granularity-audit.md` found this family over-folded (Fare-Paying
Smartcard dropped entirely; Faulty Smartpass/Dependants Pass Receipt folded away) and proposed an
un-fold list. Re-checked live: **all of it is present now** — `Fare-Paying Smartcard — validation`
(C4102559), `— top-up` (C4102561), `Faulty — Fare-Paying Smartcard` (C4102563), `Faulty — Smartpass
Receipt` (C4102564), `Faulty — Dependants Pass Receipt` (C4102565), `Validation — passback`
(C4102560), `Top Up — on expiry` (C4102562) all exist as dedicated cases. **Fully covered** — the
earlier audit's fix landed; nothing further needed here.

### 3. Payment methods (cash / card / warrant) — fully covered
`Card Payment — pay by card`, `— back from payment`, `— declined, cancelled or error` (C4099994,
C4099995, C4100424) cover contactless/chip-PIN/swipe and explicitly name 5 decline/error reasons as
a data-variation set inside one case (declined, cancelled before PIN, too many wrong PINs, amount
too big, signature mismatch) — matches the old suite's card-payment scope (no 6th reason found in
old suite titles). Warrant Return exists per-mode (`Warrant Return` C4100422, `NIR — Warrant Return`
C4100398, `Ulsterbus — Warrant Return` C4100406) and cash is the default path throughout. **Fully
covered, correctly consolidated** — no separate case needed per decline reason (data variation, not
distinct function).

### 4. Half Fare entitlement sub-types — genuine gap found and fixed
Old suite: `Half Fare Smartcards` tested 5 distinct entitlement sub-types — **NDL, LD, PIPS, DLA,
Partially Sighted** — each × Cash/Card/Warrant payment × NIR/Ulsterbus (30 cases total, e.g.
C4069354–57/4069365 NIR, C4072941–45 Ulsterbus). FBD-100250 (Smart Card Format for Translink
Preprinted Cards) confirms these are real distinct entitlement categories (e.g. "PIPS as a new
Funded Pass"), not free-text variants of one name.

New suite has one consolidated `Smartcard — Half Fare` (C4100413) asserting the half-fare mechanism
generically ("a Half Fare entitlement smartcard is available") — **none of NDL/LD/PIPS/DLA/
Partially Sighted was named anywhere** in the case (no Data-variations line), so per the task's
definition a reader of suite 30253 has no way to know these five categories exist or need covering.
The consolidation itself (one mechanism case instead of 30 near-identical ones) is correct —
equivalence partitioning applies, since the old suite's own case text shows the mechanic doesn't
differ per sub-type — but the categories still need to be visible somewhere.

**Fix applied** (C4100413, same rewrite file, `--commit`): appended `"Data variations: NDL / LD /
PIPS / Partially Sighted / DLA Half Fare entitlement categories."` to the Expected-result field.

### 5. Youth entitlement (yLink / 24+) — fully covered
Old suite had yLink and 24+ Smartcard sub-products (Single/Return/Weekly/Monthly) × Card/Cash/
Warrant × NIR/Ulsterbus. New suite has dedicated `Smartcard — yLink` (C4100415) and `Smartcard —
24+` (C4100416), each asserting the entitlement mechanism against a worked example product. Ticket-
duration variants (Single/Return/Weekly/Monthly) aren't separately named here, but that's correct —
the product-duration dimension is already covered generically elsewhere in Tickets, and the
entitlement mechanism itself doesn't vary by ticket duration (checked against old suite: identical
mechanic across durations). **Correctly consolidated.**

### 6. Smartcard issue / product catalogue (Multi-Journey, DayLink, iLink, Metro Travelcard, BVP,
Town Service, Ulsterbus Multi-Journey) — fully covered
`Issue Card — issue from blank` (C4100024) explicitly lists **all 8 products** as a Data-variations
set: "Metro Multi-Journey, Multi-Journey, DayLink, iLink, Metro Travelcard, Belfast Visitor Pass,
Ulsterbus Multi-Journey, Town Service Travelcard" — matching the old suite's `First Issue Smartcard`
product breadth. Cross-device recognition (`Issue Card — recognised by other devices`, C4100031) and
a BVP/iLink-Zone card-options edge case (`Issue Card — blank card options`, C4100390) both carry
their original TIBU regression pins (TIBU-21446/22603/23996/26721/26722/23963 etc.). **Fully
covered, correctly consolidated** — no product silently dropped.

### 7. Cross-device card recognition — fully covered
`Issue Card — recognised by other devices` (C4100031) explicitly asserts a card issued on POS is
valid on ETM/TVM and toppable back on POS, carrying 5 TIBU regression pins from the old suite's
scattered "New Smartcards used on another device" sections. **Fully covered.**

---

## Scope disclosure — not exhaustively audited (explicit, per instruction, no silent gaps)

Given suite scale (~2193 old cases), the following were **not** individually family-audited this
pass (lower risk per the task's own prioritisation, or already covered by a prior, still-valid pass):
- **Full per-mode ticket catalogues** (NIR-only: 1/3 Off Day Return, 3 Day Select, Weekly/Monthly
  Season; Ulsterbus-only: Bus Rambler, Jobseeker Single, Month Return, Rail Substitution Service) —
  spot-checked present in `NIR (Rail) / Tickets` and `Ulsterbus / Tickets` sections by title only,
  not re-graded body-by-body (already covered by `pos-suite-restructure/old-suite-audit.md`'s
  product×mode cross-tab and the 2026-07-22 deep audit's batch B).
- **Screen Validation** (322 cases) — not re-sampled here; the 2026-07-22 deep audit already did a
  disclosed 100%-title + ~15%-full-body sample and found zero template/mode-boundary outliers. Per
  the task's own risk ranking this is the lowest-risk area (1:1 per-screen already).
- **Administrator/Technician/Supervisor functional menus beyond sign-on**, Barcode Validation,
  Refund/Annulment internals, Non-Functional (Comms/Printer/Power) — not walked family-by-family
  this pass; no specific concern raised for these and time was prioritised per the brief's ranking
  (payment methods, card/entitlement types, decline reasons, ticket/product catalogues, with Sign On
  elevated to first per George's mid-task instruction).

No family reviewed above was left partially checked without saying so; the two genuine gaps found
were both fixed and verified.

---

## Changes applied

- **File:** `C:\Users\...\scratchpad\pos-completeness.rewrite.json` (via `tools/apply_rewrite.py`,
  dry-run then `--commit`, `TESTRAIL_WRITE_SUITE_ID=30253`).
- **C4099913** `Sign On — by role (manual and smartcard)` — added the Metro Operator
  Please-Present-Smartcard landing-screen exception to both THEN lines and the Expected summary;
  added `TIBU-19559` to Refs.
- **C4100413** `Smartcard — Half Fare` — added `Data variations: NDL / LD / PIPS / Partially Sighted
  / DLA Half Fare entitlement categories` to the Expected-result field.

## Verification

`python -m system_test_ops audit --suite 30253` after commit: **CLEAN of blocking findings** — 528
cases audited, 0 blocking across every rule, 43 advisory (6 title-no-emdash, 37 title-too-long) —
identical to the pre-existing advisory count, so no new advisory findings were introduced by this
pass either.

## Result

**7 families reviewed** (Sign On/Session prioritised and walked in full per George's instruction; 6
more from the risk-ranked list: Faulty Card/Fare-Paying Smartcard, Payment methods, Half Fare
entitlements, Youth entitlements, Smartcard issue/product catalogue, cross-device recognition).
**2 genuine gaps found and fixed**: (1) Metro Operator sign-on landing screen + its TIBU-19559
regression pin, silently dropped by the generic by-role Sign On case; (2) Half Fare entitlement
sub-types (NDL/LD/PIPS/DLA/Partially Sighted) named nowhere in the consolidated Half Fare case.
**4 families confirmed fully covered / correctly consolidated** with no action needed. Audit result:
**CLEAN**, no regressions introduced. Scope gaps (ticket catalogues re-grading, Screen Validation
re-sample, remaining NFR/Admin areas) are disclosed above, not silently skipped.
