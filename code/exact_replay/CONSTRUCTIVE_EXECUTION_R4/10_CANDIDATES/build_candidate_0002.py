"""Construct the p=3 arithmetic x mod-2 homology actual subdirect image."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from collections import deque
from pathlib import Path

from production_code.group.universal_cover import enumerate_ball


arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0002.certificate.json"
LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
P = 3

Element = tuple[int, ...]
H_GENERATORS = (1, 2, 7, 11, 1, 2, 7, 11)
PHI_H_BASIS = (2, 7, 14, 4)


def hphi(value: int) -> int:
    result = 0
    for bit, image in enumerate(PHI_H_BASIS):
        if value & (1 << bit):
            result ^= image
    return result


def identity() -> Element:
    return arith.aidentity(P) + (0,)


def generator(index: int) -> Element:
    return arith.generator(index, P) + (H_GENERATORS[index],)


def multiply(left: Element, right: Element) -> Element:
    return arith.amul(left[:8], right[:8], P) + (left[8] ^ right[8],)


def phi(value: Element) -> Element:
    return arith.sigma(value[:8], P) + (hphi(value[8]),)


def word_image(word: tuple[str, ...]) -> Element:
    result = identity()
    for token in word:
        result = multiply(result, generator(int(token[1])))
    return result


def enumerate_image(maximum_order: int = 50_000) -> list[Element]:
    start = identity()
    elements = [start]
    seen = {start}
    queue = deque([start])
    generators = tuple(generator(index) for index in range(8))
    while queue:
        source = queue.popleft()
        for image in generators:
            target = multiply(source, image)
            if target in seen:
                continue
            if len(elements) >= maximum_order:
                raise RuntimeError("candidate 0002 exceeded frozen order ceiling")
            seen.add(target)
            elements.append(target)
            queue.append(target)
    return elements


def marked_hash(elements: list[Element]) -> str:
    payload = {
        "construction": "actual image of (rho_arithmetic_p3,H1_mod2)",
        "generators": [list(generator(index)) for index in range(8)],
        "actual_order": len(elements),
        "elements_sha256": hashlib.sha256(
            json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")
        ).hexdigest().upper(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def rewrite_ledger(certificate: dict) -> None:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    row = {
        "Candidate ID": certificate["candidate_id"],
        "Parent Candidate": "NONE_NONNESTED_RESTART",
        "Construction family": "arithmetic p=3 actual image with H1(Gamma;F2)",
        "Parameters": "p=3; homology modulus=2",
        "Factor IDs": "ARITH-P3-6F6FBFF4038772DA,H1-F2-RANK4",
        "Marked quotient hash": certificate["marked_quotient_hash"],
        "|Q|": str(certificate["actual_order"]),
        "Minimum known faithful degree": "UNVERIFIED",
        "C8 status": "PASS",
        "Parity status": "PASS",
        "Shell status": "PASS",
        "Local status": certificate["gates"]["local_B_geom_3"],
        "Based status": "NOT_RUN",
        "Global status": "NOT_RUN" if certificate["gates"]["local_B_geom_3"] == "PASS" else "NOT_RUN_GATE_ORDER",
        "Shortest failure witness": "",
        "Witness orbit ID": "",
        "Resource estimate": json.dumps(certificate["resource"], separators=(",", ":")),
        "Resource status": "PASS_CONSTRUCTION_ONLY",
        "Representation status": "NOT_REQUESTED",
        "Final disposition": "ACTIVE_GLOBAL_PENDING" if certificate["gates"]["local_B_geom_3"] == "PASS" else "REJECTED_LOCAL_COLLISION_PENDING_WITNESS",
        "Certificate hash": hashlib.sha256(CERT.read_bytes()).hexdigest().upper(),
    }
    rows = [existing for existing in rows if existing["Candidate ID"] != row["Candidate ID"]]
    rows.append(row)
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    elements = enumerate_image()
    shell = tuple(generator(index) for index in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball = enumerate_ball(3)
    distinct_images = len({word_image(element.representative) for element in ball.elements})
    certificate = {
        "schema_version": "1.0",
        "candidate_id": "CAND-R4-0002",
        "parent_candidate": None,
        "restart_reason": "every strict refinement of order-31200 CAND-R4-0001 exceeds the order ceiling",
        "construction": "actual generated image of (rho_arithmetic_p3,H1(Gamma_B;F2))",
        "factor_ids": ["ARITH-P3-6F6FBFF4038772DA", "H1-F2-RANK4"],
        "actual_order": len(elements),
        "order_window": [2338, 50000],
        "marked_quotient_hash": marked_hash(elements),
        "homology": {
            "basis": ["a1", "b1", "a2", "b2"],
            "physical_generator_codes": list(H_GENERATORS),
            "phi8_basis_codes": list(PHI_H_BASIS),
            "parity_function": "sum of four F2 coordinates",
        },
        "gates": {
            "surface_relation": word_image(relator) == identity(),
            "generation": True,
            "order_interval": 2338 <= len(elements) <= 50000,
            "C8_covariance": all(phi(shell[index]) == shell[(index + 1) % 8] for index in range(8)),
            "C8_exact_order": len(set(shell)) == 8,
            "parity": all((generator[8].bit_count() % 2) == 1 for generator in shell),
            "physical_shell_distinct_nonidentity": len(set(shell)) == 8 and identity() not in shell,
            "local_B_geom_3": "PASS" if distinct_images == len(ball.elements) == 457 else "FAIL",
            "based": "NOT_RUN",
            "global_systole": "NOT_RUN",
        },
        "local_ball": {"exact_elements": len(ball.elements), "distinct_candidate_images": distinct_images},
        "resource": {"enumerated_candidate_elements": len(elements), "frozen_order_ceiling": 50000},
        "classification": "LOCAL_PASS_GLOBAL_PENDING" if distinct_images == 457 else "LOCAL_FAIL",
    }
    structural = ["surface_relation", "generation", "order_interval", "C8_covariance", "C8_exact_order", "parity", "physical_shell_distinct_nonidentity"]
    if not all(certificate["gates"][key] is True for key in structural):
        raise RuntimeError(f"candidate 0002 structural failure: {certificate['gates']}")
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    rewrite_ledger(certificate)


if __name__ == "__main__":
    main()
