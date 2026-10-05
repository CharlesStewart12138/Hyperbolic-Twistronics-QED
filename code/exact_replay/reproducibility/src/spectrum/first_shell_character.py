"""Declared first-shell character-sector spectral observables and derivatives."""

from __future__ import annotations

import itertools
import math

import numpy as np


def character_matrix(k: np.ndarray, *, w_over_t: float, q1: float) -> np.ndarray:
    c_value = float(np.sum(np.cos(k)))
    diagonal = -2.0 * c_value
    off_diagonal = w_over_t * (1.0 + 2.0 * q1 * c_value)
    return np.asarray([[diagonal, off_diagonal], [off_diagonal, diagonal]], dtype=float)


def solve_character(k: np.ndarray, *, w_over_t: float, q1: float) -> dict[str, object]:
    matrix = character_matrix(k, w_over_t=w_over_t, q1=q1)
    values, vectors = np.linalg.eigh(matrix)
    layer_exchange = np.asarray([[0.0, 1.0], [1.0, 0.0]])
    parities = [float(vectors[:, index] @ layer_exchange @ vectors[:, index]) for index in range(2)]
    even_index = int(np.argmax(parities))
    odd_index = 1 - even_index
    even_vector = vectors[:, even_index]
    even_projector = np.outer(even_vector, even_vector)
    residuals = {
        "matrix_hermiticity": float(np.linalg.norm(matrix - matrix.T, ord=2)),
        "eigenpair": float(np.linalg.norm(matrix @ even_vector - values[even_index] * even_vector)),
        "even_parity": abs(parities[even_index] - 1.0),
        "odd_parity": abs(parities[odd_index] + 1.0),
    }
    return {
        "even_energy_over_t": float(values[even_index]),
        "odd_energy_over_t": float(values[odd_index]),
        "even_projector": even_projector,
        "residuals": residuals,
    }


def exact_corner_grid(dimension: int = 4) -> list[np.ndarray]:
    return [np.asarray(values, dtype=float) for values in itertools.product((0.0, math.pi), repeat=dimension)]


def validation_couplings(w_star_over_t: float) -> list[dict[str, float | str]]:
    ratios = (("three_quarters", 0.75), ("seven_eighths", 0.875), ("root", 1.0), ("nine_eighths", 1.125), ("five_quarters", 1.25))
    return [{"coupling_case": label, "w_over_w_star": ratio, "w_over_t": ratio * w_star_over_t} for label, ratio in ratios]


def exact_observables(*, w_over_t: float, q1: float, m: int = 4) -> dict[str, float]:
    coefficient = w_over_t * q1 - 1.0
    even_bandwidth = 4.0 * m * abs(coefficient)
    even_min = w_over_t - 2.0 * m * abs(coefficient)
    even_max = w_over_t + 2.0 * m * abs(coefficient)
    odd_coefficient = w_over_t * q1 + 1.0
    odd_min = -w_over_t - 2.0 * m * odd_coefficient
    odd_max = -w_over_t + 2.0 * m * odd_coefficient
    lower_gap = even_min - odd_max
    return {
        "even_lower_edge_over_t": even_min,
        "even_upper_edge_over_t": even_max,
        "even_bandwidth_over_t": even_bandwidth,
        "odd_lower_edge_over_t": odd_min,
        "odd_upper_edge_over_t": odd_max,
        "signed_lower_isolation_gap_over_t": lower_gap,
        "maximum_generalized_velocity_t_over_hbar": 2.0 * abs(coefficient) * math.sqrt(m),
        "maximum_absolute_hessian_over_t": 2.0 * abs(coefficient),
        "hodge_trace_at_trivial_character_over_t": 2.0 * m * (1.0 - w_over_t * q1),
    }


