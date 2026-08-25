"""One-off: append MODE-BOTH / MODE-GLIDER-ONLY / MODE-RAIL-ONLY / MODE-PRIMARY-ONLY tags to the
Refs field of every live (non-condemned) case in PV suite 30255, per the mode-execution tagging
scheme agreed with George (2026-07-27). Appends, never overwrites existing refs. Dry-run by default;
pass --commit to actually write. Pass --sample to process only the first 5 (a dry-run sanity check).

Classification is grounded in the live case bodies (preconditions/steps explicitly say "Glider PV",
"Rail PV", "NIR", etc.) plus proposals/pv-suite-restructure/coverage-map.md + structure.md. See
proposals/pv-suite-restructure/mode-coverage.md for the full per-case rationale and the flagged
uncertain judgment calls.

Run:
    $env:TESTRAIL_WRITE_SUITE_ID="30255"
    .venv\\Scripts\\python.exe tools\\tag_pv_modes.py            # dry-run, all cases
    .venv\\Scripts\\python.exe tools\\tag_pv_modes.py --sample   # dry-run, first 5 only
    .venv\\Scripts\\python.exe tools\\tag_pv_modes.py --commit   # writes to TestRail
"""
import sys

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id

SUITE = 30255
PROJECT = 42

MODE_BOTH = [
    # Smartcard Validation family (products, could plausibly differ by mode even if steps identical)
    4100981, 4100982, 4100983, 4100984, 4100985, 4100986, 4100987, 4100988, 4100989, 4100990, 4100991,
    4101090, 4104432, 4104433, 4104435, 4104436, 4104438, 4104440, 4104442, 4104444, 4104446, 4104448,
    4104450, 4104451, 4104453, 4104455, 4104457, 4104459, 4104461, 4104464, 4104465, 4104467, 4104469,
    # Validation Outcomes (shared invalid reasons / passback / offline / machine-not-in-service)
    4100992, 4100993, 4100994, 4100995,
    # Barcodes — per-product multi-use validation + early-morning expiry (product/fare-driven)
    4101006, 4102428, 4104489, 4104491, 4104493, 4104495, 4104496, 4104498, 4104500, 4104501, 4104503,
    # Legacy & Card Tech (product/passback/operating-times rules, config-driven)
    4101007, 4101008, 4101009, 4101010,
    # Barcode Validation — Multi-Use valid/invalid outcome (product/fare-driven; Single-Use kept PRIMARY)
    4103560, 4103561,
    # Smoke — smartcard/barcode smoke mirrors the MODE-BOTH mechanism it samples
    4101072, 4101073, 4101074,
    # HMI — ABT deny-list/error/hotlisted screens: appear in the shared Platform Validator-Barcode
    # flow (no Rail-suffixed variant exists for these, unlike ABT Tag successful) - UNCERTAIN, flagged
    4101038, 4101039, 4101040,
]

MODE_GLIDER_ONLY = [
    # Functional > ABT (Glider) — cEMV/ABT tap validation, declines, lists, FEIG, TOO, transfers
    4100998, 4100999, 4101000, 4101001, 4101002, 4101003, 4101004, 4101078, 4101079, 4101080, 4101081,
    4101088, 4101089, 4101092, 4101093, 4104108, 4104480, 4104482, 4104484, 4104486, 4104487,
    4104505, 4104507, 4104509, 4104510, 4104512, 4104513, 4104515, 4104931, 4104932,
    # Pilot List (explicitly cEMV/ABT-gated)
    4103562, 4103563, 4103564,
    # Smoke — ABT contactless tap
    4101075,
    # HMI — base "ABT Tag successful" screen (Glider variant; Rail has its own suffixed screen)
    4101037,
    # NFR — Deny/BIN list download explicitly gated on "PV has cEMV" - UNCERTAIN, flagged
    4101020,
]

MODE_RAIL_ONLY = [
    # Functional > Rail-specific
    4100996, 4100997, 4102429, 4104471, 4104473, 4104475, 4104477, 4104478,
    # ABT Audit — NIR TOTO tap
    4103565,
    # Legacy Transfer — explicitly "legacy rail smartcard"
    4103566, 4103567,
    # HMI — Rail-suffixed ABT Tag successful screen
    4101036,
]

