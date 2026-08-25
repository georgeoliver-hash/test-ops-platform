"""Enrich TestRail cases with priority, estimate, automatable and cross-system flags.

Judged from each case's title/section/steps. Sets NATIVE priority_id + estimate, custom_automation_type
(2=Robot Framework=automatable, 0=None=manual-only), and (for cross-system tests) a custom_notes
"Cross-check: ..." flag. Does NOT touch custom_devtypes (BOS internal id ambiguous; avoid clobbering
the device type).

    python tools/enrich_cases.py --suite 30255            # dry-run: print judged values, no writes
    python tools/enrich_cases.py --suite 30255 --sample 12 # dry-run, first 12 only
    python tools/enrich_cases.py --suite 30255 --apply     # write to TestRail
"""
from __future__ import annotations

import argparse
import re

from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter

PRIO_HIGH, PRIO_NORMAL, PRIO_LOW = 1, 3, 4  # TestRail priority_id

HIGH = re.compile(r"payment|cash|\bcard\b|emv|cemv|top[- ]?up|topup|validat|annul|refund|sign[ -]?on|"
                  r"sign[ -]?off|signon|lock|auto sign|audit|cloudfare|\bbos\b|merit|transaction|"
                  r"deny list|bin list|pilot list|issue a|issue card|ticket issue|issue from blank|"
                  r"\bcomms\b|\btms\b|deploy|revenue|capping|fatal|freeze|hang|crash|recover|"
                  r"power interrupt|fare", re.I)
LOW = re.compile(r"screen validation|matches the (approved )?design|cosmetic|\bicon\b|banner|layout|"
                 r"alignment|gr[ae]yed|version page|software version|configuration version|serial number|"
                 r"brightness|volume|favourite|display settings|info screen|\btext\b", re.I)
# Automation tier (George 2026-06-11, Appium now available on POS): three-way.
#  No      = leave to a human eye / hardware rig — per-screen HMI visual checks, performance/timing,
#            power interruption + reboot recovery, brightness/audio/LED, DST, firmware/FEIG OTA.
#  Partial = the UI flow is Appium-automatable but a step needs a hardware fixture or human eye —
#            presenting/tapping a card, scanning a barcode, printing/receipt, cash, MIFARE/DESFire.
#  Yes     = fully software via Appium/ADB — sign-on PIN, navigation, fare look-up, menus, config,
#            force-comms, version pages, lockout logic, comms resilience.
TIER_NONE = re.compile(r"screen validation|matches the (approved )?design|\bhmi\b|per-screen|"
                       r"performance|timing|throughput|reconcil|power interrupt|power (is )?restored|"
                       r"recovers? to service|\breboot|brightness|\baudio\b|\bled\b|audible|"
                       r"daylight saving|\bdst\b|firmware|\bfeig\b|\bota\b|hardware", re.I)
TIER_PARTIAL = re.compile(r"present|\bcard\b|smartcard|barcode|\btap\b|contactless|validat|passback|"
                          r"annul|\bissue\b|top[- ]?up|payment|\bcash\b|\bemv\b|cemv|print|printout|"
                          r"receipt|paper|hotlist|faulty card|mifare|desfire|machine not in service|"
                          r"passenger display", re.I)
# Cross-system is judged by what the test DOES (confirmed routing 2026-06-09):
#  smartcard validate/top-up/issue/hotlist/passback -> CloudFare + MERIT + SmartTrack
#  ABT/cEMV tap                                      -> CloudFare + MERIT
#  ticket issue / cash or card payment / annul       -> CloudFare + MERIT
#  sign-on/off, comms, config/TMS, software dist, audit -> CloudFare
#  pure UI / menu / version / screen render          -> none
SC_PRODUCT = re.compile(r"smartcard|concession|half[- ]?fare|daylink|travelcard|multi[- ]?journey|"
                        r"ilink|alink|ylink|belfast visitor|smartpass|employee|dependents|staff pass|"
                        r"ea (bus|rail|pupil|further)", re.I)
SC_TXN = re.compile(r"validat|top[- ]?up|\bissue\b|present|\btap\b|hotlist|passback", re.I)
ABT_RX = re.compile(r"\babt\b|cemv|contactless|open payment|\bemv\b", re.I)
PAY_RX = re.compile(r"ticket issue|issue a |issue from blank|issue card|annul|\bcash\b|card payment|"
                    r"take payment|excess ticket|promo|warrant|group ticket", re.I)
COMMS_RX = re.compile(r"sign[ -]?on|sign[ -]?off|signon|\bcomms\b|force comm|\btms\b|deploy|"
                      r"configuration (download|file|version)|software (version|update|deploy|distribution)|"
                      r"\bfeig\b|deny list|bin list|pilot list|heartbeat|upload|distribution|cloudfare|"
                      r"\bbos\b|back[- ]?office|audit", re.I)


SYS_RX = {"CloudFare": re.compile(r"cloudfare", re.I),
          "MERIT": re.compile(r"\bmerit\b", re.I),
          "SmartTrack": re.compile(r"smart ?track", re.I)}
ORDER = ["CloudFare", "MERIT", "SmartTrack"]


def explicit_systems(blob: str) -> list[str]:
    """Systems the case ALREADY names in its body/audit-event line — authoritative, so the
    Cross-check tag mirrors exactly what the test asserts."""
    return [s for s in ORDER if SYS_RX[s].search(blob)]


