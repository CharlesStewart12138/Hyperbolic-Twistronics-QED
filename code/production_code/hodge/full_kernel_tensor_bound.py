"""Package the exact-ball full-kernel tensor and its certified two-sector tail.

This module intentionally does not manufacture a scalar ``q_infinity``.  The
physical nearest-neighbour tensor and the complete radius-six partial tensor
span the two-dimensional C8-invariant self-adjoint commutant, so the correct
data are the two generalized sector coefficients.
"""

from __future__ import annotations

from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PARTIAL_PATH = ROOT / "data" / "production" / "local_full_kernel" / "EXACT_BALL6_TENSOR_PARTIAL.json"
TAIL_PATH = ROOT / "data" / "production" / "local_full_kernel" / "EXACT_BALL6_TENSOR_TAIL.json"
LEGACY_PATH = ROOT / "data" / "production" / "local_full_kernel" / "LOCAL_FULL_KERNEL_PILOT.json"
JSON_PATH = ROOT / "production_code" / "hodge" / "CM_047_NP_TENSOR_BOUND.json"
MD_PATH = ROOT / "production_code" / "hodge" / "CM_047_NP_TENSOR_BOUND.md"

PRECISION = 70
FLOOR = Context(prec=PRECISION, rounding=ROUND_FLOOR)
CEILING = Context(prec=PRECISION, rounding=ROUND_CEILING)


def add_lo(a: Decimal, b: Decimal) -> Decimal:
    return FLOOR.add(a, b)


def add_hi(a: Decimal, b: Decimal) -> Decimal:
    return CEILING.add(a, b)


def sub_lo(a: Decimal, b: Decimal) -> Decimal:
    return FLOOR.subtract(a, b)


def sub_hi(a: Decimal, b: Decimal) -> Decimal:
    return CEILING.subtract(a, b)


def mul_lo(a: Decimal, b: Decimal) -> Decimal:
    if a < 0 or b < 0:
        raise ValueError("mul_lo is restricted to nonnegative operands")
    return FLOOR.multiply(a, b)


def mul_hi(a: Decimal, b: Decimal) -> Decimal:
    if a < 0 or b < 0:
        raise ValueError("mul_hi is restricted to nonnegative operands")
    return CEILING.multiply(a, b)


def div_hi(a: Decimal, b: Decimal) -> Decimal:
    if a < 0 or b <= 0:
        raise ValueError("div_hi requires a>=0 and b>0")
    return CEILING.divide(a, b)


def fmt(value: Decimal, digits: int = 15) -> str:
    with localcontext(Context(prec=digits, rounding=ROUND_CEILING)):
        return format(+value, ".12g")


def load() -> tuple[dict, dict, dict]:
    return (
        json.loads(PARTIAL_PATH.read_text(encoding="utf-8")),
        json.loads(TAIL_PATH.read_text(encoding="utf-8")),
        json.loads(LEGACY_PATH.read_text(encoding="utf-8")),
    )


