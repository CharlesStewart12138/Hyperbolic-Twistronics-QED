"""VT-012 exact Table III CSL inventory validation.

MANUSCRIPT SOURCE:
Equations: (204)--(414), rational square-CSL construction.
Table: III, all nontrivial crystallographic cells with Nsc<100.
Model scope: exact Euclidean integer geometry, before any hopping choice.
"""

from __future__ import annotations

from fractions import Fraction
from math import atan2

from production_code.euclidean.csl import all_subhundred_cells


TABLE_III_EXACT = (
    (41, 82, 9, 1, Fraction(40, 41), Fraction(9, 41)),
    (25, 50, 7, 1, Fraction(24, 25), Fraction(7, 25)),
    (37, 74, 6, 1, Fraction(35, 37), Fraction(12, 37)),
    (13, 26, 5, 1, Fraction(12, 13), Fraction(5, 13)),
    (17, 34, 4, 1, Fraction(15, 17), Fraction(8, 17)),
    (5, 10, 3, 1, Fraction(4, 5), Fraction(3, 5)),
    (29, 58, 5, 2, Fraction(21, 29), Fraction(20, 29)),
)


def validate_inventory() -> dict[str, object]:
    """Re-derive all Table III rows and independently verify each angle.

    MANUSCRIPT SOURCE:
    Equations: cos(theta)=(m^2-n^2)/(m^2+n^2),
    sin(theta)=2mn/(m^2+n^2), with both-odd CSL reduction.
    Model scope: complete Nsc<100 inventory in the reduced twist domain.
    """

    cells = all_subhundred_cells()
    actual = tuple(
        (cell.sigma, cell.n_sc, cell.m, cell.n, cell.cos_theta, cell.sin_theta)
        for cell in cells
    )
    angle_residuals = tuple(
        abs(cell.theta - atan2(float(cell.sin_theta), float(cell.cos_theta)))
        for cell in cells
    )
    ten = next(cell for cell in cells if cell.n_sc == 10)
    thirty_four = next(cell for cell in cells if cell.n_sc == 34)
    return {
        "test_id": "VT-012",
        "criterion": "exact rational data and 1e-12 angle residual",
        "expected_rows": TABLE_III_EXACT,
        "actual_rows": actual,
        "angle_residuals_radian": angle_residuals,
        "ten_site_certificate": (ten.sigma, ten.n_sc, ten.cos_theta, ten.sin_theta),
        "thirty_four_site_certificate": (
            thirty_four.sigma,
            thirty_four.n_sc,
            thirty_four.cos_theta,
            thirty_four.sin_theta,
        ),
        "passed": actual == TABLE_III_EXACT and max(angle_residuals) <= 1e-12,
    }
