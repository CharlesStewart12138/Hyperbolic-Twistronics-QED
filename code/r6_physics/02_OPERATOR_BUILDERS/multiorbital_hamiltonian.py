"""Frozen orbital contract.

The current production configuration contains one orbital per site.  The
manuscript's symbolic s/p1/p2 expressions do not include numerical
Slater--Koster functions, so this module deliberately refuses to invent them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FrozenOrbitalModel:
    labels: tuple[str, ...] = ("scalar",)
    onsite_over_t: tuple[float, ...] = (0.0,)
    source: str = "00_FROZEN_INPUTS/config/model.yaml"

    @property
    def count(self) -> int:
        return len(self.labels)

    def validate(self) -> None:
        if self.labels != ("scalar",) or self.onsite_over_t != (0.0,):
            raise ValueError("R6 only permits the numerically frozen scalar orbital model")


def require_numerically_frozen_multiorbital() -> None:
    raise RuntimeError(
        "The symbolic three-orbital manuscript model has no frozen numerical "
        "Slater--Koster amplitudes/functions; using it would invent parameters."
    )

