"""Exact universal-cover ball enumerator for the geometric Bolza shell.

Elements are deduplicated by exact matrices over
Q(sqrt(2), sqrt(2+2*sqrt(2)), i).  Coefficients are stored as normalized
dyadic integers in the ordered basis

    1, sqrt(2), beta, sqrt(2)*beta,
    i, i*sqrt(2), i*beta, i*sqrt(2)*beta.

This is a universal-cover reference.  It is not a finite quotient and it does
not define any quotient injectivity radius.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence
import csv
import gzip
import json
import math

import sympy as sp


FIELD_BASIS = (
    "1", "sqrt(2)", "beta", "sqrt(2)*beta",
    "i", "i*sqrt(2)", "i*beta", "i*sqrt(2)*beta",
)
GEOMETRIC_TOKENS = tuple(f"g{index}" for index in range(8))
GEOMETRIC_INVERSE = {f"g{index}": f"g{(index + 4) % 8}" for index in range(8)}
GEOMETRIC_RELATOR = ("g0", "g5", "g2", "g7", "g4", "g1", "g6", "g3")

# Field values are (denominator_power_of_two, eight integer numerators).
FieldValue = tuple[int, ...]
MatrixValue = tuple[FieldValue, FieldValue]  # SU(1,1) top row (a,b)


def _normalize(numerators: Sequence[int], exponent: int) -> FieldValue:
    values = tuple(int(value) for value in numerators)
    if not any(values):
        return (0, 0, 0, 0, 0, 0, 0, 0, 0)
    shift = min((abs(value) & -abs(value)).bit_length() - 1 for value in values if value)
    shift = min(int(exponent), shift)
    if shift:
        values = tuple(value >> shift for value in values)
        exponent -= shift
    return (int(exponent),) + values


ZERO: FieldValue = _normalize((0,) * 8, 0)
ONE: FieldValue = _normalize((1, 0, 0, 0, 0, 0, 0, 0), 0)


def _neg(value: FieldValue) -> FieldValue:
    return (value[0],) + tuple(-item for item in value[1:])


def _conjugate(value: FieldValue) -> FieldValue:
    return (value[0],) + value[1:5] + tuple(-item for item in value[5:9])


def _add(left: FieldValue, right: FieldValue) -> FieldValue:
    exponent = max(left[0], right[0])
    left_scale = 1 << (exponent - left[0])
    right_scale = 1 << (exponent - right[0])
    return _normalize(
        tuple(left[index] * left_scale + right[index] * right_scale for index in range(1, 9)),
        exponent,
    )


def _q2_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, int]:
    return (
        left[0] * right[0] + 2 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _q2_add(left: Sequence[int], right: Sequence[int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def _real4_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    p, q = left[:2], left[2:4]
    s, t = right[:2], right[2:4]
    ps = _q2_mul(p, s)
    qt = _q2_mul(q, t)
    # beta^2 = 2 + 2*sqrt(2).
    qt_beta2 = _q2_mul(qt, (2, 2))
    non_beta = _q2_add(ps, qt_beta2)
    beta_part = _q2_add(_q2_mul(p, t), _q2_mul(q, s))
    return non_beta + beta_part


def _mul(left: FieldValue, right: FieldValue) -> FieldValue:
    left_real, left_imag = left[1:5], left[5:9]
    right_real, right_imag = right[1:5], right[5:9]
    real = _q4_sub(_real4_mul(left_real, right_real), _real4_mul(left_imag, right_imag))
    imag = _q4_add(_real4_mul(left_real, right_imag), _real4_mul(left_imag, right_real))
    return _normalize(real + imag, left[0] + right[0])


def _q4_add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(left[index] + right[index] for index in range(4))


def _q4_sub(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(left[index] - right[index] for index in range(4))


def _field(real: Sequence[int], imag: Sequence[int] = (0, 0, 0, 0), exponent: int = 0) -> FieldValue:
    return _normalize(tuple(real) + tuple(imag), exponent)


ALPHA = _field((1, 1, 0, 0))
_PHASED_BETA = (
    _field((0, 0, 1, 0)),
    _field((0, 0, 0, 1), (0, 0, 0, 1), 1),
    _field((0, 0, 0, 0), (0, 0, 1, 0)),
    _field((0, 0, 0, -1), (0, 0, 0, 1), 1),
    _field((0, 0, -1, 0)),
    _field((0, 0, 0, -1), (0, 0, 0, -1), 1),
    _field((0, 0, 0, 0), (0, 0, -1, 0)),
    _field((0, 0, 0, 1), (0, 0, 0, -1), 1),
)
GENERATOR_MATRICES: tuple[MatrixValue, ...] = tuple((ALPHA, beta) for beta in _PHASED_BETA)
IDENTITY_MATRIX: MatrixValue = (ONE, ZERO)


def matrix_multiply(left: MatrixValue, right: MatrixValue) -> MatrixValue:
    """Multiply SU(1,1) matrices represented by their top rows."""

    a, b = left
    c, d = right
    return (
        _add(_mul(a, c), _mul(b, _conjugate(d))),
        _add(_mul(a, d), _mul(b, _conjugate(c))),
    )


def matrix_inverse(matrix: MatrixValue) -> MatrixValue:
    a, b = matrix
    return _conjugate(a), _neg(b)


def free_reduce_geometric(word: Sequence[str]) -> tuple[str, ...]:
    stack: list[str] = []
    for token in word:
        if token not in GEOMETRIC_INVERSE:
            raise ValueError(f"unknown geometric token: {token}")
        if stack and GEOMETRIC_INVERSE[token] == stack[-1]:
            stack.pop()
        else:
            stack.append(token)
    return tuple(stack)


def inverse_geometric_word(word: Sequence[str]) -> tuple[str, ...]:
    return tuple(GEOMETRIC_INVERSE[token] for token in reversed(tuple(word)))


def matrix_from_word(word: Sequence[str]) -> MatrixValue:
    product = IDENTITY_MATRIX
    for token in free_reduce_geometric(word):
        product = matrix_multiply(product, GENERATOR_MATRICES[int(token[1])])
    return product


def field_to_sympy(value: FieldValue) -> sp.Expr:
    root2 = sp.sqrt(2)
    beta = sp.sqrt(2 + 2 * root2)
    basis = (1, root2, beta, root2 * beta, sp.I, sp.I * root2, sp.I * beta, sp.I * root2 * beta)
    return sp.expand(sum(value[index + 1] * basis[index] for index in range(8)) / 2**value[0])


def field_to_complex(value: FieldValue) -> complex:
    root2 = math.sqrt(2.0)
    beta = math.sqrt(2.0 + 2.0 * root2)
    basis = (1.0, root2, beta, root2 * beta)
    real = sum(value[index + 1] * basis[index] for index in range(4))
    imag = sum(value[index + 5] * basis[index] for index in range(4))
    scale = float(1 << value[0])
    return complex(real / scale, imag / scale)


def exact_cosh_distance_over_R(matrix: MatrixValue) -> FieldValue:
    """Return exact cosh(d_H(0,M.0)/R)=2*|a|^2-1."""

    norm_a = _mul(matrix[0], _conjugate(matrix[0]))
    return _add(_add(norm_a, norm_a), _neg(ONE))


@dataclass(frozen=True)
class UniversalElement:
    element_id: int
    word_length: int
    representative: tuple[str, ...]
    matrix: MatrixValue


@dataclass(frozen=True)
class UniversalBall:
    max_radius: int
    elements: tuple[UniversalElement, ...]
    shell_counts: tuple[int, ...]
    shortest_relation_length: int | None
    shortest_relations: tuple[tuple[str, ...], ...]

    @property
    def ball_counts(self) -> tuple[int, ...]:
        running = 0
        result = []
        for count in self.shell_counts:
            running += count
            result.append(running)
        return tuple(result)


def enumerate_ball(max_radius: int = 6, relation_limit: int = 32) -> UniversalBall:
    radius = int(max_radius)
    if radius != max_radius or not 0 <= radius <= 8:
        raise ValueError("max_radius must be an integer from zero through eight")

    identity = UniversalElement(0, 0, (), IDENTITY_MATRIX)
    elements = [identity]
    visited: dict[MatrixValue, int] = {IDENTITY_MATRIX: 0}
    frontier = [identity]
    shell_counts = [1]
    shortest_length: int | None = None
    shortest: set[tuple[str, ...]] = set()

    for depth in range(1, radius + 1):
        next_frontier: list[UniversalElement] = []
        for element in frontier:
            for index, token in enumerate(GEOMETRIC_TOKENS):
                if element.representative and GEOMETRIC_INVERSE[token] == element.representative[-1]:
                    continue
                candidate_word = element.representative + (token,)
                candidate_matrix = matrix_multiply(element.matrix, GENERATOR_MATRICES[index])
                prior_id = visited.get(candidate_matrix)
                if prior_id is None:
                    candidate = UniversalElement(len(elements), depth, candidate_word, candidate_matrix)
                    visited[candidate_matrix] = candidate.element_id
                    elements.append(candidate)
                    next_frontier.append(candidate)
                    continue

                prior_word = elements[prior_id].representative
                relation = free_reduce_geometric(candidate_word + inverse_geometric_word(prior_word))
                if not relation:
                    continue
                relation_length = len(relation)
                if shortest_length is None or relation_length < shortest_length:
                    shortest_length = relation_length
                    shortest = {relation}
                elif relation_length == shortest_length and len(shortest) < relation_limit:
                    shortest.add(relation)
        frontier = next_frontier
        shell_counts.append(len(frontier))

    return UniversalBall(
        max_radius=radius,
        elements=tuple(elements),
        shell_counts=tuple(shell_counts),
        shortest_relation_length=shortest_length,
        shortest_relations=tuple(sorted(shortest)[:relation_limit]),
    )


def inverse_index(ball: UniversalBall) -> tuple[int, ...]:
    lookup = {element.matrix: element.element_id for element in ball.elements}
    return tuple(lookup[matrix_inverse(element.matrix)] for element in ball.elements)


def write_ball_artifacts(ball: UniversalBall, output_dir: Path) -> dict[str, Path]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    inverse_ids = inverse_index(ball)
    matrix_path = directory / f"ball_radius_{ball.max_radius}_exact.jsonl.gz"
    spacing_over_R = 2.0 * math.acosh(1.0 + math.sqrt(2.0))

    with gzip.open(matrix_path, "wt", encoding="utf-8", newline="\n") as handle:
        for element in ball.elements:
            a, b = element.matrix
            denominator = _conjugate(a)
            cosh_exact = exact_cosh_distance_over_R(element.matrix)
            cosh_value = max(1.0, field_to_complex(cosh_exact).real)
            distance_over_R = math.acosh(cosh_value)
            z = field_to_complex(b) / field_to_complex(denominator)
            row = {
                "element_id": element.element_id,
                "minimum_geometric_word_length": element.word_length,
                "representative": list(element.representative),
                "inverse_element_id": inverse_ids[element.element_id],
                "matrix_top_row_exact": [list(a), list(b)],
                "orbit_coordinate_exact_homogeneous": {
                    "numerator_b": list(b),
                    "denominator_conjugate_a": list(denominator),
                },
                "orbit_coordinate_decimal": [format(z.real, ".17g"), format(z.imag, ".17g")],
                "cosh_distance_over_R_exact": list(cosh_exact),
                "distance_over_R": format(distance_over_R, ".17g"),
                "distance_over_a_B": format(distance_over_R / spacing_over_R, ".17g"),
            }
            handle.write(json.dumps(row, separators=(",", ":")) + "\n")

    counts_path = directory / "shell_counts_radii_0_6.csv"
    with counts_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("radius", "shell_count", "ball_count", "inverse_pairs_nonidentity", "first_shell_degree"))
        for radius, (shell, total) in enumerate(zip(ball.shell_counts, ball.ball_counts)):
            writer.writerow((radius, shell, total, (total - 1) // 2, 8))

    relations_path = directory / "shortest_relations.json"
    relations_path.write_text(json.dumps({
        "shortest_relation_length": ball.shortest_relation_length,
        "relations": [list(word) for word in ball.shortest_relations],
        "registered_polygon_relator": list(GEOMETRIC_RELATOR),
    }, indent=2), encoding="utf-8")

    manifest_path = directory / "UNIVERSAL_COVER_MANIFEST.json"
    manifest_path.write_text(json.dumps({
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-UC",
        "scope": "universal cover; not a finite quotient",
        "generating_shell": list(GEOMETRIC_TOKENS),
        "field_basis": list(FIELD_BASIS),
        "field_encoding": "[denominator_power_of_two,n0,...,n7]",
        "matrix_encoding": "SU(1,1) top row (a,b); lower row is (conjugate(b),conjugate(a))",
        "orbit_coordinate_encoding": "z=b/conjugate(a), archived exactly as a homogeneous numerator/denominator pair",
        "distance_identity": "cosh(d_H(0,M.0)/R)=2*|a|^2-1",
        "maximum_radius": ball.max_radius,
        "shell_counts": list(ball.shell_counts),
        "ball_counts": list(ball.ball_counts),
        "shortest_relation_length": ball.shortest_relation_length,
        "first_shell_degree": 8,
        "identity_method": [
            "free inverse cancellation",
            "exact normalized algebraic SU(1,1) matrix equality",
            "decimal coordinates are reporting-only and never identify elements",
        ],
        "word_injectivity_is_geometric_injectivity": False,
        "files": [matrix_path.name, counts_path.name, relations_path.name],
    }, indent=2), encoding="utf-8")

    return {
        "elements": matrix_path,
        "counts": counts_path,
        "relations": relations_path,
        "manifest": manifest_path,
    }

