"""Append back-office (BOS activity log / MERIT / SmartTrack) verification STEPS to transactional cases.

George's catch (2026-06-11, running ETM): many cases assert the on-device outcome but have no
explicit back-office verification STEP to perform during a run — and where they do, they often name
CloudFare but not MERIT/SmartTrack. The old ETM suite (4943) phrases these as discrete WHEN/THEN
steps: "WHEN the CloudFare activity log is checked / THEN the event is recorded in the Back Office
System", "WHEN the data is reviewed in MERIT / THEN the transaction appears in MERIT".

This appends those steps to the live cases, idempotently (skips a system already verified), routed by
behaviour. Read-judged, write via the guarded writer. Mirrors tools/enrich_cases.py.

    python tools/add_audit_steps.py --suite 30254              # dry-run: show routing + what'd be added
    python tools/add_audit_steps.py --suite 30254 --sample 20  # dry-run, first 20
    python tools/add_audit_steps.py --suite 30254 --apply      # write

Routing (grounded in old-suite evidence + confirmed cross-system rules):
  smartcard validate/top-up/passback/hotlist  -> activity log + MERIT + SmartTrack
  ABT/cEMV tap, barcode validation            -> activity log + MERIT
  ticket issue / sale / top-up / annul / capping/ basket pay -> activity log + MERIT
  sign-on/off, break, lockout, comms, software/config dist, revenue limit, deny/BIN, time change,
      defects, commissioning                  -> activity log only
  pure UI / read (navigate, select, version view, waybill view, basket limit, GPS, idle) -> none
"""
from __future__ import annotations

import argparse
import re

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

# --- behaviour detection -------------------------------------------------- #
SMARTCARD = re.compile(r"smartcard|smartpass|concession|daylink|travelcard|multi[- ]?journey|\bilink\b|"
                       r"\balink\b|\bylink\b|belfast visitor|half[- ]?fare|24\+|employee|dependants|"
                       r"staff pass|passback|hotlist", re.I)
SC_ACTION = re.compile(r"validat|present|\btap\b|top[- ]?up|passback|hotlist", re.I)
ABT = re.compile(r"\babt\b|cemv|contactless|\bemv\b|payment card|tap on", re.I)
BARCODE_VAL = re.compile(r"barcode.*(validat|scan|reference)|(validat|scan).*barcode|mlink", re.I)
REVENUE = re.compile(r"\bissue\b|ticket (issue|sale|print)|sell a ticket|take payment|basket|"
                     r"top[- ]?up|annul|capping|\bcap\b|excess|warrant|promo", re.I)
# Sign-on/off + device/admin/comms events -> activity log ONLY (authentication or an event, no fare;
# a STAFF smartcard sign-on is not a fare validation, so no MERIT/SmartTrack). Checked before the
# fare rules so "Sign On - Smartcard" doesn't mis-route to the smartcard-fare bucket.
ACTIVITY_FIRST = re.compile(r"sign[ -]?on|sign[ -]?off|sign on|sign off|\bbreak\b|lock(s|ed|out)?|"
                            r"communicat|\bcomms\b|software (dist|update|deploy)|"
                            r"config(uration)?( files)? (dist|download|update)|download configuration|"
                            r"fare[- ]?mode|revenue limit|deny|bin list|pilot list|time change|\bgmt\b|"
                            r"\bbst\b|defect|de?commission|reboot|heartbeat|waybill|power (loss|interrupt|"
                            r"restore)|sequence id|sustained use", re.I)
# No completed transaction -> activity log only (cancel/abandon/availability checks).
ACTIVITY_ONLY2 = re.compile(r"cancel|abandon|availability|not available", re.I)
# Pure UI / read / perf-timing — never fires a back-office record. Checked FIRST.
NO_EVENT = re.compile(r"screen validation|matches the (approved )?design|navigat|select products|"
                      r"ticket type selection|view (and print )?versions?|historic waybills|"
                      r"line-item quantity|idle timeout|topology and fares data present|"
                      r"\bgps\b|brightness|\baudio\b|\bled\b|paper|printer (jam|error)|display|"
                      r"\btiming(s)?\b|transaction timings", re.I)

# --- the verification steps (old-suite phrasing) -------------------------- #
ROW_ACTIVITY = {"content": "**WHEN** the CloudFare activity log is checked",
                "expected": "**THEN** the corresponding event is recorded in the Back Office System (CloudFare) activity log"}
