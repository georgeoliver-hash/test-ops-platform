# NJT_FRFRP_FS002 — Fare Structure: Transactions (distilled)

**Source:** `NJT_FRFRP_FS002 - Fare Register Functional Specification.pdf`, Section 4 "Fare
Structure" → 4.1 "Transactions" (4.1.1 Class, 4.1.2 Transaction Type, 4.1.3 Class/Transaction
Combinations, 4.1.4 Ticket Selection Display). Distilled from lines 892–1424 of the extracted text
(`njt-requirements/_text/...pdf.txt`). Raw spec held locally, not committed. This note covers only
this line range — other sections of FS002 are distilled elsewhere.

## Context (§4, intro — p.~14, page marker not captured in this range)
- Routes in CloudFare are configured similarly to the legacy Waycon system: a route = the set of
  zones making up that route, with a reference fare set for each origin/destination zone pairing.
- Fare rules are driven by lookup tables of reference fares.
- **GAP** — exact page number for this intro paragraph is not confirmed: the extracted range starts
  mid-page, before the first "Page 15" footer marker appears (line 962), so this content likely sits
  on p.14 but that marker itself isn't present in the read range. Cite as "p.14 (unconfirmed)" until
  checked against the PDF directly.

## 4.1.1 Class (p.15)
"The transaction is made up of a class and a transaction type." There are **seven** rider classes
(a legacy "10T Book sale" class is explicitly **no longer supported**):

| Class | Spotter Display |
|---|---|
| Adult | AD |
| Child | CH |
| Senior | SR |
| Student | STU |
| Employee | EM |
| Family | FM |
| Foreign | FR |

Rider classes map to Fare Register softkeys via CloudFare menu groups.

## 4.1.2 Transaction Type (p.16–21)
A transaction type defines the interchange in which the customer offers payment (Cash, pre-paid
fare media — Transit Pass / ticket / transfer / continuing-trip ticket / other official paper media
— or a MyTix mobile phone payment) and receives a paper (or mobile) receipt. Fare media is called an
**"Issue"** when first issued and **"Receive"/"RX"** when used for payment on a later leg.

Full enumerated list (ID# — Name — Payment/Receipt — Comment — Selection Display / Ticket Details
Display / Spotter Display):

| ID | Transaction | Payment/Receipt | Comment | Selection Display | Ticket Details Display | Spotter Display |
|---|---|---|---|---|---|---|
| 0 | Family Fare | Fare Media Receipt | Registers free riders under "Family Fare" privilege, displaying Employee Passes, or for special promotions as designated | — | CTR1 | CTR1 |
| 1 | Cash | Cash Receipt | Bills and coins | Cash | Cash | CASH |
| 2 | Monthly Pass | Fare Media Receipt | Override function available if pass not valid for all zones the passenger wishes to travel | Monthly Pass | Mpass | PASS |
| 3 | Ticket | Fare Media Receipt | Any pre-paid ticket not issued by a FR and not a 10-trip ticket | X-Ticket | X-Ticket | XTKT |
| 4 | 10 Trip Ticket Rx | Fare Media Receipt | From a book of 10 trip tickets | X-10 Trip | X-10T | X10T |
| 5 | Transfer Rx | Fare Media Receipt | Paper receipt providing free travel within one zone (when authorised) | X-Transfer | X-Tfr | XTFR |
| 6a/6b | Transfer Issue | Cash Receipt + Fare Media | Fare media issued providing free travel within one zone on connecting bus (when authorised); fare increased by applicable transfer fare rate; an Override transfer can be issued after the initial transaction is completed | Transfer / O/R Transfer | Transfer / O/R TFR | TFR / TFR |
| 7 | Cash Round Trip Issue | Cash Receipt + Fare Media | Fare media is for the passenger's return trip | Cash Round Trip | CRT | RT |
| 8 | Override | Cash Receipt | Allows a passenger to travel further than valid for their original transaction | Override | Over | OR |
| 9 | Rail Pass | Fare Media Receipt | Override function available if pass not valid for all zones (same functionality as Monthly Pass) | Rail Pass | Rpass | RAIL |
| 10 | Cash Round Trip Rx | Fare Media Receipt | Fare media received for the passenger's return trip | X-Cash Round Trip | X-CRT | XCRT |
| 11 | Special | Cash Receipt | Allows an operator to adjust the fare for a special trip | Special | Special | SPEC |
| 12 | Cont. Trip Rx | Fare Media Receipt | Receipt given to bus operator to continue a trip | X-CTT | X-CTT | XCT |
| 13a/13b/13c | Cont Trip Issue | Cash or Fare Media Receipt + Fare Media | Allows the passenger to continue the trip on another route/bus; only available on limited routes; issuance only in conjunction with payment by cash, ticket, or 10-trip ticket | CTT Cash / CTT Ticket / CTT 10 trip | CTT CSH / CTT TKT / CTT 10T | CT / CT / CT |
| 14a/14b | No Charge Transfer ("2nd Transfer" in old system) | Fare Media Receipt | As TFR except the transfer is free; only works with a Ticket so fare is always zero | NC-Transfer / — | NC-Tfr OR NCTFR | TRF2 / TRF |
| 15 | Not used | — | — | — | — | — |
| 16 | MyTix Monthly Pass | Mobile Receipt | — | MyTix Monthly Pass | MT Mpass | *PASS |
| 17 | MyTix Ticket | Mobile Receipt | — | MyTix X-Ticket | MT X-TKT | *XTKT |
| 18 | MyTix Rail Pass | Mobile Receipt | — | MyTix Rail Pass | MT Rpass | *RAIL |
| 19 | MyTix Transfer Rx | Mobile Receipt | — | MyTix X-Transfer | MT X-Tfr | *XTRF |
| 20 | MyTix 10 Trip Ticket Rx | Mobile Receipt | — | MyTix X-10 Trip | MT X-10T | *X10T |
| 21 | MyTix Special | Mobile Receipt | — | MyTix Special | MT Spec | *SPEC |
| 22 | MyTix Cont. Trip Rx | Mobile Receipt | — | MyTix X-CTT | MT X-CTT | *XCT |
| 23a/23b | MyTix Cont. Trip Issue | Mobile Receipt + Fare Media | Issuance only in conjunction with payment by MyTix ticket or MyTix 10-trip ticket | MyTix CTT Ticket / MyTix CTT 10 Trip | MTCTTTKT / MTCTT10T | *CT / *CT |
| 24 | Non Payment | No receipt | A pass transaction used to record instances of passengers who refuse to pay for travel | Non Payment | NoPay | \<none\> |

