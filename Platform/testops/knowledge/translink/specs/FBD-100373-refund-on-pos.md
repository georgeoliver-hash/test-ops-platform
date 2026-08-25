# FBD-100373 — Refund on POS (distilled)

**Source:** `FBD-100373 Refund on POS Solution Specification V3.00` (24 Jun 2026, C. Warnes / S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Related: FBD-100306 (Merit Web Reports Viewer). **Gated by CR115** (see bottom).

## Scope — what can be refunded, on which device
- **Only the POS device performs refunds.** (HHD, TVM, ETM do NOT process refunds themselves — REQ-1630.0: TVM = sales only; HHD = sales+reversals, no refunds.)
- POS can refund **paper ticket sales (and miscellaneous sales, e.g. private hire, tachograph)** originally made on **POS, TVM or HHD** — by **cash or card**.
- POS can refund paper ticket sales made on an **ETM only if originally paid by CASH** (ETM card sales NOT refundable).
- Works **cross-device, cross-date, cross-company**: any POS (Bus or Rail) can refund any qualifying ticket regardless of originating device, date, or operating company (e.g. Rail-TVM sale refunded on a Bus POS).
- Refund is **full or partial**. Always in **Pounds Sterling (£)**, both cash and card.
- **Refund ≠ annulment** (different process). A refund is **final — cannot be annulled/cancelled** once completed.

## Authorisation (role matrix)
- **Operator**: annulment ✔, refund ✔. **Supervisor / Technician / Administrator**: annulment ✘, refund ✘.
  (Only the Operator role may refund — the reverse of what one might assume; assert this explicitly.)

## Cash refund flow & validation
- Operator Menu → **"Issue Refund"** → select **"Cash Refund"** via L1/L2 buttons.
- Operator keys the **URN** (printed on original ticket), Enter, then **Refund Amount**.
- **URN format (23 chars):** `DDMMYY`(6, original sale date) + `Device No`(6, zero-padded; TVM alpha chars omitted) + `Ticket Number`(6, zero-padded) + `Original Sale Value`(5 = 3 pounds + 2 pence, zero-padded). Example `01122400428500078601300`.
  - **Basket sales:** URN's sale-value segment uses the **per-ticket** value, not the basket total (£10 Adult + £5 Child → each ticket's URN carries its own value).
- **Amount entry auto-formats as currency** as digits are typed (`2`→£0.02, `25`→£0.25, `250`→£2.50, `2500`→£25.00). `C` clears the field; `C` on an empty Refund Amount returns to the URN field.
- **On Enter, POS validates:** (1) URN is exactly **23 characters**; (2) refund amount **≤ last-5-digit original sale value**; (3) refund **would not drive shift totals negative**.
  - Fail (1) or (2): error message + error tone, both fields cleared, operator must acknowledge and re-enter.
  - Fail (3): error "**Cash refund cannot be performed**".
- Success → prints **refund receipt (customer + operator copy, torn in half)**; success message + tone showing amount refunded.

## Card refund flow & validation
- Operator Menu → "Issue Refund" → **"Card Refund"** (L1/L2).
- Operator keys the **Payment Reference Number (PRN)** printed on the original ticket, then the refund amount.
- **PRN format by device:**
  - TVM: `TVM serial (incl. alpha)` + `ticks since 0001-01-01 midnight`
  - HHD: `H` + last 8 of IMEI + ticks + 2-digit operator code (e.g. `H81069695637665422474655130YG`)
  - POS: `P` + Way6 serial + ticks + 2-digit operator code
  - Basket: **same PRN printed on every ticket** in the basket (unlike the per-ticket URN).
- PRN is **alphanumeric**: alpha chars entered via L1–L5/R1–R5 buttons; Up/Down arrows page through alpha sets; **alpha keys shown only while the PRN field is selected**, hidden/disabled on the Refund Amount field.
- On Enter, POS calls the **payment provider (PSP) API in real time** with amount + PRN; PSP returns success/failure and the **actual amount refunded** (that returned value is what gets audited + printed).
- **If refund amount entered > original sale value, PSP caps refund at the original sale value.**
- **Network required:** timeout contacting PSP → error + tone, no refund. PSP-reported failure → error + tone.
- Success → refund receipt (customer + operator copy, torn), success message + tone.

