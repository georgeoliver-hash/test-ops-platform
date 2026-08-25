# POS operating-mode coverage map (Refs tagging)

**Why this doc exists.** POS is structured **mode-first** (Functional-Shared / NIR (Rail) / Ulsterbus
/ Metro, per `structure.md`) and executed via TestRail **Run Configurations**. That section split
already tells you, for free, which mode a case filed under NIR/Ulsterbus/Metro belongs to. What it
does **not** tell you is whether a case filed in the **shared** Functional/Non-Functional areas is
genuinely mode-irrelevant (safe to run once, under whichever mode the tester picks as primary) or
whether its outcome could still plausibly differ mode-to-mode even though the steps read identically.
Re-running every shared case under all three Configurations wastes tester time on things like Sign On
or Technician Menu, which cannot differ by mode — but skipping the wrong ones (fares, products,
payment, capping) would quietly lose coverage. This doc is the tally and the reasoning behind the
Refs tag every case in suite 30253 now carries, so that judgement is recorded once and doesn't have
to be re-litigated per run.

## The tag scheme

Every case's Refs field carries exactly one classification tag (or, where the case's own text names a
genuine 2-of-3 mode subset, two single-mode tags together — see "2-of-3 mode subsets" below):

- **`MODE-ALL`** — shared case, procedure identical, but the OUTCOME could plausibly differ by mode
  (fare amount, ticket/product, payment method, capping, mode-specific config). Run under every mode.
- **`MODE-NIR-ONLY`** / **`MODE-ULSTERBUS-ONLY`** / **`MODE-METRO-ONLY`** — mode-specific. Applied both
  to cases already filed in the NIR (Rail)/Ulsterbus/Metro sections (no judgement needed — the section
  already says so) and to cases in a shared section whose own content names a specific mode (e.g. a
  Screen Validation case for a "…Metro" screen, or a Customer Display case explicitly for Rail).
- **`MODE-PRIMARY-ONLY`** — shared AND genuinely mode-irrelevant (pure UI/menu/auth/hardware/non-fare
  mechanics; the mode cannot affect the outcome at all). Only needs running once, under whichever mode
  the tester picks as primary.

### 2-of-3 mode subsets (an extension worth flagging)

