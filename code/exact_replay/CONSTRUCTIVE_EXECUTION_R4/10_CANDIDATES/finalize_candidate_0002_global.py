"""Finalize CAND-R4-0002 at its first failing post-local gate.

The candidate passed the structural and complete B_geom(3) gates.  This
script replays the early-exit global-registry word in exact arithmetic,
registers its C8/inverse canonical orbit, and rejects the candidate at the
strict global systole gate.  Floating point values are not used.
"""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from pathlib import Path

import sympy as sp

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import (
    IDENTITY_MATRIX,
    field_to_sympy,
    matrix_from_word,
)


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0002")
arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0002.certificate.json"
WITNESS_SCAN = R4 / "10_CANDIDATES" / "CAND-R4-0002.global_witness.tsv"
CHECKPOINT = R4 / "checkpoints" / "CAND-R4-0002-axis6.tsv"
MANIFEST = R4 / "00_FROZEN_INPUTS" / "manifests" / "axis6_exact_ball_manifest.json"
SCANNER = R4 / "10_CANDIDATES" / "scan_candidate_0002_axis6_v2.cpp"
EXECUTABLE = R4 / "10_CANDIDATES" / "scan_candidate_0002_axis6_v2.exe"
DANGER_REGISTRY = R4 / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
WITNESS_LEDGER = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
SEPARATOR_MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
SEPARATOR_LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
CANDIDATE_LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
ITERATION = R4 / "09_CEGAR" / "ITERATION_0002_GLOBAL_REJECTION.json"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_single_scan_row() -> dict[str, str]:
    with WITNESS_SCAN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1:
        raise RuntimeError("candidate-specific global scanner must emit exactly one early-exit witness")
    return rows[0]


def exact_global_witness() -> dict:
    row = load_single_scan_row()
    source_word = tuple(row["word"].split())
    canonical = d0.canonical_c8_inverse_word(source_word)
    image = candidate.word_image(canonical)
    if image != candidate.identity():
        raise RuntimeError("global scanner word is not in the candidate kernel")

    matrix = matrix_from_word(canonical)
    key = projective_key(matrix)
    if key == projective_key(IDENTITY_MATRIX):
        raise RuntimeError("global scanner word is identity in Gamma_B")
    payload = json.dumps(key, separators=(",", ":"))
    key_hash = hashlib.sha256(payload.encode("ascii")).hexdigest().upper()

    a = matrix[0]
    # tr(M)/2 = Re(a).  The imaginary part of a is irrelevant to the trace.
    if a[3] or a[4]:
        raise RuntimeError("this witness unexpectedly has beta terms in its real half-trace")
    denominator = 1 << a[0]
    trace_expr = sp.re(field_to_sympy(a)).expand()
    cutoff = 2405 + 1700 * sp.sqrt(2)
    abs_trace = sp.Abs(trace_expr)
    # Resolve this witness exactly from its coefficient signs, then cross-check SymPy.
    if a[1] >= 0 and a[2] >= 0:
        abs_coefficients = (a[1], a[2])
    elif a[1] <= 0 and a[2] <= 0:
        abs_coefficients = (-a[1], -a[2])
    else:
        raise RuntimeError("mixed-sign Q(sqrt(2)) trace requires a separate exact sign branch")
    abs_expr = (abs_coefficients[0] + abs_coefficients[1] * sp.sqrt(2)) / denominator
    margin = sp.expand(cutoff - abs_expr)
    squared_delta = sp.expand(abs_expr**2 - cutoff**2)
    if margin.is_positive is not True or squared_delta.is_negative is not True:
        raise RuntimeError(f"exact global cutoff did not certify strict failure: {margin=}, {squared_delta=}")
    if sp.simplify(abs_trace - abs_expr) != 0:
        raise RuntimeError("absolute half-trace reconstruction mismatch")

    scanner_coefficients = tuple(int(row[f"re_c{i}"]) for i in range(4))
    if int(row["exponent"]) != a[0] or scanner_coefficients != tuple(a[1:5]):
        raise RuntimeError("scanner and independent exact trace coefficients disagree")

    return {
        "witness_id": f"W-{key_hash[:20]}",
        "canonical_word": list(canonical),
        "source_word": list(source_word),
        "record_index_zero_based": int(row["record_index"]),
        "record_depth": int(row["depth"]),
        "candidate_image": list(image),
        "candidate_image_identity": True,
        "nonidentity_in_Gamma_B": True,
        "exact_group_key": payload,
        "exact_group_key_sha256": key_hash,
        "global_type": "D_global(6a_B)",
        "half_trace_real_field": {
            "basis": ["1", "sqrt(2)"],
            "denominator_power_of_two": a[0],
            "signed_coefficients": [a[1], a[2]],
            "absolute_coefficients": list(abs_coefficients),
            "absolute_expression": str(abs_expr),
        },
        "cutoff_cosh_3aB_over_R": "2405 + 1700*sqrt(2)",
        "strict_positive_cutoff_margin": str(margin),
        "squared_cutoff_delta": str(squared_delta),
        "translation_length_over_a_B": f"acosh({abs_expr})/acosh(1+sqrt(2))",
        "boundary_policy": "equality is dangerous; this witness is strictly below the cutoff",
        "early_exit_scope": "first dangerous kernel hit in canonical registry order",
        "registry_manifest": "00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json",
        "registry_manifest_sha256": file_hash(MANIFEST),
        "scanner_source": "10_CANDIDATES/scan_candidate_0002_axis6_v2.cpp",
        "scanner_source_sha256": file_hash(SCANNER),
        "scanner_executable_sha256": file_hash(EXECUTABLE),
        "scanner_checkpoint_sha256": file_hash(CHECKPOINT),
        "scanner_witness_sha256": file_hash(WITNESS_SCAN),
    }


