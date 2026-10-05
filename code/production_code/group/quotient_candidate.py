"""Legacy standard-presentation-shell diagnostics for finite quotients.

``S8_PRESENTATION`` is the algebraic set
``{a1^+/-1,b1^+/-1,a2^+/-1,b2^+/-1}``.  The ``adjacency_matrix`` property in
this module is retained for historical regression and presentation-metric
diagnostics; it is not the physical nearest-neighbour operator. Production
physical adjacency is defined only in
``production_code.group.physical_adjacency`` from ``S8_GEOMETRIC``.

All tables contain integer element indices. Consequently relation, parity,
automorphism, diagnostic adjacency, and Hermiticity checks use exact arithmetic.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from functools import cached_property
import hashlib
import json
from itertools import permutations, product
from typing import Any, Mapping, Sequence


POSITIVE_GENERATORS = ("a1", "b1", "a2", "b2")
INVERSE_TOKEN = {
    "a1": "a1_inv",
    "a1_inv": "a1",
    "b1": "b1_inv",
    "b1_inv": "b1",
    "a2": "a2_inv",
    "a2_inv": "a2",
    "b2": "b2_inv",
    "b2_inv": "b2",
}
S8_PRESENTATION = ("a1", "b1", "a2", "b2", "a1_inv", "b1_inv", "a2_inv", "b2_inv")
RELATOR = ("a1", "b1", "a1_inv", "b1_inv", "a2", "b2", "a2_inv", "b2_inv")


def _compose_permutations(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right, i.e. (left*right)(x)=left(right(x))."""

    return tuple(left[right[index]] for index in range(len(left)))


