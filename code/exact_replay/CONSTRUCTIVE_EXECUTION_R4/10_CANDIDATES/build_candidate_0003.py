"""Build CAND-R4-0003 as the actual p3 x marginal-p2 subdirect image."""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
from collections import deque
from pathlib import Path

from production_code.group.universal_cover import enumerate_ball


arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
p2 = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
P2_CERT = R4 / "05_P_QUOTIENT" / "P2C2_C8_MARGINAL_SEPARATOR.certificate.json"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0003.certificate.json"
LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
WITNESSES = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
P = 3

Element = tuple[int, ...]


def selected_rows() -> tuple[int, ...]:
    return tuple(json.loads(P2_CERT.read_text(encoding="utf-8"))["construction"]["selected_dual_row_space_integers"])


def q_rotation() -> dict[p2.QuotientElement, p2.QuotientElement]:
    _, rotation = p2.enumerate_q(selected_rows())
    if rotation is None:
        raise RuntimeError("marginal p2 rotation is not well-defined")
    return rotation


def identity() -> Element:
    return arith.aidentity(P) + (0, 0)


def generator(index: int) -> Element:
    return arith.generator(index, P) + p2.q_physical_generators(selected_rows())[index]


def multiply(left: Element, right: Element) -> Element:
    rows = selected_rows()
    return arith.amul(left[:8], right[:8], P) + p2.q_multiply(left[8:], right[8:], rows)


def phi(value: Element) -> Element:
    return arith.sigma(value[:8], P) + q_rotation()[value[8:]]


def word_image(word: tuple[str, ...]) -> Element:
    result = identity()
    generators = tuple(generator(i) for i in range(8))
    for token in word:
        result = multiply(result, generators[int(token[1])])
    return result


def enumerate_image(maximum_order: int = 50_000) -> list[Element]:
    one = identity()
    generators = tuple(generator(i) for i in range(8))
    seen = {one}
    elements = [one]
    queue = deque([one])
    while queue:
        source = queue.popleft()
        for image in generators:
            target = multiply(source, image)
            if target in seen:
                continue
            if len(elements) >= maximum_order:
                raise RuntimeError("candidate 0003 exceeded frozen order ceiling")
            seen.add(target)
            elements.append(target)
            queue.append(target)
    return elements


def marked_hash(elements: list[Element]) -> str:
    payload = {
        "construction": "actual image of (rho_arithmetic_p3,p2c2_c8_d1)",
        "generators": [list(generator(i)) for i in range(8)],
        "actual_order": len(elements),
        "elements_sha256": hashlib.sha256(json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")).hexdigest().upper(),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def write_ledger(certificate: dict) -> None:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    row = {
        "Candidate ID": "CAND-R4-0003",
        "Parent Candidate": "CAND-R4-0002_STRICT_REFINEMENT",
        "Construction family": "actual subdirect image of arithmetic p=3 and C8-stable class-2 p=2 marginal separator",
        "Parameters": "p=3; p2 class=2; central quotient dimension=1",
        "Factor IDs": "ARITH-P3-6F6FBFF4038772DA,P2C2-C8-D1-7114D44C79829117",
        "Marked quotient hash": certificate["marked_quotient_hash"],
        "|Q|": str(certificate["actual_order"]),
        "Minimum known faithful degree": "UNVERIFIED",
        "C8 status": "PASS",
        "Parity status": "PASS",
        "Shell status": "PASS",
        "Local status": certificate["gates"]["local_B_geom_3"],
        "Based status": "NOT_RUN",
        "Global status": "NOT_RUN",
        "Shortest failure witness": "",
        "Witness orbit ID": "",
        "Resource estimate": json.dumps(certificate["resource"], separators=(",", ":")),
        "Resource status": "PASS_CONSTRUCTION_ONLY",
        "Representation status": "NOT_REQUESTED",
        "Final disposition": "ACTIVE_GLOBAL_PENDING",
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
    shell = tuple(generator(i) for i in range(8))
    relator = tuple(f"g{i}" for i in (0, 5, 2, 7, 4, 1, 6, 3))
    ball = enumerate_ball(3)
    distinct_local = len({word_image(element.representative) for element in ball.elements})
    with WITNESSES.open(encoding="utf-8", newline="") as handle:
        witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    accumulated = {
        row["Witness ID"]: word_image(tuple(row["Canonical word"].split())) != identity()
        for row in witness_rows
    }
    phi_orders = []
    for element in elements:
        image = element
        least = None
        for power in range(1, 9):
            image = phi(image)
            if image == element:
                least = power
                break
        phi_orders.append(least)
    certificate = {
        "schema_version": "1.0",
        "candidate_id": "CAND-R4-0003",
        "parent_candidate": "CAND-R4-0002",
        "kernel_relation": "ker(CAND-R4-0003) is the strict intersection of ker(rho_p3) and ker(P2C2-C8-D1)",
        "construction": "actual generated diagonal image of arithmetic p=3 and the C8-stable class-2 p=2 marginal separator",
        "factor_ids": ["ARITH-P3-6F6FBFF4038772DA", "P2C2-C8-D1-7114D44C79829117"],
        "actual_order": len(elements),
        "order_window": [2338, 50000],
        "marked_quotient_hash": marked_hash(elements),
        "gates": {
            "surface_relation": word_image(relator) == identity(),
            "generation": True,
            "order_interval": 2338 <= len(elements) <= 50000,
            "C8_covariance": all(phi(shell[i]) == shell[(i + 1) % 8] for i in range(8)),
            "C8_exact_order": 8 in phi_orders,
            "parity": all((element[8].bit_count() & 1) == 1 for element in shell),
            "physical_shell_distinct_nonidentity": len(set(shell)) == 8 and identity() not in shell,
            "local_B_geom_3": "PASS" if distinct_local == 457 else "FAIL",
            "based": "NOT_RUN",
            "global_systole": "NOT_RUN",
        },
        "local_ball": {"exact_elements": len(ball.elements), "distinct_candidate_images": distinct_local},
        "accumulated_witness_invariant": {
            "witness_count": len(accumulated),
            "all_separated": all(accumulated.values()),
            "rows": accumulated,
        },
        "resource": {
            "enumerated_candidate_elements": len(elements),
            "frozen_order_ceiling": 50000,
            "cartesian_product_order_used_as_actual_order": False,
            "hpc_escalation_triggered": False,
        },
        "classification": "LOCAL_PASS_GLOBAL_PENDING" if distinct_local == 457 and all(accumulated.values()) else "REJECTED_PRE_GLOBAL",
    }
    required = ("surface_relation", "generation", "order_interval", "C8_covariance", "C8_exact_order", "parity", "physical_shell_distinct_nonidentity")
    if not all(certificate["gates"][key] is True for key in required):
        raise RuntimeError(f"candidate 0003 structural failure: {certificate['gates']}")
    if certificate["classification"] != "LOCAL_PASS_GLOBAL_PENDING":
        raise RuntimeError("candidate 0003 failed local or accumulated-witness invariants")
    CERT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    write_ledger(certificate)


if __name__ == "__main__":
    main()