## Audit record (to CloudFare) — cash and card
- **Fare** = refunded amount recorded as a **POSITIVE** value (not negative).
- **Payment Method:** Cash = `1`, Card = `3`.
- **Payment Reference:** cash → the URN; card → the PRN.
- **Product ID:** a new product `7000`-style, type **"Open"**, with **"Allow Refund" = true**; device picks the product whose Allow-Refund flag is set.
- **Route Variant Id:** present + populated (most-recently signed-on route variant) for **Ulsterbus**; **absent for NIR**.
- **Route Reference Id:** present (rail route reference table) for **NIR**; absent for Ulsterbus.
- **Boarding Id** = most recent boarding id used; **Transaction Date** = refund date/time.
- **Refund Product CloudFare config:** new class product named **"Refund"** at the **Translink** hierarchy level, Product Type **Open**, Short Code "Refund", Display Description "Refund", Merit Sync = Yes, **Allow Refund = True**, enabled on **all POS types**.

## Reporting
- **CloudFare Activity Log:** filter Activity = Transaction, Device = Point of Sale, Product = "Refund". Each record shows payment type, PRN (card) or URN (cash), refund amount, refund product, and the **operator ID** who performed it.
- **MERIT:** refunds reported via class-type "Refund" in Class Breakdown / Sales Breakdown by Class / Class Revenue Performance / Sales Analysis by Class. **Refund revenue shown as POSITIVE** (MERIT can't hold negatives).
- **Pay-In Reconciliation report:** adds a refund-count column; **Total Revenue = Cash Rev + Card Rev + Refund Cash + Refund Card**.
- **POS operator waybill / end-of-shift:** lists refunds split cash vs card; cash refunds **subtract from** the cash total and from the amount sent to the PayComplete API.

## Assumptions / limitations (all testable negatives)
- POS applies **no eligibility rules**: won't block refund of expired tickets, already-used return/day products, or already-scanned barcode tickets.
- **Refund only against the original payment method** (no cash refund of a card sale, or vice versa).
- **Cannot perform more cash refunds than sales** in a shift/day.
- Smartcard issues/top-ups **out of scope** — not refundable via POS.
- Card refund needs live network; no connection = no refund.

## CR dependency
- **CR115** — enables refunding TVM/HHD/ETM transactions on a POS (card-not-present linked refunds via the printed reference), plus HHD cash+card and ETM cash-only refund functions. **If CR115 is rejected, POS refunds are limited to POS-originated sales** and the spec changes. Track CR115 acceptance state before asserting cross-device refunds.

## Suite implications (POS suite 30253)
- Assert the **device/payment matrix**: POS-only refunds; POS/TVM/HHD cash+card refundable; ETM cash-only; TVM/HHD/ETM cannot themselves refund. Tag the CR115-dependent cross-device cases so they can be deselected if CR115 slips.
- Assert **role gating** — Operator can refund, Supervisor/Technician/Admin cannot (likely a coverage gap).
- Cover **cash validation edges**: URN ≠ 23 chars, refund > original value, shift-total-negative ("Cash refund cannot be performed"), field-clear behaviour, currency auto-format.
- Cover **card path**: PSP timeout (no network), PSP failure status, over-value capped to original, alpha-char PRN entry, audit uses PSP-returned amount.
- Cover **basket URN (per-ticket value) vs basket PRN (shared)** distinction.
- Assert **audit fields**: positive Fare, Payment Method 1/3, correct reference (URN/PRN), Product type Open + Allow Refund, Ulsterbus Route Variant Id present / NIR Route Reference Id present.
- Assert **reporting**: Activity Log filter shows operator ID + reference; MERIT positive-value refund class; Pay-In total includes refunds; waybill cash total reduced.
- Assert **finality** (no annul after refund) and **partial refund** handling.
