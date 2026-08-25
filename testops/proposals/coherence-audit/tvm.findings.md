# TVM Coherence & Capability-Grounding Audit

**Scope:** all 201 cases in `suite_TVM.json` (C4103599–C4103799), checked for internal coherence
(title ↔ preface ↔ preconds ↔ steps ↔ expected) and capability grounding against
`knowledge/translink/specs/FBD-*.md` (barcode: 100167 / 100317 / 100483; smartcard: 100236 / 100250 /
100261; fares: 100336 / 100450). Report-only — no edits, no push.

**Summary:** 201 cases audited. The large majority are coherent and well-grounded (fare-issue,
payments-cash, EMV, basket, ticket-numbering, grouped-stops, commissioning, EMS/TMS, resilience are
clean, and the barcode-redemption online/offline state machine matches FBD-100483 precisely —
events 1412/1417, RouteId-not-validated, 400=3s/500=3×30s, ceiling limit, legacy stages all correct).
**16 findings**: **2 High**, **8 Med**, **6 Low**. Two systemic themes dominate: (a) the TVM is a
**booking-reference/Collect-Ticket-Code device with no barcode scanner** (FBD-100317), yet several
cases describe *presenting/scanning* barcodes; (b) the whole **Smartcards & ABT** capability on TVM
is **unsupported by the available specs** (FBD-100261: "POS is the only device that issues these
smartcard products") and needs confirmation.

---

## Findings

**C4103628** | High | grounding / incoherent | Title "a multiple-use barcode is rejected"; step "**the multiple-use barcode is presented**" → "This Barcode Type is not accepted on this device". Per FBD-100317 the TVM collects by **Collect Ticket Code entry only (NOT barcode/BRID scan)** and "has no interaction" with a presented barcode ("should never happen operationally"). There is no scanner to "present" a 2D barcode to. Directly contradicts C4103629 (same section) which states no barcode scan input exists. The rejection *message string* is real, but the trigger interaction is impossible on a TVM. | Re-scope: either delete (TVM can't be handed a multi-use barcode) or reframe as "a Collect Ticket Code for a multi-use/manifest product is refused" and assert the message on **code entry**, not on presenting a barcode.

**C4103641** | High | coherence / factual | Title "foreign notes are rejected"; preface "rejects banknotes that are **not sterling currency**"; step inserts a **Scottish banknote** → rejected. Scottish notes **are** pound sterling (issued by Scottish banks), not foreign/non-sterling — so the rationale is factually wrong. Worse, it contradicts C4103639, whose preface accepts "valid UK banknotes **from every issuing bank**" (which would include Scottish issuers). The suite both accepts and rejects Scottish-issuer notes, and the THEN here may be the wrong expected result. | Decide the real acceptance policy for the note validator, then reword: if Scottish notes are refused it is by accepted-note-type config, not because they are "foreign/non-sterling". Reconcile with C4103639's "every issuing bank" claim.

**C4103599** | Med | grounding (needs-confirmation) | Title/preface: "issuing a new journey-based smartcard **on the TVM**"; preconds cite **FBD-100261**. But FBD-100261 states plainly: **"POS is the only device that issues these smartcard products"** (SmartCreate). The case contradicts the very spec it cites. | Confirm whether Translink TVMs actually issue Multi-Journey smartcards (SmartCreate). If not, remove/relabel as POS. If yes, cite the requirement that authorises TVM issue instead of FBD-100261.

**C4103617** | Med | grounding | ABT card *issue* on the TVM: "completes the ABT card issue with name and email" → "the ABT Data and SigFile are written to the card" + registration to ABT back office. Per FBD-100236 this is the **Card Bureau / issuer (AbtPerso)** function (writes ABT Data + SigFile with the issuer private key) and **bureau-sent registration** (Child/24+/yLink) — not a device/TVM capability. Terminals *verify* the RSA signature; they do not write it. | Confirm TVM can personalise/write ABT cards. If not (expected), move to a bureau/BOS suite; a TVM case should at most assert *reading/validating* an ABT card, not writing SigFile.

**C4103729** | Med | grounding | Title "collect a pre-paid ticket **using a BRID**"; step "enters the valid **BRID**". FBD-100317 device matrix: **TVM = Collect Ticket Code only (NOT barcode/BRID)** — BRID (12-digit) is the POS/HHD fallback. Labelling the TVM entry a "BRID" mis-attributes a POS/HHD mechanism to the TVM, and contradicts C4103629 ("no … BRID scan input is offered"). | Rename to "booking reference / Collect Ticket Code" (as C4103620 does). Note the whole Ticket Collection section (C4103729–C4103732) duplicates the entry-validation cases already in Barcode Redemption (C4103620/25/26) — consider folding.

**C4103677** | Med | grounding | Smoke "Ticket Collection": precond "a pre-paid order identified by a valid **collection barcode** or booking code"; step "presents the collection reference". "Collection barcode … presents" implies a **scan**, which the TVM cannot do (FBD-100317: Collect Ticket Code entry only). | Reword to collection by keyed booking reference / Collect Ticket Code; drop "barcode" and "presents".

**C4103600 / C4103601 / C4103602 / C4103603 / C4103604 / C4103733–C4103737** | Med | grounding (needs-confirmation) | Smartcard **top-up (SmartRecharge)**, **details read**, top-up-button labelling from Display Description, and **mini-statement** — all assume the TVM reads/writes Mifare Multi-Journey/Period/DayLink cards. Available specs put smartcard *issue* on POS only (FBD-100261) and smartcard *validation* on GV/PV/HHD (FBD-100250 suite implications); none document TVM smartcard read/write. | Confirm the TVM hardware has a smartcard reader and performs top-ups/mini-statements in this deployment. If confirmed, add a TVM hardware/capability reference to `knowledge/`; if not, these belong on POS. (Grouped here as one systemic needs-confirmation, not per-case defects.)

**C4103605 / C4103606 / C4103607 / C4103608 / C4103609 / C4103610 / C4103614** | Med | grounding (needs-confirmation) | Concession pricing by **presenting a physical Smartpass/yLink/24+/Staff smartcard** to the TVM, and passback rejection (C4103614), all depend on the same unconfirmed TVM smartcard-read capability. Values/variants (Fare Foregone, funded-disability, staff variants) map correctly to FBD-100250 taxonomy — the open question is purely whether the **TVM** reads these cards. | Same confirmation as above. If the TVM has no smartcard reader, concession-by-smartcard cases are POS/validator scope.

**C4103618 / C4103619** | Low | grounding (needs-confirmation) | ABT-without-TRK rejection (AIDs `0x414254` / `0x54524B` — **correct** per FBD-100236) and ABT product top-up posting to CloudFare. ABT *validation* is a validator (GV/PV/HHD) behaviour per FBD-100236; whether a **sales TVM** performs ABT card validation/top-up is unconfirmed. | Confirm TVM ABT interaction; AID values themselves are accurate, so only the device attribution needs checking.

**C4103629** | Low | grounding (terminology) | Precond references "a **manifest** Collect Ticket Code". Manifest = barcode **type F = ETM only** (FBD-100317); TVM handles W (bus) and B/U/E/S/D/H (rail), not F. The case's core assertion (booking-reference entry only, no scan) is otherwise correct and well-grounded. | Drop "manifest"; use a TVM-valid type (e.g. a Walk-up / rail Collect Ticket Code).

**C4103675** | Low | needs-confirmation (intentional) | Fare marked "(fare per the current fares export — **needs confirming**)". This is a correctly-flagged open value, not a defect — noted for closure once FBD-100336/100450 oracle values are pinned. | Confirm the Metro Single Adult fare against the fares export and remove the marker.

**C4103660** | Low | needs-confirmation | Chip & PIN min/max limits asserted as 15p reject / 20p accept / £500.05 reject / £500.00 accept. Plausible but not present in the available specs (FBD-100183 is POS hardware; no TVM EMV floor/ceiling doc reviewed). | Confirm the configured min/max EMV transaction values for the TVM Ingenico terminal.

**C4103655 vs C4103778 ; C4103656 vs C4103779** | Low | duplication | Two separate "Coin Recycler Hopper (Kiosk only)" sections carry near-identical pairs: Cash Content Report after hopper replacement (C4103655 ≈ C4103778) and reload/replenish (C4103656 ≈ C4103779). Coherent individually but redundant. | Consolidate into one Kiosk coin-recycler section.

**C4103604 vs C4103733** | Low | duplication | Multi-Journey mini-statement-after-top-up appears in both the Smartcards & ABT section (C4103604) and the Mini Statement section (C4103733). | Keep one (Mini Statement section) and remove the duplicate.

**C4103674 vs C4103794** | Low | duplication | Screensaver-wake-on-tap appears as a Smoke case (C4103674, → Sales home) and a Resilience case (C4103794, → mode-of-transport home). Same behaviour, slightly different expected screen name. | Align the expected screen wording and keep a single canonical case.

---

## Notes for the author
- The barcode-**redemption** state machine (C4103620–C4103633) is the strongest part of the suite and
  matches FBD-100483 line-for-line (events 1412/1417, RouteId-not-validated, 400→3s-to-Home,
  500→retry-3×/30s→offline fallback, ceiling-limit offline refuse, legacy-stage resolution, exact
  message strings). No changes needed there beyond the scanner-interaction wording flagged above.
- Grouped Stops (C4103722–C4103728) matches FBD-100515 exactly (default-to-group, alighting spans all
  boarding stops, cheapest-non-zero fare, first-combination tie-break, "not nearest the TVM" gotcha,
  no-valid-fare error). Clean.
- The dominant risk is capability attribution, not wording: **does the Translink TVM have a smartcard
  reader and a barcode scanner?** The available specs say the TVM is booking-code entry only (no
  scanner) and POS-only for smartcard issue. If the real hardware differs, add a TVM capability note
  to `knowledge/` so future audits ground against it; if it matches the specs, ~30 smartcard/ABT and
  a handful of barcode-scan cases are mis-scoped to the TVM.
