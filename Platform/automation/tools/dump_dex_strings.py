"""Dump and categorise string constants from a dex file.

Most ContentProvider schemas (URIs, column names, event types, SQL DDL) live
as string literals in the compiled bytecode. Extracting and bucketing them
gives a usable approximation of the provider contract without needing a real
decompile.

Usage:
    python tools/dump_dex_strings.py <apk-or-dex> -o artifacts/<name>.json [--pattern X] [--filter-class FQCN]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def _silence_androguard() -> None:
    from loguru import logger
    logger.remove()


def _load_dex_bytes(path: Path) -> list[bytes]:
    if path.suffix.lower() == ".dex":
        return [path.read_bytes()]
    if path.suffix.lower() == ".apk":
        from androguard.core.apk import APK
        apk = APK(str(path))
        names = apk.get_dex_names()
        if not names:
            return []
        return [apk.get_file(n) for n in names]
    raise ValueError(f"Unsupported file type: {path.suffix}")


def _bucket(s: str) -> str | None:
    if not (1 <= len(s) <= 200):
        return None
    if s.startswith("content://"):
        return "uri"
    if re.match(r"^[a-z][a-z0-9_.]*\.(changed|done|startup|alarm)$", s):
        return "event_type"
    if re.match(r"^(CREATE TABLE|INSERT INTO|SELECT |UPDATE |DELETE FROM|DROP TABLE)\b", s, re.I):
        return "sql"
    if re.match(r"^/[a-z][a-z0-9_/.\-]*$", s):
        return "config_path"
    if re.match(r"^[a-z_][a-z0-9_]{1,40}$", s) and "_" in s:
        return "snake_case_token"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to .apk or .dex")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--pattern", action="append", default=[],
                        help="Regex to surface as 'matched' bucket (repeatable).")
    parser.add_argument("--filter-class", default=None,
                        help="If set, only include strings appearing inside this class FQCN")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"not a file: {args.input}", file=sys.stderr)
        return 1

    _silence_androguard()
    from androguard.core.dex import DEX

    blobs = _load_dex_bytes(args.input)
    if not blobs:
        print(f"no dex found in {args.input}", file=sys.stderr)
        return 1

    buckets: dict[str, set[str]] = defaultdict(set)
    pattern_hits: dict[str, set[str]] = defaultdict(set)
    compiled_patterns = [(p, re.compile(p)) for p in args.pattern]

    for blob in blobs:
        dex = DEX(blob)
        if args.filter_class:
            target_cls = None
            target_marker = "L" + args.filter_class.replace(".", "/") + ";"
            for cls in dex.get_classes():
                if cls.get_name() == target_marker:
                    target_cls = cls
                    break
            if target_cls is None:
                continue
            seen = set()
            for method in target_cls.get_methods():
                code = method.get_code()
                if code is None:
                    continue
                for ins in code.get_bc().get_instructions():
                    for op in ins.get_operands():
                        if isinstance(op, tuple) and len(op) >= 3 and isinstance(op[2], str):
                            seen.add(op[2])
            string_iter = seen
        else:
            string_iter = (s for s in dex.get_strings())

        for s in string_iter:
            if not isinstance(s, str):
                continue
            bucket = _bucket(s)
            if bucket:
                buckets[bucket].add(s)
            for raw, pat in compiled_patterns:
                if pat.search(s):
                    pattern_hits[raw].add(s)

    output: dict[str, Any] = {"input": str(args.input)}
    if args.filter_class:
        output["filter_class"] = args.filter_class
    output["buckets"] = {k: sorted(v) for k, v in sorted(buckets.items())}
    if pattern_hits:
        output["pattern_hits"] = {k: sorted(v) for k, v in pattern_hits.items()}

    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = ", ".join(f"{k}={len(v)}" for k, v in output["buckets"].items())
    print(f"wrote {args.output} — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
