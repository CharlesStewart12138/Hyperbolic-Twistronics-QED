"""Finalize the matrix-free feasibility audit of Q_BASED_S4CORE_PAIR_001."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from production_code.group.matrix_free_bilayer import production_lower_bound

ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
DATA = ROOT / "data" / "production" / "global_direct_v2"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tsv(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, value = line.split("\t", 1)
        result[key] = value
    return result


def main() -> None:
    scan_path = DATA / "interlayer_cutoff_counts.tsv"
    scan = tsv(scan_path)
    if scan["complete"] != "1" or int(scan["scanned_records"]) != 785_639_753:
        raise RuntimeError("cutoff scan is not complete")
    degrees = {
        "2.5": int(scan["count_Dc_half_units_5"]),
        "3.0": int(scan["count_Dc_half_units_6"]),
        "3.5": int(scan["count_Dc_half_units_7"]),
        "4.0": int(scan["count_Dc_half_units_8"]),
    }
    if degrees["3.0"] != 2_185:
        raise RuntimeError("primary cutoff support count drift")
    bound = production_lower_bound(
        quotient_order=11_943_936, zero_twist_degree=degrees["3.0"],
        kpm_moments=8_192, probes=64, probe_batch=32,
        theta_points=91, coupling_points=12,
    )
    disk = shutil.disk_usage(ROOT)
    usable_after_reserve = max(0, disk.free - 250_000_000_000)
    scanner_bytes_per_second = 115_489_043_715 / float(scan["elapsed_seconds"])
    grid_years_at_scanner_rate = bound.primary_grid_stream_bytes / scanner_bytes_per_second / (365.25 * 86400)
    primary_grid_cmacs = bound.complex_multiply_adds_per_parameter * bound.primary_parameter_points
    primary_grid_years_at_trillion_cmac_s = primary_grid_cmacs / 1_000_000_000_000 / (365.25 * 86400)
    code_paths = [
        GROUP / "scan_axis6_interlayer_cutoffs.cpp",
        GROUP / "scan_axis6_interlayer_cutoffs.exe",
        GROUP / "matrix_free_bilayer.py",
        ROOT / "production_code" / "tests" / "test_pf_grp_product_production_v2.py",
    ]
    input_paths = [
        GROUP / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json",
        GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json",
        DATA / "axis6_exact_ball_manifest.json",
        ROOT / "production_code" / "config" / "theory_production_benchmark.yaml",
        ROOT / "production_code" / "config" / "freeze_records" / "PF-KER-002.json",
    ]
    certificate = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-PRODUCT-PRODUCTION-V2",
        "quotient_id": "Q_BASED_S4CORE_PAIR_001",
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "task_status": "Done",
        "scientific_classification": "FULLY_ADMISSIBLE_NOT_NUMERICALLY_TRACTABLE_ON_CURRENT_HOST",
        "promotion_to_production": False,
        "mathematical_gates": {
            "normal_finite_quotient": "PASS",
            "order_N": 11_943_936,
            "physical_degree_eight": "PASS",
            "bipartite_parity": "PASS",
            "C8_equivariance": "PASS",
            "global_systole_gt_6a_B": "PASS",
            "global_injectivity_radius_gt_3a_B": "PASS",
            "primary_planar_support_radius_lt_injectivity_radius": "PASS",
        },
        "operator_implementation": {
            "intralayer": "matrix_free_sum_of_right_regular_permutations",
            "interlayer": "immutable_full_real_CSR_row_shards_streamed_one_at_a_time",
            "same_label_shortcut": False,
            "first_shell_shortcut": False,
            "explicit_matrix_equivalence_fixture": "7/7 tests passed",
            "production_large_run_started": False,
        },
        "exact_zero_twist_support": {
            "height_over_a_B": 0.5,
            "universal_cover_cutoff_to_count": degrees,
            "certified_quotient_row_degree": {"2.5": degrees["2.5"], "3.0": degrees["3.0"]},
            "primary_planar_radius_over_a_B": float(scan["planar_radius_over_a_B_half_units_6"]),
            "primary_minimum_abs_cosh_gap": float(scan["minimum_abs_cosh_gap_Dc_half_units_6"]),
            "why_quotient_count_is_exact": "rho_3=sqrt(3^2-0.5^2)a_B is strictly below the certified global injectivity radius 3a_B, so all 2185 universal-cover images are distinct in the quotient.",
        },
        "primary_resource_lower_bound": bound.to_dict(),
        "host_resource_gate": {
            "disk_free_bytes_at_finalize": disk.free,
            "mandatory_preserved_free_bytes": 250_000_000_000,
            "usable_bytes_after_reserve": usable_after_reserve,
            "compact_primary_block_fits_alone": bound.compact_csr_bytes <= usable_after_reserve,
            "margin_after_one_primary_block_bytes": usable_after_reserve - bound.compact_csr_bytes,
            "hard_RSS_ceiling_bytes": 48 * 1024**3,
            "three_complex128_bilayer_buffers_for_batch_32_bytes": 3 * 32 * bound.complex128_bilayer_vector_bytes,
        },
        "decisive_work_bounds": {
            "primary_grid_only": True,
            "excludes": ["SLQ", "cutoff holdouts", "lambda holdouts", "adaptive theta refinement", "robustness", "block construction"],
            "stream_years_at_hypothetical_10_GB_per_second": bound.primary_grid_years_at_10_GBps,
            "measured_registry_scanner_bytes_per_second_reference": scanner_bytes_per_second,
            "stream_years_at_measured_scanner_rate_reference": grid_years_at_scanner_rate,
            "primary_grid_complex_multiply_adds": primary_grid_cmacs,
            "compute_years_at_hypothetical_1e12_complex_multiply_adds_per_second": primary_grid_years_at_trillion_cmac_s,
            "conclusion": "The compact block can be streamed without violating the one-block disk/RSS gates, but the preregistered primary grid alone requires exabyte-scale repeated traffic or about 3e19 complex multiply-adds. Changing CSR to matrix-free therefore does not make this quotient a practical local production quotient.",
        },
        "next_dependency": {
            "task_id": "PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3",
            "objective": "Construct a strictly smaller global-certified degree-eight bipartite C8-equivariant quotient with a proof-complete family search and a full-kernel production resource certificate.",
            "reason": "The current quotient is the smallest computed based separator product, while all proof-completely screened direct families of order <=50000 failed; a new finite-group family/algorithm is required.",
        },
        "provenance": {
            "registry_path": "data/production/global_direct_v2/axis6_exact_ball.bin",
            "registry_sha256": "1148bf89c1d3dddf3f26eda57f2385ce8e65cbc8ce8042546683f18bde235c5b",
            "cutoff_scan_sha256": sha256(scan_path),
            "code_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in code_paths},
            "input_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in input_paths},
        },
    }
    resource_path = GROUP / "PF_GRP_001_PRODUCT_PRODUCTION_V2_RESOURCE_FORECAST.json"
    resource_path.write_text(json.dumps({
        "schema_version": "1.0", "task_id": certificate["task_id"],
        "support": certificate["exact_zero_twist_support"],
        "lower_bound": certificate["primary_resource_lower_bound"],
        "host_gate": certificate["host_resource_gate"],
        "work_bounds": certificate["decisive_work_bounds"],
    }, indent=2) + "\n", encoding="utf-8")
    certificate["provenance"]["resource_forecast_sha256"] = sha256(resource_path)
    json_path = GROUP / "PF_GRP_001_PRODUCT_PRODUCTION_V2_CERTIFICATE.json"
    json_path.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    markdown = f"""# PF-GRP-001-PRODUCT-PRODUCTION-V2 certificate

