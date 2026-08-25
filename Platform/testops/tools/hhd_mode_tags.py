"""ID -> MODE-* tag map for suite 30285, built from full-body content read + structure.md
(proposals/hhd-suite-restructure/structure.md). See mode-coverage.md for the section-level
rationale. Every one of the 335 live cases must appear exactly once."""

NIR_ONLY = [
    # Card Payment / Reference-Number Stations (NIR only, explicit)
    4103818, 4103819,
    # Sales - Paper Tickets / Cross-Border Tickets (NIR only, explicit)
    4103871, 4103872, 4103873, 4103874, 4104709, 4104710, 4104711, 4104712,
    # Ticket Issue - explicit "(NIR-Rail, ...)" 3 Day Select
    4103858, 4104708,
    # Single-Use Barcodes (NIR) - whole section explicit
    4103951, 4103952, 4103953, 4103954, 4103955, 4103956, 4103957, 4103958, 4103959, 4103960, 4103961,
    # Ticket Formats & Waybill - NIR Layouts
    4103939, 4103940, 4104749, 4104750, 4104751, 4104752, 4104753, 4104754, 4104763, 4104764, 4104769,
]

GLIDER_ONLY = [
    # Multi-Use Barcodes / Old Barcode Redemption (BRS) - Glider only, explicit
    4103970,
    # Sales - Paper Tickets / Metro & Ulsterbus Products - Glider only, explicit
    4103875, 4103876, 4103877, 4103878, 4104713, 4104714, 4104715, 4104716, 4104717, 4104718, 4104719,
    4104720, 4104721, 4104722, 4104723, 4104724, 4104725,
    # Revenue Inspection (cEMV/RID) - whole section; Glider TOO live now, NIR TOTO is future scope (FBD-100690)
    4103978, 4103979, 4103980, 4103981, 4103982, 4103983, 4103984, 4103985, 4103986, 4103987, 4103988,
    4103989, 4103990, 4104785, 4104786, 4104787, 4104788, 4104789,
    # Sign On & Session - Inspector/Validation Mode ties to the Glider-only TOO/inspection feature
    4104128, 4104747, 4104748,
    # Smartcards & ABT - explicit "(Glider)" products + the Glider inspection-tap cases
    4103833, 4103835, 4104674, 4104675, 4104676, 4104677, 4104678, 4104679, 4104680,
    # Ticket Formats & Waybill - Glider Formats
    4103941, 4103942, 4104755, 4104756, 4104757, 4104758, 4104759, 4104760, 4104761, 4104762, 4104765,
    4104766, 4104767, 4104768, 4104771, 4104772,
    # Top-Ups - Daylink/Metro Travelcard/BVP/Ulsterbus-labelled (Glider-only product family)
    4104726, 4104727, 4104728, 4104732, 4104735, 4104736, 4104737, 4104740,
]

PRIMARY_ONLY = [
    # Annulment & Reversal - generic device/payment mechanics, zero product/fare dependency
    4103841, 4103842, 4103843, 4103844, 4103845, 4103846,
    # Card Payment (M020) - whole section: payment-device mechanics (pairing, TID/TK, scheme
    # accept/decline, timeout, cancel, PAN masking, PRN format, on-charge) are mode-agnostic
    4103800, 4103801, 4103802, 4103803, 4103804, 4103805, 4103806, 4103807, 4103808, 4103809, 4103810,
    4103811, 4103812, 4103813, 4103814, 4103815, 4103816, 4103817, 4104663, 4104665, 4104667, 4104668,
    4104669,
    # Operator - menu/UI/device mechanics
    4103914, 4103915, 4103916, 4103917, 4103919, 4103920, 4103922,
    # Penalty Warning & Fares - RBAC-only case (not fare-content)
    4103898,
    # Sign On & Session - generic auth/session/device mechanics
    4103901, 4103902, 4103903, 4103904, 4103905, 4103906, 4103909, 4103910, 4103911, 4103912, 4103913,
    # Smartcards & ABT - device capability limitation (not fare/product driven)
    4103832,
    # Supervisor - whole section: role/device mechanics
    4103923, 4103924, 4103925, 4103926, 4103927, 4103928, 4103929, 4103930, 4103931, 4104127,
    # Technician - whole section: device/hardware config mechanics
    4103932, 4103933, 4103934, 4103935, 4103936, 4103937, 4103938,
    # Ticket Formats & Waybill - waybill reconciliation mechanic (generic aggregation, not format-specific)
    4103947, 4103948, 4103949, 4103950,
    # Non-Functional / Resilience - whole area, per the tag definition's explicit example
    4103996, 4103997, 4103998, 4103999, 4104000, 4103991, 4103992, 4103993, 4103994, 4104001, 4104002,
    4104003, 4104004,
]

