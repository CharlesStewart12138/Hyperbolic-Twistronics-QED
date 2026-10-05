"""Exhaust the S4 epimorphism/core interface up to target inner automorphism.

All automorphisms of S4 are inner, so one simultaneous-conjugacy canonical
representative corresponds to one kernel of an epimorphism Gamma_B -> S4.
The scan evaluates exact gates only through the first failure.  No candidate
that fails Q-04/Q-10/Q-11 is promoted to the expensive geometric gates.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
import csv
import hashlib
import json
from pathlib import Path
import time
from typing import Iterable

from production_code.group.automorphism import phi8_power
from production_code.group.core import CoreSignature, core_signature
from production_code.group.quotient_candidate import S8_PRESENTATION
from production_code.group.quotient_search_v2 import (
    S4_ELEMENTS,
    S4_IDENTITY,
    S4_TABLE,
    V2_FIELDS,
    V2Seed,
    base_s4_candidate,
    exact_core_order,
)


S4_INVERSE = tuple(
    next(
        other
        for other in range(24)
        if S4_TABLE[element][other] == S4_IDENTITY
        and S4_TABLE[other][element] == S4_IDENTITY
    )
    for element in range(24)
)
PHI_INVERSE_ORBIT_WORDS = {
    token: tuple(phi8_power((token,), -power) for power in range(8))
    for token in S8_PRESENTATION
}


def multiply(left: int, right: int) -> int:
    return S4_TABLE[left][right]


def commutator(left: int, right: int) -> int:
    return multiply(
        multiply(multiply(left, right), S4_INVERSE[left]),
        S4_INVERSE[right],
    )


def generates_s4(images: tuple[int, int, int, int]) -> bool:
    generators = images + tuple(S4_INVERSE[value] for value in images)
    seen = {S4_IDENTITY}
    queue = deque([S4_IDENTITY])
    while queue:
        element = queue.popleft()
        for generator in generators:
            value = multiply(element, generator)
            if value not in seen:
                seen.add(value)
                queue.append(value)
    return len(seen) == 24


def conjugate(conjugator: int, element: int) -> int:
    return multiply(multiply(conjugator, element), S4_INVERSE[conjugator])


def canonical_inner_orbit(images: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return min(
        tuple(conjugate(conjugator, element) for element in images)
        for conjugator in range(24)
    )


def canonical_relation_solutions() -> tuple[tuple[int, int, int, int], ...]:
    pairs: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for left in range(24):
        for right in range(24):
            pairs[commutator(left, right)].append((left, right))
    canonical: set[tuple[int, int, int, int]] = set()
    for value, first_pairs in pairs.items():
        for a1, b1 in first_pairs:
            for a2, b2 in pairs[S4_INVERSE[value]]:
                canonical.add(canonical_inner_orbit((a1, b1, a2, b2)))
    return tuple(sorted(canonical))


def canonical_epimorphisms() -> tuple[tuple[int, int, int, int], ...]:
    return tuple(images for images in canonical_relation_solutions() if generates_s4(images))


def _evaluate_s4_word(images: tuple[int, int, int, int], word: Iterable[str]) -> int:
    positive = dict(zip(("a1", "b1", "a2", "b2"), images))
    token_images = dict(positive)
    token_images.update({f"{token}_inv": S4_INVERSE[value] for token, value in positive.items()})
    result = S4_IDENTITY
    for token in word:
        result = multiply(result, token_images[token])
    return result


def compact_signature(images: tuple[int, int, int, int], token: str) -> tuple[int, ...]:
    return (1,) + tuple(
        _evaluate_s4_word(images, word)
        for word in PHI_INVERSE_ORBIT_WORDS[token]
    )


def rotate_compact(signature: tuple[int, ...]) -> tuple[int, ...]:
    return (signature[0], signature[-1]) + signature[1:-1]


def signature_period(signature: tuple[int, ...]) -> int:
    value = signature
    for power in range(1, 9):
        value = rotate_compact(value)
        if value == signature:
            return power
    raise AssertionError("C8 rotation did not close")


def interface_counts() -> dict[str, int]:
    solutions = canonical_relation_solutions()
    epimorphisms = tuple(images for images in solutions if generates_s4(images))
    q04_pass = 0
    q10_fail = 0
    q11_pass = 0
    for images in epimorphisms:
        signatures = tuple(compact_signature(images, token) for token in S8_PRESENTATION)
        if len(set(signatures)) != 8:
            continue
        q04_pass += 1
        if max(signature_period(signature) for signature in signatures) != 8:
            q10_fail += 1
            continue
        if Counter(rotate_compact(signature) for signature in signatures) == Counter(signatures):
            q11_pass += 1
    return {
        "canonical_relation_solutions": len(solutions),
        "non_surjective_orbits": len(solutions) - len(epimorphisms),
        "epimorphism_orbits": len(epimorphisms),
        "Q04_fail": len(epimorphisms) - q04_pass,
        "Q04_pass": q04_pass,
        "Q10_fail_after_Q04": q10_fail,
        "Q11_fail_after_prior_pass": q04_pass - q10_fail - q11_pass,
        "Q11_pass": q11_pass,
    }


def exhaustive_record(images: tuple[int, int, int, int], ordinal: int, code_hash: str) -> dict[str, object]:
    started = time.perf_counter()
    candidate_id = f"V2_S4_ORBIT_{ordinal:04d}"
    seed = V2Seed(candidate_id, images)
    base = base_s4_candidate(seed)
    signatures = tuple(compact_signature(images, token) for token in S8_PRESENTATION)
    degree = len(set(signatures))
    q04 = degree == 8
    periods = tuple(signature_period(signature) for signature in signatures)
    q10 = max(periods) == 8
    q11 = Counter(rotate_compact(signature) for signature in signatures) == Counter(signatures)
    first_failed = "Q-04" if not q04 else "Q-10" if not q10 else "Q-11" if not q11 else None
    if first_failed is None:
        raise AssertionError("S4 exhaustive scan unexpectedly produced a Q-11 survivor")
    order = exact_core_order(base)
    runtime = time.perf_counter() - started
    return {
        "candidate_id": candidate_id,
        "base_generator_indices": images,
        "base_generator_images_S4": [list(S4_ELEMENTS[index]) for index in images],
        "core_order": order,
        "degree": degree,
        "phi8_periods": periods,
        "Q04": q04,
        "Q09": True,
        "Q10": q10,
        "Q11": q11,
        "first_failed_gate": first_failed,
        "runtime_seconds": runtime,
        "code_sha256": code_hash,
    }


def exhaustive_csv_row(record: dict[str, object]) -> dict[str, object]:
    return {
        "candidate_id": record["candidate_id"],
        "construction_family": "exhaustive non-Abelian S4 epimorphism orbit plus C8/parity core",
        "base_subgroup_id": f"ker({record['candidate_id']}_BASE)",
        "core_applied": True,
        "group_order": record["core_order"],
        "generator_images": json.dumps(record["base_generator_images_S4"], separators=(",", ":")),
        "surjective": True,
        "surface_relation": True,
        "parity": True,
        "bipartite": True,
        "C8_descent": True,
        "C8_order": record["Q10"],
        "degree": record["degree"],
        "shortest_new_word_relation": "NOT_REACHED",
        "r_inj_word": "NOT_REACHED",
        "shortest_geometric_kernel_displacement": "NOT_REACHED",
        "r_inj_based_geo/a": "NOT_REACHED",
        "r_inj_global_geo/a": "NOT_REACHED",
        "Dc/a": 3.0,
        "no_wraparound": "NOT_REACHED",
        "irrep_inventory_status": "NOT_REACHED",
        "accept/reject": "REJECT",
        "first_failed_gate": record["first_failed_gate"],
        "runtime": record["runtime_seconds"],
        "code_hash": record["code_sha256"],
    }


def append_exhaustive_records(output_dir: Path) -> dict[str, object]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    csv_path = directory / "candidates.csv"
    jsonl_path = directory / "S4_EXHAUSTIVE_CANDIDATES.jsonl"
    summary_path = directory / "S4_EXHAUSTIVE_SUMMARY.json"
    if jsonl_path.exists() or summary_path.exists():
        raise FileExistsError("S4 exhaustive records are immutable and already exist")
    existing_ids: set[str] = set()
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            existing_ids = {row["candidate_id"] for row in csv.DictReader(handle)}
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    records = []
    started = time.perf_counter()
    for ordinal, images in enumerate(canonical_epimorphisms(), start=1):
        record = exhaustive_record(images, ordinal, code_hash)
        if record["candidate_id"] in existing_ids:
            raise ValueError(f"duplicate immutable candidate id: {record['candidate_id']}")
        records.append(record)
    with jsonl_path.open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")
    write_header = not csv_path.exists()
    with csv_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=V2_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerows(exhaustive_csv_row(record) for record in records)
    counts = Counter(record["first_failed_gate"] for record in records)
    orders = Counter(str(record["core_order"]) for record in records)
    summary = {
        **interface_counts(),
        "immutable_rows_appended": len(records),
        "first_failed_gate_counts": dict(counts),
        "exact_core_order_distribution": dict(sorted(orders.items(), key=lambda item: int(item[0]))),
        "Q11_survivors": 0,
        "conclusion": "S4 core family exhausted; no standard-S8_PRESENTATION C8-covariant candidate",
        "elapsed_seconds": time.perf_counter() - started,
        "code_sha256": code_hash,
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(append_exhaustive_records(Path("data/production/quotient_search_v2")), indent=2))

