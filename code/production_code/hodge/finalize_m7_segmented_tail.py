"""Certify the geodesic-segmentation tail and centered/aligned no-root result."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HODGE = ROOT / "production_code" / "hodge"
LOCAL = ROOT / "data" / "production" / "local_full_kernel"
GEO = ROOT / "data" / "production" / "geometric_ball"
SCAN = LOCAL / "m7_analytic_tail_abelian_scan"
SCAN_MANIFEST = LOCAL / "M7_ABELIAN_MAX_SCAN_MANIFEST.json"
NEW_TAIL = LOCAL / "EXACT_BALL7_TENSOR_TAIL_SEGMENTED.json"
OLD_TAIL = LOCAL / "EXACT_BALL7_TENSOR_TAIL.json"
M7_PARTIAL = LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.json"
M7_RESULT = HODGE / "CM_047_NP_M7_STREAM_RESULT.json"
TAIL_CERT = HODGE / "CM_047_NP_M7_ANALYTIC_TAIL_CERTIFICATE.json"
TAIL_MD = HODGE / "CM_047_NP_M7_ANALYTIC_TAIL_CERTIFICATE.md"
NO_ROOT_CERT = HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.json"
NO_ROOT_MD = HODGE / "CM_047_NP_FULL_TENSOR_NO_ROOT_CERTIFICATE.md"
POST_DECISION = HODGE / "CM_047_NP_POST_TAIL_DECISION.json"
POST_DECISION_MD = HODGE / "CM_047_NP_POST_TAIL_DECISION.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_text(path: Path, value: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def directed(function, rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = 100
        context.rounding = rounding
        return +function()


def sqrt2(rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = 100
        context.rounding = rounding
        return Decimal(2).sqrt()


def main() -> None:
    r6_manifest = load(GEO / "geo_ball_r6_manifest.json")
    shell_manifest = load(GEO / "geo_shell_6_7_manifest.json")
    shell_buckets = load(GEO / "geo_shell_6_7_bucket_manifest.json")
    new_tail = load(NEW_TAIL)
    old_tail = load(OLD_TAIL)
    partial = load(M7_PARTIAL)
    m7_result = load(M7_RESULT)

    summaries: dict[str, list[dict]] = {}
    output_hashes: dict[str, dict[str, str]] = {}
    for family in ("r6", "shell_6_7"):
        rows = [load(SCAN / family / f"bucket-{index:03d}.json") for index in range(256)]
        if any(row["status"] != "COMPLETE" or row["bucket"] != index for index, row in enumerate(rows)):
            raise RuntimeError(f"invalid {family} scan checkpoint")
        summaries[family] = rows
        output_hashes[family] = {
            f"bucket-{index:03d}": digest(SCAN / family / f"bucket-{index:03d}.json")
            for index in range(256)
        }

    r6_count = sum(row["elements_consumed"] for row in summaries["r6"])
    shell_count = sum(row["elements_consumed"] for row in summaries["shell_6_7"])
    r6_max = max(row["maximum_norm_squared"] for row in summaries["r6"])
    shell_max = max(row["maximum_norm_squared"] for row in summaries["shell_6_7"])
    full_max = max(r6_max, shell_max)
    maximizing_rows = [
        row
        for rows in summaries.values()
        for row in rows
        if row["maximum_norm_squared"] == full_max
    ]
    scan_acceptance = {
        "r6_256_checkpoints": len(summaries["r6"]) == 256,
        "shell_256_checkpoints": len(summaries["shell_6_7"]) == 256,
        "r6_count_matches_exact_ball": r6_count == r6_manifest["target_unique_elements"] == 23_129_593,
        "shell_count_matches_exact_shell": shell_count == shell_manifest["element_count"] == 468_775_728,
        "full_count_identity": r6_count + shell_count == shell_manifest["input_r7"]["count"] == 491_905_321,
        "r6_maximum_norm_squared": r6_max == 108,
        "shell_and_full_maximum_norm_squared": shell_max == full_max == 147,
        "r6_exact_registry_complete": r6_manifest["complete"] is True and r6_manifest["frontier_exhausted"] is True,
        "shell_exact_and_closed": (
            shell_manifest["duplicate_exact_keys"] == 0
            and shell_manifest["closure"]["inverse_full_scan_missing"] == 0
            and shell_manifest["closure"]["phi8_full_scan_missing"] == 0
        ),
        "shell_source_buckets_complete": shell_buckets["buckets_complete"] == 256,
    }
    if not all(scan_acceptance.values()):
        raise RuntimeError("abelian maximum scan acceptance failed")

    scan_manifest = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-ANALYTIC-TAIL",
        "status": "SEALED",
        "scope": "complete exact B_geo(7a_B)=B_geo(6a_B) disjoint-union S_geo(6,7]",
        "checkpoint_counts": {"r6": 256, "shell_6_7": 256, "total": 512},
        "elements": {"r6": r6_count, "shell_6_7": shell_count, "full_B7": r6_count + shell_count},
        "maxima": {
            "r6_norm_squared": r6_max,
            "shell_norm_squared": shell_max,
            "full_B7_norm_squared": full_max,
            "maximizing_records": [
                {
                    "family": row["family"],
                    "bucket": row["bucket"],
                    "vector": row["maximizing_vector"],
                    "word_depth": row["maximizing_vector_word_depth"],
                }
                for row in maximizing_rows
            ],
        },
        "source_hashes": {
            "r6_registry": r6_manifest["registry_sha256"],
            "r6_manifest": digest(GEO / "geo_ball_r6_manifest.json"),
            "shell_registry": shell_manifest["registry_sha256"],
            "shell_manifest": digest(GEO / "geo_shell_6_7_manifest.json"),
            "shell_bucket_manifest": digest(GEO / "geo_shell_6_7_bucket_manifest.json"),
        },
        "code_hashes": {
            "scanner_source": digest(HODGE / "geometric_ball_abelian_max_scan.cpp"),
            "scanner_executable": digest(HODGE / "geometric_ball_abelian_max_scan.exe"),
        },
        "checkpoint_hash_tree_sha256": canonical_hash(output_hashes),
        "resources": {
            "r6_elapsed_seconds_sum": sum(row["elapsed_seconds"] for row in summaries["r6"]),
            "shell_elapsed_seconds_sum": sum(row["elapsed_seconds"] for row in summaries["shell_6_7"]),
            "peak_rss_bytes": max(row["peak_rss_bytes"] for rows in summaries.values() for row in rows),
        },
        "acceptance": scan_acceptance,
        "sealed_utc": now(),
    }
    write_json(SCAN_MANIFEST, scan_manifest)

    # Independent high-precision checks of the closed ceil-series formulas.
    with localcontext() as context:
        context.prec = 100
        q = Decimal(new_tail["shell_ratio_upper"])
        q5 = q**5
        block = sum(q**power for power in range(3, 8))
        series1 = Decimal(2) * (1 + q + q**2) + block * (
            q5 / (1 - q5) ** 2 + Decimal(3) / (1 - q5)
        )
        series2 = Decimal(4) * (1 + q + q**2) + block * (
            q5 * (1 + q5) / (1 - q5) ** 3
            + Decimal(6) * q5 / (1 - q5) ** 2
            + Decimal(9) / (1 - q5)
        )
    formula_acceptance = {
        "circumradius_below_a_B": new_tail["circumradius_strictly_below_a_B"] is True,
        "increment_bound_inside_exact_B7": new_tail["increment_displacement_bound"] == "5a_B+2rho<7a_B",
        "exact_B7_maximum_used": new_tail["complete_ball_maximum_abelian_norm_squared"] == full_max == 147,
        "C1_ceil_series_matches_serialized_q_within_1e_70": abs(Decimal(new_tail["ceil_series_C1_upper"]) - series1) < Decimal("1e-70"),
        "C2_ceil_series_matches_serialized_q_within_1e_70": abs(Decimal(new_tail["ceil_series_C2_upper"]) - series2) < Decimal("1e-70"),
        "strict_tail_scope": new_tail["first_omitted_shell"] == 7 and "d>7a_B" in new_tail["bound"].replace(" ", ""),
        "directed_C2_below_rational_one": Decimal(new_tail["coordinate_trace_C2_upper_directed"]) < 1,
        "rational_C2_envelope_one": new_tail["certified_rational_coordinate_trace_upper"] == 1,
    }
    if not all(formula_acceptance.values()):
        raise RuntimeError("segmented tail formula acceptance failed")

    old_c2 = Decimal(old_tail["coordinate_trace_C2_upper_directed"])
    new_c2 = Decimal(new_tail["coordinate_trace_C2_upper_directed"])
    improvement = directed(lambda: old_c2 / new_c2, ROUND_FLOOR)
    tail_certificate = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-ANALYTIC-TAIL",
        "status": "Done",
        "theorem": {
            "name": "Exact-ball geodesic-segmentation tail bound",
            "hypotheses": [
                "the Bolza Dirichlet octagon has circumradius rho<a_B",
                "B_geo(7a_B) is exact and exhaustive",
                "max_{h in B_geo(7a_B)} ||n(h)||_2^2=147",
                "the frozen radial weight is exp[-5(sqrt(1/4+d^2)-1/2)]",
                "the existing packing bound N_n<=C_Gamma exp(n a_B/R) holds",
            ],
            "segmentation": "partition [o,g o] into pieces of length <=5a_B and choose orbit centres within rho; each group increment has displacement <=5a_B+2rho<7a_B",
            "coordinate_conclusion": "||n(g)||_2^2<=147 ceil((n+1)/5)^2 on shell n",
            "tail_conclusion": "Tr(T_{d>7})/|w| is bounded by P_7*147*sum_{j>=0}ceil((j+8)/5)^2*q_7^j",
            "failure_mode": "the theorem would fail if the orbit covering radius were not below a_B or if the exact B7 maximum were incomplete",
        },
        "directed_bounds": {
            "C0_per_abs_w": new_tail["C0_per_abs_w_upper_directed"],
            "C1_coordinate_per_abs_w": new_tail["C1_coordinate_per_abs_w_upper_directed"],
            "C2_coordinate_trace_per_abs_w": new_tail["coordinate_trace_C2_upper_directed"],
            "certified_rational_C2_and_alignment_budget": 1,
        },
        "comparison": {
            "old_C2_upper": str(old_c2),
            "new_C2_upper": str(new_c2),
            "improvement_factor_lower": str(improvement),
        },
        "scan_manifest": str(SCAN_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "scan_manifest_sha256": digest(SCAN_MANIFEST),
        "tail_artifact": str(NEW_TAIL.relative_to(ROOT)).replace("\\", "/"),
        "tail_artifact_sha256": digest(NEW_TAIL),
        "code_hashes": {
            "evaluator_source": digest(HODGE / "full_kernel_tail_bound_segmented_m7.cpp"),
            "evaluator_executable": digest(HODGE / "full_kernel_tail_bound_segmented_m7.exe"),
            "finalizer": digest(Path(__file__)),
        },
        "acceptance": {**scan_acceptance, **formula_acceptance},
        "scope": "LOCAL centered Bolza character/full-tensor coordinates; no physical-angle or bulk promotion",
        "physical_parameters_retuned": False,
        "main_tex_modified": False,
        "completed_utc": now(),
    }
    write_json(TAIL_CERT, tail_certificate)

    lower = partial["partial_tensor_entrywise_lower"]
    upper = partial["partial_tensor_entrywise_upper"]
    sqrt2_lo = sqrt2(ROUND_FLOOR)
    sqrt2_hi = sqrt2(ROUND_CEILING)
    x_lo, x_hi = Decimal(lower[2][3]), Decimal(upper[2][3])
    y_lo, y_hi = Decimal(lower[3][3]), Decimal(upper[3][3])
    beta_minus_lo = directed(lambda: y_lo + sqrt2_lo * x_lo, ROUND_FLOOR)
    beta_minus_hi = directed(lambda: y_hi + sqrt2_hi * x_hi, ROUND_CEILING)
    beta_plus_lo = directed(lambda: y_lo - sqrt2_hi * x_hi, ROUND_FLOOR)
    beta_plus_hi = directed(lambda: y_hi - sqrt2_lo * x_lo, ROUND_CEILING)
    budget = Decimal(1)
    delta_minus = directed(
        lambda: budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo - 1)), ROUND_CEILING
    )
    delta_plus = directed(
        lambda: budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo + 1)), ROUND_CEILING
    )
    minus_sector = [
        directed(lambda: beta_minus_lo / 2, ROUND_FLOOR),
        directed(lambda: (beta_minus_hi + delta_minus) / 2, ROUND_CEILING),
    ]
    plus_sector = [
        directed(lambda: beta_plus_lo / 2, ROUND_FLOOR),
        directed(lambda: (beta_plus_hi + delta_plus) / 2, ROUND_CEILING),
    ]
    joint_upper = directed(
        lambda: (
            budget
            + Decimal(2)
            * sqrt2_hi
            * ((sqrt2_hi - 1) * beta_minus_hi + (sqrt2_hi + 1) * beta_plus_hi)
        )
        / 16,
        ROUND_CEILING,
    )
    intersection_lower = max(minus_sector[0], plus_sector[0])
    intersection_upper = min(minus_sector[1], plus_sector[1], joint_upper)
    if not intersection_lower > intersection_upper:
        raise RuntimeError("new rational tail envelope did not certify no root")

    no_root = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-FULL-TENSOR-NO-ROOT",
        "status": "Done",
        "classification": "TENSOR-NO-ROOT-CERTIFIED",
        "scope": "LOCAL centered/aligned Bolza point with frozen h/a_B=0.5 and lambda_perp/a_B=0.2",
        "equation": "2t C_S-w B_infinity=0 in the complete four-dimensional tensor sector decomposition",
        "partial_beta": {
            "minus": [str(beta_minus_lo), str(beta_minus_hi)],
            "plus": [str(beta_plus_lo), str(beta_plus_hi)],
        },
        "strict_d_gt_7_tail": {
            "directed_C2_upper": str(new_c2),
            "rational_trace_and_alignment_budget": 1,
        },
        "necessary_sector_t_over_w_intervals": {
            "minus": [str(value) for value in minus_sector],
            "plus": [str(value) for value in plus_sector],
            "joint_upper": str(joint_upper),
        },
        "common_root_necessary_intersection": {
            "lower": str(intersection_lower),
            "upper": str(intersection_upper),
            "empty": True,
            "separation_margin_lower": str(
                directed(lambda: intersection_lower - intersection_upper, ROUND_FLOOR)
            ),
        },
        "endpoint_ratio": None,
        "proof": "Every aligned tensor root must satisfy both sector equations and the joint PSD/C8 tail constraint. Their certified necessary intervals are disjoint, so no root exists in the stated scope.",
        "root_existence_claim": False,
        "transversality_needed_for_no_root": False,
        "tail_certificate": str(TAIL_CERT.relative_to(ROOT)).replace("\\", "/"),
        "tail_certificate_sha256": digest(TAIL_CERT),
        "m7_partial_sha256": digest(M7_PARTIAL),
        "physical_parameters_retuned": False,
        "physical_chain_input_used": False,
        "scalar_hodge_used": False,
        "main_tex_modified": False,
        "completed_utc": now(),
    }
    write_json(NO_ROOT_CERT, no_root)

    decision = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-POST-TAIL-DECISION",
        "status": "Done",
        "automatic_case": "CASE_A_NO_ROOT_CERTIFIED",
        "classification": "TENSOR-NO-ROOT-CERTIFIED",
        "m8_released": False,
        "m8_reason": "A rigorous no-root certificate already exists in the registered centered/aligned scope; further radial enumeration would be cosmetic for this decision.",
        "downstream": {
            "centered_aligned_full_tensor_branch": "closed by certified negative result",
            "CM-047-NP_parent": "remains separately blocked only for its broader angle-dependent target/transport/slope scope",
            "next_global_priority": "P0-2 global geometric systole certificate",
        },
        "no_root_certificate": str(NO_ROOT_CERT.relative_to(ROOT)).replace("\\", "/"),
        "no_root_certificate_sha256": digest(NO_ROOT_CERT),
        "decided_utc": now(),
    }
    write_json(POST_DECISION, decision)

    write_text(
        TAIL_MD,
        f"""# CM-047-NP-M7 analytic tail certificate

