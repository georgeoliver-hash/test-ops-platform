# TVM card/credential-variant sweep — changelog

**Mandate.** A narrow follow-up to today's earlier `tvm-consolidation-completeness.changelog.md`
pass, modeled on a real miss just found in the PV suite: 13 old cases testing card **schemes**
(Visa Debit/Credit, Mastercard Debit/Credit, Maestro) — mechanically identical, only the card
sample differing — were folded into one new case that named only "Visa, Mastercard, mobile
wallet" generically, silently dropping the Debit/Credit split and Maestro entirely. George's
directive: card/EMV variant testing on any device is "gospel" — every scheme/card-type variant
proven real by the old suite must stay traceable, as its own case or a named `Data variations:`
line. Confirmed at the top of this session: the TVM has **no smartcard reader and no barcode
scanner** — the applicable mechanism here is the **Ingenico EMV payment terminal**.

## Method

1. Pulled all 10 old TVM suites fresh in full (`5602`, `6160`, `22270`, `22272`, `22273`, `22274`,
   `22275`, `22276`, `22278`, `22279` — 3,368 cases total, matching the count in today's earlier
   consolidation-completeness pass) via `TestRailClient.get_cases`.
2. Pulled the live suite (`30284`) fresh in full (213 cases via CLI export; 188 active after this
   pass) and isolated the `Payments - EMV & Contactless` section (887780, 16 cases) plus
   `Payments - Cash` (887777) for the payment/card-mechanism family.
3. Keyword-swept old-suite titles for `visa|mastercard|amex|american express|diners|maestro`
   (146 hits) and separately for `magnetic stripe` (17 hits) and `unionpay|jcb|fitbit` (0 hits —
   confirms no scheme families beyond the ones already known).
4. Cross-checked every scheme/mechanism family the old suite proves against the live suite's
   `Data variations:` lines (not just case titles), reading full case bodies for the ones where the
   live suite's enumeration looked incomplete.
5. Grounded the one genuine gap against `TFTS Requirements Matrix.xlsx` (REQ-0340.0, REQ-1515.0 —
   both Signed-Off/Deployed, "Applies to: TVM (All)").

## What was checked and found clean

- **Maestro** — searched all 10 old TVM suites; the only "Maestro" hit (`C1831227`, suite 6160) is
  incidental text inside a defect description (JIRA 252195, contactless pinpad-cancel bug), not a
  scheme-specific test case. Maestro card-scheme cases (`C1694410`, `C2623695`, `C3498109`) exist
  only in the **HHD** suites (5446, 13958) searched for comparison — **not a TVM finding**. Unlike
  the PV suite, Maestro was never tested as a distinct TVM scheme in any old suite, so there is
  nothing to restore.
- **Chip & PIN — Visa/Mastercard credit+debit** (`C4103657`) — already correctly enumerates
  "Visa credit/debit, Mastercard credit/debit, non-GBP issued card" as Data variations (fixed in an
  earlier pass today). Not the PV anti-pattern — left as-is.
- **Amex/Diners Chip & PIN** (`C4103659`) — already enumerates "Amex credit/debit, Diners Club".
  Clean.
- **Contactless at/below limit** (`C4103661`) — already enumerates "Visa/Mastercard credit/debit;
  legacy £30.00 limit". Clean.
- **Mobile wallet** (`C4103663`) — already enumerates "Apple/Google/Samsung Pay;
  Mastercard/Visa credit/debit". Clean.
- **UnionPay / JCB / Fitbit Pay** — zero hits in any old TVM suite; not a real member of this
  suite's scheme list, nothing to add.

## Genuine gaps found and fixed

### 1. Magnetic Stripe — a whole payment mechanism missing entirely (new: C4104129, C4104130)
The live suite's EMV & Contactless section only tests **Chip & PIN** and **Contactless** — zero
mentions of "magnetic stripe"/"stripe"/"swipe" anywhere in the 213-case suite export. But the old
base suite (6160) carries **15 Magnetic Stripe cases**: 7 "Ticket Format N … Magnetic Stripe" print
checks, a dedicated cancel/timeout/print-failure trio (`C1831417/418/419`, section 348760, titled
"…during a Magnetic Stripe transaction" — i.e. tested as its own mechanism, not folded into the EMV
generic cases), and 7 scheme-specific outcome cases (`C1831413/414` Mastercard Credit/Debit,
`C1831415/416` Visa Credit/Debit, `C1831437/438` Amex Credit/Debit, `C1831554` Diners Club).

