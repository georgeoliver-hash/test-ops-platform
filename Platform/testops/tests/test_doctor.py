"""Pin the readiness preflight's classification + rendering.

The doctor must (a) never raise — it's a preflight, not a gate; (b) put each
finding in the right who-does-what bucket; (c) detect human-only blockers so
/start knows when to stop and ask."""

from __future__ import annotations

from system_test_ops import doctor as d


def test_run_checks_never_raises_and_returns_findings():
    checks = d.run_checks()
    assert checks, "run_checks should always return findings"
    assert all(isinstance(c, d.Check) for c in checks)
    # Every finding lands in a known bucket.
    assert all(c.status in (d.READY, d.CLAUDE, d.NEEDS_YOU, d.MANUAL) for c in checks)


def test_has_blockers_only_for_needs_you():
    no_block = [d.Check("a", d.READY), d.Check("b", d.CLAUDE), d.Check("c", d.MANUAL)]
    assert d.has_blockers(no_block) is False
    blocked = no_block + [d.Check("d", d.NEEDS_YOU, "missing secret")]
    assert d.has_blockers(blocked) is True


def test_render_is_ascii_safe_and_grouped():
    checks = [
        d.Check("Python 3.11+", d.READY, "running 3.11.5"),
        d.Check("Python dependencies", d.CLAUDE, "missing: pydantic", 'pip install -e ".[dev]"'),
        d.Check("TESTRAIL_API_KEY", d.NEEDS_YOU, "missing", "My Settings -> API Keys"),
        d.Check("Atlassian (JIRA) MCP", d.MANUAL, "verify in Claude Code", "Run /mcp"),
    ]
    out = d.render(checks)
    # ASCII-only — this repo has been bitten by cp1252 consoles; the report must be safe anywhere.
    out.encode("ascii")
    # All four group headings present.
    assert "READY" in out
    assert "CLAUDE CAN HANDLE" in out
    assert "NEEDS YOU" in out
    assert "CHECK MANUALLY" in out
    # The verdict reflects the single blocker.
    assert "1 item(s) need you" in out


def test_render_all_green_verdict():
    checks = [d.Check("Python 3.11+", d.READY), d.Check("TestRail connectivity", d.READY)]
    out = d.render(checks)
    assert "all green" in out
    assert d.has_blockers(checks) is False
