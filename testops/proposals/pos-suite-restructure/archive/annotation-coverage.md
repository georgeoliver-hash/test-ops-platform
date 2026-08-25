# Annotation coverage audit — cases vs Overflow notes (flow-annotations.md)

Audit of the 540 design notes against the committed cases. Recommendations only — **confirm before
changing** (changes currently parked). Three buckets: CRITICAL mode corrections, ADD (gaps), EDIT
(tighten expected). Evidence = the quoted notes in `flow-annotations.md`.

## CRITICAL — mode-specific corrections (current cases are WRONG without these)
1. **Metro is cash-only.** "Only the cash option is available to Metro users"; "Warrant and card is
   available for NIR and Ulsterbus". → Card Payment + Warrant payment must be **NIR + Ulsterbus only**,
   not shared. Add a Metro "cash only — card/warrant not offered" case. (Card payment otherwise real,
   PCD-conditional — keep it, but scope it to NIR/Ulsterbus.)
2. **Metro has no smartcard validation.** "There are no validations for Metro POS." → Validation
   cases (validate / already-validated / hotlisted / outside-time-band) are **NIR + Ulsterbus only**.
3. **Cross-border (XB) is Rail-only.** "All XB ticket types are only available on Rail POS." → XB
   ticket-type cases belong under **NIR (Rail)** only; XB stations not offered on bus.
4. **Top-up is shared** — confirmed ("All <X> cards can be topped up on any POS"). Already corrected.
5. **Bank Card needs a PCD.** "If there isn't any PCD attached to the POS, Bank Card option will be
   unavailable." → add to the Card Payment case (precondition + negative).

## ADD — genuine coverage gaps (no case covers these)
- **Group ticket** (Numerical Input): + / - sets passenger count, **max 100**; prints **one** group
  ticket receipt; one back-office transaction with per-passenger sub-elements; Cloudfare config of
  which products allow group tickets; error if product/amount not group-eligible.
- **Calculate change** (Numerical Input): unavailable if too many digits / amount < ticket value /
  previous txn had no value.
- **Card Payment EMV flow** (currently one thin case): contactless vs chip&PIN vs swipe; "authorising";
  declined → declined receipt; signature-doesn't-match; PIN entered incorrectly too many times;
  value too big for card; PCD/M020-driven error messages; receipt optional; auto-void on error.
- **Discount/entitlement smartcard validation** (Senior, Blind, War Pensioner, yLink, 24+, Half-Fare,
  Dependants): presenting the pass sets the ticket type; **validation per transaction**; **cannot be
  added to a basket**; can still change boarding/alighting; XB variants (Rail) selectable via L4/R4.
- **Expired Multi-Journey top-up**: adding journeys to an expired MJ **removes all existing journeys**
  and prints a **journey-removal receipt**.
- **Validation error mid-transaction**: cash/warrant **not recorded**; any card txn **auto-voided**;
  a diagnostic event is audited.
- **Basket rules**: max **9** tickets, Add More disabled at max (re-enabled after delete); smartcard
  passes can't be basketed; **bus basket can't mix two routes** (can mix two boarding stages, same route).
- **Cash/max-revenue limit**: device **locks**, "Notify a Supervisor or Technician", recovers comms
  in background; approaching-limit notification (3s).
- **Power interruption**: temporary → resume to prior screen; longer than Auto-Sign-Off → Idle, **no
  waybill**; shorter → Operator Break screen; pre-boot charge check; suspend → reboot timings.
- **Auto sign-off / suspend / reboot** (configurable): FLU inactivity → Idle no waybill, break skipped;
  Idle inactivity → suspend (screen off); suspend duration → auto-reboot to Idle; keypress in suspend → reboot.
- **Audio tones**: success (top-up/issue/ticket), error (any failure), timeout, frequent beep
  (smartcard left on reader).
- **Printer**: paper-low temporary notification (3s); print-fail / partial-print-on-power-loss /
  resume-after-power-loss events sent.
- **Barcode scanning**: validate ticket by barcode type; offline-validated barcodes stored until
  Cloudfare/Corethree reconnect; some barcode types carry Notes; access via Operator Menu.
- **Cross-border currency toggle** (Rail): price button toggles GBP ↔ euro for XB journeys.

## EDIT — tighten existing cases with annotation detail
- **Sign On:** lockout threshold is **configurable** (not hard "3"); 'C' deletes a char and steps to
  previous field when empty; MotD / Word & Colour shown **if configured/available**, else an error
  screen; after fail, redirect to ID/PIN field after **3s or Enter**; Metro lands on a specific
  post-sign-on screen.
- **Supervisor Print & Zero:** confirm-before-zero; printout contents (operator/POS no., sign-on/off
  times, tickets sold, revenue, misc revenue, validations, annulled, first/last ticket no., per-ticket detail).
- **Technician:** brightness/volume incl. restore-defaults; Device Settings confirm → **reboot**;
  Network = Ethernet with cellular fallback; Soft Reboot → Idle; card-reader test → mini statement.
- **Rail FLU:** favourites use numbered slots; advance ticket = one-at-a-time, not with others in
  basket, resets after 1 min inactivity; boarding=alighting disables passenger/ticket/price/basket.

## Confirmed LEAVE (annotations back this up)
- Commissioning a smartcard on the POS was **removed** by CR (per the Admin note) → confirms leaving
  TIBU-20886 and the commissioning cases out.

## Scale
~15 ADD, ~5 CRITICAL mode corrections, ~10 EDIT clusters. Recommend a **refinement pass** flow by
flow (Sign On → … → Top Up), applied via `push --update` with George's go-ahead.
