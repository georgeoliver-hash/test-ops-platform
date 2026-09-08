# TVM deep-audit — full citation-grounding pass (suite 30284)

**Date:** 2026-07-22 (session started 2026-07-21). **Suite:** `**NEW** TVM Test Suite` (30284),
project 42, TFTS - System Test. **Scope:** every live case, cross-examined claim-by-claim against
the real FBD/spec source (not just internal coherence), per George's directive to do the full thing
this tool exists for.

## Verdict

**174 / 174 active cases reached — none skipped.** No case needed a **behaviour** change (title,
preface, preconditions, steps, or expected result) in this pass — the wording throughout the suite
is accurate to what's tested. What this pass found and fixed was entirely in the **Refs (citation)
field**: three sections had a plausible-looking FBD number that, read in full via
`tools/extract_req.py`, documents something other than the claim under test. Push committed;
`audit --suite 30284` is **CLEAN** (174 cases, 0 blocking findings, 24 pre-existing advisory
`title-too-long`, unchanged from before this pass).

## Headline numbers

| | Count |
|---|---:|
| Total active cases reviewed | 174 |
| Verified clean (citation checked and matches the claim) | 91 |
| — of which fixed in an earlier pass today (barcode/smartcard/Scottish-note/terse-rewrite) | 12 |
| Citation corrected this pass (Refs only) | 29 |
| Flagged as an unresolved conflict, left unchanged | 1 |
| No citation available anywhere in the library — systemic gap, not fabricated | 52 (one grouped finding) |
| Cases not reached | **0** |
| New gap-register questions raised | Q30, Q31, Q32, Q33 (case-specific) + Q34 (systemic) |

## The three mis-citation clusters found and fixed (30 cases)

1. **EMV & Contactless (887780) — FBD-100320 wrongly cited on 15 cases (Q30).** FBD-100320 is `TID
   Management - Embedded & Non-Embedded Payment Devices` — read in full, it is entirely about
   terminal-ID/transaction-key allocation. Zero mentions of PAN, PIN, contactless or transaction
   limits. It does not support card approval/decline, PIN timeout, Amex/Diners acceptance, min/max
   value, contactless limit, mobile wallet, PAN masking, or print-failure voiding a payment — the
   TVM's Ingenico terminal has no EMV-behaviour spec anywhere in the library (checked FBD-100183,
   which documents the POS's different Miura M020 terminal instead). Kept only on **C4103671**
   (its claim — audit record carries the TID — is genuinely FBD-100320 territory). Fixed: Refs on
   the other 15 cases now point to gap-register **Q30**.
2. **Commissioning/Config-Topology "home location" cluster — FBD-100296 wrongly cited on 7 cases
   (Q31).** FBD-100296 (`Stop, Route & Service Management in CloudFare`) covers TransXChange routes
   and the ETM route-entry UI, not Device Home Location or fares-triangle product availability.
   Better sources found and applied: **FBD-100383** (Operator Hierarchy — defines Device Home
   Location) and **PSPEC-0014 §9** (Fare Triangle). The joined "home location limits sellable
   fares-triangle products" rule isn't stated verbatim in either — flagged needs-confirmation in
   **Q31**.
3. **Commissioning/Config-Deployment cluster — FBD-100385 wrongly cited on 7 cases (Q32).**
   FBD-100385 (`CloudFare Configuration Data Exports`) is scoped to portal export reports only, not
   the device-side TMS dataset-deployment mechanism (immediate/future activation, partial-deployment
   reporting, config pushes) these 7 cases test. No replacement TMS/deployment spec exists in the
   library — logged as **Q32**.

Plus one flagged conflict, **C4103793** (Q33): claims a WAN→SIM failover on the Kiosk TVM, which
FBD-100359 doesn't document for its "Ethernet device" classification — the same "no failover"
reading that was reversed for the **PV** earlier this session on old-suite/TIBU evidence (Q9/Q23).
That same check wasn't done for the TVM in this pass (time), so left unchanged and escalated rather
than guessed either way.

