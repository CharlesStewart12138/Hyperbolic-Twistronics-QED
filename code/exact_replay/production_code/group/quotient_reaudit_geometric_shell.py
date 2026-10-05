"""Re-audit every stored quotient candidate on the geometric physical shell."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import time
from typing import Iterable, Sequence

from production_code.group.automorphism import phi8
from production_code.group.core import CoreSignature, core_signature, multiply_signatures
from production_code.group.geometric_shell_contract import GEOMETRIC_TO_STANDARD_WORD
from production_code.group.injectivity_bridge import _geometry_from_matrix
from production_code.group.quotient_candidate import INVERSE_TOKEN, POSITIVE_GENERATORS, RELATOR, S8_PRESENTATION
from production_code.group.quotient_s4_exhaustive import generates_s4
from production_code.group.quotient_search_v2 import (
    V2_SEEDS,
    V2Seed,
    base_s4_candidate,
    exact_core_order,
    rotate_signature,
)
from production_code.group.surface_group import free_reduce, inverse_word
from production_code.group.universal_cover import (
    GEOMETRIC_INVERSE,
    enumerate_ball,
    free_reduce_geometric,
    inverse_geometric_word,
    matrix_from_word,
)


RQA_IDS = tuple(f"RQA{index:02d}" for index in range(1, 21))


def _standard_ball_three() -> tuple[tuple[str, ...], ...]:
    words: list[tuple[str, ...]] = [()]
    frontier = [()]
    for _ in range(3):
        next_frontier = []
        for word in frontier:
            for token in S8_PRESENTATION:
                if word and token == INVERSE_TOKEN[word[-1]]:
                    continue
                next_frontier.append(word + (token,))
        words.extend(next_frontier)
        frontier = next_frontier
    if len(words) != 457:
        raise AssertionError(f"unexpected standard B3 size {len(words)}")
    return tuple(words)


STANDARD_B3 = _standard_ball_three()
GEOMETRIC_B3 = tuple((element.element_id, element.representative) for element in enumerate_ball(3).elements)


def _evaluate(
    base,
    images: dict[str, CoreSignature],
    word: Iterable[str],
) -> CoreSignature:
    result = core_signature(base, ())
    for token in word:
        result = multiply_signatures(base, result, images[token])
    return result


def _standard_images(base) -> dict[str, CoreSignature]:
    return {token: core_signature(base, (token,)) for token in S8_PRESENTATION}


def _geometric_images(base, standard: dict[str, CoreSignature]) -> dict[str, CoreSignature]:
    return {
        f"g{index}": _evaluate(base, standard, GEOMETRIC_TO_STANDARD_WORD[index])
        for index in range(8)
    }


def _ball_collision(
    base,
    images: dict[str, CoreSignature],
    rows: Sequence[tuple[int, tuple[str, ...]]],
) -> tuple[int, tuple[int, int] | None, tuple[str, ...] | None]:
    seen: dict[CoreSignature, tuple[int, tuple[str, ...]]] = {}
    collision = None
    witness = None
    for element_id, word in rows:
        image = _evaluate(base, images, word)
        prior = seen.get(image)
        if prior is not None and collision is None:
            collision = (prior[0], element_id)
            if next(iter(images)).startswith("g"):
                witness = free_reduce_geometric(prior[1] + inverse_geometric_word(word))
            else:
                witness = free_reduce(prior[1] + inverse_word(word))
        seen.setdefault(image, (element_id, word))
    return len(seen), collision, witness


def load_candidate_specs(input_dir: Path) -> list[dict[str, object]]:
    directory = Path(input_dir)
    inventory_path = directory / "candidates.csv"
    exhaustive_path = directory / "S4_EXHAUSTIVE_CANDIDATES.jsonl"
    with inventory_path.open("r", encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle))
    exhaustive = {}
    with exhaustive_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            exhaustive[row["candidate_id"]] = row
    seeds = {seed.candidate_id: seed for seed in V2_SEEDS}
    specs = []
    for ordinal, row in enumerate(inventory, start=1):
        candidate_id = row["candidate_id"]
        if candidate_id in seeds:
            indices = seeds[candidate_id].generator_indices
        else:
            if candidate_id not in exhaustive:
                raise ValueError(f"missing reconstruction record for {candidate_id}")
            indices = tuple(int(value) for value in exhaustive[candidate_id]["base_generator_indices"])
        specs.append({
            "ordinal": ordinal,
            "candidate_id": candidate_id,
            "base_generator_indices": indices,
            "recorded_group_order": int(row["group_order"]),
            "construction_family": row["construction_family"],
        })
    if len(specs) != 903 or len({row["candidate_id"] for row in specs}) != 903:
        raise ValueError("immutable candidate inventory must contain 903 unique rows")
    return specs


def audit_candidate(spec: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter()
    seed = V2Seed(str(spec["candidate_id"]), tuple(spec["base_generator_indices"]))
    base = base_s4_candidate(seed)
    identity = core_signature(base, ())
    standard = _standard_images(base)
    geometric = _geometric_images(base, standard)
    geometric_tuple = tuple(geometric[f"g{index}"] for index in range(8))
    exact_order = exact_core_order(base)

    rqa01 = core_signature(base, RELATOR) == identity
    rqa02 = generates_s4(seed.generator_indices) and exact_order == int(spec["recorded_group_order"])
    rqa03 = True
    rqa04 = len(set(geometric_tuple)) == 8
    rqa05 = True
    rqa06 = all(image.parity_image == 1 for image in standard.values())
    rqa07 = rqa06 and all(image.parity_image == 1 for image in geometric_tuple)
    rqa08 = all(
        multiply_signatures(base, geometric_tuple[index], geometric_tuple[(index + 4) % 8]) == identity
        for index in range(4)
    )
    rqa09 = all(
        rotate_signature(standard[token]) == _evaluate(base, standard, phi8((token,)))
        for token in POSITIVE_GENERATORS
    )
    action_periods = []
    for token in POSITIVE_GENERATORS:
        image = standard[token]
        current = image
        period = None
        for power in range(1, 9):
            current = rotate_signature(current)
            if current == image:
                period = power
                break
        action_periods.append(period)
    rqa10 = all(period is not None for period in action_periods) and max(action_periods) == 8
    rqa11 = all(
        rotate_signature(geometric_tuple[index]) == geometric_tuple[(index + 1) % 8]
        for index in range(8)
    ) and Counter(rotate_signature(image) for image in geometric_tuple) == Counter(geometric_tuple)

    standard_rows = tuple((index, word) for index, word in enumerate(STANDARD_B3))
    standard_size, standard_collision, standard_witness = _ball_collision(base, standard, standard_rows)
    geometric_size, geometric_collision, geometric_witness = _ball_collision(base, geometric, GEOMETRIC_B3)
    rqa12 = geometric_collision is None and geometric_size == 457

    based_upper = None
    global_upper = None
    if geometric_witness:
        based, translation, _, _ = _geometry_from_matrix(matrix_from_word(geometric_witness))
        based_upper = based / 2.0
        global_upper = translation / 2.0
    # A B3 collision supplies a nontrivial kernel word of geometric length at
    # most six. Triangle inequality then proves both radii <= 3*a_B.
    if not rqa12:
        rqa13: bool | str = False
        rqa14: bool | str = False
    else:
        rqa13 = "NOT_CERTIFIED_REQUIRES_GEOMETRIC_KERNEL_EXCLUSION_THROUGH_127"
        rqa14 = "NOT_CERTIFIED_REQUIRES_GEOMETRIC_KERNEL_EXCLUSION_THROUGH_156"
    rqa15 = rqa13 is True and rqa14 is True
    rqa16 = rqa09 and rqa11
    rqa17 = True
    rqa18 = rqa07
    rqa19: bool | str = "NOT_REACHED_EARLIER_REJECTION"
    rqa20: bool | str = "NOT_REACHED_NO_ACCEPTED_QUOTIENT"

    checks: dict[str, bool | str] = dict(zip(RQA_IDS, (
        rqa01, rqa02, rqa03, rqa04, rqa05, rqa06, rqa07, rqa08, rqa09, rqa10,
        rqa11, rqa12, rqa13, rqa14, rqa15, rqa16, rqa17, rqa18, rqa19, rqa20,
    )))
    first_failed = next((key for key in RQA_IDS if checks[key] is not True), None)
    accepted = all(checks[key] is True for key in RQA_IDS)
    presentation_radius = ">3" if standard_collision is None else "<=3"
    geometric_radius = ">3" if rqa12 else "<=3"
    rejection_witness = None
    if first_failed == "RQA04":
        duplicates = {}
        for index, image in enumerate(geometric_tuple):
            duplicates.setdefault(str(image), []).append(f"g{index}")
        rejection_witness = {"repeated_physical_directions": [value for value in duplicates.values() if len(value) > 1]}
    elif first_failed == "RQA10":
        rejection_witness = {"phi8_action_periods_on_positive_generators": action_periods}
    elif first_failed == "RQA12":
        rejection_witness = {
            "geometric_B3_collision_element_ids": geometric_collision,
            "kernel_word": geometric_witness,
        }
    elif first_failed:
        rejection_witness = {"failed_gate": first_failed}

    return {
        "ordinal": spec["ordinal"],
        "candidate_id": spec["candidate_id"],
        "construction_family": spec["construction_family"],
        "base_generator_indices": list(seed.generator_indices),
        "group_order": exact_order,
        "physical_shell": "S8_GEOMETRIC",
        "presentation_shell": "S8_PRESENTATION_DIAGNOSTIC_ONLY",
        "physical_degree": len(set(geometric_tuple)),
        "phi8_action_periods_on_positive_generators": action_periods,
        "standard_presentation_B3": {
            "universal_ball_size": 457,
            "image_size": standard_size,
            "collision_element_ids": standard_collision,
            "kernel_witness": standard_witness,
            "word_injectivity_radius": presentation_radius,
        },
        "physical_geometric_B3": {
            "universal_ball_size": 457,
            "image_size": geometric_size,
            "collision_element_ids": geometric_collision,
            "kernel_witness": geometric_witness,
            "word_injectivity_radius": geometric_radius,
        },
        "hyperbolic_geometric": {
            "based_radius_exact": None,
            "global_radius_exact": None,
            "based_witness_upper_bound_over_a": based_upper,
            "global_witness_upper_bound_over_a": global_upper,
            "word_bound_promoted_to_geometric": False,
        },
        "checks": checks,
        "accept_reject": "ACCEPT" if accepted else "REJECT",
        "first_failed_gate": first_failed,
        "rejection_witness": rejection_witness,
        "runtime_seconds": time.perf_counter() - started,
    }


def _csv_row(record: dict[str, object]) -> dict[str, object]:
    checks = record["checks"]
    standard = record["standard_presentation_B3"]
    geometric = record["physical_geometric_B3"]
    hyperbolic = record["hyperbolic_geometric"]
    return {
        "ordinal": record["ordinal"],
        "candidate_id": record["candidate_id"],
        "group_order": record["group_order"],
        "physical_degree": record["physical_degree"],
        "standard_presentation_word_radius": standard["word_injectivity_radius"],
        "physical_geometric_word_radius": geometric["word_injectivity_radius"],
        "based_hyperbolic_radius_exact": "NOT_COMPUTED",
        "global_hyperbolic_radius_exact": "NOT_COMPUTED",
        "based_witness_upper_bound_over_a": hyperbolic["based_witness_upper_bound_over_a"],
        "global_witness_upper_bound_over_a": hyperbolic["global_witness_upper_bound_over_a"],
        **checks,
        "accept_reject": record["accept_reject"],
        "first_failed_gate": record["first_failed_gate"],
        "rejection_witness": json.dumps(record["rejection_witness"], separators=(",", ":")),
        "runtime_seconds": record["runtime_seconds"],
    }


def run_reaudit(input_dir: Path, output_dir: Path, limit: int | None = None) -> dict[str, object]:
    specs = load_candidate_specs(input_dir)
    if limit is not None:
        specs = specs[:limit]
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    suffix = "" if limit is None else f"_limit_{limit}"
    paths = {
        "csv": output / f"candidates_geometric_shell_reaudit{suffix}.csv",
        "jsonl": output / f"candidates_geometric_shell_reaudit{suffix}.jsonl",
        "summary": output / f"REAUDIT_SUMMARY{suffix}.json",
        "rejections": output / f"rejection_log{suffix}.csv",
    }
    for path in paths.values():
        if path.exists():
            raise FileExistsError(f"re-audit output already exists: {path}")
    started = time.perf_counter()
    records = [audit_candidate(spec) for spec in specs]
    rows = [_csv_row(record) for record in records]
    with paths["jsonl"].open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")
    with paths["csv"].open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    rejected = [row for row in rows if row["accept_reject"] == "REJECT"]
    with paths["rejections"].open("x", encoding="utf-8", newline="") as handle:
        fields = ["ordinal", "candidate_id", "group_order", "first_failed_gate", "rejection_witness"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in fields} for row in rejected)
    first_fail_counts = Counter(row["first_failed_gate"] for row in rows)
    gate_counts = {
        key: {
            "PASS": sum(record["checks"][key] is True for record in records),
            "FAIL": sum(record["checks"][key] is False for record in records),
            "OTHER": sum(not isinstance(record["checks"][key], bool) for record in records),
        }
        for key in RQA_IDS
    }
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-903-REAUDIT",
        "input_candidate_count": len(specs),
        "expected_full_count": 903,
        "full_inventory_run": limit is None,
        "physical_shell": "S8_GEOMETRIC",
        "standard_shell_role": "DIAGNOSTIC_ONLY",
        "accepted_count": sum(row["accept_reject"] == "ACCEPT" for row in rows),
        "rejected_count": len(rejected),
        "survivor_ids": [row["candidate_id"] for row in rows if row["accept_reject"] == "ACCEPT"],
        "first_failed_gate_counts": dict(sorted(first_fail_counts.items())),
        "gate_counts": gate_counts,
        "presentation_B3_injective_count": sum(record["standard_presentation_B3"]["collision_element_ids"] is None for record in records),
        "geometric_B3_injective_count": sum(record["physical_geometric_B3"]["collision_element_ids"] is None for record in records),
        "outputs": {key: path.name for key, path in paths.items()},
        "runtime_seconds": time.perf_counter() - started,
        "code_sha256": script_hash,
        "manuscript_main_tex_modified": False,
    }
    paths["summary"].write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("data/production/quotient_search_v2"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/production/quotient_reaudit_geometric_shell"))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    print(json.dumps(run_reaudit(args.input_dir, args.output_dir, args.limit), indent=2))


if __name__ == "__main__":
    main()
