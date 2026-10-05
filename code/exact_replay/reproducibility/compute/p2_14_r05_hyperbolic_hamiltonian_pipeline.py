"""Hamiltonian-only clean-room reconstruction pipeline for P2-14-R05."""

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

from reproducibility.compute.p2_14_r05_finite_hamiltonian import run as run_finite  # noqa: E402
from reproducibility.compute.p2_14_r05_full_distance_kernel import run as run_full_distance  # noqa: E402


DATA_FILES = {
    "universal_full_distance_kernel.csv": "raw",
    "full_distance_checks.json": "diagnostic",
    "monolayer_h0_coo.csv": "raw",
    "interlayer_q1_coo.csv": "raw",
    "bilayer_h1_coo.csv": "raw",
    "hamiltonian_audits.json": "diagnostic",
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


def run(
    output_dir: Path,
    *,
    quotient_modulus: int,
    max_word_depth: int,
    h_over_a: float,
    lambda_over_a: float,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    full_distance = run_full_distance(
        output_dir,
        max_word_depth=max_word_depth,
        h_over_a=h_over_a,
        lambda_over_a=lambda_over_a,
    )
    finite = run_finite(
        output_dir,
        modulus=quotient_modulus,
        h_over_a=h_over_a,
        lambda_over_a=lambda_over_a,
    )
    q_difference = abs(float(full_distance["first_shell_q"]) - float(finite["parameters"]["q1"]))
    if q_difference > 2.0e-12:
        raise RuntimeError("universal-patch and finite-matrix first-shell weights disagree")

    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    parameters = {
        "task_id": "P2-14-R05",
        "scope": "HAMILTONIAN_ASSEMBLY_ONLY_NO_EIGENSOLVER_NO_DOS_NO_PLOTTING",
        "source_fixed_geometry": {
            "surface_group": "<a1,b1,a2,b2 | [a1,b1][a2,b2]=e>",
            "generator_shell_size": 8,
            "a_B_over_R": "2*acosh(1+sqrt(2))",
            "intralayer_h0_over_t": "-A_S",
            "first_shell_Q1": "I + q1*A_S",
            "full_distance_q_gamma": "exp[-(sqrt(h^2+d_H(o,gamma o)^2)-h)/lambda_perp]",
            "first_shell_root_relation": "w_star/t = 1/q1",
        },
        "clean_room_validation_fixture": {
            "status": "NOT_A_RECOVERED_PRODUCTION_PARAMETER_SET",
            "quotient": f"(Z/{quotient_modulus}Z)^4",
            "h_over_a": h_over_a,
            "lambda_perp_over_a": lambda_over_a,
            "universal_orbit_word_depth": max_word_depth,
            "w_over_t": finite["parameters"]["w_star_over_t"],
            "reason": "Rational dimensionless values inside the declared summability regime exercise every assembly and symmetry path without being entered as production parameters.",
        },
        "production_missing_inputs": [
            {"parameter_id": "PHY-M02", "role": "physical t scale", "state": "MISSING"},
            {"parameter_id": "PHY-M04", "role": "production w/t scan", "state": "MISSING"},
            {"parameter_id": "PHY-M05", "role": "production lambda_perp/a", "state": "MISSING"},
            {"parameter_id": "PHY-M06", "role": "production h/a", "state": "MISSING"},
            {"parameter_id": "COV-M01", "role": "production finite quotient tower", "state": "MISSING"},
            {"parameter_id": "COV-M04", "role": "production distance cutoff", "state": "MISSING"},
        ],
        "parameter_registry": {"path": "reproducibility/PARAMETER_REGISTRY.csv", "sha256": parameter_registry_sha256},
    }
    write_json(output_dir / "parameters.json", parameters)

    summary = {
        "task_id": "P2-14-R05",
        "status": "PASS_WITH_PRODUCTION_PARAMETERS_MISSING",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "HAMILTONIAN_ONLY",
        "completed_components": [
            "scalar surface-group monolayer h0=-t A_S",
            "physical first-shell interlayer Q1=I+q1 A_S",
            "physical full-distance exponential coefficients on a symmetric universal-orbit patch",
            "finite 512-by-512 bilayer Hamiltonian on an explicit 256-coset quotient",
            "Hermiticity, real time reversal, C8, layer exchange, sparsity, quotient relation, and exact first-shell root operator-identity audits",
        ],
        "checks": {
            "full_distance_kernel": full_distance["status"],
            "finite_hamiltonian": finite["status"],
            "universal_finite_first_shell_q_residual": q_difference,
            "spectrum_computed": False,
            "dos_computed": False,
            "plotting_performed": False,
        },
        "matrix_dimensions": {
            "single_layer": finite["single_layer_dimension"],
            "bilayer": finite["bilayer_dimension"],
        },
        "matrix_nnz": finite["matrix_nnz"],
        "production_open_inputs": parameters["production_missing_inputs"],
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, package=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r05.hyperbolic-hamiltonian-reconstruction",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R05",
        "result_ids": ["R1", "R5"],
        "observable": {
            "name": "Scalar hyperbolic surface-group Hamiltonian matrices and assembly audits",
            "definition": "Sparse matrix elements for h0, Q1, and the finite bilayer, plus full-distance exponential coefficients; no spectral observable is evaluated.",
            "units": "all matrix entries in t; distances in R",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:platform-exponential-interlayer-kernel and eq:platform-complete-one-particle-hamiltonian"},
            {"file": "source_current_195/02_ATOMIC_TASKS/TASK-37_CLEAN.tex", "section_or_equation": "eq:T37_full_distance through eq:T37_complete_bilayer"},
            {"file": "source_current_195/02_ATOMIC_TASKS/TASK-37_CLEAN.tex", "section_or_equation": "eq:T37_exact_root_data and eq:T37_regular_parity_identity"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Methods M3 quotient relation and right-regular representation audits"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {
            "status": "R04_VALIDATION_QUOTIENT",
            "quotient": f"(Z/{quotient_modulus}Z)^4",
            "cover_degree": finite["single_layer_dimension"],
            "production_cover": "MISSING",
        },
        "representation": {
            "status": "FINITE_REGULAR_MATRIX_ASSEMBLY_ONLY",
            "spectral_decomposition": "NOT_COMPUTED",
        },
        "finite_cover": {
            "status": "VALIDATION_QUOTIENT_AVAILABLE_PRODUCTION_MISSING",
            "word_injectivity_radius": 2.0,
            "production_registry_id": "COV-M01",
        },
        "algorithm": {
            "name": "scalar-surface-group-hamiltonian-assembly",
            "implementation": "reproducibility/compute/p2_14_r05_hyperbolic_hamiltonian_pipeline.py",
            "settings": {
                "quotient_modulus": quotient_modulus,
                "max_word_depth": max_word_depth,
                "h_over_a": h_over_a,
                "lambda_over_a": lambda_over_a,
                "eigensolver_enabled": False,
                "dos_enabled": False,
                "plotting_enabled": False,
            },
        },
        "environment": {"lock_file": "reproducibility/environment/environment-lock.json", "lock_sha256": environment_lock_sha256},
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "Hamiltonian assembly and every audit are deterministic.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "MISSING", "method": None, "files": [],
            "justification": "Floating audit residuals are reported, but production parameter and cover uncertainty cannot be evaluated from missing inputs.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    script_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "hamiltonian" / "scalar_surface.py",
        PROJECT_ROOT / "reproducibility" / "src" / "hamiltonian" / "full_distance.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r05_finite_hamiltonian.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r05_full_distance_kernel.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R05",
        "status": "PASS_WITH_PRODUCTION_PARAMETERS_MISSING",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "source_files": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in script_paths
        ],
        "output_files": [
            {"relative_path": path.relative_to(output_dir).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "forbidden_work": {"spectrum": False, "dos": False, "plotting": False},
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction",
    )
    parser.add_argument("--quotient-modulus", type=int, default=4)
    parser.add_argument("--max-word-depth", type=int, default=3)
    parser.add_argument("--h-over-a", type=float, default=0.5)
    parser.add_argument("--lambda-over-a", type=float, default=0.125)
    args = parser.parse_args()
    print(json.dumps(run(
        args.output_dir,
        quotient_modulus=args.quotient_modulus,
        max_word_depth=args.max_word_depth,
        h_over_a=args.h_over_a,
        lambda_over_a=args.lambda_over_a,
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
