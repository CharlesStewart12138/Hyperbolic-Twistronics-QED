"""Evaluate the actual subdirect p=3/H1 x p=5 refinement.

The frozen compact order ceiling permits a rigorous early rejection once
50,001 distinct generated diagonal-image elements have been constructed.
No Cartesian-product order is presented as the actual order.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import time
from collections import deque
from pathlib import Path


base = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0002")
arith = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "CONSTRUCTIVE_EXECUTION_R4"
OUT = R4 / "09_CEGAR" / "ITERATION_0002_P5_REFINEMENT_ORDER_OBSTRUCTION.json"
P = 5
CEILING = 50_000


def identity() -> tuple[int, ...]:
    return base.identity() + arith.aidentity(P)


def generator(index: int) -> tuple[int, ...]:
    return base.generator(index) + arith.generator(index, P)


def multiply(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return base.multiply(left[:9], right[:9]) + arith.amul(left[9:], right[9:], P)


def word_image(word: tuple[str, ...]) -> tuple[int, ...]:
    result = identity()
    for token in word:
        result = multiply(result, generator(int(token[1])))
    return result


def main() -> None:
    started = time.perf_counter()
    one = identity()
    generators = tuple(generator(i) for i in range(8))
    seen = {one}
    queue = deque([one])
    exceeded = False
    while queue and not exceeded:
        source = queue.popleft()
        for image in generators:
            target = multiply(source, image)
            if target in seen:
                continue
            seen.add(target)
            if len(seen) == CEILING + 1:
                exceeded = True
                break
            queue.append(target)

    local_witness = tuple("g0 g1 g7 g1 g0 g2".split())
    global_witness = tuple("g0 g1 g3 g6 g3 g1 g6 g3 g1 g7 g1 g4".split())
    checks = {
        "strictly_refines_base": word_image(global_witness) != one,
        "preserves_prior_local_witness_separation": word_image(local_witness) != one,
        "actual_generated_elements_exceed_ceiling": exceeded and len(seen) == CEILING + 1,
    }
    if not all(checks.values()):
        raise RuntimeError(f"p=5 refinement obstruction failed: {checks}")
    OUT.write_text(json.dumps({
        "schema_version": "1.0",
        "iteration": 2,
        "proposal_id": "REFINE-CAND-R4-0002-ARITH-P5",
        "construction": "actual diagonal image of CAND-R4-0002 and ARITH-P5-C0CA0BF862D52B5A",
        "classification": "PRUNED_EXACT_ORDER_LOWER_BOUND",
        "frozen_order_ceiling": CEILING,
        "distinct_actual_generated_elements_constructed": len(seen),
        "proved_actual_order_lower_bound": CEILING + 1,
        "complete_actual_order_enumerated": False,
        "cartesian_product_order_used_as_actual_order": False,
        "checks": checks,
        "runtime_seconds": time.perf_counter() - started,
        "base_certificate_sha256": hashlib.sha256((R4 / "10_CANDIDATES" / "CAND-R4-0002.certificate.json").read_bytes()).hexdigest().upper(),
        "conclusion": "the canonical available arithmetic separator refinement cannot lie in the frozen compact order window",
        "next_route": "construct the least-cost C8-stable p-quotient separator with marginal index at most four",
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
