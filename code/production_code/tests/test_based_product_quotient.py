from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "production_code" / "group" / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json"
MATRIX = ROOT / "data" / "production" / "quotient_separator" / "separator_matrix.npz"


def test_based_product_passes_exact_available_pq_gates_only():
    record = json.loads(CERT.read_text(encoding="utf-8"))
    assert record["quotient_id"] == "Q_BASED_S4CORE_PAIR_001"
    assert record["construction"]["selected_columns"] == [12, 231]
    assert record["construction"]["actual_generated_image_order"] == 11_943_936
    assert record["construction"]["full_cartesian_product_instantiated"] is False
    assert record["construction"]["c8_orbit_closure_applied"] is True
    assert record["construction"]["parity_factor_included_once"] is True
    pq = record["pq_checks"]
    for number in list(range(1, 14)) + [15]:
        value = next(value for key, value in pq.items() if key.startswith(f"PQ-{number:02d}_"))
        assert value.startswith("PASS")
    assert pq["PQ-14_all_global_dangerous_classes_separated"] == "UNAVAILABLE_D_GLOBAL_DEFERRED"
    assert pq["PQ-16_global_geometric_injectivity"] == "UNAVAILABLE_D_GLOBAL_DEFERRED"
    assert pq["PQ-17_Dc_no_wraparound"] == "PARTIAL_BASED_ONLY_NOT_PRODUCTION"
    assert record["smoke_released"] is False
    assert record["main_tex_modified"] is False


def test_selected_pair_has_exactly_empty_kernel_intersection():
    with np.load(MATRIX) as matrix:
        indptr = matrix["zero_indptr"]
        indices = matrix["zero_orbit_indices"]
        left = indices[int(indptr[12]):int(indptr[13])]
        right = indices[int(indptr[231]):int(indptr[232])]
        assert len(left) > 0 and len(right) > 0
        assert len(np.intersect1d(left, right, assume_unique=True)) == 0


def test_practical_bounds_are_exact_and_no_production_yaml_exists():
    record = json.loads(CERT.read_text(encoding="utf-8"))
    practical = record["practical_feasibility"]
    n = 11_943_936
    assert practical["N"] == n
    assert practical["two_N"] == 2 * n
    assert practical["nearest_neighbor_only_nnz_lower_bound"] == 16 * n
    assert practical["nearest_neighbor_only_CSR_complex128_int64_bytes_lower_bound"] == 24 * 16 * n + 8 * (2 * n + 1)
    assert practical["interlayer_cutoff_entries_included_in_these_bounds"] is False
    assert not (ROOT / "production_code" / "config" / "production_cover_A_level_1.yaml").exists()
