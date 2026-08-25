# GV Suite — Coherence & Capability-Grounding Audit

**Scope:** all 96 GV cases (4104011–4104106) in `suite_GV.json`, checked for internal coherence
(title/preface/preconds/steps/expected describe one scenario) and capability grounding against
FBD-100167 (multi-use barcodes), FBD-100690 (NIR TOTO), FBD-100658 (ABT audit), FBD-100389 (ABT
scenarios), FBD-100348 (gate acceptance), FBD-100653/100654 (router + commissioning).

**Summary:** 96 audited; the suite is largely clean and well-grounded (Declined-Reason codes,
product IDs 6000/5001, check order, £90 fare-fallback, CR105.2/CR116, commissioning params, gate
heartbeat/BIST/mode matrix all match spec). **7 findings: 0 High, 2 Med, 5 Low.** No impossible or
incoherent cases; issues are one grounding contradiction, one title-over-scope, and minor
weak-expected / duplication / labelling items.

## Findings

**C4104030** | Med | grounding | Title/preface/preconds assert a "multi-use barcode ticket printed on a TVM" validating at the GV. FBD-100167 device matrix is explicit: multi-use barcodes are **printed by ETM, HHD (and POS per ticket config)** — TVM is NOT in the print list, and "POS & TVM validate SINGLE-use barcodes only." A TVM-produced *multi-use* barcode is not a grounded artefact. | Needs-confirmation: verify whether TVM can print multi-use barcodes; if not, drop this case (the HHD/ETM-produced equivalents already cover cross-device provenance) or re-cast as a single-use scoping negative.

**C4104046** | Med | coherence (title/preface broader than step) | Title "valid on its start, additional and end dates" and preface "validates only on its start date, an additional-dates offset, or its end date" promise three date conditions, but the single precond+step exercises only the **Start date** case (green tick, gate opens). Expected covers 1 of the 3 claimed conditions. | Either narrow title/preface to the Start-date case, or add steps/rows for the additional-dates-offset and End-date conditions to match the title.

**C4104029** | Low | grounding / needs-confirmation | "A barcode on a mobile device screen validates the same as a printed one." A mobile-displayed multi-use barcode would be a **Corethree (mLink, format 02)** barcode per FBD-100167; the preconds say only "valid multi-use barcode" without naming the on-screen/Corethree variant, so the artefact under test is under-specified. | Confirm the on-screen barcode is Corethree format 02 (validated offline, same business rules) and state that in the preconds; otherwise the "same as printed Flowbird 01" claim is unverified.

**C4104070** | Low | coherence (expected doesn't verify title) | Title claims "location cannot be changed while comms to the back office is lost," but the expected only states "a no-comms condition is indicated on the Location Settings screen" — it never asserts the change is actually blocked/prevented. | Add an expected line that the location edit/save is refused (or the Change control is unavailable) while comms is lost, so the assertion matches the title.

**C4104038 / C4104051** | Low | duplication | These two describe the same CR105.2 gateline Unique-ID-share scenario (a barcode validated on the first head is rejected on the second head of the same gateline) — 4104038 filed under "Multi-Use Barcode Validation," 4104051 under "Passback." Near-identical preconds/step/expected. | Keep one (Passback is the better home) and remove or cross-reference the other to avoid double coverage.

**C4104100** | Low | labelling / mild conflation | Titled "Heartbeat — the GV updates CloudFare Last Communication..." but the mechanism tested is the **15-minute StaffList refresh**, not the gate↔validator heartbeat (which is a distinct concept tested correctly in C4104094). The body is internally coherent; only the "Heartbeat" label risks conflation. | Rename to reference the StaffList/Last-Communication refresh (e.g. "Comms — GV updates Last Communication at least every 15 min") to avoid overloading "Heartbeat." Also needs-confirmation of the 15-min StaffList-as-keepalive mechanism against FBD-100266.

**C4104013** | Low | weak expected | The preconds supply a concrete example TapId (`042002201156881725545715` from DeviceId 0420 + TID 02201156 + UNIX ts), but the expected merely restates the title ("the TapId is the DeviceId, Terminal ID and UNIX timestamp concatenated") without asserting the concrete composed value. Grounded (matches FBD-100658) but the assertion is vague. | Assert the concrete expected TapId value against the seeded DeviceId/TID/timestamp so the check is verifiable rather than a restatement.