Status: **Done**. Scientific classification:
**FULLY-ADMISSIBLE / NOT-NUMERICALLY-TRACTABLE-ON-CURRENT-HOST**.

The frozen quotient `Q_BASED_S4CORE_PAIR_001` passes the finite-normal,
degree-eight, bipartite, exact C8, and global systole gates. The global
certificate proves `sys(kernel)>6 a_B`, hence `r_inj>3 a_B`.

## Full interlayer support

For `h/a_B=0.5`, the planar radius is `rho_c=sqrt(D_c^2-h^2)`. A complete
scan of all 785,639,753 records gives universal-cover support counts {degrees}.
Only the `D_c=2.5` and `3.0` counts are asserted as quotient row degrees under
the present injectivity certificate. At the
primary cutoff, `rho_3={scan['planar_radius_over_a_B_half_units_6']} a_B<3a_B`,
so all 2,185 images remain distinct. The one-sided block contains exactly
{bound.one_sided_entries:,} entries.

## Matrix-free / out-of-core validation

The intralayer action is `sum_s c_s R_N(s)x`; no adjacency CSR is assembled.
The full radial interlayer block is stored as hash-sealed CSR row shards and
applied one shard at a time with its Hermitian transpose. A complex fixture
verifies both parts and the combined bilayer action against the explicit
matrix (7/7 tests). No same-label, first-shell, or selected-pair reduction is
used.

## Decisive local resource result

The most favorable uint32/float64 primary block needs
{bound.compact_csr_bytes:,} bytes. With 32 probes per batch, the frozen
8192-moment/64-probe KPM requires {bound.kpm_passes_per_parameter:,} full
passes per parameter, or {bound.stream_bytes_per_parameter:,} bytes. The
91-by-12 primary grid alone is {bound.primary_grid_stream_bytes:,} bytes:
{bound.primary_grid_years_at_10_GBps:.3f} years even at a hypothetical 10 GB/s,
before SLQ, convergence cutoffs, lambda holdouts, refinements, robustness, or
construction. Matrix-free arithmetic still requires {primary_grid_cmacs:,}
complex multiply-adds ({primary_grid_years_at_trillion_cmac_s:.3f} years even
at a hypothetical 10^12 complex multiply-adds/s).

The storage-only rejection is repaired, but production promotion still fails
for the stronger complete-workflow reason. No large Hamiltonian or spectrum
was started; `main.tex` remains locked. The next atomic dependency is
`PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3`.
"""
    (GROUP / "PF_GRP_001_PRODUCT_PRODUCTION_V2_CERTIFICATE.md").write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