def cross_systems(blob: str, is_hmi: bool) -> list[str]:
    if is_hmi:
        return []
    named = explicit_systems(blob)
    if named:
        return named
    s: set[str] = set()
    if SC_PRODUCT.search(blob) and SC_TXN.search(blob):
        s |= {"CloudFare", "MERIT", "SmartTrack"}
    if ABT_RX.search(blob):
        s |= {"CloudFare", "MERIT"}
    if PAY_RX.search(blob):
        s |= {"CloudFare", "MERIT"}
    if COMMS_RX.search(blob):
        s |= {"CloudFare"}
    order = ["CloudFare", "MERIT", "SmartTrack"]
    return sorted(s, key=order.index)


def case_text(c: dict) -> tuple[str, int]:
    parts = [c.get("title") or "", c.get("custom_preface") or "", c.get("custom_expected") or ""]
    rows = c.get("custom_steps_seperated") or []
    for r in rows:
        if isinstance(r, dict):
            parts += [r.get("content") or "", r.get("expected") or ""]
    return "\n".join(parts), len([r for r in rows if isinstance(r, dict)])


def judge(c: dict, section_path: str) -> dict:
    text, nsteps = case_text(c)
    blob = (section_path + "\n" + text)
    is_hmi = "HMI Screen Validation" in section_path or "Screen Validation" in section_path
    is_smoke = section_path.split(" / ")[0].strip().lower() == "smoke"

    # priority
    if is_hmi:
        prio = PRIO_LOW
    elif is_smoke or HIGH.search(blob):
        prio = PRIO_HIGH
    elif LOW.search(blob):
        prio = PRIO_LOW
    else:
        prio = PRIO_NORMAL

    # cross-system (behaviour-based)
    systems = cross_systems(blob, is_hmi)

    # estimate (manual minutes)
    if is_hmi:
        mins = 1
    else:
        mins = {0: 1, 1: 1, 2: 2, 3: 3, 4: 4}.get(nsteps, 5 if nsteps <= 6 else (8 if nsteps <= 8 else 10))
        if re.search(r"sign[ -]?on|payment|issue|top[- ]?up", blob, re.I):
            mins += 2
        if systems:
            mins += 3                      # back-office reconciliation adds time
            if len(systems) >= 3:
                mins += 2                  # 3-system (smartcard) verification
        mins = min(mins, 15)

    # automation tier
    if is_hmi or TIER_NONE.search(blob):
        tier = "No"
    elif TIER_PARTIAL.search(blob):
        tier = "Partial"
    else:
        tier = "Yes"

    return {"priority_id": prio, "estimate": f"{mins}m",
            "automation_tier": tier, "_systems": systems}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", type=int, required=True)
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--missing-only", action="store_true",
                    help="only enrich cases that lack an estimate OR an [Automatable: ...] tag; "
                         "leaves already-enriched cases untouched (additive, non-clobbering).")
    args = ap.parse_args(argv)

    client = TestRailClient()
    secs = {s["id"]: s for s in client.get_sections(42, args.suite)}

    def path(sid):
        p = []; cur = secs.get(sid)
        while cur:
            p.append(cur["name"]); cur = secs.get(cur.get("parent_id"))
        return " / ".join(reversed(p))

    cases = [c for c in client.get_cases(42, args.suite) if not str(c.get("title", "")).startswith("ZZ_DELETE")]
    if args.missing_only:
        _tag = re.compile(r"\[Automatable:\s*(Yes|Partial|No)\b", re.I)
        cases = [c for c in cases
                 if not c.get("estimate") or not _tag.search(c.get("custom_expected") or "")]
        print(f"--missing-only: {len(cases)} case(s) lack an estimate or Automatable tag.")
    writer = TestRailWriter(client, 42, args.suite, commit=True) if args.apply else None
    shown = 0
    PRN = {1: "High", 3: "Normal", 4: "Low"}
    for c in cases:
        j = judge(c, path(c["section_id"]))
        # custom_automation_type / custom_notes / custom_automation_script aren't persisted for
        # project 42's template, so the automation tier (Yes/Partial/No) + cross-system flag is
        # appended as a tag line on the Expected (custom_expected) prose. Idempotent: strip prior.
        tag = f"[Automatable: {j['automation_tier']}"
        if j["_systems"]:
            tag += " · Cross-check: " + " / ".join(j["_systems"])
        tag += "]"
        base = re.sub(r"\s*\[Automatable:[^\]]*\]\s*$", "", c.get("custom_expected") or "").rstrip()
        expected = (base + "\n\n" + tag) if base else tag
        fields = {"priority_id": j["priority_id"], "estimate": j["estimate"],
                  "custom_expected": expected}
        if args.apply:
            writer.update_case_fields(int(c["id"]), fields, section_id=c.get("section_id"))
        elif args.sample == 0 or shown < args.sample:
            print("P=%-6s est=%-4s auto=%-7s %-10s | %s" % (
                PRN[j["priority_id"]], j["estimate"], j["automation_tier"],
                ("[" + ",".join(j["_systems"]) + "]") if j["_systems"] else "",
                (c.get("title") or "")[:60]))
            shown += 1
    if args.apply:
        print(f"Applied enrichment to {len(cases)} cases in suite {args.suite}.")
    else:
        print(f"\n(dry-run; {len(cases)} cases in suite {args.suite}. Add --apply to write.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