MODE_PRIMARY_ONLY = [
    # Functional > Technician Menu
    4101011, 4101012, 4101013, 4101014, 4101015, 4101016, 4101017, 4101091,
    4102166, 4102167, 4102168, 4102181,
    # Non-Functional > PV (comms/hardware/technician maintenance; Deny/BIN download excluded -> Glider)
    4101018, 4101019, 4101021, 4101022, 4101082, 4101083, 4101084, 4101086, 4101087,
    4101094, 4101095, 4104110,
    # Non-Functional > Comms (Ethernet/cellular failover applies both modes per pv-failover-restore.md)
    4101085, 4103568, 4103569,
    # HMI Screen Validation > Validation Screens (non-fare / generic screens)
    4101023, 4101024, 4101025, 4101026, 4101027, 4101028, 4101029, 4101030, 4101031, 4101032,
    4101033, 4101034, 4101035, 4101041, 4101042, 4101043, 4101044, 4101045, 4101046, 4101047,
    # HMI Screen Validation > Technician Menu (all generic)
    4101048, 4101049, 4101050, 4101051, 4101052, 4101053, 4101054, 4101055, 4101056, 4101057,
    4101058, 4101059, 4101060, 4101061, 4101062, 4101063, 4101064, 4101065, 4101066, 4101067,
    4101068, 4101069, 4101070, 4101071,
    # Smoke — Technician Menu login + PV communicates with back office
    4101076, 4101077,
    # Commissioning
    4102430,
    # Barcode Validation — Single-Use rejection (device capability constant, not mode-driven)
    4103559,
    # Barcodes — reader disconnect banner/event (hardware fault)
    4104109,
]

TAG_MAP = {}
for cid in MODE_BOTH:
    TAG_MAP[cid] = "MODE-BOTH"
for cid in MODE_GLIDER_ONLY:
    TAG_MAP[cid] = "MODE-GLIDER-ONLY"
for cid in MODE_RAIL_ONLY:
    TAG_MAP[cid] = "MODE-RAIL-ONLY"
for cid in MODE_PRIMARY_ONLY:
    TAG_MAP[cid] = "MODE-PRIMARY-ONLY"


def main():
    commit = "--commit" in sys.argv
    sample_only = "--sample" in sys.argv

    suite = load_write_suite_id()
    if suite != SUITE:
        raise SystemExit(f"expected TESTRAIL_WRITE_SUITE_ID={SUITE}, got {suite}")

    client = TestRailClient()
    writer = TestRailWriter(client, PROJECT, suite, commit=commit)

    cases = client.get_cases(PROJECT, SUITE)
    by_id = {c["id"]: c for c in cases}

    # sanity: every live (non-condemned) case must be classified exactly once
    live_ids = {c["id"] for c in cases if not (c.get("title") or "").startswith("ZZ_DELETE_REVIEW")}
    missing = live_ids - set(TAG_MAP)
    extra = set(TAG_MAP) - live_ids
    if missing:
        print(f"WARNING: {len(missing)} live cases have no tag assigned: {sorted(missing)}")
    if extra:
        print(f"WARNING: {len(extra)} tagged ids are not live cases in this suite: {sorted(extra)}")

    todo = sorted(TAG_MAP.items())
    if sample_only:
        todo = todo[:5]

    updated, skipped_already, errors = 0, 0, 0
    for cid, tag in todo:
        case = by_id.get(cid)
        if not case:
            print(f"SKIP {cid}: not found in live suite pull")
            errors += 1
            continue
        existing_refs = (case.get("refs") or "").strip()
        existing_list = [r.strip() for r in existing_refs.split(",") if r.strip()] if existing_refs else []
        if tag in existing_list:
            skipped_already += 1
            continue
        new_refs = existing_list + [tag]
        new_refs_str = ", ".join(new_refs)
        res = writer.update_case_fields(cid, {"refs": new_refs_str}, section_id=case.get("section_id"))
        print(f"{'[DRY] ' if not commit else ''}{cid} ({case.get('title')[:60]}): "
              f"'{existing_refs}' -> '{new_refs_str}'  [{tag}]  {res if not commit else ''}")
        updated += 1

    print(f"\ndone: {updated} updated, {skipped_already} already tagged, {errors} errors, "
          f"{len(todo)} total processed (commit={commit})")


if __name__ == "__main__":
    main()
