"""Numerical QA helpers and fail-closed contract checks."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from group_inputs import FROZEN, QSTAR_MANIFEST, QSTAR_TABLE, file_sha256


def sparse_hermiticity_defect(matrix) -> float:
    defect = matrix - matrix.T.conjugate()
    return 0.0 if defect.nnz == 0 else float(np.max(np.abs(defect.data)))


def probability_norm_defect(states: np.ndarray) -> float:
    return float(np.max(np.abs(np.sum(np.abs(states) ** 2, axis=1) - 1.0)))


def check_qstar_manifest_hash() -> dict[str, object]:
    manifest = json.loads(QSTAR_MANIFEST.read_text(encoding="utf-8"))
    digest = file_sha256(QSTAR_TABLE).lower()
    expected = str(manifest["artifacts"][QSTAR_TABLE.name]["sha256"]).lower()
    return {"path": str(QSTAR_TABLE), "sha256": digest, "expected_sha256": expected, "listed_in_manifest": digest == expected}


def frozen_inputs_present() -> dict[str, bool]:
    return {
        "qstar_table": QSTAR_TABLE.is_file(),
        "r5_certificate": (FROZEN / "R5_COMMENSURATOR" / "R5_COMM_EXAMPLE_CERTIFICATE.json").is_file(),
        "universal_ball": (FROZEN / "UNIVERSAL_COVER" / "ball_radius_6_exact.jsonl.gz").is_file(),
    }


def write_qa_record(path: Path, record: dict[str, object]) -> None:
    Path(path).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