def numerical_corner_observables(*, w_over_t: float, q1: float) -> tuple[list[dict[str, object]], dict[str, float]]:
    rows: list[dict[str, object]] = []
    even_values = []
    odd_values = []
    for point_index, k in enumerate(exact_corner_grid()):
        solved = solve_character(k, w_over_t=w_over_t, q1=q1)
        even_values.append(float(solved["even_energy_over_t"]))
        odd_values.append(float(solved["odd_energy_over_t"]))
        rows.append({
            "point_index": point_index,
            "k1_over_pi": k[0] / math.pi,
            "k2_over_pi": k[1] / math.pi,
            "k3_over_pi": k[2] / math.pi,
            "k4_over_pi": k[3] / math.pi,
            "C_k": float(np.sum(np.cos(k))),
            "even_energy_over_t": solved["even_energy_over_t"],
            "odd_energy_over_t": solved["odd_energy_over_t"],
            "maximum_solver_residual": max(solved["residuals"].values()),
        })
    return rows, {
        "even_lower_edge_over_t": min(even_values),
        "even_upper_edge_over_t": max(even_values),
        "even_bandwidth_over_t": max(even_values) - min(even_values),
        "odd_lower_edge_over_t": min(odd_values),
        "odd_upper_edge_over_t": max(odd_values),
        "signed_lower_isolation_gap_over_t": min(even_values) - max(odd_values),
    }


def derivative_audit(*, w_over_t: float, q1: float, steps: tuple[float, ...]) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    coefficient = w_over_t * q1 - 1.0
    expected_velocity = 2.0 * abs(coefficient) * math.sqrt(4.0)
    expected_hessian = 2.0 * (1.0 - w_over_t * q1)
    maximum_velocity_error = 0.0
    maximum_hessian_error = 0.0
    previous_hessian_error = math.inf
    convergence_pass = True
    for step in steps:
        k_velocity = np.full(4, math.pi / 2.0)
        gradient = []
        for axis in range(4):
            delta = np.zeros(4)
            delta[axis] = step
            plus = float(solve_character(k_velocity + delta, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
            minus = float(solve_character(k_velocity - delta, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
            gradient.append((plus - minus) / (2.0 * step))
        velocity = float(np.linalg.norm(gradient))

        origin = np.zeros(4)
        center = float(solve_character(origin, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
        hessian = np.zeros((4, 4))
        for axis in range(4):
            delta = np.zeros(4)
            delta[axis] = step
            plus = float(solve_character(delta, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
            minus = float(solve_character(-delta, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
            hessian[axis, axis] = (plus - 2.0 * center + minus) / (step * step)
        for first in range(4):
            for second in range(first + 1, 4):
                d1 = np.zeros(4)
                d2 = np.zeros(4)
                d1[first] = step
                d2[second] = step
                values = [
                    float(solve_character(sign1 * d1 + sign2 * d2, w_over_t=w_over_t, q1=q1)["even_energy_over_t"])
                    for sign1, sign2 in ((1, 1), (1, -1), (-1, 1), (-1, -1))
                ]
                mixed = (values[0] - values[1] - values[2] + values[3]) / (4.0 * step * step)
                hessian[first, second] = hessian[second, first] = mixed
        principal = np.linalg.eigvalsh(hessian)
        velocity_error = abs(velocity - expected_velocity)
        hessian_error = float(np.max(np.abs(principal - expected_hessian)))
        if previous_hessian_error < math.inf and hessian_error > previous_hessian_error * 1.15:
            convergence_pass = False
        previous_hessian_error = hessian_error
        maximum_velocity_error = max(maximum_velocity_error, velocity_error)
        maximum_hessian_error = max(maximum_hessian_error, hessian_error)
        rows.append({
            "step": step,
            "velocity_fd_t_over_hbar": velocity,
            "velocity_exact_t_over_hbar": expected_velocity,
            "velocity_abs_error": velocity_error,
            "hessian_lambda_1_over_t": principal[0],
            "hessian_lambda_2_over_t": principal[1],
            "hessian_lambda_3_over_t": principal[2],
            "hessian_lambda_4_over_t": principal[3],
            "hessian_exact_over_t": expected_hessian,
            "hessian_max_abs_error": hessian_error,
        })
    final = rows[-1]
    checks = {
        "velocity_final_accuracy": float(final["velocity_abs_error"]) <= 2.0e-7,
        "hessian_final_accuracy": float(final["hessian_max_abs_error"]) <= 2.0e-6,
        "hessian_refinement_consistency": convergence_pass,
    }
    return rows, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "maximum_velocity_abs_error": maximum_velocity_error,
        "maximum_hessian_abs_error": maximum_hessian_error,
        "final_velocity_abs_error": final["velocity_abs_error"],
        "final_hessian_abs_error": final["hessian_max_abs_error"],
        "checks": checks,
    }
