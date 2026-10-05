"""Physical exponential full-distance coefficients on a checked orbit patch."""

from __future__ import annotations

import math

from reproducibility.src.hyperbolic.bolza import enumerate_orbit


def inverse_word(word: str) -> str:
    if word == "e":
        return "e"
    tokens = word.split()
    return " ".join(f"s{(int(token[1:]) + 4) % 8}" for token in reversed(tokens))


def full_distance_kernel_patch(
    *,
    max_word_depth: int,
    h_over_r: float,
    lambda_over_r: float,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    orbit, orbit_checks = enumerate_orbit(max_word_depth)
    rows = []
    by_word = {str(record["word"]): record for record in orbit}
    maximum_inverse_distance_residual = 0.0
    for record in orbit:
        distance = float(record["geodesic_radius_over_r"])
        product_distance = math.sqrt(h_over_r * h_over_r + distance * distance)
        excess = product_distance - h_over_r
        coefficient = math.exp(-excess / lambda_over_r)
        inverse = inverse_word(str(record["word"]))
        inverse_record = by_word.get(inverse)
        if inverse_record is None:
            raise AssertionError(f"inverse word missing from symmetric orbit patch: {inverse}")
        maximum_inverse_distance_residual = max(
            maximum_inverse_distance_residual,
            abs(distance - float(inverse_record["geodesic_radius_over_r"])),
        )
        rows.append({
            "orbit_index": record["orbit_index"],
            "word": record["word"],
            "inverse_word": inverse,
            "word_depth": record["word_depth"],
            "inplane_distance_over_r": distance,
            "product_distance_over_r": product_distance,
            "excess_distance_over_r": excess,
            "q_gamma": coefficient,
            "kernel_scope": "TRUNCATED_UNIVERSAL_ORBIT_PATCH_NOT_FINITE_QUOTIENT_SUM",
        })
    first_shell = [row["q_gamma"] for row in rows if row["word_depth"] == 1]
    checks = {
        "orbit_geometry": orbit_checks["status"] == "PASS",
        "identity_coefficient": abs(float(rows[0]["q_gamma"]) - 1.0) <= 1.0e-14,
        "inverse_symmetry": maximum_inverse_distance_residual <= 2.0e-11,
        "equal_first_shell": max(first_shell) - min(first_shell) <= 2.0e-12,
        "positive_bounded_coefficients": all(0.0 < float(row["q_gamma"]) <= 1.0 for row in rows),
    }
    return rows, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "FULL_DISTANCE_EXPONENTIAL_COEFFICIENTS_ON_SHORT_WORD_PATCH",
        "row_count": len(rows),
        "max_word_depth": max_word_depth,
        "h_over_r": h_over_r,
        "lambda_over_r": lambda_over_r,
        "first_shell_q": sum(first_shell) / len(first_shell),
        "maximum_inverse_distance_residual_over_r": maximum_inverse_distance_residual,
        "checks": checks,
    }
