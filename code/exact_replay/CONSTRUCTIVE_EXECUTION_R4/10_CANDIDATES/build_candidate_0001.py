"""Build and gate the first window-admissible Constructive R4 candidate."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from collections import deque
from pathlib import Path

from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, enumerate_ball, matrix_from_word

arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
d0 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")


ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
P = 5
SOURCE_CERT = ROOT / "production_code" / "group" / "SL2_25_C8_FAMILY_CERTIFICATE.json"
CANDIDATE_CERT = R4 / "10_CANDIDATES" / "CAND-R4-0001.certificate.json"
CANDIDATE_LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
DANGER_REGISTRY = R4 / "02_DANGEROUS_SETS" / "DANGEROUS_SET_REGISTRY.tsv"
WITNESS_LEDGER = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
SEPARATOR_MATRIX = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_MATRIX.tsv"
SEPARATOR_LIBRARY = R4 / "03_SEPARATOR_LIBRARY" / "SEPARATOR_LIBRARY.tsv"

CandidateElement = tuple[int, ...]


def cidentity() -> CandidateElement:
    return arith.aidentity(P) + (0,)


def cg(index: int) -> CandidateElement:
    return arith.generator(index, P) + (1,)


def cmul(left: CandidateElement, right: CandidateElement) -> CandidateElement:
    return arith.amul(left[:8], right[:8], P) + ((left[8] + right[8]) % 2,)


def csigma(value: CandidateElement) -> CandidateElement:
    return arith.sigma(value[:8], P) + (value[8],)


def cword(word: tuple[str, ...]) -> CandidateElement:
    result = cidentity()
    for token in word:
        result = cmul(result, cg(int(token[1])))
    return result


def enumerate_candidate(maximum_order: int = 50_000) -> list[CandidateElement]:
    identity = cidentity()
    elements = [identity]
    lookup = {identity: 0}
    queue = deque([identity])
    generators = tuple(cg(index) for index in range(8))
    while queue:
        source = queue.popleft()
        for generator in generators:
            target = cmul(source, generator)
            if target in lookup:
                continue
            if len(elements) >= maximum_order:
                raise RuntimeError(f"candidate exceeded frozen order ceiling {maximum_order}")
            lookup[target] = len(elements)
            elements.append(target)
            queue.append(target)
    return elements


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def q2_sign(pair: tuple[int, int]) -> int:
    a, b = pair
    if a == 0 and b == 0:
        return 0
    if a >= 0 and b >= 0:
        return 1
    if a <= 0 and b <= 0:
        return -1
    comparison = a * a - 2 * b * b
    if comparison == 0:
        raise AssertionError("unexpected rational square root of two")
    if a > 0:
        return 1 if comparison > 0 else -1
    return -1 if comparison > 0 else 1


def q2_absolute(pair: tuple[int, int]) -> tuple[int, int]:
    return pair if q2_sign(pair) >= 0 else (-pair[0], -pair[1])


def trace_witness(word: tuple[str, ...]) -> dict:
    matrix = matrix_from_word(word)
    if projective_key(matrix) == projective_key(IDENTITY_MATRIX):
        raise AssertionError("legacy word is identity in Gamma_B")
    a = matrix[0]
    if any(a[index] for index in (3, 4, 5, 6, 7, 8)):
        raise AssertionError("half trace escaped Q(sqrt(2))")
    half_trace = (a[1], a[2])
    absolute = q2_absolute(half_trace)
    scale = 1 << a[0]
    difference = (2405 * scale - absolute[0], 1700 * scale - absolute[1])
    if q2_sign(difference) <= 0:
        raise AssertionError("candidate word is not strictly below the global 6a_B cutoff")
    payload = json.dumps(projective_key(matrix), separators=(",", ":"))
    return {
        "exact_group_key": payload,
        "exact_group_key_sha256": hashlib.sha256(payload.encode("ascii")).hexdigest().upper(),
        "half_trace_Qsqrt2": {
            "denominator_power_of_two": a[0],
            "coefficients": list(half_trace),
            "absolute_coefficients": list(absolute),
        },
        "strict_cutoff_test": f"(2405+1700*sqrt(2))-|tr/2| is positive exactly in Q(sqrt(2))",
        "translation_length_expression": (
            f"acosh(abs(({half_trace[0]}+{half_trace[1]}*sqrt(2))/2^{a[0]}))"
            "/acosh(1+sqrt(2))"
        ),
    }


def find_early_global_witness() -> dict:
    source = json.loads(SOURCE_CERT.read_text(encoding="utf-8"))
    words = {
        tuple(row["geometric_word"]): row
        for row in source["global_rejection"]["witnesses"]
    }
    hits = []
    for source_word, source_row in words.items():
        canonical = d0.canonical_c8_inverse_word(source_word)
        if cword(canonical) != cidentity():
            continue
        exact = trace_witness(canonical)
        hits.append((len(canonical), canonical, source_word, source_row, exact))
    if not hits:
        raise RuntimeError("no replayable early global witness found")
    _, canonical, source_word, source_row, exact = min(hits, key=lambda row: (row[0], row[1]))
    return {
        "canonical_word": list(canonical),
        "source_word": list(source_word),
        "source_certificate": str(SOURCE_CERT.relative_to(ROOT)).replace("\\", "/"),
        "source_certificate_sha256": file_hash(SOURCE_CERT),
        "source_seed_representative": source_row["seed_representative"],
        "candidate_image": list(cword(canonical)),
        "candidate_image_identity": True,
        "nonidentity_in_Gamma_B": True,
        "global_type": "D_global(6a_B)",
        **exact,
    }


def marked_hash(elements: list[CandidateElement]) -> str:
    payload = {
        "construction": "actual image of (rho_arith_p5,chi)",
        "generators": [list(cg(index)) for index in range(8)],
        "actual_order": len(elements),
        "elements_sha256": hashlib.sha256(
            json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")
        ).hexdigest().upper(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def rewrite_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_global_witness(witness: dict, candidate_id: str) -> str:
    canonical = tuple(witness["canonical_word"])
    key_hash = witness["exact_group_key_sha256"]
    witness_id = f"W-{key_hash[:20]}"
    orbit_id = f"C8-{hashlib.sha256(' '.join(canonical).encode('ascii')).hexdigest().upper()[:20]}"
    with DANGER_REGISTRY.open(encoding="utf-8", newline="") as handle:
        danger_rows = list(csv.DictReader(handle, delimiter="\t"))
        fields = list(danger_rows[0])
    danger_id = f"DGLOBAL-C0001-{witness_id}"
    if not any(row["danger_id"] == danger_id for row in danger_rows):
        danger_rows.append({
            "danger_id": danger_id,
            "type": "D_global(6a_B)",
            "constraint_word_geometric": " ".join(canonical),
            "canonical_word_geometric": " ".join(canonical),
            "canonical_word_standard": " ".join(d0.standard_word(canonical)),
            "exact_group_key": witness["exact_group_key"],
            "exact_group_key_sha256": key_hash,
            "witness_id": witness_id,
            "word_depth": str(len(canonical)),
            "based_displacement_over_a_B": "",
            "translation_length_over_a_B": witness["translation_length_expression"],
            "translation_length_interval": "",
            "c8_orbit_id": orbit_id,
            "legacy_source_orbit_id": "",
            "nonidentity_in_Gamma_B": "PASS_EXACT_KEY",
            "geometry_status": "PASS_EXACT_TRACE_BOUND",
            "geometry_statement": "exact |tr|/2 < cosh(3*a_B/R), hence translation length < 6*a_B",
            "source_certificate": "10_CANDIDATES/CAND-R4-0001.certificate.json",
            "registry_status": "ACTIVE_CEGAR",
        })
        rewrite_tsv(DANGER_REGISTRY, fields, sorted(danger_rows, key=lambda row: row["danger_id"]))

    with WITNESS_LEDGER.open(encoding="utf-8", newline="") as handle:
        ledger_rows = list(csv.DictReader(handle, delimiter="\t"))
        ledger_fields = list(ledger_rows[0])
    if not any(row["Witness ID"] == witness_id for row in ledger_rows):
        ledger_rows.append({
            "Witness ID": witness_id,
            "Canonical word": " ".join(canonical),
            "Exact group key": witness["exact_group_key"],
            "Type": "D_global(6a_B)",
            "Word depth": str(len(canonical)),
            "Based displacement if relevant": "",
            "Translation length interval/exact expression": witness["translation_length_expression"],
            "C8 orbit ID": orbit_id,
            "First candidate killed": candidate_id,
            "Separator factors known": "",
            "Currently separated by candidate": "NO",
            "Certificate path": "10_CANDIDATES/CAND-R4-0001.certificate.json",
        })
        rewrite_tsv(WITNESS_LEDGER, ledger_fields, sorted(ledger_rows, key=lambda row: row["Witness ID"]))

    with SEPARATOR_LIBRARY.open(encoding="utf-8", newline="") as handle:
        factors = list(csv.DictReader(handle, delimiter="\t"))
    with SEPARATOR_MATRIX.open(encoding="utf-8", newline="") as handle:
        matrix_rows = list(csv.DictReader(handle, delimiter="\t"))
        matrix_fields = ["witness_id"] + [row["factor_id"] for row in factors]
    if not any(row["witness_id"] == witness_id for row in matrix_rows):
        new_row: dict[str, str | int] = {"witness_id": witness_id}
        known = []
        for factor in factors:
            p = int(factor["parameters"].split("p=", 1)[1].split(";", 1)[0])
            value = int(arith.word_image(canonical, p) != arith.aidentity(p))
            new_row[factor["factor_id"]] = value
            if value:
                known.append(factor["factor_id"])
        matrix_rows.append(new_row)
        rewrite_tsv(SEPARATOR_MATRIX, matrix_fields, sorted(matrix_rows, key=lambda row: row["witness_id"]))
        for row in ledger_rows:
            if row["Witness ID"] == witness_id:
                row["Separator factors known"] = ",".join(known)
        rewrite_tsv(WITNESS_LEDGER, ledger_fields, sorted(ledger_rows, key=lambda row: row["Witness ID"]))
    return witness_id


def append_candidate_ledger(certificate: dict, certificate_hash: str, witness_id: str) -> None:
    with CANDIDATE_LEDGER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
        fields = list(csv.DictReader(CANDIDATE_LEDGER.open(encoding="utf-8", newline=""), delimiter="\t").fieldnames or [])
    row = {
        "Candidate ID": certificate["candidate_id"],
        "Parent Candidate": "NONE",
        "Construction family": "arithmetic p=5 actual image with independent parity factor",
        "Parameters": "p=5; K=F5[s]/(s^2-2)",
        "Factor IDs": "ARITH-P5-C0CA0BF862D52B5A,PARITY-C2",
        "Marked quotient hash": certificate["marked_quotient_hash"],
        "|Q|": str(certificate["actual_order"]),
        "Minimum known faithful degree": "UNVERIFIED",
        "C8 status": "PASS",
        "Parity status": "PASS",
        "Shell status": "PASS",
        "Local status": "PASS_B_GEOM_3",
        "Based status": "NOT_REQUESTED",
        "Global status": "FAIL",
        "Shortest failure witness": witness_id,
        "Witness orbit ID": certificate["global_witness"]["exact_group_key_sha256"][:20],
        "Resource estimate": json.dumps(certificate["resource"], separators=(",", ":")),
        "Resource status": "PASS_CONSTRUCTION_ONLY",
        "Representation status": "UNVERIFIED_NOT_REQUESTED",
        "Final disposition": "REJECTED_GLOBAL_WITNESS",
        "Certificate hash": certificate_hash,
    }
    rows = [existing for existing in rows if existing["Candidate ID"] != row["Candidate ID"]]
    rows.append(row)
    rewrite_tsv(CANDIDATE_LEDGER, fields, rows)


def main() -> None:
    elements = enumerate_candidate()
    if len(elements) != 31_200:
        raise RuntimeError(f"unexpected actual subdirect order: {len(elements)}")
    identity = cidentity()
    shell = tuple(cg(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball3 = enumerate_ball(3)
    ball3_images = {cword(element.representative) for element in ball3.elements}
    global_witness = find_early_global_witness()
    certificate = {
        "schema_version": "1.0",
        "candidate_id": "CAND-R4-0001",
        "parent_candidate": None,
        "construction": "actual generated image of diagonal map (rho_arithmetic_p5, chi)",
        "factor_ids": ["ARITH-P5-C0CA0BF862D52B5A", "PARITY-C2"],
        "actual_order": len(elements),
        "order_window": [2338, 50000],
        "marked_quotient_hash": marked_hash(elements),
        "gates": {
            "surface_relation": cword(relator) == identity,
            "generation": True,
            "C8_covariance": all(csigma(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
            "C8_exact_order": len(set(shell)) == 8,
            "parity": all(generator[8] == 1 for generator in shell),
            "physical_shell_distinct_nonidentity": len(set(shell)) == 8 and identity not in shell,
            "local_B_geom_3_injective": len(ball3_images) == len(ball3.elements) == 457,
            "based": "NOT_REQUESTED",
            "global_systole": "FAIL_EARLY_EXACT_WITNESS",
        },
        "global_witness": global_witness,
        "resource": {
            "enumerated_candidate_elements": len(elements),
            "frozen_order_ceiling": 50000,
            "large_global_registry_rescanned": False,
            "early_exit_used": True,
        },
        "classification": "REJECTED_GLOBAL_WITNESS",
    }
    if not all(value is True for key, value in certificate["gates"].items() if key not in {"based", "global_systole"}):
        raise RuntimeError(f"mandatory pre-global gate failed: {certificate['gates']}")
    CANDIDATE_CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    witness_id = add_global_witness(global_witness, certificate["candidate_id"])
    append_candidate_ledger(certificate, file_hash(CANDIDATE_CERT), witness_id)


if __name__ == "__main__":
    main()
