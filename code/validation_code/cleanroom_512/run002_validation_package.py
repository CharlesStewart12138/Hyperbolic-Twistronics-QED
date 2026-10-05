"""Package the three isolated RUN-002 manuscript validation fixtures.

MANUSCRIPT SOURCE:
Equations: (623)--(640) and (3743)--(3796).
Section: five-state no-root, first-shell positive root, and registered
512-dimensional exact/KPM/SLQ DOS benchmark.
Model scope: validation only; no value or conclusion is production eligible.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

from validation_code.first_shell.vt016_positive_root import validate_positive_root
from validation_code.five_state.vt015_no_root import validate_no_root


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _data_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return max(0, sum(1 for _line in handle) - 1)


def package_validation(workspace_root: Path, cleanroom_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Audit and package the exact RUN-002 outputs under data/validation.

    MANUSCRIPT SOURCE:
    Equations: exact five-state lower bound; first-shell root/gap; registered
    KPM--SLQ CDF and fixed-broadening reconstruction protocol.
    Model scope: one validation quotient and two theorem-control fixtures;
    production eligibility is explicitly false.
    """

    cleanroom_dir = cleanroom_dir.resolve()
    required_root = (workspace_root / "data" / "validation").resolve()
    if required_root not in cleanroom_dir.parents:
        raise ValueError("clean-room data must remain under data/validation")

    audit = _read_json(cleanroom_dir / "dos_audit.json")
    config = _read_json(cleanroom_dir / "dos_config.json")
    dataset = _read_json(cleanroom_dir / "dataset.json")
    clean_summary = _read_json(cleanroom_dir / "summary.json")
    five_state = validate_no_root()
    first_shell = validate_positive_root()

    cdf_rows = _data_row_count(cleanroom_dir / "dos_cdf.csv")
    broadening_rows = _data_row_count(cleanroom_dir / "broadening_dos.csv")
    cleanroom_passed = (
        audit.get("status") == "PASS"
        and audit.get("dimension") == 512
        and all(audit.get("checks", {}).values())
        and cdf_rows == 2001
        and broadening_rows == 7203
        and "CLEAN_ROOM" in str(config.get("scope", ""))
        and clean_summary.get("task_acceptance_closed") is True
        and dataset.get("finite_cover", {}).get("cover_degree") == 256
    )
    passed = bool(five_state["passed"] and first_shell["passed"] and cleanroom_passed)

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "five_state_no_root.json", five_state)
    _write_json(output_dir / "first_shell_positive_root.json", first_shell)
    source_version = yaml.safe_load(
        (workspace_root / "production_code/config/model.yaml").read_text(encoding="utf-8")
    )["source_version"]
    summary = {
        "run_id": "RUN-002",
        "run_type": "validation",
        "output_namespace": "data/validation",
        "status": "PASS" if passed else "FAIL",
        "production_eligible": False,
        "source_version": source_version,
        "fixtures": {
            "five_state": {"status": "PASS" if five_state["passed"] else "FAIL"},
            "first_shell": {"status": "PASS" if first_shell["passed"] else "FAIL"},
            "cleanroom_512": {
                "status": "PASS" if cleanroom_passed else "FAIL",
                "dimension": audit.get("dimension"),
                "cdf_rows": cdf_rows,
                "broadening_rows": broadening_rows,
                "kpm_moment_count": config.get("kpm", {}).get("moment_count"),
                "kpm_batches": len(config.get("kpm", {}).get("batch_stream_indices", [])),
                "kpm_probes_per_batch": config.get("kpm", {}).get("probe_count_per_batch"),
                "slq_depth": config.get("slq", {}).get("lanczos_depth"),
                "slq_batches": len(config.get("slq", {}).get("batch_stream_indices", [])),
                "slq_probes_per_batch": config.get("slq", {}).get("probe_count_per_batch"),
                "metrics": audit.get("metrics"),
            },
        },
        "explicit_exclusions": [
            "production parameter choice",
            "production quotient or tower",
            "production DOS conclusion",
            "figure generation",
        ],
    }
    _write_json(output_dir / "summary.json", summary)

    package_files = tuple(sorted(path for path in output_dir.iterdir() if path.is_file()))
    cleanroom_files = tuple(sorted(path for path in cleanroom_dir.iterdir() if path.is_file()))
    manifest = {
        "run_id": "RUN-002",
        "run_type": "validation",
        "status": summary["status"],
        "files": [
            {"path": path.relative_to(workspace_root).as_posix(), "bytes": path.stat().st_size, "sha256": _sha256(path)}
            for path in package_files + cleanroom_files
        ],
    }
    _write_json(output_dir / "manifest.json", manifest)
    if not passed:
        raise RuntimeError("RUN-002 validation package failed")
    return summary


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    print(
        json.dumps(
            package_validation(
                root,
                root / "data/validation/cleanroom_512",
                root / "data/validation/RUN-002",
            ),
            indent=2,
            sort_keys=True,
        )
    )
