"""Exact acceptance contract for the physical Bolza nearest-neighbour shell.

The physical shell is the eight side-pairing maps ``g0,...,g7``.  The
standard-presentation letters are retained only as an algebraic basis and
are not substituted for this geometric shell.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from production_code.group.bolza_interface import (
    ETA,
    _field_data,
    _field_generator,
    _field_mobius,
    _inverse,
    _matmul,
    exact_certificate as bolza_certificate,
)
from production_code.group.nielsen import (
    _matrix_from_standard_word,
    geometric_to_standard,
)


GEOMETRIC_SHELL = tuple(f"g{index}" for index in range(8))
GEOMETRIC_INVERSE_INDEX = {index: (index + 4) % 8 for index in range(8)}
GEOMETRIC_TO_ORIENTED_WORD = {
    0: ("h0",),
    1: ("h1_inv",),
    2: ("h2",),
    3: ("h3_inv",),
    4: ("h0_inv",),
    5: ("h1",),
    6: ("h2_inv",),
    7: ("h3",),
}
GEOMETRIC_TO_STANDARD_WORD = {
    index: geometric_to_standard(word)
    for index, word in GEOMETRIC_TO_ORIENTED_WORD.items()
}


@dataclass(frozen=True)
class GeometricShellCertificate:
    gsc01_side_sharing_nearest_neighbours: bool
    gsc02_eight_distinct_neighbours: bool
    gsc03_inverse_closed: bool
    gsc04_universal_centre_orbit_degree_eight: bool
    gsc05_c8_cyclic_action: bool
    gsc06_physical_88_resonator_graph: bool
    gsc07_exact_nielsen_words: bool

    @property
    def passed(self) -> bool:
        return all(self.__dict__.values())


def _identity() -> tuple[Any, ...]:
    data = _field_data()
    return (data["one"], data["zero"], data["zero"], data["one"])


def _rotation() -> tuple[Any, ...]:
    data = _field_data()
    return (data["zeta16"], data["zero"], data["zero"], data["zeta16"] ** -1)


def neighbour_centres_exact() -> tuple[Any, ...]:
    """Return the eight exact images ``g_nu(0)`` in the algebraic field."""

    data = _field_data()
    return tuple(_field_mobius(_field_generator(index), data["zero"])
                 for index in range(8))


def certificate() -> GeometricShellCertificate:
    data = _field_data()
    geometric = bolza_certificate()
    generators = tuple(_field_generator(index) for index in range(8))
    centres = neighbour_centres_exact()
    eta = data["field"].convert(ETA)
    expected_centres = tuple(eta * data["zeta8"] ** index for index in range(8))

    # Side pairing plus g_nu(0)=eta*zeta_8^nu identifies the octagon across
    # that side; its centre separation is 2*R*artanh(eta)=a_B.
    gsc01 = (
        geometric.endpoint_pairing
        and geometric.midpoint_pairing
        and centres == expected_centres
        and data["beta"] == data["alpha"] * eta
    )
    gsc02 = all(centres[left] != centres[right]
                for left in range(8) for right in range(left + 1, 8))
    gsc03 = all(
        generators[GEOMETRIC_INVERSE_INDEX[index]] == _inverse(generators[index])
        for index in range(8)
    )
    gsc04 = gsc01 and gsc02 and gsc03 and len(centres) == 8

    rotation = _rotation()
    rotation_inverse = _inverse(rotation)
    gsc05 = all(
        _matmul(_matmul(rotation, generators[index]), rotation_inverse)
        == generators[(index + 1) % 8]
        for index in range(8)
    )

    # The regular {8,8} resonator graph is the dual centre graph: an edge is
    # exactly one shared octagon side.  GSC01--GSC04 therefore certify the
    # physical degree-eight nearest-neighbour graph without presentation
    # relabelling.
    gsc06 = geometric.octagon_geometry and gsc01 and gsc04 and gsc05

    gsc07 = all(
        _matrix_from_standard_word(GEOMETRIC_TO_STANDARD_WORD[index])
        == generators[index]
        for index in range(8)
    )
    return GeometricShellCertificate(gsc01, gsc02, gsc03, gsc04, gsc05, gsc06, gsc07)


def acceptance_rows() -> tuple[dict[str, object], ...]:
    cert = certificate()
    explanations = (
        ("GSC01", cert.gsc01_side_sharing_nearest_neighbours,
         "exact side endpoints/midpoint and g_nu(0)=eta*zeta8^nu"),
        ("GSC02", cert.gsc02_eight_distinct_neighbours,
         "the eight algebraic centre images are pairwise distinct"),
        ("GSC03", cert.gsc03_inverse_closed,
         "g_(nu+4)=g_nu^{-1}"),
        ("GSC04", cert.gsc04_universal_centre_orbit_degree_eight,
         "the side-sharing centre orbit has exactly eight incident edges"),
        ("GSC05", cert.gsc05_c8_cyclic_action,
         "rho*g_nu*rho^{-1}=g_(nu+1)"),
        ("GSC06", cert.gsc06_physical_88_resonator_graph,
         "dual graph of the regular {8,8} octagon tiling"),
        ("GSC07", cert.gsc07_exact_nielsen_words,
         "each geometric generator equals its transported standard word"),
    )
    return tuple({"test_id": test_id, "passed": passed, "evidence": evidence}
                 for test_id, passed, evidence in explanations)
