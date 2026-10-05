"""Clean-room Euclidean-only Topic-1 reconstruction pipeline for P2-14-R03."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.compute.p2_14_r03_euclidean_bands import run as run_bands  # noqa: E402
from reproducibility.compute.p2_14_r03_euclidean_diffraction import run as run_diffraction  # noqa: E402
from reproducibility.compute.p2_14_r03_euclidean_geometry import run as run_geometry  # noqa: E402


DATA_FILES = {
    "commensurate_cells.csv": "coordinate",
    "lattice_bases.csv": "coordinate",
    "real_space_sites.csv": "coordinate",
    "geometry_checks.json": "diagnostic",
    "bands_w0.csv": "raw",
    "band_checks.json": "diagnostic",
    "diffraction_peaks.csv": "raw",
    "diffraction_metrics.csv": "derived",
    "diffraction_checks.json": "diagnostic",
    "parameters.json": "parameter",
    "summary.json": "diagnostic",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_record(path: Path, *, relative_to: Path, role: str) -> dict[str, object]:
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "relative_path": path.relative_to(relative_to).as_posix(),
        "role": role,
        "media_type": media_type,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(output_dir: Path, *, diagnostic_points_per_segment: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    geometry = run_geometry(output_dir)
    bands = run_bands(output_dir, diagnostic_points_per_segment=diagnostic_points_per_segment)
    diffraction = run_diffraction(output_dir)

    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    parameters = {
        "task_id": "P2-14-R03",
        "scope": "EUCLIDEAN_ONLY",
        "unit_conventions": {
            "length": "a, the square-lattice constant used only as the coordinate unit",
            "reciprocal_length": "2pi/a",
            "energy": "t, the intralayer hopping used only as the energy unit",
        },
        "source_fixed_inputs": {
            "commensurate_cells": "Seven exact square-CSL records with site counts 10, 26, 34, 50, 58, 74, and 82",
            "band_control": "w/t = 0 exact decoupled-layer control",
            "diffraction_control": "Rigid unit-form-factor first reciprocal shell, including theta = pi/4 C8 union control",
        },
        "diagnostic_discretization": {
            "points_per_mbz_segment": diagnostic_points_per_segment,
            "classification": "CLEAN_ROOM_DIAGNOSTIC_GRID_NOT_PRODUCTION_PARAMETER",
            "reason": "NUM-M01 is MISSING; this grid samples exact formulas but is not represented as a recovered production mesh.",
        },
        "missing_production_inputs": [
            {"parameter_id": "PHY-M04", "role": "hybridized interlayer coupling scan", "state": "MISSING"},
            {"parameter_id": "PHY-M05", "role": "selected interlayer decay ratio", "state": "MISSING"},
            {"parameter_id": "PHY-M06", "role": "selected layer-separation ratio", "state": "MISSING"},
            {"parameter_id": "NUM-M01", "role": "production mBZ/diffraction mesh and convergence tolerance", "state": "MISSING"},
        ],
        "parameter_registry": {
            "path": "reproducibility/PARAMETER_REGISTRY.csv",
            "sha256": parameter_registry_sha256,
        },
    }
    write_json(output_dir / "parameters.json", parameters)

    completed = [
        "exact commensurate-angle and square-CSL inventory",
        "10-site and 34-site cells plus every declared cell below 100 sites",
        "direct/reciprocal lattice coordinates and both-layer real-space representatives",
        "normalized w/t=0 folded bands along Gamma-X-M-Gamma",
        "ideal rigid first-shell diffraction splitting and C8 union control",
    ]
    blocked = [
        {
            "component": "hybridized_w_positive_bands",
            "reason": "PHY-M04, PHY-M05, PHY-M06, and production NUM-M01 are MISSING",
        },
        {
            "component": "finite_window_diffraction_intensities",
            "reason": "production window, q-grid, normalization, and convergence settings are not recovered (NUM-M01 MISSING)",
        },
    ]
    summary = {
        "task_id": "P2-14-R03",
        "status": "PARTIAL_PASS",
        "scientific_closure": False,
        "scope": "EUCLIDEAN_ONLY",
        "completed_components": completed,
        "blocked_components": blocked,
        "checks": {
            "geometry": geometry["status"],
            "w0_bands": bands["status"],
            "ideal_diffraction": diffraction["status"],
            "hyperbolic_calculation_included": False,
        },
        "row_counts": {
            "real_space_sites": geometry["real_space_row_count"],
            "bands_w0": bands["row_count"],
            "diffraction_peaks": diffraction["peak_row_count"],
            "diffraction_metrics": diffraction["metric_row_count"],
        },
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, relative_to=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset_manifest = {
        "schema_version": 1,
        "dataset_id": "p2-14-r03.euclidean-topic1-reconstruction",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R03",
        "result_ids": ["R2", "R3", "R4"],
        "observable": {
            "name": "Euclidean square-bilayer benchmark geometry, w=0 folded spectrum, and ideal diffraction",
            "definition": "Exact square-CSL formulas evaluated in normalized coordinates; production hybridized bands and finite-window diffraction remain excluded where parameters are missing.",
            "units": "coordinates in a and 2pi/a; energies in t",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "Euclidean Topic-1 commensurate-cell table and square-CSL formulas"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:euclidean-full-bloch-hamiltonian and nearest-neighbor dispersion"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Gamma-X-M-Gamma mBZ path definition"},
            {"file": "source_current_195/main.tex", "section_or_equation": "III. Fourier transform and diffraction; exact splitting and C8 union control"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {
            "status": "EXACT_SQUARE_CSL",
            "cell_site_counts": geometry["declared_site_counts"],
            "coordinate_files": ["commensurate_cells.csv", "lattice_bases.csv", "real_space_sites.csv"],
        },
        "representation": {
            "status": "EUCLIDEAN_BLOCH_W0_CONTROL",
            "momentum_path": "Gamma-X-M-Gamma",
            "hybridized_w_positive_component": "MISSING_PARAMETERS",
        },
        "finite_cover": {
            "status": "NOT_APPLICABLE",
            "reason": "The declared Euclidean benchmark uses exact periodic coincidence cells, not hyperbolic finite covers.",
        },
        "algorithm": {
            "name": "exact-square-csl-euclidean-topic1-pipeline",
            "implementation": "reproducibility/compute/p2_14_r03_euclidean_pipeline.py",
            "settings": {
                "diagnostic_points_per_mbz_segment": diagnostic_points_per_segment,
                "diagnostic_mesh_is_production_parameter": False,
                "interlayer_coupling_over_t": 0.0,
                "diffraction_model": "rigid_unit_form_factor_ideal_first_shell",
            },
        },
        "environment": {
            "lock_file": "reproducibility/environment/environment-lock.json",
            "lock_sha256": environment_lock_sha256,
        },
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "Every reconstructed Euclidean subset is deterministic.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "MISSING", "method": None, "files": [],
            "justification": "Exact formula controls have no sampling uncertainty, but production numerical convergence uncertainty is unavailable because NUM-M01 is missing.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset_manifest)

    script_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "euclidean" / "commensurate.py",
        PROJECT_ROOT / "reproducibility" / "src" / "euclidean" / "bands.py",
        PROJECT_ROOT / "reproducibility" / "src" / "euclidean" / "diffraction.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r03_euclidean_geometry.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r03_euclidean_bands.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r03_euclidean_diffraction.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R03", "status": "PARTIAL_PASS", "scope": "EUCLIDEAN_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "command": f"python reproducibility/compute/p2_14_r03_euclidean_pipeline.py --output-dir {output_dir.as_posix()} --diagnostic-points-per-segment {diagnostic_points_per_segment}",
        "source_files": [
            {
                "relative_path": path.relative_to(PROJECT_ROOT).as_posix(),
                "bytes": path.stat().st_size, "sha256": sha256_file(path),
            }
            for path in script_paths
        ],
        "output_files": [
            {
                "relative_path": path.relative_to(output_dir).as_posix(),
                "bytes": path.stat().st_size, "sha256": sha256_file(path),
            }
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "excluded_components": blocked,
        "hyperbolic_calculation_included": False,
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "euclidean_topic1_reconstruction",
    )
    parser.add_argument("--diagnostic-points-per-segment", type=int, default=41)
    args = parser.parse_args()
    if args.diagnostic_points_per_segment < 2:
        parser.error("--diagnostic-points-per-segment must be at least 2")
    print(json.dumps(run(args.output_dir, diagnostic_points_per_segment=args.diagnostic_points_per_segment), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
