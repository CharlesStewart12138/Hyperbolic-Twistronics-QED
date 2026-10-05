"""Observable-specific PF-KER-005 tail-budget audit.

The shell estimates are produced by ``group.local_full_kernel`` in the
standard cohomology coordinates.  PF-HOD-002 fixes the canonical tangent
metric G with lambda_min(G)=sqrt(2)-1.  Consequently

    ||u||_2 <= sqrt(sqrt(2)+1) ||u||_G

and a bilinear second derivative acquires the square of this factor.  This
module records the distinct C0, C1 and C2 consequences; it deliberately does
not turn convergence of the operator tails into an observable certificate
without the required spectral margins.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Mapping

from production_code.group.local_full_kernel import physical_secant_tail


HODGE_C1_FACTOR = math.sqrt(math.sqrt(2.0) + 1.0)
HODGE_C2_FACTOR = math.sqrt(2.0) + 1.0


@dataclass(frozen=True)
class CanonicalTailRow:
    first_omitted_shell: int
    c0_per_abs_w: float
    c1_coordinate_per_abs_w: float
    c1_hodge_per_abs_w: float
    c2_coordinate_per_abs_w: float
    c2_hodge_per_abs_w: float


def canonical_tail(first_omitted_shell: int, abs_w: float = 1.0) -> CanonicalTailRow:
    """Return C0/C1/C2 bounds in the frozen canonical Hodge norm."""

    amplitude = float(abs_w)
    if not math.isfinite(amplitude) or amplitude < 0.0:
        raise ValueError("abs_w must be finite and nonnegative")
    row = physical_secant_tail(first_omitted_shell)
    return CanonicalTailRow(
        first_omitted_shell=row.first_omitted_shell,
        c0_per_abs_w=amplitude * row.c0_per_abs_w,
        c1_coordinate_per_abs_w=amplitude * row.c1_per_abs_w,
        c1_hodge_per_abs_w=amplitude * HODGE_C1_FACTOR * row.c1_per_abs_w,
        c2_coordinate_per_abs_w=amplitude * row.c2_per_abs_w,
        c2_hodge_per_abs_w=amplitude * HODGE_C2_FACTOR * row.c2_per_abs_w,
    )


# Each observable owns its own acceptance margin.  A generic percentage is
# intentionally absent.  ``formula`` names e0/e1/e2 from ``canonical_tail``.
OBSERVABLE_CONTRACTS: Mapping[str, dict[str, object]] = {
    "energy_edge": {
        "topology": "C0",
        "formula": "epsilon_energy=e0",
        "required_inputs": ("abs_w_over_t", "energy_tolerance_over_t"),
    },
    "bandwidth": {
        "topology": "C0",
        "formula": "epsilon_bandwidth=2*e0",
        "required_inputs": ("abs_w_over_t", "bandwidth_tolerance_over_t"),
    },
    "spectral_gap": {
        "topology": "C0",
        "formula": "epsilon_gap=2*e0",
        "required_inputs": ("abs_w_over_t", "nominal_isolation_gap_over_t", "gap_tolerance_over_t"),
    },
    "riesz_projector": {
        "topology": "C0",
        "formula": "epsilon_projector=e0/(Delta-e0), with e0<Delta/2",
        "required_inputs": ("abs_w_over_t", "nominal_isolation_gap_over_t", "projector_tolerance"),
    },
    "generalized_velocity": {
        "topology": "C1",
        "formula": "epsilon_velocity=e1+2*M1*e0/(Delta-e0)",
        "required_inputs": (
            "abs_w_over_t",
            "nominal_isolation_gap_over_t",
            "hamiltonian_c1_bound_over_t",
            "velocity_tolerance_over_t",
        ),
    },
    "first_spectral_derivative": {
        "topology": "C1",
        "formula": "epsilon_dE=e1+2*M1*e0/(Delta-e0)",
        "required_inputs": (
            "abs_w_over_t",
            "nominal_isolation_gap_over_t",
            "hamiltonian_c1_bound_over_t",
            "first_derivative_tolerance_over_t",
        ),
    },
    "spectral_hessian": {
        "topology": "C2",
        "formula": "epsilon_H=B_H(e0,e1,e2,d,L_C,M1,M2)",
        "required_inputs": (
            "abs_w_over_t",
            "riesz_contour_distance_over_t",
            "riesz_contour_length_over_t",
            "hamiltonian_c1_bound_over_t",
            "hamiltonian_c2_bound_over_t",
            "hessian_tolerance_over_t",
        ),
    },
    "principal_curvature": {
        "topology": "C2",
        "formula": "epsilon_curvature=(sqrt(2)+1)*B_H",
        "required_inputs": (
            "abs_w_over_t",
            "riesz_contour_distance_over_t",
            "riesz_contour_length_over_t",
            "hamiltonian_c1_bound_over_t",
            "hamiltonian_c2_bound_over_t",
            "principal_curvature_tolerance_over_t",
        ),
    },
    "hodge_hessian_comparison": {
        "topology": "C2",
        "formula": "epsilon_hodge=(sqrt(2)+1)*B_H",
        "required_inputs": (
            "abs_w_over_t",
            "riesz_contour_distance_over_t",
            "riesz_contour_length_over_t",
            "hamiltonian_c1_bound_over_t",
            "hamiltonian_c2_bound_over_t",
            "hodge_comparison_tolerance_over_t",
        ),
    },
}


def observable_closure_audit(values: Mapping[str, float | int | None]) -> dict[str, object]:
    """Audit whether every observable has all independently frozen inputs.

    This is an input-completeness audit, not a numerical optimizer.  Even a
    complete registry must still satisfy the strict inequalities stated in
    the per-observable formulas before PF-KER-005 can close.
    """

    observables: dict[str, object] = {}
    all_complete = True
    for name, contract in OBSERVABLE_CONTRACTS.items():
        required = tuple(contract["required_inputs"])
        missing = tuple(key for key in required if values.get(key) is None)
        complete = not missing
        all_complete = all_complete and complete
        observables[name] = {
            "topology": contract["topology"],
            "formula": contract["formula"],
            "required_inputs": required,
            "missing_inputs": missing,
            "input_complete": complete,
        }
    return {
        "all_observables_input_complete": all_complete,
        "may_close_pf_ker_005": all_complete,
        "observables": observables,
    }


def deterministic_reassessment_record() -> dict[str, object]:
    """Return the current, deliberately non-promoted PF-KER-005 record."""

    selected = [asdict(canonical_tail(m)) for m in (3, 6, 9, 12)]
    audit = observable_closure_audit({})
    return {
        "task_id": "PF-KER-005",
        "scope": "LOCAL_SCALAR_CHARACTER",
        "frozen_point": {"h_over_a": 0.5, "lambda_perp_over_a": 0.2},
        "hodge_conversion": {
            "lambda_min_G": math.sqrt(2.0) - 1.0,
            "c1_factor": HODGE_C1_FACTOR,
            "c2_factor": HODGE_C2_FACTOR,
        },
        "selected_tail_rows_per_abs_w": selected,
        "observable_closure": audit,
        "production_cutoff_first_omitted_shell": 3,
        "production_cutoff_closes": False,
        "status": "Blocked",
        "blocked_reason": (
            "The canonical C0/C1/C2 operator tails are now explicit, but the project contains "
            "no common numerical registry for |w|/t, target isolation/contour margins, M1/M2, "
            "and separate energy, gap, projector, velocity, derivative, Hessian, principal-"
            "curvature, and Hodge-comparison tolerances."
        ),
    }

