"""Test-run reporting: per-test Jira-ready writeups + collected device logs.

Plugin entry point is `framework.reporting.plugin`; registered in the root
conftest. Tests opt into richer reports via the `jira_report` fixture.
"""
