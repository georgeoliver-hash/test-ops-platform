# HHD deep-grounding audit — Batch E changelog

Suite 30285, sections: Multi-Use Barcodes / Old Barcode Redemption (BRS) / Smartcard Inspection /
Revenue Inspection (cEMV/RID). 29 cases (4103962–4103990). C4103982 left alone per instruction
(known conflict vs C4103835, gap-register Q17 — human-owned).

Legend: **verified-clean** = existing refs checked against the real spec and confirmed correct, no
change. **corrected** = refs and/or body fixed. **flagged-gap** = a claim has no supporting spec;
marked GAP/UNCONFIRMED, not invented. **left alone** = out of scope for this batch.

## Multi-Use Barcodes (FBD-100167)

| ID | Title | Verdict | Note |
|---|---|---|---|
| 4103962 | Valid barcode — green tick/audio | verified-clean | FBD-100167 §"success" para 488/504: green tick + audio confirmed verbatim. |
| 4103963 | Route/location-only failure — yellow question mark | verified-clean | FBD-100167 para 505: yellow question mark, "3 seconds or if another transaction / driver clears" — matches exactly. |
| 4103964 | Invalid barcode — red cross + reason | verified-clean | FBD-100167 para 504/507: red cross + stated failure reason confirmed. |
| 4103965 | Re-presented barcode within passback window rejected | verified-clean | FBD-100167 para 272/477: Unique ID retained for configurable passback minutes on ETM/HHD; re-presentation rejected. Value correctly left as "configured passback minutes" (assumed-knowledge), not hard-coded. |
| 4103966 | Rail location failure falls back to valid above fare threshold | verified-clean | FBD-100167 para 531 confirms verbatim: fare ≥ £90 (TMS-configurable) treated as valid under CR105.3. Refs `FBD-100167,CR105.3` correct. |
| 4103967 | Successful validation audits zero-fare BarcodeUsage transaction | verified-clean | FBD-100167 para 506: transaction record w/ barcode Product ID, zero fare, payment type BarcodeUsage — confirmed verbatim. |
| 4103968 | Failed validation sends event with Unique ID | verified-clean | FBD-100167 para 507: failed validation → event with Unique ID + reason — confirmed. |
| 4103969 | Midnight–4am expiry displays previous day, no time | verified-clean | FBD-100167 para 551/569 confirms the exact worked examples (20240520-0400→19/05/2024, -0159→19/05/24, -0401→20/05/24 04:01) under CR116. Refs `FBD-100167,CR116` correct. |

## Old Barcode Redemption (BRS)

| ID | Title | Verdict | Note |
|---|---|---|---|
| 4103970 | Old Barcode Redemption — legacy BRS barcode redeemed on Glider | **flagged-gap** | No document anywhere in the requirements library mentions "BRS" or an "Old Barcode Redemption" flow (searched FBD-100167/317/318/483 + filename search across the whole library). FBD-100317's device matrix and the "Barcode Acceptance on TFTS Devices" table both show Glider HHD validates **multi-use offline only** and rejects every single-use barcode class; FBD-100483 explicitly states "Glider HHD does NOT use single-use functionality." This confirms and upgrades the prior coherence-audit flag to a full gap — the case asserts a capability with no supporting spec. Marked GAP in preface + expected; refs corrected to the two docs actually checked (FBD-100317, FBD-100483), dropping FBD-100167 (irrelevant — multi-use only). Logged to gaps.md. |

## Smartcard Inspection

All 7 cases (4103971–4103977) cited **FBD-100651**, which is wrong for this section — FBD-100651
is the Glider cEMV bank-card Tap-On-Only spec (a different technology to iLink/period-pass NFC
smartcards). Corrected across the board to the two local docs that actually ground the general
capability: `Smartcard Use Matrix.xlsx` (confirms iLink validated on HHD) and the `HHD Inspection
and Validation Design Note` (NIR Inspection + Validation section — commercial-smartcard inspection
reuses the Validation flow, writes a usage record, "For error scenarios see UX").

