"""Spectral-only clean-room reconstruction pipeline for P2-14-R06."""

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

from reproducibility.compute.p2_14_r06_character_spectral_analysis import run as run_character  # noqa: E402
from reproducibility.compute.p2_14_r06_finite_solver_analysis import run as run_finite  # noqa: E402


DATA_FILES = {
    "character_spectral_grid.csv": "raw",
    "target_observables.csv": "raw",
    "hodge_eigenvalues.csv": "raw",
    "projector_tracking.csv": "diagnostic",
    "derivative_audit.csv": "uncertainty",
    "character_analysis_checks.json": "diagnostic",
    "finite_spectrum.csv": "raw",
    "finite_solver_checks.json": "uncertainty",
    "parameters.json": "parameter",
    "summary.json": "diagnostic",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_record(path: Path, *, package: Path, role: str) -> dict[str, object]:
    return {
        "relative_path": path.relative_to(package).as_posix(),
        "role": role,
        "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def run(output_dir: Path, *, hamiltonian_package: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_audit_path = hamiltonian_package / "hamiltonian_audits.json"
    source_dataset_path = hamiltonian_package / "dataset.json"
    source_audit = json.loads(source_audit_path.read_text(encoding="utf-8"))
    source_dataset = json.loads(source_dataset_path.read_text(encoding="utf-8"))
    q1 = float(source_audit["parameters"]["q1"])
    w_star_over_t = float(source_audit["parameters"]["w_star_over_t"])
    dimension = int(source_audit["bilayer_dimension"])
    matrix_path = hamiltonian_package / "bilayer_h1_coo.csv"

    character = run_character(output_dir, q1=q1, w_star_over_t=w_star_over_t)
    finite = run_finite(
        output_dir,
        matrix_path=matrix_path,
        dimension=dimension,
        w_star_over_t=w_star_over_t,
    )
    if character["status"] != "PASS" or finite["status"] != "PASS":
        raise RuntimeError("R06 component validation failed")

    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    production_missing_inputs = [
        {"parameter_id": "PHY-M02", "role": "physical t scale", "state": "MISSING"},
        {"parameter_id": "PHY-M04", "role": "production w/t scan", "state": "MISSING"},
        {"parameter_id": "PHY-M05", "role": "production lambda_perp/a", "state": "MISSING"},
        {"parameter_id": "PHY-M06", "role": "production h/a", "state": "MISSING"},
        {"parameter_id": "COV-M01", "role": "production finite quotient tower", "state": "MISSING"},
        {"parameter_id": "NUM-M03", "role": "production eigensolver tolerance", "state": "MISSING"},
        {"parameter_id": "NUM-M07", "role": "production derivative step sequence", "state": "MISSING"},
        {"parameter_id": "NUM-M08", "role": "production target-band ancestry rule", "state": "MISSING"},
    ]
    parameters = {
        "task_id": "P2-14-R06",
        "scope": "SPECTRAL_AND_DERIVATIVE_LAYER_ONLY_NO_REPRESENTATION_COMPLETENESS_NO_DOS_NO_PLOTTING",
        "registered_hamiltonian_input": {
            "dataset_id": source_dataset["dataset_id"],
            "dataset_json_sha256": sha256_file(source_dataset_path),
            "matrix_relative_path": matrix_path.relative_to(PROJECT_ROOT).as_posix(),
            "matrix_sha256": sha256_file(matrix_path),
            "dimension": dimension,
        },
        "clean_room_validation_fixture": {
            "status": "NOT_A_RECOVERED_PRODUCTION_PARAMETER_SET",
            "q1": q1,
            "w_star_over_t": w_star_over_t,
            "character_coupling_ratios": [0.75, 0.875, 1.0, 1.125, 1.25],
            "character_points": "all 16 exact corners of {0,pi}^4",
            "derivative_steps": [2.0 ** -5, 2.0 ** -6, 2.0 ** -7, 2.0 ** -8, 2.0 ** -9, 2.0 ** -10],
        },
        "solver_configuration": {
            "finite_dense": "scipy.linalg.eigh(driver='evr')",
            "finite_sparse_extrema": "scipy.sparse.linalg.eigsh(k=1, which='SA'/'LA', deterministic v0)",
            "character": "numpy.linalg.eigh on explicit 2-by-2 character matrices",
            "target_island_tolerance_over_t": 2.0e-9,
            "dense_sparse_eigenvalue_tolerance_over_t": 2.0e-9,
            "derivatives": "centered second-order finite differences with dyadic refinement",
        },
        "production_missing_inputs": production_missing_inputs,
        "parameter_registry": {
            "path": "reproducibility/PARAMETER_REGISTRY.csv",
            "sha256": parameter_registry_sha256,
        },
    }
    write_json(output_dir / "parameters.json", parameters)

    summary = {
        "task_id": "P2-14-R06",
        "status": "PASS_WITH_PRODUCTION_PARAMETERS_MISSING",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "SPECTRAL_AND_DERIVATIVE_LAYER",
        "component_status": {"character_sector": character["status"], "finite_registered": finite["status"]},
        "completed_components": [
            "registered dense finite eigensolver and deterministic sparse extremal-eigenpair cross-check",
            "target-island projector tracking, rank, bandwidth, and signed lower isolation gap",
            "exact first-shell character-sector bandwidth, gap, generalized velocity, Hessian, and Hodge eigenvalues",
            "dyadically refined centered-difference audit against exact character-sector derivatives",
        ],
        "explicit_exclusions": [
            "representation-completeness validation (P2-14-R07)",
            "density of states",
            "plotting and figure generation",
            "production parameter and quotient claims",
        ],
        "key_metrics": {
            "finite_dimension": dimension,
            "finite_target_rank": finite["target_rank"],
            "finite_target_bandwidth_over_t": finite["target_bandwidth_over_t"],
            "finite_lower_isolation_gap_over_t": finite["lower_isolation_gap_over_t"],
            "maximum_projector_distance": character["maximum_projector_distance"],
            "maximum_corner_extrema_residual": character["maximum_corner_extrema_residual"],
            "final_velocity_abs_error": character["derivative_checks"]["final_velocity_abs_error"],
            "final_hessian_abs_error": character["derivative_checks"]["final_hessian_abs_error"],
        },
        "production_open_inputs": production_missing_inputs,
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [
        file_record(output_dir / name, package=output_dir, role=role)
        for name, role in DATA_FILES.items()
    ]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r06.hyperbolic-spectral-reconstruction",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R06",
        "result_ids": ["R5", "R6", "R7"],
        "observable": {
            "name": "Registered finite and first-shell character spectra with projector and derivative audits",
            "definition": "Eigenvalues and target projectors of the registered Hamiltonian, plus explicitly defined bandwidth, signed isolation gap, generalized velocity norm, Hessian eigenvalues, and Hodge eigenvalues in the declared character sector.",
            "units": "energies, bandwidths, gaps, and Hessians in t; generalized velocity in t/hbar; character momenta dimensionless",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "definitions of bandwidth and gap near lines 14780-14860"},
            {"file": "source_current_195/main.tex", "section_or_equation": "generalized velocity and Hessian definitions near lines 14860-14970"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Hodge eigenproblem near lines 14970-15030"},
            {"file": "source_current_195/02_ATOMIC_TASKS/TASK-37_CLEAN.tex", "section_or_equation": "exact first-shell root data and regular parity identity"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {
            "status": "R04_VALIDATION_QUOTIENT",
            "quotient": "(Z/4Z)^4",
            "production_geometry": "MISSING",
        },
        "representation": {
            "status": "DECLARED_CHARACTER_PLUS_COMPLETE_FINITE_VALIDATION_QUOTIENT",
            "character_scope": "FIRST_SHELL_CHARACTER_NOT_REPRESENTATION_COMPLETE",
            "representation_completeness": "DEFERRED_TO_P2-14-R07",
        },
        "finite_cover": {
            "status": "VALIDATION_QUOTIENT_AVAILABLE_PRODUCTION_MISSING",
            "cover_degree": dimension // 2,
            "production_registry_id": "COV-M01",
        },
        "algorithm": {
            "name": "registered-hamiltonian-spectral-projector-derivative-analysis",
            "implementation": "reproducibility/compute/p2_14_r06_spectral_analysis_pipeline.py",
            "settings": parameters["solver_configuration"] | {
                "dos_enabled": False,
                "plotting_enabled": False,
                "representation_completeness_enabled": False,
            },
        },
        "environment": {
            "lock_file": "reproducibility/environment/environment-lock.json",
            "lock_sha256": environment_lock_sha256,
        },
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "Every matrix, character point, start vector, and finite-difference step is deterministic.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "AVAILABLE",
            "method": "dense-sparse residual/eigenvalue cross-checks and dyadic centered-difference convergence against exact character derivatives",
            "files": ["derivative_audit.csv", "finite_solver_checks.json"],
            "justification": "Numerical solver and derivative errors are quantified for the validation fixture; production input uncertainty remains open.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    source_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "spectrum" / "first_shell_character.py",
        PROJECT_ROOT / "reproducibility" / "src" / "spectrum" / "finite_registered.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r06_character_spectral_analysis.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r06_finite_solver_analysis.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R06",
        "status": "PASS_WITH_PRODUCTION_PARAMETERS_MISSING",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "source_files": [
            {
                "relative_path": path.relative_to(PROJECT_ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in source_paths
        ],
        "registered_inputs": [
            {
                "relative_path": path.relative_to(PROJECT_ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in (source_dataset_path, matrix_path, source_audit_path)
        ],
        "output_files": [
            {
                "relative_path": path.relative_to(output_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "forbidden_work": {"representation_completeness": False, "dos": False, "plotting": False},
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_spectral_reconstruction",
    )
    parser.add_argument(
        "--hamiltonian-package",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction",
    )
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, hamiltonian_package=args.hamiltonian_package), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
