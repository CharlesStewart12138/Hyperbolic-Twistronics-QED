from fractions import Fraction

from r7_theory import build_certificate


def test_exact_joint_margin() -> None:
    certificate = build_certificate()
    joint = certificate["joint_margin"]
    assert Fraction(joint["numerator"], joint["denominator"]) == Fraction(1, 48)
    assert certificate["status"] == "PASS"


def test_all_operational_margins_are_strict() -> None:
    certificate = build_certificate()
    for margin in certificate["margins"].values():
        assert Fraction(margin["numerator"], margin["denominator"]) > 0
