"""Independent detail pass for strongest PSL(3,3) x C2 direct-map orbits."""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path

from production_code.escalations.psl3_3_c8_direct_exhaustive_psl33 import (
    IDENTITY,
    b3_result,
    determinant,
    direct_subgroup_order,
    frozen_b3,
    inverse,
    matrix_json,
    multiply,
    subgroup,
)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "psl3_3_c8_direct_exhaustive_psl33.json"
OUTPUT = Path(__file__).with_suffix(".json")


def tuple_from_json(record: dict[str, object]) -> tuple[int, ...]:
    return tuple(int(value) for value in record["row_major_entries_F3"])  # type: ignore[index]


def main() -> None:
    certificate = json.loads(SOURCE.read_text(encoding="utf-8"))
    elements = tuple(a for a in product(range(3), repeat=9) if determinant(a) == 1)
    index = {value: i for i, value in enumerate(elements)}
    identity = index[IDENTITY]
    inverses = tuple(index[inverse(value)] for value in elements)
    words = frozen_b3()
    classes = []
    for class_record in certificate["classes"]:
        h = tuple_from_json(class_record["representative"])
        h_inverse = inverse(h)
        alpha = tuple(index[multiply(multiply(h, value), h_inverse)] for value in elements)
        relation_reps = class_record["centralizer_seed_orbits"]["inverse_orbit_relation"]
        generation_rep_ids = class_record["centralizer_seed_orbits"]["generation"]["representative_seed_indices"]
        details = []
        relation_image_sizes = []
        for seed_id in relation_reps["representative_seed_indices"]:
            images = [int(seed_id)]
            for _ in range(7):
                images.append(alpha[images[-1]])
            b3 = b3_result(elements, index, identity, tuple(images), words)
            relation_image_sizes.append(int(b3["image_size"]))
            details.append({
                "seed_index": seed_id,
                "seed": matrix_json(elements[seed_id]),
                "centralizer_orbit_size": relation_reps["orbit_sizes"][len(details)],
                "physical_images": [matrix_json(elements[value]) for value in images],
                "base_generated_order": len(subgroup(elements, index, identity, tuple(images))),
                "direct_product_generated_order": direct_subgroup_order(elements, index, identity, tuple(images)),
                "B3": b3,
            })
        # Verify the strongest orbit representatives reported by the exhaustive pass.
        strongest = [record for record in details if record["seed_index"] in generation_rep_ids]
        if len(strongest) != len(generation_rep_ids):
            raise AssertionError("generation representative mismatch")
        classes.append({
            "class_number": class_record["class_number"],
            "automorphism_representative": class_record["representative"],
            "inverse_orbit_relation_orbit_details": details,
            "B3_image_size_histogram_over_orbit_representatives": dict(sorted(Counter(relation_image_sizes).items())),
            "generation_orbit_representatives": strongest,
        })
    result = {
        "schema_version": "1.0",
        "source_exhaustive_certificate": SOURCE.name,
        "note": "Kernel/B3 behavior is invariant under the alpha-centralizer conjugation used for these seed orbits.",
        "classes": classes,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
