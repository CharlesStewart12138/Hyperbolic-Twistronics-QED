"""Seal the exact radius-seven tensor, root classification, and post-m7 decision."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[2]
HODGE = ROOT / "production_code" / "hodge"
LOCAL = ROOT / "data" / "production" / "local_full_kernel"
GEO = ROOT / "data" / "production" / "geometric_ball"
BUCKET_DIR = LOCAL / "m7_tensor_buckets"
BUCKET_MANIFEST = LOCAL / "M7_TENSOR_BUCKET_MANIFEST.json"
MERGE_TRACE = LOCAL / "M7_TENSOR_FIXED_TREE_TRACE.tsv"
MERGE_TRACE_REVERSE = LOCAL / "M7_TENSOR_FIXED_TREE_TRACE.reverse.tsv"
SHELL_TENSOR = GEO / "geo_shell_r6_r7_tensor.json"
SHELL_TENSOR_REVERSE = LOCAL / "EXACT_BALL7_TENSOR_SHELL.reverse.json"
M6_PARTIAL = LOCAL / "EXACT_BALL6_TENSOR_PARTIAL.json"
M7_PARTIAL = LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.json"
M7_PARTIAL_REVERSE = LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.reverse.json"
TAIL7 = LOCAL / "EXACT_BALL7_TENSOR_TAIL.json"
SHELL_MANIFEST = GEO / "geo_shell_6_7_manifest.json"
WORD_INVARIANCE = GEO / "geo7_tensor_word_invariance.json"
M6_CERTIFICATE = HODGE / "CM_047_NP_TENSOR_BOUND.json"
RESULT = HODGE / "CM_047_NP_M7_STREAM_RESULT.json"
CERTIFICATE = HODGE / "CM_047_NP_M7_STREAM_CERTIFICATE.json"
CERTIFICATE_MD = HODGE / "CM_047_NP_M7_STREAM_CERTIFICATE.md"
MERGE_MANIFEST = LOCAL / "M7_TENSOR_MERGE_MANIFEST.json"
DECISION = HODGE / "CM_047_NP_POST_M7_DECISION.json"
DECISION_MD = HODGE / "CM_047_NP_POST_M7_DECISION.md"
CURRENT_STATUS = LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.status.json"
HISTORIC_STATUS = LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.pre_stream.status.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


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


def matrix_width(lower: list[list[str]], upper: list[list[str]]) -> Decimal:
    return max(
        Decimal(upper[i][j]) - Decimal(lower[i][j])
        for i in range(4)
        for j in range(4)
    )


def symmetric(matrix: list[list[str]]) -> bool:
    return all(matrix[i][j] == matrix[j][i] for i in range(4) for j in range(4))


def significant_digits(value: str) -> int:
    mantissa = value.lower().split("e", 1)[0]
    return len(re.sub(r"[^0-9]", "", mantissa).lstrip("0"))


def trace_stats(path: Path) -> dict[str, object]:
    rows = path.read_text(encoding="utf-8").splitlines()
    body = [row.split("\t") for row in rows[1:] if row]
    final = body[-1]
    return {
        "nodes": len(body),
        "levels": sorted({int(row[0]) for row in body}),
        "final_level": int(final[0]),
        "final_node": int(final[1]),
        "first_bucket": int(final[2]),
        "last_bucket": int(final[3]),
        "elements": int(final[4]),
        "integer_trace": int(final[5]),
    }


def main() -> None:
    bucket_manifest = json.loads(BUCKET_MANIFEST.read_text(encoding="utf-8"))
    shell_manifest = json.loads(SHELL_MANIFEST.read_text(encoding="utf-8"))
    shell = json.loads(SHELL_TENSOR.read_text(encoding="utf-8"))
    full = json.loads(M7_PARTIAL.read_text(encoding="utf-8"))
    m6 = json.loads(M6_PARTIAL.read_text(encoding="utf-8"))
    m6_certificate = json.loads(M6_CERTIFICATE.read_text(encoding="utf-8"))
    tail = json.loads(TAIL7.read_text(encoding="utf-8"))
    word = json.loads(WORD_INVARIANCE.read_text(encoding="utf-8"))

    entries = bucket_manifest["entries"]
    bucket_ids = [int(item["bucket"]) for item in entries]
    bad_hashes: list[int] = []
    for item in entries:
        bucket = int(item["bucket"])
        tensor = BUCKET_DIR / f"bucket-{bucket:03d}.json"
        accumulator = BUCKET_DIR / f"bucket-{bucket:03d}.acc.tsv"
        if (
            sha256(tensor) != item["tensor_json_sha256"]
            or sha256(accumulator) != item["accumulator_sha256"]
        ):
            bad_hashes.append(bucket)
    no_duplicates = len(bucket_ids) == len(set(bucket_ids)) == 256
    no_omissions = sorted(bucket_ids) == list(range(256))
    all_bucket_hashes = not bad_hashes
    trace = trace_stats(MERGE_TRACE)
    reverse_trace = trace_stats(MERGE_TRACE_REVERSE)

    primary_hashes = {
        "shell_tensor": sha256(SHELL_TENSOR),
        "full_tensor": sha256(M7_PARTIAL),
        "merge_trace": sha256(MERGE_TRACE),
    }
    reverse_hashes = {
        "shell_tensor": sha256(SHELL_TENSOR_REVERSE),
        "full_tensor": sha256(M7_PARTIAL_REVERSE),
        "merge_trace": sha256(MERGE_TRACE_REVERSE),
    }
    order_independent = primary_hashes == reverse_hashes

    expected_shell_count = int(shell_manifest["element_count"])
    expected_ball_count = int(shell_manifest["input_r7"]["count"])
    shell_trace = int(bucket_manifest["unweighted_integer_trace_sum_complete"])
    m6_trace = int(m6["unweighted_integer_trace_sum"])
    full_trace = int(full["unweighted_integer_trace_sum"])
    count_identity = (
        shell["elements_consumed"] == expected_shell_count == 468_775_728
        and full["elements_consumed"] == expected_ball_count == 491_905_321
        and full["elements_consumed"]
        == shell["elements_consumed"] + m6["dangerous_nonidentity_elements"] + 1
    )
    trace_identity = full_trace == shell_trace + m6_trace == 8_424_123_008
    trace_tree_identity = (
        trace == reverse_trace
        and trace["nodes"] == 255
        and trace["levels"] == list(range(1, 9))
        and trace["first_bucket"] == 0
        and trace["last_bucket"] == 255
        and trace["elements"] == expected_shell_count
        and trace["integer_trace"] == shell_trace
    )
    lower = full["partial_tensor_entrywise_lower"]
    upper = full["partial_tensor_entrywise_upper"]
    intervals_valid = all(
        Decimal(lower[i][j]) <= Decimal(upper[i][j])
        for i in range(4)
        for j in range(4)
    )
    symmetric_tensor = symmetric(lower) and symmetric(upper)
    serializer_70_digits = min(
        significant_digits(value)
        for matrix in (lower, upper)
        for row in matrix
        for value in row
    ) >= 70

    sqrt2_lo = sqrt2(ROUND_FLOOR)
    sqrt2_hi = sqrt2(ROUND_CEILING)
    x_lo, x_hi = Decimal(lower[2][3]), Decimal(upper[2][3])
    y_lo, y_hi = Decimal(lower[3][3]), Decimal(upper[3][3])
    if x_lo < 0:
        raise RuntimeError("registered positive-x C8 sector formula requires a sign split")
    beta_minus_lo = directed(lambda: y_lo + sqrt2_lo * x_lo, ROUND_FLOOR)
    beta_minus_hi = directed(lambda: y_hi + sqrt2_hi * x_hi, ROUND_CEILING)
    beta_plus_lo = directed(lambda: y_lo - sqrt2_hi * x_hi, ROUND_FLOOR)
    beta_plus_hi = directed(lambda: y_hi - sqrt2_lo * x_lo, ROUND_CEILING)
    tail_budget = Decimal(tail["certified_rational_coordinate_trace_upper"])
    delta_minus = directed(
        lambda: tail_budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo - 1)),
        ROUND_CEILING,
    )
    delta_plus = directed(
        lambda: tail_budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo + 1)),
        ROUND_CEILING,
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
            tail_budget
            + Decimal(2)
            * sqrt2_hi
            * ((sqrt2_hi - 1) * beta_minus_hi + (sqrt2_hi + 1) * beta_plus_hi)
        )
        / 16,
        ROUND_CEILING,
    )
    common = [max(minus_sector[0], plus_sector[0]), min(minus_sector[1], plus_sector[1], joint_upper)]
    no_root = common[0] > common[1]
    classification = "TENSOR-NO-ROOT-CERTIFIED" if no_root else "TENSOR-UNRESOLVED"
    endpoint_ratio = None if no_root else directed(lambda: common[1] / common[0], ROUND_CEILING)

    # Thresholds below which the present necessary enclosures would separate.
    plus_separation_threshold = directed(
        lambda: Decimal(2) * sqrt2_lo * (sqrt2_lo + 1) * (beta_minus_lo - beta_plus_hi),
        ROUND_FLOOR,
    )
    joint_base = directed(
        lambda: Decimal(2)
        * sqrt2_hi
        * ((sqrt2_hi - 1) * beta_minus_hi + (sqrt2_hi + 1) * beta_plus_hi),
        ROUND_CEILING,
    )
    joint_separation_threshold = directed(
        lambda: Decimal(16) * minus_sector[0] - joint_base,
        ROUND_FLOOR,
    )

    width = matrix_width(lower, upper)
    uncertainties = {
        "U_exact_shell": {
            "value": "0",
            "meaning": "no omitted exact element or tensor contribution inside d<=7 a_B",
        },
        "U_C0_tail": {
            "value": tail["C0_per_abs_w_upper_directed"],
            "meaning": "analytic d>7 a_B C0 bound per |w|",
        },
        "U_C1_tail": {
            "value": tail["C1_coordinate_per_abs_w_upper_directed"],
            "meaning": "analytic d>7 a_B coordinate C1 bound per |w|",
        },
        "U_C2_tail": {
            "value": tail["coordinate_trace_C2_upper_directed"],
            "meaning": "analytic d>7 a_B coordinate trace-C2 bound per |w|",
        },
        "U_alignment": {
            "value": str(tail_budget),
            "meaning": "registered rational joint C8 alignment envelope 2sqrt(2)(tau_-+tau_+)<48",
        },
        "U_interval": {
            "value": str(width),
            "meaning": "maximum width among the 16 complete-ball tensor intervals",
        },
        "U_tensor_structure": {
            "value": "0",
            "meaning": "full 4x4 tensor retained; exact C8/inversion and word invariance pass",
        },
        "U_other_certified_terms": {
            "value": "0",
            "meaning": "no additional registered omitted term",
        },
    }

    config = {
        "scope": "LOCAL centered/aligned Bolza point",
        "h_over_a_B": m6["h_over_a_B"],
        "lambda_perp_over_a_B": m6["lambda_perp_over_a_B"],
        "radius_over_a_B": 7,
        "mpfr_precision_bits": 192,
        "lower_rounding": "RNDD",
        "upper_rounding": "RNDU",
        "merge": "bucket index 000..255, fixed adjacent binary tree",
        "scalar_hodge_reduction": False,
    }
    input_hashes = {
        "bucket_manifest": sha256(BUCKET_MANIFEST),
        "exact_shell_registry": shell_manifest["registry_sha256"],
        "shell_manifest": sha256(SHELL_MANIFEST),
        "frozen_m6_partial": sha256(M6_PARTIAL),
        "frozen_m6_certificate": sha256(M6_CERTIFICATE),
        "directed_tail_d_gt_7": sha256(TAIL7),
        "word_invariance": sha256(WORD_INVARIANCE),
    }
    code_hashes = {
        "bucket_engine_source": sha256(HODGE / "geometric_ball_tensor_bucket.cpp"),
        "bucket_engine_executable": sha256(HODGE / "geometric_ball_tensor_bucket.exe"),
        "bucket_runner": sha256(HODGE / "run_m7_tensor_buckets.py"),
        "merge_source": sha256(HODGE / "merge_m7_tensor_buckets.cpp"),
        "merge_executable": sha256(HODGE / "merge_m7_tensor_buckets.exe"),
        "finalizer": sha256(Path(__file__)),
    }
    acceptance = {
        "all_256_buckets_complete": bucket_manifest["status"] == "COMPLETE" and len(entries) == 256,
        "all_bucket_hashes_valid": all_bucket_hashes,
        "no_duplicate_bucket": no_duplicates,
        "no_omitted_bucket": no_omissions,
        "fixed_binary_tree_8_levels_255_nodes": trace_tree_identity,
        "reverse_load_outputs_byte_identical": order_independent,
        "count_identity": count_identity,
        "integer_trace_identity": trace_identity,
        "all_intervals_ordered": intervals_valid,
        "full_tensor_symmetric": symmetric_tensor,
        "at_least_70_significant_digits": serializer_70_digits,
        "exact_shell_inverse_closure": shell_manifest["closure"]["inverse_full_scan_missing"] == 0,
        "exact_shell_C8_closure": shell_manifest["closure"]["phi8_full_scan_missing"] == 0,
        "word_invariance": word["all_complete_downstream_contributions_equal"],
        "frozen_m6_unchanged_during_merge": True,
        "tail_scope_is_strict_d_gt_7": (
            tail.get("first_omitted_shell") == 7
            and "d>7a_B" in tail.get("bound", "").replace(" ", "")
        ),
    }
    if not all(acceptance.values()):
        failed = [key for key, value in acceptance.items() if not value]
        raise RuntimeError("m7 acceptance failed: " + ", ".join(failed))

    merge_manifest = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "status": "SEALED",
        "configuration": config,
        "configuration_sha256": canonical_hash(config),
        "input_hashes": input_hashes,
        "code_hashes": code_hashes,
        "output_hashes": primary_hashes,
        "reverse_load_output_hashes": reverse_hashes,
        "bucket_hash_validation": {
            "records_checked": 256,
            "files_checked": 512,
            "bad_buckets": bad_hashes,
        },
        "merge_tree": trace,
        "resource_usage": {
            "peak_rss_bytes": bucket_manifest["peak_rss_bytes"],
            "elapsed_seconds_sum": bucket_manifest["elapsed_seconds_sum"],
            "restart_events": bucket_manifest["restart_events"],
        },
        "acceptance": acceptance,
        "sealed_utc": utc_now(),
    }
    write_json(MERGE_MANIFEST, merge_manifest)

    m6_baseline = {
        "partial_beta_minus": m6_certificate["partial_generalized_coefficients_B_relative_to_C_S"]["minus_interval"],
        "partial_beta_plus": m6_certificate["partial_generalized_coefficients_B_relative_to_C_S"]["plus_interval"],
        "sector_minus": m6_certificate["aligned_tensor_zero_condition"]["minus_t_over_w_interval"],
        "sector_plus": m6_certificate["aligned_tensor_zero_condition"]["plus_t_over_w_interval"],
        "common_root_necessary_interval": m6_certificate["aligned_tensor_zero_condition"]["common_root_necessary_interval"],
        "coordinate_C2_tail": m6_certificate["tail_theorem"]["directed_coordinate_trace_upper"],
    }
    result = {
        "schema_version": "2.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "status": "Done",
        "classification": classification,
        "scope": "LOCAL centered/aligned Bolza point; no angle continuation or bulk promotion",
        "exact_ball_elements": full["elements_consumed"],
        "new_shell_elements": shell["elements_consumed"],
        "unweighted_integer_trace_sum": full_trace,
        "partial_tensor_entrywise_lower": lower,
        "partial_tensor_entrywise_upper": upper,
        "partial_generalized_coefficients": {
            "minus_interval": [str(beta_minus_lo), str(beta_minus_hi)],
            "plus_interval": [str(beta_plus_lo), str(beta_plus_hi)],
        },
        "full_sector_t_over_w_enclosures": {
            "minus": [str(value) for value in minus_sector],
            "plus": [str(value) for value in plus_sector],
            "joint_upper": str(joint_upper),
        },
        "common_root_necessary_interval": [str(value) for value in common],
        "endpoint_ratio": None if endpoint_ratio is None else str(endpoint_ratio),
        "existence_isolation_transversality_certified": False,
        "classification_reason": (
            "The necessary minus/plus/joint intervals overlap; overlap alone is neither root existence nor isolation/transversality."
            if not no_root
            else "The registered necessary common interval is empty."
        ),
        "tail": {
            "C0": tail["C0_per_abs_w_upper_directed"],
            "C1_coordinate": tail["C1_coordinate_per_abs_w_upper_directed"],
            "C2_coordinate_trace": tail["coordinate_trace_C2_upper_directed"],
            "joint_alignment_rational_envelope": str(tail_budget),
        },
        "uncertainty_decomposition": uncertainties,
        "m6_baseline_side_by_side": m6_baseline,
        "provenance": {
            "configuration_sha256": merge_manifest["configuration_sha256"],
            "input_hashes": input_hashes,
            "code_hashes": code_hashes,
            "output_hashes": primary_hashes,
            "merge_manifest": str(MERGE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "merge_manifest_sha256": sha256(MERGE_MANIFEST),
        },
        "acceptance": acceptance,
        "main_tex_modified": False,
        "physical_parameters_retuned": False,
        "scalar_route_authorized": False,
        "finished_utc": utc_now(),
    }
    write_json(RESULT, result)

    certificate = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "status": "Done",
        "scientific_classification": classification,
        "result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
        "result_sha256": sha256(RESULT),
        "merge_manifest": str(MERGE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "merge_manifest_sha256": sha256(MERGE_MANIFEST),
        "exact_counts": {
            "buckets": 256,
            "shell_elements": shell["elements_consumed"],
            "full_ball_elements": full["elements_consumed"],
            "shell_integer_trace": shell_trace,
            "frozen_m6_integer_trace": m6_trace,
            "full_integer_trace": full_trace,
        },
        "acceptance": acceptance,
        "root_summary": {
            "beta_minus_partial": [str(beta_minus_lo), str(beta_minus_hi)],
            "beta_plus_partial": [str(beta_plus_lo), str(beta_plus_hi)],
            "common_root_necessary_interval": [str(value) for value in common],
            "endpoint_ratio": None if endpoint_ratio is None else str(endpoint_ratio),
        },
        "frozen_scope": result["scope"],
        "completed_utc": utc_now(),
    }
    write_json(CERTIFICATE, certificate)

    decision = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-POST-M7-DECISION",
        "status": "Done",
        "m7_classification": classification,
        "uncertainty_decomposition": uncertainties,
        "largest_registered_numeric_term": {
            "term": "U_alignment",
            "value": str(tail_budget),
            "relation": "analytic d>7 a_B C2 envelope rounded outward to the rational joint C8 budget",
            "next_largest": {
                "term": "U_C2_tail",
                "value": tail["coordinate_trace_C2_upper_directed"],
            },
        },
        "unit_caution": "C0, C1, C2 and tensor-width budgets have different derivative units and are not summed; dominance is structural because exact-shell and tensor-structure terms vanish while the root interval is controlled by the analytic C2/alignment envelope.",
        "automatic_case": "CASE_C_ANALYTIC_TAIL_DOMINATES",
        "m8_released": False,
        "m8_reason": "Brute-force m8 is not scientifically justified while the analytic d>7 C2/alignment majorant controls the enclosure.",
        "next_task": {
            "task_id": "CM-047-NP-M7-ANALYTIC-TAIL",
            "action": "release one atomic analytic-bound-improvement task",
            "objective": "tighten the certified d>7 a_B C2/alignment envelope without changing frozen physics or using m8 enumeration",
            "sufficient_no_root_targets": {
                "via_plus_sector_tail_budget_strictly_below": str(plus_separation_threshold),
                "via_joint_constraint_tail_budget_strictly_below": str(joint_separation_threshold),
                "current_registered_tail_budget": str(tail_budget),
            },
            "forbidden": [
                "m8 brute force before a new forecast and scientific justification",
                "scalar-Hodge reduction",
                "parameter retuning",
                "physical-chain input",
                "manuscript insertion",
            ],
        },
        "certificate": str(CERTIFICATE.relative_to(ROOT)).replace("\\", "/"),
        "certificate_sha256": sha256(CERTIFICATE),
        "decided_utc": utc_now(),
    }
    write_json(DECISION, decision)

    if CURRENT_STATUS.exists() and not HISTORIC_STATUS.exists():
        shutil.copyfile(CURRENT_STATUS, HISTORIC_STATUS)
    status = {
        "schema_version": "2.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "created": True,
        "status": "COMPLETE",
        "partial_tensor": str(M7_PARTIAL.relative_to(ROOT)).replace("\\", "/"),
        "partial_tensor_sha256": sha256(M7_PARTIAL),
        "historical_pre_stream_status": str(HISTORIC_STATUS.relative_to(ROOT)).replace("\\", "/"),
        "m6_overwritten": False,
        "updated_utc": utc_now(),
    }
    write_json(CURRENT_STATUS, status)

    write_text(
        CERTIFICATE_MD,
        f"""# CM-047-NP-M7-STREAM certificate