def build_record() -> dict:
    partial, tail, legacy = load()
    lo = [[Decimal(value) for value in row] for row in partial["partial_tensor_entrywise_lower"]]
    hi = [[Decimal(value) for value in row] for row in partial["partial_tensor_entrywise_upper"]]

    with localcontext(FLOOR):
        sqrt2_lo = Decimal(2).sqrt()
    with localcontext(CEILING):
        sqrt2_hi = Decimal(2).sqrt()

    # Every invariant symmetric tensor is fixed by x=B_23 and y=B_33.  For
    # B relative to C_S, beta_-=y+sqrt(2)x and beta_+=y-sqrt(2)x.
    x_lo, x_hi = lo[2][3], hi[2][3]
    y_lo, y_hi = lo[3][3], hi[3][3]
    beta_minus_lo = add_lo(y_lo, mul_lo(sqrt2_lo, x_lo))
    beta_minus_hi = add_hi(y_hi, mul_hi(sqrt2_hi, x_hi))
    beta_plus_lo = sub_lo(y_lo, mul_hi(sqrt2_hi, x_hi))
    beta_plus_hi = sub_hi(y_hi, mul_lo(sqrt2_lo, x_lo))
    if beta_plus_lo <= 0:
        raise ValueError("unexpected nonpositive plus-sector partial coefficient")

    tail_integer = Decimal(str(tail["certified_rational_coordinate_trace_upper"]))
    two = Decimal(2)
    four = Decimal(4)

    # T_tail=G(tau_- P_-+tau_+ P_+), tau_s>=0, and
    # Tr(T_tail)=2 sqrt(2)(tau_-+tau_+) <= 261.
    trace_sector_den_lo = mul_lo(two, sqrt2_lo)
    tau_sum_hi = div_hi(tail_integer, trace_sector_den_lo)
    c_minus_lo = sub_lo(sqrt2_lo, Decimal(1))
    c_minus_hi = sub_hi(sqrt2_hi, Decimal(1))
    c_plus_lo = add_lo(sqrt2_lo, Decimal(1))
    c_plus_hi = add_hi(sqrt2_hi, Decimal(1))

    # Algebraically 2*sqrt(2)*(sqrt(2)-1)=4-2*sqrt(2) and
    # 2*sqrt(2)*(sqrt(2)+1)=4+2*sqrt(2).  Lower denominators give upper ratios.
    minus_den_lo = sub_lo(four, mul_hi(two, sqrt2_hi))
    plus_den_lo = add_lo(four, mul_lo(two, sqrt2_lo))
    delta_beta_minus_hi = div_hi(tail_integer, minus_den_lo)
    delta_beta_plus_hi = div_hi(tail_integer, plus_den_lo)
    full_beta_minus_hi = add_hi(beta_minus_hi, delta_beta_minus_hi)
    full_beta_plus_hi = add_hi(beta_plus_hi, delta_beta_plus_hi)

    # If a common tensor root exists, beta_-^infty=beta_+^infty=beta_common.
    # Substitute the smallest sector tails compatible with a proposed common
    # beta into the joint trace budget to obtain its sharper upper endpoint.
    numerator_hi = tau_sum_hi
    numerator_hi = add_hi(numerator_hi, mul_hi(c_minus_hi, beta_minus_hi))
    numerator_hi = add_hi(numerator_hi, mul_hi(c_plus_hi, beta_plus_hi))
    common_beta_hi = div_hi(numerator_hi, trace_sector_den_lo)
    common_beta_lo = max(beta_minus_lo, beta_plus_lo)

    half = Decimal("0.5")
    root_minus = [mul_lo(half, beta_minus_lo), mul_hi(half, full_beta_minus_hi)]
    root_plus = [mul_lo(half, beta_plus_lo), mul_hi(half, full_beta_plus_hi)]
    common_root = [mul_lo(half, common_beta_lo), mul_hi(half, common_beta_hi)]

    old_lower = Decimal(str(legacy["q_infinity_interval"][0]))
    old_upper = Decimal(str(legacy["q_infinity_interval"][1]))
    old_c2 = Decimal(str(legacy["tail_table"][0]["c2_per_abs_w"]))
    directed_c2 = Decimal(tail["coordinate_trace_C2_upper_directed"])

    record = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-TENSOR-BOUND",
        "status": "Done_MATERIAL_BOUND_IMPROVEMENT",
        "scope": "LOCAL centered/aligned Bolza point; no angle continuation or bulk promotion",
        "inputs": {
            "complete_exact_ball": str(PARTIAL_PATH.relative_to(ROOT)).replace("\\", "/"),
            "directed_tail": str(TAIL_PATH.relative_to(ROOT)).replace("\\", "/"),
            "legacy_scalar_pilot": str(LEGACY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "dangerous_nonidentity_elements": partial["dangerous_nonidentity_elements"],
            "inversion_C8_orbits": partial["inversion_C8_orbits"],
            "mpfr_partial_precision_bits": partial["mpfr_precision_bits"],
            "mpfr_tail_precision_bits": tail["mpfr_precision_bits"],
        },
        "partial_tensor_entrywise_lower": partial["partial_tensor_entrywise_lower"],
        "partial_tensor_entrywise_upper": partial["partial_tensor_entrywise_upper"],
        "exact_C8_parameterization": {
            "x": "B_23",
            "y": "B_33",
            "matrix": [
                ["-4x+3y", "-3x+2y", "x-y", "-2x+y"],
                ["-3x+2y", "-4x+3y", "2x-y", "-x+y"],
                ["x-y", "2x-y", "y", "x"],
                ["-2x+y", "-x+y", "x", "y"],
            ],
            "verified_integer_orbits": partial["exact_C8_invariant_orbit_moments"],
        },
        "partial_generalized_coefficients_B_relative_to_C_S": {
            "minus_formula": "beta_- = y + sqrt(2) x",
            "plus_formula": "beta_+ = y - sqrt(2) x",
            "minus_interval": [str(beta_minus_lo), str(beta_minus_hi)],
            "plus_interval": [str(beta_plus_lo), str(beta_plus_hi)],
            "multiplicity_each": 2,
        },
        "tail_theorem": {
            "first_omitted_shell": 6,
            "directed_coordinate_trace_upper": str(directed_c2),
            "certified_rational_coordinate_trace_upper": 261,
            "loewner_and_symmetry": "T_tail>=0, U^T T_tail U=T_tail, Tr(T_tail)<=261",
            "sector_form": "T_tail=G(tau_- P_- + tau_+ P_+), tau_-,tau_+>=0",
            "joint_budget": "2 sqrt(2)(tau_-+tau_+)<=261",
            "tau_sum_upper": str(tau_sum_hi),
            "individual_delta_beta_upper": {
                "minus": str(delta_beta_minus_hi),
                "plus": str(delta_beta_plus_hi),
            },
        },
        "full_kernel_sector_enclosure": {
            "beta_minus": [str(beta_minus_lo), str(full_beta_minus_hi)],
            "beta_plus": [str(beta_plus_lo), str(full_beta_plus_hi)],
            "joint_constraint": "2 sqrt(2)[(sqrt(2)-1)(beta_- - beta_-^partial)+(sqrt(2)+1)(beta_+ - beta_+^partial)]<=261",
        },
        "aligned_tensor_zero_condition": {
            "equation": "2t C_S - w B_infinity = 0",
            "sector_equations": "2t/w=beta_-^infinity and 2t/w=beta_+^infinity",
            "minus_t_over_w_interval": [str(root_minus[0]), str(root_minus[1])],
            "plus_t_over_w_interval": [str(root_plus[0]), str(root_plus[1])],
            "common_root_necessary_interval": [str(common_root[0]), str(common_root[1])],
            "common_root_resolved": False,
            "reason": "The certified joint tail budget still permits the plus sector to catch the minus sector; angle dependence and a microscopic target contour are absent.",
        },
        "improvement_over_legacy_scalar_envelope": {
            "legacy_q_interval": [str(old_lower), str(old_upper)],
            "legacy_m1_coordinate_C2": str(old_c2),
            "new_m6_coordinate_C2_directed": str(directed_c2),
            "raw_tail_reduction_factor": str(FLOOR.divide(old_c2, directed_c2)),
            "legacy_upper_over_new_minus_sector_q_upper": str(FLOOR.divide(old_upper, root_minus[1])),
            "legacy_upper_over_new_plus_sector_q_upper": str(FLOOR.divide(old_upper, root_plus[1])),
            "legacy_upper_over_new_common_root_upper": str(FLOOR.divide(old_upper, common_root[1])),
            "dominant_remaining_looseness": "analytic shell-count/crossing tail for 6<d/a_B, not the complete d<=6a_B partial tensor",
        },
        "scientific_decision": {
            "single_scalar_q_infinity_authorized": False,
            "scalar_root_promotion_authorized": False,
            "common_aligned_tensor_root_certified": False,
            "material_bound_improvement_certified": True,
            "parent_CM_047_NP_status": "Blocked",
            "true_parent_blocker": "No certified angle-dependent microscopic K(theta,w), target contour, or slope/transversality evaluator exists; the two sector tails also do not yet resolve a common aligned zero.",
            "main_tex_modified": False,
        },
    }
    return record


