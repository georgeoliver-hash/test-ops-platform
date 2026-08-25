# Old-suite audit — evidence base (AA-POS Acceptance Test → GG - POS - Claude Suite)

**Rule for this whole project: audit first, prove it from the old suite + docs + UX, THEN change.**
Never infer shared-vs-mode by guessing — cross-tabulate the old suite. This doc is the evidence.

## Product × mode (which modes a product is actually tested under)
Method: for every old case, take its top-level mode (NIR/Ulsterbus/Metro) and the product-naming
section, strip mode prefixes, and collect the set of modes per product.

### Shared — all 3 modes
- Faulty smartcard · Hotlisted smartcards · Smartcard Top-Ups

### Shared — NIR + Ulsterbus (the two paper-ticket-selling modes)
- **Tickets:** Single · Day Return · iLink Single · Warrant Return · Family & Friends Day
- **Smartcards:** Half Fare · Youth · Concession · Dependents Pass · New Smartcard Issue ·
  New Smartcards used on another device

### NIR (Rail) only
- 1/3 Off Day Return · 3 Day Select · Weekly Season · Monthly Season

### Ulsterbus only
- Bus Rambler · Jobseeker Single · Month Return · Rail Substitution Service · (General · Ticket
  Issue & Printer Interrupts = process/misc)

### Metro only
- 'Blank' smartcards · Smartcard Errors  (Metro is smartcard-led: Travelcard + Multi-Journey)

## Payment methods (old-suite section counts)
- cash payment: NIR 35, Ulsterbus 35, Metro 22
- card payment: NIR 13, Ulsterbus 13   ← **CONFIRM with George: POS "doesn't really do card payments"**
- warrant payment: NIR 13, Ulsterbus 13

## Correction required to the new suite (pending George's sign-off)
1. **Shared ticket products** (Single, Day Return, iLink Single, Warrant Return, Family & Friends)
   → ONE case each under `Functional / Tickets`. **Remove** the duplicated per-mode versions
   ("NIR — Single", "Ulsterbus — Single", etc.) — they were an over-build (move to Delete bin).
2. **NIR-only** tickets stay under `NIR (Rail) / Tickets`: 1/3 Off Day Return, 3 Day Select,
   Weekly Season, Monthly Season.
3. **Ulsterbus-only** stay under `Ulsterbus / Tickets`: Bus Rambler, Jobseeker Single, Month Return,
   Rail Substitution Service.
4. **Card payment** — keep or drop per George's answer. If dropped, remove the `Card Payment`
   section + the "bank card" references and the card-payment data-variation mentions.
5. Selling mechanism differs by mode (rail FLU = stations; bus FLU = route/stages) — the shared
   product cases assert the product; the per-mode FLU cases cover the selling mechanism.

## Top-up & validation cross-tab (added)
- **Smartcard top-ups are cross-mode:** iLink, Multi-Journey, BVP, **Metro Travel(card)**, Town
  Services, smartcard top-ups all appear under **all three modes** in the old suite → top-up is
  almost certainly **SHARED** (any POS mode can top up any card). This means the earlier placement
  of "Top Up — Metro Travelcard" → Metro and "Top Up — Ulsterbus / Town Service" → Ulsterbus is
  likely **wrong** — they should sit in Shared. **CONFIRM with George.**
- Metro-only top-up bits: 'Blank' smartcards (issue), Expired smartcards, Smartcard Errors.
- **Validation:** no mode-specific validation sections found → validation is **SHARED**.

## Still to audit before further change (per the audit-first rule)
- The **documentation / requirements** (REQ-#### specs) — George sourcing.
- The **UX designs** (Overflow) per mode — confirm mode-specific screen/flow differences.
- Validation + top-up per-mode differences (cross-tab the same way as products).