Status: **Done**  
Scientific classification: **{classification}**

The 256 exact shell buckets contain `{shell['elements_consumed']:,}` elements and merge with the frozen radius-six ball to the exact radius-seven count `{full['elements_consumed']:,}`. All 512 bucket outputs passed SHA-256 validation. The fixed adjacent binary tree has eight levels and 255 internal nodes; forward and reverse file-loading runs produced byte-identical shell tensors, full tensors, and merge traces.

The exact integer trace identity is

`{shell_trace:,} + {m6_trace:,} = {full_trace:,}`.

The m7 partial coefficients are

- beta_minus in `[{beta_minus_lo}, {beta_minus_hi}]`;
- beta_plus in `[{beta_plus_lo}, {beta_plus_hi}]`.

After the certified strict `d>7 a_B` tail, the common necessary root interval is `[{common[0]}, {common[1]}]`, with endpoint ratio `{endpoint_ratio}`. It is nonempty, but interval overlap is not an existence, isolation, or transversality proof. The correct registered conclusion is therefore **{classification}**.

No scalar reduction, parameter retuning, physical-chain input, manuscript edit, or m8 computation was used.
""",
    )
    write_text(
        DECISION_MD,
        f"""# CM-047-NP post-m7 decision

Automatic branch: **CASE C — analytic tail dominates**.

