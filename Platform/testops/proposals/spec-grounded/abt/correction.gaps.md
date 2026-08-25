# ABT Correction / Journey-History / Duplicate / Late-Tap — gap register (questions for the engineer)

These are the open questions raised while re-grounding the 47 cases in
`correction.rewrite.json` strictly against the requirement specs. Each is a **question**, not a
finding — per the no-invention rule, they must go through the Q&A loop before the affected cases can
be treated as grounded. Cite answers back into the cases and into `knowledge/`.

## Q21 — CR122 alighting-stop correction: does it exist live, and what is its real UX?
CR122 "Alighting Stop Adjustment" (FBD-100662 §5.6, paras 691–693) is written as a **proposal with UX
"to be determined"**. Affects **28 cases** (all Update Stop List, all Correction Limits, the
correction/dropdown Journey-History cases). Sub-questions:
- Is the correction feature actually implemented and live on env5, or still a paper CR?
- What is the real screen? (The name **"Update Stop list" appears in no requirement document** — where
  does it come from: the implementation? a defect ticket? Confirm the true name.)
- What is the real **filter** on offered stops? The spec grounds only "stops after the boarding stop
  on the same route" (para 693). The cases assert a **fare > 0** filter plus zero-fare / negative-fare
  / TVM-only / transfer exclusions and a **"No options"** empty state and an **operator-match** rule —
  **none of these are in the requirements.** Which (if any) are real, and where are they specified
  (defect/API doc)?
- Do the specific **stop counts** ("14 onward stops" for Greys Farm, "15" for Moygashel Busby Shop)
  come from a real fares/topology dataset? (see Q14)

## Q21 — Portal cancel / refund of a journey
Five Journey-History cases assumed a portal action to **cancel a journey** (and one to refund a
settled charged journey). **No such portal action is specified** — annulment is **device-only**
(FBD-100662 para 204, most-recent tap, within 1 min, boarding stage unchanged), and the only refund
mention (para 690) is a passing reference to "the normal mechanism in the ABT portal". Questions:
- Is there a portal cancel-journey action at all, or is device annulment the only cancel path?
- Since annulment cancels only the **most recent** tap within 1 minute, how is a specific one of two
  same-day taps cancelled (case 4102829)?
- What is the refund mechanism for a **settled** charged journey (case 4102830), and does it retain
  the record?

## Q21 — The "\*\*" cancelled indicator and retain-after-cancel behaviour
The "\*\*" marker for cancelled journeys and the guarantee that a cancelled journey **stays visible /
is not duplicated** in Journey History are **not in any cited requirement** — they read like a
defect-fix acceptance criterion. What is the real indicator, and which ticket/defect defines the
retention behaviour? (JH display itself is grounded — FBD-100662 para 264.)

## Q21 — Late-tap reject behaviour beyond 14 days
FBD-100389 para 233 grounds "accepted up to a **maximum of 14 days**", but the spec does **not** define
what happens to a tap arriving **after** 14 days (dropped silently? audited? flagged with a reason?).
The original case labelled it "rejected as **expired**" — that must not be used, as "expired" is
**DeclinedReason 1 (Card Expired)** (FBD-100658 para 210), an unrelated card-expiry reason. What is
the real >14-day behaviour and label? (case 4102942)

## Q21 — "Blocked ETM" hold-and-release mechanism
Case 4103485 assumes an ETM **blocked from the back office** that holds taps and uploads them when
unblocked. The spec describes late data arising from **comms failure or quarantine in CloudFare**
(FBD-100389 para 229), not a device-block state. Is there a real "device blocked → holds taps →
release on unblock" flow, and where is it specified?

## Q21 — Late annulment settlement representation
Case 4103488: when a batch of held late taps includes an annulled tap, how is the annulled tap shown
at settlement (charged £0.00 + cancelled), and does it affect the cap total of the rest? Annulment is
grounded device-only (para 204) and retrospective capping is grounded (paras 226, 263–288), but the
combined representation is not spelled out.

## Q21 — Duplicate representation in Journey History
FBD-100690 para 469 says duplicate (same-location) taps are **ignored** for journey/capping/charging,
and para 472 says they are shown via an **icon next to the From/To stop + Show More** detail. The
cases instead show a **"£0.00, marked Duplicate" journey row**. Which is correct on the live system?
Also: does the Same Location Time rule (an NIR-TOTO rule) apply to **Metro / Ulsterbus TOO** taps at
all, or is Passback (device, DeclinedReason 20) the only same-card repeat check there?

## Q14 — Unverified values (need a source, not invention)
- **Duplicate / Same Location Time window** — assumed **15 minutes**; FBD-100690 para 469 gives no
  figure. Confirm the configured value.
- **£1.90 Greys Farm** alighting fare (case 4103480) — not verified against a fares export.
- **"Metro Transfer Zone 512"** (case 4102832) — not found in the cited specs; confirm against the
  fares/topology config.
- **Onward-stop counts** ("14", "15") in the dropdown cases — confirm against the route topology for
  72b (IN) from Greys Farm / Moygashel Busby Shop.
- Metro **£4.00** / ref.60 **£7.20** caps and 10A / 72b reference fares (£2.30, £4.50) — used as worked
  examples; trace to the FBD-100662 UB-TOO fares tracker / a fares export to confirm still current.

## Minor / configurability
- Whether the **14-day** late-data maximum is operator-configurable is not stated (FBD-100389 para 233
  states it as a maximum). (case 4102941)
- The **monthly reset** of the 1/month correction allowance is implied by "maximum of 1 per month"
  but not explicitly stated (case 4103482).

---
### POSSIBLE SPEC GAP to escalate (Jira) if no one can answer
The **entire Update Stop List section and the CR122 correction cases describe screen mechanics
(a named screen, a fare>0 filter, a "No options" state, an operator-match rule) that exist in no
requirement document.** Either (a) the feature shipped ahead of the spec and the requirements are
stale, or (b) the cases were authored from an implementation/defect and not from requirements. Either
way it is a **traceability hole**: 28 cases cannot be grounded until CR122's live status and real UX
are confirmed. Recommend raising this with the requirements owner.
