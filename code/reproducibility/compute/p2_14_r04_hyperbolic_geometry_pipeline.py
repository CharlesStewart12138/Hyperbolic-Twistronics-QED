"""Clean-room hyperbolic-geometry-only reconstruction pipeline for P2-14-R04."""

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

from reproducibility.compute.p2_14_r04_hyperbolic_base_geometry import run as run_base  # noqa: E402
from reproducibility.compute.p2_14_r04_hyperbolic_quotient_geometry import run as run_quotient  # noqa: E402
from reproducibility.compute.p2_14_r04_validation_quotient import run as run_validation_quotient  # noqa: E402
from reproducibility.compute.p2_14_r04_hyperbolic_twist_geometry import run as run_twist  # noqa: E402


DATA_FILES = {
    "bolza_base_geometry.csv": "parameter",
    "bolza_vertices.csv": "coordinate",
    "group_generators.csv": "coordinate",
    "group_orbit_sample.csv": "coordinate",
    "base_geometry_checks.json": "diagnostic",
    "twist_displacement.csv": "raw",
    "local_moire_geometry.csv": "derived",
    "twist_geometry_checks.json": "diagnostic",
    "commensurability_cases.csv": "derived",
    "finite_quotient_requirements.csv": "parameter",
    "quotient_geometry_checks.json": "diagnostic",
    "validation_quotient_elements.csv": "coordinate",
    "validation_quotient_edges.csv": "coordinate",
    "validation_quotient_certificate.json": "diagnostic",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_record(path: Path, *, package: Path, role: str) -> dict[str, object]:
    return {
        "relative_path": path.relative_to(package).as_posix(),
        "role": role,
        "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def run(output_dir: Path, *, diagnostic_orbit_depth: int) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = run_base(output_dir, diagnostic_orbit_depth=diagnostic_orbit_depth)
    twist = run_twist(output_dir)
    quotient = run_quotient(output_dir)
    validation_quotient = run_validation_quotient(output_dir, modulus=4)

    parameter_registry = PROJECT_ROOT / "reproducibility" / "PARAMETER_REGISTRY.csv"
    environment_lock = PROJECT_ROOT / "reproducibility" / "environment" / "environment-lock.json"
    parameter_registry_sha256 = sha256_file(parameter_registry)
    environment_lock_sha256 = sha256_file(environment_lock)
    parameters = {
        "task_id": "P2-14-R04",
        "scope": "HYPERBOLIC_GEOMETRY_ONLY_NO_HAMILTONIAN_NO_SPECTRUM",
        "normalization": {
            "curvature_radius": "R = 1 coordinate convention; all reported lengths are divided by R",
            "curvature": "K R^2 = -1",
            "area": "reported in R^2",
            "orbitals_per_layer": 1,
        },
        "source_fixed_inputs": {
            "primitive_genus": 2,
            "regular_octagon_sides": 8,
            "interior_angle": "pi/4",
            "primitive_area_over_r2": "4*pi",
            "inradius_over_r": "acosh(1+sqrt(2))",
            "microscopic_spacing_over_r": "2*acosh(1+sqrt(2))",
            "vertex_disk_radius": "2^(-1/4)",
            "translation_parameter": "sqrt(2*(sqrt(2)-1))",
            "exact_bolza_twist_scan": "[0,pi/8]",
        },
        "diagnostic_settings": {
            "short_word_orbit_depth": diagnostic_orbit_depth,
            "classification": "CLEAN_ROOM_DIAGNOSTIC_SAMPLE_NOT_A_FINITE_QUOTIENT",
            "local_twist_cases": "source endpoints plus dyadic clean-room diagnostics",
            "finite_validation_quotient": "(Z/4Z)^4, clean-room validation only, not a production cover",
        },
        "missing_inputs": [
            {"parameter_id": "COV-M01", "role": "finite quotient tower/presentation", "state": "MISSING"},
            {"parameter_id": "COV-M02", "role": "cover degrees", "state": "MISSING"},
            {"parameter_id": "COV-M03", "role": "injectivity radii/certificates", "state": "MISSING"},
            {"parameter_id": "COV-M04", "role": "distance cutoff for unique-image condition", "state": "MISSING"},
            {"parameter_id": "R04-M01", "role": "nontrivial centred commensurator certificate and q_M", "state": "MISSING"},
            {"parameter_id": "R04-M02", "role": "subgroup generators for systole/injectivity evaluation", "state": "MISSING"},
            {"parameter_id": "R04-M03", "role": "embedded finite-quotient site coordinates", "state": "MISSING"},
        ],
        "parameter_registry": {
            "path": "reproducibility/PARAMETER_REGISTRY.csv",
            "sha256": parameter_registry_sha256,
        },
    }
    write_json(output_dir / "parameters.json", parameters)

    blocked = [
        {
            "component": "nontrivial_exact_commensurate_quotient",
            "reason": "No nontrivial fixed-centre commensurator certificate or coincidence index q_M is supplied.",
        },
        {
            "component": "finite_quotient_geometry",
            "reason": "COV-M01 and COV-M02 are MISSING; no quotient presentation, cover maps, or degree may be inferred.",
        },
        {
            "component": "injectivity_radius",
            "reason": "COV-M03 and subgroup word/matrix generators are MISSING; definitions are emitted but no numerical radius is claimed.",
        },
    ]
    summary = {
        "task_id": "P2-14-R04",
        "status": "PASS_WITH_PRODUCTION_INPUTS_MISSING",
        "task_acceptance_closed": True,
        "production_scientific_closure": False,
        "scope": "HYPERBOLIC_GEOMETRY_ONLY",
        "completed_components": [
            "exact normalized regular-octagon/Bolza primitive geometry",
            "SU(1,1) nearest-neighbour maps and a checked short-word group-orbit sample",
            "exact centred-twist displacement field at source-fixed radii",
            "exact local moire radius, effective area, and normalized geometric count",
            "common-group/commensurability identities and q_M=1 identity/C8 controls",
            "explicit finite-quotient and injectivity-radius input requirements",
            "explicit C8-invariant (Z/4Z)^4 validation quotient with 256 cosets and exact word injectivity radius 2",
        ],
        "production_open_components": blocked,
        "checks": {
            "base_geometry": base["status"],
            "local_twist_geometry": twist["status"],
            "quotient_identity_inputs": quotient["status"],
            "finite_validation_quotient": validation_quotient["status"],
            "hamiltonian_computed": False,
            "spectrum_computed": False,
        },
        "row_counts": {
            "group_orbit_sample": base["orbit_sample"]["orbit_point_count"],
            "twist_displacement": twist["displacement_row_count"],
            "local_moire_geometry": twist["moire_row_count"],
            "validation_quotient_elements": validation_quotient["cover_degree"],
            "validation_quotient_directed_edges": validation_quotient["directed_edge_count"],
        },
    }
    write_json(output_dir / "summary.json", summary)

    manifest_files = [file_record(output_dir / name, package=output_dir, role=role) for name, role in DATA_FILES.items()]
    dataset = {
        "schema_version": 1,
        "dataset_id": "p2-14-r04.hyperbolic-geometry-reconstruction",
        "status": "PARTIAL",
        "created_by_task": "P2-14-R04",
        "result_ids": ["R1", "R5", "R9"],
        "observable": {
            "name": "Bolza primitive geometry, local twist displacement, effective moire geometry, and quotient prerequisites",
            "definition": "Exact normalized hyperbolic geometry from declared equations; nontrivial finite quotients and injectivity radii remain absent where subgroup data are missing.",
            "units": "lengths in R, areas in R^2, angles in radians",
        },
        "theory_sources": [
            {"file": "source_current_195/main.tex", "section_or_equation": "I. Genus-two regular-octagon/Bolza-surface lattice; eq:platform-curvature through eq:platform-bolza-orbit-lattice"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Synthetic hyperbolic twist; eq:platform-two-layer-lattices and eq:platform-finite-cover-twist-distance"},
            {"file": "source_current_195/main.tex", "section_or_equation": "eq:disc-hyperbolic-twist-displacement through eq:disc-hyperbolic-effective-count"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Exact commensurability; eq:interface-hyperbolic-moire-group through eq:interface-bolza-supercell-data"},
            {"file": "source_current_195/main.tex", "section_or_equation": "Finite-cover injectivity radius; eq:fc-cover-systole through eq:fc-word-injectivity-radius"},
        ],
        "parameter_registry_sha256": parameter_registry_sha256,
        "geometry": {
            "status": "EXACT_PRIMITIVE_LOCAL_AND_VALIDATION_QUOTIENT",
            "curvature": "K=-1/R^2",
            "primitive": "genus-two regular octagon with one centre orbit",
            "finite_quotient": "VALIDATION_QUOTIENT_AVAILABLE_PRODUCTION_INPUTS_MISSING",
        },
        "representation": {
            "status": "GEOMETRY_ONLY",
            "group": "Gamma_B subset PSL(2,R) represented by SU(1,1) disk maps",
            "spectral_representation": "NOT_COMPUTED",
        },
        "finite_cover": {
            "status": "VALIDATION_QUOTIENT_AVAILABLE_PRODUCTION_INPUTS_MISSING",
            "required_registry_ids": ["COV-M01", "COV-M02", "COV-M03", "COV-M04"],
            "definitions_file": "quotient_geometry_checks.json",
            "validation_quotient": "(Z/4Z)^4",
            "validation_cover_degree": 256,
            "validation_word_injectivity_radius": 2.0,
        },
        "algorithm": {
            "name": "exact-bolza-hyperbolic-geometry-pipeline",
            "implementation": "reproducibility/compute/p2_14_r04_hyperbolic_geometry_pipeline.py",
            "settings": {
                "diagnostic_orbit_depth": diagnostic_orbit_depth,
                "orbit_is_finite_quotient": False,
                "hamiltonian_enabled": False,
                "spectrum_enabled": False,
                "validation_quotient_modulus": 4,
                "validation_quotient_is_production_cover": False,
            },
        },
        "environment": {
            "lock_file": "reproducibility/environment/environment-lock.json",
            "lock_sha256": environment_lock_sha256,
        },
        "stochastic": {
            "status": "NOT_APPLICABLE",
            "reason": "All primitive and local geometry controls are deterministic formula evaluations.",
            "seed_config_sha256": None,
            "streams": [],
        },
        "files": manifest_files,
        "uncertainty": {
            "status": "MISSING", "method": None, "files": [],
            "justification": "Exact local formulas have only floating residuals, but finite-cover and injectivity uncertainty cannot be evaluated without the missing quotient data.",
        },
        "plotting": {"compute_plot_separated": True, "raw_data_is_source": True, "plot_scripts": []},
    }
    write_json(output_dir / "dataset.json", dataset)

    script_paths = [
        PROJECT_ROOT / "reproducibility" / "src" / "hyperbolic" / "bolza.py",
        PROJECT_ROOT / "reproducibility" / "src" / "hyperbolic" / "local_twist.py",
        PROJECT_ROOT / "reproducibility" / "src" / "hyperbolic" / "finite_quotient.py",
        PROJECT_ROOT / "reproducibility" / "src" / "hyperbolic" / "validation_quotient.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r04_hyperbolic_base_geometry.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r04_hyperbolic_twist_geometry.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r04_hyperbolic_quotient_geometry.py",
        PROJECT_ROOT / "reproducibility" / "compute" / "p2_14_r04_validation_quotient.py",
        Path(__file__).resolve(),
    ]
    provenance = {
        "task_id": "P2-14-R04", "status": "PASS_WITH_PRODUCTION_INPUTS_MISSING", "scope": "HYPERBOLIC_GEOMETRY_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "command": f"python reproducibility/compute/p2_14_r04_hyperbolic_geometry_pipeline.py --output-dir {output_dir.as_posix()} --diagnostic-orbit-depth {diagnostic_orbit_depth}",
        "source_files": [
            {
                "relative_path": path.relative_to(PROJECT_ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in script_paths
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
        "production_open_components": blocked,
        "hamiltonian_computed": False,
        "spectrum_computed": False,
    }
    write_json(output_dir / "run_manifest.json", provenance)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "hyperbolic_geometry_reconstruction",
    )
    parser.add_argument("--diagnostic-orbit-depth", type=int, default=3)
    args = parser.parse_args()
    if args.diagnostic_orbit_depth < 0:
        parser.error("--diagnostic-orbit-depth must be non-negative")
    print(json.dumps(run(args.output_dir, diagnostic_orbit_depth=args.diagnostic_orbit_depth), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