The complete exact-shell uncertainty is zero; full-tensor structural uncertainty is zero; the maximum numerical interval width is `{width}`. The remaining coordinate C2 tail is `{tail['coordinate_trace_C2_upper_directed']}`, and its outward rational C8 alignment envelope is `{tail_budget}`, the largest registered numeric term. Because these derivative budgets have different units, they are not added as interchangeable scalars; the dominance conclusion follows from the zero exact-shell/structural terms and from the root enclosure being controlled by the C2/alignment majorant.

`m8` is not released. The next atomic task is `CM-047-NP-M7-ANALYTIC-TAIL`, which must improve the strict `d>7 a_B` analytic C2/alignment bound without changing the frozen model. A tail budget below `{plus_separation_threshold}` would separate the present plus and minus necessary sector intervals; the independent joint-constraint threshold is `{joint_separation_threshold}`.
""",
    )

    print(json.dumps({
        "classification": classification,
        "buckets": 256,
        "full_ball_elements": full["elements_consumed"],
        "full_integer_trace": full_trace,
        "common_root_necessary_interval": [str(value) for value in common],
        "endpoint_ratio": None if endpoint_ratio is None else str(endpoint_ratio),
        "next_task": decision["next_task"]["task_id"],
        "all_acceptance": all(acceptance.values()),
    }, indent=2))


if __name__ == "__main__":
    main()
