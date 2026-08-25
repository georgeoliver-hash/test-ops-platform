# HHD deep-audit — Batch A gap register entries (unnumbered — orchestrator to merge/number into gap-register.md)

## Gap: comms-outage/restore behaviour for HHD card payment
- **Category:** LIVE?
- **Affected case(s):** C4103814
- **What I found:** FBD-100320/353 (TID management) and FBD-100373 (Refund on POS) contain no content on
  what happens to M020 card payment after a comms outage is restored. FBD-100373 does confirm a related
  pattern (card refund needs live PSP network; timeout = no refund), which makes "payment resumes after
  comms restore" plausible, but nothing confirms the resume behaviour itself.
- **What's missing:** A spec statement (or live confirmation) that card payment becomes available again
  automatically/without extra steps once HHD↔M020/M020↔NMI comms are restored.

## Gap: PAN masking on printed HHD card-sale ticket/receipt
- **Category:** VALUE
- **Affected case(s):** C4103815
- **What I found:** FBD-100658's `MaskedPan` field is part of the ABT-tap `CardDetails` audit block
  (smartcard/ABT inspection context) — not the same thing as a printed EMV card-SALE ticket. Checked
  FBD-100373, FBD-100183, and the NIR/Glider HHD ticket-layout documents under "Documents from
  Translink/Ticket Formats" — none confirm PAN masking on the printed card-sale receipt.
- **What's missing:** A ticket-layout or hardware spec confirming the HHD masks the PAN on printed
  card-sale receipts (this is standard PCI-DSS practice industry-wide, but that alone isn't a citable
  Translink requirement).

## Gap: M020 payment capability while on charge
- **Category:** LIVE?
- **Affected case(s):** C4103817, C4103819
- **What I found:** No document in the requirement library (FBD-100320, FBD-100353, FBD-100373,
  FBD-100183) mentions the payment device's charging/cradle state as a factor in payment availability.
- **What's missing:** Confirmation (spec or live) that a card sale completes normally while the M020 is
  charging — currently just an assumed/likely-true claim with no citation.

## Gap: reference-number-station card-payment keying mechanism (NIR)
- **Category:** SURFACE
- **Affected case(s):** C4103818, C4103819
- **What I found:** Neither of the previously-cited FBD-100320/FBD-100373 nor any other doc in the
  library mentions "reference number station" or a station-reference-number keying step for HHD card
  payments. FBD-100383 (Operator Hierarchy) does confirm Yorkgate and several other NIR halts
  (Ballymoney, Larne, Larne Harbour, Portrush, Whitehead) are real HHD-only locations, which grounds the
  *location* example, but says nothing about a reference-number keying mechanism for card sales there.
- **What's missing:** A spec describing what a "reference-number station" is for HHD card payment and
  how/why the Operator selects a station reference number as part of the sale (this concept exists
  elsewhere for Ulsterbus Multi-Journey card-reference numbers on smartcards, FBD-100261/FBD-100277,
  but that is a different mechanism — a smartcard product reference, not a card-payment station
  reference — and should not be assumed to be the same thing without confirmation).

## Gap/Conflict: HHD smartcard top-up (SmartRecharge) capability
- **Category:** CONFLICT
- **Affected case(s):** C4103829, C4103830
- **What I found:** FBD-100261 §5 (Metro & Ulsterbus Multi-Journey Configuration) states: "the logic
  described here is only used by the POS device as this is the only device that will issue these
  smartcard products" — describing the product-group-driven UI mechanism used for BOTH SmartCreate
  (issue) and SmartRecharge (top-up) transactions (§5.1/5.2 confirm SmartRecharge products use the same
  product-group mechanism). This same document is the (correctly-cited) basis for C4103832 in this same
  batch, which states the HHD does NOT issue new smartcards, POS-only. No HHD-specific knowledge note or
  flow document in this repo describes an HHD top-up capability either.
- **What's missing:** Either (a) confirmation that HHD top-up is a genuine, real capability not covered
  by FBD-100261's POS-only statement (in which case FBD-100261 may be stale/incomplete and a newer
  CR/spec should be found), or (b) confirmation that C4103829/C4103830 wrongly moved a POS-only
  capability onto the HHD and should be corrected/retired. This is a capability-existence question, not
  a wording issue — flagged for the engineer rather than resolved unilaterally, per the cross-surface
  invention rule in `docs/gherkin-standard.md`.
