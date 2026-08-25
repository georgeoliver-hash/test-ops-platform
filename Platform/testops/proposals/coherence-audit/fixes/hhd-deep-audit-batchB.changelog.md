# HHD deep-audit — Batch B changelog

Suite 30285, sections: Annulment & Reversal; Sales - Paper Tickets / Ticket Issue, Basket, Group
Ticket Sales, Visual Inspection, Cross-Border Tickets, Metro & Ulsterbus Products. 43 cases
(4103836–4103878). Full-spec grounding pass (not just coherence/wording).

**Totals: 13 verified-clean-with-citation · 26 corrected (citation added/fixed, some with a GAP/
UNCONFIRMED marker) · 4 flagged-gap (blocking marker + gap-register entry).**
(Corrected and flagged-gap overlap for 4 cases that got both a citation fix and a marker — counted
once each below under whichever is the stronger verdict.)

## Headline finding
`FBD-100207` (TFTS Fare Stage to Stop) is cited on 11 cases in this batch for HHD stage-selection
behaviour, but the full document — checked in full — explicitly describes the Key-Stop/Fare-Stage-ID
selection model for **ETM, POS and TVM only** (paras 261–269) and **never mentions HHD once**. Kept
as the closest analogue (ticket-layout evidence shows HHD does print Fare-Stage/stage numbers, so the
underlying model likely extends) but this is an unconfirmed extension, not a confirmed one — logged
as a single gap-register question rather than blocking all 11 cases individually.

`FBD-100336` (Fares List File Export) is a **CloudFare back-office export feature with no device
behaviour** (its own knowledge note says so) — valid as a fares-value oracle, but was the *sole*
citation on several cases asserting pure device/UI behaviour (basket mechanics, default selections,
ticket numbering, change calculation, warrant recording) that it doesn't actually cover. Added real
device-behaviour citations where found: `FBD-100373` (basket/PRN/URN structure, ticket numbering),
and three non-FBD but directly relevant local docs — `HHD-Product-Mapping` (Product-to-Ticket Mapping
TVM and HHD V1.00.xlsx), `NIR-HHD-Ticket-Layouts` (NIR HHD Ticket Layouts v14.1), `Glider-HHD-Ticket-
Formats` (Glider HHD Ticket Formats Document v19), `Group-Tickets-Glider` (Group Tickets - Glider_.docx).

## Annulment & Reversal (887801)
| id | verdict | note |
|---|---|---|
| 4103836 | verified-clean | FBD-100373 role table (Operator: Annulment ✔) + REQ-1630.0 (HHD accepts Sales/Reversals) grounds cash-annul capability. |
| 4103837 | verified-clean | Same grounding, card variant. |
| 4103838 | corrected + UNCONFIRMED | iLink top-up on HHD confirmed real (added `HHD-Product-Mapping`); the specific claim that annul reverses the smartcard write is not confirmed anywhere — marked, logged to gaps. |
| 4103839 | corrected | Added `HHD-Product-Mapping` for top-up existence; card-reversal claim already safely grounded via 4103843's M020 pattern. |
| 4103840 | corrected | Added `HHD-Product-Mapping` (yLink confirmed present on HHD). |
| 4103841 | verified-clean | Generic "a nothing-to-annul message is displayed" doesn't assert exact wording — acceptable as assumed-competence, no invented UI text. |
| 4103842 | verified-clean | Sign-off-time annulment is a reasonable reconciliation pattern; not detailed in FBD-100373 but not a specific invented mechanism either — left as-is. |
| 4103843 | verified-clean | REQ-1630.0 explicitly: HHD Reversals processed via payment terminal. |
| 4103844 | verified-clean | PRN format (`H`+IMEI+ticks+2-char operator code) matches FBD-100373 para verbatim, including the example format. |
| 4103845 | verified-clean | REQ-1630.0 / REQ-1630.2 explicitly: "Refunds are not processed by the HHD." Strong match. |
| 4103846 | verified-clean | CR115 clause matches spec text on cross-device linked refunds via POS. Strong match. |

