"""Extract centralizer-orbit representatives of direct S8 cheap survivors."""

from __future__ import annotations

import csv
from itertools import permutations
from pathlib import Path

from production_code.group.compact_c8_equivariant_search import (
    compose,
    conjugate,
    generated_order,
    inverse,
    parity,
    power,
    relation_image,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "production" / "compact_quotient_search" / "s8_survivor_manifest.tsv"


def encode(value: tuple[int, ...]) -> str:
    return "".join(str(item) for item in value)


def main() -> None:
    identity = tuple(range(8))
    cycle = tuple((index + 1) % 8 for index in range(8))
    powers = tuple(power(cycle, index) for index in range(8))
    survivors: list[tuple[int, tuple[int, ...], tuple[tuple[int, ...], ...]]] = []
    for seed_index, seed in enumerate(permutations(range(8))):
        if parity(seed) != 1:
            continue
        images = tuple(conjugate(powers[index], seed) for index in range(8))
        if not all(images[index + 4] == inverse(images[index]) for index in range(4)):
            continue
        if relation_image(images) != identity or len(set(images)) != 8:
            continue
        if generated_order(images) != 40320:
            continue
        survivors.append((seed_index, seed, images))
    if len(survivors) != 48:
        raise AssertionError(f"cheap survivor drift: {len(survivors)}")

    by_seed = {seed: (seed_index, images) for seed_index, seed, images in survivors}
    seen: set[tuple[int, ...]] = set()
    representatives = []
    for seed_index, seed, images in survivors:
        if seed in seen:
            continue
        orbit = {conjugate(powers[index], seed) for index in range(8)}
        survivor_orbit = orbit.intersection(by_seed)
        if len(survivor_orbit) != 8:
            raise AssertionError("centralizer orbit is not a full cheap-survivor orbit")
        seen.update(survivor_orbit)
        representatives.append((seed_index, seed, images, sorted(by_seed[item][0] for item in survivor_orbit)))
    if len(representatives) != 6 or len(seen) != 48:
        raise AssertionError("expected six centralizer-kernel representatives")

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["kernel_orbit_id", "representative_seed_index", "member_seed_indices", *[f"g{i}" for i in range(8)]])
        for orbit_index, (seed_index, _seed, images, members) in enumerate(representatives):
            writer.writerow([
                f"DIRECT_S8_KERNEL_ORBIT_{orbit_index:02d}",
                seed_index,
                ",".join(map(str, members)),
                *[encode(image) for image in images],
            ])
    print(f"cheap_survivors={len(survivors)} kernel_orbits={len(representatives)} output={OUT}")


if __name__ == "__main__":
    main()
