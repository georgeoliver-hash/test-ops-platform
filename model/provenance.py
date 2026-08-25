"""Every fact in model/ traces to a real source — never a bare claim.

Minimal on purpose: a Citation is attached wherever model/flows.py or a future distilled fact
needs to say "here's where this came from." Kept separate from devices.py/functions.py because
those two are already self-citing (their `source_file` field IS the citation, since they're a
direct parse of a real mirrored file) — this module is for facts that come from distillation
(Tier 2 in the AI Boundary Map) rather than direct mechanical parsing.
"""
from __future__ import annotations

from pydantic import BaseModel


class Citation(BaseModel):
    """Where a distilled fact came from — required on anything not directly parsed from a file."""

    source_kind: str  # "spec" | "flow_map" | "testrail_case" | "run" | "human_confirmed"
    source_ref: str  # e.g. "FBD-100167 para 12", "C4099911", "knowledge/flows/translink-pos-signon.md"
    confidence: str = "confirmed"  # "confirmed" | "gap" | "unconfirmed" — mirrors testops's
    #                                GAP/UNCONFIRMED marker convention; never silently omitted


class CitedFact(BaseModel):
    """A single distilled fact plus its citation — the atomic unit Tier 2 distillation produces."""

    fact: str
    citation: Citation
