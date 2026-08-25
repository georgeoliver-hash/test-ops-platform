"""Same "Data variations:" -> one-case-per-variant expansion, for suite 30287 (BOS — CloudFare/
Merit/Merit Web Reporter/Smartrack). 3 families found (full-suite grep, excl. ZZ_DELETE_*):
  - C4104254 Configure report access for a role   -> TVM/Cash, Staff, Alert, Asset, Topology (5)
  - C4104255 Configure module/group access role   -> operator-scope, 7 modules, gate/station (9)
  - C4104258 Fares export                          -> 5 export-scope variants (file format
                                                        XLSX/CSV kept as in-case supporting detail,
                                                        same treatment as EMV Summary Report's
                                                        export-format list in suite 30279)

Split granularity matches the 30279 pass exactly: split at the literal top-level semicolon-
delimited item in the original "Data variations:" line (same rule that gave 4 cases for
C4102857's claim groups); nested comma-lists inside one item stay as in-case supporting detail,
not exploded further.

Writes:
  - bos-variant-expansion-30287.rewrite.json    (3 primary-case updates, for apply_rewrite.py)
  - bos-variant-expansion-30287.new-cases.json  (16 new-case rows, for push_new_cases.py)
"""
from __future__ import annotations
import json
from pathlib import Path

OUT = Path(__file__).parent
TAG = "\n\n[Automatable: {auto} · Cross-check: {check}]"

rewrite_rows = []
new_rows = []


def add_primary(cid, title, preface, preconds, steps, expected, refs):
    rewrite_rows.append({
        "id": cid, "title": title, "preface": preface, "preconds": preconds,
        "steps": steps, "expected": expected, "refs": refs,
    })


def add_new(section_id, title, preface, preconds, steps, expected, refs, priority_id=1, devtypes=None):
    new_rows.append({
        "section_id": section_id, "title": title, "preface": preface, "preconds": preconds,
        "steps": steps, "expected": expected, "refs": refs, "priority_id": priority_id,
        "custom_devtypes": devtypes or [100],
    })


# ------------------------------------------------------------------ #
# A. C4104254 — Configure report access for a role: TVM/Cash / Staff / Alert / Asset / Topology
# ------------------------------------------------------------------ #
SEC_254 = 887862
REPORT_CATS = ["TVM/Cash", "Staff", "Alert", "Asset", "Topology"]
for cat in REPORT_CATS:
    title = f"Configure report access for a role — {cat} reports"
    preface = (f"This test is to confirm that an administrator can manage which {cat} reports a "
               "role can access, including specific reports.")
    preconds = "**GIVEN** an administrator is signed into CloudFare"
    steps = [{
        "content": f"**WHEN** the administrator sets the {cat} report access for a role, including specific report access",
        "expected": f"**THEN** the role can access only the permitted {cat} reports",
    }]
    expected = (f"A role's {cat} report access matches the administrator's configuration." +
                TAG.format(auto="Yes", check="CloudFare"))
    refs = "FBD-100342"
    if cat == "TVM/Cash":
        add_primary(4104254, title, preface, preconds, steps, expected, refs)
    else:
        add_new(SEC_254, title, preface, preconds, steps, expected, refs)


# ------------------------------------------------------------------ #
# B. C4104255 — Configure module and group access for a role: operator-scope, 7 modules, gate/station
# ------------------------------------------------------------------ #
SEC_255 = 887862

# B1: operator-scope claims (kept as one case — a Full-vs-named comparison, same shape as the
# original un-split case, which already compared two operators with differing claims).
add_primary(
    4104255,
    "Configure module and group access for a role — operator-scope claims",
    "This test is to confirm that an administrator can set a role's operator-scope claim (CF "
    "Full Operator vs CF-Operator-<Name>).",
    "**GIVEN** an administrator is signed into CloudFare",
    [{
        "content": ("**WHEN** the administrator sets a role's operator-scope claim — CF Full "
                    "Operator (AccessControlFullAccess, all operators in hierarchy) or "
                    "CF-Operator-<Name> (AccessControl<name>, that operator only, no sub-operators)"),
        "expected": "**THEN** the role's visible operators match the configured scope",
    }],
    "A role's operator-scope claim (Full Operator vs a named single operator) matches the "
    "administrator's configuration." + TAG.format(auto="Yes", check="CloudFare"),
    "FBD-100342",
)

