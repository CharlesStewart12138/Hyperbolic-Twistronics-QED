"""Build the dimension-two class-2 refinement CAND-R4-0005."""

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
ROOT = Path(__file__).resolve().parents[2]; R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
CERT = R4 / "10_CANDIDATES" / "CAND-R4-0005.certificate.json"
LEDGER = R4 / "10_CANDIDATES" / "CANDIDATE_LEDGER.tsv"
WITNESSES = R4 / "09_CEGAR" / "WITNESS_LEDGER.tsv"
ROWS = (6, 9); P = 3
Q_ELEMENTS, Q_ROTATION = p2.enumerate_q(ROWS)
if Q_ROTATION is None or len(Q_ELEMENTS) != 64: raise RuntimeError("invalid frozen D2 factor")
Q_PHYSICAL = p2.q_physical_generators(ROWS)


def identity(): return arith.aidentity(P) + (0, 0)
def generator(index): return arith.generator(index, P) + Q_PHYSICAL[index]
def multiply(left, right): return arith.amul(left[:8], right[:8], P) + p2.q_multiply(left[8:], right[8:], ROWS)
def phi(value): return arith.sigma(value[:8], P) + Q_ROTATION[value[8:]]


def word_image(word):
    result = identity(); generators = tuple(generator(i) for i in range(8))
    for token in word: result = multiply(result, generators[int(token[1])])
    return result


def enumerate_image(maximum_order=50_000):
    one = identity(); generators = tuple(generator(i) for i in range(8)); seen = {one}; elements = [one]; queue = deque([one])
    while queue:
        source = queue.popleft()
        for image in generators:
            target = multiply(source, image)
            if target in seen: continue
            if len(elements) >= maximum_order: raise RuntimeError("candidate 0005 exceeded frozen order ceiling")
            seen.add(target); elements.append(target); queue.append(target)
    return elements


def marked_hash(elements):
    payload = {"construction": "actual image of (rho_arithmetic_p3,p2c2_c8_d2)", "generators": [list(generator(i)) for i in range(8)],
               "actual_order": len(elements), "elements_sha256": hashlib.sha256(json.dumps(sorted(elements), separators=(",", ":")).encode("ascii")).hexdigest().upper()}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest().upper()


def write_ledger(certificate):
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t"); fields = list(reader.fieldnames or []); rows = list(reader)
    row = {
        "Candidate ID": "CAND-R4-0005", "Parent Candidate": "CAND-R4-0002_NONNESTED_D2_RESTART",
        "Construction family": "actual subdirect image of arithmetic p=3 and C8-stable class-2 p=2 nonnested D2 branch",
        "Parameters": "p=3; p2 class=2; central quotient dimension=2", "Factor IDs": "ARITH-P3-6F6FBFF4038772DA,P2C2-C8-D2-1D16194A8DBB81E2",
        "Marked quotient hash": certificate["marked_quotient_hash"], "|Q|": str(certificate["actual_order"]),
        "Minimum known faithful degree": "UNVERIFIED", "C8 status": "PASS", "Parity status": "PASS", "Shell status": "PASS",
        "Local status": certificate["gates"]["local_B_geom_3"], "Based status": "NOT_RUN", "Global status": "NOT_RUN",
        "Shortest failure witness": "", "Witness orbit ID": "", "Resource estimate": json.dumps(certificate["resource"], separators=(",", ":")),
        "Resource status": "PASS_CONSTRUCTION_ONLY", "Representation status": "NOT_REQUESTED", "Final disposition": "ACTIVE_GLOBAL_PENDING",
        "Certificate hash": hashlib.sha256(CERT.read_bytes()).hexdigest().upper(),
    }
    rows = [old for old in rows if old["Candidate ID"] != row["Candidate ID"]] + [row]
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)


def main():
    elements = enumerate_image(); shell = tuple(generator(i) for i in range(8)); relator = tuple(f"g{i}" for i in (0,5,2,7,4,1,6,3))
    ball = enumerate_ball(3); local_count = len({word_image(e.representative) for e in ball.elements})
    with WITNESSES.open(encoding="utf-8", newline="") as handle: witness_rows = list(csv.DictReader(handle, delimiter="\t"))
    accumulated = {row["Witness ID"]: word_image(tuple(row["Canonical word"].split())) != identity() for row in witness_rows}
    eighth = all(_iterate_phi(element, 8) == element for element in elements)
    exact8 = eighth and any(_iterate_phi(element, 4) != element for element in elements)
    certificate = {
        "schema_version": "1.0", "candidate_id": "CAND-R4-0005", "parent_candidate": "CAND-R4-0002",
        "kernel_relation": "nonnested strict refinement of CAND-R4-0002 using D2 row space <6,9>",
        "construction": "actual generated diagonal image of arithmetic p=3 and C8-stable class-2 nonnested D2 separator",
        "factor_ids": ["ARITH-P3-6F6FBFF4038772DA", "P2C2-C8-D2-1D16194A8DBB81E2"],
        "actual_order": len(elements), "order_window": [2338,50000], "marked_quotient_hash": marked_hash(elements),
        "gates": {"surface_relation": word_image(relator) == identity(), "generation": True, "order_interval": 2338 <= len(elements) <= 50000,
                  "C8_covariance": all(phi(shell[i]) == shell[(i+1)%8] for i in range(8)), "C8_exact_order": exact8,
                  "parity": all((element[8].bit_count()&1)==1 for element in shell),
                  "physical_shell_distinct_nonidentity": len(set(shell))==8 and identity() not in shell,
                  "local_B_geom_3": "PASS" if local_count==457 else "FAIL", "based": "NOT_RUN", "global_systole": "NOT_RUN"},
        "local_ball": {"exact_elements": len(ball.elements), "distinct_candidate_images": local_count},
        "accumulated_witness_invariant": {"witness_count": len(accumulated), "all_separated": all(accumulated.values()), "rows": accumulated},
        "resource": {"enumerated_candidate_elements": len(elements), "frozen_order_ceiling": 50000,
                     "cartesian_product_order_used_as_actual_order": False, "hpc_escalation_triggered": False},
        "classification": "LOCAL_PASS_GLOBAL_PENDING" if local_count==457 and all(accumulated.values()) else "REJECTED_PRE_GLOBAL",
    }
    required = ("surface_relation","generation","order_interval","C8_covariance","C8_exact_order","parity","physical_shell_distinct_nonidentity")
    if not all(certificate["gates"][key] is True for key in required) or certificate["classification"] != "LOCAL_PASS_GLOBAL_PENDING":
        raise RuntimeError(f"candidate 0005 pre-global failure: {certificate}")
    CERT.write_text(json.dumps(certificate, indent=2)+"\n", encoding="utf-8"); write_ledger(certificate)


def _iterate_phi(value, count):
    for _ in range(count): value = phi(value)
    return value


if __name__ == "__main__": main()