def register_witness(witness: dict) -> tuple[str, str, list[str]]:
    word = tuple(witness["canonical_word"])
    witness_id = witness["witness_id"]
    orbit_id = f"C8-{hashlib.sha256(' '.join(word).encode('ascii')).hexdigest().upper()[:20]}"

    with DANGER_REGISTRY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        danger_fields = list(reader.fieldnames or [])
        danger_rows = list(reader)
    danger_id = f"DGLOBAL-R6-C0002-{witness_id}"
    if not any(row["danger_id"] == danger_id for row in danger_rows):
        danger_rows.append({
            "danger_id": danger_id,
            "type": "D_global(6a_B)",
            "constraint_word_geometric": " ".join(word),
            "canonical_word_geometric": " ".join(word),
            "canonical_word_standard": " ".join(d0.standard_word(word)),
            "exact_group_key": witness["exact_group_key"],
            "exact_group_key_sha256": witness["exact_group_key_sha256"],
            "witness_id": witness_id,
            "word_depth": str(len(word)),
            "based_displacement_over_a_B": "",
            "translation_length_over_a_B": witness["translation_length_over_a_B"],
            "translation_length_interval": "STRICTLY_LESS_THAN_6",
            "c8_orbit_id": orbit_id,
            "legacy_source_orbit_id": "",
            "nonidentity_in_Gamma_B": "PASS_EXACT_KEY",
            "geometry_status": "PASS_EXACT_TRACE_STRICT",
            "geometry_statement": "kernel element has translation length strictly less than 6*a_B",
            "source_certificate": "10_CANDIDATES/CAND-R4-0002.certificate.json",
            "registry_status": "ACTIVE_CEGAR",
        })
        write_tsv(DANGER_REGISTRY, danger_fields, sorted(danger_rows, key=lambda item: item["danger_id"]))

    with SEPARATOR_LIBRARY.open(encoding="utf-8", newline="") as handle:
        factors = list(csv.DictReader(handle, delimiter="\t"))
    factor_values: dict[str, str] = {}
    known: list[str] = []
    for factor in factors:
        prime = int(factor["parameters"].split("p=", 1)[1].split(";", 1)[0])
        separated = arith.word_image(word, prime) != arith.aidentity(prime)
        factor_values[factor["factor_id"]] = str(int(separated))
        if separated:
            known.append(factor["factor_id"])

    with WITNESS_LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        witness_fields = list(reader.fieldnames or [])
        witness_rows = list(reader)
    if not any(row["Witness ID"] == witness_id for row in witness_rows):
        witness_rows.append({
            "Witness ID": witness_id,
            "Canonical word": " ".join(word),
            "Exact group key": witness["exact_group_key"],
            "Type": "D_global(6a_B)",
            "Word depth": str(len(word)),
            "Based displacement if relevant": "",
            "Translation length interval/exact expression": witness["translation_length_over_a_B"],
            "C8 orbit ID": orbit_id,
            "First candidate killed": "CAND-R4-0002",
            "Separator factors known": ",".join(known),
            "Currently separated by candidate": "NO",
            "Certificate path": "10_CANDIDATES/CAND-R4-0002.certificate.json",
        })
        write_tsv(WITNESS_LEDGER, witness_fields, sorted(witness_rows, key=lambda item: item["Witness ID"]))

    with SEPARATOR_MATRIX.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        matrix_fields = list(reader.fieldnames or [])
        matrix_rows = list(reader)
    if not any(row["witness_id"] == witness_id for row in matrix_rows):
        matrix_rows.append({"witness_id": witness_id, **factor_values})
        write_tsv(SEPARATOR_MATRIX, matrix_fields, sorted(matrix_rows, key=lambda item: item["witness_id"]))
    return witness_id, orbit_id, known


