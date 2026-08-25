# ABT / CloudFare Configuration — gap register (Q&A loop)

Questions for the engineer. Each is a `GAP` (absent from requirements) or `UNCONFIRMED` (specified
somewhere but not verified on the surface named). Answers get cited back into the case and into
`knowledge/`. A gap nobody can answer is itself a finding — flag `POSSIBLE DESIGN/SPEC BUG` and raise.

## GAP — no governing spec in this set (out-of-scope surfaces)

### Smartrack (Card Data + Import & Export) — 5 cases: 4103160, 4103161, 4103162, 4103163, 4103164
- Smartrack is a separate card-management application. **No Smartrack spec exists anywhere in the
  requirements library** (searched). ESN list export is *not* a CloudFare config export (FBD-100385
  covers map-point / rules / route / product / product-to-ticket only).
- **Q:** Which document governs Smartrack? Should these cases live in an ABT/CloudFare suite at all,
  or move to a Smartrack suite? Are "Display Card Data", ESN/PSN search, notes/attachments real?

### Merit revenue stored procedures (Stored Procedures) — 3 cases: 4103138, 4103139, 4103140
- These are Merit Data Warehouse artefacts, not CloudFare configuration. Related Merit specs exist
  (**FBD-100387** ABT Reporting Data Warehouse; FBD-100347; FBD-100306 Merit Web) but were not in the
  governing set for this pass and none is a "stored procedures" spec.
- **Q:** Provide FBD-100387 (or the SP catalogue) so procedure names, payment-type / operational-
  payment-type breakdowns and expected outputs can be grounded.

### Station Manager — 3 cases: 4103088, 4103089, 4103090
- No CloudFare Station Manager spec in the library (only hardware gate/station schematics).
  "Network View", "rail line", "station", "branch" are all unverified labels.
- **Q:** Which spec covers Station Manager? Confirm the module, the "Network View" page, and the
  rail line / station / branch objects and operations.

### Device Dataset Deployment — 3 cases: 4103041, 4103042, 4103043
- No spec for Device Datasets, dataset version states, software distribution, or deployment.
- **Q:** Which spec governs Device Dataset Deployment? Confirm version lifecycle states, the
  software-distribution page, and the deploy-to-devices behaviour.

### Quick Product Assignment (Asset Manager) — 1 case: 4103038
- Not in FBD-100263 (which is asset-tracking *reports*, and explicitly not full asset management).
- **Q:** Which spec/screen defines Quick Product Assignment, its operator-level scoping, and the
  add / remove / abandon behaviour?

## UNCONFIRMED — specified/partial but surface or detail unverified

### Setup & Import
- **4102977 Filter by operator** — no "filter by operator" widget in the specs; only an Operator
  Hierarchy level (FBD-100385 §178) and a fixed OperatorId 1 (FBD-100698 §86). *Is there a real
  operator filter, or is scoping purely by hierarchy level?*
- **4102978 Export fares** — fares export is a Reports-module / dedicated Fares Export function
  (FBD-100385 §157, detail in **FBD-100336**) and is service-group based (FBD-100296 §241), not
  "per operator" on the Topology & Fares page. *Where is fares export driven from, and by what key?*
- **4102980 Import route data (parent/child)** — spec covers only CSV map-point import; TransXChange
  route import was deferred at R2.0 (FBD-100296 §72). *Does an XLSX route-data import exist? Format/screen?*

### Rules
- **4103007 Add a fares rule** — rules exist (Rules Report export, FBD-100385 §125) but the creation
  screen/fields are not specified. *Where and how is a rule added?*
- **4103008 e-Purse single-fare charge rule** and **4103009 fixed-fare rule (incl. smartcard fixed
  fare)** — neither rule type is described in any governing spec. *Confirm these rule types exist and
  their configuration.*

### Route Management
- **4102986 Copy route** — does a copied route "retain its assigned fare area"? Fares are out of scope
  of FBD-100296 (§44); copy semantics for fare area unverified.
- **4102987 "service code" / "operator"** — FBD-100296 route attributes are "Public Route Code" and
  "Add to a Service"; there is no "service code" field and routes attach to a *Service*, not an
  operator. *What do "service code" and "operator" mean on the live route screen?*
- **4102988 ABT flat fare** — not a route attribute in FBD-100296 (§234-249). *Does a flat-fare toggle
  exist and where?*
- **4102989 transfer fare within window** — Transfer Time is grounded (FBD-100296 §242); the fare
  returned within the window is fares-engine behaviour (FBD-100698). *Confirm the fare against seeded data.*
- **4102990 fares triangle / fare area / calculate fare** — fares management is out of scope of
  FBD-100296 (§44); belongs to a fares spec (FBD-100336). *Provide it to ground the screen/fields.*
- **4102991 ETM rail substitute route** — rail substitution is grounded as an ABT fare-request concept
  (FBD-100698 §109); a config screen to *create* such a route is not described.

### Products
- **4102996 Preset Reverse FLU** — FBD-100268 has a "Preset" type but no "Reverse FLU" variant.
- **4102998 Excess product** — not a product-type column; FBD-100268 treats Excess as an open-value
  ticket via Minimum/Maximum Value (§47-48). *Is "Excess" a named type live?*
- **4103004 device keyboard buttons** — button assignment is via **Menu-type Product Groups**
  (L1-L5/R1-R5 keys — FBD-100293 §155,202), not a per-product field. *Confirm the intended surface.*
- **4103006 product assignment expiry** — no such named field; nearest are product-level expiry dates
  (FBD-100268 §89,110) and a ticket-assignment "Enabled" flag (FBD-100385 §202). *What does it control?*

### Asset Manager
- **4103036 view/edit device information** — Device Details page + Edit mode grounded (FBD-100263
  §418,450) but editable fields not enumerated (spec is reports-only).
- **4103037 disable/enable a device** — spec describes selectable *status categories* from Device
  Details (FBD-100263 §423), not an enable/disable state. *Is it disable/enable or a status?*

### Configuration & Setup
- **4102953 multi-zone stop** — multi-zone membership grounded (FBD-100229 §119,182); corrected the
  surface to **Zone Settings** (Settings>Topology>Zones §187) — it is **not** set "within the capping
  rules", and the "BusinessRules CreateEdit" claim was removed. Per-zone capping at settlement is
  engine behaviour. *Confirm the settlement outcome against seeded caps.*
- **4102954 Declined Taps Report** — the report, its decline-reason strings (Expired / Declined-ODA /
  On BIN List / On Deny List) and the report claim are **not** in this governing set. *Provide the
  reports / card-verification spec so the report name, claim and reason labels can be grounded.*

## POSSIBLE SPEC/DESIGN GAPS to raise if unanswerable
- Whole feature areas in the ABT suite (Smartrack, Merit SPs, Station Manager, Device Dataset
  Deployment) have **no requirement document** in the library. If confirmed, that is a requirements
  hole to raise in Jira, not just a test gap.