BOTH = [
    # Annulment & Reversal - annulling a specific product/entitlement (fare/product-driven)
    4103836, 4103837, 4103838, 4103839, 4103840, 4104694,
    # Multi-Use Barcodes - shared product, fare/location-threshold driven
    4103962, 4103963, 4103964, 4103965, 4103966, 4103967, 4103968, 4103969,
    # Operator - favourites (product-driven) + penalty fare issue (fare-driven)
    4103918, 4103921,
    # Penalty Warning & Fares - fare/entitlement driven (rest of section)
    4103893, 4103894, 4103895, 4103896, 4103897, 4103899, 4103900, 4104741, 4104742, 4104743, 4104744,
    4104745, 4104746,
    # Sales - Paper Tickets / Basket - basket lines are product/fare-driven paper-ticket sales
    4103862, 4103863, 4103864, 4103865, 4103866, 4103867,
    # Sales - Paper Tickets / Group Ticket Sales
    4103868, 4103869,
    # Sales - Paper Tickets / Ticket Issue - generic products/payment methods (rest of section)
    4103847, 4103848, 4103849, 4103850, 4103851, 4103852, 4103853, 4103854, 4103855, 4103856, 4103857,
    4103859, 4103860, 4103861, 4104695, 4104696, 4104697, 4104698, 4104699, 4104700, 4104701, 4104702,
    4104703, 4104704, 4104705, 4104706, 4104707,
    # Sales - Paper Tickets / Visual Inspection
    4103870,
    # Sign On & Session - topology/route-service selection (config-driven, differs by mode)
    4103907, 4103908,
    # Smartcard Inspection - whole section: shared concessionary/entitlement types
    4103971, 4103972, 4103973, 4103974, 4103975, 4103976, 4104773, 4104774, 4104775, 4104776, 4104777,
    4104778, 4104779, 4104780, 4104781, 4104782, 4104783, 4104784,
    # Smartcards & ABT - shared entitlement/product validation (rest of section)
    4103820, 4103821, 4103822, 4103823, 4103824, 4103825, 4103826, 4103827, 4103828, 4103829, 4103830,
    4103834, 4104670, 4104671, 4104672, 4104673, 4104681, 4104682, 4104683, 4104684, 4104685, 4104686,
    4104687, 4104688, 4104689, 4104690, 4104691, 4104692, 4104693,
    # Ticket Formats & Waybill - generic across-mode formats (Format 16 paper ticket, faulty
    # smartpass receipt, travel/print-test, penalty ticket)
    4103943, 4103944, 4103945, 4103946, 4104770,
    # Top-Ups - shared entitlement/product top-ups (rest of section)
    4103879, 4103880, 4103881, 4103882, 4103883, 4103884, 4103885, 4103886, 4103887, 4103888, 4103889,
    4103890, 4103891, 4103892, 4104729, 4104730, 4104731, 4104733, 4104734, 4104738, 4104739,
    # Smoke - critical path across products/fares, needs per-mode verification
    4104005, 4104006, 4104007, 4104008, 4104009, 4104010,
]

TAG_MAP: dict[int, str] = {}
for cid in NIR_ONLY:
    TAG_MAP[cid] = "MODE-NIRRAIL-ONLY"
for cid in GLIDER_ONLY:
    TAG_MAP[cid] = "MODE-GLIDER-ONLY"
for cid in PRIMARY_ONLY:
    TAG_MAP[cid] = "MODE-PRIMARY-ONLY"
for cid in BOTH:
    TAG_MAP[cid] = "MODE-BOTH"

if __name__ == "__main__":
    all_ids = NIR_ONLY + GLIDER_ONLY + PRIMARY_ONLY + BOTH
    dupes = [i for i in set(all_ids) if all_ids.count(i) > 1]
    print(f"NIR_ONLY={len(NIR_ONLY)} GLIDER_ONLY={len(GLIDER_ONLY)} PRIMARY_ONLY={len(PRIMARY_ONLY)} BOTH={len(BOTH)} TOTAL={len(all_ids)}")
    print(f"duplicates: {dupes}")
