"""Finalize CAND-R4-0003 at its exact global-systole failure."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from functools import lru_cache
from pathlib import Path

import sympy as sp

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, field_to_sympy, matrix_from_word


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0003")
candidate.selected_rows = lru_cache(maxsize=1)(candidate.selected_rows)
candidate.q_rotation = lru_cache(maxsize=1)(candidate.q_rotation)
arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
p2 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0003.certificate.json"
SCAN = R4 / "10_CANDIDATES" / "CAND-R4-0003.global_witness-v2.tsv"
CHECKPOINT = R4 / "checkpoints" / "CAND-R4-0003-axis6-v2.tsv"
MANIFEST = R4 / "00_FROZEN_INPUTS" / "manifests" / "axis6_exact_ball_manifest.json"
SCANNER = R4 / "10_CANDIDATES" / "scan_candidate_0003_axis6_v2.cpp"
EXECUTABLE = R4 / "10_CANDIDATES" / "scan_candidate_0003_axis6_v2.exe"
DANGER_REGISTRY = R4 / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
WITNESS_LEDGER = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
SEPARATOR_MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
SEPARATOR_LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"
CANDIDATE_LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
ITERATION = R4 / "09_CEGAR" / "ITERATION_0003_GLOBAL_REJECTION.json"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def exact_witness() -> dict:
    with SCAN.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 1:
        raise RuntimeError("expected one candidate-0003 global scan witness")
    row = rows[0]
    source = tuple(row["word"].split())
    word = d0.canonical_c8_inverse_word(source)
    image = candidate.word_image(word)
    if image != candidate.identity():
        raise RuntimeError("scanner witness is not in candidate-0003 kernel")
    matrix = matrix_from_word(word)
    key = projective_key(matrix)
    if key == projective_key(IDENTITY_MATRIX):
        raise RuntimeError("scanner witness is identity in Gamma_B")
    payload = json.dumps(key, separators=(",", ":"))
    key_hash = hashlib.sha256(payload.encode("ascii")).hexdigest().upper()
    a = matrix[0]
    if a[3] or a[4] or a[1] > 0 or a[2] > 0:
        raise RuntimeError("unexpected real half-trace branch")
    absolute = -sp.re(field_to_sympy(a)).expand()
    cutoff = 2405 + 1700 * sp.sqrt(2)
    margin = sp.expand(cutoff - absolute)
    delta = sp.expand(absolute**2 - cutoff**2)
    if margin.is_positive is not True or delta.is_negative is not True:
        raise RuntimeError("strict trace cutoff was not certified")
    scanner_coeffs = tuple(int(row[f"re_c{i}"]) for i in range(4))
    if int(row["exponent"]) != a[0] or scanner_coeffs != tuple(a[1:5]):
        raise RuntimeError("scanner/full exact trace mismatch")
    return {
        "witness_id": f"W-{key_hash[:20]}",
        "canonical_word": list(word),
        "source_word": list(source),
        "record_index_zero_based": int(row["record_index"]),
        "record_depth": int(row["depth"]),
        "candidate_image": list(image),
        "candidate_image_identity": True,
        "nonidentity_in_Gamma_B": True,
        "exact_group_key": payload,
        "exact_group_key_sha256": key_hash,
        "global_type": "D_global(6a_B)",
        "universal_class2_image": list(p2.word_full_geometric(word)),
        "half_trace_absolute_expression": str(absolute),
        "cutoff_cosh_3aB_over_R": "2405 + 1700*sqrt(2)",
        "strict_positive_cutoff_margin": str(margin),
        "squared_cutoff_delta": str(delta),
        "translation_length_over_a_B": f"acosh({absolute})/acosh(1+sqrt(2))",
        "boundary_policy": "equality is dangerous; this witness is strictly below the cutoff",
        "early_exit_scope": "first dangerous kernel hit in canonical registry order",
        "registry_manifest": "00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json",
        "registry_manifest_sha256": file_hash(MANIFEST),
        "scanner_source": "10_CANDIDATES/scan_candidate_0003_axis6_v2.cpp",
        "scanner_source_sha256": file_hash(SCANNER),
        "scanner_executable_sha256": file_hash(EXECUTABLE),
        "scanner_checkpoint_sha256": file_hash(CHECKPOINT),
        "scanner_witness_sha256": file_hash(SCAN),
    }


def factor_value(factor: dict[str, str], word: tuple[str, ...]) -> int:
    if factor["factor_id"].startswith("ARITH-P"):
        prime = int(factor["parameters"].split("p=", 1)[1].split(";", 1)[0])
        return int(arith.word_image(word, prime) != arith.aidentity(prime))
    if factor["factor_id"].startswith("P2C2-C8-D1-"):
        return int(p2.q_word(word, (19,)) != (0, 0))
    raise RuntimeError(f"unknown separator family: {factor['factor_id']}")


def register(witness: dict) -> tuple[str, str, list[str]]:
    word = tuple(witness["canonical_word"])
    witness_id = witness["witness_id"]
    orbit_id = f"C8-{hashlib.sha256(' '.join(word).encode('ascii')).hexdigest().upper()[:20]}"
    with DANGER_REGISTRY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); fields = list(reader.fieldnames or []); rows = list(reader)
    danger_id = f"DGLOBAL-R6-C0003-{witness_id}"
    if not any(row["danger_id"] == danger_id for row in rows):
        rows.append({
            "danger_id": danger_id, "type": "D_global(6a_B)",
            "constraint_word_geometric": " ".join(word), "canonical_word_geometric": " ".join(word),
            "canonical_word_standard": " ".join(d0.standard_word(word)),
            "exact_group_key": witness["exact_group_key"], "exact_group_key_sha256": witness["exact_group_key_sha256"],
            "witness_id": witness_id, "word_depth": str(len(word)), "based_displacement_over_a_B": "",
            "translation_length_over_a_B": witness["translation_length_over_a_B"], "translation_length_interval": "STRICTLY_LESS_THAN_6",
            "c8_orbit_id": orbit_id, "legacy_source_orbit_id": "", "nonidentity_in_Gamma_B": "PASS_EXACT_KEY",
            "geometry_status": "PASS_EXACT_TRACE_STRICT", "geometry_statement": "kernel element has translation length strictly less than 6*a_B",
            "source_certificate": "10_CANDIDATES/CAND-R4-0003.certificate.json", "registry_status": "ACTIVE_CEGAR",
        })
        write_tsv(DANGER_REGISTRY, fields, sorted(rows, key=lambda item: item["danger_id"]))

    with SEPARATOR_LIBRARY.open(encoding="utf-8", newline="") as handle:
        factors = list(csv.DictReader(handle, delimiter="\t"))
    values = {factor["factor_id"]: str(factor_value(factor, word)) for factor in factors}
    known = [factor["factor_id"] for factor in factors if values[factor["factor_id"]] == "1"]
    with WITNESS_LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); wfields = list(reader.fieldnames or []); wrows = list(reader)
    if not any(row["Witness ID"] == witness_id for row in wrows):
        wrows.append({
            "Witness ID": witness_id, "Canonical word": " ".join(word), "Exact group key": witness["exact_group_key"],
            "Type": "D_global(6a_B)", "Word depth": str(len(word)), "Based displacement if relevant": "",
            "Translation length interval/exact expression": witness["translation_length_over_a_B"], "C8 orbit ID": orbit_id,
            "First candidate killed": "CAND-R4-0003", "Separator factors known": ",".join(known),
            "Currently separated by candidate": "NO", "Certificate path": "10_CANDIDATES/CAND-R4-0003.certificate.json",
        })
        write_tsv(WITNESS_LEDGER, wfields, sorted(wrows, key=lambda item: item["Witness ID"]))
    with SEPARATOR_MATRIX.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); mfields = list(reader.fieldnames or []); mrows = list(reader)
    if not any(row["witness_id"] == witness_id for row in mrows):
        mrows.append({"witness_id": witness_id, **values})
        write_tsv(SEPARATOR_MATRIX, mfields, sorted(mrows, key=lambda item: item["witness_id"]))
    return witness_id, orbit_id, known


def update_candidate(certificate: dict, witness_id: str, orbit_id: str) -> None:
    with CANDIDATE_LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); fields = list(reader.fieldnames or []); rows = list(reader)
    for row in rows:
        if row["Candidate ID"] == "CAND-R4-0003":
            row["Based status"] = "NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"
            row["Global status"] = "FAIL_EARLY_EXACT_WITNESS"
            row["Shortest failure witness"] = witness_id
            row["Witness orbit ID"] = orbit_id
            row["Resource estimate"] = json.dumps(certificate["resource"], separators=(",", ":"))
            row["Final disposition"] = "REJECTED_GLOBAL_WITNESS"
            row["Certificate hash"] = file_hash(CERT)
            break
    else:
        raise RuntimeError("candidate-0003 ledger row absent")
    write_tsv(CANDIDATE_LEDGER, fields, rows)


def main() -> None:
    certificate = json.loads(CERT.read_text(encoding="utf-8"))
    if certificate["classification"] != "LOCAL_PASS_GLOBAL_PENDING":
        raise RuntimeError("candidate 0003 is not global-pending")
    witness = exact_witness()
    certificate["schema_version"] = "1.1"
    certificate["gates"]["based"] = "NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"
    certificate["gates"]["global_systole"] = "FAIL_EARLY_EXACT_WITNESS"
    certificate["global_failure_witness"] = witness
    certificate["resource"].update({
        "global_registry_total_records": 785_639_753,
        "global_registry_scanned_records": 2_488_106,
        "global_scan_early_exit": True,
        "global_scan_elapsed_seconds": 0.52153,
    })
    certificate["classification"] = "REJECTED_GLOBAL_WITNESS"
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    witness_id, orbit_id, known = register(witness)
    update_candidate(certificate, witness_id, orbit_id)
    ITERATION.write_text(json.dumps({
        "schema_version": "1.0", "iteration": 3, "candidate_id": "CAND-R4-0003",
        "candidate_order": certificate["actual_order"], "first_failed_gate": "global_systole",
        "classification": "EXACT_GLOBAL_COUNTEREXAMPLE_REGISTERED", "witness_id": witness_id,
        "witness_orbit_id": orbit_id, "known_separator_factors": known,
        "universal_class2_image": witness["universal_class2_image"],
        "next_action": "search C8-stable dimension-two central quotient containing the dimension-one row space",
        "hpc_escalation_triggered": False, "candidate_certificate_sha256": file_hash(CERT),
        "witness_ledger_sha256": file_hash(WITNESS_LEDGER), "danger_registry_sha256": file_hash(DANGER_REGISTRY),
        "separator_matrix_sha256": file_hash(SEPARATOR_MATRIX),
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
