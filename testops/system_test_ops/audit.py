"""Standard-conformance audit for a TestRail suite — reusable for ANY project/device.

Audits every case in a suite against ``docs/gherkin-standard.md`` + the case-format rules and
returns structured findings. Read-only: this module never mutates TestRail.

Two classes of finding:
  * **blocking** — a real deviation from the standard that should be fixed (mojibake, missing
    objective/preconds, malformed When/Then, genuine compound THEN, stray tags, ...).
  * **advisory** — reviewed-intentional style items (see ``ADVISORY``): title length and the
    em-dash separator, which are sometimes deliberately broken (e.g. Screen Validation titles that
    mirror an exact UI screen name, or bare product names under a section). Reported, never gating.

The CLI surfaces this as ``python -m system_test_ops audit`` and ``push --commit`` runs it
automatically on the target suite so no authoring happens without a conformance read-out.
"""

from __future__ import annotations

import re
from collections import defaultdict

TAG_RE = re.compile(r"@(project|device|mode|feature|regression)\b", re.I)
MOJI_RE = re.compile(r"Ã|â‚|â€|Â")
# After 'and', a token that signals a *second predicate* (a genuine second outcome) rather than a
# noun list belonging to a single observable assertion.
SECOND_OUTCOME = re.compile(
    r"\band\b\s+(is|are|its?|the|a|an|pressing|success|it|they|print|prints|printed|printing|"
    r"shown|show|shows|added|retained|reported|completes?|completed|issued|recorded|cleared|read|"
    r"calculated|displayed|applied|updated|accepted|removed|corrected|written|dismissed)\b",
    re.I,
)

# Order + human description of every rule. Keys in ADVISORY are non-gating.
ORDER: list[tuple[str, str]] = [
    ("mojibake", "Residual mojibake in any field"),
    ("title-no-emdash", "Title missing the ' - ' feature separator"),
    ("title-too-long", "Title over 72 chars"),
    ("preface-empty", "Objective/preface empty"),
    ("preface-bad-preamble", "Objective not starting 'This test is to confirm'"),
    ("preconds-empty", "Preconditions empty"),
    ("preconds-no-given", "Preconditions without a GIVEN"),
    ("steps-empty", "No When/Then steps at all"),
    ("step-first-not-when", "First step is not a WHEN"),
    ("step-content-not-when-and", "Step content not WHEN/AND"),
    ("step-no-then", "A WHEN with no THEN outcome"),
    ("then-compound-genuine", "Genuine compound THEN (two distinct outcomes) - should split"),
    ("expected-empty", "Expected (prose) empty"),
    ("expected-starts-then", "Expected starts with THEN (should be prose)"),
    ("has-tags", "Tags (@project/@device/...) written into the case"),
]
ADVISORY = {"title-no-emdash", "title-too-long"}

# Cases whose title carries this prefix are housekeeping (flagged for binning — duplicates or
# review-driven removals) and are excluded from conformance counts.
SKIP_TITLE_PREFIX = "ZZ_DELETE"


def steprows(case: dict) -> list:
    s = case.get("custom_steps_seperated")
    return s if isinstance(s, list) else []


def _alltext(case: dict) -> str:
    parts = [case.get(f) or "" for f in ("title", "custom_preface", "custom_preconds", "custom_expected")]
    for r in steprows(case):
        if isinstance(r, dict):
            parts += [r.get("content") or "", r.get("expected") or ""]
    return "\n".join(parts)


def genuine_compound_then(expected_text: str) -> list[str]:
    """THEN clauses that bundle two *distinct outcomes* inline with 'and' (split-worthy).

    Parenthetical 'and' and plain noun lists are not flagged — that is valid declarative Gherkin.
    """
    out: list[str] = []
    for line in expected_text.splitlines():
        m = re.match(r"^\*\*THEN\*\*\s*(.*)", line.strip(), re.I)
        if not m:
            continue
        clause = m.group(1).strip()
        bare = re.sub(r"\([^)]*\)", "", clause)  # drop parenthetical 'and'
        if " and " in bare.lower() and SECOND_OUTCOME.search(bare):
            out.append(clause)
    return out


def audit_cases(cases: list[dict]) -> dict[str, list[tuple[int, str, str]]]:
    """Return {rule_key: [(case_id, title, detail), ...]} for the given cases."""
    V: dict[str, list] = defaultdict(list)
    for k in cases:
        if str(k.get("title", "")).startswith(SKIP_TITLE_PREFIX):
            continue
        cid, title = k["id"], k["title"]
        preface = (k.get("custom_preface") or "").strip()
        preconds = (k.get("custom_preconds") or "").strip()
        expected = (k.get("custom_expected") or "").strip()
        rows = steprows(k)

        if "—" not in title:
            V["title-no-emdash"].append((cid, title, ""))
        if len(title) > 72:
            V["title-too-long"].append((cid, title, f"{len(title)} chars"))

        if not preface:
            V["preface-empty"].append((cid, title, ""))
        elif not re.match(r'["\']?This test is to confirm', preface, re.I):
            V["preface-bad-preamble"].append((cid, title, preface[:70]))

        if not preconds:
            V["preconds-empty"].append((cid, title, ""))
        elif "GIVEN" not in preconds.upper():
            V["preconds-no-given"].append((cid, title, preconds[:70]))

        if not rows:
            V["steps-empty"].append((cid, title, ""))
        for i, r in enumerate(rows):
            if not isinstance(r, dict):
                continue
            content = (r.get("content") or "").strip()
            exp = (r.get("expected") or "").strip()
            cu = content.upper()
            if i == 0 and not cu.startswith("**WHEN**"):
                V["step-first-not-when"].append((cid, title, content[:60]))
            if not (cu.startswith("**WHEN**") or cu.startswith("**AND**")):
                V["step-content-not-when-and"].append((cid, title, content[:60]))
            if "THEN" not in exp.upper():
                V["step-no-then"].append((cid, title, content[:60]))
            for clause in genuine_compound_then(exp):
                V["then-compound-genuine"].append((cid, title, clause[:70]))

        if not expected:
            V["expected-empty"].append((cid, title, ""))
        elif re.match(r"\*?\*?THEN", expected, re.I):
            V["expected-starts-then"].append((cid, title, expected[:60]))

        if TAG_RE.search(_alltext(k)):
            V["has-tags"].append((cid, title, ""))
        if MOJI_RE.search(_alltext(k)):
            V["mojibake"].append((cid, title, ""))
    return V


def summarize(findings: dict[str, list]) -> tuple[int, int]:
    """Return (blocking_count, advisory_count)."""
    blocking = sum(len(v) for key, v in findings.items() if key not in ADVISORY)
    advisory = sum(len(v) for key, v in findings.items() if key in ADVISORY)
    return blocking, advisory


def render_report(suite_id: int, cases_count: int, findings: dict[str, list]) -> str:
    blocking, advisory = summarize(findings)
    lines = [
        f"# Alignment audit - suite {suite_id}",
        "",
        f"- Cases audited: **{cases_count}**",
        f"- Blocking findings: **{blocking}**",
        f"- Advisory (reviewed-intentional) findings: **{advisory}**",
        "",
    ]
    for key, desc in ORDER:
        items = findings.get(key, [])
        tag = " _(advisory)_" if key in ADVISORY else ""
        lines.append(f"## {desc}{tag} - {len(items)}")
        if not items:
            lines.append("_none_\n")
            continue
        for cid, title, detail in items[:300]:
            d = f" - {detail}" if detail else ""
            lines.append(f"- C{cid} | {title}{d}")
        lines.append("")
    return "\n".join(lines)