**Grounded as real, not incidental:** `TFTS Requirements Matrix.xlsx` — **REQ-0340.0** ("The TVM
shall be capable of handling card transactions … using Chip & PIN, Magnetic Stripe, and Contactless
payment media technologies", Test/Accepted-by-customer, Applies to TVM (All)) and **REQ-1515.0**
("The TVM payment terminal shall support contact, contactless and magnetic stripe cards with an
integrated Payment Card Device", Test/Deployed, TVM (All)) — both explicitly name Magnetic Stripe as
a mandated TVM payment technology alongside Chip & PIN and Contactless, the same REQ family already
used to resolve gap-register Q30 for the rest of this section. This is not capability-blocked like
the smartcard/barcode findings — it is a confirmed, signed-off, deployed mechanism with zero live
coverage.

**The scheme split is the genuinely distinct part, not just "another Chip & PIN case":** the old
suite proves Magnetic Stripe behaves **oppositely** to Chip & PIN for two schemes — Visa/Mastercard
credit+debit are **approved** by swipe (`C1831413-416`), but American Express and Diners Club are
**declined** by swipe (`C1831437/438/1554`) even though the same schemes are explicitly accepted via
Chip & PIN (`C4103659`). This is exactly the kind of channel-dependent scheme distinction the PV
audit's directive is about — a card type behaving differently depending on the acceptance mechanism,
not a cosmetic variant.

**Fixed:** two new cases under `Payments - EMV & Contactless` (887780):
- `C4104129` "Magnetic Stripe — a valid card completes payment and prints the ticket" — Data
  variations: Visa credit/debit, Mastercard credit/debit.
- `C4104130` "Magnetic Stripe — American Express and Diners cards are declined" — Data variations:
  Amex credit/debit, Diners Club. Cross-referenced against `C4103659` in the expected-result text so
  the contrast with Chip & PIN acceptance isn't lost.

The mechanism-agnostic behaviours (cancel at pinpad, payment timeout, print failure) were **not**
given new cases — per the "same partition, no new test" rubric they're folded as an added `Data
variations:` entry on the existing generic EMV cases (below), since the old suite's own
cancel/timeout/print-failure assertions for Magnetic Stripe are worded identically to the Chip & PIN/
Contactless ones, just scoped to a different entry method.

### 2. Existing cases missing scheme/mechanism enumeration they should carry (5 Data-variation additions)
- **`C4103658`** (Chip & PIN, no PIN entered) — carried no Data variations at all. Old suite names
  the specific schemes tested for this exact no-PIN path: `C1831399` Visa Debit, `C1831402`
  Mastercard Debit. **Fixed:** added `Data variations: Visa Debit, Mastercard Debit`.
- **`C4103662`** (Contactless above the limit falls back to Chip & PIN) — carried no Data variations,
  unlike its sibling `C4103661` (at/below limit) which already lists Visa/Mastercard credit/debit.
  Old suite proves the same scheme split for the above-limit fallback (`C1831357`/`C3546404` Visa,
  `C1831394`/`C1831396` Mastercard credit/debit). **Fixed:** added `Data variations: Visa
  credit/debit, Mastercard credit/debit`, matching C4103661's pattern.
- **`C4103665`** (cancel at pinpad), **`C4103666`** (payment timeout), **`C4103667`** (print failure
  voids payment) — each already covers the behaviour generically but named no entry-method
  variations. Old suite tests cancel/timeout/print-failure explicitly for Magnetic Stripe
  (`C1831417/418/419`) as well as EMV (`C1831362`/`C3546374` cancel, `C1831418`/`C3546396` timeout,
  `C1831351/1363`/`C3546375` print-failure). **Fixed:** added `Data variations: Chip & PIN,
  Contactless, Magnetic Stripe` to all three, so the newly-restored Magnetic Stripe mechanism isn't
  silently unlinked from its own cancel/timeout/print-failure coverage.

## Push

```
$env:TESTRAIL_WRITE_SUITE_ID="30284"
python -m system_test_ops push --file proposals/coherence-audit/fixes/tvm-card-variant-sweep.cases.yaml --commit
python tools/apply_rewrite.py proposals/coherence-audit/fixes/tvm-card-variant-sweep.rewrite.json --commit
```
Push: 1 section (`Payments - EMV & Contactless`, existing id 887780), 2 new cases created
(`C4104129`, `C4104130`). Rewrite: 5 existing cases updated (Refs/Data-variations only, no
behaviour/step change) — `updated: 5  removed(ZZ): 0  fare-reframed: 0  skipped: 0  missing: 0`.

## Audit

```
python -m system_test_ops audit --suite 30284
```
**CLEAN** — 188 active cases (186 + 2 new), 0 blocking findings, 30 advisory `title-too-long`
(unchanged count — the two new titles are within the advisory length norm already used across the
suite).

## Totals

| Family | New cases | Data-variation additions | Investigated, found clean (no change) |
|---|---:|---:|---:|
| Maestro | 0 | 0 | confirmed HHD-only, not a TVM finding |
| Chip & PIN Visa/Mastercard/Amex/Diners | 0 | 0 | already correctly enumerated |
| Contactless at/below limit, mobile wallet | 0 | 0 | already correctly enumerated |
| UnionPay/JCB/Fitbit Pay | 0 | 0 | zero evidence in any old suite |
| **Magnetic Stripe mechanism** | **2 (C4104129, C4104130)** | 0 | — |
| No-PIN / contactless-above-limit / cancel / timeout / print-failure | 0 | **5** (C4103658, C4103662, C4103665, C4103666, C4103667) | — |
| **Total** | **2 new cases** | **5 Data-variation additions** | 4 families checked and confirmed clean |

**Not touched:** every old TVM suite (5602, 6160, 22270, 22272–22276, 22278, 22279) — read-only
throughout. No gap-register question was needed this pass — the one genuine finding (Magnetic
Stripe) was fully grounded from the old suite plus a signed-off/deployed REQ pair, no escalation
required.