def update_candidate_ledger(certificate: dict, witness_id: str, orbit_id: str) -> None:
    with CANDIDATE_LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    for row in rows:
        if row["Candidate ID"] != "CAND-R4-0002":
            continue
        row["Based status"] = "NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"
        row["Global status"] = "FAIL_EARLY_EXACT_WITNESS"
        row["Shortest failure witness"] = witness_id
        row["Witness orbit ID"] = orbit_id
        row["Resource estimate"] = json.dumps(certificate["resource"], separators=(",", ":"))
        row["Final disposition"] = "REJECTED_GLOBAL_WITNESS"
        row["Certificate hash"] = file_hash(CERT)
        break
    else:
        raise RuntimeError("candidate 0002 row is absent from the ledger")
    write_tsv(CANDIDATE_LEDGER, fields, rows)


def main() -> None:
    certificate = json.loads(CERT.read_text(encoding="utf-8"))
    if certificate["classification"] != "LOCAL_PASS_GLOBAL_PENDING":
        raise RuntimeError("candidate 0002 is not at the expected pre-global stage")
    witness = exact_global_witness()
    certificate["schema_version"] = "1.1"
    certificate["gates"]["based"] = "NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"
    certificate["gates"]["global_systole"] = "FAIL_EARLY_EXACT_WITNESS"
    certificate["global_failure_witness"] = witness
    certificate["resource"].update({
        "global_registry_total_records": 785_639_753,
        "global_registry_scanned_records": 2_488_063,
        "global_scan_early_exit": True,
        "global_scan_elapsed_seconds": 0.265863,
        "hpc_escalation_triggered": False,
    })
    certificate["classification"] = "REJECTED_GLOBAL_WITNESS"
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")

    witness_id, orbit_id, known = register_witness(witness)
    update_candidate_ledger(certificate, witness_id, orbit_id)
    ITERATION.write_text(json.dumps({
        "schema_version": "1.0",
        "iteration": 2,
        "candidate_id": "CAND-R4-0002",
        "candidate_order": certificate["actual_order"],
        "first_failed_gate": "global_systole",
        "classification": "EXACT_GLOBAL_COUNTEREXAMPLE_REGISTERED",
        "witness_id": witness_id,
        "witness_orbit_id": orbit_id,
        "known_separator_factors": known,
        "next_action": "evaluate actual order of strict separator refinements before admitting CAND-R4-0003",
        "hpc_escalation_triggered": False,
        "candidate_certificate_sha256": file_hash(CERT),
        "witness_ledger_sha256": file_hash(WITNESS_LEDGER),
        "danger_registry_sha256": file_hash(DANGER_REGISTRY),
        "separator_matrix_sha256": file_hash(SEPARATOR_MATRIX),
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