(pp.16–21, table spans "Page 16" through "Page 21" footer markers)

## 4.1.3 Class / Transaction Combinations (p.22–23)
"The class and transaction types are only allowed in certain combinations." The spec presents a
checkmark matrix: 25 transaction-type rows (IDs 0–24, ID 15 unused) × 7 class columns (1 Adult,
2 Child, 3 Senior, 4 Student, 5 Family, 6 Empl., 7 Foreign).

The table is also used to **auto-select** the transaction type when a class with only one valid
transaction type is chosen by the operator (p.23).

**GAP — exact per-class checkmark columns cannot be reliably reconstructed from the extracted text.**
The PDF-to-text extraction collapsed the checkmark grid into a run-on line and lost the original
column (x-position) alignment that distinguishes which of the 7 class columns each ✔ belongs to —
unlike the surrounding prose, spacing in this specific table is not a reliable proxy for column
position. What IS extractable with confidence:
- Row 15 ("not used") has **zero** valid class combinations — this transaction type is fully retired.
- Every other row (0, 1–14, 16–24) has **at least one** valid class, i.e. no other transaction type
  is universally disallowed.
- Rows 3 (Ticket) and 5 (Transfer Rx) appear to have the broadest class applicability (most
  checkmarks in the row); rows 2 (Monthly Pass), 4 (10 Trip Ticket Rx), 9 (Rail Pass), 16 (MyTix
  Monthly Pass), 18 (MyTix Rail Pass), 23 (MyTix Cont. Trip Issue) appear narrowest (fewest
  checkmarks) — but the **specific class(es)** each of these maps to is not confirmed from text
  alone.
- Do not treat any specific "Transaction X is/isn't valid for Class Y" claim from this note as
  fact until the actual table (p.22–23) has been visually re-checked against the source PDF, or the
  engineer has confirmed the mapping. This must go into the gap register per repo policy — a
  case built against a guessed class/transaction mapping would be exactly the kind of invented
  detail the hard rules forbid.

## 4.1.4 Ticket Selection Display (p.23–25)
Transactions are shown on the ticket-selection screen in a fixed order, paginated (P/N keys scroll
pages). The exact order **varies by which optional transaction types are configured/enabled** for
the route — the spec gives 4 named display variants:

1. **Normal**
2. **No ISS CTT** (Issue Cont. Trip disabled)
3. **No Iss CTT nor RX CTT** (Issue and Receive Cont. Trip both disabled)
4. **No ISS CTT nor RXCTT nor transfer** (Issue/Receive Cont. Trip AND Transfer disabled)

Reconstructed page-by-page order per variant:

