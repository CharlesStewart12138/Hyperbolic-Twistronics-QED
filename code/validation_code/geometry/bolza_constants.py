"""VT-002 independent regression of the Bolza constants.

MANUSCRIPT SOURCE:
Equations: (46)--(54).
Section: genus-two regular-octagon geometry, pp. 7--8.
Model scope: exact dimensionless Bolza geometry for every R>0.
"""

from __future__ import annotations

from math import acosh, isclose, sqrt

from production_code.geometry.bolza import constants


def validate_bolza_constants(radii: tuple[float, ...] = (0.25, 1.0, 3.5)) -> dict[str, object]:
    """Check analytic identities and scale independence at 1e-12 relative error.

    MANUSCRIPT SOURCE:
    Equations: a_B/R=2 arcosh(1+sqrt(2)); |z_vertex|=2^(-1/4).
    Model scope: exact {8,8} Bolza tessellation, not a fitted discretization.
    """

    expected_kappa = 2.0 * acosh(1.0 + sqrt(2.0))
    expected_vertex_radius = 2.0 ** (-0.25)
    measurements = []
    for radius in radii:
        measured = constants(radius)
        measurements.append(
            {
                "R": radius,
                "a_B_over_R": measured.lattice_spacing / radius,
                "kappa_B": measured.kappa_B,
                "vertex_radius": measured.vertex_disk_radius,
            }
        )
    display_decimal = 3.057141839
    literal_relative_difference = abs(expected_kappa / display_decimal - 1.0)
    passed = all(
        isclose(item["a_B_over_R"], expected_kappa, rel_tol=1e-12)
        and isclose(item["kappa_B"], expected_kappa, rel_tol=1e-12)
        and round(item["kappa_B"], 9) == display_decimal
        and isclose(item["vertex_radius"], expected_vertex_radius, rel_tol=1e-12)
        for item in measurements
    )
    return {
        "test_id": "VT-002",
        "relative_tolerance": 1e-12,
        "expected_kappa_exact": expected_kappa,
        "expected_kappa_decimal": display_decimal,
        "display_decimal_places": 9,
        "literal_relative_difference": literal_relative_difference,
        "expected_vertex_radius": expected_vertex_radius,
        "measurements": tuple(measurements),
        "passed": passed,
    }
