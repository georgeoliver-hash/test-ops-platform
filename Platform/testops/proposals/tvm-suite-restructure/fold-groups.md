# TVM Suite — Itemized Fold Groups

Companion to `consolidation-audit.md`. Every group below: **keeper** (the case that survives,
enriched with an Examples/data table covering the absorbed variants) + **absorbed** (retired as
`ZZ_DELETE_REVIEW -`, moved to `ZZ - To Delete (review then bin)` for a human to bin in the UI).
Keeper chosen as the first/most-complete case in each group — reviewable before push.

## High-confidence groups (44 keepers, 99 cases absorbed)

### Functional / Barcode Redemption (5 groups, 20 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 1 | C4103620 — valid booking reference collects/prints (Type B) | C4104806 (Type D), C4104807 (Type E), C4104808 (Type H), C4104809 (Type S), C4104810 (Type U) |
| 2 | C4103625 — invalid booking reference rejected (invalid To Station) | C4104812 (From Station), C4104813 (Product Type), C4104814 (dates) |
| 3 | C4103626 — malformed reference rejected (incomplete entry) | C4104815 (no characters), C4104816 (over-max length), C4104817 (invalid character) |
| 4 | C4103627 — legacy stage resolves name (Type B) | C4104818 (Type E), C4104819 (Type U) |
| 5 | C4103633 — ticket prints in barcode layout (Single) | C4104820 (Day Return), C4104821 (3 Day Select), C4104822 (Cross Border), C4104823 (Half-fare), C4104824 (yLink), C4104825 (24+), C4104826 (Family) |

### Functional / Payments - Cash (6 groups, 13 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 6 | C4103637 — sub-value/out-of-circulation coin rejected (old round £1) | C4104831 (2p), C4104832 (1p) |
| 7 | C4103638 — foreign coin rejected (Euro) | C4104833 (other non-sterling) |
| 8 | C4103639 — banknote valid any orientation (Bank of England) | C4104834 (BoI), C4104835 (Ulster Bank), C4104836 (Danske), C4104837 (First Trust) |
| 9 | C4103640 — withdrawn paper note rejected (£10) | C4104838 (£5), C4104839 (£20) |
| 10 | C4104116 — jam cleared successfully (coin during payment) | C4104841 (note during payment), C4104842 (coin during change) |
| 11 | C4104117 — jam cannot be cleared, fails cleanly (coin during payment) | C4104843 (note during payment), C4104844 (coin during change) |

### Functional / Payments - Cash / Note Recycler (2 groups, 2 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 12 | C4103650 — BNR note in exit beak, Astreo (Cancel) | C4104845 (Back) |
| 13 | C4104113 — BNR note in exit beak, Kiosk (Cancel) | C4104846 (Back) |

### Functional / Payments - EMV & Contactless (15 groups, 31 absorbed) — largest area

| # | Keeper | Absorbed |
|---|---|---|
| 14 | C4103657 — Chip&PIN valid card completes payment (Visa Debit) | C4104561 (Visa Credit), C4104562 (MC Debit), C4104563 (MC Credit), C4104564 (non-GBP) |
| 15 | C4103659 — Amex/Diners cards accepted (Amex Credit) | C4104566 (Amex Debit), C4104567 (Diners Club) |
| 16 | C4103658 — Chip&PIN no PIN entered, doesn't complete (Visa Debit) | C4104565 (MC Debit) |
| 17 | C4103661 — contactless tap at/below limit approved (Visa Credit) | C4104568 (Visa Debit), C4104569 (MC Credit), C4104570 (MC Debit), C4104571 (legacy £30 limit) |
| 18 | C4103662 — contactless tap above limit falls back to Chip&PIN (Visa Credit) | C4104572 (Visa Debit), C4104573 (MC Credit), C4104574 (MC Debit) |
| 19 | C4103663 — mobile wallet payment approved (Apple Pay) | C4104575 (Google Pay), C4104576 (Samsung Pay) |
| 20 | C4103664 — declined card offers retry/cancel (acquirer decline) | C4104577 (unsupported issuer/scheme) |
| 21 | C4103665 — cancel at pinpad ends payment, no ticket (Chip&PIN) | C4104578 (Contactless), C4104579 (Magnetic Stripe) |
| 22 | C4103666 — payment times out, not completed (Chip&PIN) | C4104580 (Contactless), C4104581 (Magnetic Stripe) |
| 23 | C4103667 — print failure voids card payment (Chip&PIN) | C4104582 (Contactless), C4104583 (Magnetic Stripe) |
| 24 | C4104115 — card removed before completion, handled safely (Chip&PIN) | C4104586 (Contactless) |
| 25 | C4104129 — magstripe valid card completes payment (Visa Credit) | C4104587 (Visa Debit), C4104588 (MC Credit), C4104589 (MC Debit) |
| 26 | C4104130 — magstripe cards declined (Amex Credit) | C4104590 (Amex Debit), C4104591 (Diners Club) |
| 27 | C4103670 — switching to card pays by card (before cash inserted) | C4104585 (after cash inserted) |
| 28 | C4103668 — card rejected (expired) | C4104584 (blocked) |

