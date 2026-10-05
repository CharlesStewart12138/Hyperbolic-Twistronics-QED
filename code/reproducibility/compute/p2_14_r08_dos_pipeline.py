"""Package the registered exact/KPM/SLQ DOS reconstruction for P2-14-R08."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.compute.p2_14_r08_dos_analysis import run as run_dos  # noqa: E402
from reproducibility.random.seed_registry import config_sha256, load_seed_config  # noqa: E402


DATA_FILES = {
    "exact_spectrum.csv": "raw",
    "dos_cdf.csv": "raw",
    "kpm_moments.csv": "uncertainty",
    "slq_atoms.csv": "raw",
    "broadening_dos.csv": "raw",
    "broadening_schedule.csv": "parameter",
    "resolved_dos.csv": "raw",
    "dos_audit.json": "uncertainty",
    "dos_config.json": "parameter",
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


def run(output_dir: Path, *, hamiltonian_package: Path, spectral_package: Path, config_path: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    hamiltonian_audit_path = hamiltonian_package / "hamiltonian_audits.json"
    hamiltonian_dataset_path = hamiltonian_package / "dataset.json"
    matrix_path = hamiltonian_package / "bilayer_h1_coo.csv"
    spectral_dataset_path = spectral_package / "dataset.json"
    registered_spectrum_path = spectral_package / "finite_spectrum.csv"
    hamiltonian_audit = json.loads(hamiltonian_audit_path.read_text(encoding="utf-8"))
    hamiltonian_dataset = json.loads(hamiltonian_dataset_path.read_text(encoding="utf-8"))
    spectral_dataset = json.loads(spectral_dataset_path.read_text(encoding="utf-8"))
    dimension = int(hamiltonian_audit["bilayer_dimension"])
    w_star_over_t = float(hamiltonian_audit["parameters"]["w_star_over_t"])
    audit = run_dos(
        output_dir,
        matrix_path=matrix_path,
        registered_spectrum_path=registered_spectrum_path,
        config_path=config_path,
        dimension=dimension,
        w_star_over_t=w_star_over_t,
    )
    if audit["status"] != "PASS":
        raise RuntimeError("R08 DOS analysis failed")
    shutil.copyfile(config_path, output_dir / "dos_config.json")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    seed_config = load_seed_config()
    seed_hash = config_sha256()
    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    production_missing = [
        {"parameter_id": "PHY-M02", "role": "physical t scale", "state": "MISSING"},
        {"parameter_id": "COV-M01", "role": "production cover/tower", "state": "MISSING"},
        {"parameter_id": "NUM-M04", "role": "production broadening schedule", "state": "MISSING"},
        {"parameter_id": "NUM-M05", "role": "production KPM order and probe batches", "state": "MISSING"},
        {"parameter_id": "NUM-M06", "role": "production SLQ depth and probe batches", "state": "MISSING"},
        {"parameter_id": "NUM-M08", "role": "production target projector ancestry", "state": "MISSING"},
    ]
    parameters = {
        "task_id": "P2-14-R08",
        "scope": "DOS_ONLY_ON_REGISTERED_512_DIMENSIONAL_VALIDATION_HAMILTONIAN_NO_COVER_CONVERGENCE_NO_PLOTTING",
        "registered_inputs": {
            "hamiltonian_dataset_id": hamiltonian_dataset["dataset_id"],
            "hamiltonian_dataset_sha256": sha256_file(hamiltonian_dataset_path),
            "spectral_dataset_id": spectral_dataset["dataset_id"],
            "spectral_dataset_sha256": sha256_file(spectral_dataset_path),
            "matrix_sha256": sha256_file(matrix_path),
            "registered_spectrum_sha256": sha256_file(registered_spectrum_path),
            "dimension": dimension,
        },
        "validation_configuration": config,
        "random_policy": {
            "policy_version": seed_config["policy_version"],
            "seed_config_path": "reproducibility/random/seeds.json",
            "seed_config_sha256": seed_hash,
            "bit_generator": seed_config["numpy_bit_generator"],
        },
        "production_missing_inputs": production_missing,
        "parameter_registry": {"path": "reproducibility/PARAMETER_REGISTRY.csv", "sha256": parameter_registry_sha256},
    }
    write_json(output_dir / "parameters.json", parameters)

    metrics = audit["metrics"]
    summary = {
        "task_id": "P2-14-R08",
        "status": "PASS_WITH_PRODUCTION_DOS_SETTINGS_AND_COVER_MISSING",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "EXACT_KPM_SLQ_CDF_BROADENED_AND_RESOLVED_DOS",
        "completed_components": [
            "exact 512-state finite-system spectrum and normalized empirical CDF",
            "four independent registered KPM batches with Jackson damping, moment tables, CDF, and batch standard errors",
            "four independent registered SLQ batches with atom/weight tables, CDF, and batch standard errors",
            "three fixed Lorentzian broadening levels with exact, KPM-convolved, and SLQ densities",
            "global, per-layer, two origin-site local, layer-even, layer-odd, and target-root-projector resolved DOS",
        ],
        "key_metrics": metrics,
        "broadening_schedule": audit["broadening_schedule"],
        "target_root_rank": audit["target_root_rank"],
        "explicit_exclusions": ["finite-cover/tower convergence (P2-14-R09)", "production DOS claim", "plotting"],
        "production_open_inputs": production_missing,
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, package=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r08.hyperbolic-dos-reconstruction",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R08",
        "result_ids": ["R6", "R8"],
        "observable": {
            "name": "Exact, KPM, SLQ, cumulative, broadened, local, and projector-resolved density of states",
            "definition": "The normalized trace spectral measure of the registered finite Hamiltonian, its Jackson-KPM and stochastic-Lanczos estimates, empirical cumulative distributions, Lorentzian convolutions, and explicitly normalized local/projector restrictions.",
            "units": "energies and eta in t; DOS in t^-1; CDF and spectral weights dimensionless",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:obs-complete-finite-cluster-DOS through eq:obs-finite-broadened-DOS"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:obs-layer-resolved-DOS and eq:obs-local-DOS"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:obs-KPM-rescaling-parameters through eq:obs-stochastic-KPM-moment"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:obs-SLQ-measure through eq:obs-KPM-SLQ-DOS-distance"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {"status": "R04_VALIDATION_QUOTIENT", "quotient": "(Z/4Z)^4", "production_geometry": "MISSING"},
        "representation": {
            "status": "COMPLETE_FINITE_MATRIX_TRACE_MEASURE_FOR_VALIDATION_QUOTIENT",
            "resolved_projectors": ["layer_1", "layer_2", "layer_even", "layer_odd", "target_root"],
        },
        "finite_cover": {
            "status": "SINGLE_VALIDATION_QUOTIENT_ONLY_PRODUCTION_TOWER_MISSING",
            "cover_degree": dimension // 2,
            "convergence": "DEFERRED_TO_P2-14-R09",
        },
        "algorithm": {
            "name": "exact-kpm-slq-resolved-dos",
            "implementation": "reproducibility/compute/p2_14_r08_dos_pipeline.py",
            "settings": {
                "config_file": "dos_config.json",
                "exact_solver": "scipy.linalg.eigh(driver='evr')",
                "KPM": "stochastic Chebyshev moments with Jackson damping",
                "SLQ": "fully reorthogonalized Lanczos quadrature",
                "broadening_kernel": "Lorentzian eta/[pi(E^2+eta^2)]",
                "cover_convergence_enabled": False,
                "plotting_enabled": False,
            },
        },
        "environment": {"lock_file": "reproducibility/environment/environment-lock.json", "lock_sha256": environment_lock_sha256},
        "stochastic": {
            "status": "USED",
            "reason": "KPM trace moments and SLQ quadrature use independent registered random-vector batches.",
            "seed_config_sha256": seed_hash,
            "streams": [
                {"namespace": config["kpm"]["namespace"], "first_index": min(config["kpm"]["batch_stream_indices"]), "count": len(config["kpm"]["batch_stream_indices"])},
                {"namespace": config["slq"]["namespace"], "first_index": min(config["slq"]["batch_stream_indices"]), "count": len(config["slq"]["batch_stream_indices"])},
            ],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "AVAILABLE",
            "method": "independent registered KPM/SLQ batches, exact finite-spectrum reference, moment/CDF discrepancies, and fixed-broadening method comparisons",
            "files": ["kpm_moments.csv", "dos_audit.json"],
            "justification": "Stochastic, polynomial, quadrature, grid, and broadening diagnostics are explicit for the validation Hamiltonian; cover/shell uncertainty remains outside R08.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    source_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "spectrum" / "stochastic_dos.py",
        PROJECT_ROOT / "reproducibility" / "src" / "spectrum" / "resolved_dos.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r08_dos_analysis.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R08",
        "status": "PASS_WITH_PRODUCTION_DOS_SETTINGS_AND_COVER_MISSING",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "source_files": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in source_paths
        ],
        "registered_inputs": [
            {"relative_path": path.relative_to(PROJECT_ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in (hamiltonian_dataset_path, matrix_path, spectral_dataset_path, registered_spectrum_path, config_path)
        ],
        "random_streams": dataset["stochastic"]["streams"],
        "seed_config_sha256": seed_hash,
        "output_files": [
            {"relative_path": path.relative_to(output_dir).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(output_dir.iterdir())
            if path.is_file() and path.name != "run_manifest.json"
        ],
        "forbidden_work": {"cover_convergence": False, "plotting": False},
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_dos_reconstruction",
    )
    parser.add_argument(
        "--hamiltonian-package", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_hamiltonian_reconstruction",
    )
    parser.add_argument(
        "--spectral-package", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_spectral_reconstruction",
    )
    parser.add_argument(
        "--config", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "spectrum" / "p2_14_r08_config.json",
    )
    args = parser.parse_args()
    print(json.dumps(run(
        args.output_dir,
        hamiltonian_package=args.hamiltonian_package,
        spectral_package=args.spectral_package,
        config_path=args.config,
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
