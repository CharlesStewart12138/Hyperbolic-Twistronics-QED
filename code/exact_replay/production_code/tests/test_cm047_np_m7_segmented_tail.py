from __future__ import annotations

from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / "data" / "production" / "local_full_kernel"
HODGE = ROOT / "production_code" / "hodge"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_segmented_tail_scan_is_complete_and_exact() -> None:
    scan = load(LOCAL / "M7_ABELIAN_MAX_SCAN_MANIFEST.json")
    assert scan["status"] == "SEALED"
    assert scan["checkpoint_counts"] == {"r6": 256, "shell_6_7": 256, "total": 512}
    assert scan["elements"] == {"r6": 23_129_593, "shell_6_7": 468_775_728, "full_B7": 491_905_321}
    assert scan["maxima"]["r6_norm_squared"] == 108
    assert scan["maxima"]["shell_norm_squared"] == scan["maxima"]["full_B7_norm_squared"] == 147
    assert all(scan["acceptance"].values())


def test_bolza_circumradius_supports_five_a_segmentation() -> None:
    root2 = math.sqrt(2.0)
    a_over_r = 2.0 * math.acosh(1.0 + root2)
    rho_over_r = math.acosh((1.0 + root2) ** 2)
    assert rho_over_r < a_over_r
    assert 5.0 + 2.0 * rho_over_r / a_over_r < 7.0
    # Exact monotonic-cosh reduction: cosh(a)-cosh(rho)=(1+sqrt(2))^2-1>0.
    assert (1.0 + root2) ** 2 - 1.0 > 0.0


def test_shell_coordinate_ceiling_is_the_registered_consequence() -> None:
    tail = load(LOCAL / "EXACT_BALL7_TENSOR_TAIL_SEGMENTED.json")
    assert tail["complete_ball_maximum_abelian_norm_squared"] == 147
    assert tail["segmentation_length_over_a_B"] == 5
    assert tail["increment_displacement_bound"] == "5a_B+2rho<7a_B"
    assert tail["shell_coordinate_bound"] == "||n(g)||_2^2<=147*ceil((n+1)/5)^2 for n a_B<=d(g o,o)<(n+1)a_B"
    assert [math.ceil((j + 8) / 5) for j in range(8)] == [2, 2, 2, 3, 3, 3, 3, 3]


def test_closed_ceil_series_matches_independent_long_sum() -> None:
    tail = load(LOCAL / "EXACT_BALL7_TENSOR_TAIL_SEGMENTED.json")
    with localcontext() as context:
        context.prec = 100
        q = Decimal(tail["shell_ratio_upper"])
        direct1 = sum(Decimal(math.ceil((j + 8) / 5)) * q**j for j in range(1000))
        direct2 = sum(Decimal(math.ceil((j + 8) / 5) ** 2) * q**j for j in range(1000))
        assert abs(Decimal(tail["ceil_series_C1_upper"]) - direct1) < Decimal("1e-70")
        assert abs(Decimal(tail["ceil_series_C2_upper"]) - direct2) < Decimal("1e-70")


def test_segmented_directed_tail_strictly_improves_old_tail() -> None:
    old = load(LOCAL / "EXACT_BALL7_TENSOR_TAIL.json")
    new = load(LOCAL / "EXACT_BALL7_TENSOR_TAIL_SEGMENTED.json")
    assert new["mpfr_precision_bits"] == 256
    assert "RNDU" in new["rounding_contract"]
    assert Decimal(new["coordinate_trace_C2_upper_directed"]) < 1
    assert Decimal(old["coordinate_trace_C2_upper_directed"]) / Decimal(new["coordinate_trace_C2_upper_directed"]) > 144
    assert new["certified_rational_coordinate_trace_upper"] == 1


def test_full_tensor_no_root_intervals_are_strictly_disjoint() -> None:
    result = load(HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.json")
    assert result["classification"] == "TENSOR-NO-ROOT-CERTIFIED"
    minus = list(map(Decimal, result["necessary_sector_t_over_w_intervals"]["minus"]))
    plus = list(map(Decimal, result["necessary_sector_t_over_w_intervals"]["plus"]))
    common = result["common_root_necessary_intersection"]
    assert Decimal(common["lower"]) > Decimal(common["upper"])
    assert Decimal(common["separation_margin_lower"]) > Decimal("0.104")
    assert plus[1] < minus[0]
    assert common["empty"] is True
    assert result["endpoint_ratio"] is None


def test_no_root_depends_on_certified_improvement_not_interval_overlap() -> None:
    old = load(HODGE / "CM_047_NP_M7_STREAM_RESULT.json")
    new = load(HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.json")
    assert old["classification"] == "TENSOR-UNRESOLVED"
    assert Decimal(old["common_root_necessary_interval"][0]) <= Decimal(old["common_root_necessary_interval"][1])
    assert new["strict_d_gt_7_tail"]["rational_trace_and_alignment_budget"] == 1
    assert new["common_root_necessary_intersection"]["empty"] is True


def test_scientific_scope_and_provenance_remain_separated() -> None:
    tail = load(HODGE / "CM_047_NP_M7_ANALYTIC_TAIL_CERTIFICATE.json")
    root = load(HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.json")
    decision = load(HODGE / "CM_047_NP_POST_TAIL_DECISION.json")
    assert tail["physical_parameters_retuned"] is False
    assert tail["main_tex_modified"] is False
    assert root["physical_parameters_retuned"] is False
    assert root["physical_chain_input_used"] is False
    assert root["scalar_hodge_used"] is False
    assert root["main_tex_modified"] is False
    assert decision["automatic_case"] == "CASE_A_NO_ROOT_CERTIFIED"
    assert decision["m8_released"] is False
    assert hashlib.sha256((HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.json").read_bytes()).hexdigest() == decision["no_root_certificate_sha256"]
