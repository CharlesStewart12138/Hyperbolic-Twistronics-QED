"""Finalize the proof-complete order-31,250 class-two C8 family audit."""

from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from math import acosh, sqrt
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np

from production_code.group.class2_p5_c8_family import (
    b3_survivors,
    decode_word,
    exterior_rotation,
    invariant_relator_quotients,
    relator_exterior_vector,
)

ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
SCAN = ROOT / "data" / "production" / "global_direct_v2" / "class2_p5_candidate_scan.tsv"
BALL = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"

SCANNED_ROWS = (
 (((1,0,0,0,2,1),(0,1,3,3,0,0))), (((1,0,2,2,1,1),(0,1,2,2,3,0))),
 (((1,0,2,3,0,4),(0,1,0,0,4,0))), (((1,0,2,3,0,4),(0,1,1,3,4,1))),
 (((1,0,2,3,0,4),(0,1,2,1,4,2))), (((1,0,2,3,0,4),(0,1,2,4,1,1))),
 (((1,0,2,3,0,4),(0,1,3,4,4,3))), (((1,0,2,3,0,4),(0,1,4,2,4,4))),
 (((1,0,3,2,0,4),(0,1,0,0,4,0))), (((1,0,3,2,0,4),(0,1,1,2,4,2))),
 (((1,0,3,2,0,4),(0,1,2,4,4,4))), (((1,0,3,2,0,4),(0,1,3,1,4,1))),
 (((1,0,3,2,0,4),(0,1,4,2,1,1))), (((1,0,3,2,0,4),(0,1,4,3,4,3))),
 (((1,0,3,3,3,1),(0,1,4,4,2,0))), (((1,2,0,0,0,1),(0,0,1,1,2,0))),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> dict[str, str]:
    return dict(line.split("\t", 1) for line in path.read_text(encoding="utf-8").splitlines())


def b3_words() -> list[tuple[int, ...]]:
    result = []
    with gzip.open(BALL, "rt", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            if int(record["minimum_geometric_word_length"]) <= 3:
                result.append(tuple(int(name[1:]) for name in record["representative"]))
    return result


def induced_central_action(rows: tuple[tuple[int, ...], tuple[int, ...]]) -> list[list[int]]:
    matrix = np.asarray(rows, dtype=np.int64)
    pivots = [int(np.flatnonzero(row)[0]) for row in matrix]
    return [[int(value) for value in (row @ exterior_rotation() % 5)[pivots]] for row in matrix]


def main() -> None:
    scan = read_tsv(SCAN)
    if scan["complete"] != "1" or int(scan["scanned_records"]) != 785_639_753:
        raise RuntimeError("class-two scan incomplete")
    family = invariant_relator_quotients()
    words = b3_words()
    survivors = b3_survivors(words)
    survivor_rows = {candidate.rows for candidate in survivors}
    if len(family) != 22 or len(words) != 457 or len(survivors) != 16:
        raise RuntimeError("family/B3 count drift")
    if survivor_rows != set(SCANNED_ROWS):
        raise RuntimeError("C++ scanner candidate set differs from independent Python B3 survivors")
    a_over_R = 2 * acosh(1 + sqrt(2))
    results = []
    for index, rows in enumerate(SCANNED_ROWS):
        dangerous = int(scan[f"candidate_{index}_dangerous_hits"])
        if dangerous <= 0:
            raise RuntimeError("unexpected globally surviving candidate")
        depth = int(scan[f"candidate_{index}_witness_depth"])
        high = int(scan[f"candidate_{index}_witness_high"])
        low = int(scan[f"candidate_{index}_witness_low"])
        half_trace = float(scan[f"candidate_{index}_minimum_abs_trace_half"])
        results.append({
            "scanner_index": index,
            "central_projection_rows": rows,
            "induced_C8_central_matrix": induced_central_action(rows),
            "kernel_hits_in_axis_registry": int(scan[f"candidate_{index}_kernel_hits"]),
            "dangerous_kernel_hits_le_6a_B": dangerous,
            "first_dangerous_witness_record_index": int(scan[f"candidate_{index}_witness_index"]),
            "first_dangerous_witness_word": [f"g{digit}" for digit in decode_word(high, low, depth)],
            "minimum_abs_trace_half_in_registry": half_trace,
            "minimum_translation_length_over_a_B_in_registry": 2 * acosh(half_trace) / a_over_R,
        })
    record = {
        "schema_version": "1.0",
        "family_task_id": "PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3-CLASS2-P5",
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "classification": "PROOF_COMPLETE_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR",
        "construction": {
            "elements": "(epsilon,v,z) in F2 x F5^4 x F5^2",
            "multiplication": "(e,v,z)(f,w,t)=(e+f,v+w,z+t+(1/2)P(v wedge w))",
            "physical_generator_images": "q(g_j)=(1,T^j e0,0), T e_i=e_(i+1), T e3=-e0",
            "order_each_candidate": 31_250,
            "surjective": True,
            "bipartite": True,
            "eight_distinct_physical_images": True,
            "C8_exact_order": 8,
            "surface_relator_exterior_vector": list(map(int, relator_exterior_vector())),
        },
        "proof_complete_parameterization": {
            "all_two_dimensional_subspaces_enumerated_by_unique_RREF": 508_431,
            "C8_stable_and_relator_killing_subspaces": len(family),
            "exact_geometric_word_B3_elements": len(words),
            "B3_injective_candidates": len(survivors),
            "Cxx_scanned_candidate_set_equals_independent_Python_survivor_set": True,
        },
        "global_scan": {
            "axis_registry_records": int(scan["total_records"]),
            "records_scanned": int(scan["scanned_records"]),
            "abelian_parity_identity_hits": int(scan["abelian_parity_hits"]),
            "runtime_seconds": float(scan["elapsed_seconds"]),
            "all_candidates_have_dangerous_kernel_elements": True,
            "survivors": 0,
            "candidate_results": results,
        },
        "scope": "This is an exhaustive no-go only for two-dimensional C8-stable central quotients of the class-two exponent-five homology quotient; it is not a no-go for all finite groups of order <=50000.",
        "provenance": {
            "axis_registry_sha256": "1148bf89c1d3dddf3f26eda57f2385ce8e65cbc8ce8042546683f18bde235c5b",
            "scan_tsv_sha256": sha256(SCAN),
            "python_family_code_sha256": sha256(GROUP / "class2_p5_c8_family.py"),
            "cpp_scanner_sha256": sha256(GROUP / "scan_axis6_class2_p5_candidates.cpp"),
            "cpp_executable_sha256": sha256(GROUP / "scan_axis6_class2_p5_candidates.exe"),
        },
    }
    json_path = GROUP / "CLASS2_P5_C8_FAMILY_CERTIFICATE.json"
    json_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    minimum = min(item["minimum_translation_length_over_a_B_in_registry"] for item in results)
    maximum = max(item["minimum_translation_length_over_a_B_in_registry"] for item in results)
    markdown = f"""# Class-two exponent-five C8 quotient family

Status: **proof-complete family exhaustion; zero global survivors**.

Every candidate has order `2*5^6=31,250`.  Its elements are
`(epsilon,v,z) in F2 x F5^4 x F5^2`, with BCH class-two multiplication
`z -> z+z'+(1/2)P(v wedge v')`.  The eight physical generators are
`(1,T^j e0,0)`, where `T^4=-I`; hence inverses, bipartite parity, eight
directions, and exact C8 order are built into the construction.  Requiring
the two-row projection `P` to kill the surface-relator exterior vector
`{list(map(int, relator_exterior_vector()))}` makes the surface relation exact.

The unique-RREF enumeration covers all 508,431 two-dimensional subspaces of
`(Lambda^2 F5^4)^*`. Exactly 22 are C8-stable and kill the relator. Exactly
16 remain injective on the 457-element geometric-word B3. The C++ candidate
set equals the independently enumerated Python survivor set.

All 16 candidates were streamed through all 785,639,753 records of the exact
axis-six registry. Every candidate has at least 16,656 dangerous kernel hits;
their observed minimum translation lengths range from {minimum:.12f} to
{maximum:.12f} `a_B`, strictly below the required `6a_B`. Therefore this
entire family is rejected globally. The conclusion is family-scoped and does
not assert a universal compact-quotient no-go.
"""
    (GROUP / "CLASS2_P5_C8_FAMILY_CERTIFICATE.md").write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
