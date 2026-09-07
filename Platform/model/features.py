"""Common features vs. bespoke variants — the "functionality axis" the Foundation Plan
named as a missing key (no `function_id` anywhere in the existing key set).

A **Feature** is the same conceptual behaviour regardless of which project embodies it —
"tap a card at a reader" is one feature whether the credential is DESFire, MIFARE, EMV
contactless, or a mobile wallet. A **FeatureVariant** is one project's bespoke embodiment
of that feature, and it MUST cite where the fact came from (a TestRail case, a spec
paragraph, or both) — the same no-gap-fabrication rule that governs case text applies here:
a variant with no citation is a GAP, not a guess.

This is deliberately NOT auto-derived from anything. Which card technologies a project
actually uses is exactly the kind of fact that lives in spec prose and case bodies — Tier 2
distillation territory (see the AI Boundary Map), not something a mechanical parser can
extract safely. `load_feature_registry()` reads a manually-curated, cited seed file; nothing
here silently infers a variant that wasn't actually confirmed.

Real seed case (2026-07-23 card-variant sweep, system-test-ops
proposals/coherence-audit/fixes/pv-card-variant-sweep.changelog.md): Translink's PV device
had a case titled "FEIG - ITSO Smartcard Tap" — but Translink's own card-format spec
(FBD-100236, "Translink DESFire ABT Card Format Specification") never mentions ITSO at all;
the real credential is DESFire EV3. The case was corrected. That's precisely the failure
mode this model exists to prevent going forward: "ITSO" was a plausible-sounding label that
had drifted from what the cited spec actually says, and it survived until someone happened
to cross-check it by hand.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from model.provenance import Citation


class Feature(BaseModel):
    key: str
    name: str
    description: str = ""


class FeatureVariant(BaseModel):
    feature_key: str
    project: str
    device_type: str | None = None
    variant_name: str
    note: str = ""
    citation: Citation


class FeatureRegistry(BaseModel):
    features: list[Feature] = Field(default_factory=list)
    variants: list[FeatureVariant] = Field(default_factory=list)

    def variants_for(self, feature_key: str, project: str | None = None) -> list[FeatureVariant]:
        return [
            v for v in self.variants
            if v.feature_key == feature_key and (project is None or v.project == project)
        ]

    def features_missing_variants(self, project: str) -> list[Feature]:
        """Features with zero cited variants for this project — a real, queryable coverage
        gap (the same question `function-granularity-audit.md` had to answer by hand,
        cross-reading seven suites) rather than something someone has to notice."""
        have = {v.feature_key for v in self.variants if v.project == project}
        return [f for f in self.features if f.key not in have]

    def uncited_variants(self) -> list[FeatureVariant]:
        return [v for v in self.variants if v.citation.confidence != "confirmed"]


def _default_seed_path() -> Path:
    override = os.environ.get("TESTOPS_FEATURES_PATH")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent / "knowledge" / "features.yaml"


SEED_PATH = _default_seed_path()


def load_feature_registry(path: Path | None = None) -> FeatureRegistry:
    p = path or SEED_PATH
    if not p.is_file():
        raise FileNotFoundError(
            f"No features.yaml at {p}. This is manually-curated seed data, not auto-generated — "
            f"see model/features.py's module docstring for why."
        )
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return FeatureRegistry(
        features=[Feature(**f) for f in data.get("features", [])],
        variants=[FeatureVariant(**v) for v in data.get("variants", [])],
    )
