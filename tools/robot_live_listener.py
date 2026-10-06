"""Robot Framework listener: appends one JSON line per event, flushed at once, so the console can show a run
as it happens (output.xml is buffered by Robot and only complete at the end).

Use (no change to any test):
    robot --listener tools/robot_live_listener.py:<results folder>/live-events.jsonl  Tests/POS
or set TOPS_LIVE_EVENTS=<file> and pass --listener tools/robot_live_listener.py
Point the console's Live results folder at <results folder>.
"""
import json
import os
import time

ROBOT_LISTENER_API_VERSION = 2


class robot_live_listener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, path=None):
        self.path = path or os.environ.get("TOPS_LIVE_EVENTS") or "live-events.jsonl"
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        self.f = open(self.path, "a", encoding="utf-8")
        self.suites = []
        self._emit("run_start")

    def _emit(self, ev, **kw):
        self.f.write(json.dumps({"ev": ev, "t": time.time(), **kw}, ensure_ascii=False) + "\n")
        self.f.flush()

    def start_suite(self, name, attrs):
        self.suites.append(name)
        if len(self.suites) == 1:
            self._emit("suite_start", name=name, total=attrs.get("totaltests"))

    def end_suite(self, name, attrs):
        if self.suites:
            self.suites.pop()

    def start_test(self, name, attrs):
        self._emit("test_start", name=name, suite=".".join(self.suites), tags=attrs.get("tags", []))

    def end_test(self, name, attrs):
        self._emit("test_end", name=name, suite=".".join(self.suites), status=attrs.get("status"),
                   message=(attrs.get("message") or "")[:400], seconds=(attrs.get("elapsedtime") or 0) / 1000.0,
                   tags=attrs.get("tags", []))

    def log_message(self, message):
        if message.get("level") in ("INFO", "WARN", "ERROR", "FAIL"):
            self._emit("log", level=message.get("level"), text=(message.get("message") or "")[:400])

    def close(self):
        self._emit("run_end")
        self.f.close()