| ID | Title | Verdict | Note |
|---|---|---|---|
| 4103971 | Valid period pass inspected successfully | corrected | Ref fixed only; body already correctly uses an assumed-knowledge "configurable time" precondition (no invented number). |
| 4103972 | Adult iLink pass shows adult colour | **flagged-gap** | No spec found anywhere documents pass-type colour-coding on the HHD inspection screen (checked FBD-100236, FBD-100250, the Design Note, Smartcard Use Matrix). Marked **UNCONFIRMED** at the exact claim. |
| 4103973 | Child pass shows child colour | **flagged-gap** | Same finding as 4103972 — no colour-coding rule found. Marked **UNCONFIRMED**. |
| 4103974 | Expired smartcard fails inspection | corrected | Ref fixed only. General failure outcome is safely inferable (Design Note defers error screens to a separate UX doc, confirming a failure path exists; EA Smartpass Logic / FBD-100250 confirm validity is fare/expiry-gated) and the case only asserts a generic "unsuccessful result", not an invented screen — correct "unknown how" treatment, no marker needed. |
| 4103975 | Pass inspected within passback window accepted | **flagged-gap** | The hard-coded "20 minutes ago... 90-minute window" could not be traced to any spec. The only "~90 minute" figure anywhere in the reqs library is the Glider/NIR **cEMV inspection** Maximum Journey Time (FBD-100651/FBD-100716) — a different mechanism (bank-card penalty-fare window, not smartcard revalidation). This looks like cross-contamination between the two inspection flows (matches the task brief's concern about cEMV duplication bleeding into other sections). Reframed as an assumed-knowledge precondition per gherkin-standard's "unknown configured value" rule instead of asserting an unconfirmed number. |
| 4103976 | Pass inspected after window offers revalidation | **flagged-gap** | Same finding/fix as 4103975. |
| 4103977 | Inspection available in break mode (CR78) | **flagged-gap** | CR78 could not be found anywhere in the requirements library (`--find "CR78"`, `"break mode"`, `"break"` all empty except an unrelated ETM config sheet). Existence of a "break mode" sign-on state and whether smartcard inspection works in it is unconfirmed. Marked GAP. |

## Revenue Inspection (cEMV/RID)

All verified word-for-word against `FBD-100716 Translink Revenue Inspection Specification v5.00`
(paras 275–352, 447, 498–502) and, where cited, `FBD-100651` for the ABT-Type inspection-button
gating rule. No changes needed — this section was already accurately grounded.

| ID | Title | Verdict | Note |
|---|---|---|---|
| 4103978 | Inspection Mode enabled on Tap-On-Only route | verified-clean | FBD-100651 "Enable cEMV inspection via ABT Type... Tap On Only (Flat Fare) ⇒ inspection button enabled"; FBD-100716 para 277 confirms oval soft key trigger + M020 wake. |
| 4103979 | Inspection Mode disabled on non-Tap-On-Only route | verified-clean | Same FBD-100651 rule, inverse case — correct. |
| 4103980 | Valid card inspection succeeds, event 5008 | verified-clean | FBD-100716 para 347 verbatim: "Successful inspection – Event code 5008". |
| 4103981 | Card on RID List fails, event 5009 | verified-clean | FBD-100716 para 336/348 verbatim: message "Card on RID List", event 5009. |
| 4103982 | Expired card declined, event 5010 | **left alone** | Known unresolved conflict vs C4103835 (gap-register Q17) — human-owned, not touched per instruction. (For the record: FBD-100716 para 349 does confirm "Card Declined" + event 5010 as a real M020-integrity-check outcome, so the conflict is about modelling/overlap with C4103835, not about whether this behaviour exists.) |
| 4103983 | Card failing ODA declined, event 5011 | verified-clean | FBD-100716 para 350 verbatim. |
| 4103984 | Unsupported scheme declined, event 5012 | verified-clean | FBD-100716 para 282/351 verbatim (Visa/Mastercard/Maestro accepted schemes). |
| 4103985 | No BO connection — try-again message | verified-clean | FBD-100716 para 334 verbatim: "Failed to connect please try again". |
| 4103986 | No card in 30s times out to Sales screen | verified-clean | FBD-100716 para 323 verbatim: 30-second timeout to Sales screen. |
| 4103987 | Inspection tap cannot be annulled | verified-clean | FBD-100716 para 304 verbatim: "there is no way to annul the inspection tap." |
| 4103988 | Full RID List requested on app start-up | verified-clean | FBD-100716 para 258 verbatim (full list, deferred if comms down). |
| 4103989 | 15-minute poll requests delta RID List | verified-clean | FBD-100716 paras 262–270 verbatim. |
| 4103990 | First poll after EOD requests full RID List | verified-clean | FBD-100716 para 264 verbatim (list timestamp before last EOD ⇒ full request). |

## Informational finding (not actioned — structural, human decision)

The Revenue Inspection (cEMV/RID) cases in this batch (4103978–4103990) are the properly-scoped,
well-cited home for cEMV/M020 inspection behaviour per FBD-100716. If C4103833/C4103834/C4103835
(flagged in the "Smartcards & ABT" section of another batch) genuinely duplicate this cEMV
inspection-tap behaviour, that duplication should be folded into this Revenue Inspection section
per `docs/test-practices.md`'s consolidation lens — but that is a structural/human decision, not
made here.

## Totals

- verified-clean-with-citation: 19 (8 barcode + 12 cEMV, minus untouched 4103982 counted separately)
- corrected: 2 (4103971, 4103974)
- flagged-gap: 6 (4103970, 4103972, 4103973, 4103975, 4103976, 4103977)
- left alone (out of scope): 1 (4103982)
- Total: 28 actioned + 1 left alone = 29