| Page | Normal | No ISS CTT | No Iss CTT nor RX CTT | No ISS CTT nor RXCTT nor transfer |
|---|---|---|---|---|
| 1 | Cash | Cash | Cash | Cash |
| 1 | Monthly Pass | Monthly Pass | Monthly Pass | Monthly Pass |
| 1 | MyTix Monthly Pass | MyTix Monthly Pass | MyTix Monthly Pass | MyTix Monthly Pass |
| 1 | X-Ticket | X-Ticket | X-Ticket | X-Ticket |
| 1 | MyTix X-Ticket | MyTix X-Ticket | MyTix X-Ticket | MyTix X-Ticket |
| 1 | Rail Pass | Rail Pass | Rail Pass | Rail Pass |
| 2 | MyTix Rail Pass | MyTix Rail Pass | MyTix Rail Pass | MyTix Rail Pass |
| 2 | Transfer | Transfer | Transfer | Override |
| 2 | X-Transfer | X-Transfer | X-Transfer | X-10 Trip |
| 2 | MyTix X-Transfer | MyTix X-Transfer | MyTix X-Transfer | MyTix X-10 Trip |
| 2 | NC-Transfer | NC-Transfer | NC-Transfer | Cash Round Trip |
| 2 | Override | Override | Override | X-Cash Round Trip |
| 3 | X-10 Trip | X-10 Trip | X-10 Trip | Special |
| 3 | MyTix X-10 Trip | MyTix X-10 Trip | MyTix X-10 Trip | MyTix Special |
| 3 | Cash Round Trip | Cash Round Trip | Cash Round Trip | Non Payment |
| 3 | X-Cash Round Trip | X-Cash Round Trip | X-Cash Round Trip | (blank) |
| 3/4 | Special | Special | Special | (blank) |
| 3/4 | MyTix Special | MyTix Special | MyTix Special | (blank) |
| 4 | O/R Transfer | O/R Transfer | O/R Transfer | (blank) |
| 4 | CTT Cash | MyTix CTT Ticket | Non Payment | (blank) |
| 4 | CTT Ticket | X-CTT | (blank) | (blank) |
| 4 | MyTix CTT Ticket | MyTix X-CTT | (blank) | (blank) |
| 4 | CTT 10 Trip | Non Payment | (blank) | (blank) |
| 4 | MyTix CTT 10 Trip | (blank) | (blank) | (blank) |
| 5 | X-CTT | (blank) | (blank) | (blank) |
| 5 | MyTix X-CTT | (blank) | (blank) | (blank) |
| 5 | Non Payment | (blank) | (blank) | (blank) |

(pp.23–25; the "Page 3/4" boundary for Special/MyTix Special rows is ambiguous in the source layout
— the spec's own "Page 3" / "Page 4" column labels don't align exactly with where these two rows
fall in the extracted text. Treat as p.3-or-4, not a hard fact either way.)

Additional route-level configurability (p.25):
- Product availability is configured in CloudFare; disabling issuance on a route can disable
  **Transfers, ISS CTT, RX CTT** for selection on that route (this is what drives which of the 4
  display variants above applies).
- **Student products can also be disabled on a route**, independent of the transaction-type
  disabling above.

## Suite implications
- **One case per Class** (7 total: Adult, Child, Senior, Student, Employee, Family, Foreign) —
  verify each class is selectable via its softkey/menu group and reflected correctly in Spotter
  Display (AD/CH/SR/STU/EM/FM/FR).
- **One case per Transaction Type** (IDs 0–14, 16–24; skip 15 "not used") — verify payment/receipt
  behaviour, Selection/Ticket-Details/Spotter display strings match the table above, and — where the
  ID has lettered sub-variants (6a/6b, 13a/b/c, 14a/b, 23a/b) — a case per sub-variant since each
  represents a distinct issue/receive or payment-method path.
- **GATED ON GAP RESOLUTION — Class/Transaction combination coverage:** once the engineer confirms
  the true checkmark mapping (see gap above), add: (a) one case per valid Class×Transaction
  combination actually exercised by the suite's target classes/transactions, and (b) explicit
  negative/rejection cases for combinations the spec marks invalid — e.g. attempting a transaction
  type not permitted for the selected class must be blocked/hidden, not silently accepted. Do not
  author these combination cases from a guessed mapping — log to the gap register first.
- **Auto-select behaviour:** a case verifying that when an operator selects a Class with only one
  valid Transaction Type, the system auto-selects that Transaction Type (p.23) — this itself depends
  on the same combination table, so also gated on the same gap.
- **Ticket Selection Display variants:** one case per of the 4 named display variants (Normal / No
  ISS CTT / No Iss CTT nor RX CTT / No ISS CTT nor RXCTT nor transfer), each confirming page
  order/contents matches the table above and P/N page-scroll works across however many pages that
  variant produces (5 pages Normal, fewer as more types are disabled).
- **Route-level disabling:** a case confirming CloudFare-configured disabling of Transfer/ISS
  CTT/RX CTT for a route removes exactly those transaction types from the selection display (driving
  the variant switch), and a separate case for Student-product route disabling (independent toggle).
- **Non Payment (ID 24):** confirm "no receipt" behaviour and that it still records a transaction
  (used to log fare-refusal) rather than being purely cosmetic.
