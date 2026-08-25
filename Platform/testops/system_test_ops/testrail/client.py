"""Read-only TestRail API v2 client.

Deliberately implements GET endpoints only. There is NO method that creates or
updates TestRail data — this enforces the repo's propose-first policy at the
code level. If you find yourself wanting `add_case`/`update_case`, stop: the
design is that humans apply changes the agents propose.

Auth + base URL come from environment (loaded from .env by load_config()):
    TESTRAIL_URL       e.g. https://yourco.testrail.io
    TESTRAIL_USER      the login email
    TESTRAIL_API_KEY   generated under My Settings -> API Keys
"""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv


class TestRailConfigError(RuntimeError):
    """Raised when required TestRail credentials are missing."""


class TestRailError(RuntimeError):
    """Raised when the TestRail API returns an error response."""


def load_config() -> tuple[str, str, str]:
    """Load (url, user, api_key) from environment / .env. Raises if incomplete."""
    load_dotenv()  # no-op if there's no .env; real env vars take precedence
    url = (os.environ.get("TESTRAIL_URL") or "").rstrip("/")
    user = os.environ.get("TESTRAIL_USER") or ""
    api_key = os.environ.get("TESTRAIL_API_KEY") or ""
    missing = [
        name
        for name, val in (
            ("TESTRAIL_URL", url),
            ("TESTRAIL_USER", user),
            ("TESTRAIL_API_KEY", api_key),
        )
        if not val
    ]
    if missing:
        raise TestRailConfigError(
            "Missing TestRail credentials: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill them in (see docs/getting-started.md)."
        )
    return url, user, api_key


class TestRailClient:
    """Thin, paginating, read-only wrapper over the TestRail v2 API."""

    def __init__(
        self,
        url: str | None = None,
        user: str | None = None,
        api_key: str | None = None,
        *,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ) -> None:
        if url is None or user is None or api_key is None:
            url, user, api_key = load_config()
        self.base = f"{url.rstrip('/')}/index.php?/api/v2/"
        self.timeout = timeout
        self._session = session or requests.Session()
        self._session.auth = (user, api_key)
        self._session.headers.update({"Content-Type": "application/json"})

    # ------------------------------------------------------------------ #
    # low-level GET with TestRail pagination handling
    # ------------------------------------------------------------------ #
    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        url = self.base + endpoint
        resp = self._session.get(url, params=params, timeout=self.timeout)
        if resp.status_code >= 400:
            raise TestRailError(
                f"TestRail GET {endpoint} -> {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()

    def _get_collection(self, endpoint: str, key: str, params: dict[str, Any] | None = None) -> list[dict]:
        """GET an endpoint that returns a collection, following pagination.

        Handles both shapes:
          * legacy: a bare JSON list
          * modern (TestRail >= 6.7): {"<key>": [...], "_links": {"next": "..."}}
        """
        out: list[dict] = []
        data = self._get(endpoint, params)
        while True:
            if isinstance(data, list):
                out.extend(data)
                break
            if isinstance(data, dict):
                out.extend(data.get(key, []) or [])
                nxt = (data.get("_links") or {}).get("next")
                if not nxt:
                    break
                # _links.next is like "/api/v2/get_cases/1&suite_id=2&limit=250&offset=250"
                next_endpoint = nxt.split("/api/v2/", 1)[-1].lstrip("/")
                data = self._get(next_endpoint)
                continue
            break
        return out

    # ------------------------------------------------------------------ #
    # read endpoints
    # ------------------------------------------------------------------ #
    def get_projects(self) -> list[dict]:
        return self._get_collection("get_projects", "projects")

    def get_suites(self, project_id: int) -> list[dict]:
        # get_suites returns a bare list in all versions
        data = self._get(f"get_suites/{project_id}")
        return data if isinstance(data, list) else data.get("suites", [])

    def get_sections(self, project_id: int, suite_id: int | None = None) -> list[dict]:
        params = {"suite_id": suite_id} if suite_id else None
        return self._get_collection(f"get_sections/{project_id}", "sections", params)

    def get_cases(self, project_id: int, suite_id: int | None = None) -> list[dict]:
        params = {"suite_id": suite_id} if suite_id else None
        return self._get_collection(f"get_cases/{project_id}", "cases", params)

    def get_runs(self, project_id: int, limit: int | None = None) -> list[dict]:
        params = {"limit": limit} if limit else None
        return self._get_collection(f"get_runs/{project_id}", "runs", params)

    def get_active_runs_for_suite(self, project_id: int, suite_id: int) -> list[dict]:
        """Runs against `suite_id` that are still in progress (not completed).

        Used to warn before pushing changes to a suite that has a live run against
        it — editing cases mid-run can desync the run's result history from what a
        tester is actually looking at. Standalone runs only; a suite embedded in a
        multi-suite Test Plan's entry isn't visible via get_runs and won't be
        caught here (a known limitation — check TestRail directly if in doubt).
        """
        runs = self.get_runs(project_id)
        return [
            r for r in runs
            if r.get("suite_id") == suite_id and not r.get("is_completed")
        ]

    def get_tests(self, run_id: int) -> list[dict]:
        return self._get_collection(f"get_tests/{run_id}", "tests")

    def get_results_for_run(self, run_id: int) -> list[dict]:
        return self._get_collection(f"get_results_for_run/{run_id}", "results")

    def get_case_fields(self) -> list[dict]:
        data = self._get("get_case_fields")
        return data if isinstance(data, list) else data.get("case_fields", [])

    def get_case(self, case_id: int) -> dict:
        return self._get(f"get_case/{int(case_id)}")

    def get_statuses(self) -> list[dict]:
        data = self._get("get_statuses")
        return data if isinstance(data, list) else data.get("statuses", [])

    def status_label_map(self) -> dict[int, str]:
        """{status_id: human label} e.g. {1: 'Passed', 5: 'Failed'}."""
        out: dict[int, str] = {}
        for s in self.get_statuses():
            sid = s.get("id")
            label = s.get("label") or s.get("name")
            if sid is not None and label:
                out[int(sid)] = str(label)
        return out
