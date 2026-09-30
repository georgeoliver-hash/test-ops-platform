# Cross-examination: `POS-Functional-Specification.docx` vs everything held on Translink POS

**New document:** `C:\Users\GeorgeOliver\Downloads\POS-Functional-Specification.docx` (not yet uploaded to the platform). 28 sections, 617 headings, 435 tables, 223-page inventory. Its own §28 ("Traceability — Source Files") shows it was built by reverse-engineering the actual POS app source (Xamarin/Android C# — `POS_Features/…`, `Submodules/…`, with file:line citations throughout), not from the FBD requirement docs. That is the single most important fact about this document: **it is a different kind of source than everything else in this comparison** — ground truth from the shipped code/build, not a requirements spec. Treat contradictions against it as "the FBD doc / knowledge note is describing intent or an older build; the new doc is describing what the code on this build actually does" — not as two equally-weighted opinions.

**Compared against:**
1. Old TestRail suite snapshot — `system-test-ops/reports/tfts-system-test/aa-pos-acceptance-test/2026-09-24/cases.md` (2,193 cases)
2. Uploaded POS docs on the platform — `test-ops-platform/Platform/webapp/data/uploads/Translink/POS/` (~120 files)
3. Curated POS knowledge notes — `system-test-ops/knowledge/translink/specs/*.md` (cited-to-paragraph summaries of individual FBD docs)
4. In-progress TestRail proposals — `system-test-ops/proposals/Translink-POS-suite-restructure/*.cases.yaml` (9 areas authored so far)
5. sit's real POS automation — `sit/Resources/Devices/POS/**` (Bindings) and `sit/Tests/POS/**/*.robot` (42 existing tests)

---

## Executive summary

- **A direct contradiction found, and it's live in a case I already edited today.** FBD-100261 (CloudFare product-config spec) says the Ulsterbus Multi-Journey card reference number is chosen from an **on-screen menu** (range group → leaf, ~62 CloudFare product groups). The new doc's §12.4.2 (screens `8_2_1_1`/`8_2_1_2`) says it is **typed on the numeric keypad as free text** into a "Card Reference Number" field, validated with an "Invalid number entered" error state. These describe two different UIs for the same action. **See finding #1 — this needs fixing in the FBD-100277 proposal before it's pushed.**
- **One of the two open GAP/UNCONFIRMED markers from FBD-100277 is now answerable with cited evidence.** §25.9 of the new doc names the exact class that runs card-reference validation: `POS_Features/POS.Android/Workflow/SmartCard/Validation/BRCompleteValidation.cs`. That's POS Android app code — the "which device runs this?" marker can be closed as **POS, confirmed by source citation** (with the caveat below about which algorithm it actually is).
- **That same evidence opens a new, second-order question**, though: the new doc's §25.10 says the *furthest-alighting-point file* (`FurthestAlightingPoints.json`) is downloaded but **never read by any code** — real alighting lookups go through a `TopologyService` instead. FBD-100277's "furthest-down fares-triangle column" algorithm may be describing a mechanism that's since been replaced or is implemented differently inside `TopologyService`. Not resolved — flagged as a new, more precise question to put to an engineer.
- **The new doc fully covers two categories sit's Robot suite has zero automation for**: Transactions (§8 Basket & Payment, §9 Card Payment, §11 Smartcard Top-Up, §12 Issue Card) and Printing (§22). It's screen-by-screen with button maps, timeouts and error states — everything `test-author` would need to actually build `Tests/POS/Transactions/` and `Tests/POS/Printing/` from scratch.
- **The new doc also gives sit a real, previously "not confirmed" BOS audit contract.** `test-automation-sit`'s own project memory states the BOS API is unconfirmed and `BOSClient.get_audit_events` deliberately raises `NotImplementedError`. The new doc's §24 specifies the actual endpoints, envelope, sequence-number injection, retry/lock thresholds and headers, with source citations. This is a real gap-closer, just not for *this* repo (sit) directly — it's evidence for whoever owns that decision in `test-automation-sit` or eventually in `sit` itself.
- No device-attribution violations found: a full-text sweep for ETM/TVM/GV/PV/HHD/BV mentions turned up only correct usage (config-tree entries like "ETM Ulsterbus", a UI convention literally named "letters (ETM) entry mode", and a code-comment citation about ETM's own separate behaviour) — nothing that attributes POS-specific behaviour to another device type or vice versa.

---

## Finding 1 (CONTRADICTION) — Ulsterbus Multi-Journey card reference: menu selection vs. keypad entry

**Old side:**
- `knowledge/translink/specs/FBD-100261-multi-journey-product-configuration.md` §"POS Ulsterbus Multi-Journey card issue flow (section 5.2)": *"Select a card reference number — approx. 50 reference numbers available, grouped into ranges of max 8 per range (7 range-groups) for on-screen selection... Requires ~62 new product groups for POS: 1 range-selector + 7 range sub-groups + ~54 card-reference-number leaf groups (Menu type throughout)."*
- This was cited into `proposals/Translink-POS-suite-restructure/FBD-100277-card-reference-file-usage.cases.yaml` **by me, earlier today**, to resolve an UNCONFIRMED marker — the case now reads *"selects the card-reference range... then the specific card reference number leaf... on-screen Menu-type group selection, not free text entry"*.

**New side:**
- New doc §12.4.1 (`8_2_1` — journey count) → §12.4.2 (`8_2_1_1`/`8_2_1_2` — Card Reference Number): *"A New Smartcard sub-screen... prompting for a 'Card Reference Number' in a **text field**, with Cancel and Confirm... shown again with an error banner when the entered reference fails validation."* Button table: `0–9 keypad | type... the reference number`; `8_2_1_2 — Reference Number Invalid | A red banner reading 'Invalid number entered'`.

**What this means:** the operator does not pick from a menu of ~50 pre-configured options — they calculate/look up a number and **type it in**, and the device validates it live (hence the error state). This is actually more consistent with there being a physical "crib sheet" (still unconfirmed — see below) that the operator reads a number off before typing it, than the menu-based story was.

**Action needed:** revert my edit to `FBD-100277-card-reference-file-usage.cases.yaml`'s Ulsterbus case — the "on-screen Menu-type group selection, not free text entry" line is now contradicted by higher-quality evidence (reverse-engineered from the real build vs. a CloudFare-configuration-intent doc) and should say free-text keypad entry with live validation instead, citing new-doc §12.4.2 screens `8_2_1_1`/`8_2_1_2`. **Not fixed yet — flagging for you to confirm before I touch the case again**, since you're mid-onboarding-run on this exact file.

---

## Finding 2 (GAP PARTIALLY RESOLVED) — Card Reference File Usage: device attribution

FBD-100277's own UNCONFIRMED marker #3 ("device attribution for the Card Validation algorithm... is not stated in this document") now has real evidence:

- New doc §25.9: *"Card reference file (DM.cardRefFile → config/br.cardref.json...). This maps WTS product field ids to a reference id and a fare. It is loaded by `WtsSmartCardFeature.cs:77, 274-281` and used by the **POS pseudo-zone check** (`POS_Features/POS.Android/Workflow/SmartCard/Validation/BRCompleteValidation.cs:396-440`)."*

This confirms **POS runs its own card-reference-file validation locally** — a real, source-cited answer, not a guess. Recommend closing that marker as: *"POS (confirmed: `BRCompleteValidation.cs`, per POS-Functional-Specification §25.9). Whether other device types (ETM) run an equivalent check independently is not addressed by either document — that part of the original question is still open."*

**New sub-gap this opens (not in FBD-100277, not previously known):** §25.10 says the furthest-alighting-point file the FBD-100277 "furthest-down fares-triangle column" algorithm would plausibly depend on (`FurthestAlightingPoints.json`) is **downloaded but never read by any code today** — the real lookup goes through `TopologyService.cs:537-580` instead. Two readings are possible: (a) `TopologyService` implements the same triangle-column logic internally using different data, and FBD-100277's description is still accurate at the behavioural level; or (b) the mechanism has changed and FBD-100277 is describing a superseded implementation. **Neither document says which — this is a genuine new open question, not something to guess past.**

---

## Finding 3 (GAP STILL OPEN) — Ulsterbus Multi-Journey crib sheet

Not resolved by the new document either. Searched the full extracted text for "crib" — no match. The new doc confirms *that* the operator must arrive at a reference number by some external means (Finding 1: it's typed, not menu-picked, which requires the operator to already know the number), but not *how* they know it. Still a real GAP, exactly as you chose to leave it earlier today ("don't know / need to check").

---

## Finding 4 (COVERAGE GAP CLOSER) — Transactions & Printing, entirely missing from sit today

Confirmed earlier in this session: `sit/Tests/POS/` has no `Transactions/` or `Printing/` folder at all — a real, complete gap, not a naming mismatch (`grep -rl "topup|annulment|basket|print.*receipt" Tests/POS` matched nothing outside the Audit file's own transaction-audit test).

The new document covers this ground exhaustively and screen-by-screen:
- **§8 Basket and Payment** — basket entry, errors/clearing, advance-ticket date, payment, cash/warrant/card tender, smartcard-removed-mid-payment.
- **§9 Card Payment** — the full bank-card flow: initialising → present/insert → authorising → approved/declined, with the exact screen IDs (`5_1_1` → `5_5_2`).
- **§11 Smartcard Top-Up and Validation** — present card, mini statement, top-up selection/payment/result, fare-product validation, faulty/hotlisted/passback cards.
- **§12 Issue Card** — full card-issue flow for every product family (see Finding 1), payment, success/error, "please remove smartcard."
- **§22 Printing** — printer service/config, ticket & receipt templates (with the actual template-selection logic and logo-selection logic), printer error screens, passenger display.

This is a directly actionable source for whoever (you, or the sit team) builds `Tests/POS/Transactions/*.robot` and `Tests/POS/Printing/*.robot` for the first time — far more detailed than anything currently in `knowledge/translink/specs/`.

**Old suite comparison:** the old TestRail suite has substantial transaction/printing coverage already (2,193 cases include this ground), but sit's *Robot automation* has none. This is a sit-automation gap, not a TestRail-suite gap — the new doc is most valuable for closing the automation gap, not for finding new TestRail cases (which the FBD docs already cover for that purpose).

**Correction while researching the work-items list below:** `system-test-ops/knowledge/flows/` already has detailed flow write-ups for most of this ground — `translink-pos-basket-payment.md`, `translink-pos-card-payment.md`, `translink-pos-issue-card-abt.md` / `-metro.md` / `-ulsterbus-nir.md`, `translink-pos-topup-validation-topup.md` / `-validation.md`, `translink-pos-printer-errors.md`, plus a full prior transcription `translink-pos-full-transcription-v4.0.3.md`. So the *documentation* for Transactions/Printing isn't starting from zero — what's actually missing is the sit **automation** (Bindings + screenflow templates + Tests) built from it. See the work-items list below for exactly what that gap is, file by file. The new document's own §28.1 source revision (`translinkpos` repo, merge of PR #168, **25 Sep 2026** — 3 days before this report) postdates the v4.0.3 flow transcription, so treat the new doc as the freshest version of this ground, not a duplicate of it.

---

## Finding 5 (CLARIFIES A KNOWN GAP ELSEWHERE) — BOS audit protocol, previously "unconfirmed"

`test-automation-sit`'s `CLAUDE.md` (a sibling repo, not `sit` or `system-test-ops`) states: *"BOS audit API is not confirmed... `BOSClient.get_audit_events` in this repo deliberately raises `NotImplementedError`... Avoid `Expect BOS Audit Event` until the API contract is confirmed."*

The new doc's §24 (Auditing and Back-Office Messages) gives a fully specified, source-cited contract:
- Three message families (Audit records `.aud`, Device status `.sta`, BOS events `.evt`), each with its own transport class and file extension in the offline queue.
- Real endpoints per record type (§24.1.3 — e.g. `POST /transaction`, `PUT /transaction`, `POST /info/deviceStatus`), against `https://device-uktest-tl-env7.albedo-gen.co.uk` (note: **-env7**, not the -env5 recorded in `test-automation-sit`'s CLAUDE.md for this same device — worth checking whether that's a different test environment or a stale note).
- Sequence-number injection mechanics (`AuditSId`/`AuditCTd` counters), JSON conventions (default-value omission, date format), retry/backoff (30s / 15min), and the exact condition that locks the POS (`NoCommunicationLimit = 7200 minutes`, matches the "5 days" comms-lock note already in the FBD docs).
- **No heartbeat is sent** — explicitly stated and explains why `test-automation-sit`'s device-status assertions rely on state-change events rather than a heartbeat.

This doesn't change anything in `system-test-ops`/`sit` directly, but it's real, actionable evidence for the separate BOS-audit-assertion decision blocked in `test-automation-sit` — worth passing along if that repo gets revisited.

---

## Device attribution check — clean

Full-text search for ETM / TVM / GV / PV / HHD / BV / "Bus Validator" / "Gate Validator" / "Platform Validator" / "Ticket Vending" across the whole new document found only:
- Correct FareProducts operator-tree entries ("ETM Ulsterbus", "ETM Metro", "TVM Metro", "TVM Ulsterbus") — these are Translink's own operator/company naming, not device-behaviour claims.
- A UI input-mode convention literally named "letters (ETM) entry mode" for alphanumeric keypad entry — a naming artifact, not a device claim.
- One code-comment citation about ETM's own, separate, unrelated behaviour ("ETM does not subscribe" — from `TransactionConfigurationUpdate.cs`, describing why a *different* device doesn't use a shared config file) — correctly scoped to ETM, not misattributed to POS.

No instance found of the new document attributing POS-specific behaviour to another device type, or vice versa. Clean.

---

## Section map — new doc vs. existing FBD docs/knowledge (heading-level only, not read in full)

| New doc section | Nearest existing coverage | Status |
|---|---|---|
| §1 Purpose/Scope, §2 Device Controls, §4 Welcome/Status Symbols | `FBD-100183-pos-hardware.md` (partial — hardware only, not the full control/symbol catalog) | **New** — no existing doc catalogs every symbol/control this exhaustively |
| §3 Customer-Facing Display | No FBD equivalent found | **New** |
| §5 Sign On | No dedicated FBD doc; sit's `Tests/POS/SignOn/test_pos_signon.robot` covers the behavioural cases already, ported from George's handover | Complements sit's existing automation with full screen/button detail sit's tests don't need but future maintainers might |
| §6/§7 Fare Look-Up (Bus/Rail) | No FBD equivalent found; sit's `Tests/POS/FLU/test_pos_flu.robot` (3 tests) is thin by comparison | **New**, and a candidate source for expanding sit's FLU coverage |
| §8/§9/§11/§12 Transactions, §22 Printing | See Finding 4 | **Coverage gap closer** |
| §10 Numerical Input | No FBD equivalent | **New** |
| §13 Operator (incl. Annulment §13.4, Refund §13.7, Totals §13.5) | Old TestRail suite: "annul" = 404 hits, "refund" = 1 hit (real existing coverage); sit's `Tests/POS/Options/` and `Supervisor/` don't cover Annulment or Refund at all | Old suite already covers this ground for TestRail; **sit automation gap** the new doc could close |
| §14 Supervisor, §15 Technician, §16 Administrator | Loosely mirrored by sit's existing `Tests/POS/Supervisor/` and `Technician/` (18 tests total) | New doc has far more screens (versions, network settings, device settings) than sit's current tests touch |
| §17 Printer Errors, §18 Power/Audio | No FBD equivalent | **New** |
| §19 Device States/System Pages | Loosely related to `FBD-100183-pos-hardware.md` | New doc's is far more complete (lock-outs, fatal error, sequence-ID sync) |
| §20 Operating Mode Model | No FBD equivalent — this is a genuinely new synthesized reference (Metro/Ulsterbus/Rail branching rules) | **New**, high value — nothing else documents this model this precisely |
| §21 Screen Canvas/Visual Language | No FBD equivalent | **New**, design-reference only |
| §23 Remote Commands | No FBD equivalent | **New** |
| §24 Auditing | See Finding 5 | **Clarifies a known gap** (in a sibling repo) |
| §25 Configuration/Reference Data | Overlaps `FBD-100277` (§25.9, see Findings 1–3), `FBD-100268-cloudfare-product-configuration.md` (§25.13 Product groups by operator), `FBD-100293-product-group-usage.md` (§25.13) | Mixed — mostly new detail, with the one direct contradiction above |
| §26 Pages Not Reachable, §27 Page Inventory, §28 Traceability | No FBD equivalent — meta/analysis sections about the doc itself | **New**, not suite-relevant directly but explains provenance |

Not cross-checked line-by-line against the old suite's full 2,193 cases or the other 8 already-pushed proposal areas (FBD-100167/100183/100250/100260/100263/100268) beyond the targeted greps above — that would need a section-by-section pass at roughly this same depth per area, which is its own follow-up task if you want it before treating any specific area as done.

---

## Recommended next steps

1. **Fix `FBD-100277-card-reference-file-usage.cases.yaml` before it's pushed** — my earlier edit (Menu-type selection) is now known-wrong per Finding 1. Needs your sign-off since you're actively driving that onboarding run.
2. **Don't mark FBD-100261 (already pushed, area 5 of 9) as fully trustworthy on the Ulsterbus card-reference mechanism** — it's pushed to TestRail already with the menu-based description. Worth a follow-up case edit once you're through onboarding, not a stop-the-line issue.
3. **Treat this new document as a primary source once uploaded**, not a peer to the FBD docs — its own §28 traceability plus the code citations throughout make it a stronger authority on *current on-device behaviour* than any FBD spec, which describe intended/configured behaviour. Where they conflict, the FBD doc is usually describing the "why"/config-time intent and the new doc the "what actually happens" — both are worth keeping, cited against each other, not one replacing the other outright.
4. **No FBD doc should be marked fully superseded.** The new document describes runtime UI/code behaviour; the FBD docs describe CloudFare-configuration intent and back-office contracts the new doc doesn't cover from the CloudFare side (e.g., how product groups get named/created). They're complementary, not duplicates.
5. **High-value follow-up, separate from onboarding:** hand §8/§9/§11/§12/§22 to whoever's building sit's POS automation next — this is the single best source available today for the Transactions/Printing gap identified earlier this session.
6. **Pass Finding 5 (BOS audit contract) to whoever owns `test-automation-sit`'s BOS-assertion decision** — not actionable in this repo, but resolves a documented blocker there.

---

## Automation work-items list — what sit actually needs

Checked against sit's real Bindings files directly (`Resources/Devices/POS/Bindings/*.robot` — read in full, not inferred from the `Tests/POS/` folder), the real `screenflow_map.jsonc`/`Templates/` for POS (`Resources/Common/ConfigSets/Translink/1/ScreenFlow/POS/`), and sit's smartcard fixtures/utilities. Each item cites exactly what's missing and where it would be built.

### 1. Keywords / Bindings

sit's five POS Bindings files today: `POSAuditBindings` (EventLog/audit-ledger checks — generic, event-type-parameterised, already covers *any* audit event by name), `POSDiagnosticsBindings` (app-install/platform-report smoke checks), `POSScreenBindings` (generic screen/label/element assertions + navigation via `POS: Go To Screen`, plus one generic stub `the operator completes a test transaction` → `POS: Complete Test Transaction`), `POSSignOnBindings` (sign-on/off, role sign-on, commissioning), `POSSmokeBindings` (installed/version/process checks). All of them are **generic** — they drive by screen name and label, not by specific transaction logic. None of them contain anything product-, payment-, or printing-specific.

- [ ] **No card-issue keywords exist.** `POSScreenBindings`/`POSSignOnBindings` have nothing for choosing a card-issue product, entering a card reference number, or completing an issue-card payment. New keywords needed (new file, e.g. `POSCardIssueBindings.robot`): something like `the operator issues a ${product} card`, `the operator enters card reference number ${ref}`, `the card issue should show ${error}`, mapped onto new-doc §12 screens `8_1_1`→`8_5_1`/`8_4_1a`/`8_4_1b`.
- [ ] **No card-payment (bank card) keywords exist.** Nothing for the §9 flow (present/insert card, authorising, approved/declined, signature). Needed: e.g. `the operator pays by bank card`, `the bank card payment should be ${outcome}` — new file or folded into a new `POSPaymentBindings.robot`.
- [ ] **No top-up/validation keywords beyond audit-ledger checks exist.** `POSAuditBindings` can assert *an* EventLog row happened, but nothing drives the §11 top-up selection/payment UI or asserts the specific validation outcomes (expired, no journeys left, hotlisted, etc. — new-doc §11.8). Needed: `POSTopUpBindings.robot`.
- [ ] **No basket keywords exist.** §8's basket-full, clear-basket-confirm, advance-ticket-date-entry have no Bindings equivalent. Fold into whichever of the above ends up owning "the shared payment summary," since §8 is the common entry point into §9/§11/§12.
- [ ] **No printing keywords exist.** `POSDiagnosticsBindings`/`POSAuditBindings` never touch the printer. Needed: `POSPrintingBindings.robot` for §22 — printer-error screens (`PrinterError`, `Out of Paper`, `Paper Jam`), receipt/template selection outcomes, passenger-display content during printing.
- [ ] **No annulment or refund keywords exist**, despite the old TestRail suite having ~404 annulment cases and sit's `Tests/POS/Options`/`Supervisor` never touching either. Needed: fold into a `POSOperatorMenuBindings.robot` (or extend `POSScreenBindings`) for new-doc §13.4 (Annulment) and §13.7 (Issue Refund).
- [ ] **`the operator completes a test transaction` (`POSScreenBindings.robot`, `POS: Complete Test Transaction`) is a single generic stub standing in for all of the above.** Worth checking what it currently does before writing any of the above — it may already be a reasonable base to specialise from rather than a blank slate.

### 2. Flows

Checked `knowledge/flows/` (system-test-ops) and sit's own POS screenflow map (`Resources/Common/ConfigSets/Translink/1/ScreenFlow/POS/screenflow_map.jsonc` + `Templates/`).

- [ ] **The documentation-level flows already exist** — `translink-pos-basket-payment.md`, `translink-pos-card-payment.md`, `translink-pos-issue-card-abt/metro/ulsterbus-nir.md`, `translink-pos-topup-validation-topup/validation.md`, `translink-pos-printer-errors.md`, `translink-pos-operator-annulment.md` all cover this ground at flow level. **Not a documentation gap** — recheck these against the new doc's §8/§9/§11/§12/§13/§22 for drift before treating them as current (the new doc is 3 days old; these flow files' own dates aren't visible from filenames alone).
- [ ] **The sit screenflow *map* (the thing Bindings actually navigate through) is missing the corresponding screens.** Checked the real `Templates/` folder for POS — it has `Payment.json` (one generic payment screen) and `PrinterError.json`, but **no** `CardIssueMenu`, `CardIssueSummary`, `CardIssueSuccess`, `CardIssueError`, `SmartcardMenu` (top-up entry, distinct from the existing `SmartcardReader.json`), `MiniStatement`, `BasketFull`/`ClearBasketConfirm`, or any of the bank-card sub-screens (`InitialisingTransaction`, `PresentCard` (bank card, distinct from smartcard), `ProcessingTransaction`, `TransactionApproved`/`Declined`). **This is the real blocker** for item 1 above — a Binding calling `POS: Go To Screen    CardIssueMenu` has nothing to navigate to until these templates exist.
- [ ] Building these templates is its own task per new-doc screen ID (e.g. `8_1_1` → `CardIssueMenu.json`), following the existing Templates' pattern (compare an existing one like `Payment.json` for the expected shape) — not something to guess at structurally without reading a working template first.

### 3. EMV config

- [ ] **The one real captured Translink POS build has `enableEmv: "false"`** (`DatasetParameters.json`, per `test-automation-sit`'s CLAUDE.md — a different repo's captured fixture, cited here only as the one real data point available). The new doc's own §28.2 config-file map names `DeviceApp/Assets/config/sales.config.json` as holding `EMVPaymentsAllowed` (sections 8–10) — that's the real lever, not `DatasetParameters.json`'s `enableEmv` (which may be a different, possibly legacy/unrelated flag — **not confirmed to be the same setting**, flag before assuming they're one and the same).
- [ ] **sit does have generic, cross-device EMV/payment-card infrastructure already** — `Resources/Devices/Common/Bindings/PaymentCardBindings.robot`, `Tests/Devices/DeviceFunctions/SelectTicketEMV.robot`, `Tests/Devices/DevicePaymentCards/TransactionsPaidByEMV.robot`, `Tests/Devices/DeviceFunctions/PaymentLabel.robot`. These are device-agnostic (`Tests/Devices/`, not `Tests/POS/`) — check whether they already exercise POS today or only other device types, before assuming POS needs EMV support built from scratch.
- [ ] **Open question, not answered by either document:** is EMV actually enabled/configured on the real Translink POS test unit today? If `sales.config.json`'s `EMVPaymentsAllowed` is off on the live device (consistent with the `enableEmv: "false"` fixture), any bank-card automation built per item 1 above needs that flag confirmed/changed first, or it should target Cash/Warrant tender only until EMV is actually turned on for testing.

### 4. Smartcard config

- [ ] **sit already has extensive matching smartcard fixtures** — checked `Resources/Common/ConfigSets/Translink/1/Smartcards/` and `SmartcardImages/` directly: pre-built XML cards for Ulsterbus Multi-Journey (`Adult-UBMJ(10jnys)-New.xml`), iLink Zones 1–4/NW, Metro Travelcard, Belfast Visitor Pass, DayLink, plus state variants — `Hotlisted/`, `Faulty/` (bad CRC), `Invalid/`, `Expired/`, `NotYetValid/`, `NoJourneys/`. These map directly onto new-doc §11.8/§11.9's validation-outcome screens (Expired, No Journeys Left, Not Valid Yet, Card Write Failed, Hotlisted) — **most of the card-state preconditions item 1's top-up/validation keywords would need already exist as fixtures**, just not wired to any POS-specific keyword yet.
- [ ] **No fixture found for "Parkeon Card Type" blank cards** (new-doc §25.9/§12 — the raw card-type-to-product-group lookup that drives which card-issue menu appears, e.g. Card Type 10 vs 12). The existing fixtures are pre-*issued* WTS product cards, not blank pre-encoded cards keyed by Parkeon Card Type. Needed for card-issue testing specifically — check with an engineer whether blank cards of specific Parkeon Card Types exist physically before assuming a fixture can be synthesised.
- [ ] **Utility layer is ready, just unused for this**: `Resources/Devices/Common/Utility/Platforms/` has `AndroidSmartcardUtility.robot` (the one relevant to POS, an Android device) alongside `LinuxSmartcardUtility.robot`/`WECSmartcardUtility.robot` for other platforms, plus a generic `SmartcardUtility.robot`. None of item 1's missing keywords need a new utility layer — they'd call into `AndroidSmartcardUtility.robot`, which already exists.

**Item count: 16** (6 under Keywords/Bindings, 3 under Flows, 3 under EMV config, 4 under Smartcard config).

---

## List A — for the SA / engineer to answer or check (old suite / old docs / knowledge notes vs. new doc)

Checked against the old suite's real section structure (2,193 cases, grouped by TestRail section; the 773-case "Delete" top-level folder was excluded as already-legacy) and the 8 pushed proposal areas / knowledge notes. Each line: source → what's missing or unconfirmed in the new doc.

1. `NIR / NIR Tickets / NIR Weekly Season Ticket` (24 cases) — new doc's Rail Ticket Types picker (§7.4.3) only shows generic placeholders ("Ticket Type 1–9"); "Weekly Season" is never named — confirm it's actually a configured ticket type on this build.
2. `NIR / NIR Tickets / NIR Monthly Season Ticket` (24 cases) — same gap as above; "Monthly Season" is never named anywhere in the new doc.
3. `NIR / NIR Smartcards / Youth Smartcards` (24 cases) — new doc's concessionary product list (Senior, Half Fare/DLA, yLink, 24+, Dependants Pass — §11.7) never uses the word "Youth" — confirm whether Youth = one of these products under a different on-screen name, or a distinct product the new doc doesn't cover at all.
4. `NIR / NIR Tickets / NIR Family & Friends Day Ticket` (16 cases) — new doc only shows `FamilyDay_POS_NIR` / `FamilyFriends_POS_NIR` / `FamilyFriendsAddCH_POS_NIR` as print-template names (§22.2.2); the actual purchase flow (which Ticket Types slot triggers it, whether selecting "Family" as Passenger Type alone is sufficient) is not described.
5. `NIR / NIR Smartcards / Dependents Pass Smartcard` (1 case) — old suite spells it "Dependents", new doc spells it "Dependants" throughout (§11.7/§11.9) — confirm same product before assuming coverage.
6. `NIR / NIR Smartcards / New Smartcards that have been used on another Device` (27 cases) and `Delete / Previously Used Smartcards that have been used on another Device` (48 cases, legacy) — new doc's §11 checks list ("passback, expiry, first use...") never explicitly names a cross-device reuse check — confirm "passback" is the same check the old suite calls "used on another device," not a same-device-only anti-passback timer.
7. `Confirmation Tests / 2.0.X` — TIBU-13513 "must be able to store an array of encryption keys and encrypt a barcode using the right key" — new doc covers barcode printing/scanning generically (12 mentions) but never once mentions encryption-key storage or selection for barcodes.
8. `Confirmation Tests / 1.3.1` — TIBU-21122 "TL POS: Transactions do not appear in Merit" — new doc never mentions "Merit" (the back-office DWH/reporting system) at all — confirm whether cross-checking the §24 audit chain against Merit ingestion is genuinely out of scope for a POS-only functional spec, or a real gap.
9. `Delete / cEMV Card Validation for Glider PV` and related Glider-PV cEMV cases (8+ cases) — new doc never mentions "cEMV" or "contactless EMV" validation at all; these old cases are filed under "Delete" (Glider PV, not POS) — confirm they're correctly excluded from POS scope and not accidentally-orphaned live POS coverage.
10. Proposal area `FBD-100276-operator-totals-api.cases.yaml` (pushed) — new doc has zero mention of "Operator Totals API" — confirm this remains entirely back-office-side with no POS-observable behaviour to cross-check.
11. Proposal area `FBD-100263-asset-tracking-reports.cases.yaml` (pushed) — new doc has zero mention of "Asset Tracking" — same confirm-out-of-scope check as #10.
12. Proposal area `FBD-100341-revenue-apportionment-reporting.cases.yaml` (pushed) — new doc has zero mention of "Revenue Apportionment" — same confirm-out-of-scope check.
13. Proposal area `FBD-100385-configuration-data-exports.cases.yaml` (pushed) — new doc has zero mention of "Configuration Data Export" — same confirm-out-of-scope check.
14. Knowledge note `FBD-100469-back-office-data-integrity-validation.md` — new doc has zero mention of "Data Integrity Validation" — same confirm-out-of-scope check.
15. Knowledge notes `FBD-100236-desfire-abt-card-format.md`, `FBD-100307-tfts-abt-data-flow-diagrams.md`, `FBD-100658-abt-audit-specification.md`, `FBD-100389-abt-scenarios.md`, `FBD-100698-abt-cloudfare-topology-usage.md` — new doc's own §26.3 states ABT (Account-Based Ticketing) is a "Feature Not Loaded" on this build — confirm whether existing/old-suite ABT-related POS cases are still meant to run (different build/config?) or should be parked given the new doc's explicit statement that ABT isn't active.
16. `Metro / Metro Waybills` (4 cases) — new doc's §24.10 "Waybill and end-of-shift records" exists but doesn't call out Metro-mode-specific waybill content distinctly from NIR/Ulsterbus — confirm the Metro-specific fields the old cases check are actually covered, not just a generic mention.
17. `Metro / Metro Error Handling & Performance / TMS Settings & Configuration` (9 cases) — new doc's §25.1–25.5 describe the happy-path manifest/artifact download only; confirm the old suite's error-handling scenarios (malformed/partial config download, rollback) have a real counterpart rather than being silently un-described.
18. `Confirmation Tests / 2.0.X` — TIBU-19374 "Cross Border (XB) Tickets not displaying the correct Price" — new doc mentions "Cross Border" exactly once (one Senior XB Single example, §11.7.2); confirm the broader Cross Border pricing rule this defect implies (across other passenger/ticket types) is actually covered, not just one worked example.
19. `Confirmation Tests / 1.2.1` — TIBU-20868 "Metro Daylink Adult - Card Ref Amount used in Days Left Field" and sibling card-reference-number display defects — directly relevant to the still-open contradiction in this report's Finding 1/3 (menu-pick vs. keypad-entry for card reference numbers) — flag to the SA together with that finding, since these are real historical defects in exactly that area, not just a documentation nuance.

## List B — for the sit automation team (automation-specific, distinct from List A)

1. No sit Binding, fixture, or screenflow template exists for "Season" ticket types (Weekly/Monthly) at all — don't build until List A #1/#2 is answered by an SA.
2. No sit smartcard fixture or keyword exists for a "Youth" product — blocked on List A #3.
3. No sit screenflow template exists for a Family & Friends ticket **purchase** flow (`Templates/` has no `FamilyDay`/`FamilyFriends` screen entries — only the print-template names appear in the new doc, not a UI screen) — only worth building if List A #4 confirms it's a real, distinct on-device flow.
4. No sit keyword exists to assert cross-device/passback smartcard-reuse detection (the old suite's "used on another device" scenarios, 27+48 cases across NIR/Delete) — needs the same new screenflow templates already flagged in the main work-items list, plus a dedicated assertion keyword once List A #6 is resolved.
5. No sit coverage at all — Binding, fixture, or test-support-service capability — for barcode encryption-key selection/storage (TIBU-13513); per List A #7, the new doc doesn't describe the mechanism either, so there's nothing to automate against yet.
6. No sit keyword or fixture exists for Cross Border (XB) ticket pricing beyond what a generic fare-lookup test would already exercise — don't build a dedicated XB assertion until List A #18 is answered, to avoid encoding just the one worked example as if it were the general rule.
7. No sit template or Binding exists for Metro-specific Waybill content, distinct from the generic audit-event checks `POSAuditBindings` already supports by event type — only build once List A #16 confirms there's Metro-specific detail to assert on.
8. No sit way to simulate a malformed/partial TMS config download (List A #17) — this would need a new Test Support Service capability to inject a broken config artifact, not just a new Robot keyword; flag as infrastructure work, not test-authoring work.
9. Don't build a card-reference-number entry keyword (already flagged as missing in the main work-items list, item 1) against **either** source (menu-pick or keypad-entry) until the Finding 1/3 contradiction and List A #19's historical defects are resolved with an SA — building it against the wrong UI model would encode the bug pattern TIBU-20868 already found once.

**List A: 19 items. List B: 9 items.**