## The one systemic non-fix (Q34, 52 cases)

Payments-Cash hardware behaviour, the Astreo note-recycler/BNR, Kiosk coin-recycler hoppers, the
whole Alarmboard & Enclosure section (siren/LED/temperature/UPS/door/speaker/fan/TL80/touchscreen),
and the hardware-state half of Resilience (degraded/amber, low-change, lockout, 98%-acceptance/
performance) carry **no citation at all**, and a filename search of the entire requirements library
for every plausible keyword (cash, hardware, printer, alarm, BNR, note acceptor, escrow, lockout,
degraded, AML/laundering/cash-limit/suspicious) turned up **nothing** — this physical/procedural
layer isn't covered by any FBD/REQ document in scope for this library at all (presumably OEM/vendor
Astreo/Kiosk/TL80 hardware-acceptance documentation that was never brought into `REQS_DIR`).

These 52 cases are **not** marked `GAP`/`UNCONFIRMED` in the body. Per `docs/gherkin-standard.md`'s
assumed-competence guidance, that marker is for disputed *existence* of a behaviour (does this
device have a barcode scanner / smartcard reader — already checked and fixed earlier today) — not
for "no bespoke citation exists for a mechanical fact a tester can directly observe on live
hardware" (does this coin get accepted, does the siren sound). The original 2026-07-17 coherence
audit already called this area "clean"; this pass adds the citation check on top and records the
result as one grouped finding (Q34) rather than 52 duplicate register entries, matching this
register's own grouping convention.

## Full case table (all 174 active cases)

