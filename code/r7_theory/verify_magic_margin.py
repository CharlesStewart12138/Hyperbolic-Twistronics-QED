"""Exact rational replay of the R7 operational anchor margin."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any


def build_certificate() -> dict[str, Any]:
    """Build and verify the exact R7 margin certificate in memory."""
    spectral_upper = Fraction(1, 36)
    propagation_upper = Fraction(1, 48)
    return_lower = Fraction(37, 48)
    coherence_lower = Fraction(1, 1)
    ldos_lower = Fraction(4, 5)

    thresholds = {
        "spectral_max": Fraction(1, 18),
        "propagation_max": Fraction(1, 24),
        "return_min": Fraction(3, 4),
        "coherence_min": Fraction(3, 4),
        "ldos_min": Fraction(3, 4),
    }
    margins = {
        "spectral": thresholds["spectral_max"] - spectral_upper,
        "propagation": thresholds["propagation_max"] - propagation_upper,
        "return": return_lower - thresholds["return_min"],
        "coherence": coherence_lower - thresholds["coherence_min"],
        "ldos": ldos_lower - thresholds["ldos_min"],
    }
    if not all(value > 0 for value in margins.values()):
        raise ArithmeticError("an R7 operational margin is not strict")
    joint = min(margins.values())
    if joint != Fraction(1, 48):
        raise ArithmeticError(f"unexpected joint margin: {joint}")

    def encode(value: Fraction) -> dict[str, object]:
        return {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "decimal": float(value),
        }

    return {
        "schema": "R7_MAGIC_MARGIN_CERTIFICATE_V1",
        "arithmetic": "exact rational",
        "hypotheses": {
            "epsilon_over_gap": "strictly less than 1/6",
            "epsilon_times_T": "at most 1/4",
            "eta_over_epsilon": "at least 2 (epsilon>0)",
        },
        "margins": {key: encode(value) for key, value in margins.items()},
        "joint_margin": encode(joint),
        "status": "PASS",
    }


def default_output() -> Path:
    return Path(__file__).resolve().parents[2] / "outputs" / "r7" / "magic_margin_certificate.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default_output())
    args = parser.parse_args(argv)
    certificate = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print("R7_MAGIC_MARGIN_CERTIFICATE = PASS")
    print("R7_JOINT_MARGIN = 1/48")
    print(f"R7_CERTIFICATE_PATH = {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
