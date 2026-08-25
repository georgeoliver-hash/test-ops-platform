# ABT/BOS back-office — spec-grounding changelog

**Scope:** 41 cases across 8 sections of `suite_ABT.json` (BOS & ABT suite 30279): Debt Recovery (9),
Customers (8), Customer Services (2), Account Functions (6), Card Verification (4), Activity Log (5),
Shift Board (3), Events & Alerts (4).
**Method:** each case's action/screen/field re-verified against the cited specs, read on demand via
`tools/extract_req.py` from the local `dev/translink-requirements/` library. No invention — every fact
traces to a cited paragraph/section, or is marked GAP.
**Status (2026-07-21): this file already used the correct `{"content","expected"}` step schema (not
the buggy `{"when","then"}` shorthand found in `admin.rewrite.json`), so its cases were never among
the 51 blank-step cases found in the 2026-07-17 partial push. Verified directly against the live
suite before and after: 0 blank-step cases from this file at any point. Properly (re-)pushed
2026-07-21 alongside the admin/cloudfare-config/correction batch via the same, now-hardened
`tools/apply_rewrite.py` (which now also refuses to push any blank step outright). See
`proposals/coherence-audit/fixes/abt-blank-steps-fix.changelog.md` for the full writeup.**
**Output:** `backoffice.rewrite.json` (per-case), this changelog, and `backoffice.gaps.md` (Q&A register).

## Counts

| Action | Count |
|--------|-------|
| grounded (verified; kept / tightened only) | 33 |
| rewrite (substantive change) | 8 |
| unconfirmed (specified, not verified live) | 0 |
| **Total** | **41** |

- **Grounded vs unconfirmed:** 41 grounded to a cited spec, 0 pure-UNCONFIRMED. (No case in these
  sections depends on an unshipped CR; the one spec conflict — C4102867 — is grounded on *both* sides
  and raised as a Q&A/POSSIBLE-SPEC-BUG item, not left as a silent UNCONFIRMED.)
- **Cases carrying a GAP / needs-verify flag:** 18 (see `backoffice.gaps.md`).

## Citation-accuracy corrections (task-supplied paragraphs re-verified)

The task cited three anchors; two needed correction against the raw specs (extractor paragraph numbers):

1. **"store… for historic reporting" is FBD-100307 para 367, not 460.** Para 367 (verbatim): *"The
   device will store transaction information and declined reason for historic reporting."* Task said
   para 460 — but para 460 is a different line: *"Data | These refunds are not provided into the MERIT
   system."* Cited para 367 (+ para 222/376 "declined reason … must be audited") throughout.
2. **FBD-100662 "Journey History shows valid journeys only" has no verbatim para 264 in v5.00.** The
   closest grounding is **para 108**: *"Display taps in the Journey History under the associated customer
   account utilising the boarding and alighting stops received from devices"* — i.e. Journey History is
   built from the journeys' boarding/alighting stops (valid journeys). Cited para 108; flagged the
   para-264 discrepancy in gaps.
3. **FBD-100658 DeclinedReason — confirmed** as an audit-message field: enum `0`=Success, `1`=Expired,
   `2`=On Deny List, `3`=Declined, `4`=Cancelled, `15`=On BIN List, `20`=Passback. Cited as-is.

## Rewrites (8)

