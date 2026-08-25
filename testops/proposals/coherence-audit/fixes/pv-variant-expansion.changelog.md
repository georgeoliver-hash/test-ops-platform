# PV Acceptance Suite (30255) — variant expansion, 2026-07-24

**Mandate (George, 2026-07-24, a hard rule, superseding the earlier "list variants in one case"
guidance in both `docs/gherkin-standard.md` and `docs/test-practices.md`):** "no test should tell
someone to test multiple variants... we should have a test for each." Every case carrying a
`Data variations:`/`Variation —` line naming several distinct products, schemes, entitlements, or
decline reasons must be **expanded into one separate, individually-executable case per named
variant** — a bundled list is not equivalent coverage, only one example ever actually gets run.
Mirrors the Operator/Passenger Portal split done earlier in the ABT suite.

## Method

1. Re-read `CLAUDE.md`, `docs/gherkin-standard.md` and `docs/test-practices.md` in full, focusing on
   the 2026-07-24 sections that state the new rule and retire the old "Data variations as an
   Examples list" guidance.
2. Pulled suite 30255 fully and fresh (`TestRailClient.get_cases(42, 30255)`, full body: title,
   refs, `custom_preface`/`preconds`/`steps_seperated`/`expected`) — 136 cases before this session,
   excluding the 1 pre-existing `ZZ_DELETE_REVIEW` condemned case.
3. Grepped every case body for `Variation`, `Data variations`, and the known product/entitlement
   vocabulary (Concession SmartPass sub-types, card schemes, decline conditions, etc.), then read
   each hit's full body (not just the `custom_expected` summary line).
4. Cross-checked the 11-case Smartcard Validation family against
   `proposals/pv-suite-restructure/smartcard-validation.cases.yaml` and `coverage-map.md` to confirm
   the full named sub-type list per family, per today's task brief.
5. For each hit, split the bundled list into one case per named variant: the first/primary variant
   reuses the original case id (retitled + body trimmed to that one variant, keeping its existing
   worked example untouched where already product-specific); the remaining variants become new
   cases in the same section, built from the same body pattern with the product name swapped in
   (no invented detail — every new case's precondition/steps/expected mirrors the already-cited
   pattern and Refs of its family).
6. Applied via `tools/apply_rewrite.py proposals/coherence-audit/fixes/pv-variant-expansion.rewrite.json`
   (11 in-place edits; dry-run then `--commit`) and a bespoke
   `proposals/coherence-audit/fixes/push_pv_variant_expansion.py` (47 new cases; dry-run then
   `--commit`) — mirroring the existing `push_abt_portal_split.py` pattern, suite-locked via
   `TestRailWriter`/`TESTRAIL_WRITE_SUITE_ID=30255`.
7. Re-ran `python -m system_test_ops audit --suite 30255`.

## Families found and expanded

### Group A — 11-case Smartcard Validation family (+ adjacent Rail-specific case)

| Case | Primary (kept id, retitled) | New cases created |
|---|---|---|
| C4100981 Concession SmartPass | 60+ | Blind (C4104432), Senior (C4104433), ROI Senior (C4104435), War Pensioner (C4104436) |
| C4100982 Half-Fare SmartPass | DLA | Learning Disability (C4104438), No Driving Licence (C4104440), PIPS (C4104442), Partially Sighted (C4104444) |
| C4100984 Metro Multi-Journey | City zone | Inner zone (C4104446), Extended zone (C4104448) |
| C4100987 iLink | Zone 4 (Botanic) | Zone 1 (C4104450), Zone 2 (C4104451), Zone 3 (C4104453), NW (C4104455), Belfast Visitor Pass (C4104457) |
| C4100989 yLink or 24+ | yLink (title/body de-bundled from "or 24+") | 24+ (C4104459) |
| C4100990 Translink Employee | Staff | Staff Partner (C4104461), Retired Staff (C4104464), External Staff (C4104465), Dependents Pass (C4104467) |
| C4100991 EA Smartpass (title bundled "Pupil and Further Education") | Pupil | Further Education (C4104469) |
| C4100996 Rail — NIR transfer validation | iLink | Belfast Visitor (C4104471), Staff Smartpass (C4104473), aLink (C4104475), EA Pupil (C4104477), EA Further Education (C4104478) — the old "EA Pupil/FE" list item was itself 2 bundled names, split accordingly |

26 new cases in this group.

### Group B — card-scheme / product-type lists outside the smartcard family

