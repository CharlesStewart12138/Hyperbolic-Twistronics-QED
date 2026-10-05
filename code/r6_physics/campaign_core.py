"""Numerical core for the four R6 physics programs.

All generic angles use exact universal-cover Dirichlet restrictions.  No
generic periodic cell is constructed anywhere in this file.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import sys
import time

import h5py
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
from scipy.sparse.linalg import expm_multiply


ROOT = Path(__file__).resolve().parent
BUILDERS = ROOT / "02_OPERATOR_BUILDERS"
if str(BUILDERS) not in sys.path:
    sys.path.insert(0, str(BUILDERS))

from commensurate_angles import THETA_C, THETA_MAX, approximation_sequences, enumerate_exact_angles, generic_angles, nearby_generic
from geometry import load_orbit_patch
from green_function import green_entries
from group_inputs import file_sha256, write_frozen_manifest
from local_operator import ScalarBilayerParameters, build_local_bilayer, schur_row_sum_bound
from observables import dynamical_observables, eigensystem_summary, gaussian_ldos, spectral_moments
from qa import check_qstar_manifest_hash, frozen_inputs_present, sparse_hermiticity_defect
from time_evolution import evolve


RAW = ROOT / "10_RAW_DATA"
PROCESSED = ROOT / "11_PROCESSED_DATA"
LOGS = ROOT / "logs"
CHECKPOINTS = ROOT / "checkpoints"
for directory in (RAW, PROCESSED, LOGS, CHECKPOINTS):
    directory.mkdir(parents=True, exist_ok=True)

SEED = 5203006
ETA = 1.0
PRIMARY_DEPTH = 2
OMEGA_VALUES = np.asarray([0.0, 0.25, 0.50, 0.75, 0.90, 0.97, 1.00, 1.03, 1.10, 1.25, 1.50, 2.00])
LAMBDA_VALUES = np.asarray([0.125, 0.20, 0.25])


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(message: str) -> None:
    stamp = utc_now()
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (LOGS / "campaign.log").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def metadata(phenomenon: str, extra: dict[str, object] | None = None) -> dict[str, object]:
    value: dict[str, object] = {
        "phenomenon": phenomenon,
        "model_version": "R6-scalar-frozen-v1",
        "r4_root": "00_FROZEN_INPUTS/QSTAR_ARTIFACTS",
        "r5_root": "00_FROZEN_INPUTS/R5_COMMENSURATOR",
        "boundary_semantics": "generic: exact universal-cover Dirichlet restriction; theta=0: Q* periodic available",
        "solver": "dense Hermitian eigensystem for depth-2 local scans; sparse Krylov for dynamics",
        "tolerance": 1e-10,
        "precision": "float64/complex128",
        "seed": SEED,
        "timestamp_utc": utc_now(),
        "hardware": platform.platform(),
        "python": sys.version,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "code_sha256": file_sha256(Path(__file__)),
    }
    if extra:
        value.update(extra)
    return value


def _write_h5(path: Path, arrays: dict[str, np.ndarray], attrs: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    with h5py.File(temporary, "w") as handle:
        for key, value in arrays.items():
            handle.create_dataset(key, data=np.asarray(value), compression="gzip", compression_opts=4, shuffle=True)
        for key, value in attrs.items():
            handle.attrs[key] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list, tuple)) else value
    temporary.replace(path)


def _write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    lines = ["\t".join(keys)]
    for row in rows:
        lines.append("\t".join("" if row.get(key) is None else str(row.get(key)) for key in keys))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dense_record(theta: float, omega: float = 1.0, decay: float = 0.20, depth: int = PRIMARY_DEPTH, energy: np.ndarray | None = None) -> dict[str, object]:
    patch = load_orbit_patch(depth)
    parameters = ScalarBilayerParameters(theta=float(theta), omega_over_omega_ref=float(omega), lambda_perp_over_a=float(decay))
    model = build_local_bilayer(patch, parameters)
    dense = model.hamiltonian.toarray()
    eigenvalues, eigenvectors = np.linalg.eigh(dense)
    n = patch.size
    summary = eigensystem_summary(eigenvalues, eigenvectors, n)
    weights = np.abs(eigenvectors[0]) ** 2
    weights_upper = np.abs(eigenvectors[n]) ** 2
    normalized_energy = eigenvalues / max(np.max(np.abs(eigenvalues)), 1e-15)
    moments = np.asarray([np.sum(weights * normalized_energy**order) for order in range(9)])
    z = 1j * ETA
    green00 = np.sum(weights / (z - eigenvalues))
    return_fixed = np.asarray([abs(np.sum(weights * np.exp(-1j * eigenvalues * t))) ** 2 for t in (0.05, 0.10, 0.20, 0.50)])
    result: dict[str, object] = {
        "patch": patch,
        "model": model,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "summary": summary,
        "moments": moments,
        "green00": green00,
        "return_fixed": return_fixed,
        "row_sum_bound": schur_row_sum_bound(patch, parameters),
        "hermiticity_defect": sparse_hermiticity_defect(model.hamiltonian),
    }
    if energy is not None:
        result["ldos_lower"] = gaussian_ldos(eigenvalues, eigenvectors, 0, energy, ETA)
        result["ldos_upper"] = gaussian_ldos(eigenvalues, eigenvectors, n, energy, ETA)
    return result


def _stack_summary(records: list[dict[str, object]]) -> tuple[list[str], np.ndarray]:
    names = list(records[0]["summary"].keys())
    return names, np.asarray([[record["summary"][name] for name in names] for record in records], dtype=float)


def compute_phenomenon_i(force: bool = False) -> Path:
    path = RAW / "phenomenon_I_local_global.h5"
    if path.exists() and not force:
        log("Phenomenon I checkpoint found")
        return path
    log("Phenomenon I: local/global spectral split")
    thetas = np.linspace(0.0, THETA_MAX, 33)
    energy = np.linspace(-165.0, 165.0, 401)
    records = [dense_record(theta, energy=energy) for theta in thetas]
    names, summaries = _stack_summary(records)

    selected_indices = np.asarray([0, 8, 16, 24, 32])
    distance_grid = np.asarray(records[0]["patch"].radii_over_a)
    green_profiles = []
    for index in selected_indices:
        record = records[int(index)]
        values = green_entries(record["model"].hamiltonian, 0.0, ETA, [(site, 0) for site in range(record["patch"].size)])
        green_profiles.append(np.abs(values))

    times = np.linspace(0.0, 2.0, 81)
    initial_labels = ["site", "layer_compact", "symmetric"]
    dynamic_names = ["survival", "return_probability", "mean_radius", "mean_square_radius", "participation", "layer_imbalance", "entropy"]
    dynamics = np.zeros((len(selected_indices), len(initial_labels), len(dynamic_names), len(times)))
    norm_defects = np.zeros((len(selected_indices), len(initial_labels)))
    for ai, index in enumerate(selected_indices):
        record = records[int(index)]
        patch, model = record["patch"], record["model"]
        n = patch.size
        single = np.zeros(2 * n); single[0] = 1.0
        compact = np.zeros(2 * n); compact[0] = 1.0
        neighbours = patch.adjacency.getrow(0).indices
        compact[neighbours] = 1.0
        symmetric = np.zeros(2 * n); symmetric[0] = symmetric[n] = 1.0
        for si, initial in enumerate((single, compact, symmetric)):
            trace = evolve(model.hamiltonian, initial, times)
            obs = dynamical_observables(trace.states, initial, patch.radii_over_a, n)
            dynamics[ai, si] = np.asarray([obs[name] for name in dynamic_names])
            norm_defects[ai, si] = trace.norm_residual

    arrays = {
        "theta": thetas,
        "energy": energy,
        "summary": summaries,
        "moments_scaled": np.asarray([record["moments"] for record in records]),
        "green00_real": np.real([record["green00"] for record in records]),
        "green00_imag": np.imag([record["green00"] for record in records]),
        "ldos_lower": np.asarray([record["ldos_lower"] for record in records]),
        "ldos_upper": np.asarray([record["ldos_upper"] for record in records]),
        "selected_theta_indices": selected_indices,
        "green_distance": distance_grid,
        "green_profiles": np.asarray(green_profiles),
        "times": times,
        "dynamics": dynamics,
        "norm_defects": norm_defects,
        "row_sum_bounds": np.asarray([record["row_sum_bound"] for record in records]),
        "hermiticity_defects": np.asarray([record["hermiticity_defect"] for record in records]),
    }
    attrs = metadata("I", {
        "summary_columns": names,
        "initial_states": initial_labels,
        "dynamic_observables": dynamic_names,
        "primary_depth": PRIMARY_DEPTH,
        "local_dimension": 130,
        "eta_over_t": ETA,
        "global_periodic_availability": {"theta_0": True, "theta_c_metadata_only": True, "generic": False},
    })
    _write_h5(path, arrays, attrs)
    _write_tsv(PROCESSED / "phenomenon_I_summary.tsv", [dict(theta=float(theta), **{name: summaries[i, j] for j, name in enumerate(names)}) for i, theta in enumerate(thetas)])
    log("Phenomenon I complete")
    return path


def compute_phenomenon_ii(force: bool = False) -> Path:
    path = RAW / "phenomenon_II_commensurability.h5"
    if path.exists() and not force:
        log("Phenomenon II checkpoint found")
        return path
    log("Phenomenon II: arithmetic commensurability resonance test")
    exact = enumerate_exact_angles(8)
    energy = np.linspace(-165.0, 165.0, 321)
    records = [dense_record(angle.theta, energy=energy) for angle in exact]
    names, summaries = _stack_summary(records)
    heights = np.asarray([angle.height for angle in exact], dtype=int)
    theta = np.asarray([angle.theta for angle in exact])
    ldos = np.asarray([record["ldos_lower"] for record in records])

    selected = np.unique(np.concatenate([np.linspace(0, len(exact) - 1, 8, dtype=int), [int(np.argmin(abs(theta - THETA_C)))] ]))
    delta_scales = np.asarray([400, 1200, 3600], dtype=int)
    nearby_summary = np.full((len(selected), len(delta_scales), 2, len(names)), np.nan)
    resonance = np.full((len(selected), len(delta_scales), len(names)), np.nan)
    for si, index in enumerate(selected):
        base = exact[int(index)]
        for di, scale in enumerate(delta_scales):
            candidates = nearby_generic(base, (int(scale),))
            by_side = {"minus": None, "plus": None}
            for candidate in candidates:
                side = "minus" if "minus" in candidate["label"] else "plus"
                row = dense_record(float(candidate["theta"]))
                by_side[side] = np.asarray([row["summary"][name] for name in names])
            if by_side["minus"] is None or by_side["plus"] is None:
                continue
            nearby_summary[si, di, 0] = by_side["minus"]
            nearby_summary[si, di, 1] = by_side["plus"]
            central = summaries[int(index)]
            baseline = 0.5 * (by_side["minus"] + by_side["plus"])
            scale_value = 0.5 * np.abs(by_side["minus"] - by_side["plus"]) + 1e-9 * np.maximum(np.abs(central), 1.0)
            resonance[si, di] = np.abs(central - baseline) / scale_value

    spline_residual = np.zeros_like(summaries)
    for column in range(summaries.shape[1]):
        spline = CubicSpline(theta, summaries[:, column])
        dense_theta = np.linspace(0, THETA_MAX, 2001)
        smooth = CubicSpline(dense_theta[::40], spline(dense_theta[::40]))
        spline_residual[:, column] = summaries[:, column] - smooth(theta)

    sff_times = np.linspace(0.0, 8.0, 241)
    sff = np.zeros((len(selected), len(sff_times)))
    for si, index in enumerate(selected):
        values = records[int(index)]["eigenvalues"]
        scaled = (values - np.mean(values)) / max(np.std(values), 1e-15)
        sff[si] = np.abs(np.sum(np.exp(-1j * scaled[:, None] * sff_times[None, :]), axis=0)) ** 2 / len(values) ** 2

    index_values = np.asarray([np.nan if angle.common_cover_index is None else angle.common_cover_index for angle in exact])
    arrays = {
        "theta": theta,
        "height": heights,
        "common_cover_index": index_values,
        "energy": energy,
        "summary": summaries,
        "ldos": ldos,
        "selected_indices": selected,
        "delta_scales": delta_scales,
        "nearby_summary": nearby_summary,
        "resonance_metric": resonance,
        "spline_residual": spline_residual,
        "sff_times": sff_times,
        "sff": sff,
    }
    attrs = metadata("II", {
        "summary_columns": names,
        "height_cutoff": 8,
        "angle_count": len(exact),
        "cover_index_semantics": "unknown entries remain NaN; only theta=0 and theta_c are certified",
        "resonance_definition": "absolute central-minus-two-sided-baseline divided by side spread plus 1e-9 scale floor",
    })
    _write_h5(path, arrays, attrs)
    rows = []
    for index, angle in enumerate(exact):
        row = angle.record()
        row.update({name: summaries[index, col] for col, name in enumerate(names)})
        rows.append(row)
    _write_tsv(PROCESSED / "phenomenon_II_exact_angle_observables.tsv", rows)
    log("Phenomenon II complete")
    return path


def compute_phenomenon_iii(force: bool = False) -> Path:
    path = RAW / "phenomenon_III_sequences.h5"
    if path.exists() and not force:
        log("Phenomenon III checkpoint found")
        return path
    log("Phenomenon III: three arithmetic approximation routes per target")
    targets = generic_angles()
    target_theta = np.asarray([row["theta"] for row in targets])
    target_t = np.asarray([row["t"] for row in targets])
    sequence_names = ["rational", "sqrt2", "mixed"]
    denominators = np.asarray([8, 13, 21, 34, 55, 89])
    sample = dense_record(float(target_theta[0]))
    summary_names = list(sample["summary"].keys()) + ["green_abs", "return_t0p2", "moment2_scaled"]
    target_values = np.zeros((3, len(summary_names)))
    values = np.zeros((3, 3, len(denominators), len(summary_names)))
    approximants = np.zeros((3, 3, len(denominators)))
    heights = np.zeros_like(approximants)
    for ti in range(3):
        target_record = dense_record(float(target_theta[ti]))
        target_values[ti] = [*target_record["summary"].values(), abs(target_record["green00"]), target_record["return_fixed"][2], target_record["moments"][2]]
        sequences = approximation_sequences(float(target_t[ti]), denominators)
        for si, name in enumerate(sequence_names):
            for li, angle in enumerate(sequences[name]):
                record = dense_record(angle.theta)
                approximants[ti, si, li] = angle.theta
                heights[ti, si, li] = angle.height
                values[ti, si, li] = [*record["summary"].values(), abs(record["green00"]), record["return_fixed"][2], record["moments"][2]]

    depth_values = np.zeros((3, 3, 4))
    depth_sizes = np.zeros(3, dtype=int)
    depth_norm_defect = np.zeros((3, 3))
    for di, depth in enumerate((1, 2, 3)):
        patch = load_orbit_patch(depth)
        depth_sizes[di] = patch.size
        for ti, theta in enumerate(target_theta):
            parameters = ScalarBilayerParameters(theta=float(theta))
            model = build_local_bilayer(patch, parameters)
            scaled = spectral_moments(model.hamiltonian, 0, orders=4)
            row_bound = schur_row_sum_bound(patch, parameters)
            g00 = green_entries(model.hamiltonian, 0.0, ETA, [(0, 0)])[0]
            initial = np.zeros(model.dimension); initial[0] = 1.0
            states = expm_multiply(-0.2j * model.hamiltonian, initial)
            depth_values[di, ti] = [scaled[2] / row_bound**2, scaled[4] / row_bound**4, abs(g00), abs(states[0]) ** 2]
            depth_norm_defect[di, ti] = abs(np.vdot(states, states).real - 1.0)

    arrays = {
        "target_theta": target_theta,
        "target_t": target_t,
        "denominators": denominators,
        "approximant_theta": approximants,
        "height": heights,
        "values": values,
        "target_values": target_values,
        "depths": np.asarray([1, 2, 3]),
        "depth_sizes_per_layer": depth_sizes,
        "depth_values": depth_values,
        "depth_norm_defect": depth_norm_defect,
    }
    attrs = metadata("III", {
        "sequence_names": sequence_names,
        "observable_names": summary_names,
        "target_labels": [row["label"] for row in targets],
        "global_cover_indices": "not present in frozen R5 inputs for these approximants",
        "scope": "tests sequence independence of local real-space observables; does not claim global common-cover convergence",
    })
    _write_h5(path, arrays, attrs)
    rows = []
    for ti, target in enumerate(targets):
        sequences = approximation_sequences(float(target["t"]), denominators)
        for si, name in enumerate(sequence_names):
            for li, angle in enumerate(sequences[name]):
                rows.append({"target": target["label"], "sequence": name, "level": li + 1, "theta_target": target["theta"], "theta_n": angle.theta, "error": abs(angle.theta - target["theta"]), "height": angle.height, **{obs: values[ti, si, li, oi] for oi, obs in enumerate(summary_names)}})
    _write_tsv(PROCESSED / "phenomenon_III_sequence_observables.tsv", rows)
    log("Phenomenon III complete")
    return path


def compute_phenomenon_iv(force: bool = False) -> Path:
    path = RAW / "phenomenon_IV_nonbloch_magic.h5"
    if path.exists() and not force:
        log("Phenomenon IV checkpoint found")
        return path
    log("Phenomenon IV: non-Bloch multidimensional magic scan")
    theta = np.linspace(0.0, THETA_MAX, 17)
    metric_names = ["local_width", "propagation_proxy", "return_t0p2", "coherence_zero", "green_abs", "ipr_zero", "gap_zero"]
    metrics = np.zeros((len(LAMBDA_VALUES), len(OMEGA_VALUES), len(theta), len(metric_names)))
    for li, decay in enumerate(LAMBDA_VALUES):
        for wi, omega in enumerate(OMEGA_VALUES):
            for ai, angle in enumerate(theta):
                record = dense_record(float(angle), float(omega), float(decay))
                eigenvalues, eigenvectors, patch = record["eigenvalues"], record["eigenvectors"], record["patch"]
                weights = np.abs(eigenvectors[0]) ** 2
                mean = np.sum(weights * eigenvalues)
                width = np.sqrt(max(np.sum(weights * eigenvalues**2) - mean**2, 0.0))
                action = record["model"].hamiltonian @ np.eye(record["model"].dimension)[:, 0]
                probability_rate = np.abs(action) ** 2
                radial = np.concatenate([patch.radii_over_a, patch.radii_over_a])
                propagation = np.sqrt(np.sum(probability_rate * radial**2) / max(np.sum(probability_rate), 1e-300))
                summary = record["summary"]
                metrics[li, wi, ai] = [width, propagation, record["return_fixed"][2], summary["coherence_zero"], abs(record["green00"]), summary["ipr_zero"], summary["gap_zero"]]

    score_components = np.zeros(metrics.shape[:3] + (5,))
    signs = np.asarray([-1, -1, 1, 1, 1])
    raw_components = metrics[..., :5]
    for li in range(len(LAMBDA_VALUES)):
        for mi in range(5):
            values = raw_components[li, ..., mi]
            low, high = np.quantile(values, [0.05, 0.95])
            normalized = np.clip((values - low) / max(high - low, 1e-15), 0.0, 1.0)
            score_components[li, ..., mi] = normalized if signs[mi] > 0 else 1.0 - normalized
    combined_score = np.mean(score_components, axis=-1)
    simultaneous = np.sum(score_components >= 0.75, axis=-1)
    best = np.unravel_index(int(np.argmax(combined_score)), combined_score.shape)

    candidate_theta = float(theta[best[2]])
    candidate_omega = float(OMEGA_VALUES[best[1]])
    candidate_decay = float(LAMBDA_VALUES[best[0]])
    selected_parameters = [
        (candidate_theta, candidate_omega, candidate_decay),
        (candidate_theta, 0.25, candidate_decay),
        (candidate_theta, 2.0, candidate_decay),
        (float(THETA_C), candidate_omega, candidate_decay),
        (min(THETA_MAX, float(THETA_C + 1.0 / (1200 * np.pi))), candidate_omega, candidate_decay),
    ]
    energy = np.linspace(-300.0, 300.0, 501)
    times = np.linspace(0.0, 2.0, 101)
    candidate_ldos = np.zeros((len(selected_parameters), len(energy)))
    candidate_dynamics = np.zeros((len(selected_parameters), 7, len(times)))
    dynamic_names = ["survival", "return_probability", "mean_radius", "mean_square_radius", "participation", "layer_imbalance", "entropy"]
    for pi, (angle, omega, decay) in enumerate(selected_parameters):
        record = dense_record(angle, omega, decay, energy=energy)
        candidate_ldos[pi] = record["ldos_lower"]
        initial = np.zeros(record["model"].dimension); initial[0] = 1.0
        trace = evolve(record["model"].hamiltonian, initial, times)
        obs = dynamical_observables(trace.states, initial, record["patch"].radii_over_a, record["patch"].size)
        candidate_dynamics[pi] = np.asarray([obs[name] for name in dynamic_names])

    arrays = {
        "theta": theta,
        "omega_over_omega_ref": OMEGA_VALUES,
        "lambda_perp_over_a": LAMBDA_VALUES,
        "metrics": metrics,
        "score_components": score_components,
        "combined_score": combined_score,
        "simultaneous_top_quartile_count": simultaneous,
        "best_index": np.asarray(best),
        "selected_parameters": np.asarray(selected_parameters),
        "candidate_energy": energy,
        "candidate_ldos": candidate_ldos,
        "candidate_times": times,
        "candidate_dynamics": candidate_dynamics,
    }
    attrs = metadata("IV", {
        "metric_names": metric_names,
        "score_component_names": metric_names[:5],
        "dynamic_names": dynamic_names,
        "magic_rule": "multi-diagnostic score is reported only with simultaneous component count; no one scalar is decisive",
        "best_parameters": {"theta": candidate_theta, "omega_over_omega_ref": candidate_omega, "lambda_perp_over_a": candidate_decay},
        "scan_shape": list(metrics.shape[:3]),
    })
    _write_h5(path, arrays, attrs)
    rows = []
    for li, decay in enumerate(LAMBDA_VALUES):
        for wi, omega in enumerate(OMEGA_VALUES):
            for ai, angle in enumerate(theta):
                rows.append({"lambda_perp_over_a": decay, "omega_over_omega_ref": omega, "theta": angle, **{name: metrics[li, wi, ai, index] for index, name in enumerate(metric_names)}, "combined_score": combined_score[li, wi, ai], "simultaneous_count": int(simultaneous[li, wi, ai])})
    _write_tsv(PROCESSED / "phenomenon_IV_magic_scan.tsv", rows)
    log("Phenomenon IV complete")
    return path


def prepare_audits() -> None:
    write_frozen_manifest()
    record = {
        "timestamp_utc": utc_now(),
        "frozen_inputs": frozen_inputs_present(),
        "qstar_hash": check_qstar_manifest_hash(),
        "r4_rerun": False,
        "r5_rerun": False,
        "generic_periodicization": False,
        "python_executable": sys.executable,
    }
    (ROOT / "14_AUDITS" / "PRE_RUN_INPUT_AUDIT.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def compute_all(force: bool = False) -> dict[str, Path]:
    start = time.perf_counter()
    prepare_audits()
    outputs = {
        "I": compute_phenomenon_i(force),
        "II": compute_phenomenon_ii(force),
        "III": compute_phenomenon_iii(force),
        "IV": compute_phenomenon_iv(force),
    }
    resource = {
        "elapsed_seconds": time.perf_counter() - start,
        "machine": platform.platform(),
        "python": sys.executable,
        "pid": os.getpid(),
        "outputs": {key: str(value) for key, value in outputs.items()},
        "timestamp_utc": utc_now(),
    }
    (ROOT / "14_AUDITS" / "LOCAL_RESOURCE_USAGE.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    return outputs