### Sales - Tickets / Ticket Issue (9 groups, 18 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 29 | C4103680 — selected product issued/printed (cash) | C4104847 (card), C4104848 (contactless) |
| 30 | C4103681 — Adult single (cash) | C4104849 (card), C4104850 (contactless) |
| 31 | C4103682 — Child single (cash) | C4104851 (card), C4104852 (contactless) |
| 32 | C4103683 — F&F day ticket (cash) | C4104853 (card), C4104854 (contactless) |
| 33 | C4103684 — F&F additional child (cash) | C4104855 (card), C4104856 (contactless) |
| 34 | C4103685 — Popular tickets shortcut (cash) | C4104857 (card), C4104858 (contactless) |
| 35 | C4103686 — Evening ticket (cash) | C4104859 (card), C4104860 (contactless) |
| 36 | C4103688 — Summer Bus Rambler ticket (cash) | C4104861 (card), C4104862 (contactless) |
| 37 | C4103689 — concessionary half-fare single (cash) | C4104863 (card), C4104864 (contactless) |

### Sales - Tickets / Advance & 3-Day (1 group, 2 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 38 | C4103694 — 3-day ticket issued (cash) | C4104868 (card), C4104869 (contactless) |

### Sales - Tickets / Rail & Cross-Border (Kiosk) (3 groups, 6 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 39 | C4103696 — NI Rail Adult single (cash) | C4104870 (card), C4104871 (contactless) |
| 40 | C4103698 — NI Rail 3-Day Select (cash) | C4104872 (card), C4104873 (contactless) |
| 41 | C4103699 — Cross-Border Adult single (cash) | C4104874 (card), C4104875 (contactless) |

### Non-Functional / Resilience (2 groups, 5 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 42 | C4103780 — degraded service → amber (card reader failure) | C4103781 (printer), C4104904 (coin selector), C4104905 (banknote acceptor) |
| 43 | C4103797 — audio prompts + audible feedback (cash) | C4104908 (card), C4104909 (contactless) |

### Non-Functional / EMS & TMS Maintenance (1 group, 1 absorbed)

| # | Keeper | Absorbed |
|---|---|---|
| 44 | C4103766 — backlight increase persists into Sales App | C4104895 (decrease — folded in as the other direction of the same persistence behaviour) |

**Total: 44 keepers, 99 absorbed → net −99 cases.**

## Ambiguous groups — pending your aggressiveness call

### Basket (34 cases)

**Obvious-only** (1 group, 1 absorbed): C4105305 ("Pay Now reaches Payment Process") keeps;
C4105306 ("Pay Now (Basket - 2025 variant) continues the payment flow") absorbed as a literal
duplicate. Everything else in Basket left as-is.

**Full** would additionally collapse the 11-case navigation chain (destination selection → search →
Single-Return Ulsterbus → Select Tickets → Basket → Select Payment Type: C4105309, C4105310,
C4105311, C4105312, C4105313, C4105314, C4105315, C4105316, C4105317, C4105318, C4105319, C4105320,
C4105321, C4105322 — 14 cases) into **2 flow-level cases** (happy path forward; back-navigation),
each walking the full chain and citing every screen in its steps. Net for Basket under "full": 34 →
~16 (leaving C4105303/C4105304 edit-screen cases and C4105323 cancel-empties-basket as distinct).

### Smartcards & ABT (29 cases)

**Obvious-only** (1 group, 1 absorbed): C4105383 ("Faulty smartcard no-update") keeps; C4105384
("... - Cash") absorbed as a near-duplicate.

**Full** would additionally collapse the 9-case Home-Screen/Multi-Modal-Home entry-point navigation
(C4105346, C4105347, C4105350, C4105351, C4105356, C4105357, C4105358, C4105359, C4105360) into
**2 flow-level cases** (one per entry surface). Net for Smartcards under "full": 29 → ~19.

## Net outcome

| Scope | Before | After |
|---|---|---|
| High-confidence only, Basket/Smartcards untouched beyond literal dupes | 409 | **~308** |
| + full fold of Basket/Smartcards navigation | 409 | **~278** |
