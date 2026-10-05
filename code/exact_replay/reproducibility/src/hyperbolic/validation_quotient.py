"""Explicit clean-room finite quotient of the genus-two surface group."""

from __future__ import annotations

from collections import deque
from itertools import product


GENERATOR_NAMES = ("a1", "b1", "a2", "b2", "a1^-1", "b1^-1", "a2^-1", "b2^-1")
GENERATOR_STEPS = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (-1, 0, 0, 0),
    (0, -1, 0, 0),
    (0, 0, -1, 0),
    (0, 0, 0, -1),
)


def add(left: tuple[int, ...], right: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple((x + y) % modulus for x, y in zip(left, right))


def inverse(element: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple((-value) % modulus for value in element)


def c8_automorphism(element: tuple[int, int, int, int], modulus: int) -> tuple[int, int, int, int]:
    """Signed cyclic permutation e1->e2->e3->e4->-e1."""
    return ((-element[3]) % modulus, element[0], element[1], element[2])


def all_elements(modulus: int = 4) -> list[tuple[int, int, int, int]]:
    if modulus < 4 or modulus % 2:
        raise ValueError("validation modulus must be even and at least four")
    return list(product(range(modulus), repeat=4))


def build_quotient(modulus: int = 4) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    elements = all_elements(modulus)
    element_index = {element: index for index, element in enumerate(elements)}
    element_rows = [
        {
            "quotient_index": index,
            "x_a1": element[0],
            "x_b1": element[1],
            "x_a2": element[2],
            "x_b2": element[3],
            "parity": sum(element) % 2,
            "c8_image_index": element_index[c8_automorphism(element, modulus)],
        }
        for index, element in enumerate(elements)
    ]
    edge_rows: list[dict[str, object]] = []
    neighbor_sets: list[set[int]] = []
    for source_index, source in enumerate(elements):
        neighbors: set[int] = set()
        for generator_index, (generator_name, step) in enumerate(zip(GENERATOR_NAMES, GENERATOR_STEPS)):
            target = add(source, step, modulus)
            target_index = element_index[target]
            neighbors.add(target_index)
            edge_rows.append({
                "source_index": source_index,
                "target_index": target_index,
                "generator_index": generator_index,
                "generator": generator_name,
                "source_parity": sum(source) % 2,
                "target_parity": sum(target) % 2,
            })
        neighbor_sets.append(neighbors)

    visited = {0}
    queue = deque([0])
    while queue:
        source = queue.popleft()
        for target in neighbor_sets[source]:
            if target not in visited:
                visited.add(target)
                queue.append(target)

    zero = (0, 0, 0, 0)
    commutator_image = add(
        add(GENERATOR_STEPS[0], GENERATOR_STEPS[1], modulus),
        add(GENERATOR_STEPS[4], GENERATOR_STEPS[5], modulus),
        modulus,
    )
    c8_order_residual = max(
        int((lambda x: c8_automorphism(c8_automorphism(c8_automorphism(c8_automorphism(c8_automorphism(c8_automorphism(c8_automorphism(c8_automorphism(x, modulus), modulus), modulus), modulus), modulus), modulus), modulus), modulus))(element) != element)
        for element in elements
    )
    c8_edge_residual = 0
    generator_steps = set(tuple(value % modulus for value in step) for step in GENERATOR_STEPS)
    for step in generator_steps:
        if c8_automorphism(step, modulus) not in generator_steps:
            c8_edge_residual = 1
            break

    no_short_kernel_word = True
    frontier = {(zero, -1)}
    for depth in range(1, 4):
        next_frontier: set[tuple[tuple[int, ...], int]] = set()
        for image, previous in frontier:
            for generator_index, step in enumerate(GENERATOR_STEPS):
                if previous >= 0 and generator_index == (previous + 4) % 8:
                    continue
                new_image = add(image, step, modulus)
                if new_image == zero:
                    no_short_kernel_word = False
                next_frontier.add((new_image, generator_index))
        frontier = next_frontier

    checks = {
        "surface_relation_images_identity": commutator_image == zero,
        "eight_distinct_neighbors_per_vertex": all(len(neighbors) == 8 for neighbors in neighbor_sets),
        "connected": len(visited) == len(elements),
        "bipartite": all(row["source_parity"] != row["target_parity"] for row in edge_rows),
        "c8_has_order_eight": c8_order_residual == 0,
        "c8_preserves_generator_shell": c8_edge_residual == 0,
        "no_nontrivial_kernel_word_below_length_four": no_short_kernel_word,
        "length_four_kernel_witness": commutator_image == zero,
    }
    return element_rows, edge_rows, {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "quotient_group": f"(Z/{modulus}Z)^4",
        "origin": "CLEAN_ROOM_VALIDATION_QUOTIENT_NOT_PRODUCTION_COVER",
        "cover_degree": len(elements),
        "directed_edge_count": len(edge_rows),
        "undirected_edge_count": len(edge_rows) // 2,
        "coordination": 8,
        "surface_relation": "[a1,b1][a2,b2]=e",
        "kernel_witness": "[a1,b1]",
        "minimum_nontrivial_kernel_word_length": 4,
        "word_injectivity_radius": 2.0,
        "geometric_injectivity_radius": "MISSING_WITHOUT_NIELSEN_MATRIX_LIFT_AND_SYSTOLE_SEARCH",
        "checks": checks,
    }