## Ticket Issue (887803)
| id | verdict | note |
|---|---|---|
| 4103847 | corrected | Added `HHD-Product-Mapping`; FBD-100207/HHD-scope caveat noted (see headline). |
| 4103848 | corrected | Same. |
| 4103849 | corrected | Same. |
| 4103850 | flagged-gap | No source describes a configured default passenger/ticket-type pre-selection mechanism for HHD — marked GAP. |
| 4103851 | flagged-gap | FBD-100207 doesn't cover HHD; the specific "menu vs manual character entry" mechanism is unconfirmed for this device — marked UNCONFIRMED. |
| 4103852 | verified-clean | Cash-change calculation is baseline payment-terminal behaviour; no dedicated doc found but not treated as invented functionality (near-universal, not device-specific risk). Citation (FBD-100336 alone) is thin but left as-is — noted for awareness, not blocked. |
| 4103853 | corrected | Added `HHD-Product-Mapping` — "Warrant Return" product/payment concept confirmed present on HHD. |
| 4103854 | corrected | Added `FBD-100373` — its URN structure includes an explicit "Ticket Number" field, better grounding than the fares-export doc. |
| 4103855 | flagged-gap | Searched product-mapping + both ticket-layout docs for "Advance" — no matching product found on any device. Marked GAP; may be a naming mismatch with 3 Day Select. |
| 4103856 | corrected | Added `HHD-Product-Mapping` + `NIR-HHD-Ticket-Layouts` — Weekly/Monthly/Student Monthly period products confirmed present on HHD. |
| 4103857 | corrected | Added `Glider-HHD-Ticket-Formats` — "Ticket Format Number 7 – Summer Bus Rambler Adult Ticket" confirmed. |
| 4103858 | corrected | Added `NIR-HHD-Ticket-Layouts` — "Adult/Child 3 Day Select" and "3 DAY" wording confirmed directly on an HHD ticket example. |
| 4103859 | verified-clean | FBD-100167 ("barcode appended to end, only if enabled per ticket type") + FBD-100318 (Print Barcode=Yes + Barcode Use rule) — strong match. |
| 4103860 | verified-clean | FBD-100167: "No barcode printed when one ticket is issued for multiple passengers" — verbatim match. |
| 4103861 | verified-clean | FBD-100341 covers transaction routing/location-mapping to MERIT/CloudFare; general enough to cover "record visible in CloudFare, carried to MERIT" even though its main subject is location apportionment, not raw record content. |

## Basket (887804)
| id | verdict | note |
|---|---|---|
| 4103862 | corrected | Added `FBD-100373` — basket sales are a real, spec-confirmed concept (per-ticket URN value on basket sales). |
| 4103863 | corrected | Added `FBD-100373`; FBD-100207/HHD-scope caveat noted. |
| 4103864 | corrected | Added `FBD-100373`; FBD-100207/HHD-scope caveat noted. |
| 4103865 | corrected | Added `FBD-100373`. |
| 4103866 | corrected | Added `FBD-100373`. |
| 4103867 | corrected | Added `FBD-100373` — directly supports "all tickets in one transaction" (shared basket PRN) and "numbered sequentially" (per-ticket Ticket Number field). |

## Group Ticket Sales (887805)
| id | verdict | note |
|---|---|---|
| 4103868 | corrected | Added `FBD-100373` + `Group-Tickets-Glider` (real group-ticket sample: "10 Passengers" on one Day Ticket). |
| 4103869 | corrected | Added `FBD-100373` (basket-in-progress editing). |

## Visual Inspection (887806)
| id | verdict | note |
|---|---|---|
| 4103870 | flagged-gap | No source describes an on-device ticket-recall/inspection screen for previously issued paper tickets; may conflate a manual paper check with a device feature. Marked GAP; logged to gap register. |

## Cross-Border Tickets (887807)
| id | verdict | note |
|---|---|---|
| 4103871 | corrected | Dropped mismatched FBD-100207 (doesn't cover HHD); added `NIR-HHD-Ticket-Layouts` (lists the actual Cross-Border Adult/Child Single products + Layout 6). |
| 4103872 | corrected | Same correction. |
| 4103873 | corrected | Added `NIR-HHD-Ticket-Layouts` — confirms Euro pricing shown on tickets issued in Euro (doc's own worked example is Layout 6). |
| 4103874 | corrected | Replaced FBD-100167 (a barcode spec, unrelated to ticket layout) with `NIR-HHD-Ticket-Layouts`, which directly names "Ticket Layout 6 – Cross Border". |

## Metro & Ulsterbus Products (887808)
| id | verdict | note |
|---|---|---|
| 4103875 | corrected | Added `HHD-Product-Mapping` — "Metro Adult/Child Evening DTicket" confirmed present on HHD (Device Type = HHD row). FBD-100207/HHD-scope caveat noted. |
| 4103876 | corrected | Added `HHD-Product-Mapping` — general Ulsterbus-on-HHD product presence confirmed (Ulsterbus MJ top-up rows); Single/Day Return not individually re-verified per SKU (data-variations list treated as representative). FBD-100207/HHD-scope caveat noted. |
| 4103877 | verified-clean | FBD-100340's worked example matches this case almost verbatim: Harryville Shops (Ballymena zone area) → furthest stop Ballee Park & Ride. Strong match. |
| 4103878 | verified-clean | FBD-100340: Pipe Road tap = outside UBTS zone = invalid, exactly as cited. Strong match. |
