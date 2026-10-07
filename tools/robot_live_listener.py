"""Robot Framework listener: appends one JSON line per event, flushed at once, so the console can show a run
as it happens (output.xml is buffered by Robot and only complete at the end).

Use (no change to any test):
    robot --listener tools/robot_live_listener.py:<results folder>/live-events.jsonl  Tests/POS
or set TOPS_LIVE_EVENTS=<file> and pass --listener tools/robot_live_listener.py

Push mode (runner and console share no folder): also set TOPS_LIVE_URL=<console>/api/live/ingest and TOPS_LIVE_TOKEN.
Events are posted in small batches from a background thread, keyed by TOPS_LIVE_RUN_ID (default: GITHUB_RUN_ID, then a
timestamp). A failed post is dropped silently: pushing can never fail or slow a test; the file stays the record.
Point the console's Live results folder at <results folder>.
"""
import json
import os
import queue
import threading
import time
import urllib.request

ROBOT_LISTENER_API_VERSION = 2


class robot_live_listener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, path=None):
        self.path = path or os.environ.get("TOPS_LIVE_EVENTS") or "live-events.jsonl"
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        self.f = open(self.path, "a", encoding="utf-8")
        self.suites = []
        self._push_url = os.environ.get("TOPS_LIVE_URL")
        if self._push_url:
            self._run_id = (os.environ.get("TOPS_LIVE_RUN_ID") or os.environ.get("GITHUB_RUN_ID") or str(int(time.time())))
            label = os.environ.get("JOB_LABEL")
            if label:
                self._run_id = f"{label}-{self._run_id}"
            self._q = queue.Queue()
            self._thread = threading.Thread(target=self._pusher, daemon=True)
            self._thread.start()
        self._emit("run_start")

    def _post(self, batch):
        req = urllib.request.Request(
            self._push_url, data=json.dumps({"run_id": self._run_id, "events": batch}).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json", "X-Live-Token": os.environ.get("TOPS_LIVE_TOKEN", "")})
        urllib.request.urlopen(req, timeout=5).read()

    def _pusher(self):
        batch = []
        while True:
            try:
                item = self._q.get(timeout=1.0)
            except queue.Empty:
                item = None
            if item is not None and item != "STOP":
                batch.append(item)
            if batch and (item is None or item == "STOP" or len(batch) >= 50):
                try:
                    self._post(batch)
                except Exception:  # noqa: BLE001 - never let the network affect a test
                    pass
                batch = []
            if item == "STOP":
                return

    def _emit(self, ev, **kw):
        event = {"ev": ev, "t": time.time(), **kw}
        self.f.write(json.dumps(event, ensure_ascii=False) + "\n")
        self.f.flush()
        if self._push_url:
            self._q.put(event)

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
        if self._push_url:
            self._q.put("STOP")
            self._thread.join(timeout=8)
