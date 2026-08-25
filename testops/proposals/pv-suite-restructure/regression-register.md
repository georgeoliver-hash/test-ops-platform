# PV regression register

The old suite's defect history lives in **`Fixes/Changes / PV vX`** (PV v3.0.8, v3.1.1, v3.1.2,
v4.2.0, v5.0.0 — ~34 cases). The latest live regression plan (`PV 3.1.2.15214`) ran only **2** of
these — so they are mostly stale version-specific fix checks, not a live regression set.

**Approach (per `docs/test-practices.md` rubric step 4):** fold each fix into the functional case that
owns the behaviour and link the defect id via **Refs** — these PV defects map onto behaviours the new
suite already covers:
- Validation behaviour (zone/time/expiry/passback/invalid reasons) → `Functional / Smartcard
  Validation` + `Functional / Validation Outcomes`.
- ABT/cEMV (deny/BIN, declined, enablement, transfers) → `Functional / ABT (Glider)`.
- Barcode fixes → `Functional / Barcodes`.
- Technician/config/comms fixes → `Functional / Technician Menu` + `Non-Functional / PV`.

**No dedicated PV Regression section is created** — there is no fix with a behaviour the functional
layer doesn't already exercise. If a future defect has no home, add one case under a `Regression`
section with the defect id in Refs (see `/fold-defect`). Enrich each historical fix's Refs onto its
owning case as a follow-up if full defect-traceability in TestRail is wanted (the fix list is in the
old suite's `Fixes/Changes` sections).