ROW_MERIT = {"content": "**WHEN** the data is reviewed in MERIT",
             "expected": "**THEN** the transaction appears in MERIT"}
ROW_SMARTTRACK = {"content": "**WHEN** the smartcard record is reviewed in SmartTrack",
                  "expected": "**THEN** the updated smartcard record appears in SmartTrack"}


def route(blob: str) -> list[str]:
    """Return the systems this behaviour records to (ordered), or [] if none. Precedence matters."""
    if NO_EVENT.search(blob) and not re.search(r"sign[ -]?off|sign[ -]?on", blob, re.I):
        return []
    if ACTIVITY_FIRST.search(blob):          # sign-on/off + device/admin/comms events -> activity only
        return ["activity"]
    if ACTIVITY_ONLY2.search(blob):          # cancel / abandon / availability -> no completed txn
        return ["activity"]
    if BARCODE_VAL.search(blob):             # barcode (may mention 'smartcard') -> activity + MERIT
        return ["activity", "merit"]
    if ABT.search(blob):                     # ABT/cEMV tap -> activity + MERIT (never SmartTrack)
        return ["activity", "merit"]
    if SMARTCARD.search(blob) and SC_ACTION.search(blob):   # smartcard FARE op -> all three
        return ["activity", "merit", "smarttrack"]
    if REVENUE.search(blob):                 # ticket issue / sale / capping -> activity + MERIT
        return ["activity", "merit"]
    return []


def case_blob(c: dict, section_path: str) -> str:
    parts = [section_path, c.get("title", ""), c.get("custom_preface") or "", c.get("custom_expected") or ""]
    for r in (c.get("custom_steps_seperated") or []):
        if isinstance(r, dict):
            parts += [r.get("content", "") or "", r.get("expected", "") or ""]
    return "\n".join(parts)


def existing_systems(c: dict) -> set[str]:
    """Which back-office systems the case already verifies AS A STEP (so we don't duplicate).

    Scans only the step rows — NOT custom_expected, because that holds the inline
    '[Automatable · Cross-check: …]' tag and prose, which is not an executable verification step.
    A case whose only back-office mention is that tag will (correctly) be treated as missing the
    step and get one added.
    """
    blob = ""
    for r in (c.get("custom_steps_seperated") or []):
        if isinstance(r, dict):
            blob += " " + (r.get("content", "") or "") + " " + (r.get("expected", "") or "")
    have = set()
    if re.search(r"activity log|cloudfare|back office", blob, re.I):
        have.add("activity")
    if re.search(r"\bmerit\b", blob, re.I):
        have.add("merit")
    if re.search(r"smart\s?track", blob, re.I):
        have.add("smarttrack")
    return have


ROWS = {"activity": ROW_ACTIVITY, "merit": ROW_MERIT, "smarttrack": ROW_SMARTTRACK}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", type=int, required=True)
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    client = TestRailClient()
    secs = {s["id"]: s for s in client.get_sections(42, args.suite)}

    def path(sid):
        p = []; cur = secs.get(sid)
        while cur:
            p.append(cur["name"]); cur = secs.get(cur.get("parent_id"))
        return " / ".join(reversed(p))

    cases = [c for c in client.get_cases(42, args.suite) if not str(c.get("title", "")).startswith("ZZ_DELETE")]
    writer = TestRailWriter(client, 42, args.suite, commit=True) if args.apply else None
    shown = 0
    n_changed = 0
    for c in cases:
        sp = path(c["section_id"])
        # Skip HMI per-screen checks and the thin Smoke path (smoke stays a quick device-only check).
        if "Screen Validation" in sp or sp.split(" / ")[0] in ("HMI", "Smoke"):
            continue
        want = route(case_blob(c, sp))
        if not want:
            continue
        have = existing_systems(c)
        add = [s for s in want if s not in have]
        if not add:
            continue
        n_changed += 1
        rows = list(c.get("custom_steps_seperated") or [])
        rows += [ROWS[s] for s in add]
        if args.apply:
            writer.update_case_fields(int(c["id"]), {"custom_steps_seperated": rows}, section_id=c.get("section_id"))
        elif args.sample == 0 or shown < args.sample:
            print("  +%-22s %-26s | %s" % ("/".join(add), sp.split(" / ")[-1][:26], (c.get("title") or "")[:46]))
            shown += 1
    if args.apply:
        print(f"Added back-office verification steps to {n_changed} cases in suite {args.suite}.")
    else:
        print(f"\n(dry-run; {n_changed} cases would gain steps in suite {args.suite}. Add --apply to write.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
