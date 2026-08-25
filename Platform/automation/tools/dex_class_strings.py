"""Dump string constants used by methods of a specific Java class in a dex.

Class-filtered dex inspection. Walks every method of the target class via
androguard's bytecode analyzer and extracts every `const-string`-loaded
literal — far more reliable than scanning the dex string pool, because the
pool is shared across the whole APK and most of its entries are irrelevant.

Usage:
    python tools/dex_class_strings.py <apk> <fqcn> [-o out.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _silence_androguard() -> None:
    from loguru import logger
    logger.remove()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("fqcn", help="Fully-qualified class name, e.g. com.parkeon.data.ConfigurationHelper")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    if not args.apk.is_file():
        print(f"not a file: {args.apk}", file=sys.stderr)
        return 1

    _silence_androguard()
    from androguard.misc import AnalyzeAPK

    apk, dvm_list, analysis = AnalyzeAPK(str(args.apk))
    descriptor = "L" + args.fqcn.replace(".", "/") + ";"

    out_methods: dict[str, list[str]] = {}
    for cls in analysis.get_classes():
        if cls.name != descriptor:
            continue
        for method_analysis in cls.get_methods():
            method = method_analysis.get_method()
            method_id = f"{method.name}{method.get_descriptor()}"
            literals: list[str] = []
            if not hasattr(method, "get_code"):
                out_methods[method_id] = ["<external>"]
                continue
            code = method.get_code()
            if code is None:
                out_methods[method_id] = []
                continue
            for ins in code.get_bc().get_instructions():
                name = ins.get_name()
                if name not in ("const-string", "const-string/jumbo"):
                    continue
                output = ins.get_output()
                if "'" in output:
                    start = output.index("'") + 1
                    end = output.rindex("'")
                    if end > start:
                        literals.append(output[start:end])
            out_methods[method_id] = literals

    payload = {"apk": str(args.apk), "class": args.fqcn, "methods": out_methods}
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output} — {len(out_methods)} methods, "
              f"{sum(len(v) for v in out_methods.values())} string literals")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
