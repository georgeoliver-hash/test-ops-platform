# TVM variant expansion — changelog, batch 2 (2026-07-24)

Suite: **NEW** TVM Test Suite (30284), project 42 (TFTS - System Test). Follow-up to
`tvm-variant-expansion.changelog.md` (batch 1: Payments - EMV & Contactless, 15→46 cases). This
batch executes the 4 families batch 1 scoped but did not action: Barcode Redemption, Payments -
Cash incl. BNR, Sales - Tickets, Non-Functional. Old suites untouched throughout (read-only
reference only). Same rule as batch 1: George's hard rule that every genuinely distinct
`Data variations:` variant gets its own separate, individually-executable case (see
`docs/test-practices.md` / `docs/gherkin-standard.md`, both 2026-07-24 sections).

## Step 1 — verified live before touching anything

Pulled suite 30284 fresh (`TestRailClient.get_cases(42, 30284)` — 246 cases — and
`get_sections(42, 30284)` — 25 sections) rather than trusting batch 1's case-id table. Confirmed:
section ids and names in the changelog table still match live (887776 Barcode Redemption, 887777/
887778/887843 Payments - Cash + its two Note Recycler & Change sub-sections, 887783/887784/887785
Sales - Tickets sub-sections, 887793-887796 Non-Functional sub-sections). All 48 case ids named in
the batch-1 changelog were re-dumped in full (title/refs/preface/preconds/steps/expected) and their
content, including the exact `Data variations:` wording, matched the changelog's table exactly — no
drift since batch 1. This confirmed the axis choices documented in batch 1 were safe to execute
directly, per the task's "verify it's still correct against live content" instruction.

## What was done — per family

### Barcode Redemption (887776): 6 → 27 cases

| Original | Axis | New/renamed |
|---|---|---|
| C4103620 valid booking reference collects | barcode type | Type B*, D, E, H, S, U (6) |
| C4103624 above-limit refused offline | **kept as-is** + new sibling | above-limit (unchanged) + below-limit validated offline (new) (2) |
| C4103625 invalid booking reference rejected | invalid-field reason | invalid To Station*, From Station, Product Type, dates (4) |
| C4103626 malformed reference rejected | malformed-entry reason | incomplete entry*, no characters, over-max length, invalid character (4) |
| C4103627 legacy-stage resolves | legacy-stage barcode type | Type B*, E, U (3) |
| C4103633 ticket prints barcode layout | ticket layout | Single*, Day Return, 3 Day Select, Cross Border, Half-fare, yLink, 24+, Family (8) |

`*` = primary variant, reuses the original id via `match:`. Primary variant chosen to match what the
**source case's own body already described** where it named one concretely (e.g. C4103625's
precondition already said "whose station does not match the product" → mapped to "invalid To
Station"; C4103626's precondition already said "shorter than the required length" → mapped to
"incomplete entry"); where the source was generic (C4103620, C4103627, C4103633), the first-named
variant in the Data-variations list was used as primary.

Push: `tvm-variant-expansion-2-barcode.cases.yaml` → dry-run (6 would-update, 21 dry-run creates),
`--commit` → 6 updated in place, 21 created (C4104806-C4104826... consecutively, with gaps where
other suites/batches also wrote in the same id range). Suite count 246 → 273 after this family's
audit run (240 excl. `ZZ_DELETE_REVIEW`).

### Payments - Cash incl. BNR (887777 / 887778 Astreo-only / 887843 Kiosk-only): 9 → 25 cases

| Original | Axis | New/renamed |
|---|---|---|
| C4103637 out-of-circulation/sub-value coins rejected | coin denomination | old round £1*, 2p, 1p (3) |
| C4103638 foreign coins rejected | currency class | Euro*, other non-sterling (2) |
| C4103639 valid banknote any orientation | issuing bank | Bank of England*, Bank of Ireland, Ulster Bank, Danske Bank, First Trust Bank (5) |
| C4103640 withdrawn paper notes rejected | denomination | £10* (matches original example), £5, £20 (3) |
| C4103641 Scottish banknote accepted | **kept as-is** + new sibling | Scottish (unchanged) + non-sterling banknote rejected (new) (2) |
| C4104116 jam cleared successfully | jam location | coin-during-payment*, note-during-payment, coin-during-change (3) |
| C4104117 jam cannot be cleared | jam location | coin-during-payment*, note-during-payment, coin-during-change (3) |
| C4103650 BNR note left non-functional (Astreo) | dismiss path | Cancel*, Back (2) |
| C4104113 BNR note left functional (Kiosk) | dismiss path | Cancel*, Back (2) |