## Theorem

Let `F` be the centered Bolza Dirichlet octagon and `rho` its circumradius. The exact formulas give `rho<a_B`. Divide the geodesic from `o` to `g o` into segments of length at most `5a_B`; choose an orbit centre within `rho` of every division point. Consecutive centres differ by an element `h` with

`d(o,h o) <= 5a_B+2rho < 7a_B`.

The exhaustive exact ball scan proves `max_{{h in B_geo(7a_B)}} ||n(h)||_2^2=147`. Additivity of abelianization and the triangle inequality therefore give, on `n a_B<=d<(n+1)a_B`,

`||n(g)||_2^2 <= 147 ceil((n+1)/5)^2`.

Combining this with the existing rigorous orbit-count envelope and the convex physical-kernel secant yields

`Tr(T_{{d>7}})/|w| <= P_7 147 sum_{{j>=0}} ceil((j+8)/5)^2 q_7^j < {new_c2} < 1`.

All transcendental and series evaluations use 256-bit MPFR directed rounding. The C0 and coordinate-C1 bounds are `{new_tail['C0_per_abs_w_upper_directed']}` and `{new_tail['C1_coordinate_per_abs_w_upper_directed']}`. The old C2 bound `{old_c2}` is improved by a factor greater than `{improvement}`.