# B2: 7 module/sub-module cases
MODULES = [
    ("Dashboard", ""),
    ("Events & Alerts", " (Alert Configuration, Event Group Configuration)"),
    ("Topology & Fares", " (Route Management, Service Delete, Legacy Stages, Product Editor, "
                          "Fare Rules, Ticket Editor, Delete Label)"),
    ("Schedule Manager", " (Import, Topology Sync)"),
    ("Estate Management", " (Comms Monitor, Activity Log, Asset Manager, Cash View, Staff Manager, "
                           "Device Dataset Deployment, Quarantine, Device Logging)"),
    ("Reports", ""),
    ("System Configuration", " (Notifications)"),
]
for module, subclaims in MODULES:
    title = f"Configure module and group access for a role — {module} module access"
    preface = (f"This test is to confirm that an administrator can set a role's {module} module "
               f"access{subclaims}.")
    preconds = "**GIVEN** an administrator is signed into CloudFare"
    steps = [{
        "content": f"**WHEN** the administrator sets a role's {module} access{subclaims}",
        "expected": f"**THEN** the role can access only the permitted {module} functions",
    }]
    expected = (f"A role's {module} module access matches the administrator's configuration." +
                TAG.format(auto="Yes", check="CloudFare"))
    add_new(SEC_255, title, preface, preconds, steps, expected, "FBD-100342")

# B3: gate/station claims
add_new(
    SEC_255,
    "Configure module and group access for a role — gate/station claims",
    "This test is to confirm that an administrator can set a role's gate/station claim "
    "(StationAdmin, TransitGuard, SystemSupervisor, StationSupervisor, Admin).",
    "**GIVEN** an administrator is signed into CloudFare",
    [{
        "content": ("**WHEN** the administrator sets a role's gate/station claim (StationAdmin, "
                    "TransitGuard, SystemSupervisor, StationSupervisor or Admin)"),
        "expected": "**THEN** the role's gate/station access matches the configured claim",
    }],
    "A role's gate/station claim matches the administrator's configuration." +
    TAG.format(auto="Yes", check="CloudFare"),
    "FBD-100342",
)


# ------------------------------------------------------------------ #
# C. C4104258 — Fares export: 5 export-scope variants (file format XLSX/CSV kept in-case,
#    same treatment as "export format PDF/XLS/CSV" in the 30279 EMV/Retail Debt Report split)
# ------------------------------------------------------------------ #
SEC_258 = 887866
SCOPES = ["standard fares list", "ABT Fares export", "Route Attributes", "Area/Zone overlays",
          "single-file export"]
FARES_REFS = "FBD-100385 para 157-159,FBD-100336,FBD-100296 para 241,OldSuite-C2828485,OldSuite-C2828486,OldSuite-C2925143"
for scope in SCOPES:
    title = f"Fares export — {scope} is exported"
    preface = f"This test is to confirm the user can export the {scope} from CloudFare."
    preconds = ("**GIVEN** the user is signed into CloudFare\n"
                "**AND** routes with a shared Service Group have fares configured (e.g. routes "
                "sharing one service group)")
    steps = [{
        "content": f"**WHEN** the user runs the fares export for the {scope} (XLSX or CSV)",
        "expected": ("**THEN** the fares file is produced\n"
                     "**AND** **UNCONFIRMED** — the export surface/parameters are not confirmed; "
                     "confirm live"),
    }]
    expected = (f"The {scope} for the selected operator is exported (XLSX or CSV)." +
                TAG.format(auto="Yes", check="CloudFare"))
    if scope == "standard fares list":
        add_primary(4104258, title, preface, preconds, steps, expected, FARES_REFS)
    else:
        add_new(SEC_258, title, preface, preconds, steps, expected, FARES_REFS)


# ------------------------------------------------------------------ #
def main():
    (OUT / "bos-variant-expansion-30287.rewrite.json").write_text(
        json.dumps(rewrite_rows, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (OUT / "bos-variant-expansion-30287.new-cases.json").write_text(
        json.dumps(new_rows, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"Built {len(rewrite_rows)} primary-case updates + {len(new_rows)} new cases.")


if __name__ == "__main__":
    main()