| Case | Old | New | Why |
|------|-----|-----|-----|
| **C4102867** | "View all taps including taps not valid for a journey" | "Customer Services — operator reviews a customer's journeys over a date range" | Per the confirmed fact. Journey History shows valid journeys only (FBD-100662 para 108); declined/invalid taps are reviewed via the Declined Taps report + Activity Log and stored in audit (FBD-100307 para 367; FBD-100658 DeclinedReason). **NB the old case was NOT invented** — it traces to REQ-3498.0 / PSPEC-0015 §3.3.6, which is exactly why the conflict is raised (see gaps), not silently discarded. |
| C4103031 | "Filter the activity log by activity, device, date and time" | added the two grounded validation rules | FBD-100358: at-least-one-of Activity/Device-Type is mandatory; date/time range mandatory and capped at 7 continuous days. Original asserted only a generic "filter works". |
| C4103035 | "Failed validations and payments appear in the activity log" | named Declined Reasons + stated this is the invalid-tap review surface | Strengthened to support the C4102867 reframe and the confirmed fact (FBD-100358 + FBD-100307 para 367 + FBD-100658). |
| C4103060 | "Alert Viewer — filter, acknowledge and clear alerts" | added the acknowledge-**before**-clear ordering + named status filters | PSPEC-0013: "an alert must always be acknowledged before it can be cleared"; status filters Acknowledged/Unacknowledged/Cleared/Uncleared. |
| C4102850 | "…card returns to Active" | "…card is re-enabled" (deny-list removal) + flagged status-label inconsistency | FBD-100307 para 314-316/449 grounds deny-list removal, not the portal string "Active"; label conflicts with C4102854's "ACCEPTED". |
| C4102852 | "Visa MIT recovery clears a recoverable issuer-liability debt" | "automated (scheme) recovery…" | FBD-100307 para 309 defines the trigger as *Automated Debt Recovery per card-scheme rules*; "Visa MIT (merchant-initiated)" is a scheme label not used in the cited spec. |
| C4102854 | asserted status literal "ACCEPTED" | "correct recovered status (no longer on deny list)" | Removed the hard literal because it conflicts with "Active" used by C4102850/C4102853 for the same state — one true label needed (gap). |
| C4102947 | "…recovered via one of the four channels" | "…via one of the three triggers" | FBD-100307 para 307-311 defines **three** triggers (web-initiated, automated, tap-initiated); para 305 says web-initiated covers passenger *and* operator, so the original's "customer online" + "operator online" is a UI split of one trigger, not a fourth channel. |

## Grounded (33) — verification notes by section

- **Activity Log (5):** filtering/paging/taxonomy/barcode-ID/failed-validations all trace to FBD-100358.
  C4103035 is the key surface for declined/invalid taps (with the Declined Taps report and the stored
  audit) — cross-linked to the C4102867 reframe.
- **Events & Alerts (4):** Alert Configuration, Alert Viewer, Event Group Configuration, Event Viewer
  all named + behaviour-grounded in **PSPEC-0013** (Events and Alerts Manager) and the module claims in
  FBD-100342.
- **Debt Recovery (9):** deny-list add/remove, recoverable vs unrecoverable, automated/tap/web triggers,
  declined-tap audit (Declined Reason 2) all trace to FBD-100307 (paras 258, 305-316, 439-449) +
  FBD-100658. C4102946 kept verbatim as a model declined-tap audit case.
- **Customers (8):** operator-portal search/select/journey-history/transaction-history/refund/aftercare/
  authorisations grounded in PSPEC-0015 §6.2 + FBD-100307 (refund flow) + FBD-100342 (Account-Management
  and Refund claims / two-person control).
- **Account Functions (6):** passenger-portal aftercare options (**Request refund / Request card
  replacement / Raise a general query**) are enumerated verbatim in PSPEC-0015 §2.3.2; retry-declined-
  payment = web-initiated re-auth (FBD-100307 para 441/445-447).
- **Card Verification (4):** Issuer Liability £10 UK (PSPEC-0015 §4.7.3), Visa AVR first-use-in-network +
  every 14 days, Mastercard daily pre-auth / >14-day / post-deny-removal (PSPEC-0015 §Initial Card
  Requests). Narrowed C4102939/C4102940 to Mastercard (Maestro flagged).
- **Shift Board (3):** CSV validation, Sun→Sat vs Mon→Sun bitmask flip, 4am Valid-From + 7-day purge —
  all already written from FBD-100831; kept verbatim, titles tightened only.

## Encoding note

Source `suite_ABT.json` titles carry mojibake (em-dash rendered `â€"`, `&` as `&`). The rewrite
was authored with clean UTF-8 via the editor (never PowerShell `Set-Content`/`Out-File`, per the
CLAUDE.md encoding rule) so em-dashes and ampersands are correct.