Push: `tvm-variant-expansion-2-cash.cases.yaml`, 3 section blocks (Payments - Cash + its two
Note Recycler & Change sub-sections, resolved correctly to existing section ids 887777/887778/
887843). Dry-run (8 would-update, 17 creates) → `--commit` (8 updated, 17 created, C4104831-
C4104846 plus one gap-fill). Post-audit count: 256 cases (excl. deleted).

### Sales - Tickets: Ticket Issue / Advance & 3-Day / Rail & Cross-Border (887783/4/5): 19 → 60 cases

Mode (`NIR-Rail/Ulsterbus/Metro/Glider`) and Kiosk/Astreo model stayed untouched (Configurations) —
every source Data-variations line in this family named mode/model **alongside** a data-value axis;
only the data-value axis was split, per the carve-out.

- **Payment-method split (3-way: cash / card Chip&PIN / contactless)** — the only in-scope axis for
  13 cases: C4103680 (generic Ticket Issue), 681 (Adult single), 682 (Child single), 683 (F&F day),
  684 (F&F additional child), 685 (Popular shortcut), 686 (Evening), 688 (Bus Rambler), 689
  (concessionary half-fare), 694 (3-Day), 696 (NI Rail Adult single), 698 (NI Rail 3-Day Select), 699
  (Cross-Border Adult single). Each → 3 cases (1 renamed + 2 new) = 39 cases from 13 sources.
- **Product-axis split (not crossed with payment)**: C4103687 Day/Day Return/1 Month Return (3-way,
  1+2), C4103697 Day Return/Weekly/Monthly/1-3-off Day Return/Day Tracker (5-way, 1+4), C4103700 Day
  Return/Weekly/Monthly/1 Month Return (4-way, 1+3), C4103701 Single/1 Month Return (2-way, 1+1).
  4 sources → 14 cases.
- **Concession-axis split**: C4103702 Senior/ROI Senior/Blind/War Pensioner/60+ (5-way, 1+4) → 5
  cases.
- **C4103691 (kept as-is) + 1 new sibling**: the Data-variations note here describes a genuinely
  *different behaviour* (Cross Border/Family & Friends/concession products print a **multi-use**
  barcode, vs the standard single-use barcode), not another value of the same behaviour — so it was
  split as a distinct case per the rubric's step-3 test, not folded into the payment/product pattern.
- **Passenger type (Adult/Child) was NOT split** — same equivalence-class reasoning as batch 1's
  rule: same code path/screen, differs only in which fares-export price is looked up. Each surviving
  case keeps one concrete passenger in its worked example (Adult, per the source cases' own
  examples).

Push: `tvm-variant-expansion-2-sales.cases.yaml`, 3 section blocks. Dry-run (19 would-update, 41
creates) → `--commit` (19 updated, 41 created, C4104847-C4104887). Post-audit count: 297 cases.

### Non-Functional: EMS & TMS Maintenance / Alarmboard / Coin Recycler Hopper / Resilience
(887793-887796): 14 → 34 cases

| Original | Axis | New/renamed |
|---|---|---|
| C4103755 remote reboot/de-activate/re-activate | command | reboot*, de-activate, re-activate (3) |
| C4103757 EMS cash reports | report type | Cash Collection*, Bank Note Collection, Coins Reload (3) |
| C4103766 backlight persists | direction | increase*, decrease (2) |
| C4104118 burglary event | trigger scenario | hopper door*, 3 failed logins, TVM door after 3 fails, TVM door no login (4) |
| C4104121 EMS exit to Sales | reboot option | without General Reboot*, with General Reboot (2) |
| C4103769 alarmboard LED test | LED type | ticket-tray*, payment (2) |
| C4103772 alarmboard door/sensor test | test type | door state*, sensor (2) |
| C4103775 printer alignment | printer model | TL80*, IML5 (2) |
| C4103779 hopper reload updates content | reload method | full-cassette*, empty-then-correct (2) |
| C4103780 payment hardware failure → amber | component | Ingenico card reader*, coin selector, banknote acceptor (3) |
| C4103786 lockout at limit | ticket type | paper*, discounted (2) |
| C4103796 multi-modal home | Bus/Rail | Bus*, Rail (2) |
| C4103797 speech prompts + payment feedback | payment-input type | cash*, card, contactless (3) — the shared workflow-speech-prompt step is repeated on every sibling; only the payment-feedback line varies |
| C4103798 workflow launch performance | workflow | Quick Select*, Buy Other Tickets (2) |

