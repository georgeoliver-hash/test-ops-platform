# POS Data-variations expansion — suite 30253, 2026-07-24

**Rule applied (George, 2026-07-24, superseding the earlier "Data variations: list" guidance in
both `docs/gherkin-standard.md` and `docs/test-practices.md`):** no case may tell a tester to test
multiple variants via a named list — every genuinely distinct card/product/entitlement/payment
variant gets its own separate, individually-executable case. A `Data variations:` line is not
coverage; only one example in it was ever actually executed. This mirrors the earlier
Operator/Passenger-portal split (same test, duplicated once per variant, not one case claiming to
cover both).

## Method

1. Pulled suite 30253 (project 42) fully live via `TestRailClient.get_cases`/`get_case` — full
   body (preface/preconds/steps/expected/refs) for all 628 raw cases, excluding `ZZ_DELETE_*`.
2. Searched every case (title + preface + preconds + every step's content/expected + expected
   result) for `data variations?`, `variation —`, and a broader parenthetical-enumeration pattern
   (`<signal word> (X / Y / Z)`) to catch any equivalent phrasing not using the exact label. The
   broader sweep found **zero** additional families beyond the ones already caught by the literal
   `Data variations:` phrase — this suite's convention is consistent, so the 23 hits below are the
   full set (both today's card-variant-sweep fix and every earlier session's).
3. For each hit, read the full case body and flattened every named variant across *all* lists in
   that case (a preface parenthetical, a `Data variations:` trailer, a named sub-type list) into
   one set — not just the trailing line — since some cases (notably C4100427) named the same
   variant family in more than one place.
