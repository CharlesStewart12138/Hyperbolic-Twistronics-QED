import math
from pathlib import Path

from production_code.group.local_full_kernel import (
    REGISTERED_Q1,
    abelianization,
    bolza_local_constants,
    physical_first_shell_weight,
    physical_secant_tail,
    pilot_record,
)


def test_nonfitted_constants_and_decay_margin() -> None:
    constants = bolza_local_constants()
    assert math.isclose(constants.kappa_a, 3.057141838961996, rel_tol=0.0, abs_tol=2e-15)
    assert constants.shell_growth_constant >= 1.0
    assert constants.abelian_weight_constant_euclidean > 0.0
    row = physical_secant_tail(1)
    assert 0.0 < row.shell_ratio < 1.0


def test_tail_bounds_decay_with_cutoff() -> None:
    rows = [physical_secant_tail(m) for m in range(1, 13)]
    for key in ("c0_per_abs_w", "c1_per_abs_w", "c2_per_abs_w"):
        values = [getattr(row, key) for row in rows]
        assert all(right < left for left, right in zip(values, values[1:]))
        assert values[-1] < values[0]


def test_geometric_generator_abelianization() -> None:
    assert abelianization(["g0", "g4"]) == (0, 0, 0, 0)
    assert abelianization(["g1", "g5"]) == (0, 0, 0, 0)
    assert abelianization(["g2"]) == (-1, -1, 1, 0)
    assert abelianization(["g3"]) == (-1, -1, 0, -1)


def test_frozen_lambda_rejects_registered_persistence_contract() -> None:
    q_physical = physical_first_shell_weight()
    assert q_physical > 2.0 * REGISTERED_Q1
    archive = Path("data/production/universal_cover/ball_radius_6_exact.jsonl.gz")
    record = pilot_record(archive, maximum_shell=4)
    assert record["persistence_condition_abs_delta_lt_q1"] is False
    assert record["failure_class"].startswith("F5")
    assert record["q_infinity_lower_bound"] > q_physical
    lower, upper = record["q_infinity_interval"]
    assert 0.0 < lower < upper
    assert record["delta_q_lower_bound"] > REGISTERED_Q1

