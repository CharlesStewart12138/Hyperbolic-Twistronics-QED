"""Package finite-cover convergence and inconclusivity certificates for P2-14-R09."""

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

from reproducibility.compute.p2_14_r09_finite_cover_analysis import run as run_convergence  # noqa: E402


DATA_FILES = {
    "cover_sequence.csv": "parameter",
    "cover_spectral_sets.csv": "raw",
    "moment_aliasing_margins.csv": "diagnostic",
    "cross_cover_diagnostics.csv": "uncertainty",
    "shell_budgets.csv": "uncertainty",
    "no_loss_no_pollution.csv": "uncertainty",
    "convergence_audit.json": "diagnostic",
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
    hamiltonian_audit_path = hamiltonian_package / "hamiltonian_audits.json"
    hamiltonian_dataset_path = hamiltonian_package / "dataset.json"
    kernel_path = hamiltonian_package / "universal_full_distance_kernel.csv"
    hamiltonian_audit = json.loads(hamiltonian_audit_path.read_text(encoding="utf-8"))
    hamiltonian_dataset = json.loads(hamiltonian_dataset_path.read_text(encoding="utf-8"))
    w_star_over_t = float(hamiltonian_audit["parameters"]["w_star_over_t"])
    audit = run_convergence(output_dir, kernel_path=kernel_path, w_star_over_t=w_star_over_t)
    if audit["status"] != "PASS":
        raise RuntimeError("R09 finite-cover analysis failed")

    upstream_packages = {
        "R05": hamiltonian_package / "dataset.json",
        "R06": PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_spectral_reconstruction" / "dataset.json",
        "R07": PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_representation_completion" / "dataset.json",
        "R08": PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_dos_reconstruction" / "dataset.json",
    }
    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    production_missing = [
        {"parameter_id": "COV-M01", "role": "production quotient tower", "state": "MISSING"},
        {"parameter_id": "COV-M02", "role": "production quotient presentations and maps", "state": "MISSING"},
        {"parameter_id": "COV-M03", "role": "geometric injectivity-radius certificates", "state": "MISSING"},
        {"parameter_id": "COV-M04", "role": "production hopping-cutoff/shell schedule", "state": "MISSING"},
        {"parameter_id": "NUM-M03", "role": "production eigensolver tolerances", "state": "MISSING"},
        {"parameter_id": "NUM-M04", "role": "production DOS broadening/tower schedule", "state": "MISSING"},
        {"parameter_id": "NUM-M07", "role": "production C1/C2 differentiation settings", "state": "MISSING"},
    ]
    parameters = {
        "task_id": "P2-14-R09",
        "scope": "FINITE_ABELIAN_VALIDATION_COVER_FAMILIES_WITH_EXPLICIT_FULL_GROUP_INCONCLUSIVITY",
        "registered_inputs": {
            task: {
                "dataset_id": json.loads(path.read_text(encoding="utf-8"))["dataset_id"],
                "dataset_sha256": sha256_file(path),
            }
            for task, path in upstream_packages.items()
        },
        "cover_families": {
            "A_power_of_two": [4, 8, 16],
            "B_three_multiple": [6, 18],
            "quotients": "(Z/mZ)^4",
            "maps": "coordinate reduction when the lower modulus divides the higher modulus",
            "known_common_kernel": "commutator subgroup; witness [a1,b1] has word length four",
        },
        "injectivity_and_shell_law": {
            "word_injectivity_radius": 2.0,
            "geometric_injectivity_radius": "MISSING",
            "registered_balanced_law": "L_N=floor(sqrt(r_inj,N^L))",
            "realized_balanced_depth": 1,
            "available_full_distance_patch_depths": [1, 2, 3],
            "infinite_tail": "UNKNOWN_BEYOND_DEPTH_THREE",
        },
        "production_missing_inputs": production_missing,
        "parameter_registry": {"path": "reproducibility/PARAMETER_REGISTRY.csv", "sha256": parameter_registry_sha256},
    }
    write_json(output_dir / "parameters.json", parameters)

    summary = {
        "task_id": "P2-14-R09",
        "status": "PASS_PIPELINE_WITH_FULL_SURFACE_GROUP_CONVERGENCE_INCONCLUSIVE",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "FINITE_COVER_CONVERGENCE_DIAGNOSTICS",
        "completed_components": [
            "two explicit finite Abelian quotient sequences with verified inter-level reduction maps",
            "cover degree, matrix dimension, kernel witness, word-injectivity radius, balanced-shell law, and moment-aliasing margins",
            "separate C0 spectral, C1 velocity, and C2 Hessian sampling errors",
            "successive-cover and cross-tower CDF diagnostics",
            "direct one-sided no-loss and no-pollution products in the declared Abelian character sector",
            "separate depth-1/2/3 C0/C1/C2 full-distance shell-tail bounds",
        ],
        "validation_sector_result": {
            "sector": "FIRST_SHELL_ABELIAN_CHARACTER_TORUS",
            "minimum_C0_Hausdorff_error_over_t": audit["minimum_C0_Hausdorff_error_over_t"],
            "maximum_C0_Hausdorff_error_over_t": audit["maximum_C0_Hausdorff_error_over_t"],
            "no_pollution": "DIRECT_UPPER_INCLUSION_ZERO_ERROR",
        },
        "inconclusive_certificates": {
            "full_surface_group": audit["full_surface_group_conclusion"],
            "long_range_kernel": audit["long_range_conclusion"],
            "geometric_injectivity_radius": "MISSING",
            "weak_convergence_upgraded": audit["weak_convergence_upgrade"],
        },
        "production_open_inputs": production_missing,
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, package=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r09.hyperbolic-finite-cover-convergence",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R09",
        "result_ids": ["R6", "R7", "R8", "R9"],
        "observable": {
            "name": "Finite-cover C0/C1/C2, cross-cover, shell-tail, no-loss, and no-pollution diagnostics",
            "definition": "Cover-resolved character spectra and CDFs, separate value/velocity/Hessian errors, shell-tail operator/derivative bounds, injectivity and moment-aliasing margins, and distinct one-sided spectral loss and pollution errors.",
            "units": "energies and C0 in t; C1 in t/hbar; C2 in t; CDF and ratios dimensionless; injectivity in generator-word units",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:M8-local-exactness through eq:M8-aliasing-margin"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:M8-no-loss-error through eq:M8-licensed-spectral-budget"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:M8-balanced-shell-law through eq:M8-C012-budgets"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:M8-derivative-topology-hierarchy and eq:M8-cross-tower-residual"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {
            "status": "ABELIAN_VALIDATION_QUOTIENT_FAMILIES_NONEXHAUSTIVE_IN_SURFACE_GROUP",
            "word_injectivity_radius": 2.0,
            "geometric_injectivity_radius": "MISSING",
        },
        "representation": {
            "status": "COMPLETE_AT_EACH_FINITE_ABELIAN_QUOTIENT",
            "infinite_surface_group_completion": "NOT_CERTIFIED",
        },
        "finite_cover": {
            "status": "DIAGNOSTICS_COMPLETE_FULL_GROUP_CONVERGENCE_INCONCLUSIVE",
            "tower_count": 2,
            "cover_count": 5,
            "injectivity_radius_growth": False,
            "no_loss_full_group": "UNRESOLVED",
            "no_pollution_full_group": "UNRESOLVED",
        },
        "algorithm": {
            "name": "finite-cover-C012-no-loss-no-pollution-validation",
            "implementation": "reproducibility/compute/p2_14_r09_finite_cover_pipeline.py",
            "settings": {
                "tower_moduli": parameters["cover_families"],
                "balanced_shell_law": "floor(sqrt(r_inj))",
                "C0": "two-sided Hausdorff spectral-set error",
                "C1": "generalized-velocity maximum sampling error",
                "C2": "Hessian maximum sampling error",
                "shell_tail_reference_depth": 3,
                "extrapolation_enabled": False,
                "weak_to_strong_upgrade_enabled": False,
                "plotting_enabled": False,
            },
        },
        "environment": {"lock_file": "reproducibility/environment/environment-lock.json", "lock_sha256": environment_lock_sha256},
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "Every quotient grid, character spectrum, CDF, and tail bound is deterministic.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "AVAILABLE",
            "method": "separate cross-cover CDF, C0/C1/C2, shell-tail, and one-sided no-loss/no-pollution diagnostics",
            "files": ["cross_cover_diagnostics.csv", "shell_budgets.csv", "no_loss_no_pollution.csv"],
            "justification": "Computable Abelian-sector errors and explicit unresolved full-group/long-range channels are retained without extrapolation.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    source_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "finite_cover" / "abelian_validation_towers.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r09_finite_cover_analysis.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R09",
        "status": "PASS_PIPELINE_WITH_FULL_SURFACE_GROUP_CONVERGENCE_INCONCLUSIVE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "source_files": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in source_paths
        ],
        "registered_inputs": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in (*upstream_packages.values(), kernel_path, hamiltonian_audit_path)
        ],
        "output_files": [
            {"relative_path": path.relative_to(output_dir).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "prohibited_upgrades": {"weak_to_strong": False, "C0_to_C1": False, "C0_to_C2": False, "unknown_tail_to_zero": False},
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_finite_cover_convergence",
    )
    parser.add_argument(
        "--hamiltonian-package", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction",
    )
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir, hamiltonian_package=args.hamiltonian_package), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