4. Where a case said "passenger type" / "payment" / "iLink zone" with **no explicit value list**,
   values were grounded from evidence already in the suite/spec library, never invented:
   - **payment** (vague) → `cash / card / warrant` — the only payment-method set used anywhere
     else in this suite for POS ticket sales (explicit in Single/NIR Single/Ulsterbus Single/
     Cross-Border/Top-Up); suite-internal consistency, not invention.
   - **passenger type** (vague) → `Adult / Child` — `FBD-100293` ("only Passenger Type is
     currently used … drives Adult/Child"). Where a case's *own* line explicitly names a 3rd value
     (`concession`), that explicit list was used instead and takes precedence.
   - **iLink zone** (vague) → `Zone 1 / Zone 2 / Zone 3 / Zone 4 / NW Zone` — cited to `FBD-100250`
     ("iLink zones 1-4 + NW") and `FBD-100690` ("iLink Zones 1/2/3/4/NW (nested)").
5. For each family: the **first/primary** variant reused the original case id (retitled, body
   rewritten to name that one variant, `Data variations:` line dropped from the expected result).
   The **remaining** variants became new cases in the *same TestRail section* as the original.
   Multi-dimension families (e.g. passenger type × payment) were expanded per-dimension against a
   baseline (not a full cross-product): one new case per additional value in each dimension, other
   dimension held at its baseline value — every named value gets its own trackable case without an
   explosive N×M blow-up, consistent with "minimal sufficient set" (`test-practices.md`).
6. Built via `build_pos_variant_expansion.py` (generates the rewrite/new-case JSON from templates
   — only the worked-example clause + title change per variant; the declarative When/Then steps
   are unchanged, per `gherkin-standard.md`), applied by `push_pos_variant_expansion.py`
   (dry-run confirmed 23 updates + 73 new cases with 0 errors, then `--commit`).

## Families expanded (23 families → 73 new cases)

| Original case | Section | Variants named | New cases created |
|---|---|---|---|
| **C4100427** Validation — entitlement smartcard sets the ticket type | Functional / Top Up & Validation / Validation | Concession — Senior / 60+ / ROI Senior / Blind / War Pensioner; yLink; 24+; Half-Fare — Partially Sighted / Learning Disability / No Driving Licence / PIPS / DLA; Dependants (13 total, flattened from 3 in-body lists) | 12 (C4104592–C4104603) |
| **C4100413** Smartcard — Half Fare | Functional / Smartcards | NDL; LD; PIPS; Partially Sighted; DLA (5) | 4 (C4104604–C4104607) |
| **C4100419** Single ticket | Functional / Tickets | passenger type (Adult/Child/concession) × payment (cash/card/warrant) | 4 (C4104608–C4104611) |
| **C4100420** Day Return ticket | Functional / Tickets | passenger type (Adult/Child) | 1 (C4104612) |
| **C4100421** iLink Single | Functional / Tickets | iLink zone (Z1/Z2/Z3/Z4/NW, grounded) × passenger type (Adult/Child) | 5 (C4104613–C4104617) |
| **C4100423** Family & Friends Day ticket | Functional / Tickets | payment (cash/card/warrant) | 2 (C4104618–C4104619) |
| **C4100393** NIR — Single | NIR (Rail) / Tickets | passenger type (Adult/Child/concession) × payment (cash/card/warrant) | 4 (C4104620–C4104623) |
| **C4100394** NIR — Day Return | NIR (Rail) / Tickets | passenger type (Adult/Child) | 1 (C4104624) |
| **C4100395** NIR — 1/3 Off Day Return | NIR (Rail) / Tickets | passenger type (Adult/Child) | 1 (C4104625) |
| **C4100396** NIR — Weekly Season | NIR (Rail) / Tickets | passenger type (Adult/Child, grounded) × payment (cash/card/warrant, grounded) | 3 (C4104626–C4104628) |
| **C4100397** NIR — Monthly Season | NIR (Rail) / Tickets | passenger type (Adult/Child, grounded) × payment (cash/card/warrant, grounded); TIBU-19299 regression pin kept on all 4 | 3 (C4104629–C4104631) |
| **C4100399** NIR — 3 Day Select | NIR (Rail) / Tickets | passenger type (Adult/Child, grounded) × payment (cash/card/warrant, grounded) | 3 (C4104632–C4104634) |
| **C4100400** NIR — Family & Friends Day | NIR (Rail) / Tickets | payment (cash/card/warrant, grounded) | 2 (C4104635–C4104636) |
| **C4100401** NIR — iLink Single | NIR (Rail) / Tickets | iLink zone (Z1/Z2/Z3/Z4/NW, grounded) × passenger type (Adult/Child, grounded) | 5 (C4104637–C4104641) |
| **C4100503** NIR — Cross-Border Single | NIR (Rail) / Tickets | currency (GBP/EUR) × payment (cash/warrant/card) | 3 (C4104642–C4104644) |
| **C4100504** NIR — Cross-Border Day Return | NIR (Rail) / Tickets | currency (GBP/EUR) × payment (cash/warrant/card) | 3 (C4104645–C4104647) |
| **C4100392** Top Up — Ulsterbus Multi-Journey | Ulsterbus / Top Up | payment (Cash/Warrant/Card); TIBU-26861/TIBU-21133 regression pins kept on all 3 | 2 (C4104648–C4104649) |
| **C4100403** Ulsterbus — Single | Ulsterbus / Tickets | passenger type (Adult/Child) × payment (cash/card/warrant) | 3 (C4104650–C4104652) |
| **C4100404** Ulsterbus — Day Return | Ulsterbus / Tickets | passenger type (Adult/Child) | 1 (C4104653) |
| **C4100405** Ulsterbus — Month Return | Ulsterbus / Tickets | passenger type (Adult/Child) | 1 (C4104654) |
| **C4100407** Ulsterbus — Bus Rambler | Ulsterbus / Tickets | passenger type (Adult/Child, grounded) × payment (cash/card/warrant, grounded) | 3 (C4104655–C4104657) |
| **C4100408** Ulsterbus — Family & Friends Day | Ulsterbus / Tickets | payment (cash/card/warrant, grounded) | 2 (C4104658–C4104659) |
| **C4100410** Ulsterbus — iLink Single | Ulsterbus / Tickets | iLink zone (Z1/Z2/Z3/Z4/NW, grounded) × passenger type (Adult/Child, grounded) | 5 (C4104660, C4104661, C4104662, C4104664, C4104666 — non-contiguous ids are TestRail's own allocation across the whole push batch, not a gap; verified all 5 + the primary exist in section) |

**Total: 23 original cases retitled/rewritten (one variant each, `Data variations:` line removed)
+ 73 new cases = 96 cases now covering what 23 previously did via a variation list.**

## Case count

| | Raw (incl. `ZZ_DELETE_*`) | Excl. `ZZ_DELETE_*` (audited) |
|---|---|---|
| Before | 628 | 528 |
| After | 701 | 601 |

`ZZ_DELETE_*` count unchanged at 100 — nothing was retired as part of this pass, only expanded.

## Judgement calls (not forced expansions — noted per the brief's "or leave as judgement call" allowance)

- None of the 23 hits were judged cosmetic-only; every named variant in every family names a
  card/product/entitlement/payment/zone/currency value that can independently fail (a specific
  smartcard type not recognised, a specific payment tender not accepted, a specific currency/zone
  priced wrong) — all were expanded, per George's default-to-expand instruction.
- Where a case's dimension was named without explicit values ("passenger type", "payment", "iLink
  zone"), the values used are grounded in cited specs/suite-consistency (see Method §4) rather than
  invented; this is flagged here for engineer review rather than silently asserted, in case the
  true configured set differs (e.g. if "concession" passenger pricing is later confirmed to apply
  to season products too, those would need the same expansion applied later).
- Multi-dimension families (2 named dimensions) were expanded per-dimension against a baseline,
  not as a full cross-product — e.g. Single ticket (Adult/Child/concession × cash/card/warrant)
  produced 5 cases (baseline + 2 passenger-type + 2 payment), not 9. This keeps every value
  individually trackable (George's actual requirement) without an N×M explosion that the
  "minimal sufficient set" principle in `test-practices.md` would flag as excessive.

## Verification

`python -m system_test_ops audit --suite 30253` after commit:

```
        0  mojibake
       18  title-no-emdash (advisory)
       47  title-too-long (advisory)
        0  preface-empty / preface-bad-preamble
        0  preconds-empty / preconds-no-given
        0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
        0  then-compound-genuine
        0  expected-empty / expected-starts-then
        0  has-tags
audited 601 cases: CLEAN; 65 advisory.
```

**CLEAN of blocking findings** — 0 across every blocking rule. The two advisory title checks
(title-no-emdash, title-too-long) rose slightly (new cases inherit the parent case's naming style,
several with a bracket suffix that pushes past the advisory length threshold) — reviewed and kept:
these are the same advisory categories the pre-existing suite already carried, and the bracketed
variant suffix is exactly the pattern `gherkin-standard.md` recommends ("Add a variant in brackets
only when it distinguishes the case").

## Result

**23 Data-variations families found and expanded** (all pre-existing hits, from both today's
card-variant sweep and earlier consolidation passes — a targeted broader sweep for equivalent
unlabelled variant-list patterns found no additional families). **73 new cases created**, 23
originals retitled/rewritten in place. Case count: **528 → 601** (excl. `ZZ_DELETE_*`), **628 →
701** (raw). Audit: **CLEAN**, no new blocking findings.

## Artefacts

- `proposals/coherence-audit/fixes/pos-suite-30253-raw.json` — full raw dump used for the sweep.
- `proposals/coherence-audit/fixes/_variations_full_bodies.txt` — full body of all 23 hits before rewrite.
- `proposals/coherence-audit/fixes/build_pos_variant_expansion.py` — generator (source of truth for every family's templates/variants).
- `proposals/coherence-audit/fixes/pos-variant-expansion.rewrite.json` — the 23 primary-case rewrites.
- `proposals/coherence-audit/fixes/pos-variant-expansion.new-cases.json` — the 73 new cases.
- `proposals/coherence-audit/fixes/push_pos_variant_expansion.py` — the suite-locked push script (dry-run default, `--commit` applied).
