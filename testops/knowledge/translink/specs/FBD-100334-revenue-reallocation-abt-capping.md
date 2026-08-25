# FBD-100334 — Revenue Reallocation with ABT Capping (distilled)

**Source:** `FBD-100334 - Revenue Reallocation with ABT Capping Specification V0.01` (28 May 2021, K. Horton).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.

> **Status caveat:** V0.01 is an **unfilled template** — body sections are placeholder text. The only
> concrete, distillable content is the **requirement list** below. Treat capping *mechanics* as owned by
> FBD-100389 (scenarios), FBD-100698 (fares-engine capping calls) and FBD-100307 (data flow); this note
> captures the **reallocation/reporting requirements** only. Do not invent behaviour beyond these REQs.

## Requirements (reporting-side revenue reallocation)
- **REQ-2121.0** — reallocate revenue from ticket sales across **companies, home locations and routes** (reporting only). Example: a paper return bought on a rural operator then used to transfer to an Ulsterbus service. *Constraint:* e-Purse smartcard issues/top-ups/validations are reallocated via a **separate facility**.
- **REQ-2121.1** — reallocate revenue from the **initial sale** (first route/home location/company) to the **transfer** route/home location/company.
- **REQ-2121.4** — allow Translink staff to reallocate revenue back to the route/home location/company operating the **majority of the route** where there are disproportionately fewer ticket sales.
- **REQ-2137.0** — allocate **nominal revenue per pass value** (for £0.00-recorded smartcard travel). Each product class + reference fare has a **'valid from' date**; each company can set its **own** pass-revenue value per class+reference; reports must pick the correct value across the selected date range. Pass revenue is taken from the **extended reference fare record** in the transaction audit data.
- **REQ-2153.0** — allocate **generation factor** values per product class **by company** (for Fare Forgone). Up to **2 dp** (e.g. 1.25); **default 1.00**; reports use the correct value per date range; each company independent.
- **REQ-2154.0** — allocate a **journey factor** per product class **by company** (passenger journeys vs ticket counts/passes). Up to **2 dp**; **default 1.00**; one valid factor per class (may be many with different 'applicable from' dates); some classes (e.g. smartcard issue/top-up) have journey factor **0.00** (not counted as passenger journeys).

## Suite implications
- These are **MERIT/DWH reporting** rules, not device behaviour — coverage belongs to the ABT-BOS/reporting suite, not POS/ETM/PV device suites.
- Assert **date-effective correctness**: pass-revenue, generation-factor and journey-factor lookups must honour **'valid from'/'applicable from'** dates across a report's date range (regression-prone).
- Assert **per-company independence** of pass value, generation factor and journey factor for the same product class.
- Assert **journey factor 0.00** classes (smartcard issue/top-up) are excluded from passenger-journey counts.
- **Gap flag:** spec is a stub — before writing detailed reallocation cases, obtain a completed version or confirm behaviour against MERIT; log unconfirmed items as "needs checking" rather than authoring against the template.