| Case | Primary (kept id, retitled) | New cases created |
|---|---|---|
| C4100998 ABT — contactless tap validation | Visa Debit | Visa Credit (C4104480), Mastercard Debit (C4104482), Mastercard Credit (C4104484), Maestro (C4104486), mobile wallet (C4104487) |
| C4101006 Barcode — multi-use validation | Adult | Child (C4104489), 3 Day Select (C4104491), 1/3 Off Day Return (C4104493), 24+ (C4104495), Ylink (C4104496), Concession (C4104498), Half Fare (C4104500), Day Tracker (C4104501), Unemployed Day Return — HHD only (C4104503) |

14 new cases in this group. Each barcode case carries its own already-cited audible beep-pattern
fact (TIBU-27324/old-suite C4091912) instead of the shared enumeration line the old consolidated
case used — distributing an existing sourced fact per product, not inventing one.

### Group C — cEMV decline reasons (C4101088), found via the comprehensive sweep, not on the known list

`cEMV — decline reasons and route-type enablement` bundled 7 named decline conditions (card not
read, unsupported scheme e.g. AMEX or Diners, expired, ODA fail, on BIN list, on Deny list, card
clash) behind **one** generic `WHEN`/`THEN` step ("present a card that hits one of those decline
conditions") — the same anti-pattern in a different guise: a decline can be reason-specific, and
only one example ever actually got exercised. Split into 7 dedicated decline-reason cases
(C4104505, 4104507, 4104509, 4104510, 4104512, 4104513, 4104515). The original case (C4101088) is
retitled to `cEMV — route-type enablement and passback distinctness` and keeps the 3 remaining
behaviours (route enablement, route disablement, passback-vs-decline) that were already correctly
tested as one flow — those are genuinely one behaviour walked end-to-end, not a variant list, per
`docs/test-practices.md` rubric step 5.

## Scope decisions (documented, not silently dropped)

- **Glider/Rail Configuration axis** — untouched, per the task brief: TestRail Configurations
  already cover this dimension; none of the "Run under Glider and Rail" phrasing was expanded.
- **Adult/Child axis** — left as the existing secondary dimension on every family case (an age-tier
  of the same product/entitlement code, not a distinct product), matching how the task's own known
  examples (card schemes, barcode products, entitlement sub-types) never mention Adult/Child.
  Flagged here explicitly rather than silently left out: **if this is later judged a genuine
  independent-failure axis, it is a follow-up expansion, not a gap missed by this pass.**
- **Metro Daylink (C4100983), Metro Travelcard (C4100985), Ulsterbus Multi-Journey (C4100986),
  aLink (C4100988)** — not expanded. Each names only the Adult/Child axis (no further product/
  entitlement sub-type list), so nothing to split per this rule.
- **`Validation — invalid reasons displayed` (C4100992)** — lists several invalid *reasons* in its
  `custom_expected` summary, but the case body already exercises them via the standard "flow with a
  seeded card per condition" pattern (rubric step 5, a distinct-branch enumeration test, not a
  card/product-variant list), consistent with how the passback/offline/machine-not-in-service cases
  are structured. Left as-is.

## Result

- **47 new cases created**, **11 existing cases edited in place** (retitled + body trimmed to their
  primary variant) — **0 cases removed/retired**.
- Suite count: **136 → 183** (before/after this session), **182 non-condemned** (1 pre-existing
  `ZZ_DELETE_REVIEW` unrelated to this pass).
- **`python -m system_test_ops audit --suite 30255`: CLEAN of blocking findings** — 182 cases
  audited, 0 blocking across every rule, 45 advisory (32 `title-no-emdash`, 13 `title-too-long`,
  pre-existing and unrelated to this pass — no new advisory findings introduced by the new/edited
  cases beyond the pre-existing baseline count staying proportionate to the larger suite).
- **Old suite 10047: untouched** (read-only throughout, never queried for write).

## Files

- `proposals/coherence-audit/fixes/build_pv_variant_expansion.py` — generator for the rewrite +
  new-cases payloads (documents the expansion logic and scope decisions in code comments).
- `proposals/coherence-audit/fixes/pv-variant-expansion.rewrite.json` — the 11 in-place edits,
  applied via `tools/apply_rewrite.py`.
- `proposals/coherence-audit/fixes/pv-variant-expansion.new-cases.json` — the 47 new cases.
- `proposals/coherence-audit/fixes/push_pv_variant_expansion.py` — the pusher for the new cases
  (mirrors `push_abt_portal_split.py`).
- `proposals/coherence-audit/fixes/pv-variant-expansion.changelog.md` — this file.
- `proposals/coherence-audit/fixes/pv-suite-30255-full-20260724.json` — full raw case dump used for
  this session's sweep (scratch, not authoritative going forward).
