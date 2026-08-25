"""Apply spec-grounded rewrite proposals to existing cases, in place, by id.

Reads one or more `*.rewrite.json` files (array of {id,title,preface,preconds,steps,action,...})
and updates title + custom_preface + custom_preconds + custom_steps_seperated via the guarded,
suite-locked writer. action=remove -> ZZ_DELETE_REVIEW title prefix (not a hard delete).

--reframe-fares rewrites the "fare/cap value from the UB-TOO tracker … (gap Q14)" UNCONFIRMED
markers (values are back-end configurable per George) into a runnable note, leaving CR122 and
other UNCONFIRMED markers intact.

Step schema: each entry in `steps` may be written either as
  {"content": "**WHEN** ...", "expected": "**THEN** ... \n**AND** ..."}   (the real TestRail
  `custom_steps_seperated` shape), or as
  {"when": "...", "then": ["...", "..."]}                                (a shorthand some
  proposal batches used).
Both are normalised to {"content", "expected"} before pushing. `{"when","then"}` is turned into
Gherkin-marked text: "content" becomes "**WHEN** <when>" and "expected" becomes "**THEN** <then[0]>"
followed by "\n**AND** <then[i]>" for each subsequent item — unless the source text already starts
with a **WHEN**/**THEN**/**AND** marker, in which case it is used as-is (no double-marking).

Hard guard: after building `custom_steps_seperated`, every step's `content` and `expected` must be
non-empty. If any is blank, the case is refused (printed as an error) and NOT pushed — this is the
defence against the 2026-07-17 bug where a schema mismatch silently produced blank step rows.

Usage:
  set TESTRAIL_WRITE_SUITE_ID=<suite id>
  python tools/apply_rewrite.py <file.rewrite.json> [...] [--reframe-fares] [--commit]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from system_test_ops.testrail.client import TestRailClient
from system_test_ops.testrail.writer import TestRailWriter, load_write_suite_id

FARE_MARK = re.compile(r"\s*[—-]\s*\*\*UNCONFIRMED\*\*[^\n]*?\(gap Q14\)\.?")
FARE_NOTE = (" — *example per current ABT pricing config (back-end configurable); "
             "verify the charge matches the configured ABT pricing rule*")

MARKERS = ("**WHEN**", "**THEN**", "**AND**")

def reframe(text):
    return FARE_MARK.sub(FARE_NOTE, text) if text else text

def _marked(text: str) -> bool:
    return text.strip().startswith(MARKERS)

def normalize_step(s: dict) -> dict:
    """Normalise one step dict into the real {"content","expected"} schema.

    Accepts either the native {"content","expected"} shape or the {"when","then"} shorthand.
    Never invents wording — only adds the Gherkin **WHEN**/**THEN**/**AND** markers when the
    source text doesn't already carry one.
    """
    if "content" in s or "expected" in s:
        return {"content": s.get("content") or "", "expected": s.get("expected") or ""}

    when = s.get("when") or ""
    then = s.get("then")
    if then is None:
        then = []
    elif isinstance(then, str):
        then = [then]

    content = when if _marked(when) else (f"**WHEN** {when}" if when else "")

    lines = []
    for i, t in enumerate(then):
        t = t or ""
        if not t:
            continue
        if _marked(t):
            lines.append(t)
        else:
            lines.append(f"{'**THEN**' if i == 0 else '**AND**'} {t}")
    expected = "\n".join(lines)

    return {"content": content, "expected": expected}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--project", type=int, default=42)
    ap.add_argument("--reframe-fares", action="store_true")
    ap.add_argument("--commit", action="store_true")
    a = ap.parse_args()
    suite = load_write_suite_id()
    if suite is None:
        print("error: TESTRAIL_WRITE_SUITE_ID not set", file=sys.stderr); return 2
    client = TestRailClient()
    writer = TestRailWriter(client, a.project, suite, commit=a.commit)
    by_id = {int(c["id"]): c for c in client.get_cases(a.project, suite)}
    print(f"[{'COMMIT' if a.commit else 'DRY-RUN'}] apply rewrite -> suite {suite}")
    upd = removed = missing = skip = fares = 0
    for fp in a.files:
        doc = json.loads(Path(fp).read_text(encoding="utf-8"))
        rows = doc.get("cases", []) if isinstance(doc, dict) else doc
        for r in rows:
            if not isinstance(r, dict):
                continue
            cid = int(r["id"]); ex = by_id.get(cid)
            if not ex:
                missing += 1; print(f"  MISSING C{cid}"); continue
            if r.get("action") == "remove":
                title = ex.get("title","")
                if not title.upper().startswith("ZZ_DELETE"):
                    writer.update_case_fields(cid, {"title": f"ZZ_DELETE_REVIEW - {title}"}, section_id=ex.get("section_id"))
                    removed += 1
                continue
            def _s(v):
                if v is None: return ""
                if isinstance(v, list): return "\n".join(str(x) for x in v)
                return str(v)
            preface = _s(r.get("preface")); preconds = _s(r.get("preconds")); expected = _s(r.get("expected"))
            raw_steps = r.get("steps") or []
            raw_steps = [s for s in raw_steps if isinstance(s, dict)]
            steps = [normalize_step(s) for s in raw_steps]
            if a.reframe_fares:
                before = preface + preconds + json.dumps(steps)
                preface, preconds = reframe(preface), reframe(preconds)
                steps = [{"content": reframe(s.get("content","")), "expected": reframe(s.get("expected",""))} for s in steps]
                if FARE_NOTE in (preface+preconds+json.dumps(steps)) and "gap Q14" in before:
                    fares += 1
            extra = {}
            if r.get("title"): extra["title"] = r["title"]
            if preface: extra["custom_preface"] = preface
            if preconds: extra["custom_preconds"] = preconds
            if expected: extra["custom_expected"] = expected
            if steps: extra["custom_steps_seperated"] = steps
            if r.get("refs"):
                rv = r["refs"]
                extra["refs"] = rv if isinstance(rv, str) else ",".join(rv)
            if not extra:
                skip += 1; continue
            # Hard guard: never silently push a step row with blank content/expected. This is the
            # defence against the 2026-07-17 bug (a {"when","then"} source file pushed with the
            # writer expecting {"content","expected"} -> every step row came out empty).
            if "custom_steps_seperated" in extra:
                bad = [
                    i for i, s in enumerate(extra["custom_steps_seperated"])
                    if not (s.get("content") or "").strip() or not (s.get("expected") or "").strip()
                ]
                if bad:
                    print(f"  REFUSED C{cid}: blank content/expected in step(s) {bad} after normalisation "
                          f"— not pushed. Fix the source proposal, do not push blanks.", file=sys.stderr)
                    skip += 1
                    continue
            writer.update_case_fields(cid, extra, section_id=ex.get("section_id"))
            upd += 1
    print(f"  updated: {upd}  removed(ZZ): {removed}  fare-reframed: {fares}  skipped: {skip}  missing: {missing}")
    if not a.commit: print("  (dry-run)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
