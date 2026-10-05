"""Finite Abelian validation towers and non-exhaustivity diagnostics."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


TOWERS = {
    "A_power_of_two": (4, 8, 16),
    "B_three_multiple": (6, 18),
}


def cover_spectrum(modulus: int, *, w_star_over_t: float) -> tuple[np.ndarray, np.ndarray]:
    angles = 2.0 * math.pi * np.arange(modulus, dtype=float) / modulus
    cosines = np.cos(angles)
    sums = (
        cosines[:, None, None, None]
        + cosines[None, :, None, None]
        + cosines[None, None, :, None]
        + cosines[None, None, None, :]
    ).reshape(-1)
    even = np.full(sums.size, w_star_over_t, dtype=float)
    odd = -w_star_over_t - 4.0 * sums
    return even, odd


def kolmogorov_distance(left: np.ndarray, right: np.ndarray) -> float:
    left = np.sort(left)
    right = np.sort(right)
    grid = np.unique(np.concatenate((left, right)))
    left_cdf = np.searchsorted(left, grid, side="right") / left.size
    right_cdf = np.searchsorted(right, grid, side="right") / right.size
    return float(np.max(np.abs(left_cdf - right_cdf)))


def spectral_set_rows(tower_id: str, level: int, modulus: int, even: np.ndarray, odd: np.ndarray) -> list[dict[str, object]]:
    values = np.concatenate((even, odd))
    rounded = np.round(values, decimals=11)
    unique, counts = np.unique(rounded, return_counts=True)
    return [
        {
            "tower_id": tower_id,
            "level": level,
            "modulus": modulus,
            "energy_over_t": float(value),
            "multiplicity": int(count),
            "normalized_weight": float(count / values.size),
            "declared_sector": "COMPLETE_DUAL_OF_ABELIAN_VALIDATION_QUOTIENT",
        }
        for value, count in zip(unique, counts)
    ]


def cover_diagnostic(tower_id: str, level: int, modulus: int, *, w_star_over_t: float) -> tuple[dict[str, object], np.ndarray, list[dict[str, object]]]:
    even, odd = cover_spectrum(modulus, w_star_over_t=w_star_over_t)
    unique_odd = np.unique(np.round(np.sort(odd), decimals=11))
    maximum_gap = float(np.max(np.diff(unique_odd))) if unique_odd.size > 1 else 0.0
    no_loss = 0.5 * maximum_gap
    maximum_sine = float(np.max(np.abs(np.sin(2.0 * math.pi * np.arange(modulus) / modulus))))
    maximum_cosine = float(np.max(np.abs(np.cos(2.0 * math.pi * np.arange(modulus) / modulus))))
    velocity_maximum = 8.0 * maximum_sine
    hessian_maximum = 4.0 * maximum_cosine
    word_injectivity_radius = 2.0
    balanced_shell = math.floor(math.sqrt(word_injectivity_radius))
    states = np.sort(np.concatenate((even, odd)))
    diagnostic = {
        "tower_id": tower_id,
        "level": level,
        "modulus": modulus,
        "cover_degree": modulus ** 4,
        "bilayer_dimension": 2 * modulus ** 4,
        "quotient_group": f"(Z/{modulus}Z)^4",
        "quotient_map_from_previous": "coordinate reduction modulo lower modulus" if level > 0 else "BASE_LEVEL",
        "minimum_kernel_word_length": 4,
        "kernel_witness": "[a1,b1]",
        "word_injectivity_radius": word_injectivity_radius,
        "geometric_injectivity_radius": "MISSING",
        "balanced_shell_depth": balanced_shell,
        "shell_to_injectivity_ratio": balanced_shell / word_injectivity_radius,
        "C0_no_loss_error_over_t": no_loss,
        "C0_no_pollution_error_over_t": 0.0,
        "C0_Hausdorff_error_over_t": no_loss,
        "C1_velocity_maximum_t_over_hbar": velocity_maximum,
        "C1_velocity_maximum_error_t_over_hbar": 8.0 - velocity_maximum,
        "C2_Hessian_maximum_over_t": hessian_maximum,
        "C2_Hessian_maximum_error_over_t": 4.0 - hessian_maximum,
        "target_even_bandwidth_over_t": 0.0,
        "declared_sector": "FIRST_SHELL_ABELIAN_CHARACTER_TORUS",
        "full_surface_group_convergence_status": "INCONCLUSIVE_NONEXHAUSTIVE_ABELIANIZATION_KERNEL",
    }
    return diagnostic, states, spectral_set_rows(tower_id, level, modulus, even, odd)


def build_cover_products(*, w_star_over_t: float) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[tuple[str, int], np.ndarray]]:
    diagnostics: list[dict[str, object]] = []
    spectral_rows: list[dict[str, object]] = []
    aliasing_rows: list[dict[str, object]] = []
    states: dict[tuple[str, int], np.ndarray] = {}
    for tower_id, moduli in TOWERS.items():
        previous = None
        for level, modulus in enumerate(moduli):
            if previous is not None and modulus % previous != 0:
                raise RuntimeError(f"tower {tower_id} lacks a quotient map from modulus {modulus} to {previous}")
            diagnostic, spectrum, rows = cover_diagnostic(tower_id, level, modulus, w_star_over_t=w_star_over_t)
            diagnostics.append(diagnostic)
            spectral_rows.extend(rows)
            states[(tower_id, level)] = spectrum
            for moment_order in range(1, 7):
                margin = 2.0 * float(diagnostic["word_injectivity_radius"]) - moment_order
                aliasing_rows.append({
                    "tower_id": tower_id,
                    "level": level,
                    "modulus": modulus,
                    "moment_order": moment_order,
                    "propagation_radius_per_hop": 1.0,
                    "aliasing_margin": margin,
                    "moment_exactness_certified": margin > 0.0,
                })
            previous = modulus
    return diagnostics, spectral_rows, aliasing_rows, states


def cross_cover_rows(diagnostics: list[dict[str, object]], states: dict[tuple[str, int], np.ndarray]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    by_tower: dict[str, list[dict[str, object]]] = {}
    for row in diagnostics:
        by_tower.setdefault(str(row["tower_id"]), []).append(row)
    for tower_id, tower_rows in by_tower.items():
        tower_rows.sort(key=lambda row: int(row["level"]))
        for left, right in zip(tower_rows, tower_rows[1:]):
            distance = kolmogorov_distance(
                states[(tower_id, int(left["level"]))],
                states[(tower_id, int(right["level"]))],
            )
            rows.append({
                "comparison_type": "SUCCESSIVE_COVER",
                "left_tower": tower_id,
                "left_level": left["level"],
                "left_modulus": left["modulus"],
                "right_tower": tower_id,
                "right_level": right["level"],
                "right_modulus": right["modulus"],
                "word_injectivity_radius_left": left["word_injectivity_radius"],
                "word_injectivity_radius_right": right["word_injectivity_radius"],
                "cdf_kolmogorov_distance": distance,
                "matching_status": "NOT_LICENSED_AS_BULK_CONVERGENCE_CONSTANT_INJECTIVITY_RADIUS",
            })
    for level in range(min(len(by_tower["A_power_of_two"]), len(by_tower["B_three_multiple"]))):
        left = by_tower["A_power_of_two"][level]
        right = by_tower["B_three_multiple"][level]
        distance = kolmogorov_distance(
            states[("A_power_of_two", level)],
            states[("B_three_multiple", level)],
        )
        rows.append({
            "comparison_type": "CROSS_TOWER",
            "left_tower": left["tower_id"],
            "left_level": left["level"],
            "left_modulus": left["modulus"],
            "right_tower": right["tower_id"],
            "right_level": right["level"],
            "right_modulus": right["modulus"],
            "word_injectivity_radius_left": left["word_injectivity_radius"],
            "word_injectivity_radius_right": right["word_injectivity_radius"],
            "cdf_kolmogorov_distance": distance,
            "matching_status": "INJECTIVITY_RADII_MATCH_BUT_DO_NOT_GROW_FULL_GROUP_CLAIM_INCONCLUSIVE",
        })
    return rows


def shell_budget_rows(kernel_path: Path, *, w_star_over_t: float) -> list[dict[str, object]]:
    generator_steps = {
        "s0": np.asarray((1, 0, 0, 0), dtype=float),
        "s1": np.asarray((0, 1, 0, 0), dtype=float),
        "s2": np.asarray((0, 0, 1, 0), dtype=float),
        "s3": np.asarray((0, 0, 0, 1), dtype=float),
        "s4": np.asarray((-1, 0, 0, 0), dtype=float),
        "s5": np.asarray((0, -1, 0, 0), dtype=float),
        "s6": np.asarray((0, 0, -1, 0), dtype=float),
        "s7": np.asarray((0, 0, 0, -1), dtype=float),
    }
    records = []
    with kernel_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            displacement = np.zeros(4, dtype=float)
            if row["word"] != "e":
                for token in row["word"].split():
                    displacement += generator_steps[token]
            records.append((int(row["word_depth"]), float(row["q_gamma"]), displacement))
    maximum_depth = max(depth for depth, _, _ in records)
    rows: list[dict[str, object]] = []
    for retained_depth in range(1, maximum_depth + 1):
        omitted = [(weight, displacement) for depth, weight, displacement in records if depth > retained_depth]
        c0 = w_star_over_t * sum(abs(weight) for weight, _ in omitted)
        c1 = w_star_over_t * sum(abs(weight) * float(np.linalg.norm(displacement)) for weight, displacement in omitted)
        c2 = w_star_over_t * sum(abs(weight) * float(np.linalg.norm(displacement)) ** 2 for weight, displacement in omitted)
        rows.append({
            "retained_word_depth": retained_depth,
            "available_reference_word_depth": maximum_depth,
            "retained_coefficient_count": sum(depth <= retained_depth for depth, _, _ in records),
            "omitted_coefficient_count_within_patch": len(omitted),
            "C0_operator_tail_bound_over_t": c0,
            "C1_derivative_tail_bound_over_t": c1,
            "C2_Hessian_tail_bound_over_t": c2,
            "infinite_shell_tail_status": "UNKNOWN_BEYOND_DEPTH_THREE",
            "budget_scope": "FINITE_AVAILABLE_PATCH_ONLY_NOT_INFINITE_KERNEL_CONVERGENCE",
        })
    return rows
