"""Pin the conformance auditor's rules — especially the compound-THEN distinction, which is the
subtle one: a noun list inside one observable assertion is valid Gherkin and must NOT be flagged,
while two distinct outcomes joined inline by 'and' must be."""

from __future__ import annotations

from system_test_ops.audit import audit_cases, genuine_compound_then, summarize


def _case(cid=1, title="Sign On — confirm sign on", preface="This test is to confirm the operator can sign on.",
          preconds="**GIVEN** the device is idle", steps=None, expected="The operator signs on."):
    return {
        "id": cid,
        "title": title,
        "custom_preface": preface,
        "custom_preconds": preconds,
        "custom_steps_seperated": steps or [{"content": "**WHEN** the operator signs on",
                                             "expected": "**THEN** the home screen is shown"}],
        "custom_expected": expected,
    }


def test_genuine_compound_then_splits_two_outcomes():
    assert genuine_compound_then("**THEN** the breakdown is displayed and printed")  # two predicates
    assert genuine_compound_then("**THEN** the card is cleared and success is reported")


def test_noun_list_and_is_not_flagged():
    # single observable check that merely lists attributes -> valid, not a finding
    assert genuine_compound_then("**THEN** the screen matches the approved design (layout, wording, labels and colours)") == []
    assert genuine_compound_then("**THEN** up and down arrows are available") == []
    assert genuine_compound_then("**THEN** the date and time are shown") == []


def test_clean_case_has_no_blocking_findings():
    findings = audit_cases([_case()])
    blocking, _ = summarize(findings)
    assert blocking == 0


def test_detects_missing_objective_and_given_and_compound_then():
    bad = _case(
        preface="Check sign on",  # missing the 'This test is to confirm' preamble
        preconds="the device is idle",  # no GIVEN
        steps=[{"content": "**WHEN** the operator signs on",
                "expected": "**THEN** the home screen is shown and a tone plays"}],
    )
    findings = audit_cases([bad])
    assert findings["preface-bad-preamble"]
    assert findings["preconds-no-given"]
    assert findings["then-compound-genuine"]


def test_dup_flagged_cases_are_skipped():
    assert audit_cases([_case(title="ZZ_DELETE_DUP (created in error) - 999")]) == {}