def write_markdown(record: dict) -> None:
    p = record["partial_generalized_coefficients_B_relative_to_C_S"]
    t = record["tail_theorem"]
    f = record["full_kernel_sector_enclosure"]
    z = record["aligned_tensor_zero_condition"]
    improvement = record["improvement_over_legacy_scalar_envelope"]
    text = rf"""# CM-047-NP tensor bound (LOCAL centered/aligned scope)

**Status:** `Done_MATERIAL_BOUND_IMPROVEMENT`.  This closes the released bound-improvement subtask; it does not close the parent magic-angle/root task.

## Complete finite part

The exact based geometric ball contains **{record['inputs']['dangerous_nonidentity_elements']:,}** nonidentity elements and **{record['inputs']['inversion_C8_orbits']:,}** inversion/C8 orbits.  Every orbit second moment was constructed with integer arithmetic and passed
\(U^T M U=M\).  MPFR directed rounding at {record['inputs']['mpfr_partial_precision_bits']} bits then gave the complete tensor \(B_{{\leq6a_B}}\), including all off-diagonal entries.

On the exact two-dimensional C8-invariant cone, write \(x=B_{{23}}\), \(y=B_{{33}}\).  The generalized coefficients relative to the physical first-shell tensor \(C_S\) are
\[
\beta_- = y+\sqrt2x\in[{p['minus_interval'][0]},{p['minus_interval'][1]}],\qquad
\beta_+ = y-\sqrt2x\in[{p['plus_interval'][0]},{p['plus_interval'][1]}].
\]
Each has multiplicity two.  Their inequality is the explicit obstruction to replacing the kernel by one scalar \(q_\infty\).

## Certified omitted tail

The geometric shell/counting theorem was re-evaluated with MPFR directed rounding.  For the omitted \(d>6a_B\) terms,
\[
T_{{>6a_B}}\succeq0,\qquad \operatorname{{Tr}}T_{{>6a_B}}\leq261.
\]
C8 invariance and the exact commutant theorem force
\[
T_{{>6a_B}}=G(\tau_-P_-+\tau_+P_+),\qquad
\tau_\pm\geq0,\qquad 2\sqrt2(\tau_-+\tau_+)\leq261.
\]
Consequently the full generalized coefficients obey
\[
\beta_-^\infty\in[{f['beta_minus'][0]},{f['beta_minus'][1]}],\qquad
\beta_+^\infty\in[{f['beta_plus'][0]},{f['beta_plus'][1]}],
\]
together with the stronger joint budget recorded in the JSON certificate.

## Root consequence and honest stopping point

For \(2tC_S-wB_\infty=0\), a common tensor zero requires both sector equations \(2t/w=\beta_-^\infty=\beta_+^\infty\).  If such a centered/aligned common zero exists, its necessary interval is
\[
t/w\in[{z['common_root_necessary_interval'][0]},{z['common_root_necessary_interval'][1]}].
\]
The tail budget still permits equality, so existence is unresolved.  No scalar root, angle slope, or physical magic angle is promoted.

## Quantified improvement

The historical scalar envelope was `{improvement['legacy_q_interval'][0]}--{improvement['legacy_q_interval'][1]}` and depended on an incomplete word-ball lower sum plus an m=1 shell upper bound.  The complete geometric ball moves the only remaining looseness to \(d>6a_B\): the raw C2 tail contracts by a factor **{fmt(Decimal(improvement['raw_tail_reduction_factor']))}**.  Relative to the historical upper endpoint, the new minus-sector, plus-sector, and common-root upper endpoints improve by factors **{fmt(Decimal(improvement['legacy_upper_over_new_minus_sector_q_upper']))}**, **{fmt(Decimal(improvement['legacy_upper_over_new_plus_sector_q_upper']))}**, and **{fmt(Decimal(improvement['legacy_upper_over_new_common_root_upper']))}**, respectively.

The parent `CM-047-NP` remains genuinely Blocked because no certified angle-dependent microscopic \(K(\theta,w)\), target contour, or transversality evaluator exists, and the present tail is not sharp enough to decide equality of the two aligned sectors.  `main.tex` remains locked.
"""
    MD_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    record = build_record()
    JSON_PATH.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    write_markdown(record)
    print(json.dumps({
        "json": str(JSON_PATH),
        "markdown": str(MD_PATH),
        "partial_beta_minus": record["partial_generalized_coefficients_B_relative_to_C_S"]["minus_interval"],
        "partial_beta_plus": record["partial_generalized_coefficients_B_relative_to_C_S"]["plus_interval"],
        "common_root_interval": record["aligned_tensor_zero_condition"]["common_root_necessary_interval"],
    }, indent=2))


if __name__ == "__main__":
    main()
