"""Guarded, opt-in TestRail writer — scoped to a SINGLE target suite.

Safety model (so the old/source suites can never be touched):
  * Writes are allowed ONLY to the suite id in TESTRAIL_WRITE_SUITE_ID (the new suite).
  * Every add_case verifies its target section actually belongs to that allowed suite.
  * Dry-run is the default; nothing is sent to TestRail unless commit=True.
  * The read-only client.py has no write methods at all — all POSTs live here.

This is a deliberate, opt-in capability. If TESTRAIL_WRITE_SUITE_ID is unset, the writer
refuses to do anything.
"""

from __future__ import annotations

import os
from typing import Any

from system_test_ops.testrail.client import TestRailClient, TestRailError


class TestRailWriteError(RuntimeError):
    """Raised when a write is refused by the safety guards or rejected by TestRail."""


def load_write_suite_id() -> int | None:
    val = os.environ.get("TESTRAIL_WRITE_SUITE_ID")
    return int(val) if val and val.strip().isdigit() else None


class TestRailWriter:
    def __init__(
        self,
        client: TestRailClient,
        project_id: int,
        allowed_suite_id: int | None = None,
        *,
        commit: bool = False,
    ) -> None:
        allowed_suite_id = allowed_suite_id if allowed_suite_id is not None else load_write_suite_id()
        if not allowed_suite_id:
            raise TestRailWriteError(
                "No write suite configured. Set TESTRAIL_WRITE_SUITE_ID to the NEW suite id "
                "(the only suite writes are permitted to). Refusing to write."
            )
        self.client = client
        self.project_id = int(project_id)
        self.allowed_suite_id = int(allowed_suite_id)
        self.commit = commit
        # cache of section name-path -> id within the allowed suite
        self._section_index: dict[tuple[str, ...], int] | None = None
        self._existing_by_title: dict[str, dict] | None = None

    # ------------------------------------------------------------------ #
    # internals
    # ------------------------------------------------------------------ #
    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict:
        if not self.commit:  # belt-and-braces; callers gate on commit too
            raise TestRailWriteError("internal: _post called during dry-run")
        url = self.client.base + endpoint
        resp = self.client._session.post(url, json=payload, timeout=self.client.timeout)
        if resp.status_code >= 400:
            raise TestRailWriteError(f"TestRail POST {endpoint} -> {resp.status_code}: {resp.text[:300]}")
        return resp.json()

    def _build_section_index(self) -> dict[tuple[str, ...], int]:
        """Map every existing section in the allowed suite to its full name-path."""
        sections = self.client.get_sections(self.project_id, self.allowed_suite_id)
        by_id = {int(s["id"]): s for s in sections}

        def path(sid: int) -> tuple[str, ...]:
            s = by_id[sid]
            parent = s.get("parent_id")
            prefix = path(int(parent)) if parent else ()
            return prefix + (str(s.get("name", "")),)

        return {path(sid): sid for sid in by_id}

    @property
    def section_index(self) -> dict[tuple[str, ...], int]:
        if self._section_index is None:
            self._section_index = self._build_section_index()
        return self._section_index

    @property
    def existing_by_title(self) -> dict[str, dict]:
        """Lower-cased title -> case dict (id, section_id, …) for the allowed suite.

        Used for idempotent create (skip existing) and for update-in-place by title.
        Every case here is, by construction, in the allowed write suite.
        """
        if self._existing_by_title is None:
            self._existing_by_title = {}
            try:
                for c in self.client.get_cases(self.project_id, self.allowed_suite_id):
                    self._existing_by_title[(c.get("title") or "").strip().lower()] = c
            except TestRailError:
                pass
        return self._existing_by_title

    def _assert_section_in_allowed_suite(self, section_id: int) -> None:
        try:
            sec = self.client._get(f"get_section/{section_id}")
        except TestRailError as exc:
            raise TestRailWriteError(f"Could not verify section {section_id}: {exc}") from exc
        sid = sec.get("suite_id")
        if sid is not None and int(sid) != self.allowed_suite_id:
            raise TestRailWriteError(
                f"REFUSED: section {section_id} is in suite {sid}, not the allowed write suite "
                f"{self.allowed_suite_id}. Writes are locked to the configured new suite only."
            )

    # ------------------------------------------------------------------ #
    # public write ops (dry-run aware)
    # ------------------------------------------------------------------ #
    def find_or_create_section_path(self, path: list[str]) -> int | None:
        """Ensure the nested section path exists in the allowed suite; return leaf id.

        Returns None in dry-run for not-yet-existing sections (so cases can still be planned).
        """
        key: tuple[str, ...] = ()
        parent_id: int | None = None
        leaf_id: int | None = None
        for name in path:
            key = key + (name,)
            existing = self.section_index.get(key)
            if existing:
                parent_id = leaf_id = existing
                continue
            if not self.commit:
                parent_id = leaf_id = None  # would be created
                continue
            payload: dict[str, Any] = {"suite_id": self.allowed_suite_id, "name": name}
            if parent_id:
                payload["parent_id"] = parent_id
            created = self._post(f"add_section/{self.project_id}", payload)
            new_id = int(created["id"])
            self.section_index[key] = new_id
            parent_id = leaf_id = new_id
        return leaf_id

    def add_case(
        self,
        section_id: int | None,
        title: str,
        *,
        steps: str | None = None,
        refs: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict:
        if not self.commit:
            return {"_dry_run": True, "would_create_case": title, "section_id": section_id}
        if section_id is None:
            raise TestRailWriteError(f"Cannot create case '{title}': section not resolved.")
        ex = self.existing_by_title.get(title.strip().lower())
        # Skip only if the same title already exists IN THIS SECTION — identical titles are allowed
        # in different sections (e.g. bus FLU duplicated into Ulsterbus and Metro).
        if ex and ex.get("section_id") == section_id:
            return {"skipped": True, "reason": "title already exists in this section", "title": title}
        self._assert_section_in_allowed_suite(section_id)
        payload: dict[str, Any] = {"title": title}
        if steps:
            payload["custom_steps"] = steps
        if refs:
            # refs may be a YAML string ("TIBU-1, TIBU-2") or a list — never char-join a string.
            payload["refs"] = refs if isinstance(refs, str) else ",".join(refs)
        if extra:
            payload.update(extra)
        res = self._post(f"add_case/{section_id}", payload)
        self.existing_by_title[title.strip().lower()] = res
        return res

    def update_case_fields(
        self,
        case_id: int,
        extra: dict[str, Any],
        *,
        section_id: int | None = None,
    ) -> dict:
        """Partial-update specific custom fields on an existing case, matched by id.

        Unlike `update_case` (which the push composes from a full YAML body), this sends ONLY
        the fields in `extra`, so callers can append a line to one field without disturbing the
        rest of the body. Still suite-locked: the case's section must be in the allowed suite.
        """
        cid = int(case_id)
        if section_id is None:
            try:
                section_id = self.client.get_case(cid).get("section_id")
            except TestRailError as exc:
                raise TestRailWriteError(f"Could not read case {cid} to verify its suite: {exc}") from exc
        if section_id is not None:
            self._assert_section_in_allowed_suite(int(section_id))
        if not self.commit:
            return {"_dry_run": True, "would_update_case": cid, "fields": list(extra)}
        return self._post(f"update_case/{cid}", dict(extra))

    def add_attachment(self, case_id: int, file_path: str) -> dict:
        """Attach a local file (e.g. a screen image) to a case in the allowed suite."""
        if not self.commit:
            return {"_dry_run": True, "would_attach": file_path, "case_id": case_id}
        url = self.client.base + f"add_attachment_to_case/{int(case_id)}"
        with open(file_path, "rb") as fh:
            # Drop the session's application/json content-type so requests sets the multipart boundary.
            resp = self.client._session.post(
                url,
                files={"attachment": fh},
                headers={"Content-Type": None},
                timeout=self.client.timeout,
            )
        if resp.status_code >= 400:
            raise TestRailWriteError(
                f"TestRail attach -> case {case_id} -> {resp.status_code}: {resp.text[:200]}"
            )
        return resp.json()

    def update_case(
        self,
        title: str,
        *,
        new_title: str | None = None,
        refs: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> dict:
        """Update an existing case (matched by `title`) in the allowed suite.

        Pass `new_title` to rename it (keeps the title-based cache consistent so a rename
        never creates a duplicate on re-push).
        """
        key = title.strip().lower()
        existing = self.existing_by_title.get(key)
        if not existing:
            return {"missing": True, "title": title}
        case_id = int(existing["id"])
        if not self.commit:
            return {"_dry_run": True, "would_update_case": case_id, "title": title}
        section_id = existing.get("section_id")
        if section_id is not None:
            self._assert_section_in_allowed_suite(int(section_id))
        payload: dict[str, Any] = {"title": new_title or title}
        if refs is not None:
            payload["refs"] = refs if isinstance(refs, str) else ",".join(refs)
        if extra:
            payload.update(extra)
        res = self._post(f"update_case/{case_id}", payload)
        if new_title and new_title.strip().lower() != key:
            self.existing_by_title.pop(key, None)
            self.existing_by_title[new_title.strip().lower()] = {**existing, "title": new_title}
        return res
