"""model/features.py against the real, cited seed data in knowledge/features.yaml."""
from __future__ import annotations

import pytest

from model.features import load_feature_registry


def test_seed_loads_and_has_real_features():
    reg = load_feature_registry()
    keys = {f.key for f in reg.features}
    assert "card_reading.tap" in keys
    assert "backoffice.cloudfare_comm" in keys
    assert "driver.sign_on" in keys


def test_translink_pv_card_reading_variants_are_cited():
    reg = load_feature_registry()
    variants = reg.variants_for("card_reading.tap", project="translink")
    names = {v.variant_name for v in variants}
    assert "MIFARE" in names
    assert any("DESFire" in n for n in names)
    for v in variants:
        assert v.citation.source_ref  # every variant traces to something real
        assert v.citation.confidence == "confirmed"


def test_itso_misnomer_correction_is_the_desfire_variant():
    """Pin the real finding: the old 'ITSO' case was actually DESFire EV3 per Translink's
    own spec — this is the exact drift this model exists to catch."""
    reg = load_feature_registry()
    desfire = [v for v in reg.variants_for("card_reading.tap", "translink") if "DESFire EV3" in v.variant_name]
    assert len(desfire) == 1
    assert "FBD-100236" in desfire[0].citation.source_ref
    assert "ITSO" not in desfire[0].variant_name  # corrected, not perpetuated


def test_cross_project_feature_has_variants_from_both_projects():
    reg = load_feature_registry()
    projects = {v.project for v in reg.variants_for("backoffice.cloudfare_comm")}
    assert projects == {"njt", "translink"}

    signon_projects = {v.project for v in reg.variants_for("driver.sign_on")}
    assert "njt" in signon_projects and "translink" in signon_projects


def test_features_missing_variants_flags_a_real_gap():
    reg = load_feature_registry()
    # njt has no transaction.annulment variant seeded yet -> a real, queryable gap
    # (card_reading.tap used to be this gap; the 2026-09-08 extraction pass filled it in
    # with a real cEMV-tap variant from knowledge/njt/specs/fs002-obv-barcode-emv.md)
    missing = reg.features_missing_variants("njt")
    assert any(f.key == "transaction.annulment" for f in missing)


def test_missing_seed_file_raises_not_silently_empty(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_feature_registry(tmp_path / "does-not-exist.yaml")


def test_uncited_variants_are_real_flagged_gaps_not_missing_citations():
    # Post-2026-09-08 extraction, some variants are honestly marked gap/unconfirmed (the
    # source docs themselves say so) rather than all being "confirmed" — that's correct
    # behaviour, not a defect. What must still hold: every one of them cites a real,
    # non-empty source, so "uncited" never actually means "no citation at all".
    reg = load_feature_registry()
    for v in reg.uncited_variants():
        assert v.citation.confidence in ("gap", "unconfirmed")
        assert v.citation.source_ref.strip()
