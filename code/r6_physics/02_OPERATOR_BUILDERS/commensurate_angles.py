"""Exact centered commensurator angles and certified generic controls."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import atan, gcd, pi, sqrt
from typing import Iterable


THETA_MAX = pi / 8.0
T_MAX = __import__("math").tan(pi / 16.0)
THETA_C = 2.0 * atan(1.0 / (4.0 + sqrt(2.0)))


@dataclass(frozen=True)
class ExactAngle:
    label: str
    a: int
    b: int
    c: int
    theta: float
    height: int
    common_cover_index: int | None
    cover_index_status: str

    @property
    def t_value(self) -> float:
        return (self.a + self.b * sqrt(2.0)) / self.c

    def record(self) -> dict[str, object]:
        row = asdict(self)
        row["t_exact"] = f"({self.a}+{self.b}*sqrt(2))/{self.c}"
        row["hilbert_dimension"] = None if self.common_cover_index is None else 92_160 * self.common_cover_index
        row["normalizer_status"] = self.theta == 0.0
        row["commensurator_status"] = True
        return row


def _primitive(a: int, b: int, c: int) -> bool:
    return gcd(gcd(abs(a), abs(b)), abs(c)) == 1


def enumerate_exact_angles(height: int) -> list[ExactAngle]:
    bound = int(height)
    if bound < 1:
        raise ValueError("height must be positive")
    selected: dict[int, ExactAngle] = {
        0: ExactAngle("theta_0", 0, 0, 1, 0.0, 1, 1, "CERTIFIED")
    }
    for c in range(1, bound + 1):
        for a in range(-bound, bound + 1):
            for b in range(-bound, bound + 1):
                if not _primitive(a, b, c):
                    continue
                value = (a + b * sqrt(2.0)) / c
                if not 0.0 < value < T_MAX:
                    continue
                theta = 2.0 * atan(value)
                key = round(theta * 10**14)
                candidate = ExactAngle(
                    f"H{bound}_{a}_{b}_{c}", a, b, c, theta, max(abs(a), abs(b), c), None, "NOT_CERTIFIED",
                )
                prior = selected.get(key)
                if prior is None or candidate.height < prior.height:
                    selected[key] = candidate
    theta_c = ExactAngle("theta_c", 0, 1, 4, THETA_C, 4, 234, "CERTIFIED_R5")
    selected[round(THETA_C * 10**14)] = theta_c
    return sorted(selected.values(), key=lambda row: row.theta)


def generic_angles() -> list[dict[str, object]]:
    values = [
        ("g_exp2", __import__("math").exp(-2.0), "t=exp(-2) is transcendental"),
        ("g_inv2pi", 1.0 / (2.0 * pi), "t=1/(2*pi) is transcendental"),
        ("g_inv3pi", 1.0 / (3.0 * pi), "t=1/(3*pi) is transcendental"),
    ]
    return [
        {"label": label, "t": t, "theta": 2.0 * atan(t), "classification": "Theta_G", "certificate": reason}
        for label, t, reason in values if 0.0 < t < T_MAX
    ]


def nearby_generic(angle: ExactAngle, scales: Iterable[int] = (400, 1200, 3600)) -> list[dict[str, object]]:
    rows = []
    for scale in scales:
        epsilon = 1.0 / (scale * pi)
        for sign in (-1, 1):
            t = angle.t_value + sign * epsilon
            if 0.0 < t < T_MAX:
                rows.append({
                    "label": f"{angle.label}_{'minus' if sign < 0 else 'plus'}_{scale}",
                    "theta": 2.0 * atan(t),
                    "t": t,
                    "classification": "Theta_G",
                    "certificate": "algebraic t_comm plus nonzero transcendental 1/(n*pi)",
                })
    return rows


def approximation_sequences(target_t: float, denominators: Iterable[int] = (5, 8, 13, 21, 34, 55)) -> dict[str, list[ExactAngle]]:
    target = float(target_t)
    sequences: dict[str, list[ExactAngle]] = {"rational": [], "sqrt2": [], "mixed": []}
    for q in denominators:
        p = round(q * target)
        sequences["rational"].append(ExactAngle(f"A_q{q}", p, 0, q, 2 * atan(p / q), max(abs(p), q), None, "NOT_CERTIFIED"))
        b = round(q * target / sqrt(2.0))
        sequences["sqrt2"].append(ExactAngle(f"B_q{q}", 0, b, q, 2 * atan(b * sqrt(2.0) / q), max(abs(b), q), None, "NOT_CERTIFIED"))
        b2 = (q % 5) - 2
        a2 = round(q * target - b2 * sqrt(2.0))
        sequences["mixed"].append(ExactAngle(f"C_q{q}", a2, b2, q, 2 * atan((a2 + b2 * sqrt(2.0)) / q), max(abs(a2), abs(b2), q), None, "NOT_CERTIFIED"))
    return sequences

