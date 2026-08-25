"""Thin shim — the suite linter now lives in the package and the CLI.

Prefer:  python -m system_test_ops audit [--suite <id>]

This wrapper just forwards to that command so older docs/links keep working.
"""
import sys

from system_test_ops.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["audit", *sys.argv[1:]]))
