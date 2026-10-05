"""Independent exact replay of the CAND-R4-0002 global rejection."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from pathlib import Path

import sympy as sp

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import (
    IDENTITY_MATRIX,
    enumerate_ball,
    field_to_sympy,
    matrix_from_word,
)


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0002")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0002.certificate.json"
SCAN = R4 / "10_CANDIDATES" / "CAND-R4-0002.global_witness.tsv"
REGISTRY = R4 / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
LEDGER = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
RESULT = R4 / "11_CERTIFICATES" / "CAND-R4-0002.global_independent_replay.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    certificate_bytes = CERT.read_bytes()
    certificate = json.loads(certificate_bytes)
    witness = certificate["global_failure_witness"]
    with SCAN.open(encoding="utf-8", newline="") as handle:
        scan_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(scan_rows) != 1:
        raise RuntimeError("expected one early-exit scan witness")
    source_word = tuple(scan_rows[0]["word"].split())
    word = d0.canonical_c8_inverse_word(source_word)
    matrix = matrix_from_word(word)
    key_payload = json.dumps(projective_key(matrix), separators=(",", ":"))
    key_hash = hashlib.sha256(key_payload.encode("ascii")).hexdigest().upper()
    a = matrix[0]
    real_half_trace = sp.re(field_to_sympy(a)).expand()
    cutoff = 2405 + 1700 * sp.sqrt(2)
    delta = sp.expand(real_half_trace**2 - cutoff**2)

    elements = candidate.enumerate_image()
    ball = enumerate_ball(3)
    shell = tuple(candidate.generator(i) for i in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))

    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        danger_rows = list(csv.DictReader(handle, delimiter="\t"))
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        matrix_rows = list(csv.DictReader(handle, delimiter="\t"))

    checks = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest().upper(),
        "classification_rejected_global": certificate["classification"] == "REJECTED_GLOBAL_WITNESS",
        "actual_order_11520": len(elements) == 11520,
        "surface_relation": candidate.word_image(relator) == candidate.identity(),
        "physical_shell": len(set(shell)) == 8 and candidate.identity() not in shell,
        "C8_covariance": all(candidate.phi(shell[i]) == shell[(i + 1) % 8] for i in range(8)),
        "parity": all((element[8].bit_count() % 2) == 1 for element in shell),
        "complete_local_B_geom_3": len({candidate.word_image(e.representative) for e in ball.elements}) == 457,
        "canonical_word_matches": list(word) == witness["canonical_word"],
        "candidate_kernel_identity": candidate.word_image(word) == candidate.identity(),
        "nonidentity_in_Gamma_B": projective_key(matrix) != projective_key(IDENTITY_MATRIX),
        "exact_key_matches": key_payload == witness["exact_group_key"] and key_hash == witness["exact_group_key_sha256"],
        "real_half_trace_in_Qsqrt2": a[3] == 0 and a[4] == 0,
        "strict_global_cutoff_failure": delta.is_negative is True,
        "exact_squared_delta_matches": str(delta) == witness["squared_cutoff_delta"],
        "danger_registry_row_present": any(row["witness_id"] == witness["witness_id"] and row["type"] == "D_global(6a_B)" for row in danger_rows),
        "witness_ledger_row_present": any(row["Witness ID"] == witness["witness_id"] for row in witness_rows),
        "separator_matrix_row_present": any(row["witness_id"] == witness["witness_id"] for row in matrix_rows),
    }
    if not all(value for key, value in checks.items() if key != "certificate_sha256"):
        raise RuntimeError(f"candidate 0002 global replay failed: {checks}")
    RESULT.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "CAND-R4-0002-GLOBAL-INDEPENDENT-REPLAY",
        "classification": "PASS_REJECTION_CONFIRMED",
        "checks": checks,
        "exact_real_half_trace": str(real_half_trace),
        "exact_squared_cutoff_delta": str(delta),
        "registry_sha256": sha256(REGISTRY),
        "witness_ledger_sha256": sha256(LEDGER),
        "separator_matrix_sha256": sha256(MATRIX),
        "conclusion": "candidate passes the structural and complete local gates but fails the strict global systole gate",
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
