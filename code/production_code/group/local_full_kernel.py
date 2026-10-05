"""Rigorous LOCAL-scope shell bounds for the centered Bolza full kernel.

This module deliberately does not use a finite quotient.  All lengths are
measured in units of the Bolza nearest-neighbour spacing ``a_B``.  The shell
count is obtained from disjoint hyperbolic inballs, and the abelianization
weight is obtained from the certified fundamental-domain crossing bound.
Neither constant is fitted to the radius-six universal-cover sample.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import gzip
import json
import math
from pathlib import Path
from typing import Iterable


REGISTERED_Q1 = 0.007124099762028338
FROZEN_H_OVER_A = 0.50
FROZEN_LAMBDA_OVER_A = 0.20

# Abelianization in the standard (a1,b1,a2,b2) basis for the exact geometric
# generators.  It follows from the parity-compatible Nielsen map v1.1:
# g0=a1, g1=b1^-1, g2=a1^-1 b1^-1 a2,
# g3=a1^-1 b1^-1 b2^-1, and g_{j+4}=g_j^-1.
GEOMETRIC_ABELIANIZATION = {
    "g0": (1, 0, 0, 0),
    "g1": (0, -1, 0, 0),
    "g2": (-1, -1, 1, 0),
    "g3": (-1, -1, 0, -1),
    "g4": (-1, 0, 0, 0),
    "g5": (0, 1, 0, 0),
    "g6": (1, 1, -1, 0),
    "g7": (1, 1, 0, 1),
}


@dataclass(frozen=True)
class BolzaLocalConstants:
    kappa_a: float
    h_gamma_times_a: float
    shell_width_over_a: float
    inradius_over_R: float
    circumradius_over_R: float
    tube_radius_over_R: float
    shell_growth_constant: float
    crossing_linear_coefficient: float
    crossing_intercept: float
    abelian_weight_constant_euclidean: float


@dataclass(frozen=True)
class TailRow:
    first_omitted_shell: int
    cutoff_over_a: float
    secant_slope: float
    shell_ratio: float
    c0_per_abs_w: float
    c1_per_abs_w: float
    c2_per_abs_w: float


def bolza_local_constants() -> BolzaLocalConstants:
    """Return theorem-derived, non-fitted shell and derivative constants."""

    root2 = math.sqrt(2.0)
    kappa_a = 2.0 * math.acosh(1.0 + root2)  # a_B/R
    r_in = kappa_a / 2.0
    r_out = math.acosh((1.0 + root2) ** 2)
    tube_radius = r_in + r_out

    # Orbit centres are a_B-separated.  In shell n, their disjoint a_B/2
    # balls lie in B((n+3/2)a_B).  Since cosh(x)-1 <= exp(x)/2,
    # N_n <= C_Gamma exp(n a_B/R).
    c_gamma = math.exp(1.5 * kappa_a) / (2.0 * (math.cosh(r_in) - 1.0))

    # The stadium argument gives |gamma| <= p*d/R+b.  A geometric generator
    # has Euclidean abelianization norm at most sqrt(3).  On shell n,
    # d<(n+1)a_B, so ||n(gamma)||_2 <= C_A[1+(n+1)a_B] with a_B=1.
    p = math.sinh(tube_radius) / (math.pi * (math.cosh(r_in) - 1.0))
    b = (math.cosh(tube_radius) - 1.0) / (math.cosh(r_in) - 1.0)
    p_times_a = p * kappa_a
    c_a = math.sqrt(3.0) * max(p_times_a, 0.5 * (p_times_a + b))
    return BolzaLocalConstants(
        kappa_a=kappa_a,
        h_gamma_times_a=kappa_a,
        shell_width_over_a=1.0,
        inradius_over_R=r_in,
        circumradius_over_R=r_out,
        tube_radius_over_R=tube_radius,
        shell_growth_constant=c_gamma,
        crossing_linear_coefficient=p,
        crossing_intercept=b,
        abelian_weight_constant_euclidean=c_a,
    )


def reduced_physical_distance(lateral_distance_over_a: float, h_over_a: float) -> float:
    """Return (sqrt(h^2+d^2)-h)/a for the centered radial kernel."""

    d = float(lateral_distance_over_a)
    h = float(h_over_a)
    if d < 0.0 or h <= 0.0:
        raise ValueError("distance must be nonnegative and h must be positive")
    return math.sqrt(h * h + d * d) - h


def _moment_sums(q: float, first: int) -> tuple[float, float, float]:
    """Return sum q^n, sum n q^n, sum n^2 q^n from n=first."""

    m = int(first)
    if m != first or m < 0 or not 0.0 <= q < 1.0:
        raise ValueError("invalid geometric-tail arguments")
    q_m = q**m
    s0 = q_m / (1.0 - q)
    s1 = q_m * (m - (m - 1) * q) / (1.0 - q) ** 2
    s2 = q_m * (
        m * m + (-2 * m * m + 2 * m + 1) * q + (m - 1) ** 2 * q * q
    ) / (1.0 - q) ** 3
    return s0, s1, s2


def physical_secant_tail(
    first_omitted_shell: int,
    *,
    h_over_a: float = FROZEN_H_OVER_A,
    lambda_over_a: float = FROZEN_LAMBDA_OVER_A,
) -> TailRow:
    """Evaluate C0/C1/C2 tails for the physical radial kernel.

    The shell ``n`` contains elements with ``n*a_B <= d < (n+1)*a_B``.
    Convexity of phi_h(d)=sqrt(h^2+d^2)-h makes the first secant slope a
    lower bound for every later consecutive slope.  The resulting geometric
    ratio controls the physical kernel directly and is sharper than replacing
    phi_h(d) by d-h.

    C1 and C2 are in the marked standard-coordinate Euclidean norm.  A
    canonical-Hodge norm conversion remains a separate PF-HOD-002 task.
    """

    m = int(first_omitted_shell)
    if m != first_omitted_shell or m < 1:
        raise ValueError("first_omitted_shell must be a positive integer")
    h = float(h_over_a)
    lam = float(lambda_over_a)
    if h <= 0.0 or lam <= 0.0:
        raise ValueError("h and lambda must be positive")

    constants = bolza_local_constants()
    phi_m = reduced_physical_distance(float(m), h)
    phi_next = reduced_physical_distance(float(m + 1), h)
    secant = phi_next - phi_m
    decay_margin = secant / lam - constants.h_gamma_times_a
    if decay_margin <= 0.0:
        raise ValueError("secant decay does not dominate hyperbolic growth")
    q = math.exp(-decay_margin)
    shell_prefactor = constants.shell_growth_constant * math.exp(
        constants.h_gamma_times_a * m - phi_m / lam
    )
    s0, s1, s2 = _moment_sums(q, m)
    # The moment sums above include q^m.  The secant envelope has its exact
    # first-shell prefactor, so normalize the moments by q^m.
    scale = shell_prefactor / (q**m)
    ca = constants.abelian_weight_constant_euclidean
    c0 = scale * s0
    c1 = scale * ca * (s1 + 2.0 * s0)
    c2 = scale * ca * ca * (s2 + 4.0 * s1 + 4.0 * s0)
    return TailRow(m, float(m), secant, q, c0, c1, c2)


def physical_first_shell_weight(
    *,
    h_over_a: float = FROZEN_H_OVER_A,
    lambda_over_a: float = FROZEN_LAMBDA_OVER_A,
) -> float:
    return math.exp(-reduced_physical_distance(1.0, h_over_a) / lambda_over_a)


def abelianization(word: Iterable[str]) -> tuple[int, int, int, int]:
    total = [0, 0, 0, 0]
    for token in word:
        vector = GEOMETRIC_ABELIANIZATION[token]
        for index, value in enumerate(vector):
            total[index] += value
    return tuple(total)  # type: ignore[return-value]


def partial_hodge_scalar_lower_bound(
    archive: Path,
    *,
    h_over_a: float = FROZEN_H_OVER_A,
    lambda_over_a: float = FROZEN_LAMBDA_OVER_A,
) -> dict[str, object]:
    """Positive partial-sum lower bound for q_infinity=b_infinity/2.

    The word-radius archive need not be a complete geometric ball: positivity
    makes every archived term a valid lower contribution.  No missing term is
    treated as zero.
    """

    diagonal = [0.0, 0.0, 0.0, 0.0]
    rows = 0
    with gzip.open(Path(archive), "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            vector = abelianization(row["representative"])
            distance = float(row["distance_over_a_B"])
            weight = math.exp(-reduced_physical_distance(distance, h_over_a) / lambda_over_a)
            for index, value in enumerate(vector):
                diagonal[index] += weight * value * value
            rows += 1
    q_lower_each = [0.5 * value for value in diagonal]
    return {
        "archive_rows": rows,
        "partial_B_diagonal": diagonal,
        "q_infinity_lower_each_coordinate": q_lower_each,
        "q_infinity_lower_bound": max(q_lower_each),
        "logic": "B_infinity=b_infinity*C_S by Bolza point-group symmetry; every omitted summand is positive semidefinite",
    }


def pilot_record(archive: Path, maximum_shell: int = 12) -> dict[str, object]:
    constants = bolza_local_constants()
    rows = [physical_secant_tail(m) for m in range(1, maximum_shell + 1)]
    q_first = physical_first_shell_weight()
    partial = partial_hodge_scalar_lower_bound(archive)
    lower = max(q_first, float(partial["q_infinity_lower_bound"]))
    upper = 0.5 * rows[0].c2_per_abs_w
    delta_lower = lower - REGISTERED_Q1
    return {
        "scope": "LOCAL universal-cover; no finite quotient and no bulk promotion",
        "frozen_parameters": {
            "kappa_a": "kappa_B",
            "h_over_a": FROZEN_H_OVER_A,
            "lambda_perp_over_a": FROZEN_LAMBDA_OVER_A,
        },
        "constants": asdict(constants),
        "tail_table": [asdict(row) for row in rows],
        "registered_first_shell_q1": REGISTERED_Q1,
        "registered_q1_reconstructed_at_lambda_over_a_0p125": math.exp(
            -reduced_physical_distance(1.0, FROZEN_H_OVER_A) / 0.125
        ),
        "physical_first_shell_weight_at_frozen_lambda": q_first,
        "partial_positive_sum": partial,
        "q_infinity_lower_bound": lower,
        "q_infinity_upper_bound_from_full_m1_C2_envelope": upper,
        "q_infinity_interval": [lower, upper],
        "delta_q_lower_bound": delta_lower,
        "delta_q_interval": [delta_lower, upper - REGISTERED_Q1],
        "persistence_condition_abs_delta_lt_q1": False,
        "failure_class": "F5 scientific full-kernel failure",
        "failure_reason": (
            "At frozen lambda_perp/a=0.20 the physical first-shell contribution alone "
            "exceeds 2*the registered q1 from the lambda/a=0.125 validation fixture; "
            "positive later-shell contributions cannot restore |delta_q|<q1."
        ),
        "omega_infinity": None,
        "omega_reason": "persistence contract fails before a certified continued root can be promoted",
        "unpromoted_positive_root_interval_t_over_w": [1.0 / upper, 1.0 / lower],
        "canonical_hodge_tail_status": (
            "coordinate C0/C1/C2 tails instantiated; conversion to the canonical Hodge operator norm "
            "requires the separately released PF-HOD-001/PF-HOD-002 construction"
        ),
    }


def write_pilot_artifacts(archive: Path, output_dir: Path, maximum_shell: int = 12) -> dict[str, Path]:
    """Write the deterministic JSON and tail table for the LOCAL pilot."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    record = pilot_record(archive, maximum_shell=maximum_shell)
    json_path = directory / "LOCAL_FULL_KERNEL_PILOT.json"
    csv_path = directory / "LOCAL_FULL_KERNEL_TAILS.csv"
    json_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        rows = record["tail_table"]
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {"record": json_path, "tails": csv_path}


if __name__ == "__main__":
    paths = write_pilot_artifacts(
        Path("data/production/universal_cover/ball_radius_6_exact.jsonl.gz"),
        Path("data/production/local_full_kernel"),
    )
    print(json.dumps({name: str(path) for name, path in paths.items()}, indent=2))

