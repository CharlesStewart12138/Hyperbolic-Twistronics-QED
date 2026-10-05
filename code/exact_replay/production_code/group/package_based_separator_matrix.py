"""Package the exact default-one based separator matrix as a NumPy archive."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import struct

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "quotient_separator"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_orbits(path: Path):
    with path.open("rb") as handle:
        if handle.read(8) != b"BOLZAO01":
            raise ValueError("bad orbit binary magic")
        elements, rows = struct.unpack("<QQ", handle.read(16))
    offset = 24
    element_to_row = np.memmap(path, mode="r", dtype="<u4", offset=offset, shape=(elements,))
    offset += elements * 4
    representatives = np.memmap(path, mode="r", dtype="<u4", offset=offset, shape=(rows,))
    offset += rows * 4
    weights = np.memmap(path, mode="r", dtype="<u4", offset=offset, shape=(rows,))
    if offset + rows * 4 != path.stat().st_size:
        raise ValueError("orbit binary length mismatch")
    return elements, rows, element_to_row, representatives, weights


def read_csc(path: Path):
    with path.open("rb") as handle:
        if handle.read(8) != b"BOLZAK01":
            raise ValueError("bad kernel CSC magic")
        rows, columns, nnz = struct.unpack("<QQQ", handle.read(24))
    offset = 32
    indptr = np.memmap(path, mode="r", dtype="<u8", offset=offset, shape=(columns + 1,))
    offset += (columns + 1) * 8
    indices = np.memmap(path, mode="r", dtype="<u4", offset=offset, shape=(nnz,))
    if offset + nnz * 4 != path.stat().st_size:
        raise ValueError("kernel CSC length mismatch")
    return rows, columns, nnz, indptr, indices


def main() -> None:
    orbit_path = OUT / "based_orbit_map.bin"
    csc_path = OUT / "separator_kernel_exceptions.cscbin"
    manifest_path = OUT / "candidate_manifest.tsv"
    solution_path = OUT / "based_separator_solution.json"
    matrix_path = OUT / "separator_matrix.npz"

    elements, orbit_rows, element_to_row, representatives, weights = read_orbits(orbit_path)
    csc_rows, columns, nnz, indptr, indices = read_csc(csc_path)
    if elements != 23_129_593 or orbit_rows != csc_rows or columns != 1182:
        raise AssertionError("matrix dimensions drifted from the exact certificate")
    if int(weights.sum(dtype=np.uint64)) != elements - 1:
        raise AssertionError("orbit weights do not expand to every dangerous element")
    if int(indptr[0]) != 0 or int(indptr[-1]) != nnz or np.any(indptr[1:] < indptr[:-1]):
        raise AssertionError("invalid CSC pointer array")
    if nnz and int(indices.max()) >= orbit_rows:
        raise AssertionError("kernel exception row outside matrix")

    with manifest_path.open(encoding="utf-8", newline="") as handle:
        manifest = list(csv.DictReader(handle, dialect="excel-tab"))
    if len(manifest) != columns:
        raise AssertionError("candidate manifest width mismatch")
    candidate_ids = np.array([row["candidate_id"] for row in manifest])
    candidate_families = np.array([row["family"] for row in manifest])
    candidate_base_degree = np.array([int(row["degree"]) for row in manifest], dtype=np.int8)
    candidate_parent_columns = np.array(
        [[int(row["parent_left"]), int(row["parent_right"])] for row in manifest], dtype=np.int32
    )
    solution = json.loads(solution_path.read_text(encoding="utf-8"))
    selected = np.array(solution["selected_columns"], dtype=np.uint32)
    selected_column = int(selected[0])
    if selected.tolist() != [973] or int(indptr[selected_column + 1] - indptr[selected_column]) != 0:
        raise AssertionError("selected exact one-column cover is not kernel-free")

    np.savez_compressed(
        matrix_path,
        schema_version=np.array("1.0"),
        encoding=np.array("default_one_with_zero_kernel_exceptions_csc"),
        default_entry=np.array(1, dtype=np.uint8),
        exception_entry=np.array(0, dtype=np.uint8),
        element_matrix_shape=np.array([elements - 1, columns], dtype=np.uint64),
        orbit_matrix_shape=np.array([orbit_rows, columns], dtype=np.uint64),
        element_ids=np.arange(1, elements, dtype=np.uint32),
        element_to_orbit_row=np.asarray(element_to_row[1:]),
        orbit_representative_element_id=np.asarray(representatives),
        orbit_weight=np.asarray(weights, dtype=np.uint8),
        zero_indptr=np.asarray(indptr),
        zero_orbit_indices=np.asarray(indices),
        candidate_ids=candidate_ids,
        candidate_families=candidate_families,
        candidate_base_degree=candidate_base_degree,
        candidate_parent_columns=candidate_parent_columns,
        selected_columns=selected,
        source_based_csv_sha256=np.array("80e004296de1410c6bf5a1caa54bfcebdca4592f453a53f559893eecde38267c"),
    )

    hashes = {
        "dangerous_based_csv": "80e004296de1410c6bf5a1caa54bfcebdca4592f453a53f559893eecde38267c",
        "candidate_manifest_tsv": sha256(manifest_path),
        "based_tree_meta_bin": sha256(OUT / "based_tree_meta.bin"),
        "based_orbit_map_bin": sha256(orbit_path),
        "separator_kernel_exceptions_cscbin": sha256(csc_path),
        "separator_matrix_npz": sha256(matrix_path),
    }
    selected_id = str(candidate_ids[selected_column])
    selected_record = next(
        json.loads(line)
        for line in (ROOT / "data" / "production" / "quotient_search_v3" / "candidates_v3.jsonl").read_text(encoding="utf-8").splitlines()
        if json.loads(line)["candidate_id"] == selected_id
    )
    summary = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-Q-GEO-SEP-BASED",
        "status": "Done",
        "scope": "BASED_ONLY",
        "dangerous_elements": elements - 1,
        "lossless_inversion_c8_orbit_rows": orbit_rows,
        "candidate_maps_evaluated": columns,
        "registered_candidate_breakdown": {"repaired_shell_v2": 903, "v3": 279},
        "independent_base_maps_evaluated": 1158,
        "exact_composite_columns": 24,
        "matrix_encoding": {
            "logical_entry": "1 iff the candidate separates the dangerous element; 0 iff the element is in the candidate kernel",
            "storage": "default 1; zero/kernel exceptions in CSC over lossless inversion-C8 orbit rows",
            "kernel_exception_orbit_entries": int(nnz),
            "element_expansion_is_explicit": True,
        },
        "uncovered_elements": 0,
        "separator_solution": {
            "status": solution["solution_status"],
            "count": 1,
            "column": selected_column,
            "candidate_id": selected_id,
            "base_group": selected_record["base_group"],
            "base_generator_indices": selected_record["base_generator_indices"],
            "practical_core_image_order": selected_record["exact_core_order"],
            "separated_based_elements": elements - 1,
            "kernel_hits_in_based_set": 0,
        },
        "scientific_scope": {
            "based_geometric_condition": "certified",
            "global_systolic_condition": "not evaluated; global obstruction enumeration is Deferred",
            "production_quotient": "not released because PQ-14/PQ-16 remain unavailable",
            "numerical_tractability": "selected core order is 335,923,200,000,000 and is not a tractable direct Hamiltonian quotient",
        },
        "hashes": hashes,
        "main_tex_modified": False,
    }
    (OUT / "BASED_SEPARATOR_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (OUT / "BASED_SEPARATOR_SUMMARY.md").write_text(
        f"# Exact based separator matrix\n\n"
        f"All **{elements - 1:,}** certified based-dangerous elements were evaluated against all "
        f"**{columns:,}** registered quotient-map columns (903 repaired-shell candidates and 279 v3 candidates).\n\n"
        f"The logical matrix entry is one exactly when the candidate separates the element.  "
        f"`separator_matrix.npz` stores this default-one matrix losslessly by recording only its "
        f"{int(nnz):,} zero/kernel exceptions on {orbit_rows:,} inversion-by-C8 symmetry rows, together "
        f"with an explicit map for every one of the {elements - 1:,} original element rows.\n\n"
        f"## Exact cover result\n\n"
        f"Column {selected_column}, `{selected_id}`, has no kernel hit in the exact based set and therefore separates "
        f"all {elements - 1:,} elements by itself.  The certified separator count is **1**, which is "
        f"automatically optimal.  The selected practical-core image has exact order "
        f"{selected_record['exact_core_order']:,}.\n\n"
        f"This closes `Q-GEO-SEP-BASED` only.  It does not establish the global systolic condition, "
        f"does not create a production quotient, and does not make the selected image numerically tractable.\n\n"
        f"## Archive integrity\n\n"
        + "\n".join(f"- `{name}`: `{digest}`" for name, digest in hashes.items())
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "matrix": str(matrix_path),
        "matrix_bytes": matrix_path.stat().st_size,
        "matrix_sha256": hashes["separator_matrix_npz"],
        "element_shape": [elements - 1, columns],
        "orbit_shape": [orbit_rows, columns],
        "zero_exceptions": int(nnz),
        "selected": selected_id,
    }, indent=2))


if __name__ == "__main__":
    main()
