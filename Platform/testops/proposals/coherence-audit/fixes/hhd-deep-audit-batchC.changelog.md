# HHD Deep Audit — Batch C changelog

Suite 30285, sections: Functional / Top-Ups, Functional / Penalty Warning & Fares,
Functional / Sign On & Session, Functional / Operator. 44 cases (4103879–4103922).

Legend: **verified-clean** = citation checked against the full spec and it genuinely supports the
claims, no change. **corrected** = citation and/or wording fixed. **flagged-gap** = a claim has no
supporting text anywhere searched in the requirement library; logged to the gaps file, refs marked
`gap-register`, case body otherwise left intact (no invented fill-in).

## Functional / Top-Ups

| ID | Verdict | Note | Refs (final) |
|---|---|---|---|
| 4103879 | corrected | Added FBD-100268 (Recharge Allowed=Yes on HHD) — the actual device-capability evidence; FBD-100261 never mentions HHD. "Period" product marked GAP in the data-variations list (not in the card taxonomy). | FBD-100261,FBD-100268 |
| 4103880 | verified-clean | FBD-100261 fare-configuration section (manual/rule-based per journey amount) directly supports the claim. | FBD-100261 |
| 4103881 | corrected | "45-journey maximum" is not in FBD-100261 or anywhere searched — reworded to the assumed-knowledge-value pattern ("the configured maximum"); underlying enforcement behaviour itself also unconfirmed, logged. | FBD-100261,gap-register |
| 4103882 | flagged-gap | "Expired journeys removed before new top-up" has no textual support anywhere searched. | FBD-100261,gap-register |
| 4103883 | verified-clean | Already carries an internally-tracked conflict (`gap-register Q16`, opposite outcome to C4103831) — left as-is, no new action needed from this batch. | FBD-100261,gap-register Q16 |
| 4103884 | verified-clean | Generic cash-tender behaviour, adequately covered by top-up context. | FBD-100261 |
| 4103885 | verified-clean | Same. | FBD-100261 |
| 4103886 | verified-clean | Same. | FBD-100261 |
| 4103887 | verified-clean | Same. | FBD-100261 |
| 4103888 | corrected | Added FBD-100236 — Operator Number `0x2057` gate is the actual mechanism rejecting a non-Translink card. | FBD-100261,FBD-100236 |
| 4103889 | verified-clean | Generic reprint behaviour, no contradicting evidence. | FBD-100261 |
| 4103890 | corrected | Dropped FBD-100373 — that spec explicitly excludes HHD from refunds ("HHD = sales+reversals, no refunds"); citing it here is actively misleading. Flagged the underlying reversal mechanism as unconfirmed. | FBD-100261,gap-register |
| 4103891 | verified-clean | Mini-statement-after-top-up behaviour consistent with FBD-100261 + cross-device mini-statement pattern (ETM flow). | FBD-100261 |
| 4103892 | corrected | Dropped FBD-100341 — that spec is scoped explicitly to "TVM & POS" (zero HHD mentions, verified by full-text search). | FBD-100261 |

## Functional / Penalty Warning & Fares — headline finding

**All 8 cases in this section (plus 4103921 in Operator) describe a manual, operator-menu-driven,
ticket-printing "penalty warning / penalty fare" workflow. FBD-100716 — the only spec that actually
covers HHD revenue-inspection/penalty behaviour — describes something categorically different: an
automated cEMV-bank-card inspection that, absent a valid tap-on, triggers an ABT back-office
"Standard Fare" charged automatically at End-of-Day settlement (no operator action, no printed
ticket).** A full-text search of FBD-100716 for "penalty warning", "whitelist", and "waybill" found:
one line mentioning "penalty fares/warnings issued" (a reporting rollup, §5.10 Revenue Inspectors
report) and nothing else. No whitelist, no waybill, no role-differentiated ticket, no manual
issuance action, no printed-ticket format exists anywhere in the cited spec, in FBD-100651, in
FBD-100690, or in FBD-100658 (ABT Audit) — all checked directly.

| ID | Verdict | Note | Refs (final) |
|---|---|---|---|
| 4103893 | flagged-gap | Manual "issue a penalty warning" + printed ticket — unsupported. | FBD-100716,gap-register |
| 4103894 | flagged-gap | Same, off a smartcard (not cEMV) inspection — unsupported. | FBD-100716,FBD-100651,gap-register |
| 4103895 | flagged-gap | Manual "issue a penalty fare" from operator menu — unsupported. | FBD-100716,gap-register |
| 4103896 | flagged-gap | Same, against invalid/expired smartcard — unsupported. | FBD-100716,FBD-100651,gap-register |
| 4103897 | flagged-gap | Role-differentiated ticket printing (Operator/Supervisor) — unsupported. | FBD-100716,gap-register |
| 4103898 | flagged-gap | Operator "whitelist" for issuing penalty fares — zero hits for "whitelist" in FBD-100716. | FBD-100716,gap-register |
| 4103899 | flagged-gap | Dropped FBD-100341 (wrong scope, see 4103892). "Client shift id" IS a real requirement on cEMV inspection events (FBD-100716 para 353) but that's the automated path, not a manual "penalty fare" transaction. | FBD-100716,gap-register |
| 4103900 | flagged-gap | Waybill listing issued penalties — unsupported (waybills exist in ETM/POS flows, never in a penalty context). | FBD-100716,gap-register |