@dataclass(frozen=True)
class FiniteQuotientCandidate:
    """Finite group and an epimorphism candidate from Gamma_B.

    ``multiplication_table[x][y]`` is the exact index of ``x*y``.
    ``phi8_permutation[x]`` is the proposed descended centered-octagon
    automorphism.  It is optional at construction time but its absence fails
    the production Q0 contract.
    """

    quotient_id: str
    element_labels: tuple[str, ...]
    multiplication_table: tuple[tuple[int, ...], ...]
    identity: int
    generator_images: Mapping[str, int]
    construction_method: str
    provenance: str
    phi8_permutation: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        order = len(self.element_labels)
        if order == 0 or len(self.multiplication_table) != order:
            raise ValueError("multiplication table must be nonempty and square")
        if not 0 <= self.identity < order:
            raise ValueError("identity index is outside the group")
        for row in self.multiplication_table:
            if len(row) != order or any(not 0 <= value < order for value in row):
                raise ValueError("multiplication table contains an invalid row or element index")
        if set(self.generator_images) != set(POSITIVE_GENERATORS):
            raise ValueError(f"generator_images must contain exactly {POSITIVE_GENERATORS}")
        if any(not 0 <= value < order for value in self.generator_images.values()):
            raise ValueError("generator image is outside the group")
        if self.phi8_permutation is not None and len(self.phi8_permutation) != order:
            raise ValueError("phi8 permutation has the wrong size")

    @property
    def order(self) -> int:
        return len(self.element_labels)

    def multiply(self, left: int, right: int) -> int:
        return self.multiplication_table[left][right]

    @cached_property
    def inverse_indices(self) -> tuple[int, ...]:
        result = []
        for element in range(self.order):
            matches = [
                other
                for other in range(self.order)
                if self.multiply(element, other) == self.identity
                and self.multiply(other, element) == self.identity
            ]
            result.append(matches[0] if len(matches) == 1 else -1)
        return tuple(result)

    @cached_property
    def s8_images(self) -> tuple[int, ...]:
        positive = tuple(self.generator_images[name] for name in POSITIVE_GENERATORS)
        negative = tuple(self.inverse_indices[value] for value in positive)
        return positive + negative

    def evaluate_word(self, word: Sequence[str]) -> int:
        image = self.identity
        token_images = dict(zip(S8_PRESENTATION, self.s8_images))
        for token in word:
            if token not in token_images:
                raise ValueError(f"unknown generator token: {token}")
            image = self.multiply(image, token_images[token])
        return image

    def right_regular_permutation(self, token: str) -> tuple[int, ...]:
        """Return the exact permutation x -> x*s for one S8_PRESENTATION token."""

        if token not in S8_PRESENTATION:
            raise ValueError(f"unknown generator token: {token}")
        generator = self.s8_images[S8_PRESENTATION.index(token)]
        return tuple(self.multiply(source, generator) for source in range(self.order))

    @cached_property
    def adjacency_matrix(self) -> tuple[tuple[int, ...], ...]:
        rows: list[tuple[int, ...]] = []
        for source in range(self.order):
            counts = Counter(self.multiply(source, generator) for generator in self.s8_images)
            rows.append(tuple(counts.get(target, 0) for target in range(self.order)))
        return tuple(rows)

    def _group_axiom_checks(self) -> dict[str, Any]:
        n = self.order
        table = self.multiplication_table
        identity = self.identity
        identity_exact = all(table[identity][x] == x and table[x][identity] == x for x in range(n))
        inverse_exact = all(value >= 0 for value in self.inverse_indices)
        rows_are_permutations = all(set(row) == set(range(n)) for row in table)
        associativity_exact = True
        witness = None
        for left in range(n):
            if not associativity_exact:
                break
            left_row = table[left]
            for middle in range(n):
                lm = left_row[middle]
                middle_row = table[middle]
                for right in range(n):
                    if table[lm][right] != left_row[middle_row[right]]:
                        associativity_exact = False
                        witness = [left, middle, right]
                        break
                if not associativity_exact:
                    break
        return {
            "identity_exact": identity_exact,
            "unique_two_sided_inverses": inverse_exact,
            "left_rows_are_permutations": rows_are_permutations,
            "associativity_exact": associativity_exact,
            "associativity_failure_witness": witness,
        }

    def _connectivity_and_degree(self) -> dict[str, Any]:
        visited = {self.identity}
        queue = deque([self.identity])
        while queue:
            source = queue.popleft()
            for generator in self.s8_images:
                target = self.multiply(source, generator)
                if target not in visited:
                    visited.add(target)
                    queue.append(target)
        simple_degrees = []
        maximum_multiplicity = 0
        repeated_rows = 0
        for source in range(self.order):
            neighbors = [self.multiply(source, generator) for generator in self.s8_images]
            counts = Counter(neighbors)
            simple_degrees.append(len(counts))
            maximum_multiplicity = max(maximum_multiplicity, max(counts.values()))
            repeated_rows += int(any(value > 1 for value in counts.values()))
        return {
            "connected": len(visited) == self.order,
            "generated_vertex_count": len(visited),
            "weighted_degree_exactly_8": all(sum(row) == 8 for row in self.adjacency_matrix),
            "simple_degree_exactly_8": all(value == 8 for value in simple_degrees),
            "simple_degree_min": min(simple_degrees),
            "simple_degree_max": max(simple_degrees),
            "maximum_edge_multiplicity": maximum_multiplicity,
            "vertices_with_repeated_neighbors": repeated_rows,
            "production_multiplicity_policy": "REQUIRE_EIGHT_DISTINCT_S8_PRESENTATION_NEIGHBORS",
        }

    def _algebraic_parity(self) -> dict[str, Any]:
        parity: list[int | None] = [None] * self.order
        parity[self.identity] = 0
        queue = deque([self.identity])
        conflict = None
        while queue and conflict is None:
            source = queue.popleft()
            assert parity[source] is not None
            for token, generator in zip(S8_PRESENTATION, self.s8_images):
                target = self.multiply(source, generator)
                proposed = 1 - int(parity[source])
                if parity[target] is None:
                    parity[target] = proposed
                    queue.append(target)
                elif parity[target] != proposed:
                    conflict = {
                        "source": source,
                        "generator": token,
                        "target": target,
                        "existing": parity[target],
                        "proposed": proposed,
                    }
                    break
        complete = all(value is not None for value in parity)
        homomorphism = complete and conflict is None
        multiplication_witness = None
        if homomorphism:
            for left in range(self.order):
                for right in range(self.order):
                    if parity[self.multiply(left, right)] != (int(parity[left]) + int(parity[right])) % 2:
                        homomorphism = False
                        multiplication_witness = [left, right]
                        break
                if not homomorphism:
                    break
        return {
            "algebraic_parity_exists": homomorphism,
            "parity_labels": parity if homomorphism else None,
            "edge_assignment_conflict": conflict,
            "multiplication_failure_witness": multiplication_witness,
        }

    def _graph_bipartite(self) -> dict[str, Any]:
        colors: list[int | None] = [None] * self.order
        conflict = None
        for root in range(self.order):
            if colors[root] is not None:
                continue
            colors[root] = 0
            queue = deque([root])
            while queue and conflict is None:
                source = queue.popleft()
                for target, multiplicity in enumerate(self.adjacency_matrix[source]):
                    if multiplicity == 0:
                        continue
                    expected = 1 - int(colors[source])
                    if colors[target] is None:
                        colors[target] = expected
                        queue.append(target)
                    elif colors[target] != expected:
                        conflict = [source, target]
                        break
            if conflict is not None:
                break
        return {
            "graph_bipartite": conflict is None,
            "graph_color_labels": colors if conflict is None else None,
            "graph_bipartite_conflict": conflict,
        }

    def _phi8_checks(self) -> dict[str, Any]:
        phi = self.phi8_permutation
        if phi is None:
            return {
                "phi8_supplied": False,
                "phi8_bijection": False,
                "phi8_group_automorphism": False,
                "phi8_order_exactly_8": False,
                "phi8_preserves_s8_multiset": False,
                "adjacency_covariance_exact": False,
                "adjacency_covariance_residual": None,
            }
        bijection = set(phi) == set(range(self.order))
        automorphism = bijection and phi[self.identity] == self.identity
        if automorphism:
            automorphism = all(
                phi[self.multiply(left, right)] == self.multiply(phi[left], phi[right])
                for left in range(self.order)
                for right in range(self.order)
            )
        powers = []
        current = tuple(range(self.order))
        for power in range(1, 9):
            current = tuple(phi[current[index]] for index in range(self.order))
            if current == tuple(range(self.order)):
                powers.append(power)
        order_eight = powers == [8]
        preserves_shell = Counter(phi[value] for value in self.s8_images) == Counter(self.s8_images)
        residual = 0
        if bijection:
            for source in range(self.order):
                for target in range(self.order):
                    residual = max(
                        residual,
                        abs(
                            self.adjacency_matrix[phi[source]][phi[target]]
                            - self.adjacency_matrix[source][target]
                        ),
                    )
        else:
            residual = -1
        return {
            "phi8_supplied": True,
            "phi8_bijection": bijection,
            "phi8_group_automorphism": automorphism,
            "phi8_order_exactly_8": order_eight,
            "phi8_preserves_s8_multiset": preserves_shell,
            "adjacency_covariance_exact": residual == 0,
            "adjacency_covariance_residual": residual,
        }

    def _adjacency_checks(self, parity: dict[str, Any]) -> dict[str, Any]:
        matrix = self.adjacency_matrix
        hermitian = all(matrix[left][right] == matrix[right][left] for left in range(self.order) for right in range(self.order))
        uniform_residual = max(abs(sum(row) - 8) for row in matrix)
        staggered_residual = None
        staggered_exact = False
        labels = parity["parity_labels"]
        if labels is not None:
            signs = [1 if value == 0 else -1 for value in labels]
            staggered_residual = max(
                abs(sum(matrix[source][target] * signs[target] for target in range(self.order)) + 8 * signs[source])
                for source in range(self.order)
            )
            staggered_exact = staggered_residual == 0
        return {
            "adjacency_hermitian_exact": hermitian,
            "adjacency_hermiticity_residual": 0 if hermitian else 1,
            "uniform_mode_eigenvalue_plus_8": uniform_residual == 0,
            "uniform_mode_residual": uniform_residual,
            "staggered_mode_applicable": labels is not None,
            "staggered_mode_eigenvalue_minus_8": staggered_exact,
            "staggered_mode_residual": staggered_residual,
        }

    @cached_property
    def q0_certificate(self) -> dict[str, Any]:
        axioms = self._group_axiom_checks()
        relation = self.evaluate_word(RELATOR) == self.identity if all(self.inverse_indices[value] >= 0 for value in self.generator_images.values()) else False
        inverse_pairing = all(
            self.multiply(self.s8_images[index], self.s8_images[index + 4]) == self.identity
            and self.multiply(self.s8_images[index + 4], self.s8_images[index]) == self.identity
            for index in range(4)
        )
        graph = self._connectivity_and_degree()
        parity = self._algebraic_parity()
        bipartite = self._graph_bipartite()
        phi8 = self._phi8_checks()
        adjacency = self._adjacency_checks(parity)
        checks = {
            **axioms,
            "surface_relation_exact": relation,
            "generator_inverse_pairing_exact": inverse_pairing,
            "right_regular_generator_maps_are_permutations": all(
                set(self.right_regular_permutation(token)) == set(range(self.order)) for token in S8_PRESENTATION
            ),
            "presentation_homomorphism_defined": relation and all(axioms[name] for name in (
                "identity_exact", "unique_two_sided_inverses", "associativity_exact"
            )),
            "epimorphism_surjective": relation and graph["connected"],
            "kernel_normal_by_homomorphism": relation and graph["connected"],
            **graph,
            **parity,
            **bipartite,
            "parity_and_graph_bipartiteness_agree": parity["algebraic_parity_exists"] == bipartite["graph_bipartite"],
            **phi8,
            **adjacency,
        }
        required = [
            "identity_exact",
            "unique_two_sided_inverses",
            "left_rows_are_permutations",
            "associativity_exact",
            "surface_relation_exact",
            "generator_inverse_pairing_exact",
            "right_regular_generator_maps_are_permutations",
            "presentation_homomorphism_defined",
            "epimorphism_surjective",
            "kernel_normal_by_homomorphism",
            "connected",
            "weighted_degree_exactly_8",
            "simple_degree_exactly_8",
            "algebraic_parity_exists",
            "graph_bipartite",
            "parity_and_graph_bipartiteness_agree",
            "phi8_bijection",
            "phi8_group_automorphism",
            "phi8_order_exactly_8",
            "phi8_preserves_s8_multiset",
            "adjacency_covariance_exact",
            "adjacency_hermitian_exact",
            "uniform_mode_eigenvalue_plus_8",
            "staggered_mode_eigenvalue_minus_8",
        ]
        failed = [name for name in required if not checks[name]]
        return {
            "schema_version": 1,
            "quotient_id": self.quotient_id,
            "candidate_order": self.order,
            "construction_method": self.construction_method,
            "provenance": self.provenance,
            "generator_convention": list(S8_PRESENTATION),
            "relation": "[a1,b1][a2,b2]=e",
            "checks": checks,
            "required_q0_checks": required,
            "failed_q0_checks": failed,
            "q0_status": "PASS" if not failed else "REJECT",
            "exact_arithmetic": True,
            "adjacency_sha256": self.adjacency_sha256,
        }

    @cached_property
    def adjacency_sha256(self) -> str:
        canonical = json.dumps(self.adjacency_matrix, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "quotient_id": self.quotient_id,
            "element_labels": list(self.element_labels),
            "multiplication_table": [list(row) for row in self.multiplication_table],
            "identity": self.identity,
            "generator_images": dict(self.generator_images),
            "construction_method": self.construction_method,
            "provenance": self.provenance,
            "phi8_permutation": list(self.phi8_permutation) if self.phi8_permutation is not None else None,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "FiniteQuotientCandidate":
        if value.get("schema_version") != 1:
            raise ValueError("unsupported candidate schema")
        phi = value.get("phi8_permutation")
        return cls(
            quotient_id=str(value["quotient_id"]),
            element_labels=tuple(str(item) for item in value["element_labels"]),
            multiplication_table=tuple(tuple(int(item) for item in row) for row in value["multiplication_table"]),
            identity=int(value["identity"]),
            generator_images={str(key): int(item) for key, item in value["generator_images"].items()},
            construction_method=str(value["construction_method"]),
            provenance=str(value["provenance"]),
            phi8_permutation=None if phi is None else tuple(int(item) for item in phi),
        )


def abelian_validation_candidate(modulus: int = 4) -> FiniteQuotientCandidate:
    """Build (Z/modulus Z)^4 with the validation signed-cycle phi8.

    This factory does not confer production status.  For modulus four its
    commutator kernel witness has length four and word r_inj=2, so it must be
    rejected by the registered production cutoff D_c/a=3.
    """

    if modulus < 2:
        raise ValueError("modulus must be at least two")
    elements = tuple(product(range(modulus), repeat=4))
    index = {element: number for number, element in enumerate(elements)}
    table = tuple(
        tuple(index[tuple((x + y) % modulus for x, y in zip(left, right))] for right in elements)
        for left in elements
    )
    basis = [[1 if axis == coordinate else 0 for coordinate in range(4)] for axis in range(4)]
    # Materialize after the compact basis expression to retain a transparent
    # generator convention in serialized output.
    basis_tuples = [tuple(row) for row in basis]
    phi = tuple(index[((-element[3]) % modulus, element[0], element[1], element[2])] for element in elements)
    return FiniteQuotientCandidate(
        quotient_id=f"QVAL_Z{modulus}_POWER4_N{modulus**4}",
        element_labels=tuple(",".join(map(str, element)) for element in elements),
        multiplication_table=table,
        identity=index[(0, 0, 0, 0)],
        generator_images=dict(zip(POSITIVE_GENERATORS, (index[element] for element in basis_tuples))),
        construction_method=f"direct product (Z/{modulus}Z)^4",
        provenance="CLEAN_ROOM_VALIDATION_FAMILY_NOT_PRODUCTION",
        phi8_permutation=phi,
    )


def symmetric_group_3_relation_failure_candidate() -> FiniteQuotientCandidate:
    """Exact negative fixture: S3 images that violate the surface relation."""

    elements = tuple(permutations(range(3)))
    index = {element: number for number, element in enumerate(elements)}
    table = tuple(
        tuple(index[_compose_permutations(left, right)] for right in elements)
        for left in elements
    )
    identity = index[(0, 1, 2)]
    transposition = index[(1, 0, 2)]
    three_cycle = index[(1, 2, 0)]
    return FiniteQuotientCandidate(
        quotient_id="NEG_S3_RELATION_FAILURE",
        element_labels=tuple("".join(map(str, element)) for element in elements),
        multiplication_table=table,
        identity=identity,
        generator_images={"a1": transposition, "b1": three_cycle, "a2": identity, "b2": identity},
        construction_method="exact S3 permutation table",
        provenance="NEGATIVE_UNIT_TEST_FIXTURE",
        phi8_permutation=None,
    )

def symmetric_group_3_validation_candidate() -> FiniteQuotientCandidate:
    """Reproduce the exact non-Abelian S3 quotient witness from VT-003.

    The generator images satisfy the surface relation and generate S3, but
    this fixture has repeated/involutory S8_PRESENTATION neighbors, no supplied centered
    phi8 descent, and cannot meet the production finite-cover contract.
    """

    elements = tuple(permutations(range(3)))
    index = {element: number for number, element in enumerate(elements)}
    table = tuple(
        tuple(index[_compose_permutations(left, right)] for right in elements)
        for left in elements
    )
    identity = index[(0, 1, 2)]
    a = index[(1, 0, 2)]
    b = index[(0, 2, 1)]
    return FiniteQuotientCandidate(
        quotient_id="VT003_S3_N6",
        element_labels=tuple("".join(map(str, element)) for element in elements),
        multiplication_table=table,
        identity=identity,
        generator_images={"a1": a, "b1": b, "a2": b, "b2": a},
        construction_method="exact S3 permutation quotient from validation_code/group/surface_relation.py",
        provenance="VT-003_NONABELIAN_RELATION_WITNESS_NOT_PRODUCTION",
        phi8_permutation=None,
    )
