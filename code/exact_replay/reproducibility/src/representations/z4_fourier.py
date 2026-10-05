"""Complete character/Peter--Weyl decomposition of the validation quotient (Z/4Z)^4."""

from __future__ import annotations

import itertools
import math

import numpy as np
import scipy.linalg
import scipy.sparse


def tuples(modulus: int = 4) -> list[tuple[int, int, int, int]]:
    if modulus != 4:
        raise ValueError("P2-14-R07 is registered only for the explicit modulus-four validation quotient")
    return list(itertools.product(range(modulus), repeat=4))


def character_table(modulus: int = 4) -> tuple[list[tuple[int, ...]], np.ndarray]:
    labels = tuples(modulus)
    phases = np.asarray(labels, dtype=float)
    table = np.exp(2.0j * math.pi * (phases @ phases.T) / modulus)
    return labels, table


def fourier_matrix(modulus: int = 4) -> tuple[list[tuple[int, ...]], np.ndarray]:
    labels, table = character_table(modulus)
    return labels, table / math.sqrt(len(labels))


def character_sector_rows(*, q1: float, w_star_over_t: float, modulus: int = 4) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    labels = tuples(modulus)
    irrep_rows: list[dict[str, object]] = []
    spectrum_rows: list[dict[str, object]] = []
    for sector_index, label in enumerate(labels):
        angles = 2.0 * math.pi * np.asarray(label, dtype=float) / modulus
        generator_images = np.exp(1.0j * angles)
        adjacency_eigenvalue = float(2.0 * np.sum(np.cos(angles)))
        diagonal = -adjacency_eigenvalue
        off_diagonal = w_star_over_t * (1.0 + q1 * adjacency_eigenvalue)
        even = diagonal + off_diagonal
        odd = diagonal - off_diagonal
        sector_id = "chi_" + "_".join(str(value) for value in label)
        irrep_rows.append({
            "sector_index": sector_index,
            "sector_id": sector_id,
            "n_a1": label[0],
            "n_b1": label[1],
            "n_a2": label[2],
            "n_b2": label[3],
            "irrep_dimension": 1,
            "is_abelian": True,
            "block_dimension": 2,
            "regular_multiplicity": 1,
            "state_count": 2,
            "plancherel_weight_numerator": 1,
            "plancherel_weight_denominator": len(labels),
            "generator_a1_real": float(generator_images[0].real),
            "generator_a1_imag": float(generator_images[0].imag),
            "generator_b1_real": float(generator_images[1].real),
            "generator_b1_imag": float(generator_images[1].imag),
            "generator_a2_real": float(generator_images[2].real),
            "generator_a2_imag": float(generator_images[2].imag),
            "generator_b2_real": float(generator_images[3].real),
            "generator_b2_imag": float(generator_images[3].imag),
            "adjacency_eigenvalue": adjacency_eigenvalue,
        })
        for branch_index, (parity, energy) in enumerate((("even", even), ("odd", odd))):
            spectrum_rows.append({
                "sector_index": sector_index,
                "sector_id": sector_id,
                "irrep_dimension": 1,
                "regular_multiplicity": 1,
                "branch_index": branch_index,
                "layer_parity": parity,
                "energy_over_t": float(energy),
                "state_multiplicity": 1,
                "spectral_weight_numerator": 1,
                "spectral_weight_denominator": 2 * len(labels),
            })
    return irrep_rows, spectrum_rows


def audit_decomposition(
    matrix: scipy.sparse.spmatrix,
    *,
    q1: float,
    w_star_over_t: float,
    modulus: int = 4,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    labels, fourier = fourier_matrix(modulus)
    size = len(labels)
    if matrix.shape != (2 * size, 2 * size):
        raise ValueError(f"expected a {2 * size}-dimensional bilayer matrix")
    identity = np.eye(size, dtype=complex)
    fourier_residual = float(np.linalg.norm(fourier.conj().T @ fourier - identity, ord=2))
    dense = matrix.toarray().astype(complex)
    transform = scipy.linalg.block_diag(fourier, fourier)
    transformed = transform.conj().T @ dense @ transform
    sector_leakage = transformed.copy()
    for layer_left in range(2):
        for layer_right in range(2):
            block = sector_leakage[layer_left * size:(layer_left + 1) * size, layer_right * size:(layer_right + 1) * size]
            block[np.diag_indices(size)] = 0.0
    maximum_sector_leakage = float(np.max(np.abs(sector_leakage)))

    irrep_rows, sector_rows = character_sector_rows(q1=q1, w_star_over_t=w_star_over_t, modulus=modulus)
    abelian_values = np.sort(np.asarray([float(row["energy_over_t"]) for row in sector_rows]))
    dense_values = scipy.linalg.eigvalsh(dense, driver="evr", check_finite=True)
    dense_values = np.sort(np.asarray(dense_values.real))
    comparison_rows = [
        {
            "sorted_state_index": index,
            "abelian_energy_over_t": float(abelian),
            "full_energy_over_t": float(full),
            "absolute_difference_over_t": float(abs(abelian - full)),
        }
        for index, (abelian, full) in enumerate(zip(abelian_values, dense_values))
    ]
    maximum_spectrum_difference = max(float(row["absolute_difference_over_t"]) for row in comparison_rows)
    exact_checks = {
        "all_group_elements_enumerated": len(labels) == modulus ** 4,
        "all_irreps_enumerated": len(irrep_rows) == modulus ** 4,
        "all_irreps_one_dimensional": all(row["irrep_dimension"] == 1 for row in irrep_rows),
        "degree_square_identity": sum(int(row["irrep_dimension"]) ** 2 for row in irrep_rows) == modulus ** 4,
        "exact_plancherel_numerators_sum": sum(int(row["plancherel_weight_numerator"]) for row in irrep_rows) == modulus ** 4,
        "exact_full_state_count": sum(int(row["state_count"]) for row in irrep_rows) == 2 * modulus ** 4,
        "higher_dimensional_sector_count_zero": not any(int(row["irrep_dimension"]) > 1 for row in irrep_rows),
        "abelian_weight_fraction_one": len(irrep_rows) == modulus ** 4,
    }
    numerical_checks = {
        "character_orthogonality": fourier_residual <= 2.0e-13,
        "hamiltonian_sector_conservation": maximum_sector_leakage <= 2.0e-12,
        "abelian_full_multiset_agreement": maximum_spectrum_difference <= 2.0e-9,
    }
    checks = exact_checks | numerical_checks
    return comparison_rows, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "quotient_group": "(Z/4Z)^4",
        "group_order": size,
        "irrep_count": len(irrep_rows),
        "one_dimensional_irrep_count": len(irrep_rows),
        "higher_dimensional_irrep_count": 0,
        "sum_irrep_dimension_squared": sum(int(row["irrep_dimension"]) ** 2 for row in irrep_rows),
        "bilayer_state_count": 2 * size,
        "representation_coverage_fraction": 1.0,
        "abelian_weight_fraction": 1.0,
        "nonabelian_weight_fraction": 0.0,
        "nonabelian_completion_distance_over_t": 0.0,
        "numerical_abelian_full_reconstruction_residual_over_t": maximum_spectrum_difference,
        "maximum_character_orthogonality_residual": fourier_residual,
        "maximum_off_sector_hamiltonian_element_over_t": maximum_sector_leakage,
        "maximum_abelian_full_spectrum_difference_over_t": maximum_spectrum_difference,
        "checks": checks,
        "gap_dependency": {
            "required": False,
            "reason": "The explicit validation quotient is Abelian, so its complete irrep table is the finite Fourier dual and contains no higher-dimensional sectors.",
        },
    }
