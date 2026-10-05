"""Finalize CAND-R4-0001 from its candidate-specific axis6 early-exit hit."""

from __future__ import annotations

import csv
import hashlib
import importlib
from pathlib import Path


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
    exact = candidate.trace_witness(canonical)
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


candidate.find_early_global_witness = scanned_witness
candidate.main()
