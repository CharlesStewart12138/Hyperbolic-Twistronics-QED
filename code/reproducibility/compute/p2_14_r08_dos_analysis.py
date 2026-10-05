"""Exact, KPM, SLQ, CDF, broadening, and resolved-DOS analysis for P2-14-R08."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import scipy.linalg


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from reproducibility.random.seed_registry import numpy_rng  # noqa: E402
from reproducibility.src.spectrum.finite_registered import load_coo_csv  # noqa: E402
from reproducibility.src.spectrum.resolved_dos import (  # noqa: E402
    convolve_grid_density,
    exact_resolved_weights,
    lorentzian_density,
    normalize_on_grid,
)
from reproducibility.src.spectrum.stochastic_dos import (  # noqa: E402
    cdf_from_atoms,
    cdf_from_density,
    kpm_density,
    scale_hermitian,
    slq_quadrature,
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_registered_spectrum(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return np.asarray([float(row["energy_over_t"]) for row in csv.DictReader(handle)], dtype=float)


def relative_error(candidate: float, reference: float) -> float:
    return abs(candidate - reference) / max(abs(reference), 1.0)


def run(
    output_dir: Path,
    *,
    matrix_path: Path,
    registered_spectrum_path: Path,
    config_path: Path,
    dimension: int,
    w_star_over_t: float,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    matrix = load_coo_csv(matrix_path, dimension=dimension)
    exact_values, exact_vectors = scipy.linalg.eigh(matrix.toarray(), driver="evr", check_finite=True)
    registered_values = np.sort(read_registered_spectrum(registered_spectrum_path))
    registered_residual = float(np.max(np.abs(np.sort(exact_values) - registered_values)))
    span = float(exact_values[-1] - exact_values[0])
    padding = float(config["bound_padding_fraction"]) * span
    lower = float(exact_values[0] - padding)
    upper = float(exact_values[-1] + padding)
    scaled, scaling = scale_hermitian(matrix, lower=lower, upper=upper)

    kpm_settings = config["kpm"]
    kpm_batches = []
    for batch_index, stream_index in enumerate(kpm_settings["batch_stream_indices"]):
        result = kpm_density(
            scaled,
            scaling,
            moment_count=int(kpm_settings["moment_count"]),
            probe_count=int(kpm_settings["probe_count_per_batch"]),
            rng=numpy_rng(str(kpm_settings["namespace"]), int(stream_index)),
            grid_size=int(config["cdf_grid_size"]),
        )
        result["batch_index"] = batch_index
        result["stream_index"] = int(stream_index)
        kpm_batches.append(result)
    energy_grid = np.asarray(kpm_batches[0]["energy"])
    kpm_density_batches = np.asarray([np.asarray(batch["density"]) for batch in kpm_batches])
    kpm_cdf_batches = np.asarray([cdf_from_density(energy_grid, density) for density in kpm_density_batches])
    kpm_density_mean = np.mean(kpm_density_batches, axis=0)
    kpm_density_mean, _ = normalize_on_grid(energy_grid, kpm_density_mean)
    kpm_cdf_mean = cdf_from_density(energy_grid, kpm_density_mean)
    kpm_cdf_se = np.std(kpm_cdf_batches, axis=0, ddof=1) / np.sqrt(len(kpm_batches))
    kpm_moments = np.asarray([np.asarray(batch["moments"]) for batch in kpm_batches])

    slq_settings = config["slq"]
    slq_batches = []
    slq_cdf_batches = []
    for batch_index, stream_index in enumerate(slq_settings["batch_stream_indices"]):
        result = slq_quadrature(
            scaled,
            scaling,
            depth=int(slq_settings["lanczos_depth"]),
            probe_count=int(slq_settings["probe_count_per_batch"]),
            rng=numpy_rng(str(slq_settings["namespace"]), int(stream_index)),
            breakdown_tolerance=float(slq_settings["breakdown_tolerance"]),
        )
        result["batch_index"] = batch_index
        result["stream_index"] = int(stream_index)
        slq_batches.append(result)
        slq_cdf_batches.append(cdf_from_atoms(energy_grid, np.asarray(result["atoms"]), np.asarray(result["weights"])))
    slq_cdf_batches_array = np.asarray(slq_cdf_batches)
    slq_cdf_mean = np.mean(slq_cdf_batches_array, axis=0)
    slq_cdf_se = np.std(slq_cdf_batches_array, axis=0, ddof=1) / np.sqrt(len(slq_batches))
    slq_atoms = np.concatenate([np.asarray(batch["atoms"]) for batch in slq_batches])
    slq_weights = np.concatenate([np.asarray(batch["weights"]) / len(slq_batches) for batch in slq_batches])

    exact_weights = np.full(dimension, 1.0 / dimension)
    exact_cdf = cdf_from_atoms(energy_grid, exact_values, exact_weights)
    cdf_rows = [
        {
            "grid_index": index,
            "energy_over_t": float(energy),
            "exact_empirical_cdf": float(exact_cdf[index]),
            "kpm_density_over_t_inverse": float(kpm_density_mean[index]),
            "kpm_cdf": float(kpm_cdf_mean[index]),
            "kpm_cdf_batch_standard_error": float(kpm_cdf_se[index]),
            "slq_cdf": float(slq_cdf_mean[index]),
            "slq_cdf_batch_standard_error": float(slq_cdf_se[index]),
        }
        for index, energy in enumerate(energy_grid)
    ]
    write_csv(output_dir / "dos_cdf.csv", cdf_rows, list(cdf_rows[0]))

    scaled_exact = (exact_values - scaling.center) / scaling.radius
    angles = np.arccos(np.clip(scaled_exact, -1.0, 1.0))
    exact_moments = np.asarray([float(np.mean(np.cos(order * angles))) for order in range(int(kpm_settings["moment_count"]))])
    moment_rows = []
    for order in range(exact_moments.size):
        batch_values = kpm_moments[:, order]
        row = {
            "moment_order": order,
            "exact_moment": float(exact_moments[order]),
            "kpm_batch_mean": float(np.mean(batch_values)),
            "kpm_batch_standard_error": float(np.std(batch_values, ddof=1) / np.sqrt(len(batch_values))),
            "absolute_error": float(abs(np.mean(batch_values) - exact_moments[order])),
        }
        for batch_index, value in enumerate(batch_values):
            row[f"kpm_batch_{batch_index}"] = float(value)
        moment_rows.append(row)
    write_csv(output_dir / "kpm_moments.csv", moment_rows, list(moment_rows[0]))

    atom_rows = []
    for batch in slq_batches:
        for atom_index, (atom, weight) in enumerate(zip(batch["atoms"], batch["weights"])):
            atom_rows.append({
                "batch_index": batch["batch_index"],
                "stream_index": batch["stream_index"],
                "atom_index": atom_index,
                "energy_over_t": float(atom),
                "within_batch_weight": float(weight),
                "aggregate_weight": float(weight) / len(slq_batches),
            })
    write_csv(output_dir / "slq_atoms.csv", atom_rows, list(atom_rows[0]))
    exact_rows = [
        {"eigenvalue_index": index, "energy_over_t": float(value), "normalized_weight": 1.0 / dimension}
        for index, value in enumerate(exact_values)
    ]
    write_csv(output_dir / "exact_spectrum.csv", exact_rows, list(exact_rows[0]))

    broadening_fractions = [float(value) for value in config["broadening_fractions_of_spectral_span"]]
    etas = [fraction * span for fraction in broadening_fractions]
    tail = float(config["broadening_tail_multiple"]) * max(etas)
    broadening_grid = np.linspace(float(exact_values[0] - tail), float(exact_values[-1] + tail), int(config["broadening_grid_size"]))
    broadening_rows = []
    broadening_metrics = []
    for schedule_index, (fraction, eta) in enumerate(zip(broadening_fractions, etas)):
        exact_density, exact_raw_mass = normalize_on_grid(
            broadening_grid,
            lorentzian_density(broadening_grid, exact_values, exact_weights, eta),
        )
        kpm_broadened, kpm_raw_mass = normalize_on_grid(
            broadening_grid,
            convolve_grid_density(broadening_grid, energy_grid, kpm_density_mean, eta),
        )
        slq_density, slq_raw_mass = normalize_on_grid(
            broadening_grid,
            lorentzian_density(broadening_grid, slq_atoms, slq_weights, eta),
        )
        broadening_metrics.append({
            "schedule_index": schedule_index,
            "eta_over_t": eta,
            "eta_over_spectral_span": fraction,
            "exact_raw_grid_mass": exact_raw_mass,
            "kpm_raw_grid_mass": kpm_raw_mass,
            "slq_raw_grid_mass": slq_raw_mass,
            "kpm_exact_density_linf": float(np.max(np.abs(kpm_broadened - exact_density))),
            "slq_exact_density_linf": float(np.max(np.abs(slq_density - exact_density))),
            "kpm_slq_density_linf": float(np.max(np.abs(kpm_broadened - slq_density))),
        })
        for grid_index, energy in enumerate(broadening_grid):
            broadening_rows.append({
                "schedule_index": schedule_index,
                "eta_over_t": eta,
                "eta_over_spectral_span": fraction,
                "grid_index": grid_index,
                "energy_over_t": float(energy),
                "exact_lorentzian_dos_over_t_inverse": float(exact_density[grid_index]),
                "kpm_then_lorentzian_dos_over_t_inverse": float(kpm_broadened[grid_index]),
                "slq_lorentzian_dos_over_t_inverse": float(slq_density[grid_index]),
            })
    write_csv(output_dir / "broadening_dos.csv", broadening_rows, list(broadening_rows[0]))
    write_csv(output_dir / "broadening_schedule.csv", broadening_metrics, list(broadening_metrics[0]))

    target_mask = np.abs(exact_values - w_star_over_t) <= 2.0e-9
    resolved_weights = exact_resolved_weights(exact_vectors, target_mask=target_mask)
    reference_eta = float(config["resolved_dos_reference_fraction"]) * span
    resolved_rows = []
    resolved_density: dict[str, np.ndarray] = {}
    resolved_masses: dict[str, float] = {}
    for resolution_id, weights in resolved_weights.items():
        raw_density = lorentzian_density(broadening_grid, exact_values, weights, reference_eta)
        if resolution_id in {"layer_1", "layer_2"}:
            resolved_density[resolution_id] = raw_density
            resolved_masses[resolution_id] = float(np.trapz(raw_density, broadening_grid))
        else:
            normalized, raw_mass = normalize_on_grid(broadening_grid, raw_density)
            resolved_density[resolution_id] = normalized
            resolved_masses[resolution_id] = raw_mass
    layer_global_raw = resolved_density["layer_1"] + resolved_density["layer_2"]
    global_mass = float(np.trapz(layer_global_raw, broadening_grid))
    resolved_density["layer_1"] /= global_mass
    resolved_density["layer_2"] /= global_mass
    for resolution_id, density_values in resolved_density.items():
        resolution_type = "global"
        if resolution_id.startswith("layer_") and resolution_id not in {"layer_even_projector", "layer_odd_projector"}:
            resolution_type = "layer"
        if resolution_id.startswith("local_"):
            resolution_type = "local"
        if resolution_id.endswith("projector"):
            resolution_type = "projector"
        for grid_index, energy in enumerate(broadening_grid):
            resolved_rows.append({
                "resolution_id": resolution_id,
                "resolution_type": resolution_type,
                "eta_over_t": reference_eta,
                "grid_index": grid_index,
                "energy_over_t": float(energy),
                "density_over_t_inverse": float(density_values[grid_index]),
            })
    write_csv(output_dir / "resolved_dos.csv", resolved_rows, list(resolved_rows[0]))

    exact_mean = float(np.mean(exact_values))
    exact_variance = float(np.mean(np.square(exact_values - exact_mean)))
    kpm_mean = float(np.trapz(energy_grid * kpm_density_mean, energy_grid))
    kpm_variance = float(np.trapz(np.square(energy_grid - kpm_mean) * kpm_density_mean, energy_grid))
    slq_mean = float(np.sum(slq_weights * slq_atoms))
    slq_variance = float(np.sum(slq_weights * np.square(slq_atoms - slq_mean)))
    metrics = {
        "registered_exact_spectrum_linf_over_t": registered_residual,
        "kpm_exact_cdf_linf": float(np.max(np.abs(kpm_cdf_mean - exact_cdf))),
        "slq_exact_cdf_linf": float(np.max(np.abs(slq_cdf_mean - exact_cdf))),
        "kpm_slq_cdf_linf": float(np.max(np.abs(kpm_cdf_mean - slq_cdf_mean))),
        "kpm_mean_over_span_error": abs(kpm_mean - exact_mean) / span,
        "slq_mean_over_span_error": abs(slq_mean - exact_mean) / span,
        "kpm_variance_relative_error": relative_error(kpm_variance, exact_variance),
        "slq_variance_relative_error": relative_error(slq_variance, exact_variance),
        "kpm_batch_cdf_standard_error_max": float(np.max(kpm_cdf_se)),
        "slq_batch_cdf_standard_error_max": float(np.max(slq_cdf_se)),
        "resolved_sum_rule_linf": float(np.max(np.abs(
            resolved_density["layer_1"] + resolved_density["layer_2"] - resolved_density["global"]
        ))),
        "projector_mass_error": max(
            abs(float(np.trapz(resolved_density[name], broadening_grid)) - 1.0)
            for name in ("layer_even_projector", "layer_odd_projector", "target_root_projector")
        ),
    }
    tolerances = {key: float(value) for key, value in config["audit_tolerances"].items()}
    checks = {key: metrics[key] <= limit for key, limit in tolerances.items()}
    audit = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "dimension": dimension,
        "exact_spectral_bounds_over_t": {"lower": float(exact_values[0]), "upper": float(exact_values[-1])},
        "scaled_bounds_over_t": {"lower": lower, "upper": upper},
        "target_root_rank": int(np.count_nonzero(target_mask)),
        "exact_moments": {"mean_over_t": exact_mean, "variance_over_t2": exact_variance},
        "estimated_moments": {
            "kpm_mean_over_t": kpm_mean,
            "kpm_variance_over_t2": kpm_variance,
            "slq_mean_over_t": slq_mean,
            "slq_variance_over_t2": slq_variance,
        },
        "metrics": metrics,
        "tolerances": tolerances,
        "checks": checks,
        "failed_checks": sorted(key for key, passed in checks.items() if not passed),
        "broadening_schedule": broadening_metrics,
        "resolved_raw_grid_masses": resolved_masses,
        "kpm_batches": [
            {
                "namespace": kpm_settings["namespace"],
                "stream_index": batch["stream_index"],
                "moment_count": batch["moment_count"],
                "probe_count": batch["probe_count"],
                "mass_before_normalization": batch["mass_before_normalization"],
            }
            for batch in kpm_batches
        ],
        "slq_batches": [
            {
                "namespace": slq_settings["namespace"],
                "stream_index": batch["stream_index"],
                "requested_depth": batch["requested_depth"],
                "probe_count": batch["probe_count"],
                "minimum_realized_depth": batch["minimum_realized_depth"],
                "maximum_realized_depth": batch["maximum_realized_depth"],
                "mass_before_normalization": batch["mass_before_normalization"],
            }
            for batch in slq_batches
        ],
    }
    (output_dir / "dos_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if audit["status"] != "PASS":
        raise RuntimeError("R08 DOS validation failed")
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--matrix-path", type=Path, required=True)
    parser.add_argument("--registered-spectrum-path", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--w-star-over-t", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(run(
        args.output_dir,
        matrix_path=args.matrix_path,
        registered_spectrum_path=args.registered_spectrum_path,
        config_path=args.config,
        dimension=args.dimension,
        w_star_over_t=args.w_star_over_t,
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