The statement depends on exact B7 completeness and `rho<a_B`; it does not extrapolate observed shell ratios, retune parameters, reduce the tensor to a scalar, or use physical-chain data.
""",
    )
    write_text(
        NO_ROOT_MD,
        f"""# Centered/aligned full-tensor no-root certificate

Classification: **TENSOR-NO-ROOT-CERTIFIED**.

With the new rational tail/alignment budget `1`, the necessary minus-sector interval is `[{minus_sector[0]}, {minus_sector[1]}]`; the plus-sector interval is `[{plus_sector[0]}, {plus_sector[1]}]`; and the joint upper bound is `{joint_upper}`. Their common necessary intersection is empty because `{intersection_lower}>{intersection_upper}`, with directed separation margin at least `{directed(lambda: intersection_lower - intersection_upper, ROUND_FLOOR)}`.

Thus `2t C_S-w B_infinity=0` has no solution in the stated LOCAL centered/aligned Bolza scope. This is a certified negative scientific result, not an execution failure. It does not claim absence on an unfrozen angle path, a finite quotient, or the bulk model.
""",
    )
    write_text(
        POST_DECISION_MD,
        """# Post-tail decision

The analytic-tail task closes with `TENSOR-NO-ROOT-CERTIFIED`. This is Case A. `m8` is not released because it cannot change the certified centered/aligned no-root conclusion. The broader `CM-047-NP` angle-dependent task remains separate; its missing target, angle transport and slope data are not supplied by this certificate. The next global priority is the global geometric systole certificate.
""",
    )

    print(json.dumps({
        "tail_status": "Done",
        "max_B7_abelian_norm_squared": full_max,
        "C2_upper": str(new_c2),
        "improvement_factor_lower": str(improvement),
        "classification": no_root["classification"],
        "minus_sector": no_root["necessary_sector_t_over_w_intervals"]["minus"],
        "plus_sector": no_root["necessary_sector_t_over_w_intervals"]["plus"],
        "joint_upper": no_root["necessary_sector_t_over_w_intervals"]["joint_upper"],
        "separation_margin_lower": no_root["common_root_necessary_intersection"]["separation_margin_lower"],
        "next_global_priority": decision["downstream"]["next_global_priority"],
    }, indent=2))


if __name__ == "__main__":
    main()
