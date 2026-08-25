"""Screen/path model — NOT YET IMPLEMENTED.

Phase 1 continuation, deliberately left as a stub rather than a guessed schema: this needs to
unify two real but differently-shaped sources that haven't been reconciled yet —

  - testops/knowledge/flows/*.md   — hand/AI-transcribed flow maps (Mermaid + path list + a
                                      `Covered by` column already resolved against TestRail cases)
  - sit's Tools/DeviceTools/discover_screenflow.py — automated Android screenflow discovery output
                                      (shape not yet read; check its actual output format before
                                      designing FlowPath/Screen models here)

Building this without reading discover_screenflow.py's real output first would be exactly the
kind of invented-schema mistake this whole platform exists to avoid. Next concrete step: run or
read that tool's output on one real device, then design FlowPath/Screen against BOTH real shapes.
"""
from __future__ import annotations

# Intentionally no models defined yet — see module docstring.
