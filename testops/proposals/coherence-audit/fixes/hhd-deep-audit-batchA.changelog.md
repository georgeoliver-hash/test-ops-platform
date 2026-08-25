# HHD deep-audit — Batch A changelog

Suite 30285, sections "Functional / Card Payment (M020)" (887798), "Functional / Card Payment (M020) /
Reference-Number Stations" (887799), "Functional / Smartcards & ABT" (887800). 36 cases, all accounted
for below (3 left alone per instructions).

| Case | Verdict | Note |
|---|---|---|
| C4103800 | verified-clean | M020 Bluetooth pairing enables card payment — FBD-100320 device matrix confirms HHD = Miura M020, non-embedded, Bluetooth pairing required. |
| C4103801 | verified-clean | TID/TK download by serial after pairing — FBD-100320 confirms serial-keyed TMS config, no manual entry, occurs after pairing for HHD. |
| C4103802 | verified-clean | "HHD Retailing" Terminal Group — exact match to FBD-100320 device matrix. |
| C4103803 | verified-clean | Payment-device swap keeps TID/TK — FBD-100320 states explicitly payment-device replacement does not change in-use TID/TK. |
| C4103804 | corrected | Chip-and-PIN Visa sale — refs FBD-100373 (refund-only, no sale/EMV content) replaced with FBD-100183 (M020 EMV L1/L2/P2PE cert, chip-and-PIN). |
| C4103805 | corrected | Chip-and-PIN Mastercard sale — same ref fix as C4103804. |
| C4103806 | corrected | Contactless Visa sale — same ref fix; FBD-100183 confirms ISO 14443 A/B contactless EMV. |
| C4103807 | corrected | Mobile-wallet contactless sale — FBD-100183 explicitly names mobile-wallet contactless support; direct citation. |
| C4103808 | corrected | Card declined, no ticket — FBD-100373 (irrelevant) replaced with FBD-100183; no dedicated decline-flow spec exists but wording is already generic/non-invented. |
| C4103809 | corrected | Expired card rejected — same ref fix as C4103808. |
| C4103810 | corrected | Blocked card rejected — same ref fix as C4103808. |
| C4103811 | corrected | EMV timeout abandons sale — same ref fix as C4103808. |
| C4103812 | corrected | Cancel EMV before card presented — same ref fix as C4103808. |
| C4103813 | corrected | Cancel EMV refused after card presented — same ref fix as C4103808. |
| C4103814 | flagged-gap | EMV Unavailable — resumes after comms restore — no spec anywhere covers comms-outage/restore behaviour; flagged GAP, refs left as FBD-100320 (best available). |
| C4103815 | flagged-gap | PAN Masking on printed ticket — FBD-100658's MaskedPan is an ABT-tap CardDetails field (different context), not a printed EMV sale receipt; no spec confirms PAN masking on the HHD ticket. Flagged GAP. |
| C4103816 | verified-clean | PRN format H+IMEI+ticks+operator code — FBD-100373 gives this exact HHD PRN format verbatim. Strong citation. |
| C4103817 | flagged-gap | Card sale while M020 on charge — refs corrected (FBD-100373→FBD-100183) but no spec addresses charging-state effect on payment capability. Flagged GAP. |
| C4103818 | flagged-gap | Reference-number-station sale (NIR) — old refs (FBD-100320/373) have zero "reference number station" content. Replaced with FBD-100383 (confirms Yorkgate is a real HHD-only NIR halt) but the keying mechanism itself is unconfirmed anywhere. Flagged GAP. |
| C4103819 | flagged-gap | Ref-station sale + M020 on charge — same reference-number-station gap as C4103818 plus the on-charge gap from C4103817. Also swapped the worked example from unconfirmed "Carrickfergus" to confirmed "Larne" (FBD-100383). Flagged GAP. |
| C4103820 | corrected | Adult iLink accepted in-zone — FBD-100271 (transfer logic only, no zone-acceptance content) replaced/supplemented with FBD-100389 (ABT Scenarios, explicit zone-acceptance rule). |
| C4103821 | corrected | Adult iLink rejected out-of-zone — added FBD-100389 alongside FBD-100250, symmetric fix to C4103820. |
| C4103822 | verified-clean | Senior Smartpass accepted — FBD-100250 confirms Senior card type under Fare Foregone group. |
| C4103823 | corrected | Expired Smartpass rejected — added FBD-100658 DeclinedReason=1 "Card Expired" to ground the rejection outcome (FBD-100250 only grounds the card's expiry encoding). |
| C4103824 | corrected | Hotlisted Smartpass rejected — added FBD-100658 DeclinedReason=2 "On Deny List"; "hotlist" wording confirmed as legitimate established Translink terminology elsewhere (etm.md, FBD-100340 note) even though the CloudFare spec itself says "Deny List". |
| C4103825 | verified-clean | Unreadable smartcard rejected — FBD-100250 explicitly covers bad LRC/CRC/Customer-CRC → card rejected. |
| C4103826 | verified-clean | Staff Pass accepted — FBD-100250 confirms Staff card type under Corporate group. |
| C4103827 | corrected | Passback re-tap rejected within window — added FBD-100658 DeclinedReason=20 "Passback" alongside FBD-100271's passback-priority rule. |
| C4103828 | corrected | Successful validation posts audit + communicated to Merit — added FBD-100307 (ABT Data Flow), which explicitly states CloudFare ABT forwards tap data on to Merit; FBD-100658 alone (message structure) doesn't state this. |
| C4103829 | flagged-gap | HHD cash top-up (Adult iLink) — CONFLICT: FBD-100261 states the multi-journey product-group UI (covering both issue AND recharge) "is only used by the POS device as this is the only device that will issue these smartcard products" — same doc that correctly grounds C4103832's "HHD does not issue" claim. Flagged as a capability conflict, not resolved. |
| C4103830 | flagged-gap | HHD card top-up (Child iLink) — same CONFLICT as C4103829. |
| C4103831 | left-alone — known conflict, human-owned | Do not touch (gap-register Q16). No definitive spec answer surfaced during this pass beyond what's already noted. |
| C4103832 | verified-clean | HHD does not issue new smartcards (POS-only) — FBD-100261 §5 confirms explicitly: "the logic described here is only used by the POS device as this is the only device that will issue these smartcard products." Strong citation, well grounded. |
| C4103833 | verified-clean | Glider inspection tap — IsInspection true, product 5001, TID "0" — FBD-100658 confirms this exact triple for HHD taps. |
| C4103834 | verified-clean | HHD tap carries CardDetails block with masked PAN, no raw CardData — FBD-100658 confirms this exact structural distinction for HHD taps. |
| C4103835 | left-alone — known conflict, human-owned | Do not touch (gap-register Q17). No definitive spec answer surfaced during this pass. |

## Totals
- verified-clean: 11 (C4103800–4103803, C4103816, C4103822, C4103825, C4103826, C4103832–4103834)
- corrected: 16 (C4103804–4103813, C4103820, C4103821, C4103823, C4103824, C4103827, C4103828)
- flagged-gap: 7 (C4103814, C4103815, C4103817–4103819, C4103829, C4103830)
- left-alone-conflict: 2 (C4103831, C4103835)
- Total: 36

All 33 touchable cases were completed; none remain outstanding.
