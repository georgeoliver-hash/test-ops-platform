# HHD deep-audit — Batch D changelog

Suite 30285 (`**NEW** HHD Test Suite`), sections: Functional / Supervisor (887813), Functional /
Technician (887814), Functional / Ticket Formats & Waybill (887815), Functional / Single-Use
Barcodes NIR (887816). 39 cases, ids 4103923–4103961. Every citation below was opened and checked
via `tools/extract_req.py` against the real spec text — an existing `refs` value was never assumed
correct without opening the document.

Grounding sources used beyond the batch's named FBDs: **TFTS Requirements Matrix** (`1_Requirements\
TFTS Project Delivery Matrices & VCRMs\TFTS Requirements Matrix.xlsx` — the authoritative REQ-####
source), **Waybills V.5** (`Documents from Translink\Ticket Formats\Waybills\Waybills V.5.pdf`),
**NIR HHD Ticket Layouts v14.1** and **Glider HHD Ticket Formats v19** (same folder tree, `Ticket
Formats\HHD\...`). None of these are FBD-numbered but are real, distinct documents from the FBDs
they were previously (wrongly) cited against.

## Headline finding

**4103926** asserted the *opposite* of the documented behaviour: the case said a Supervisor's
sign-on to a PIN-locked HHD is refused. REQ-0099.1 (current, signed-off) says the Supervisor
*unlocks* the device by presenting their smartcard + PIN. Rewritten to match the confirmed
requirement. See rewrite JSON for full detail.

## Verdicts

| id | title | verdict | note | citation |
|---|---|---|---|---|
| 4103923 | Sign On — Supervisor sign on (manual and smartcard) | corrected | ref was FBD-100383 (hierarchy doc, no sign-on content) | REQ-0050.0/.1/.2 |
| 4103924 | Supervisor — act as Operator (sign on, sign off, end duty) | flagged-gap | "act as Operator" not found anywhere in the requirement library after exhaustive search | GAP, gap-register |
| 4103925 | Supervisor — authorise an operator break (ID entry and card) | flagged-gap | spec describes Supervisor *overriding/ending* a break (REQ-0360.0), not *authorising* one to start | UNCONFIRMED, gap-register |
| 4103926 | Sign On — Supervisor fails to sign on to a PIN-locked HHD | corrected | **behaviour reversed** — spec says Supervisor unlocks, not refused (see headline) | REQ-0099.1 |
| 4103927 | Supervisor — view and print previous waybills | corrected | ref was FBD-100373 (Refund on POS, unrelated) | REQ-0350.0/.1/.2 |
| 4103928 | Supervisor — print software versions | corrected | ref was FBD-100320 (TID mgmt, unrelated) | REQ-0353.1 |
| 4103929 | Supervisor — pair with a different payment device | verified-clean-with-citation | device/payment matrix + TID/TK-unchanged rule confirmed in FBD-100320 | FBD-100320 |
| 4103930 | Supervisor Menu — navigation and role scope | corrected | ref was FBD-100342 (BOS/CloudFare web claims, not on-device menu) | REQ-0656.0 |
| 4103931 | Sign Off — Supervisor sign off | corrected | ref was FBD-100383 (hierarchy, no sign-off content) | REQ-0098.1, FBD-100358 |
| 4103932 | Sign On — Technician sign on (manual and smartcard) | corrected | same issue as 4103923 | REQ-0050.0/.1/.2 |
| 4103933 | Technician — set the device home location | corrected | ref was FBD-100383 (hierarchy, no config-action content) | REQ-0514.1 |
| 4103934 | Technician — set the Terminal ID and Transaction Key | verified-clean-with-citation | TMS-by-serial, HHD Retailing group, post-pairing sequence confirmed | FBD-100320 |
| 4103935 | Technician — pair with the payment device | verified-clean-with-citation | M020/Bluetooth pairing-required matrix confirmed | FBD-100320 |
| 4103936 | Technician — connect the printer (MAC entered or scanned) | flagged-gap | ref was FBD-100320 (TID mgmt, unrelated); specific MAC-entry/scan mechanism not documented anywhere found | REQ-0819.0 (partial), gap-register |
| 4103937 | Technician Menu — navigation and role scope | corrected | same issue as 4103930 | REQ-0656.0 |
| 4103938 | Sign Off — Technician sign off | corrected | same issue as 4103931 | REQ-0098.1, FBD-100358 |
| 4103939 | Ticket Format — travel-ticket layouts print to the approved format | corrected | FBD-100363 doesn't carry layout numbers; all NIR/Glider layout numbers verified directly and added as citations | FBD-100363 + layout docs |
| 4103940 | Ticket Format — Cross-Border ticket format (NIR) | corrected | Layout 6 verified directly; layout doc added as citation | FBD-100363 + NIR layouts |
| 4103941 | Ticket Format — concession, free and half-fare smartpass ticket formats | corrected | NIR 7a/7b/8a/8b + Glider 8a/8b/10/10b verified directly | FBD-100363 + layout docs |
| 4103942 | Ticket Format — smartcard top-up receipt formats | corrected | NIR Layout 12 + Glider 13/13C verified directly; 13A/13B inferred from same family | FBD-100363 + layout docs |
| 4103943 | Ticket Format — annul or cancel ticket (Format 16) and Non-Issue | corrected | ref FBD-100373 wrong (Refund spec, explicitly a different process from annulment); Format 16 (4 variants) + Layout 16 Non-Issue verified directly | FBD-100363 + layout docs |
| 4103944 | Ticket Format — faulty smartpass or smartcard receipt | corrected | Layout 18 + Glider Faulty Smartcard Receipt verified directly | FBD-100363 + layout docs |
| 4103945 | Ticket Format — travel receipt and print-test ticket | corrected | Layout 17 + Layout 15 verified directly | FBD-100363 + NIR layouts |
| 4103946 | Ticket Format — penalty fare warning ticket | corrected | ref FBD-100690 unsubstantiated (dropped); Glider Penalty Fare Warning + XB NIR Penalty Fare formats verified directly | FBD-100716, FBD-100363 + layout docs |
| 4103947 | Waybill — Operator Waybill prints the duty's transactions | corrected | ref FBD-100373 wrong (Refund spec, only mentions waybill in passing); Waybills V.5 + REQ-0329.1 verified directly | Waybills-V5, REQ-0329.1 |
| 4103948 | Waybill — end-of-shift waybill with no transactions | corrected | same ref correction; nil-transaction edge case not explicit in source, reasonable inference flagged for a live spot-check | Waybills-V5, REQ-0329.1 |
| 4103949 | Waybill — annulment lines are included | corrected | ref FBD-100373 wrong; Annul row in Payments Summary confirmed directly | Waybills-V5 |
| 4103950 | Waybill — validation, inspection and barcode activity are included | corrected | refs FBD-100373 + FBD-100651 both wrong (FBD-100651 is Glider ABT tap-validation logic, unrelated); all four fields confirmed directly | Waybills-V5, REQ-0329.1 |
| 4103951 | Single-Use Barcode — encryption keys fetched once per shift at sign-on | verified-clean-with-citation | once-per-shift GET + ≤6 keys confirmed verbatim in FBD-100483 v7.00 | FBD-100483 |
| 4103952 | Single-Use Barcode — encryption-key fetch failure does not block sign-on | verified-clean-with-citation | 500/no-response retry-every-30s behaviour confirmed verbatim | FBD-100483 |
| 4103953 | Single-Use Barcode — AES versus TripleDES selected from encrypted string | verified-clean-with-citation | pipe/version-number rule confirmed verbatim | FBD-100483 |
| 4103954 | Single-Use Barcode — valid decrypt has exactly 17 commas and a known type | verified-clean-with-citation | "18 fields... 17 commas... B,D,E,H,S,U" confirmed verbatim | FBD-100483 |
| 4103955 | Single-Use Barcode — decrypt failure shows the decryption-failed message | verified-clean-with-citation | exact message text + 3s timeout confirmed verbatim | FBD-100483 |
| 4103956 | Single-Use Barcode — manual 12-digit reference validated as the ShortID | verified-clean-with-citation | manual reference entry as ShortID → /validate path confirmed | FBD-100483 |
| 4103957 | Single-Use Barcode — locally used ShortID rejected before going online | verified-clean-with-citation | exact "already been used" message + no-online-call confirmed verbatim | FBD-100483 |
| 4103958 | Single-Use Barcode — redeemed barcode emits event 1412 | verified-clean-with-citation | event code 1412 confirmed verbatim | FBD-100483 |
| 4103959 | Single-Use Barcode — redeem timeout queues offline and emits event 1416 | verified-clean-with-citation | event code 1416 + offline queue + still-prints confirmed verbatim | FBD-100483 |
| 4103960 | Single-Use Barcode — offline value above ceiling limit is rejected | verified-clean-with-citation | exact "exceeds offline validation limit" message + Retry/Cancel confirmed verbatim | FBD-100483 |
| 4103961 | Single-Use Barcode — offline sweep redeems queued barcodes without CloudFare events | verified-clean-with-citation | 15-minute sweep interval + no-events-during-sweep confirmed verbatim | FBD-100483 |

