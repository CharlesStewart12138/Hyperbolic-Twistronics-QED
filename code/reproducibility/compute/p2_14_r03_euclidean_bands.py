"""Rebuild normalized zero-interlayer-coupling Euclidean folded bands."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.src.euclidean.bands import folded_w0_bands  # noqa: E402
from reproducibility.src.euclidean.commensurate import all_cell_records  # noqa: E402


FIELDS = [
    "site_count", "sigma", "angle_degrees", "point_index", "segment_index",
    "segment", "segment_fraction", "kx_a", "ky_a", "path_distance_ka",
    "layer", "folded_branch", "energy_over_t", "interlayer_coupling_over_t", "scope",
]


def run(output_dir: Path, *, diagnostic_points_per_segment: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for cell in all_cell_records():
        rows, cell_check = folded_w0_bands(
            p=int(cell["p"]), q=int(cell["q"]), sigma=int(cell["sigma"]),
            angle_radians=float(cell["angle_radians"]),
            points_per_segment=diagnostic_points_per_segment,
        )
        for row in rows:
            all_rows.append({
                "site_count": cell["site_count"], "sigma": cell["sigma"],
                "angle_degrees": cell["angle_degrees"], **row,
            })
        checks.append({"site_count": cell["site_count"], "sigma": cell["sigma"], **cell_check})

    with (output_dir / "bands_w0.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    summary = {
        "status": "PASS" if all(entry["status"] == "PASS" for entry in checks) else "FAIL",
        "scope": "EXACT_W0_FOLDING_CONTROL_ONLY",
        "mesh_classification": "CLEAN_ROOM_DIAGNOSTIC_GRID_NOT_PRODUCTION_PARAMETER",
        "diagnostic_points_per_segment": diagnostic_points_per_segment,
        "row_count": len(all_rows),
        "cell_checks": checks,
        "excluded_component": {
            "name": "hybridized_w_positive_bands", "state": "MISSING_PARAMETERS",
            "parameter_registry_ids": ["PHY-M04", "PHY-M05", "PHY-M06", "NUM-M01"],
        },
    }
    (output_dir / "band_checks.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if summary["status"] != "PASS":
        raise RuntimeError("Euclidean w=0 folded-band validation failed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--diagnostic-points-per-segment", type=int, default=41)
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, diagnostic_points_per_segment=args.diagnostic_points_per_segment), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
