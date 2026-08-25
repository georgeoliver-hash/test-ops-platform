# TVM consolidation-COMPLETENESS audit — changelog

**Question asked:** did consolidating 9 old TVM suites (5602, 6160, 22270, 22272, 22273, 22274,
22275, 22276, 22278, 22279 — Kiosk/Astreo × NIR-Rail/Ulsterbus/Metro/Glider) down to suite 30284
silently drop a genuinely distinct scenario, or did it only remove true model×mode triplication?

**Method.** Pulled every case (full body) from all 9 old suites (3,368 cases total) and the live
suite (201 cases, 174 active before this pass) via `TestRailClient.get_cases`. Cross-tabulated by
family (ticket/product catalogue, payment methods, EMV/contactless decline reasons, smartcard/
barcode, hardware/procedural) — for each, listed every genuinely distinct member (product, payment
method, decline reason, hardware state) proven real by an old-suite case, and checked whether the
live suite names it anywhere (own case or an explicit Data variations line). Model/mode restatements
of the *same* member (Kiosk vs Astreo vs Rail vs Bus vs Metro vs Ulsterbus vs Glider retelling one
scenario) were treated as correctly-removed triplication, not gaps.

**Suite:** `**NEW** TVM Test Suite` (30284), project 42. **Pushed to TestRail:**
```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python -m system_test_ops push --file proposals/coherence-audit/fixes/tvm-consolidation-completeness.cases.yaml --commit
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-consolidation-completeness.rewrite.json --commit
```
Push: 12 new cases created (C4104113–C4104124), 1 new section (`Note Recycler & Change (Kiosk
only)`, id 887843). Rewrite: 4 existing cases updated (Refs/Data-variations only, no behaviour
change except C4103691's factual correction below). Post-push `audit --suite 30284`: **CLEAN** — 186
active cases, 0 blocking findings, 30 advisory `title-too-long` (pre-existing pattern across the
suite, unrelated to this change).

---

## Family-by-family accounting

### 1. Ticket / product catalogue — no genuine gaps found
Basket, Ticket Numbering, Adult/Child products, Cross-Border, Family & Friends, Advance/3-Day, and
Glider-as-a-mode all check out as **correctly consolidated** (Kiosk×Astreo×mode triplication
removed, every member still named via a case or a Data-variations line — e.g. C4103681/682,
C4103699–701, C4103683/684, C4103694/698, C4103704–716, C4103717–721).

Two clusters an initial pass flagged as "missing" (Half-Fare/yLink/24+ ticket-layout format,
`Kiosk-Rail C3544566/3544567/3544764`; yLink as a sold ticket, `R2-MAN-FNC-TVM C1831795/1850173/
1898228`, `Kiosk-Bus C2113860/3545050`) turned out, on reading the old case bodies directly, to
**require presenting a physical smartcard to a reader** ("Insert the yLink card into the card
reader", "the user has presented a valid yLink smartcard to the reader") to identify the concession
before the discounted ticket is offered. That is exactly the capability George confirmed **absent**
on 2026-07-21 (`tvm.changelog.md` §2: "the TVM has no smartcard reader/writer at all") — the same
finding that already condemned C4103605–609 (concession-by-smartcard: yLink/24+/half-fare/free-
concession/funded-disability) and C4103610 (Staff Pass). So these are **not completeness gaps** —
they are the same confirmed-absent capability, correctly reflected by the existing condemnations.
No case added for this cluster.

Also checked: old-suite Staff-Pass cases contradict each other internally (Kiosk-Rail
`C3544681–3544684` show a presented Staff smartcard being *accepted* into the normal fare flow;
Kiosk-Bus/Astreo-Glider `C3545347/3545348/C3546594` show the *same* action producing a "Smart Card
cannot be Recognised" rejection screen) — noted here for the record, but moot either way since Staff-
by-smartcard is capability-blocked regardless of which old behaviour was "correct".

### 2. Payment methods / EMV & contactless decline reasons — 5 genuine gaps, 2 Data-variation additions, 1 not-a-gap correction
Coin/note/foreign-currency validation, escrow limits, Chip&PIN/contactless boundary values, AMEX/
Diners acceptance, and expired/blocked-card rejection are **fully covered** (C4103634–47, C4103659–
68), consistent with `tvm.findings.md`/`tvm-deep-audit.changelog.md`'s existing findings on this
area (unaffected, not re-litigated here).

**Genuinely missing (5, new cases added):**
- **Kiosk-vs-Astreo BNR divergence** — the live suite's C4103650/51 assert the BNR becomes
  **non-functional** when a note is left in the exit beak, sourced from the **Astreo**-suite cases
  (`Astreo-Cash-EMV C3546354–3546356`, titled "BNR is **Non Functional**..."). The base/Kiosk-era
  suite has the *opposite* outcome for the identical trigger (`R2-MAN-FNC-TVM C1831504–1831506`,
  titled "BNR **is Functional**..."). This is exactly the #1 Kiosk-vs-Astreo divergence
  `old-suite-audit.md` flagged to prove, and only the Astreo half survived consolidation. **Fixed:**
  added `C4104113`/`C4104114` under a new `Note Recycler & Change (Kiosk only)` section (887843),
  mirroring C4103650/51 with the Kiosk "remains functional" outcome.
- **Card physically removed mid-transaction** (`Kiosk-Rail C3544878/3544882`, mirrored in
  `Astreo-Cash-EMV C3546372/3546376` — same outcome both models, correctly one case) — distinct from
  "declined" (C4103664) or "cancel at pinpad" (a step within it); the card leaves the reader before
  authorisation resolves. **Fixed:** added `C4104115`, Data variations Chip & PIN / contactless.
- **Coin/note jam clearing during payment and change-issuing** (`R2-MAN-FNC-TVM C1831511–1831516`) —
  a recoverable jam-clear flow, distinct from the hard hardware-failure case already folded into
  Degraded Service (C4103780). **Fixed:** added `C4104116` (successful clear) and `C4104117`
  (unsuccessful clear), each with Data variations for coin/payment, note/payment, coin/change.
- **Unsupported card issuer/scheme** (`R2-MAN-FNC-TVM C1831364`, mirrored `Kiosk-Rail`/
  `Astreo-Cash-EMV`) — never cited on the declined-card case. **Fixed:** added as a Data variation to
  `C4103664` (Refs updated to cite C1831364).
- **Non-GBP-issued card acceptance** (`R2-MAN-FNC-TVM C2144092`) — a positive-path gap, low risk.
  **Fixed:** added as a Data variation to `C4103657` (Refs updated).

**Investigated, found NOT a gap:** "Hotlisted Card - Cannot use on TVM" (`AA-TVM-Acceptance-V03
C1705901`, mirrored across 5 old suites) reads, in the old case body, as presenting a **smartcard**
to the TVM's smartcard reader after Smartrack hotlisting — the same confirmed-absent smartcard-reader
capability as §1 above, not an EMV/payment-card decline reason. Not added (would be restoring a
capability-blocked scenario under a misleading "payment decline" label).

**Left as an open question, not fabricated:** "EMV Offline Payment — Chip & PIN / Contactless"
(`R2-MAN-FNC-TVM C2041439/C2041440`) and "Chip & Pin - Purchase with No Network Availability"
(`C1831600`) describe the Ingenico/ChipDNA terminal completing a payment in a "pre-authorised" state
while the TVM is offline. Given this session's Q33 (TVM has a real WAN↔SIM failover), it's unclear
whether this is a distinct terminal capability or already subsumed by comms failover. Logged as
**gap-register Q59** rather than guessed into a case.

### 3. Smartcard & barcode handling — 1 genuine gap (barcode), rest confirmed not-a-gap
The entire Smartcard & ABT area (issue, top-up, mini-statement, concession-by-card, invalid/passback,
screensaver-wake) is **correctly capability-blocked**, not a completeness defect: George's 2026-07-21
live confirmation ("no smartcard reader/writer at all") already condemned all 27 cases + 3 Data-
variation strips (`tvm.changelog.md` §2). Retired (`ZZ_DELETE_REVIEW`) cases are excluded from "still
covered" counting in this audit — they are not active coverage.

Barcode redemption (booking-reference/Collect-Ticket-Code entry, online/offline state machine,
ceiling limit, legacy stage) is **fully covered and correctly consolidated**, matching FBD-100483
exactly (unchanged from the original coherence audit's verdict).

**Genuine gap found:** the live `C4103691` asserted, in its Expected-result parenthetical, that "TVM
prints single-use only" — but 13 old-suite `Kiosk-Rail` cases (`C3544955–C3544968`, "… — Rail —
Multi use Barcode", covering Adult/Child Single, Day Return, Day Tracker, 1/3-off Return, 3-Day
Select, Concession, Half-Fare Concession, 24+, yLink) show the TVM **issuing** multi-use-type
barcodes for several rail products. Cross-checked against this register's own **Q10** (resolved
2026-07-22, GV audit session): the FBD-100167 device table's `*` footnote — "POS and TVM will
validate Single Use barcodes but not multiple use" — applies to the **Validate** column, not the
**Print** column; TVM's tick is in **Print**, unrestricted. So the blanket "prints single-use only"
claim in C4103691 was too broad — a wording defect this audit surfaces, not a fabricated capability.
**Fixed:** corrected `C4103691`'s Expected result (removed the false blanket claim, added a Data
variations line naming which rail products print a multi-use-type barcode, with the accurate
restriction — the TVM cannot **validate** a multi-use barcode presented back to it) and updated Refs
to cite the old-suite evidence + Q10.

### 4. Hardware / procedural (lower priority — narrow miss-check only)
Cash mechanisms/commissioning were already checked today for spec-grounding (`tvm-deep-audit`
Q34 — ~52 cases, resolved via `TFTS Requirements Matrix.xlsx` REQ-ids); this pass only checked for
**missing variants**, not re-grounding. **7 genuine gaps found, all fixed as new cases:**

- **Security/tamper cluster** — hopper door opened without authorisation, 3 failed EMS login
  attempts, TVM door opened after failed logins, TVM door opened without any login attempt (`R2-MAN-
  FNC-TVM C1831725/1831215/1831216/1831218`, mirrored identically in both `Kiosk-EMS-TMS` and
  `Astreo-EMS-TMS` — genuinely shared, not model-specific). **Fixed:** `C4104118`, one case with the
  4 triggers as a Data-variations list (same consequence — a burglary event — across all 4; matches
  the standard's "don't fragment into a case per trigger" guidance).
- **EMS Battery Saver Mode** during a mains power failure (`AA-TVM-Acceptance-V03 C2691863`).
  **Fixed:** `C4104119`.
- **Panic-event suppression on coin/note vault swap** after a power cut (`R2-MAN-FNC-TVM C2038477`).
  **Fixed:** `C4104120`.
- **EMS-exit "Back to Sales" with vs without a General Reboot** (`Kiosk-EMS-TMS C4041250/4041251`,
  mirrored `Astreo-EMS-TMS C4041252/4041253`). **Fixed:** `C4104121`, Data variations for both exit
  paths.
- **Alarmboard "Request Version"** (`R2-MAN-FNC-TVM C1857325`) — the live alarmboard cluster
  (siren/LED/temp/UPS/door/speaker/fan) had no firmware-version-request case. **Fixed:** `C4104122`.
- **Corethree ticket-collection server address configured via TMS** (`Kiosk-Rail C3544768`, mirrored
  `Kiosk-Bus`/`Astreo-Glider`). **Fixed:** `C4104123`.
- **Topology rejection for another device type** ("Send Topology to Impertinent Devices",
  `AA-TVM-Acceptance-V03 C1785735`, mirrored `R2-MAN-FNC-TVM C1831898`/`Kiosk-EMS-TMS C3544461`).
  **Fixed:** `C4104124`.

**Investigated, found NOT a gap (capability-blocked, same as §1/§3):** smartcard-reader antenna
coverage (Front/Coinbox/Unstacker, `C1857410-412`) and smartcard-status-after-USB-disconnect
(`C2049100`) both depend on the confirmed-absent smartcard reader — not added.

**Left as an open question, not fabricated:** whether the Astreo TVM has an alarmboard at all (the
live cluster and this session's new "Request Version" case are both worded Kiosk-only, matching the
old suite's own Kiosk-only scoping convention, but the base R2 suite that originated the case wasn't
itself model-specific). Logged as **gap-register Q60**.

**IML5 printer** — the live suite only tests TL80 alignment (`C4103775`); the old suite's combined
"Printer Test - IML5 & TL80" (`C1865202`) tests both models via the identical maintenance-menu
mechanism. **Fixed:** added IML5 as a Data variation on `C4103775` (retitled slightly from "TL80
Printer —" to "Printer —" since it's no longer TL80-only, matching the DV pattern used elsewhere in
the suite, e.g. C4103657 isn't titled "Chip & PIN (Visa)").

---

## Totals

| Family | New cases | Data-variation additions | Corrections | Genuine gaps found but left as gap-register Q (not fabricated) |
|---|---:|---:|---:|---:|
| Ticket/product catalogue | 0 | 0 | 0 | 0 (all flagged candidates were capability-blocked, not gaps) |
| Payment / EMV decline reasons | 5 (C4104113–4104117) | 2 (C4103664, C4103657) | 0 | 1 (Q59, EMV offline/pre-auth) |
| Smartcard & barcode | 0 | 0 | 1 (C4103691) | 0 |
| Hardware / procedural | 6 (C4104118–4104124, minus one already counted above) | 1 (C4103775) | 0 | 1 (Q60, Astreo alarmboard) |
| **Total** | **12 new cases** | **3 Data-variation additions** | **1 correction** | **2 new gap-register questions (Q59, Q60)** |

**Push commands** (both dry-run-verified before commit, counts matched):
```
python -m system_test_ops push --file proposals/coherence-audit/fixes/tvm-consolidation-completeness.cases.yaml --commit
  -> 6 sections, 12 cases created (C4104113-C4104124), incl. new section "Note Recycler & Change (Kiosk only)" (887843)
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-consolidation-completeness.rewrite.json --commit
  -> updated: 4  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0
```

**Audit:** `python -m system_test_ops audit --suite 30284` — **CLEAN**, 186 active cases (174 + 12
new), 0 blocking findings, 30 advisory `title-too-long` (up from 24 — the new cases contribute a few
long titles, all reviewed and intentional per the standard's title-length being advisory-only).

**Not touched:** every old TVM suite (5602, 6160, 22270, 22272–22276, 22278, 22279) — read-only
throughout, nothing added/edited/deleted in any of them. The 27 previously condemned smartcard/ABT
cases and every other prior fix (barcode wording, Scottish banknote, the three deep-audit citation
passes) are unchanged by this pass.

**Remaining open for George:** gap-register **Q59** (EMV offline/pre-authorised payment — distinct
capability or already covered by comms failover?) and **Q60** (does the Astreo TVM have an
alarmboard?). Both logged, neither blocking — no case was fabricated to close either.