## Totals

- **verified-clean-with-citation:** 14 (4103929, 4103934, 4103935, 4103951–4103961)
- **corrected:** 22 (4103923, 4103926–4103935 excl. verified ones, 4103937–4103950 — see table)
- **flagged-gap:** 3 (4103924, 4103925, 4103936)

## Spec surprises worth flagging to the wider audit

1. **FBD-100373 (Refund on POS) was cited on 6 of 12 Ticket Formats & Waybill cases** and supports
   none of them — it is a refund-process spec that only mentions waybills/refund-lines in passing.
   The real source for waybill content is a non-FBD document (`Waybills V.5.pdf`) plus REQ-0329.1/
   REQ-0350.x in the TFTS Requirements Matrix. Worth checking whether other batches/sections made
   the same substitution (FBD-100373 looks like it was picked by keyword-match on "waybill" rather
   than opened and read).
2. **FBD-100383 (Operator Hierarchy) was used as a catch-all HHD-role citation** (sign-on, sign-off,
   act-as-operator, home location) across 6 cases in this batch — it is purely an org-tree/config-
   inheritance document and contains none of that content. The real source for HHD role mechanics is
   the TFTS Requirements Matrix (REQ-0050.x, REQ-0098.1, REQ-0099.1, REQ-0305.x, REQ-0360.0,
   REQ-0514.1, REQ-0656.0, REQ-1137.0) — none of these REQ numbers were cited anywhere in the batch
   before this pass.
3. **FBD-100342 (User Claims) was used for on-device Supervisor/Technician menu cases** — it's the
   CloudFare/ABT Operator Portal web-claims spec, unrelated to the HHD's own menu.
4. **FBD-100651 (Glider Tap-On-Only) was cited on a waybill case** with no barcode/waybill content
   at all — it's entirely Glider ABT PV/HHD-inspection tap-validation logic.
