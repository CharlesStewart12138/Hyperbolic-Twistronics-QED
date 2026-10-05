"""Freeze the resource-gated m=7 tensor reassessment without false completion."""

from __future__ import annotations

from decimal import Context, Decimal, ROUND_CEILING, localcontext
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "local_full_kernel"
HODGE = ROOT / "production_code" / "hodge"
M6 = HODGE / "CM_047_NP_TENSOR_BOUND.json"
FORECAST = DATA / "EXACT_BALL7_TENSOR_RESOURCE_FORECAST.json"
TAIL7 = DATA / "EXACT_BALL7_TENSOR_TAIL.json"
PARTIAL_STATUS = DATA / "EXACT_BALL7_TENSOR_PARTIAL.status.json"
JSON_OUT = HODGE / "CM_047_NP_TENSOR_REASSESSMENT.json"
MD_OUT = HODGE / "CM_047_NP_TENSOR_REASSESSMENT.md"


def main() -> None:
    m6 = json.loads(M6.read_text(encoding="utf-8"))
    forecast = json.loads(FORECAST.read_text(encoding="utf-8"))
    tail = json.loads(TAIL7.read_text(encoding="utf-8"))
    up = Context(prec=70, rounding=ROUND_CEILING)
    with localcontext(up):
        sqrt2 = Decimal(2).sqrt()
        c0_7 = Decimal(tail["C0_per_abs_w_upper_directed"])
        c1_7 = Decimal(tail["C1_coordinate_per_abs_w_upper_directed"])
        c2_7 = Decimal(tail["coordinate_trace_C2_upper_directed"])
        c1_hodge = c1_7 * (sqrt2 + Decimal(1)).sqrt()
        c2_hodge = c2_7 * (sqrt2 + Decimal(1))
        tau_sum = Decimal(48) / (Decimal(2) * sqrt2)
        m6_c2 = Decimal(m6["tail_theorem"]["directed_coordinate_trace_upper"])
        reduction = c2_7 / m6_c2
        improvement = m6_c2 / c2_7

    partial_status = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7",
        "requested_scope": "complete exact centered Bolza ball d<=7a_B with every 4x4 tensor entry",
        "created": False,
        "status": "RESOURCE_GATED_NOT_EXECUTED",
        "resource_forecast": str(FORECAST.relative_to(ROOT)).replace("\\", "/"),
        "estimated_states_including_identity": forecast["m7_forecast"]["estimated_states_including_identity"],
        "estimated_peak_working_set_bytes": forecast["m7_forecast"]["estimated_peak_working_set_bytes"],
        "host_total_physical_memory_bytes": forecast["host"]["total_physical_memory_bytes"],
        "reason": forecast["decision"]["reason"],
        "m6_overwritten": False,
    }
    PARTIAL_STATUS.write_text(json.dumps(partial_status, indent=2) + "\n", encoding="utf-8")

    record = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7",
        "m6_baseline_retained": True,
        "m7": {
            "complete_exact_ball": False,
            "partial_status": str(PARTIAL_STATUS.relative_to(ROOT)).replace("\\", "/"),
            "resource_forecast": str(FORECAST.relative_to(ROOT)).replace("\\", "/"),
            "conditional_directed_tail_for_d_gt_7a_B": str(TAIL7.relative_to(ROOT)).replace("\\", "/"),
            "C0_per_abs_w_upper": str(c0_7),
            "C1_coordinate_per_abs_w_upper": str(c1_7),
            "C1_hodge_per_abs_w_upper": str(c1_hodge),
            "C2_coordinate_trace_upper": str(c2_7),
            "C2_hodge_upper": str(c2_hodge),
            "aligned_tensor_tail": "T_{>7}>=0, C8 invariant, Tr(T_{>7})<48; hence 2sqrt(2)(tau_-+tau_+)<48",
            "tau_minus_plus_sum_upper": str(tau_sum),
            "inversion_reduction": "Not evaluated because the exact m=7 ball was not generated.",
            "C8_orbit_reduction": "Not evaluated because the exact m=7 ball was not generated.",
            "beta_minus_partial_interval": None,
            "beta_plus_partial_interval": None,
            "certified_sector_intervals": None,
            "certified_common_root_intersection": None,
            "endpoint_ratio": None,
        },
        "uncertainty_decomposition": {
            "finite_ball_residual": "The exact shell 6a_B<d<=7a_B is missing; it cannot be subtracted from an upper bound and prevents an m=7 sector enclosure.",
            "shell_growth_bound": "Conditional d>7a_B coordinate C2 trace <47.7257051375.",
            "tensor_alignment_bound": "Conditional joint sector tail 2sqrt(2)(tau_-+tau_+)<48.",
            "derivative_bound": {"C0": str(c0_7), "C1_coordinate": str(c1_7), "C2_coordinate": str(c2_7)},
            "geometric_envelope_bound": "MPFR-directed secant ratio at m=7; shell ratio <0.144896600.",
            "dominant_remaining_uncertainty": "Missing complete exact shell 6a_B<d<=7a_B, caused by the in-memory exact-ball resource boundary.",
        },
        "tail_sharpening_relative_to_m6": {
            "m6_coordinate_C2_upper": str(m6_c2),
            "conditional_m7_coordinate_C2_upper": str(c2_7),
            "ratio_m7_over_m6": str(reduction),
            "improvement_factor": str(improvement),
            "root_interval_improved": False,
            "reason": "The exact m=7 partial tensor is absent, so the conditional d>7 tail cannot be combined into a complete m=7 enclosure.",
        },
        "m6_sector_intervals_retained": m6["full_kernel_sector_enclosure"],
        "m6_common_root_interval_retained": m6["aligned_tensor_zero_condition"]["common_root_necessary_interval"],
        "m6_endpoint_ratio_retained": "61.9661 approximately",
        "terminal_classification": "TENSOR-UNRESOLVED",
        "m7_completed": False,
        "m8_released": False,
        "m8_completed": False,
        "task_status": "Deferred",
        "exact_primary_stop_condition": "The complete exact d<=7a_B ball is estimated at 491,889,816 states and 81,271,655,167 bytes peak working set, exceeding 68,112,736,256 bytes host RAM; swap execution is forbidden.",
        "required_to_resume": "A proved out-of-core/external-memory exact Dirichlet-Voronoi flood and orbit accumulator below the registered resource guard, or a stronger theorem bounding the missing shell 6a_B<d<=7a_B without enumeration.",
        "scalar_route_authorized": False,
        "physical_parameters_retuned": False,
        "main_tex_modified": False,
    }
    JSON_OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    MD_OUT.write_text(
        "# CM-047-NP full-tensor reassessment at requested depth m=7\n\n"
        "## Terminal classification\n\n"
        "**TENSOR-UNRESOLVED.** The frozen m=6 result is retained verbatim. A complete m=7 tensor was not generated, and "
        "m=8 was not released.\n\n"
        "## Exact-ball resource gate\n\n"
        f"Scaling the frozen exact radius-6 enumeration by the hyperbolic disk-area ratio predicts "
        f"{forecast['m7_forecast']['estimated_states_including_identity']:,} states at radius 7 and "
        f"{forecast['m7_forecast']['estimated_peak_working_set_bytes'] / 2**30:.2f} GiB peak working set before additional "
        "tensor/orbit overhead. The host has 63.44 GiB total RAM and only the smaller registered working-set guard is "
        "available. An in-memory exact flood would therefore force paging and is prohibited.\n\n"
        "## Conditional directed tail beyond 7 a_B\n\n"
        "Without pretending the missing finite shell is known, the 256-bit MPFR secant bound gives\n\n"
        f"- C0/|w| < `{c0_7}`;\n"
        f"- coordinate C1/|w| < `{c1_7}`;\n"
        f"- coordinate C2 trace/|w| < `{c2_7}` < 48;\n"
        f"- canonical-Hodge C2/|w| < `{c2_hodge}`.\n\n"
        "C8 invariance yields the conditional joint aligned-sector budget "
        "`2 sqrt(2) (tau_-+tau_+) < 48`. This is a factor "
        f"{improvement:.6f} sharper than the m=6 tail for the strict region `d>7a_B`.\n\n"
        "## Why the root interval cannot be updated\n\n"
        "The exact shell `6a_B<d<=7a_B` has not been accumulated. An upper bound for `d>6a_B` minus an upper bound for "
        "`d>7a_B` is not a valid shell bound. Therefore no m=7 partial beta intervals, sector intervals, common-root "
        "intersection, or endpoint ratio are certified. The m=6 necessary interval remains "
        f"`[{record['m6_common_root_interval_retained'][0]}, {record['m6_common_root_interval_retained'][1]}]`.\n\n"
        "The exact next object is either a resource-certified out-of-core radius-7 flood/orbit accumulator or a stronger "
        "analytic theorem for the missing shell. No scalar q, parameter retuning, physical-angle claim, or manuscript "
        "insertion is made.\n",
        encoding="utf-8",
    )
    print(json.dumps({"classification": record["terminal_classification"], "m7_completed": False, "m8_released": False, "conditional_C2": str(c2_7)}, indent=2))


if __name__ == "__main__":
    main()
