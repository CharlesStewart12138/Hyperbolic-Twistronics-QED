"""Finalize CAND-R4-0001 using the full real trace field Q(sqrt2,beta)."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, matrix_from_word


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0001")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

R4 = Path(__file__).resolve().parents[1]
WITNESS = R4 / "10_CANDIDATES" / "CAND-R4-0001.global_witness.tsv"
CHECKPOINT = R4 / "checkpoints" / "CAND-R4-0001-axis6.tsv"
MANIFEST = R4 / "00_FROZEN_INPUTS" / "manifests" / "axis6_exact_ball_manifest.json"
SCANNER = R4 / "10_CANDIDATES" / "scan_candidate_0001_axis6_v2.cpp"
EXECUTABLE = R4 / "10_CANDIDATES" / "scan_candidate_0001_axis6_v2.exe"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def full_trace_witness(word: tuple[str, ...]) -> dict:
    matrix = matrix_from_word(word)
    if projective_key(matrix) == projective_key(IDENTITY_MATRIX):
        raise AssertionError("scanner word is identity in Gamma_B")
    a = matrix[0]
    payload = json.dumps(projective_key(matrix), separators=(",", ":"))
    coefficients = list(a[1:5])
    expression = (
        f"({coefficients[0]}+{coefficients[1]}*sqrt(2)+{coefficients[2]}*beta+"
        f"{coefficients[3]}*sqrt(2)*beta)/2^{a[0]}"
    )
    return {
        "exact_group_key": payload,
        "exact_group_key_sha256": hashlib.sha256(payload.encode("ascii")).hexdigest().upper(),
        "half_trace_real_field": {
            "basis": ["1", "sqrt(2)", "beta", "sqrt(2)*beta"],
            "denominator_power_of_two": a[0],
            "coefficients": coefficients,
            "expression": expression,
        },
        "exact_cutoff_test": "half_trace^2-(2405+1700*sqrt(2))^2 <= 0 by exact real-field sign",
        "boundary_policy": "equality is dangerous and rejects the strict sys>6*a_B target",
        "translation_length_expression": f"acosh(abs({expression}))/acosh(1+sqrt(2))",
    }


def scanned_witness() -> dict:
    with WITNESS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1:
        raise RuntimeError("candidate-specific scanner must emit exactly one early-exit witness")
    row = rows[0]
    source_word = tuple(row["word"].split())
    canonical = d0.canonical_c8_inverse_word(source_word)
    if candidate.cword(canonical) != candidate.cidentity():
        raise RuntimeError("scanner witness does not replay to candidate identity")
    exact = full_trace_witness(canonical)
    trace = exact["half_trace_real_field"]
    scanner_coefficients = [int(row[f"re_c{index}"]) for index in range(4)]
    if trace["denominator_power_of_two"] != int(row["exponent"]) or trace["coefficients"] != scanner_coefficients:
        raise RuntimeError("scanner/full-field trace replay mismatch")
    return {
        "canonical_word": list(canonical),
        "source_word": list(source_word),
        "record_index": int(row["record_index"]),
        "registry_manifest": "00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json",
        "registry_manifest_sha256": file_hash(MANIFEST),
        "scanner_source": "10_CANDIDATES/scan_candidate_0001_axis6_v2.cpp",
        "scanner_source_sha256": file_hash(SCANNER),
        "scanner_executable_sha256": file_hash(EXECUTABLE),
        "scanner_checkpoint_sha256": file_hash(CHECKPOINT),
        "scanner_witness_sha256": file_hash(WITNESS),
        "candidate_image": list(candidate.cword(canonical)),
        "candidate_image_identity": True,
        "nonidentity_in_Gamma_B": True,
        "global_type": "D_global(6a_B)",
        "early_exit_scope": "first dangerous kernel hit in canonical registry order",
        **exact,
    }


candidate.trace_witness = full_trace_witness
candidate.find_early_global_witness = scanned_witness
candidate.main()
