"""VT-015 exact five-state no-root reproduction.

MANUSCRIPT SOURCE:
Equations: (623)--(633).
Section: exact no-go theorem for the square five-state model.
Model scope: validation only; it makes no production-band claim.
"""

from __future__ import annotations

from math import isclose, sqrt

from validation_code.five_state.five_state_square import (
    ALPHA_MIN_SQUARED,
    LOWER_BOUND,
    curvature_coefficient,
)


def validate_no_root() -> dict[str, float | bool | str]:
    """Reproduce the global minimum and disprove the formal quadratic zero.

    MANUSCRIPT SOURCE:
    Equations: dc/dr=2(r^2-2r-1)/(r^2+r)^2 and
    min c_square=4sqrt(2)-5>0; weak-coupling c=1-8 alpha^2+O(alpha^4).
    Model scope: all alpha>=0 in the exact validation Hamiltonian.
    """

    r_min = 1.0 + sqrt(2.0)
    alpha_min = sqrt(ALPHA_MIN_SQUARED)
    minimum = curvature_coefficient(alpha_min, run_type="validation")
    formal_alpha = 1.0 / sqrt(8.0)
    exact_at_formal_zero = curvature_coefficient(formal_alpha, run_type="validation")
    closed_form_at_formal_zero = 3.0 - 4.0 * sqrt(3.0) / 3.0
    return {
        "test_id": "VT-015",
        "criterion": "1e-12 and strict positivity",
        "stationary_r": r_min,
        "alpha_min_squared": ALPHA_MIN_SQUARED,
        "minimum": minimum,
        "minimum_closed_form": LOWER_BOUND,
        "formal_quadratic_alpha": formal_alpha,
        "exact_at_formal_zero": exact_at_formal_zero,
        "formal_zero_closed_form": closed_form_at_formal_zero,
        "minimum_matches": isclose(minimum, LOWER_BOUND, rel_tol=1e-12),
        "formal_zero_remains_positive": exact_at_formal_zero > 0.0,
        "passed": isclose(minimum, LOWER_BOUND, rel_tol=1e-12)
        and LOWER_BOUND > 0.0
        and isclose(exact_at_formal_zero, closed_form_at_formal_zero, rel_tol=1e-12)
        and exact_at_formal_zero > 0.0,
    }
