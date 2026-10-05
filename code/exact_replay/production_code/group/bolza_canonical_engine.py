"""Bounded proof-grade canonical interface for the physical Bolza shell.

The present certificate intentionally limits its uniqueness statement to the
exact breadth-first domain ``|g|_geom <= 6``.  It is the regression gate for
later streaming infrastructure, not a claim that a complete automatic
structure has already been constructed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from production_code.group.geometric_shell_contract import certificate as shell_certificate
from production_code.group.nielsen import certificate as nielsen_certificate
from production_code.group.physical_parity import geometric_shell_parities
from production_code.group.universal_cover import (
    GENERATOR_MATRICES,
    GEOMETRIC_RELATOR,
    IDENTITY_MATRIX,
    MatrixValue,
    UniversalBall,
    enumerate_ball,
    exact_cosh_distance_over_R,
    inverse_index,
    matrix_from_word,
    matrix_inverse,
    matrix_multiply,
)


ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "production_code" / "group" / "CM_AUTO_001_CERTIFICATE.json"
OUT_MD = ROOT / "production_code" / "group" / "CM_AUTO_001_CERTIFICATE.md"
EXPECTED_SHELLS = (1, 8, 56, 392, 2736, 19096, 133288)
EXPECTED_BALLS = (1, 9, 65, 457, 3193, 22289, 155577)


def _matrix_payload(matrix: MatrixValue) -> list[list[int]]:
    return [list(matrix[0]), list(matrix[1])]


def matrix_id(matrix: MatrixValue) -> str:
    """Content address for one exact normalized algebraic SU(1,1) matrix."""

    payload = json.dumps(_matrix_payload(matrix), separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class BoundedCanonicalIndex:
    maximum_word_length: int
    ball: UniversalBall
    word_by_matrix: dict[MatrixValue, tuple[str, ...]]

    @classmethod
    def build(cls, maximum_word_length: int = 6) -> "BoundedCanonicalIndex":
        if not 0 <= maximum_word_length <= 6:
            raise ValueError("proof-grade bounded index is certified only for depths 0..6")
        ball = enumerate_ball(maximum_word_length)
        mapping = {element.matrix: element.representative for element in ball.elements}
        if len(mapping) != len(ball.elements):
            raise RuntimeError("exact matrix collision escaped breadth-first canonicalization")
        return cls(maximum_word_length, ball, mapping)

    def canonical_word(self, matrix: MatrixValue) -> tuple[str, ...]:
        try:
            return self.word_by_matrix[matrix]
        except KeyError as exc:
            raise KeyError("matrix is outside the certified bounded ball") from exc

    def contains_word(self, word: Iterable[str]) -> bool:
        return matrix_from_word(tuple(word)) in self.word_by_matrix


def build_certificate() -> dict[str, Any]:
    index = BoundedCanonicalIndex.build(6)
    ball = index.ball
    inverses = inverse_index(ball)
    shell = shell_certificate()
    nielsen = nielsen_certificate()

    ordered_matrix_hash = hashlib.sha256()
    for element in ball.elements:
        ordered_matrix_hash.update(bytes.fromhex(matrix_id(element.matrix)))

    first_shell_cosh = [exact_cosh_distance_over_R(matrix) for matrix in GENERATOR_MATRICES]
    tests = {
        "shell_counts_exact": ball.shell_counts == EXPECTED_SHELLS,
        "ball_counts_exact": ball.ball_counts == EXPECTED_BALLS,
        "shortlex_first_discovery_unique_in_certified_domain": len(index.word_by_matrix) == len(ball.elements),
        "inverse_pairing_exact": all(
            inverses[inverses[i]] == i
            and matrix_inverse(ball.elements[i].matrix) == ball.elements[inverses[i]].matrix
            for i in range(len(ball.elements))
        ),
        "registered_surface_relator_exact": matrix_from_word(GEOMETRIC_RELATOR) == IDENTITY_MATRIX,
        "generator_inverse_products_exact": all(
            matrix_multiply(GENERATOR_MATRICES[i], GENERATOR_MATRICES[(i + 4) % 8]) == IDENTITY_MATRIX
            for i in range(8)
        ),
        "exact_orbit_coordinate_inputs": len(set(first_shell_cosh)) == 1 and len(set(GENERATOR_MATRICES)) == 8,
        "physical_degree_eight": shell.gsc04_universal_centre_orbit_degree_eight,
        "C8_action_exact": shell.gsc05_c8_cyclic_action,
        "physical_shell_nielsen_transport_exact": shell.gsc07_exact_nielsen_words and nielsen.exact_matrix_reconstruction,
        "physical_shell_parity_odd": geometric_shell_parities() == (1,) * 8,
        "deterministic_repeat_prefix": tuple(e.matrix for e in enumerate_ball(4).elements) == tuple(e.matrix for e in ball.elements[:3193]),
    }
    if not all(tests.values()):
        raise RuntimeError(f"CM-AUTO-001 regression failure: {tests}")

    return {
        "schema_version": "1.0",
        "task_id": "CM-AUTO-001",
        "classification": "BOUNDED_CANONICAL_ENGINE_CERTIFIED",
        "status": "Done",
        "scientific_scope": "exact physical Bolza shell; bounded word-length regression only",
        "canonical_order": "breadth-first minimum physical-geometric word length, then generator order g0<...<g7",
        "identity_semantics": "normalized exact Q(sqrt(2),sqrt(2+2sqrt(2)),i) SU(1,1) matrix equality",
        "certified_unique_domain": {"minimum_geometric_word_length_maximum": 6, "elements": len(ball.elements)},
        "shell_counts": list(ball.shell_counts),
        "ball_counts": list(ball.ball_counts),
        "shortest_relation_length": ball.shortest_relation_length,
        "ordered_exact_matrix_sha256": ordered_matrix_hash.hexdigest(),
        "automatic_group_environment": {"GAP": False, "KBMAG": False, "SageMath": False, "libgap": False},
        "tests": tests,
        "large_state_policy": {
            "python_per_state_objects_permitted_here": True,
            "reason": "The complete regression domain has 155,577 states, below the 10^6 directive threshold.",
            "per_state_python_objects_permitted_above_1e6": False,
        },
        "nonclaims": [
            "No complete shortlex/geodesic automatic structure beyond depth 6 is claimed.",
            "No global systole proof or m=7 tensor result is issued by this task.",
            "No approximate matrix or disk-coordinate identity is used.",
        ],
        "next_gate": {"CM_STREAM_001_released": True, "deep_proof_search_released": False},
        "main_tex_modified": False,
    }


def render_markdown(c: dict[str, Any]) -> str:
    rows = "\n".join(f"| `{name}` | {'PASS' if value else 'FAIL'} |" for name, value in c["tests"].items())
    return f"""# CM-AUTO-001 bounded Bolza canonical engine

## Result

The exact breadth-first canonical interface is certified through physical
geometric word length 6.  It contains **{c['certified_unique_domain']['elements']:,}**
distinct exact SU(1,1) matrices and reproduces the frozen shell and ball counts.

Canonical order is minimum physical-geometric word length followed by
`g0<...<g7`.  Equality uses normalized algebraic matrices, never rounded disk
coordinates.

| Regression | Result |
|---|---|
{rows}

## Scope boundary

GAP, KBMAG, SageMath and libgap are absent.  This task therefore does **not**
claim a complete automatic/geodesic language beyond depth 6.  It releases the
prefix-sharding infrastructure task, whose own acceptance must preserve
complete generation and exact per-shard accounting.  Deep proof searches and
the m=7 scientific run remain closed until their additional gates pass.

`main.tex` remains unchanged.
"""


def main() -> None:
    cert = build_certificate()
    OUT_JSON.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(cert), encoding="utf-8")


if __name__ == "__main__":
    main()
