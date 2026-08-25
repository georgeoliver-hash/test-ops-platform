"""system-test-ops: read-only TestRail/JIRA coverage & run-history intelligence.

The package is the deterministic core: it fetches reproducible data (TestRail
cases and run results) and renders reports. Judgment (classification,
recommendations, Gherkin drafting) lives in the Claude agents under .claude/.
"""

__version__ = "0.1.0"