| Case | Section | Title | Refs (after this pass) | Grounding status |
|---|---|---|---|---|
| C4103620 | Barcode Redemption | Ticket Collection — a valid booking reference collects and prints the pre-paid ticket | FBD-100483,FBD-100317 | Verified clean (fixed earlier today, prior pass) |
| C4103621 | Barcode Redemption | Ticket Collection — the booking reference is validated against the back office | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103622 | Barcode Redemption | Ticket Collection — a successful redemption emits a Barcode Redemption event | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103623 | Barcode Redemption | Ticket Collection — an offline redemption still prints and queues an offline event | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103624 | Barcode Redemption | Ticket Collection — a redemption above the barcode ceiling limit cannot validate offline | FBD-100483,FBD-100317 | Verified clean — citation checked, matches claim |
| C4103625 | Barcode Redemption | Booking Reference — an invalid booking reference is rejected | FBD-100483 | Verified clean (fixed earlier today, prior pass) |
| C4103626 | Barcode Redemption | Booking Reference — a malformed reference entry is rejected before submission | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103627 | Barcode Redemption | Ticket Collection — a collection against a legacy stage resolves the legacy stage name | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103628 | Barcode Redemption | Single-Use only — a multi-use ticket's Collect Ticket Code is rejected | FBD-100167,FBD-100317,confirmed George (live-system) 2026-07-21 | Verified clean (fixed earlier today, prior pass) |
| C4103629 | Barcode Redemption | Single-Use only — collection accepts a booking reference and not a scanned barcode | FBD-100317,FBD-100483 | Verified clean — citation checked, matches claim |
| C4103630 | Barcode Redemption | Ticket Collection — a business error shows an error screen and returns to Home after the timeout | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103631 | Barcode Redemption | Ticket Collection — repeated server errors retry and then fall back | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103632 | Barcode Redemption | Ticket Collection — an already-redeemed booking reference is rejected as used | FBD-100483 | Verified clean — citation checked, matches claim |
| C4103633 | Barcode Redemption | Barcode Ticket Format — a collected ticket prints in the barcode ticket layout | FBD-100167,FBD-100318 | Verified clean — citation checked, matches claim |
| C4103634 | Payments - Cash | Coins — valid coins pay for a transaction and change is returned | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103635 | Payments - Cash | Coins — a valid coin is accepted after an invalid coin is inserted | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103636 | Payments - Cash | Coins — coins inserted during the "More Time Required" screen complete the payment | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103637 | Payments - Cash | Coins — out-of-circulation and sub-value coins are rejected | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103638 | Payments - Cash | Coins — foreign coins are rejected | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103639 | Payments - Cash | Banknotes — a valid banknote in any orientation pays for a transaction | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103640 | Payments - Cash | Banknotes — withdrawn paper notes are rejected | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103641 | Payments - Cash | Banknotes — a Scottish banknote is accepted as valid sterling | confirmed George (live-system) 2026-07-21; gap-register Q15 | Verified clean (fixed earlier today, prior pass) |
| C4103642 | Payments - Cash | Cash — mixed coins and banknotes pay for a transaction | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103643 | Payments - Cash | Cash — overpayment returns the correct change | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103644 | Payments - Cash | Cash — pressing Back returns the inserted cash before the escrow limit | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103645 | Payments - Cash | Cash — pressing Cancel returns the inserted cash after the escrow limit | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103646 | Payments - Cash | Cash — the coin escrow limit stops further coins being accepted | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103647 | Payments - Cash | Cash — the banknote escrow limit stops further notes being accepted | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103648 | Payments - Cash | Cash — a print failure returns the inserted cash | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103649 | Payments - Cash | Cash — a completed cash sale posts audit data to CloudFare | FBD-100341 | Verified clean — citation checked, matches claim |
| C4103650 | Note Recycler & Change (Astreo) | BNR — a note left in the exit beak leaves the recycler non-functional | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103651 | Note Recycler & Change (Astreo) | BNR — a rejected invalid note left hanging from the exit beak leaves the recycler non-functional | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103652 | Note Recycler & Change (Astreo) | BNA — a note-acceptor error makes note payment unavailable | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103653 | Note Recycler & Change (Astreo) | Change — insufficient change prints a Refuse Change Voucher for the balance | FBD-100341 | Verified clean — citation checked, matches claim |
| C4103654 | Note Recycler & Change (Astreo) | Change — a Refuse Change Voucher is printed when cash is inserted during the "More Time Required" screen | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103655 | Coin Recycler Hopper (Kiosk) | Coin recycler — a Cash Content Report is produced after a hopper is replaced | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103656 | Coin Recycler Hopper (Kiosk) | Coin recycler — replenishing a hopper restores change-giving from a low-change state | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103657 | Payments - EMV & Contactless | Chip & PIN — a valid card completes payment and prints the ticket | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103658 | Payments - EMV & Contactless | Chip & PIN — a payment with no PIN entered does not complete | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103659 | Payments - EMV & Contactless | Chip & PIN — American Express and Diners cards are accepted | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103660 | Payments - EMV & Contactless | Chip & PIN — transaction value limits are enforced | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103661 | Payments - EMV & Contactless | Contactless — a tap at or below the contactless limit is approved | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103662 | Payments - EMV & Contactless | Contactless — a tap above the contactless limit falls back to Chip & PIN | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103663 | Payments - EMV & Contactless | Contactless — a mobile wallet payment is approved | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103664 | Payments - EMV & Contactless | EMV — a declined card offers retry or cancel | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103665 | Payments - EMV & Contactless | EMV — cancelling at the pinpad ends the payment without a ticket | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103666 | Payments - EMV & Contactless | EMV — a payment that times out is not completed | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103667 | Payments - EMV & Contactless | EMV — a print failure voids the card payment | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103668 | Payments - EMV & Contactless | EMV — an expired or blocked card is rejected | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103669 | Payments - EMV & Contactless | EMV — the PAN is masked on the receipt and back-office systems | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103670 | Payments - EMV & Contactless | EMV — selecting card after a cash transaction returns any inserted cash and pays by card | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103671 | Payments - EMV & Contactless | EMV — a completed card sale posts audit data to CloudFare under the TVM terminal ID | FBD-100320,FBD-100341 | Verified clean — citation checked, matches claim |
| C4103672 | Payments - EMV & Contactless | EMV — a card payment receipt is printed when selected | gap-register Q30 (no TVM/Ingenico EMV spec in REQS_DIR) | Corrected (Q30) — FBD-100320 mis-cited (TID spec, not EMV) |
| C4103680 | Ticket Issue | Ticket Issue — a selected product is issued and printed | FBD-100336,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103681 | Ticket Issue | Ticket Issue — Adult single ticket | FBD-100336,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103682 | Ticket Issue | Ticket Issue — Child single ticket | FBD-100336,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103683 | Ticket Issue | Ticket Issue — Family and Friends day ticket | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103684 | Ticket Issue | Ticket Issue — Family and Friends additional child | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103685 | Ticket Issue | Ticket Issue — Popular tickets shortcut | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103686 | Ticket Issue | Ticket Issue — Evening ticket | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103687 | Ticket Issue | Ticket Issue — Day and Day Return tickets | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103688 | Ticket Issue | Ticket Issue — Summer Bus Rambler ticket | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103689 | Ticket Issue | Ticket Issue — concessionary half-fare single | FBD-100336,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103690 | Ticket Issue | Ticket Issue — buy a product in a different language | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103691 | Ticket Issue | Ticket Issue — issued ticket carries a single-use barcode | FBD-100167,FBD-100317 | Verified clean — citation checked, matches claim |
| C4103692 | Ticket Issue | Ticket Issue — a single ticket for multiple passengers carries no barcode | FBD-100167 | Verified clean — citation checked, matches claim |
| C4103693 | Ticket Issue | Ticket Issue — the sale posts an audit record to the back office | FBD-100341 | Verified clean (fixed earlier today, prior pass) |
| C4103694 | Advance & 3-Day | 3-Day — a 3-day ticket is issued | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103695 | Advance & 3-Day | 3-Day — the ticket is valid across three consecutive days | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103696 | Rail & Cross-Border (Kiosk) | NI Rail — Adult single between two stations | FBD-100450,FBD-100207 | Verified clean (fixed earlier today, prior pass) |
| C4103697 | Rail & Cross-Border (Kiosk) | NI Rail — Day Return, Weekly and Monthly products | FBD-100450 | Verified clean — citation checked, matches claim |
| C4103698 | Rail & Cross-Border (Kiosk) | NI Rail — 3-Day Select ticket | FBD-100450,FBD-100167 | Verified clean — citation checked, matches claim |
| C4103699 | Rail & Cross-Border (Kiosk) | Cross-Border — Adult single | FBD-100450,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103700 | Rail & Cross-Border (Kiosk) | Cross-Border — Return, Monthly and 1-Month-Return products | FBD-100450 | Verified clean — citation checked, matches claim |
| C4103701 | Rail & Cross-Border (Kiosk) | Cross-Border — 1st Class ticket | FBD-100450 | Verified clean — citation checked, matches claim |
| C4103702 | Rail & Cross-Border (Kiosk) | NI Rail — concessionary single | FBD-100450 | Verified clean — citation checked, matches claim |
| C4103703 | Rail & Cross-Border (Kiosk) | NI Rail — grouped-station area name prints on a cross-border ticket | FBD-100515,FBD-100450 | Verified clean (fixed earlier today, prior pass) |
| C4103704 | Basket | Basket — adding a product increases the basket quantity | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103705 | Basket | Basket — adding more of the same product increases the quantity | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103706 | Basket | Basket — an identical product merges into the existing basket line | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103707 | Basket | Basket — the same product with different stages is a separate line | FBD-100336,FBD-100207 | Verified clean — citation checked, matches claim |
| C4103708 | Basket | Basket — reducing an item quantity lowers the total | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103709 | Basket | Basket — removing a product with the bin icon deletes the line | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103710 | Basket | Basket — removing the final product empties the basket | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103711 | Basket | Basket — remaining ticket numbers are contiguous after a removal | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103712 | Basket | Basket — amending the boarding stage reduces the fare | FBD-100207,FBD-100336 | Verified clean — citation checked, matches claim |
| C4103713 | Basket | Basket — amending the alighting stage increases the fare | FBD-100207,FBD-100336 | Verified clean — citation checked, matches claim |
| C4103714 | Basket | Basket — Family and Friends quantity set to zero removes the line | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103715 | Basket | Basket — increasing the Family and Friends quantity raises the total | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103716 | Basket | Basket — cash overpayment is handled after amending the basket | FBD-100336 | Verified clean — citation checked, matches claim |
| C4103717 | Ticket Numbering | Ticket Numbering — identical products in separate transactions | FBD-100336,regression: 6160 Ticket Numbering | Verified clean — citation checked, matches claim |
| C4103718 | Ticket Numbering | Ticket Numbering — different products in separate transactions | FBD-100336,regression: 6160 Ticket Numbering | Verified clean — citation checked, matches claim |
| C4103719 | Ticket Numbering | Ticket Numbering — identical products in a single transaction | FBD-100336,regression: 6160 Ticket Numbering | Verified clean — citation checked, matches claim |
| C4103720 | Ticket Numbering | Ticket Numbering — different products in a single transaction | FBD-100336,regression: 6160 Ticket Numbering | Verified clean — citation checked, matches claim |
| C4103721 | Ticket Numbering | Ticket Numbering — cancelling a selection does not skip a number | FBD-100336,regression: 6160 Ticket Numbering | Verified clean — citation checked, matches claim |
| C4103722 | Grouped Stops | Grouped Stops — a grouped TVM defaults to the group boarding stage | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103723 | Grouped Stops | Grouped Stops — alighting list spans all stops in the group | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103724 | Grouped Stops | Grouped Stops — the cheapest non-zero fare combination is selected | FBD-100515,FBD-100336 | Verified clean — citation checked, matches claim |
| C4103725 | Grouped Stops | Grouped Stops — a fare tie is broken by the first combination | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103726 | Grouped Stops | Grouped Stops — the printed boarding stop need not be nearest the TVM | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103727 | Grouped Stops | Grouped Stops — the group name shows on screen and prints on the ticket | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103728 | Grouped Stops | Grouped Stops — no valid fare shows an error screen | FBD-100515 | Verified clean — citation checked, matches claim |
| C4103729 | Ticket Collection | Ticket Collection — collect a pre-paid ticket using a booking reference (Collect Ticket Code) | FBD-100336,FBD-100317,confirmed George (live-system) 2026-07-21 | Verified clean (fixed earlier today, prior pass) |
| C4103730 | Ticket Collection | Ticket Collection — an incomplete booking reference is rejected | FBD-100336,regression: 6160 Pre-Booked Tickets | Verified clean — citation checked, matches claim |
| C4103731 | Ticket Collection | Ticket Collection — an invalid-character booking reference is rejected | FBD-100336,regression: 6160 Pre-Booked Tickets | Verified clean — citation checked, matches claim |
| C4103732 | Ticket Collection | Ticket Collection — a full-length valid reference is accepted | FBD-100336,regression: 6160 Pre-Booked Tickets | Verified clean — citation checked, matches claim |
| C4103738 | Commissioning & Deployment | Commissioning — a TVM downloads its config and credentials by serial | FBD-100320 | Verified clean — citation checked, matches claim |
| C4103739 | Commissioning & Deployment | Commissioning — credentials stay within the TVM Terminal Group | FBD-100320 | Verified clean — citation checked, matches claim |
| C4103740 | Commissioning & Deployment | Commissioning — topology makes home-location products sellable | FBD-100383,PSPEC-0014 sec9,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103741 | Commissioning & Deployment | Software Deployment — immediate dataset installs and updates versions | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103742 | Commissioning & Deployment | Software Deployment — future dataset downloads but waits to activate | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103743 | Commissioning & Deployment | Software Deployment — report separates downloaded from installed | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103744 | Commissioning & Deployment | Failed Deployment — partial update reports both success and failure | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103745 | Commissioning & Deployment | Topology Deployment — new fares deploy for future activation | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103746 | Commissioning & Deployment | Topology Deployment — changing location changes sellable products | FBD-100383,PSPEC-0014 sec9,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103747 | Commissioning & Deployment | Configuration Deployment — coin vault threshold set in TMS applies | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103748 | Commissioning & Deployment | Configuration Deployment — EMV-only mode disables cash | gap-register Q32 (no TMS device-deployment spec in REQS_DIR) | Corrected (Q32) — FBD-100385 mis-cited (export-report spec, not deployment) |
| C4103749 | Commissioning & Deployment | BOS Interface — CloudFare forces communication with the TVM | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103750 | Commissioning & Deployment | BOS Interface — a secure connection is required for uVNC | FBD-100359 | Verified clean — citation checked, matches claim |
| C4103673 | Smoke | Power-On — a cold boot reaches the Sales home screen | C1831643,REQ-0326 | Verified clean — citation checked, matches claim |
| C4103674 | Smoke | Screensaver Wake — touching the idle screen returns to the Sales home screen | C1705882,REQ-0270,REQ-0277 | Verified clean — citation checked, matches claim |
| C4103675 | Smoke | Ticket Sale — a basic single ticket is issued and printed when paid by cash | C1831788,C1705885,REQ-0782,REQ-1877 | Verified clean — citation checked, matches claim |
| C4103676 | Smoke | Ticket Sale — a basic single ticket is issued and printed when paid by contactless card | C1705893,FBD-100320,FBD-100353,REQ-0095,REQ-0097 | Verified clean — citation checked, matches claim |
| C4103677 | Smoke | Ticket Collection — a pre-paid ticket is collected and printed | C1898219,REQ-1576,FBD-100317,confirmed George (live-system) 2026-07-21 | Verified clean (fixed earlier today, prior pass) |
| C4103678 | Smoke | EMS Access — an engineer opens the EMS/TMS screen and returns to Sales | C1898221 | Verified clean — citation checked, matches claim |
| C4103679 | Smoke | Comms — the TVM reports to CloudFare and updates Last Communication | C1898222,FBD-100266,FBD-100341 | Verified clean — citation checked, matches claim |
| C4103751 | EMS & TMS Maintenance | EMS Access — a Technician signs in with a staff-list ID | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103752 | EMS & TMS Maintenance | EMS Access — only authorised roles can sign into EMS | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103753 | EMS & TMS Maintenance | Remote Control — remote Out of Service persists across reboot | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103754 | EMS & TMS Maintenance | Remote Control — CloudFare returns the TVM to In Service | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103755 | EMS & TMS Maintenance | Remote Control — remote reboot, de-activate and re-activate | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103756 | EMS & TMS Maintenance | Cash Collection — an Engineer prints a Cash Content Report | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103757 | EMS & TMS Maintenance | Cash Collection — prints collection and reload reports | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103758 | EMS & TMS Maintenance | Configuration Topology — home location sets the selling operator | FBD-100383,PSPEC-0014 sec9,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103759 | EMS & TMS Maintenance | Configuration Topology — destination outside triangle unavailable | FBD-100383,PSPEC-0014 sec9,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103760 | EMS & TMS Maintenance | Location Settings — amend home location to another valid location | FBD-100383,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103761 | EMS & TMS Maintenance | Location Settings — an invalid location ID is rejected | FBD-100383,gap-register Q31 | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103762 | EMS & TMS Maintenance | Sub Location — a sub-location must be a valid 3-digit ID | gap-register Q31 (no location-ID-format spec found) | Corrected (Q31) — FBD-100296 mis-cited (route spec, not home-location) |
| C4103763 | EMS & TMS Maintenance | Ticket Roll Length — an Engineer corrects the roll length | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103764 | EMS & TMS Maintenance | Transaction Report — prints after multiple transactions | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103765 | EMS & TMS Maintenance | Volume Control — volume adjusts within limits and persists | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103766 | EMS & TMS Maintenance | Screen Brightness — backlight change persists into the Sales App | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103767 | EMS & TMS Maintenance | Config Export — Product List reflects the TVM's configuration | FBD-100385 | Verified clean — citation checked, matches claim |
| C4103768 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer tests the siren | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103769 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer tests the status LEDs | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103770 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer measures the enclosure temperature | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103771 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer reads the UPS status | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103772 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer runs the door and sensor tests | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103773 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer tests the speaker | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103774 | Alarmboard & Enclosure (Kiosk) | Alarmboard — an Engineer tests the ticket-chute fan | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103775 | Alarmboard & Enclosure (Kiosk) | TL80 Printer — an Engineer adjusts the print alignment | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103776 | Alarmboard & Enclosure (Kiosk) | Touchscreen — an Engineer runs the touchscreen test | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103777 | Alarmboard & Enclosure (Kiosk) | Comms Configuration — an Engineer kills the on-screen keyboard | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103778 | Coin Recycler Hopper (EMS, Kiosk) | Coin Recycler Hopper — Cash Content Report after replacement | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103779 | Coin Recycler Hopper (EMS, Kiosk) | Coin Recycler Hopper — reloading updates recorded cash content | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103780 | Resilience | Degraded Service — payment hardware failure transitions to amber | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103781 | Resilience | Degraded Service — low printer stock raises an amber status | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103782 | Resilience | Low Change — change unavailable notifies customer and CloudFare | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103783 | Resilience | Low Change — a change voucher is issued on request | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103784 | Resilience | Print Failure — cash is returned when a ticket fails to print | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103785 | Resilience | Mains Power Failure — runs on battery and keeps vaults secure | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103786 | Resilience | Device Lockout — cash sale at the lockout limit goes Out of Service | — | Verified clean (fixed earlier today, prior pass) |
| C4103787 | Resilience | Device Lockout — card sale at the lockout limit stays In Service | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103788 | Resilience | Device Lockout — a cancelled cash sale stays In Service | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103789 | Resilience | Heartbeat — idle TVM updates Last Communication every 15 minutes | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103790 | Resilience | Heartbeat — a StaffList message resets Hours Since Last Comms | FBD-100266 | Verified clean — citation checked, matches claim |
| C4103791 | Resilience | Comms Lock — sustained outage drives the TVM to comms-locked OOS | FBD-100359 | Verified clean — citation checked, matches claim |
| C4103792 | Resilience | Comms Recovery — returns to service and delivers queued sales | FBD-100359,FBD-100266 | Verified clean — citation checked, matches claim |
| C4103793 | Resilience | Comms Reporting — WAN-to-SIM failover reported to CloudFare | FBD-100266,gap-register Q33 (conflict vs FBD-100359 Ethernet-only classification) | Flagged (Q33) — WAN/SIM failover vs FBD-100359 conflict, unresolved |
| C4103794 | Resilience | Screensaver Wake-Up — a screen tap wakes to the mode home | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103796 | Resilience | Multi-Modal Home — selecting Bus or Rail shows the right home | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |
| C4103797 | Resilience | Audio Prompts — speech prompts and payment feedback play | — | Verified clean (fixed earlier today, prior pass) |
| C4103798 | Resilience | Performance — workflows launch from idle within tolerance | — | Verified clean (fixed earlier today, prior pass) |
| C4103799 | Resilience | Performance — the TVM accepts at least 98% of valid cash | — | No citation — Q34 systemic hardware/procedural gap (not fabricated) |

## Artefacts

- Rewrite applied: `proposals/coherence-audit/fixes/tvm-deep-audit.rewrite.json` (30 Refs-only
  updates, committed).
- Changelog: `proposals/coherence-audit/fixes/tvm-deep-audit.changelog.md`.
- New gap-register entries: `proposals/coherence-audit/gap-register.md` Q30–Q34.
- Audit re-run: `reports/tfts-system-test/new-tvm-test-suite/2026-07-22/alignment-audit.md` — CLEAN.

## Not touched

Every other TestRail suite; the 27 `ZZ_DELETE_REVIEW` cases and the 9 terse-rewrite cases from
today's earlier passes (already handled, out of scope for this pass).
