"""Regression tests for the internal-parity PSL(3,3):2 exact certificate."""

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def test_internal_graph_extension_certificate()->None:
    record=json.loads((ROOT/"production_code"/"group"/"AUT_PSL3_3_INTERNAL_C8_CERTIFICATE.json").read_text(encoding="utf-8"))
    assert record["classification"]=="PROOF_COMPLETE_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR"
    assert record["group"]["order"]==11232
    assert record["enumeration"]["exact_B3_survivors"]==16
    assert record["enumeration"]["kernel_orbits"]==2
    assert len(record["global_rejection"]["witnesses"])==2
    assert max(w["translation_length_over_a_B"] for w in record["global_rejection"]["witnesses"])<6

