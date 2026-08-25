# HHD deep-audit — Batch B gap register entries

Q&A-register-style entries for cases flagged `flagged-gap` (or carrying a new UNCONFIRMED marker)
during the full-spec grounding pass of suite 30285 batch B. Orchestrator to number centrally and
route through the Q&A loop with the engineer.

---

**Question:** Does the HHD's Key-Stop/Fare-Stage-ID boarding & alighting selection model (arrow-scroll
Key Stops or numeric Fare Stage ID entry, Fare Stage name shown/printed instead of stop name) — as
documented in FBD-100207 for ETM, POS and TVM — also govern the HHD, or does the HHD use a different
mechanism / have its own spec not present in the current requirements library?

**Category:** SURFACE

**Case ids:** 4103847, 4103848, 4103849, 4103851, 4103863, 4103864, 4103871, 4103872, 4103875,
4103876, 4103877

**What we found:** FBD-100207 "TFTS Fare Stage to Stop Migration Solution v4.00" was read in full
(paragraph-by-paragraph search for "HHD"/"Handheld" returned zero hits). It explicitly documents the
selection UI for ETM (paras 261–265), POS (267) and TVM (269) as three separate device sections, but
never adds a fourth section for HHD — a document that otherwise goes out of its way to be exhaustive
per device type. Circumstantial support that the underlying stage/fare-stage model does extend to HHD:
the NIR HHD Ticket Layouts doc instructs that boarding/alighting stage numbers print with leading zeros
on every ticket (implying a stage-based model), and HHD products throughout the Product-to-Ticket
Mapping xlsx are keyed the same way as POS/TVM products.

**What's missing:** Direct confirmation that HHD's actual UI mechanism (menu scroll vs manual keypad
entry) matches FBD-100207's description, or a citation to whatever spec (if any) actually documents the
HHD boarding/alighting selection screen. This is currently used as a same-model analogy, not a confirmed
fact, across 11 cases.

---

**Question:** Does annulling an iLink smartcard top-up on the HHD actually reverse the value already
written to the customer's smartcard, or does it only cancel the back-office/payment record (leaving a
correction to be handled separately, e.g. via a later card read/reconciliation)?

**Category:** LIVE?

**Case ids:** 4103838

**What we found:** iLink top-up as a product/transaction type on the HHD is confirmed real (Product-
to-Ticket Mapping TVM & HHD xlsx lists multiple iLink Period-Update products with Device Type = HHD,
mapped to "Ticket Format 13A – Period Pass Smartcard Top-up Receipt"). FBD-100373 (Refund on POS)
explicitly puts smartcard issues/top-ups **out of scope** for its refund process ("not refundable via
POS") but says nothing about what an *annulment* (a different, earlier-stage undo than a refund) does
to a smartcard's already-written value.

**What's missing:** Confirmation of the actual on-card effect of an HHD top-up annulment. This matters
because if the card was already updated at the point of tap, "annulling" the transaction record without
also correcting the card would leave the passenger with value they didn't pay for (or vice versa) — a
genuine reconciliation risk worth confirming before the case is trusted as written.

---

**Question:** Does the HHD ticket-sales screen have a configured "default passenger type" / "default
ticket type" pre-selection on entry, and if so what governs it (device config, CloudFare/TMS
provisioning, last-used value)?

**Category:** SURFACE

**Case ids:** 4103850

**What we found:** No document in the requirements library (fares-export spec, ticket-layout docs,
product-mapping xlsx) describes a default-selection mechanism for the HHD ticket-sales screen. FBD-
100336 (the case's only citation) is a CloudFare fares-export back-office feature with no device
behaviour at all.

**What's missing:** Any source confirming this configurable-default behaviour exists on HHD. Could be
real (common UX pattern) or could be describing a POS-specific behaviour incorrectly carried over to
the HHD suite — cross-surface risk.

---

**Question:** Does an "advance ticket" product (a ticket sold in advance and printed with a future
travel date) exist as a distinct HHD product, or is this the same thing as the "3 Day Select" product
already covered by case 4103858 under a different name?

**Category:** SURFACE

**Case ids:** 4103855

**What we found:** Searched the Product-to-Ticket Mapping TVM & HHD xlsx and both HHD ticket-layout
docs (NIR, Glider) for "Advance" — no matching product name found for any device, HHD included. FBD-
100336 (the case's only citation) doesn't name any advance product either — it's a generic fares-export
feature spec.

**What's missing:** A named "advance" product/ticket type anywhere in the checked sources. Possible
outcomes: (a) it's a real product under a name we didn't search for, (b) it's a duplicate of 3 Day
Select/period-product date-validity behaviour, or (c) it doesn't exist on HHD and the case should be
retired or rescoped to whichever device/product actually has this behaviour.

---

**Question:** Is the "Visual Inspection" behaviour in this suite section an on-device HHD software
feature (an Operator recalls a previously issued ticket's stored details — product, stages, validity —
on screen) or is it a manual process (the conductor visually reads the physical paper ticket, no device
feature involved)?

**Category:** CONFLICT

**Case ids:** 4103870

**What we found:** The case preface explicitly says "the Operator can visually inspect a previously
issued paper ticket **on the HHD**", which asserts a device software capability. No source in the
requirements library (fares export, ticket-layout docs, product mapping, the RID/cEMV inspection spec
FBD-100716 which covers a completely different kind of inspection — bank cards, not paper tickets)
describes any ticket-recall/lookup screen on the HHD.

**What's missing:** Confirmation of which of the two readings is correct. If it's actually a manual
visual check of the paper (no software feature), the case as written over-asserts an "on the HHD"
device capability that doesn't exist, and should be reworded or rescoped; if a lookup screen genuinely
exists, we need the spec/screen name to ground it properly instead of guessing.
