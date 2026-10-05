"""PF-GRP-001 product-production-v2 matrix-free and resource tests."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from production_code.group.matrix_free_bilayer import (
    production_lower_bound,
    right_regular_action,
    streamed_hermitian_interlayer_action,
    write_full_interlayer_row_shards,
)


def _fixture(tmp_path: Path):
    order = 8
    q = np.arange(order)
    permutations = np.vstack(((q + 1) % order, (q - 1) % order, (3 * q + 1) % order))
    coefficients = np.array([1.0, 1.0, -0.25])
    rows, columns = np.indices((order, order))
    mask = ((rows + 2 * columns) % 3) != 0
    rows, columns = rows[mask], columns[mask]
    weights = np.exp(-0.1 * (1 + rows + columns))
    manifest = write_full_interlayer_row_shards(
        tmp_path / "interlayer", order=order, rows=rows, columns=columns,
        weights=weights, rows_per_shard=3,
    )
    return order, permutations, coefficients, rows, columns, weights, manifest


def test_right_regular_action_matches_explicit_matrix(tmp_path: Path) -> None:
    order, permutations, coefficients, *_ = _fixture(tmp_path)
    x = np.arange(order) + 1j * np.arange(order)[::-1]
    explicit = np.zeros((order, order), dtype=np.complex128)
    for permutation, coefficient in zip(permutations, coefficients, strict=True):
        explicit[np.arange(order), permutation] += coefficient
    np.testing.assert_allclose(right_regular_action(x, permutations, coefficients), explicit @ x)


def test_streamed_full_interlayer_matches_explicit_hermitian_block(tmp_path: Path) -> None:
    order, _, _, rows, columns, weights, manifest = _fixture(tmp_path)
    rng = np.random.default_rng(170217)
    x1 = rng.normal(size=order) + 1j * rng.normal(size=order)
    x2 = rng.normal(size=order) + 1j * rng.normal(size=order)
    block = np.zeros((order, order), dtype=np.complex128)
    block[rows, columns] = weights
    y1, y2 = streamed_hermitian_interlayer_action(manifest, x1, x2)
    np.testing.assert_allclose(y1, block @ x2, rtol=2e-15, atol=2e-15)
    np.testing.assert_allclose(y2, block.conj().T @ x1, rtol=2e-15, atol=2e-15)


def test_combined_bilayer_action_matches_explicit_matrix(tmp_path: Path) -> None:
    order, permutations, coefficients, rows, columns, weights, manifest = _fixture(tmp_path)
    rng = np.random.default_rng(170218)
    x1 = rng.normal(size=order) + 1j * rng.normal(size=order)
    x2 = rng.normal(size=order) + 1j * rng.normal(size=order)
    adjacency = np.zeros((order, order), dtype=np.complex128)
    for permutation, coefficient in zip(permutations, coefficients, strict=True):
        adjacency[np.arange(order), permutation] += coefficient
    interlayer = np.zeros((order, order), dtype=np.complex128)
    interlayer[rows, columns] = weights
    explicit = np.block([[adjacency, interlayer], [interlayer.conj().T, adjacency]])
    z1, z2 = streamed_hermitian_interlayer_action(manifest, x1, x2)
    observed = np.concatenate((
        right_regular_action(x1, permutations, coefficients) + z1,
        right_regular_action(x2, permutations, coefficients) + z2,
    ))
    np.testing.assert_allclose(observed, explicit @ np.concatenate((x1, x2)), rtol=2e-15, atol=2e-15)


def test_manifest_forbids_reduced_interlayer_semantics(tmp_path: Path) -> None:
    *_, manifest = _fixture(tmp_path)
    record = json.loads(manifest.read_text(encoding="utf-8"))
    assert record["preserves_all_supplied_supported_pairs"] is True
    assert record["same_label_reduction"] is False
    assert record["first_shell_reduction"] is False
    assert record["entries"] > record["order"]


def test_hash_verification_rejects_tampered_shard(tmp_path: Path) -> None:
    order, *_, manifest = _fixture(tmp_path)
    record = json.loads(manifest.read_text(encoding="utf-8"))
    target = manifest.parent / record["shards"][0]["files"]["weights"]["path"]
    with target.open("ab") as stream:
        stream.write(b"tamper")
    with pytest.raises(ValueError, match="hash mismatch"):
        streamed_hermitian_interlayer_action(manifest, np.ones(order), np.ones(order))


def test_frozen_primary_resource_lower_bound() -> None:
    bound = production_lower_bound(
        quotient_order=11_943_936, zero_twist_degree=2_185,
        kpm_moments=8_192, probes=64, probe_batch=32,
        theta_points=91, coupling_points=12,
    )
    assert bound.one_sided_entries == 26_097_500_160
    assert bound.compact_csr_bytes == 313_265_553_416
    assert bound.kpm_passes_per_parameter == 16_384
    assert bound.primary_parameter_points == 1_092
    assert bound.primary_grid_years_at_10_GBps > 17.7
    assert bound.complex_multiply_adds_per_parameter == 27_365_212_327_772_160


def test_completed_cutoff_scan_is_far_from_numeric_boundaries() -> None:
    values = {}
    for line in Path("data/production/global_direct_v2/interlayer_cutoff_counts.tsv").read_text(encoding="utf-8").splitlines():
        key, value = line.split("\t", 1)
        values[key] = value
    assert values["complete"] == "1"
    assert int(values["count_Dc_half_units_6"]) == 2_185
    assert float(values["planar_radius_over_a_B_half_units_6"]) < 3.0
    assert float(values["minimum_abs_cosh_gap_Dc_half_units_6"]) > 70.0
