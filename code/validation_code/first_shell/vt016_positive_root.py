"""VT-016 positive-root reproduction for the first-shell control.

MANUSCRIPT SOURCE:
Equations: (635)--(640).
Section: centered surface-group first-shell validation.
Model scope: validation-only scalar-commutant class.
"""

from __future__ import annotations

import numpy as np

from validation_code.first_shell.first_shell_surface import (
    REGISTERED_ADJACENCY_NORM,
    REGISTERED_Q1,
    gap_lower_bound,
    parity_blocks,
    root,
)


def validate_positive_root(t: float = 1.0) -> dict[str, object]:
    """Reproduce w*/t=1/q1, exact plus-block flattening and the gap.

    MANUSCRIPT SOURCE:
    Equations: H_+=wI+(-t+wq1)A_S and
    g*=2t(q1^-1-||A_S||).
    Model scope: registered first-shell validation constants only.
    """

    w_star = root(t, REGISTERED_Q1, run_type="validation")
    adjacency = np.diag((-8.0, -3.0, 0.5, 8.0))
    plus, _minus = parity_blocks(
        adjacency,
        t,
        w_star,
        REGISTERED_Q1,
        run_type="validation",
    )
    flat_residual = float(np.linalg.norm(plus - w_star * np.eye(4), ord=2))
    gap = gap_lower_bound(
        t,
        REGISTERED_Q1,
        REGISTERED_ADJACENCY_NORM,
        run_type="validation",
    )
    expected_gap = 2.0 * t * (1.0 / REGISTERED_Q1 - REGISTERED_ADJACENCY_NORM)
    root_residual = abs(w_star / t - 1.0 / REGISTERED_Q1)
    gap_residual = abs(gap - expected_gap)
    tolerance = 5e-13 * max(1.0, abs(w_star))
    return {
        "test_id": "VT-016",
        "registered_tolerance": tolerance,
        "q1": REGISTERED_Q1,
        "adjacency_norm": REGISTERED_ADJACENCY_NORM,
        "w_star_over_t": w_star / t,
        "root_residual": root_residual,
        "g_star_over_t": gap / t,
        "gap_residual": gap_residual,
        "flat_plus_block_residual": flat_residual,
        "passed": root_residual <= tolerance
        and gap_residual <= tolerance
        and flat_residual <= tolerance
        and gap > 0.0,
    }
