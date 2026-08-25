# TVM variant expansion — changelog (2026-07-24)

Suite: **NEW** TVM Test Suite (30284), project 42 (TFTS - System Test). Old suites untouched
(read-only reference only).

## The rule

George: *"no test should tell someone to test multiple variants... we should have a test for each."*
Every case carrying an in-body `Data variations:` line is expanded into one separate, individually
executable case per named variant (mirrors the Operator/Passenger portal split done earlier today).
**Unaffected**: Kiosk/Astreo model and route-mode (NIR-Rail/Ulsterbus/Metro/Glider) coverage — those
stay on TestRail **Configurations**, per George's explicit carve-out. Only in-body data-value variant
lists (card scheme, entry method, entitlement/concession type, denomination, product, command,
component) are in scope.

## Comprehensive sweep (step 2)

Pulled suite 30284 in full (`TestRailClient.get_cases(42, 30284)`, all custom fields) and grepped
every `custom_preface` / `custom_preconds` / `custom_steps_seperated` / `custom_expected` field for
`Data variations` (any casing/punctuation). **74 cases matched.** Of those, **11 already live in the
`Delete` section as `ZZ_DELETE_REVIEW -` cases** (old Smartcards & ABT / Mini Statement families
pending the engineer's UI bin-cleanup) — out of scope, not touched. **63 cases** remain as genuine
in-scope candidates, grouped by family:

| Family (section) | Cases | Axis found |
|---|---|---|
| **Payments - EMV & Contactless** (887780) | 15 | card scheme / entry method — **done this batch** |
| Barcode Redemption (887776) | 6 | barcode type, invalid-field reason, malformed-entry reason, legacy-stage type, ticket layout |
| Payments - Cash incl. BNR (887777/887778/887843) | 9 | coin/note denomination, currency, jam location, Cancel/Back dismiss path |
| Sales - Tickets: Ticket Issue / Advance & 3-Day / Rail & Cross-Border (887783/4/5) | 19 | payment method, ticket product, concession type |
| Non-Functional: EMS & TMS Maintenance / Alarmboard / Resilience (887793-6) | 14 | remote command, report type, LED/sensor/component, dismiss variant |

## What was done this batch

Named in the task, plus the two new Magnetic Stripe cases checked for a further scheme split:

- **C4103658** (Chip & PIN, no PIN) → split by scheme: Visa Debit (primary, retitled in place),
  Mastercard Debit (new).
- **C4103662** (Contactless above limit → Chip & PIN fallback) → split by scheme: Visa Credit
  (primary), Visa Debit, Mastercard Credit, Mastercard Debit (new).
- **C4103665 / C4103666 / C4103667** (cancel at pinpad / timeout / print failure) → each split by
  entry method: Chip & PIN (primary), Contactless, Magnetic Stripe (new).
- **C4104129** (Magnetic Stripe valid card) — checked: yes, needs a further scheme split like the
  Chip & PIN family. Split into Visa Credit (primary), Visa Debit, Mastercard Credit, Mastercard
  Debit (new) — was previously only "Visa/Mastercard credit+debit" as one Data-variations line.
- **C4104130** (Magnetic Stripe Amex/Diners declined) — checked: split into Amex Credit (primary),
  Amex Debit, Diners Club (new).

Given all 15 cases in the **Payments - EMV & Contactless** section carried the same pattern, the
whole section was expanded in one pass rather than piecemeal:

| Original case | Axis | New/renamed cases |
|---|---|---|
| C4103657 valid Chip & PIN card | scheme | Visa Debit*, Visa Credit, Mastercard Debit, Mastercard Credit, non-GBP card (5) |
| C4103658 no PIN | scheme | Visa Debit*, Mastercard Debit (2) |
| C4103659 Amex/Diners accepted | scheme | Amex Credit*, Amex Debit, Diners Club (3) |
| C4103661 at/below contactless limit | scheme + boundary | Visa Credit*, Visa Debit, Mastercard Credit, Mastercard Debit, legacy £30 limit (5) |
| C4103662 above limit → fallback | scheme | Visa Credit*, Visa Debit, Mastercard Credit, Mastercard Debit (4) |
| C4103663 mobile wallet | wallet type | Apple Pay*, Google Pay, Samsung Pay (3) |
| C4103664 declined, retry/cancel | decline reason | acquirer decline*, unsupported issuer/scheme (2) |
| C4103665 cancel at pinpad | entry method | Chip & PIN*, Contactless, Magnetic Stripe (3) |
| C4103666 payment times out | entry method | Chip & PIN*, Contactless, Magnetic Stripe (3) |
| C4103667 print failure voids | entry method | Chip & PIN*, Contactless, Magnetic Stripe (3) |
| C4103668 expired/blocked rejected | reason | expired card*, blocked card (2) |
| C4103670 cash→card switch | stage | before cash inserted*, after cash inserted (2) |
| C4104115 card removed mid-transaction | entry method | Chip & PIN*, Contactless (2) |
| C4104129 Magnetic Stripe valid card | scheme | Visa Credit*, Visa Debit, Mastercard Credit, Mastercard Debit (4) |
| C4104130 Magnetic Stripe Amex/Diners declined | scheme | Amex Credit*, Amex Debit, Diners Club (3) |

`*` = primary variant, reuses the original case id via `match:` (retitled with the variant in
brackets, per `docs/gherkin-standard.md`'s title convention). Every other row is a new case in the
same section. **Total: 15 source cases → 46 cases (15 renamed in place + 31 new).**

Scoping notes:
- **Boundary value, not a scheme**: C4103661's "legacy £30.00 limit" is a configured-threshold
  boundary, not a card scheme, so it became its own standalone case (boundary value analysis per
  `docs/test-practices.md`'s rubric item 2) rather than crossed against all 4 schemes.
- **Mobile wallet ≠ full scheme cross**: C4103663 was split by wallet provider (Apple/Google/Samsung
  Pay), each keeping one illustrative card-scheme pairing from the original data (not a full
  wallet×scheme cross) — flagged here for visibility, not hidden.
- Refs were attributed to the specific old-suite case id per scheme where the original refs string
  named one (e.g. "C1831399 Visa Debit / C1831402 Mastercard Debit"); where the source only cited a
  range or a single "closest analogue" (e.g. C1831418 for Magnetic Stripe timeout), that ref was
  carried to the one case it actually supports and not duplicated across siblings without evidence.

## Push mechanics

- `proposals/coherence-audit/fixes/tvm-variant-expansion.cases.yaml` — 1 section (Functional /
  Payments - EMV & Contactless), 46 cases (15 `match:` renames + 31 new).
- Dry-run: `push --file ... ` (no `--update` first, confirmed as new-only; re-ran with `--update` to
  get the correct match/rename plan — 15 "would update", 31 dry-run creates).
- Commit: `push --file ... --update --commit` → 15 updated in place, 31 created (C4104561-C4104591).
- Suite case count: **215 → 246** (`system_test_ops cases --suite 30284`).

## Re-audit (step 5)

`python -m system_test_ops audit --suite 30284` (also auto-run by `push --commit`):

```
0  mojibake
0  title-no-emdash (advisory)
57 title-too-long (advisory)
0  preface-empty / preface-bad-preamble
0  preconds-empty / preconds-no-given
0  steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
0  then-compound-genuine
0  expected-empty / expected-starts-then
0  has-tags
audited 219 cases: CLEAN; 57 advisory.
```

**CLEAN of blocking findings.** The 57 `title-too-long` hits are advisory (per
`docs/test-practices.md`) — several of today's titles carry a bracketed variant suffix
(`(Mastercard Debit)`, `(non-GBP issued card)`) which pushes some titles past the advisory length
threshold; reviewed and kept, since the bracket is exactly the gherkin-standard's own convention for
"add a variant in brackets only when it distinguishes the case."

## Not done this batch — scoped as a follow-up (48 cases, 4 families)

The sweep above found the *same* pattern in four more families (table above). These were **not**
expanded in this pass — the task named the EMV/Payments family explicitly and asked to check the 2
Magnetic Stripe cases; doing those thoroughly and correctly, with per-case refs attribution and a
real conformance/audit loop, filled this session. Rather than rush ~150 additional cases across
domains this pass didn't re-ground against the underlying specs (rail fares FBD-100450, cash
hardware REQ-0339.x, EMS/alarmboard non-functional behaviour), the axis choice for each remaining
family is recorded here so a follow-up batch can execute directly without re-auditing:

- **Barcode Redemption** (6 cases) — split by: barcode type B/D/E/H/S/U (C4103620, 6-way); add a
  new "value below limit validated offline" case alongside the existing above-limit case (C4103624,
  the Data-variations line names both outcomes but only "above" exists as a case); invalid-field
  reason (C4103625, 4-way: To Station/From Station/Product Type/dates); malformed-entry reason
  (C4103626, 4-way: no characters/incomplete/over-length/invalid character); legacy-stage barcode
  type (C4103627, 3-way: B/E/U); ticket layout (C4103633, 8-way: Single/Day Return/3 Day
  Select/Cross Border/Half-fare/yLink/24+/Family).
- **Payments - Cash** (9 cases) — split by: coin denomination (C4103637, 3-way: old £1/2p/1p);
  foreign-currency class (C4103638, 2-way: Euro/other); issuing bank (C4103639, 5-way: BoE/BoI/
  Ulster/Danske/First Trust — denomination×series folded into each bank's worked example, not fully
  crossed); withdrawn-note denomination (C4103640, 3-way: £5/£10/£20); C4103641 keep as-is (Scottish
  accepted) + add one new "non-sterling banknote rejected" case (mirrors the coin-rejection pair,
  same reasoning as C4103624 above); jam location (C4104116/C4104117, 3-way each: coin-during-
  payment/note-during-payment/coin-during-change); Cancel/Back dismiss path (C4103650/C4104113,
  2-way each).
- **Sales - Tickets** (19 cases) — split by **payment method** {cash, card, contactless} where that
  is the only data axis beyond mode/passenger (C4103680-4103686, 4103688, 4103689, 4103694,
  4103696, 4103698, 4103699 — mostly 3-way); split by **ticket product** where product is the named
  axis (C4103687 Day/Day Return/1 Month Return 3-way; C4103697 Day Return/Weekly/Monthly/1-3-off Day
  Return/Day Tracker 5-way; C4103700 Day Return/Weekly/Monthly/1 Month Return 4-way; C4103701
  Single/1 Month Return 2-way); split by **concession type** (C4103702, 5-way: Senior/ROI Senior/
  Blind/War Pensioner/60+); C4103691 keep as-is + add one new case for the Cross Border/Family &
  Friends/concession multi-use-barcode exception behaviour. **Passenger type (Adult/Child) is
  treated as an equivalence class, not split** — same code path/screen, differs only by which fares-
  export price is looked up, not a credential/scheme/product that fails independently; each
  surviving case keeps one concrete passenger (Adult) in its worked example.
- **Non-Functional** (14 cases) — split by the named command/component list in each: C4103755
  reboot/de-activate/re-activate (3-way); C4103757 report type (3-way); C4103766 increase/decrease
  brightness (2-way); C4104118 burglary-trigger scenario (4-way); C4104121 with/without General
  Reboot (2-way); C4103769 LED type (2-way); C4103772 door state/sensor test (2-way); C4103775
  printer model TL80/IML5 (2-way); C4103779 cassette-reload method (2-way); C4103780 degraded
  hardware component (3-way); C4103786 ticket type at lockout (2-way); C4103796 Bus/Rail home
  (2-way); C4103797 payment-input audio feedback (3-way); C4103798 workflow (2-way).

Estimated additional yield if executed: ~146 new/renamed cases across these 48 sources (net suite
size after both batches: roughly 215 + 31 + ~98 net-new ≈ 344 cases). Recommend a dedicated follow-up
PR per family so each can get its own grounding check and audit pass, rather than one very large
diff.