Push: `tvm-variant-expansion-2-nonfunc.cases.yaml`, 4 section blocks (EMS & TMS Maintenance,
Alarmboard & Enclosure/Kiosk only, Coin Recycler Hopper/Kiosk only, Resilience — all resolved to
their existing nested section ids). Dry-run (14 would-update, 20 creates) → `--commit` (14 updated,
20 created, C4104888-C4104910). Post-audit count: 317 cases.

## Grounding notes

- No further spec/old-suite lookups (`tools/extract_req.py`, old-suite `get_cases`) were needed
  beyond what batch 1 already did: every split in this batch is a same-behaviour, different-value
  split (a coin denomination, a card scheme label, a command name, a report name) where the source
  case's own body already supplied the full mechanics and the Data-variations line supplied the
  exhaustive name list — nothing was invented, and no variant's mechanics were suspected to differ
  materially from its siblings. The two exceptions that needed a "does this differ in kind, not just
  value" judgement (C4103624/below-limit sibling, C4103641/non-sterling sibling, C4103691/multi-use
  sibling) were each grounded directly in the **opposite outcome already named in the same case's own
  Data-variations or Expected text** (e.g. C4103624's own line named both "value below limit
  validated offline / value above limit refused" — the below-limit case is not invented, it's the
  other half of a pair the source case already asserted existed).
- Refs: where the source case cited a single shared FBD/REQ (not a per-variant old-suite id, unlike
  the EMV family in batch 1), the same refs were carried to every sibling — there was no more
  granular per-variant citation available in the live suite to split further.

## Totals

| Family | Before | After | New cases |
|---|---|---|---|
| Barcode Redemption | 6 | 27 | 21 |
| Payments - Cash (+ 2 sub-sections) | 9 | 25 | 16 |
| Sales - Tickets (3 sub-sections) | 19 | 60 | 41 |
| Non-Functional (4 sub-sections) | 14 | 34 | 20 |
| **Total this batch** | **48** | **146** | **98** |

Suite total: 246 (start of this batch, i.e. after batch 1) → **344** (`system_test_ops cases --suite
30284`, confirmed).

## Re-audit (final, after all 4 families)

`python -m system_test_ops audit --suite 30284`:

```
0    mojibake
0    title-no-emdash (advisory)
100  title-too-long (advisory)
0    preface-empty / preface-bad-preamble
0    preconds-empty / preconds-no-given
0    steps-empty / step-first-not-when / step-content-not-when-and / step-no-then
0    then-compound-genuine
0    expected-empty / expected-starts-then
0    has-tags
audited 317 cases: CLEAN; 100 advisory.
```

**CLEAN of blocking findings** (317 = 344 minus the `ZZ_DELETE_REVIEW` cases the audit excludes from
its count). The 100 `title-too-long` advisories are the expected consequence of adding a bracketed
variant suffix to titles that were already close to the length threshold — reviewed, same rationale
as batch 1: the bracket is the standard's own convention for "add a variant only when it
distinguishes the case," not a defect.

## Combined status (batch 1 + batch 2)

All 5 families the original comprehensive sweep found (74 candidates, 11 out of scope in `Delete`,
63 genuine) are now complete: Payments - EMV & Contactless (batch 1, 15→46), Barcode Redemption,
Payments - Cash, Sales - Tickets, Non-Functional (this batch, 48→146). Suite 30284 grew from 215
(pre-batch-1) to 344 cases across both batches. No further `Data variations:` follow-up remains
outstanding from the original sweep.
