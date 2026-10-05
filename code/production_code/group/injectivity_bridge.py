"""Certified bridge without conflating word and geometric injectivity.

The bridge provides exact geometry for displayed kernel witnesses and
finite-radius universal-cover comparison tables.  A word lower bound alone is
never promoted to a physical no-wraparound certificate.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, asdict
from pathlib import Path
import csv
import json
import math

from production_code.group.nielsen import standard_to_geometric
from production_code.group.surface_group import free_reduce
from production_code.group.universal_cover import (
    FieldValue,
    MatrixValue,
    enumerate_ball,
    exact_cosh_distance_over_R,
    field_to_complex,
    matrix_from_word,
)


ACTIVE_DC_OVER_A = 3.0
_H_TO_G = {
    "h0": ("g0",), "h0_inv": ("g4",),
    "h1": ("g5",), "h1_inv": ("g1",),
    "h2": ("g2",), "h2_inv": ("g6",),
    "h3": ("g7",), "h3_inv": ("g3",),
}


@dataclass(frozen=True)
class WitnessGeometry:
    standard_word: tuple[str, ...]
    geometric_word: tuple[str, ...]
    standard_word_length: int
    geometric_word_length: int
    based_displacement_over_a: float
    translation_length_over_a: float
    based_injectivity_upper_bound_over_a: float
    global_injectivity_upper_bound_over_a: float
    cosh_based_displacement_over_R_exact: FieldValue
    half_trace_exact: FieldValue


def standard_word_to_geometric(word: Sequence[str]) -> tuple[str, ...]:
    oriented = standard_to_geometric(free_reduce(word))
    return tuple(token for h_token in oriented for token in _H_TO_G[h_token])


def _half_trace(matrix: MatrixValue) -> FieldValue:
    """Return Re(a)=tr(M)/2 in the universal-cover exact field encoding."""

    a = matrix[0]
    return (a[0],) + a[1:5] + (0, 0, 0, 0)


def _geometry_from_matrix(matrix: MatrixValue) -> tuple[float, float, FieldValue, FieldValue]:
    spacing_over_R = 2.0 * math.acosh(1.0 + math.sqrt(2.0))
    cosh_exact = exact_cosh_distance_over_R(matrix)
    cosh_value = max(1.0, field_to_complex(cosh_exact).real)
    based_over_a = math.acosh(cosh_value) / spacing_over_R
    trace_exact = _half_trace(matrix)
    half_trace_value = abs(field_to_complex(trace_exact).real)
    translation_over_a = 2.0 * math.acosh(max(1.0, half_trace_value)) / spacing_over_R
    return based_over_a, translation_over_a, cosh_exact, trace_exact


def witness_geometry(standard_word: Sequence[str]) -> WitnessGeometry:
    standard = free_reduce(standard_word)
    if not standard:
        raise ValueError("kernel witness must be nontrivial in the surface group")
    geometric = standard_word_to_geometric(standard)
    matrix = matrix_from_word(geometric)
    based, translation, cosh_exact, trace_exact = _geometry_from_matrix(matrix)
    return WitnessGeometry(
        standard_word=standard,
        geometric_word=geometric,
        standard_word_length=len(standard),
        geometric_word_length=len(geometric),
        based_displacement_over_a=based,
        translation_length_over_a=translation,
        based_injectivity_upper_bound_over_a=based / 2.0,
        global_injectivity_upper_bound_over_a=translation / 2.0,
        cosh_based_displacement_over_R_exact=cosh_exact,
        half_trace_exact=trace_exact,
    )


def separated_injectivity_record(
    *,
    quotient_id: str,
    word_injectivity_radius: float | None,
    standard_kernel_witness: Sequence[str] | None,
    active_cutoff_over_a: float = ACTIVE_DC_OVER_A,
) -> dict[str, object]:
    """Serialize distinct radii and fail closed on missing global geometry."""

    if active_cutoff_over_a <= 0:
        raise ValueError("active cutoff must be positive")
    geometry = witness_geometry(standard_kernel_witness) if standard_kernel_witness else None
    witness_rejects = (
        geometry is not None
        and geometry.global_injectivity_upper_bound_over_a <= active_cutoff_over_a
    )
    return {
        "schema_version": "1.0",
        "quotient_id": quotient_id,
        "word_metric": "standard_primitive_s8",
        "r_inj_word": word_injectivity_radius,
        "r_inj_word_units": "standard-generator steps",
        "r_inj_based_geo_over_a": None,
        "r_inj_based_geo_status": "NOT_COMPUTED_GLOBAL_MINIMUM",
        "r_inj_global_geo_over_a": None,
        "r_inj_global_geo_status": "NOT_COMPUTED_GLOBAL_SYSTOLE",
        "kernel_witness": asdict(geometry) if geometry is not None else None,
        "witness_based_upper_bound_over_a": (
            geometry.based_injectivity_upper_bound_over_a if geometry else None
        ),
        "witness_global_upper_bound_over_a": (
            geometry.global_injectivity_upper_bound_over_a if geometry else None
        ),
        "active_Dc_over_a": active_cutoff_over_a,
        "physical_requirement": "r_inj_global_geo/a > Dc/a",
        "physical_no_wraparound_pass": False if witness_rejects else None,
        "physical_status": "REJECTED_BY_EXPLICIT_TRANSLATION_WITNESS" if witness_rejects
                           else "NOT_CERTIFIED_GEOMETRY_INCOMPLETE",
        "word_lower_bound_promoted_to_geometric": False,
        "based_radius_copied_from_word_radius": False,
        "global_radius_copied_from_word_radius": False,
    }


def finite_radius_bounds(max_radius: int = 6) -> list[dict[str, object]]:
    """Return exact-matrix finite-radius minima for the geometric word shells."""

    ball = enumerate_ball(max_radius)
    minima: dict[int, dict[str, object]] = {}
    for element in ball.elements[1:]:
        based, translation, cosh_exact, trace_exact = _geometry_from_matrix(element.matrix)
        row = minima.setdefault(element.word_length, {
            "radius": element.word_length,
            "minimum_based_displacement_over_a": math.inf,
            "minimum_translation_length_over_a": math.inf,
        })
        if based < row["minimum_based_displacement_over_a"]:
            row.update({
                "minimum_based_displacement_over_a": based,
                "based_witness": element.representative,
                "based_cosh_exact": cosh_exact,
            })
        if translation < row["minimum_translation_length_over_a"]:
            row.update({
                "minimum_translation_length_over_a": translation,
                "translation_witness": element.representative,
                "translation_half_trace_exact": trace_exact,
            })
    return [minima[radius] for radius in sorted(minima)]


def write_bridge_artifacts(output_dir: Path, validation_dir: Path) -> dict[str, Path]:
    output = Path(output_dir)
    validation = Path(validation_dir)
    output.mkdir(parents=True, exist_ok=True)
    validation.mkdir(parents=True, exist_ok=True)

    bounds = finite_radius_bounds(6)
    bounds_path = output / "word_geometry_bounds_radii_1_6.csv"
    with bounds_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow((
            "geometric_word_radius", "minimum_based_displacement_over_a",
            "based_witness", "based_cosh_exact", "minimum_translation_length_over_a",
            "translation_witness", "translation_half_trace_exact",
        ))
        for row in bounds:
            writer.writerow((
                row["radius"], format(row["minimum_based_displacement_over_a"], ".17g"),
                " ".join(row["based_witness"]), json.dumps(row["based_cosh_exact"]),
                format(row["minimum_translation_length_over_a"], ".17g"),
                " ".join(row["translation_witness"]), json.dumps(row["translation_half_trace_exact"]),
            ))

    fixture = separated_injectivity_record(
        quotient_id="QVAL_Z4_POWER4_N256",
        word_injectivity_radius=2.0,
        standard_kernel_witness=("a1", "a1", "a1", "a1"),
    )
    fixture_path = validation / "QVAL_Z4_POWER4_INJECTIVITY_BRIDGE.json"
    fixture_path.write_text(json.dumps(fixture, indent=2), encoding="utf-8")

    contract_path = output / "INJECTIVITY_BRIDGE_CONTRACT.json"
    contract_path.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-INJ-BRIDGE",
        "universal_inequalities_for_a_geometric_word_witness_of_length_n": [
            "translation_length(gamma) <= based_displacement(0,gamma*0) <= n*a_B",
            "r_inj_global_geo/a_B <= r_inj_based_geo/a_B <= n/2 for that kernel witness",
        ],
        "forbidden_converse": "r_inj_word > Dc/a does not imply r_inj_geo > Dc",
        "physical_requirement": "r_inj_global_geo/a_B > 3.0",
        "finite_radius_table": bounds_path.name,
        "known_validation_fixture": str(fixture_path).replace("\\", "/"),
    }, indent=2), encoding="utf-8")
    return {"bounds": bounds_path, "fixture": fixture_path, "contract": contract_path}