A meaningful chunk of shared cases (215 of 601) aren't cleanly "every mode" or "one mode" — their own
precondition text explicitly scopes them to **exactly two** of the three modes, most commonly "NIR or
Ulsterbus" with Metro explicitly excluded (Metro is cash-only with no card payment and no smartcard
validation), or "Ulsterbus or Metro" (a bus-only concept like Fare Stage or a bus-basket rule, which
NIR/rail doesn't have). Tagging these `MODE-ALL` would be actively misleading (it would send a tester
to run a card-payment case under Metro, where the precondition can't even be met); tagging them
`MODE-PRIMARY-ONLY` would silently drop a genuinely mode-varying case down to a single run. Neither fit
the 3-value scheme as literally written, so these cases carry **both** applicable single-mode tags
together (e.g. `MODE-NIR-ONLY,MODE-ULSTERBUS-ONLY`) — same comma-separated Refs convention as
citations, just two mode tags instead of one. Flagging this as a deliberate, evidence-grounded
extension to the scheme rather than a silent deviation — worth George's sign-off if the convention
should be named differently going forward (e.g. a dedicated `MODE-NIR-UB` shorthand).

## Tally (601 cases classified, `ZZ_DELETE_*`/bin-review cases excluded)

| Tags | Count | What it covers |
|---|---:|---|
| `MODE-PRIMARY-ONLY` | 294 | Auth/session, menus, admin/technician config, printer/comms/power resilience, most Screen Validation (pure UI render checks with no mode-named screen), generic refund mechanics |
| `MODE-NIR-ONLY` | 105 | Filed in NIR (Rail) (56) + Rail-only shared cases: Screen Validation "Fare Look-Up — Rail" (23), Barcode print/scan/validate family (12), 2 Numerical Input/Operator screen exceptions, 1 Sign On screen exception |
| `MODE-NIR-ONLY` + `MODE-ULSTERBUS-ONLY` | 49 | Tickets (17), Smartcards/entitlement fare application (8), Top Up & Validation/Validation (20, Metro explicitly has no smartcard validation), Card Payment (3, Metro is cash-only), Receipts/day summary (1) |
| `MODE-ULSTERBUS-ONLY` + `MODE-METRO-ONLY` | 54 | Screen Validation "Fare Look-Up — Bus" (40, shared bus screen family) + Functional Fare Look-Up/Fare-Stage (3, bus-only concept) + assorted per-case bus-screen exceptions (11) |
| `MODE-ULSTERBUS-ONLY` | 46 | Filed in Ulsterbus (32) + Revenue Allocation (1) + Technician Default Boarding Stage (1) + assorted per-case Screen Validation exceptions naming Ulsterbus specifically (12) |
| `MODE-ALL` | 46 | Basket & Payment (Annulment 8, Basket 5, Cash Payment 2, Receipts 4), Fare Look-Up/Common (2), Issue Card (3), Top Up & Faulty Card (5+8=13), Customer Displays generic case (1), Numerical Input/group ticket (1), Refund's 2 mode-varying cases, Mini Statement (1), Smoke (4) |
| `MODE-METRO-ONLY` | 7 | Filed in Metro (3) + assorted per-case Screen Validation exceptions naming Metro specifically (4) |

**Total: 601.** (294 + 105 + 49 + 54 + 46 + 46 + 7 = 601.)

## How the shared-section calls were made

Read every shared case's actual preface/preconditions/steps (not just its title) and grouped by
functional area, per `docs/test-practices.md`'s "systematic by section/area" guidance:

- **Sign On & Session (all subsections), Operator/Break Mode/Options/Ticket History/Totals,
  Supervisor, Technician (all but one), Administrator, Comms & Status, Non-Functional resilience
  sections (Comms/Stability/Power/Printer)** — read in full; zero fare/product/payment dependency in
  any case body → `MODE-PRIMARY-ONLY` across the board.
- **Basket & Payment, Top Up & Validation, Issue Card, Fare Look-Up/Common, Smartcards, Tickets,
  Refund (2 of 12), Revenue Allocation** — fare/product/payment/audit-field content, differs by mode
  in ways confirmed by the case text itself (explicit "NIR or Ulsterbus mode", "Metro is cash-only",
  "Metro has no smartcard validation", route/allocation fields that differ by mode) → `MODE-ALL` or the
  explicit 2-of-3 subset per the evidence in that case.
- **Refund (10 of 12)** — read in full; despite being money-related, the actual behaviour under test
  (URN/PRN format, amount-vs-sale-value boundaries, role restriction, "final and cannot be annulled")
  is generic verification logic that doesn't vary by which mode sold the original ticket →
  `MODE-PRIMARY-ONLY`. Only the 2 cases whose text names a mode-specific field (the Ulsterbus Route
  Variant Id vs NIR Route Reference Id audit mapping; the CR115 cross-device refund) got `MODE-ALL`.
- **Non-Functional / Screen Validation** — default `MODE-PRIMARY-ONLY` (a screen-render check against
  the approved design doesn't depend on mode). Two whole sub-sections are already mode-split by their
  own name ("Fare Look-Up — Bus" / "— Rail"); within every other Screen Validation section, a case
  whose *screen name itself* names a mode (`_Metro`, `Ulsterbus …`, `Rail-…`, a bare `Bus …`) only
  renders in that mode, so it was pulled out of the section default and tagged for that mode instead.
- **Barcode Scanning + Barcode Validation** — reclassified from an initial "generic, MODE-ALL" guess to
  `MODE-NIR-ONLY` after reading the full family: every case's worked example is a **Rail** single-use
  barcode (types B/U/E/S/D/H, Corethree sync, scheme id 5720); no case anywhere in the family uses a
  bus example. No case explicitly states "other modes don't support barcodes," so this is grounded
  inference from consistent example evidence, not a stated exclusion — **flagged for engineer
  confirmation**, not asserted as certain.

## Flagged for engineer confirmation (18 cases, not guessed past their evidence)

These got a real, evidence-based classification but rest on an inference worth a second pair of eyes
before being treated as settled:

- **C4100507** `Technician — set Default Boarding Stage` → `MODE-ULSTERBUS-ONLY`. Precondition says
  "(Ulsterbus)" explicitly; unclear whether Metro has an equivalent zone-based default that this case
  (or a sibling) should also cover — possible coverage gap, not just a tagging call.
- **C4103578–4103580** (Fare-Stage Selection, 3 cases) → `MODE-ULSTERBUS-ONLY,MODE-METRO-ONLY`. Fare
  Stage is a bus fare-lookup concept; confirm NIR genuinely has no Fare Stage equivalent (it uses
  station-to-station) before treating this split as final.
- **C4100033** `Customer Display — passenger display` → kept `MODE-ALL` rather than assumed to be "the
  missing Metro variant" alongside its Rail/Ulsterbus siblings (C4100499/C4100500) — no text in the
  case supports guessing which mode it was meant to be, so it stayed broad instead of being narrowed
  on a guess.
- **C4100034, C4100035, C4100439, C4100440, C4103570–4103577** (12 cases, Barcode Scanning + Barcode
  Validation families) → `MODE-NIR-ONLY`. See reasoning above — grounded on consistent Rail-only
  examples across the whole family, but no case states the exclusion outright.
- **C4103582** `Revenue Allocation — a rail ticket sold on an Ulsterbus POS...` → `MODE-ULSTERBUS-ONLY`.
  The scenario is specifically about an Ulsterbus-home POS; tagged by the POS's own mode, though the
  case's subject matter (NIR revenue allocation) crosses both.

## Keeping this accurate

Regenerate this tally whenever cases move sections, a new mode-specific case is added, or an old case
is split/merged. If a new shared case is authored, classify it the same way at authoring time (read
the actual behaviour, not the title) and set its Refs tag before it's pushed — don't leave a
newly-authored case untagged for a later sweep to catch.
