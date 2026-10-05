"""Independent replay of CAND-R4-0001 and its exact global witness."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, enumerate_ball, matrix_from_word

from .build_candidate_0001 import (
    CANDIDATE_CERT,
    R4,
    cidentity,
    cg,
    csigma,
    cword,
    enumerate_candidate,
    q2_absolute,
    q2_sign,
)


RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0001.independent_replay.json"


def main() -> None:
    certificate_bytes = CANDIDATE_CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    elements = enumerate_candidate()
    identity = cidentity()
    shell = tuple(cg(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball3 = enumerate_ball(3)
    word = tuple(certificate["global_witness"]["canonical_word"])
    matrix = matrix_from_word(word)
    a = matrix[0]
    assert not any(a[index] for index in (3, 4, 5, 6, 7, 8))
    absolute = q2_absolute((a[1], a[2]))
    scale = 1 << a[0]
    cutoff_margin = (2405 * scale - absolute[0], 1700 * scale - absolute[1])

    checks = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "actual_order_31200": len(elements) == 31200,
        "surface_relation": cword(relator) == identity,
        "physical_shell": len(set(shell)) == 8 and identity not in shell,
        "C8_covariance": all(csigma(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
        "parity": all(element[8] == 1 for element in shell),
        "local_B_geom_3": len({cword(element.representative) for element in ball3.elements}) == 457,
        "global_witness_candidate_identity": cword(word) == identity,
        "global_witness_nonidentity_Gamma_B": projective_key(matrix) != projective_key(IDENTITY_MATRIX),
        "global_witness_strict_trace_cutoff": q2_sign(cutoff_margin) > 0,
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"independent candidate replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "CAND-R4-0001-INDEPENDENT-REPLAY",
        "classification": "PASS_REJECTION_CONFIRMED",
        "checks": checks,
        "conclusion": "candidate fails the strict global systole gate and remains rejected",
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
