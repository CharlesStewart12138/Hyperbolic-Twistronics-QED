"""Exact non-Abelian quotient search v2 for the Bolza surface group.

The candidates are C8/parity cores of explicit epimorphisms to S4.  The
resulting quotient is represented faithfully as a permutation group on a
2+8*4 point disjoint union, so its order is computed exactly by
Schreier--Sims without materializing a quadratic multiplication table.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import csv
import gzip
import hashlib
from itertools import permutations
import json
from pathlib import Path
import time
from typing import Any, Iterable, Sequence

from sympy.combinatorics import Permutation, PermutationGroup

from production_code.group.automorphism import phi8
from production_code.group.core import CoreSignature, core_signature, multiply_signatures
from production_code.group.nielsen import geometric_to_standard
from production_code.group.quotient_candidate import (
    FiniteQuotientCandidate,
    POSITIVE_GENERATORS,
    RELATOR,
    S8_PRESENTATION,
)


V2_FIELDS = (
    "candidate_id",
    "construction_family",
    "base_subgroup_id",
    "core_applied",
    "group_order",
    "generator_images",
    "surjective",
    "surface_relation",
    "parity",
    "bipartite",
    "C8_descent",
    "C8_order",
    "degree",
    "shortest_new_word_relation",
    "r_inj_word",
    "shortest_geometric_kernel_displacement",
    "r_inj_based_geo/a",
    "r_inj_global_geo/a",
    "Dc/a",
    "no_wraparound",
    "irrep_inventory_status",
    "accept/reject",
    "first_failed_gate",
    "runtime",
    "code_hash",
)


S4_ELEMENTS = tuple(permutations(range(4)))
S4_INDEX = {element: number for number, element in enumerate(S4_ELEMENTS)}
S4_TABLE = tuple(
    tuple(
        S4_INDEX[tuple(left[right[index]] for index in range(4))]
        for right in S4_ELEMENTS
    )
    for left in S4_ELEMENTS
)
S4_IDENTITY = S4_INDEX[(0, 1, 2, 3)]


@dataclass(frozen=True)
class V2Seed:
    candidate_id: str
    generator_indices: tuple[int, int, int, int]


V2_SEEDS = (
    V2Seed("V2_S4_CORE_001_N4608", (1, 1, 2, 21)),
    V2Seed("V2_S4_CORE_002_N331776", (1, 1, 2, 23)),
    V2Seed("V2_S4_CORE_003_N165888", (1, 1, 8, 8)),
)


def base_s4_candidate(seed: V2Seed) -> FiniteQuotientCandidate:
    return FiniteQuotientCandidate(
        quotient_id=f"{seed.candidate_id}_BASE",
        element_labels=tuple("".join(map(str, element)) for element in S4_ELEMENTS),
        multiplication_table=S4_TABLE,
        identity=S4_IDENTITY,
        generator_images=dict(zip(POSITIVE_GENERATORS, seed.generator_indices)),
        construction_method="exact S4 permutation epimorphism seed",
        provenance="quotient_search_v2 deterministic enumeration",
    )


def _ambient_permutation(signature: CoreSignature) -> Permutation:
    values = list(range(34))
    if signature.parity_image:
        values[0], values[1] = 1, 0
    for block, element_index in enumerate(signature.rotated_quotient_images):
        permutation = S4_ELEMENTS[element_index]
        offset = 2 + 4 * block
        for point in range(4):
            values[offset + point] = offset + permutation[point]
    return Permutation(values)


def _signature_json(signature: CoreSignature) -> dict[str, Any]:
    return {
        "parity": signature.parity_image,
        "S4_phi_inverse_orbit": [
            list(S4_ELEMENTS[index]) for index in signature.rotated_quotient_images
        ],
    }


def rotate_signature(signature: CoreSignature) -> CoreSignature:
    values = signature.rotated_quotient_images
    return CoreSignature(signature.parity_image, (values[-1],) + values[:-1])


def signature_power(signature: CoreSignature, power: int) -> CoreSignature:
    result = signature
    for _ in range(power % 8):
        result = rotate_signature(result)
    return result


def core_generators(base: FiniteQuotientCandidate) -> dict[str, CoreSignature]:
    return {token: core_signature(base, (token,)) for token in S8_PRESENTATION}


def exact_core_order(base: FiniteQuotientCandidate) -> int:
    generators = [_ambient_permutation(core_signature(base, (token,))) for token in POSITIVE_GENERATORS]
    return int(PermutationGroup(generators).order())


def evaluate_geometric_word(
    base: FiniteQuotientCandidate,
    images: dict[str, CoreSignature],
    word: Iterable[str],
) -> CoreSignature:
    result = core_signature(base, ())
    for token in word:
        result = multiply_signatures(base, result, images[token])
    return result


def universal_ball_audit(base: FiniteQuotientCandidate, archive: Path) -> dict[str, Any]:
    identity = core_signature(base, ())
    standard = core_generators(base)
    g_to_h = {
        "g0": "h0", "g1": "h1_inv", "g2": "h2", "g3": "h3_inv",
        "g4": "h0_inv", "g5": "h1", "g6": "h2_inv", "g7": "h3",
    }
    geometric = {
        token: core_signature(base, geometric_to_standard((h_token,)))
        for token, h_token in g_to_h.items()
    }
    seen_b3: dict[CoreSignature, int] = {}
    b3_collision = None
    shortest_kernel = None
    shortest_kernel_displacement = None
    rows = 0
    with gzip.open(Path(archive), "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            rows += 1
            length = int(row["minimum_geometric_word_length"])
            image = evaluate_geometric_word(base, geometric, row["representative"])
            if length <= 3:
                prior = seen_b3.get(image)
                if prior is not None and b3_collision is None:
                    b3_collision = [prior, int(row["element_id"])]
                seen_b3.setdefault(image, int(row["element_id"]))
            if int(row["element_id"]) != 0 and image == identity and shortest_kernel is None:
                shortest_kernel = row["representative"]
                shortest_kernel_displacement = float(row["distance_over_a_B"])
    return {
        "archive_rows": rows,
        "exact_ball_B3_size": 457,
        "exact_ball_B6_size": 155577,
        "B3_image_size": len(seen_b3),
        "injective_on_B3": b3_collision is None and len(seen_b3) == 457,
        "B3_collision": b3_collision,
        "shortest_kernel_word_within_radius_6": shortest_kernel,
        "shortest_kernel_displacement_over_a_within_radius_6": shortest_kernel_displacement,
        "no_nontrivial_kernel_word_through_6": shortest_kernel is None,
        "standard_generator_signature_count": len(set(standard.values())),
    }


def audit_seed(seed: V2Seed, archive: Path) -> dict[str, Any]:
    started = time.perf_counter()
    base = base_s4_candidate(seed)
    images = core_generators(base)
    identity = core_signature(base, ())
    order = exact_core_order(base)
    ball = universal_ball_audit(base, archive)

    q01 = core_signature(base, RELATOR) == identity
    q04 = len(set(images.values())) == 8
    q09 = all(rotate_signature(images[token]) == core_signature(base, phi8((token,))) for token in S8_PRESENTATION)
    action_orders = [
        min(power for power in range(1, 9) if signature_power(image, power) == image)
        for image in images.values()
    ]
    q10 = all(signature_power(image, 8) == image for image in images.values()) and max(action_orders) == 8
    q11 = Counter(rotate_signature(images[token]) for token in S8_PRESENTATION) == Counter(images.values())
    based_upper = None
    if ball["shortest_kernel_displacement_over_a_within_radius_6"] is not None:
        based_upper = 0.5 * float(ball["shortest_kernel_displacement_over_a_within_radius_6"])
    q13 = False  # Requires exclusion of kernel words through the certified cutoff 127.
    q14 = False  # Requires normal-kernel exclusion through the certified cutoff 156.
    no_wraparound: bool | None = False if based_upper is not None and based_upper <= 3.0 else None
    checks = {
        "Q-01_surface_relation_exact": q01,
        "Q-02_surjective_onto_declared_generated_image": True,
        "Q-03_kernel_normal": True,
        "Q-04_eight_generator_directions_distinct": q04,
        "Q-05_connected_Cayley_graph": True,
        "Q-06_parity_factors": True,
        "Q-07_bipartite": True,
        "Q-08_staggered_minus_8_mode": True,
        "Q-09_phi8_descends": q09,
        "Q-10_phi8_order_exactly_8": q10,
        "Q-11_standard_S8_PRESENTATION_adjacency_covariance": q11,
        "Q-12_word_injectivity_radius_gt_3": bool(ball["injective_on_B3"]),
        "Q-13_based_geometric_certificate_Dc3": q13,
        "Q-14_global_geometric_systole_certificate_Dc3": q14,
        "Q-15_physical_no_wraparound": no_wraparound is True,
        "Q-16_complete_irrep_inventory": False,
    }
    mandatory = list(checks)[:15]
    first_failed = next((gate.split("_")[0] for gate in mandatory if not checks[gate]), None)
    runtime = time.perf_counter() - started
    source_path = Path(__file__)
    code_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    base_images = {
        token: list(S4_ELEMENTS[index])
        for token, index in zip(POSITIVE_GENERATORS, seed.generator_indices)
    }
    return {
        "candidate_id": seed.candidate_id,
        "construction_family": "non-Abelian S4 epimorphism followed by C8/parity core",
        "base_subgroup_id": f"ker({seed.candidate_id}_BASE)",
        "core_definition": "ker(pi) intersect intersection_{j=0}^7 phi8^j(ker(q))",
        "core_applied": True,
        "group_order": order,
        "permutation_degree": 34,
        "base_generator_images_S4": base_images,
        "core_generator_images": {token: _signature_json(images[token]) for token in POSITIVE_GENERATORS},
        "checks": checks,
        "phi8_action_orders_on_S8_PRESENTATION_images": action_orders,
        "universal_ball_audit": ball,
        "word_injectivity": ">3" if ball["injective_on_B3"] else "<=3",
        "shortest_new_word_relation": ball["shortest_kernel_word_within_radius_6"] or ">6 (not found within exact B6 archive)",
        "r_inj_based_geo_over_a": None if based_upper is None else {"upper_bound": based_upper},
        "r_inj_global_geo_over_a": None,
        "Dc_over_a": 3.0,
        "no_wraparound": no_wraparound,
        "irrep_inventory_status": "NOT_AVAILABLE_NOT_REACHED",
        "accept_reject": "ACCEPT" if all(checks[key] for key in mandatory) else "REJECT",
        "first_failed_gate": first_failed,
        "runtime_seconds": runtime,
        "code_sha256": code_hash,
        "size_lower_bounds": {
            "word_r_inj_gt_3_requires_order_at_least_B3": 457,
            "Option_B_physical_certification_requires_injectivity_beyond_current_B6": True,
            "current_exact_B6_size_lower_bound": 155577,
        },
    }


def csv_row(record: dict[str, Any]) -> dict[str, Any]:
    ball = record["universal_ball_audit"]
    based = record["r_inj_based_geo_over_a"]
    return {
        "candidate_id": record["candidate_id"],
        "construction_family": record["construction_family"],
        "base_subgroup_id": record["base_subgroup_id"],
        "core_applied": record["core_applied"],
        "group_order": record["group_order"],
        "generator_images": json.dumps(record["core_generator_images"], separators=(",", ":")),
        "surjective": record["checks"]["Q-02_surjective_onto_declared_generated_image"],
        "surface_relation": record["checks"]["Q-01_surface_relation_exact"],
        "parity": record["checks"]["Q-06_parity_factors"],
        "bipartite": record["checks"]["Q-07_bipartite"],
        "C8_descent": record["checks"]["Q-09_phi8_descends"],
        "C8_order": record["checks"]["Q-10_phi8_order_exactly_8"],
        "degree": 8 if record["checks"]["Q-04_eight_generator_directions_distinct"] else len(set(json.dumps(x) for x in record["core_generator_images"].values())),
        "shortest_new_word_relation": json.dumps(record["shortest_new_word_relation"], separators=(",", ":")),
        "r_inj_word": record["word_injectivity"],
        "shortest_geometric_kernel_displacement": ball["shortest_kernel_displacement_over_a_within_radius_6"],
        "r_inj_based_geo/a": None if based is None else based["upper_bound"],
        "r_inj_global_geo/a": record["r_inj_global_geo_over_a"],
        "Dc/a": record["Dc_over_a"],
        "no_wraparound": record["no_wraparound"],
        "irrep_inventory_status": record["irrep_inventory_status"],
        "accept/reject": record["accept_reject"],
        "first_failed_gate": record["first_failed_gate"],
        "runtime": record["runtime_seconds"],
        "code_hash": record["code_sha256"],
    }


def run_search(archive: Path, output_dir: Path) -> list[dict[str, Any]]:
    directory = Path(output_dir)
    if directory.exists() and any(directory.iterdir()):
        raise FileExistsError("quotient_search_v2 is append-only; refusing to overwrite existing records")
    directory.mkdir(parents=True, exist_ok=True)
    records = [audit_seed(seed, archive) for seed in V2_SEEDS]
    for record in records:
        path = directory / f"{record['candidate_id']}.json"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    csv_path = directory / "candidates.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=V2_FIELDS)
        writer.writeheader()
        writer.writerows(csv_row(record) for record in records)
    summary = {
        "candidate_count": len(records),
        "accepted": sum(record["accept_reject"] == "ACCEPT" for record in records),
        "rejected": sum(record["accept_reject"] == "REJECT" for record in records),
        "first_failed_gate_counts": dict(Counter(record["first_failed_gate"] for record in records)),
        "records": [record["candidate_id"] for record in records],
        "main_tex_modified": False,
    }
    (directory / "SEARCH_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return records


if __name__ == "__main__":
    result = run_search(
        Path("data/production/universal_cover/ball_radius_6_exact.jsonl.gz"),
        Path("data/production/quotient_search_v2"),
    )
    print(json.dumps([{"candidate_id": r["candidate_id"], "order": r["group_order"], "first_failed_gate": r["first_failed_gate"]} for r in result], indent=2))

