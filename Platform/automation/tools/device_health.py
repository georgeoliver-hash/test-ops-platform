"""Ping every device in every project's registry; report reachable/unreachable.

Usage:
  python -m tools.device_health
  python -m tools.device_health translink
"""
from __future__ import annotations

import sys

from framework.registry.loader import list_projects, load_project
from framework.registry.models import ADBTransport, SSHTransport
from framework.transport.adb import ADBTransportImpl
from framework.transport.ssh import SSHTransportImpl


def check(transport) -> tuple[bool, str]:
    try:
        transport.connect()
    except Exception as e:
        return False, str(e)
    try:
        result = transport.run("echo ok", timeout=5)
        return result.ok, (result.stdout.strip() or result.stderr.strip())
    except Exception as e:
        return False, str(e)
    finally:
        try:
            transport.disconnect()
        except Exception:
            pass


def main(argv: list[str]) -> int:
    names = argv[1:] or list_projects()
    if not names:
        print("No projects with a devices.yaml found.")
        return 1
    for name in names:
        proj = load_project(name)
        print(f"\n[{proj.project}]")
        for d in proj.devices:
            if isinstance(d.transport, SSHTransport):
                t = SSHTransportImpl(d.transport)
            elif isinstance(d.transport, ADBTransport):
                t = ADBTransportImpl(d.transport)
            else:
                print(f"  {d.id}: unknown transport")
                continue
            ok, info = check(t)
            mark = "OK  " if ok else "FAIL"
            print(f"  [{mark}] {d.id} ({d.type.value}/{d.os.value}) — {info}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
