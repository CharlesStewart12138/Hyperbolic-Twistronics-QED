"""Independent exact replay of the CAND-R4-0003 global rejection."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from functools import lru_cache
from pathlib import Path

import sympy as sp

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, enumerate_ball, field_to_sympy, matrix_from_word


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0003")
candidate.selected_rows = lru_cache(maxsize=1)(candidate.selected_rows)
candidate.q_rotation = lru_cache(maxsize=1)(candidate.q_rotation)
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]; R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0003.certificate.json"
SCAN = R4 / "10_CANDIDATES" / "CAND-R4-0003.global_witness-v2.tsv"
RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0003.global_independent_replay.json"


def main() -> None:
    cert_bytes = CERT.read_bytes(); cert = json.loads(cert_bytes); witness = cert["global_failure_witness"]
    with SCAN.open(encoding="utf-8", newline="") as handle: rows = list(csv.DictReader(handle, delimiter="\t"))
    source = tuple(rows[0]["word"].split()); word = d0.canonical_c8_inverse_word(source)
    matrix = matrix_from_word(word); payload = json.dumps(projective_key(matrix), separators=(",", ":"))
    half_trace = sp.re(field_to_sympy(matrix[0])).expand(); cutoff = 2405 + 1700 * sp.sqrt(2)
    delta = sp.expand(half_trace**2 - cutoff**2)
    elements = candidate.enumerate_image(); ball = enumerate_ball(3)
    checks = {
        "certificate_sha256": hashlib.sha256(cert_bytes).hexdigest().upper(),
        "classification": cert["classification"] == "REJECTED_GLOBAL_WITNESS",
        "actual_order_23040": len(elements) == 23040,
        "complete_local_B_geom_3": len({candidate.word_image(e.representative) for e in ball.elements}) == 457,
        "canonical_word": list(word) == witness["canonical_word"],
        "candidate_kernel_identity": candidate.word_image(word) == candidate.identity(),
        "Gamma_B_nonidentity": projective_key(matrix) != projective_key(IDENTITY_MATRIX),
        "exact_key": payload == witness["exact_group_key"],
        "strict_global_cutoff_failure": delta.is_negative is True,
        "squared_delta": str(delta) == witness["squared_cutoff_delta"],
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"candidate-0003 global replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0", "task_id": "CAND-R4-0003-GLOBAL-INDEPENDENT-REPLAY",
        "classification": "PASS_REJECTION_CONFIRMED", "checks": checks,
        "exact_real_half_trace": str(half_trace), "exact_squared_cutoff_delta": str(delta),
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__": main()
