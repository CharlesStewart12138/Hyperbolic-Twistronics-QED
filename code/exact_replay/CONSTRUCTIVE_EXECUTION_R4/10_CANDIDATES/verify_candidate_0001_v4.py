"""Independent replay of the first failing gate for CAND-R4-0001."""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, enumerate_ball, matrix_from_word


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0001")
ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0001.certificate.json"
RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0001.independent_replay.json"


def main() -> None:
    certificate_bytes = CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    elements = candidate.enumerate_candidate()
    identity = candidate.cidentity()
    shell = tuple(candidate.cg(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball = enumerate_ball(3)
    image_count = len({candidate.cword(element.representative) for element in ball.elements})
    witness = tuple(certificate["local_failure_witness"]["canonical_word"])
    matrix = matrix_from_word(witness)
    left, right = (tuple(word) for word in certificate["local_failure_witness"]["colliding_ball_words"])
    checks = {
        "candidate_certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "actual_order": len(elements) == 31200,
        "surface_relation": candidate.cword(relator) == identity,
        "physical_shell": len(set(shell)) == 8 and identity not in shell,
        "C8_covariance": all(candidate.csigma(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
        "parity": all(element[8] == 1 for element in shell),
        "B_geom_3_complete_count": len(ball.elements) == 457,
        "B_geom_3_collision": image_count < len(ball.elements),
        "collision_pair_same_image": candidate.cword(left) == candidate.cword(right),
        "difference_candidate_identity": candidate.cword(witness) == identity,
        "difference_nonidentity_Gamma_B": projective_key(matrix) != projective_key(IDENTITY_MATRIX),
    }
    if not all(value for key, value in checks.items() if key != "candidate_certificate_sha256"):
        raise RuntimeError(f"independent replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.1",
        "task_id": "CAND-R4-0001-INDEPENDENT-REPLAY",
        "classification": "PASS_REJECTION_CONFIRMED",
        "first_failing_gate": "LOCAL_B_GEOM_3",
        "checks": checks,
        "global_posthoc_artifact_used": False,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
