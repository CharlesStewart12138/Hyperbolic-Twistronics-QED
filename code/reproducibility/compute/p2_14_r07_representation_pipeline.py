"""Package the complete finite-quotient representation reconstruction for P2-14-R07."""

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

from reproducibility.compute.p2_14_r07_representation_completion import run as run_completion  # noqa: E402


DATA_FILES = {
    "irreducible_representations.csv": "raw",
    "sector_spectra.csv": "raw",
    "abelian_spectrum.csv": "raw",
    "full_spectrum.csv": "raw",
    "abelian_full_spectrum_comparison.csv": "uncertainty",
    "higher_dimensional_sectors.csv": "raw",
    "peter_weyl_audit.json": "uncertainty",
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
    matrix_path = hamiltonian_package / "bilayer_h1_coo.csv"
    source_audit = json.loads(source_audit_path.read_text(encoding="utf-8"))
    source_dataset = json.loads(source_dataset_path.read_text(encoding="utf-8"))
    q1 = float(source_audit["parameters"]["q1"])
    w_star_over_t = float(source_audit["parameters"]["w_star_over_t"])
    dimension = int(source_audit["bilayer_dimension"])
    audit = run_completion(
        output_dir,
        matrix_path=matrix_path,
        dimension=dimension,
        q1=q1,
        w_star_over_t=w_star_over_t,
    )
    if audit["status"] != "PASS":
        raise RuntimeError("R07 representation completion failed")

    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    production_missing = [
        {"parameter_id": "COV-M01", "role": "production finite quotient and quotient tower", "state": "MISSING"},
        {"parameter_id": "COV-M02", "role": "production quotient presentation and maps", "state": "MISSING"},
        {"parameter_id": "REP-M01", "role": "production irreducible-representation catalogue", "state": "MISSING"},
        {"parameter_id": "REP-M02", "role": "production exact irrep multiplicities", "state": "MISSING"},
    ]
    parameters = {
        "task_id": "P2-14-R07",
        "scope": "COMPLETE_REPRESENTATION_DECOMPOSITION_OF_THE_EXPLICIT_R04_VALIDATION_QUOTIENT_ONLY",
        "registered_hamiltonian_input": {
            "dataset_id": source_dataset["dataset_id"],
            "dataset_json_sha256": sha256_file(source_dataset_path),
            "matrix_relative_path": matrix_path.relative_to(PROJECT_ROOT).as_posix(),
            "matrix_sha256": sha256_file(matrix_path),
            "bilayer_dimension": dimension,
            "q1": q1,
            "w_star_over_t": w_star_over_t,
        },
        "validation_quotient": {
            "group": "(Z/4Z)^4",
            "order": 256,
            "group_structure": "FINITE_ABELIAN",
            "dual": "256 one-dimensional characters labelled by (n_a1,n_b1,n_a2,n_b2) in (Z/4Z)^4",
            "higher_dimensional_irreps": "EXACT_EMPTY_SET",
            "gap_required": False,
            "gap_reason": "The complete dual is explicit for this Abelian validation quotient; GAP would be required only after a non-Abelian production quotient is supplied.",
        },
        "exact_weight_rule": {
            "sector_state_count": "nu_M*d_rho^2 with nu_M=2",
            "regular_plancherel_weight": "d_rho^2/|Q|",
            "spectral_state_weight": "d_rho/(nu_M*|Q|) per eigenvalue of H[rho]",
        },
        "production_missing_inputs": production_missing,
        "parameter_registry": {"path": "reproducibility/PARAMETER_REGISTRY.csv", "sha256": parameter_registry_sha256},
    }
    write_json(output_dir / "parameters.json", parameters)

    summary = {
        "task_id": "P2-14-R07",
        "status": "PASS_FOR_EXPLICIT_VALIDATION_QUOTIENT_WITH_PRODUCTION_QUOTIENT_MISSING",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "FINITE_QUOTIENT_REPRESENTATION_COMPLETION",
        "completed_components": [
            "enumeration of all 256 inequivalent one-dimensional irreducible representations",
            "exact Peter-Weyl/Wedderburn degree-square, multiplicity, Plancherel-weight, and 512-state-count identities",
            "unitary finite Fourier transform and sector-conservation audit of the registered Hamiltonian",
            "separately exported Abelian-sector and full finite-matrix spectra with multiset comparison",
            "explicit empty higher-dimensional-sector dataset certified by the Abelian group structure",
        ],
        "key_metrics": {
            "group_order": audit["group_order"],
            "irrep_count": audit["irrep_count"],
            "higher_dimensional_irrep_count": audit["higher_dimensional_irrep_count"],
            "sum_irrep_dimension_squared": audit["sum_irrep_dimension_squared"],
            "bilayer_state_count": audit["bilayer_state_count"],
            "representation_coverage_fraction": audit["representation_coverage_fraction"],
            "abelian_weight_fraction": audit["abelian_weight_fraction"],
            "nonabelian_weight_fraction": audit["nonabelian_weight_fraction"],
            "nonabelian_completion_distance_over_t": audit["nonabelian_completion_distance_over_t"],
            "numerical_abelian_full_reconstruction_residual_over_t": audit["numerical_abelian_full_reconstruction_residual_over_t"],
            "maximum_character_orthogonality_residual": audit["maximum_character_orthogonality_residual"],
            "maximum_off_sector_hamiltonian_element_over_t": audit["maximum_off_sector_hamiltonian_element_over_t"],
        },
        "gap_status": audit["gap_dependency"],
        "production_open_inputs": production_missing,
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, package=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r07.hyperbolic-representation-completion",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R07",
        "result_ids": ["R5", "R6", "R7"],
        "observable": {
            "name": "Complete finite-quotient representation sectors, exact state weights, and Abelian-versus-full spectra",
            "definition": "All irreducible sectors of the explicit validation quotient, their exact regular multiplicities and rational weights, their two-layer block eigenvalues, the direct full-matrix spectrum, and their sorted multiset differences.",
            "units": "energies and spectral differences in t; weights dimensionless exact rational numerator/denominator pairs",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:interface-finite-degree-square-identity through eq:interface-full-state-count"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:interface-isotypic-projector through eq:interface-isotypic-projector-completeness"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:interface-representation-coverage-fraction through eq:interface-nonabelian-completion-distance"},
            {"file": "source_current_195/02_ATOMIC_TASKS/TASK-37_CLEAN.tex", "section_or_equation": "finite-quotient representation-completeness qualification near lines 518-544"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {"status": "R04_VALIDATION_QUOTIENT", "quotient": "(Z/4Z)^4", "production_geometry": "MISSING"},
        "representation": {
            "status": "COMPLETE_FOR_EXPLICIT_FINITE_VALIDATION_QUOTIENT",
            "irrep_count": 256,
            "all_irreps_one_dimensional": True,
            "higher_dimensional_sector_dataset": "higher_dimensional_sectors.csv (header-only exact empty set)",
            "production_representation_catalogue": "MISSING",
        },
        "finite_cover": {
            "status": "VALIDATION_QUOTIENT_COMPLETE_PRODUCTION_QUOTIENT_MISSING",
            "cover_degree": 256,
            "representation_coverage_fraction": 1.0,
            "production_registry_id": "COV-M01",
        },
        "algorithm": {
            "name": "finite-abelian-peter-weyl-representation-completion",
            "implementation": "reproducibility/compute/p2_14_r07_representation_pipeline.py",
            "settings": {
                "modulus": 4,
                "rank": 4,
                "fourier_normalization": "1/sqrt(|Q|)",
                "character_convention": "chi_n(x)=exp(2*pi*i*n dot x/4)",
                "full_spectrum_solver": "scipy.linalg.eigvalsh(driver='evr')",
                "orthogonality_tolerance": 2.0e-13,
                "sector_leakage_tolerance_over_t": 2.0e-12,
                "spectrum_multiset_tolerance_over_t": 2.0e-9,
                "dos_enabled": False,
                "plotting_enabled": False,
            },
        },
        "environment": {"lock_file": "reproducibility/environment/environment-lock.json", "lock_sha256": environment_lock_sha256},
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "The finite Fourier dual, exact weights, and direct diagonalization are deterministic.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "AVAILABLE",
            "method": "unitarity, transformed-sector leakage, and independently diagonalized spectral-multiset residuals",
            "files": ["abelian_full_spectrum_comparison.csv", "peter_weyl_audit.json"],
            "justification": "Exact enumeration and rational weights are accompanied by floating-point reconstruction residuals.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    source_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "representations" / "z4_fourier.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r07_representation_completion.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R07",
        "status": "PASS_FOR_EXPLICIT_VALIDATION_QUOTIENT_WITH_PRODUCTION_QUOTIENT_MISSING",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "source_files": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in source_paths
        ],
        "registered_inputs": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in (source_dataset_path, matrix_path, source_audit_path)
        ],
        "output_files": [
            {"relative_path": path.relative_to(output_dir).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "gap_usage": {"installed": False, "required_for_validation_quotient": False, "production_nonabelian_quotient": "MISSING"},
        "forbidden_work": {"dos": False, "plotting": False},
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_representation_completion",
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
