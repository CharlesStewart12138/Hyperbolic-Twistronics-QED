"""Exact square coincidence-cell geometry from manuscript formulas."""

from __future__ import annotations

import math

import numpy as np


CELL_SPECS = (
    {"site_count": 82, "m": 9, "n": 1, "angle_degrees_source": 12.680383492},
    {"site_count": 50, "m": 7, "n": 1, "angle_degrees_source": 16.260204708},
    {"site_count": 74, "m": 6, "n": 1, "angle_degrees_source": 18.924644416},
    {"site_count": 26, "m": 5, "n": 1, "angle_degrees_source": 22.619864948},
    {"site_count": 34, "m": 4, "n": 1, "angle_degrees_source": 28.072486936},
    {"site_count": 10, "m": 3, "n": 1, "angle_degrees_source": 36.869897646},
    {"site_count": 58, "m": 5, "n": 2, "angle_degrees_source": 43.602818973},
)


def parity_divisor(m: int, n: int) -> int:
    return 2 if (m - n) % 2 == 0 else 1


def reduced_pq(m: int, n: int, divisor: int) -> tuple[int, int]:
    if divisor == 1:
        return m, n
    return (m + n) // 2, (n - m) // 2


def cell_record(specification: dict[str, int | float]) -> dict[str, object]:
    m = int(specification["m"])
    n = int(specification["n"])
    divisor = parity_divisor(m, n)
    sigma = (m * m + n * n) // divisor
    p, q = reduced_pq(m, n, divisor)
    angle = 2.0 * math.atan2(n, m)
    source_angle = float(specification["angle_degrees_source"])
    site_count = int(specification["site_count"])
    direct = np.asarray([[p, -q], [q, p]], dtype=int)
    reciprocal_normalized = direct.astype(float) / sigma
    checks = {
        "site_count": site_count == 2 * sigma,
        "coprime_pq": math.gcd(abs(p), abs(q)) == 1,
        "direct_gram": bool(np.array_equal(direct.T @ direct, sigma * np.eye(2, dtype=int))),
        "direct_determinant": round(np.linalg.det(direct)) == sigma,
        "source_angle": abs(math.degrees(angle) - source_angle) <= 5.0e-10,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    return {
        "site_count": site_count,
        "sigma": sigma,
        "m": m,
        "n": n,
        "parity_divisor": divisor,
        "p": p,
        "q": q,
        "cos_theta": (m * m - n * n) / (m * m + n * n),
        "sin_theta": 2.0 * m * n / (m * m + n * n),
        "angle_radians": angle,
        "angle_degrees": math.degrees(angle),
        "angle_degrees_source": source_angle,
        "direct_basis_a": direct,
        "reciprocal_basis_a_over_2pi": reciprocal_normalized,
        "supercell_length_over_a": math.sqrt(sigma),
        "supercell_area_over_a2": sigma,
        "mbz_area_over_primitive_bz": 1.0 / sigma,
        "checks": checks,
        "failed_checks": failed,
    }


def all_cell_records() -> list[dict[str, object]]:
    return [cell_record(specification) for specification in CELL_SPECS]


def lattice_representatives(p: int, q: int, sigma: int) -> list[dict[str, int]]:
    """Return exact integer square-lattice representatives in the CSL cell."""
    representatives: dict[tuple[int, int], dict[str, int]] = {}
    direct = np.asarray([[p, -q], [q, p]], dtype=int)
    for x in range(sigma):
        for y in range(sigma):
            u0 = (p * x + q * y) % sigma
            u1 = (-q * x + p * y) % sigma
            key = (u0, u1)
            if key in representatives:
                continue
            numerator = direct @ np.asarray([u0, u1], dtype=int)
            if np.any(numerator % sigma):
                raise AssertionError("representative coordinate is not integral")
            coordinate = numerator // sigma
            representatives[key] = {
                "fractional_u_numerator": u0,
                "fractional_v_numerator": u1,
                "fractional_denominator": sigma,
                "x_over_a": int(coordinate[0]),
                "y_over_a": int(coordinate[1]),
            }
            if len(representatives) == sigma:
                return list(representatives.values())
    raise AssertionError("failed to enumerate every quotient representative")


def wrap_rotated_representatives(
    representatives: list[dict[str, int]],
    *,
    direct_basis: np.ndarray,
    angle_radians: float,
) -> list[dict[str, float]]:
    rotation = np.asarray([
        [math.cos(angle_radians), -math.sin(angle_radians)],
        [math.sin(angle_radians), math.cos(angle_radians)],
    ])
    inverse = np.linalg.inv(np.asarray(direct_basis, dtype=float))
    output = []
    for entry in representatives:
        coordinate = rotation @ np.asarray([entry["x_over_a"], entry["y_over_a"]], dtype=float)
        fractional = np.mod(inverse @ coordinate, 1.0)
        wrapped = np.asarray(direct_basis, dtype=float) @ fractional
        output.append({
            "fractional_u": float(fractional[0]),
            "fractional_v": float(fractional[1]),
            "x_over_a": float(wrapped[0]),
            "y_over_a": float(wrapped[1]),
        })
    return output