## Functional / Sign On & Session

**Systemic finding:** most cases in this section cite FBD-100383 ("TFTS Operator Hierarchy") as
their sole ref. A full-text search of FBD-100383 for sign-on, PIN, duty, lockout, "Device Locked",
and "Message of the Day" returns **zero hits** — the document is entirely about the CloudFare
operator/location hierarchy tree and config inheritance, and never once touches sign-on mechanics.
The closest real evidence for the sign-on UX (3-attempt lockout, "Device Locked — Present Supervisor
Card", Message of the Day / Word & Colour with "Unavailable" fallbacks, "Sign On Failed — N of 3")
is the **POS** Overflow flow (`knowledge/flows/translink-pos-signon.md`) — but that is explicitly a
POS (Wayfarer) flow, not an HHD one, and no HHD-specific sign-on design doc exists in the local
library.

| ID | Verdict | Note | Refs (final) |
|---|---|---|---|
| 4103901 | flagged-gap | Manual+smartcard sign-on reaching Operator menu — FBD-100383 doesn't cover it; POS analog exists but unconfirmed for HHD. | gap-register |
| 4103902 | flagged-gap | Invalid ID/PIN rejection — same issue. | gap-register |
| 4103903 | flagged-gap | Lockout after configured attempts + Device Locked screen — same issue. | gap-register |
| 4103904 | verified-clean | FBD-100359 genuinely uses the term "communication locked state" for a sustained Translink-network outage; adequate citation. | FBD-100359 |
| 4103905 | flagged-gap | Duty number entry — FBD-100383 has no duty-number content. | gap-register |
| 4103906 | flagged-gap | Message of the Day / Word & Colour — FBD-100383 has zero content; matches the POS flow doc exactly (uncited, unconfirmed for HHD). | gap-register |
| 4103907 | verified-clean | FBD-100383 genuinely covers per-location config/topology inheritance — the one case in this run where the citation is correct. | FBD-100383 |
| 4103908 | verified-clean | FBD-100296 covers route selection at sign-on governing fares/topology (ETM-detailed but principle-general) — adequate. | FBD-100296 |
| 4103909 | flagged-gap | Sign off / CloudFare audit — FBD-100383 has no sign-off content. | gap-register |
| 4103910 | flagged-gap | Auto sign-off after inactivity — same issue. | gap-register |
| 4103911 | flagged-gap | Forced sign-off when docked — same issue; the POS flow's "power interruption" note is a different scenario. | gap-register |
| 4103912 | verified-clean | FBD-100266 is an exact match (15-min staff-list heartbeat, works signed-off, resets Hours-Since-Last-Communication). | FBD-100266 |
| 4103913 | flagged-gap | "CR78" is not locatable in the requirement library; neither FBD-100651 nor FBD-100690 contains any driver/operator-break or mode-resume text (checked directly). | FBD-100651,FBD-100690,gap-register |

## Functional / Operator

| ID | Verdict | Note | Refs (final) |
|---|---|---|---|
| 4103914 | flagged-gap | FBD-100342 covers only KeyCloak back-office admin menus — no on-device Operator Menu content. | gap-register |
| 4103915 | verified-clean | FBD-100342's composite/base-claim + negative-permission model directly supports role-scoped menu restriction. | FBD-100342 |
| 4103916 | flagged-gap | FBD-100276 is a back-office-only REST API ("no user interaction" per its own scope) — no on-device View Totals content. | gap-register |
| 4103917 | flagged-gap | Dropped FBD-100276 (same reason). The specific layout labels "NIR Layout 20 / Glider Format 15" in Expected Result have no source anywhere searched — marked GAP in place. | gap-register |
| 4103918 | flagged-gap | FBD-100260 has zero "favourites" content; no spec anywhere describes a sale-favourites feature — existence itself unconfirmed. | gap-register |
| 4103919 | flagged-gap | Same as 4103913 (CR78 unfindable, cited FBDs have no break/resume content). | FBD-100651,FBD-100690,gap-register |
| 4103920 | flagged-gap | FBD-100266 never describes an on-device "Status" menu option (it's the back-office heartbeat/Comms-Monitor spec). | gap-register |
| 4103921 | flagged-gap | Same core issue as the Penalty Warning & Fares section — manual "issue a penalty fare warning" + printed ticket unsupported by FBD-100716 or FBD-100690. | FBD-100716,FBD-100690,gap-register |
| 4103922 | flagged-gap | Dropped FBD-100383 (zero printer content). FBD-100320 confirms HHD Bluetooth-pairs to its Miura M020 *payment* device — closest analog, but doesn't confirm ticket-printer pairing specifically. | FBD-100320,gap-register |

## Totals

- **verified-clean-with-citation:** 13 (4103880, 4103883, 4103884, 4103885, 4103886, 4103887,
  4103889, 4103891, 4103904, 4103907, 4103908, 4103912, 4103915)
- **corrected:** 5 (4103879, 4103881, 4103888, 4103890, 4103892)
- **flagged-gap:** 26 (all Penalty Warning & Fares cases + 4103921; most of Sign On & Session;
  most of Operator — see tables above)
