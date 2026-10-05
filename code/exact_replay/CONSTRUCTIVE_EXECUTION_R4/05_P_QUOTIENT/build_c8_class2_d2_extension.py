"""Extend the selected C8-stable class-2 row space from dimension 1 to 2."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
import time
from pathlib import Path


p2 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")

ROOT = Path(__file__).resolve().parents[2]; R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "05_P_QUOTIENT" / "P2C2_C8_D2_EXTENSION.certificate.json"
WITNESSES = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
PARENT_ROW = 19


def span(rows: tuple[int, ...]) -> set[int]:
    result = {0}
    for row in rows:
        result |= {value ^ row for value in tuple(result)}
    return result


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def factor_hash(rows: tuple[int, ...], elements: list[tuple[int, int]]) -> str:
    payload = {
        "family": "C8-stable class-2 p2 dimension-two extension",
        "parent_dual_row": PARENT_ROW,
        "dual_row_space": rows,
        "physical_generators": p2.q_physical_generators(rows),
        "actual_order": len(elements),
        "elements_sha256": hashlib.sha256(json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")).hexdigest().upper(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def main() -> None:
    started = time.perf_counter(); columns = p2.phi_central_columns()
    with WITNESSES.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    target_row = next(row for row in witness_rows if row["First candidate killed"] == "CAND-R4-0003")
    target_word = tuple(target_row["Canonical word"].split())
    tested = 0; stable_extensions = 0; selected = None; elements = []; rotation = None
    for rows in p2.canonical_row_spaces(2):
        tested += 1
        if PARENT_ROW not in span(rows):
            continue
        if not p2.stable(rows, columns):
            continue
        stable_extensions += 1
        if p2.q_word(target_word, rows) == (0, 0):
            continue
        trial_elements, trial_rotation = p2.enumerate_q(rows)
        if trial_rotation is None or len(trial_elements) != 64:
            continue
        selected, elements, rotation = rows, trial_elements, trial_rotation
        break
    if selected is None or rotation is None:
        raise RuntimeError("no dimension-two C8-stable extension separates the candidate-0003 witness")
    physical = p2.q_physical_generators(selected)
    coverage = {
        row["Witness ID"]: int(p2.q_word(tuple(row["Canonical word"].split()), selected) != (0, 0))
        for row in witness_rows
    }
    marked_hash = factor_hash(selected, elements); factor_id = f"P2C2-C8-D2-{marked_hash[:16]}"
    certificate = {
        "schema_version": "1.0", "factor_id": factor_id,
        "family": "C8-stable lower-exponent-2 class-2 dimension-two central quotient",
        "parent_factor_id": "P2C2-C8-D1-7114D44C79829117",
        "kernel_relation": "dimension-two kernel is contained in the parent dimension-one kernel",
        "marginal_dimension": 2, "actual_order": len(elements), "marked_quotient_hash": marked_hash,
        "construction": {
            "central_basis": list(p2.CENTRAL_BASIS), "parent_dual_row": PARENT_ROW,
            "selected_dual_row_space_integers": list(selected),
            "selected_dual_row_space_nonzero_vectors": sorted(span(selected) - {0}),
            "selected_dual_row_space_bits_lsb_first": [format(row, "09b")[::-1] for row in selected],
            "deterministic_search": "lexicographic canonical dimension-two row spaces containing row 19",
        },
        "search_counts": {"row_spaces_examined_through_selection": tested, "C8_stable_extensions_through_selection": stable_extensions},
        "proof_rows": {
            "contains_parent_dual_row": PARENT_ROW in span(selected),
            "C8_stable": p2.stable(selected, columns),
            "target_witness_id": target_row["Witness ID"],
            "target_image": list(p2.q_word(target_word, selected)),
            "target_separated": p2.q_word(target_word, selected) != (0, 0),
            "actual_generated_order": len(elements),
            "complete_normal_form_order": 64,
            "physical_shell_distinct_nonidentity": len(set(physical)) == 8 and (0, 0) not in physical,
            "rotation_bijective": len(set(rotation.values())) == 64,
            "rotation_eighth_identity": all(_iterate(rotation, element, 8) == element for element in elements),
            "rotation_exact_order_eight": any(_iterate(rotation, element, 4) != element for element in elements),
            "parity": all((element[0].bit_count() & 1) == 1 for element in physical),
        },
        "witness_coverage": coverage, "runtime_seconds": time.perf_counter() - started,
        "classification": "PASS",
    }
    if not all(value for value in certificate["proof_rows"].values() if isinstance(value, bool)):
        raise RuntimeError(f"dimension-two proof failure: {certificate['proof_rows']}")
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")

    with LIBRARY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); fields = list(reader.fieldnames or []); factors = list(reader)
    factors.append({
        "factor_id": factor_id, "family": certificate["family"], "parameters": "p=2; class=2; marginal_dimension=2; extends D1",
        "actual_order": "64", "marked_quotient_hash": marked_hash, "coverage_count": str(sum(coverage.values())),
        "C8_cost": "0", "parity_cost": "0", "subdirect_marginal_order_increase": "2",
        "resource_marginal_increase": "64", "certificate_path": "05_P_QUOTIENT/P2C2_C8_D2_EXTENSION.certificate.json",
        "certificate_sha256": hashlib.sha256(CERT.read_bytes()).hexdigest().upper(), "status": "AVAILABLE",
    })
    write_tsv(LIBRARY, fields, factors)
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); old_fields = list(reader.fieldnames or []); rows = list(reader)
    new_fields = old_fields + [factor_id]
    for row in rows: row[factor_id] = str(coverage[row["witness_id"]])
    write_tsv(MATRIX, new_fields, rows)


def _iterate(mapping: dict, value, count: int):
    for _ in range(count): value = mapping[value]
    return value


if __name__ == "__main__": main()
