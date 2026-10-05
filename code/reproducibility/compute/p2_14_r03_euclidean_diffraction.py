"""Rebuild ideal rigid Euclidean first-shell diffraction geometry."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.euclidean.commensurate import all_cell_records  # noqa: E402
from reproducibility.src.euclidean.diffraction import (  # noqa: E402
    c8_union_residual, diffraction_metrics, rigid_first_shell_peaks,
)


def _write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    peak_rows: list[dict[str, object]] = []
    metric_rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for cell in all_cell_records():
        angle = float(cell["angle_radians"])
        label = f"commensurate_{int(cell['site_count'])}_site"
        for peak in rigid_first_shell_peaks(angle):
            peak_rows.append({"case": label, "site_count": cell["site_count"], **peak})
        metric = diffraction_metrics(
            angle_radians=angle, sigma=int(cell["sigma"]),
            n=int(cell["n"]), divisor=int(cell["parity_divisor"]),
        )
        metric_rows.append({"case": label, "site_count": cell["site_count"], **metric})
        direct_ratio = float(metric["first_shell_split_a_over_2pi"]) * math.sqrt(int(cell["sigma"]))
        exact_ratio = float(metric["split_to_mbz_ratio"])
        checks.append({
            "case": label, "split_ratio_residual": abs(direct_ratio - exact_ratio),
            "status": "PASS" if abs(direct_ratio - exact_ratio) <= 1.0e-12 else "FAIL",
        })

    c8_label = "incommensurate_c8_control"
    for peak in rigid_first_shell_peaks(math.pi / 4.0):
        peak_rows.append({"case": c8_label, "site_count": "", **peak})
    metric_rows.append({
        "case": c8_label, "site_count": "",
        **diffraction_metrics(angle_radians=math.pi / 4.0, sigma=None, n=None, divisor=None),
    })
    c8_residual = c8_union_residual()
    checks.append({
        "case": c8_label, "c8_union_residual": c8_residual,
        "status": "PASS" if c8_residual <= 1.0e-12 else "FAIL",
    })

    _write_csv(
        output_dir / "diffraction_peaks.csv", peak_rows,
        ["case", "site_count", "layer", "peak_index", "qx_a_over_2pi", "qy_a_over_2pi", "ideal_relative_intensity", "scope"],
    )
    _write_csv(
        output_dir / "diffraction_metrics.csv", metric_rows,
        [
            "case", "site_count", "angle_radians", "angle_degrees",
            "first_shell_split_a_over_2pi", "beat_length_over_a", "sigma",
            "mbz_reciprocal_magnitude_a_over_2pi", "split_to_mbz_ratio",
            "supercell_to_beat_length_ratio", "scope",
        ],
    )
    summary = {
        "status": "PASS" if all(entry["status"] == "PASS" for entry in checks) else "FAIL",
        "scope": "IDEAL_RIGID_DELTA_PEAK_GEOMETRY_ONLY",
        "peak_row_count": len(peak_rows), "metric_row_count": len(metric_rows),
        "checks": checks,
        "excluded_component": {
            "name": "finite_window_diffraction_intensity", "state": "MISSING_NUMERICAL_SETTINGS",
            "parameter_registry_ids": ["NUM-M01"],
        },
    }
    (output_dir / "diffraction_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("Euclidean diffraction validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
