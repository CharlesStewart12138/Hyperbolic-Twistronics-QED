"""Path-corrected entry point for the immutable post-construction report builder."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "postconstruction_report_builder_v1",
    HERE / "finalize_postconstruction_state_b.py",
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MODULE.ROOT = HERE.parent
MODULE.OUT = HERE
MODULE.main()
