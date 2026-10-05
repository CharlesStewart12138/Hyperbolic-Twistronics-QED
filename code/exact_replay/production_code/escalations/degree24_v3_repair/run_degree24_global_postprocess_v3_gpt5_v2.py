#!/usr/bin/env python3
"""Corrected V2 entry for the Degree-24 V3 certificate-layer postprocessor.

The original entry is preserved as failed provenance.  This wrapper changes
only parsing of the legacy profile TOTAL record, whose RANGE field has two
values and therefore is not a plain key/value sequence.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "run_degree24_global_postprocess_v3_gpt5.py"
SPEC = importlib.util.spec_from_file_location("degree24_global_postprocess_v3_base", SOURCE)
assert SPEC is not None and SPEC.loader is not None
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def parse_profile_corrected():
    entries = {}
    total = None
    for raw in M.PROFILE.read_text(encoding="utf-8").splitlines():
        t = raw.split("\t")
        if t[0] == "ENTRY":
            data = M.kv(t, 2)
            key = t[1]
            assert key not in entries
            row = {
                "order": int(data["ORDER"]),
                "classes": int(data["ORDER8_CLASSES"]),
                "raw": int(data["RAW_PAIRS"]),
                "parity_maps": int(data["PARITY_MAPS"]),
            }
            assert row["raw"] == row["order"] * row["classes"]
            assert row["parity_maps"] > 0
            entries[key] = row
        elif t[0] == "TOTAL":
            total = {
                "profile_keys": int(t[t.index("PARITY_KEYS") + 1]),
                "positive_keys": int(t[t.index("POSITIVE_CLASS_KEYS") + 1]),
                "zero_keys": int(t[t.index("ZERO_CLASS_KEYS") + 1]),
                "class_units": int(t[t.index("ORDER8_CLASSES") + 1]),
                "raw": int(t[t.index("RAW_PAIRS") + 1]),
            }
    assert total is not None
    assert len(entries) == total["profile_keys"] == M.EXPECTED["profile_keys"]
    assert sum(r["classes"] > 0 for r in entries.values()) == total["positive_keys"] == M.EXPECTED["positive_keys"]
    assert sum(r["classes"] == 0 for r in entries.values()) == total["zero_keys"] == M.EXPECTED["zero_keys"]
    assert sum(r["classes"] for r in entries.values()) == total["class_units"] == M.EXPECTED["global_class_units"]
    assert sum(r["raw"] for r in entries.values()) == total["raw"] == M.EXPECTED["global_raw"]
    return entries, total


M.parse_profile = parse_profile_corrected
M.main()
