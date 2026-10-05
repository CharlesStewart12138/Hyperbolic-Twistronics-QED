"""Build the exact R5 commensurator example and its local branch registry.

This script is deliberately separate from the frozen R5 implementation. It uses
the independently reconstructed reduced Bolza generators and only reads the
frozen R4 quotient table.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
R4_TABLE = (
    WORKSPACE
    / "CONSTRUCTIVE_EXECUTION_R4"
    / "17_FINAL_FREEZE"
    / "artifacts"
    / "CAND-R4-0005.right_generators_u32le.bin"
)
OUT_JSON = HERE / "R5_COMM_EXAMPLE_CERTIFICATE.json"
OUT_TSV = HERE / "R5_COMM_BRANCH_REGISTRY.tsv"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def inverse_word(word: list[int]) -> list[int]:
    return [((token + 4) % 8) for token in reversed(word)]


def point_text(point, local) -> str:
    if point is None:
        return "INF"
    return f"{point[0]}+{point[1]}u"


def main() -> int:
    local = load_module(
        "r5_local_search", HERE / "search_k_local_generators_p233.py"
    )
    import array

    table = array.array("I")
    with R4_TABLE.open("rb") as stream:
        table.fromfile(stream, 8 * local.NQ)

    base_words = [
        [1, 3, 1, 0, 6, 4, 2, 7, 2, 0, 0, 1, 2, 3],
        [0, 7, 7, 2, 7, 1, 6, 4],
    ]
    quotient_orders = [local.quotient_order(table, w) for w in base_words]
    if quotient_orders != [8, 10]:
        raise AssertionError(f"unexpected quotient orders {quotient_orders}")

    kernel_words = [
        base_words[i] * quotient_orders[i] for i in range(len(base_words))
    ]
    generators = local.geometric_generators()
    kernel_matrices = [local.matrix_word(generators, w) for w in kernel_words]
    if any(local.quotient_apply(table, 0, w) != 0 for w in kernel_words):
        raise AssertionError("a claimed kernel word is nontrivial in Q")

    moves = []
    for i, (word, matrix) in enumerate(zip(kernel_words, kernel_matrices), start=1):
        moves.append((f"k{i}", word, matrix))
        inv_word = inverse_word(word)
        moves.append((f"k{i}^-1", inv_word, local.minv(matrix)))

    start = None
    queue = deque([start])
    paths: dict[object, tuple[str, ...]] = {start: ()}
    while queue:
        point = queue.popleft()
        for label, _word, matrix in moves:
            image = local.projective_action(matrix, point)
            if image not in paths:
                paths[image] = paths[point] + (label,)
                queue.append(image)

    if len(paths) != local.P + 1:
        raise AssertionError(f"P1 orbit has size {len(paths)}, expected {local.P + 1}")

    move_map = {label: word for label, word, _matrix in moves}
    rows = []
    for point, path in sorted(paths.items(), key=lambda item: point_text(item[0], local)):
        physical_word: list[int] = []
        for label in path:
            physical_word.extend(move_map[label])
        if local.quotient_apply(table, 0, physical_word) != 0:
            raise AssertionError("branch word left the frozen K-kernel")
        encoded_word = bytes(physical_word)
        record_seed = json.dumps(
            {"point": point_text(point, local), "moves": list(path)},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
        rows.append(
            {
                "branch_id": hashlib.sha256(record_seed).hexdigest(),
                "projective_point": point_text(point, local),
                "kernel_move_path": " ".join(path) if path else "identity",
                "physical_word_length": len(physical_word),
                "physical_word_sha256": hashlib.sha256(encoded_word).hexdigest(),
            }
        )

    header = [
        "branch_index",
        "branch_id",
        "projective_point",
        "kernel_move_path",
        "physical_word_length",
        "physical_word_sha256",
    ]
    lines = ["\t".join(header)]
    for index, row in enumerate(rows):
        lines.append(
            "\t".join(
                [
                    str(index),
                    row["branch_id"],
                    row["projective_point"],
                    row["kernel_move_path"],
                    str(row["physical_word_length"]),
                    row["physical_word_sha256"],
                ]
            )
        )
    OUT_TSV.write_text("\n".join(lines) + "\n", encoding="ascii")

    sqrt2_mod_233 = 85
    beta2_mod_233 = 172
    a0, a1 = 4, 1
    pi0 = a0 * a0 + 2 * a1 * a1 + 1
    pi1 = 2 * a0 * a1
    rational_norm = pi0 * pi0 - 2 * pi1 * pi1
    if (pi0, pi1, rational_norm) != (19, 8, 233):
        raise AssertionError("number-field norm identity failed")

    theta = 2.0 * math.atan(1.0 / (4.0 + math.sqrt(2.0)))
    m_theta = 234
    hilbert_dimension = 92160 * m_theta

    frozen_operator = load_module(
        "r5_frozen_operator",
        WORKSPACE
        / "OPERATOR_CLOSURE_R5"
        / "16_IMPLEMENTATION"
        / "global_operator_r5.py",
    )
    algorithm_run = frozen_operator.GLOBAL_OPERATOR_R5(
        twist_class=frozen_operator.TwistClass.COMMENSURATOR_NOT_NORMALIZER,
        support=(),
        correspondence_degree=m_theta,
    )

    certificate = {
        "schema": "r5-commensurator-example-certificate-v1",
        "status": "PASS",
        "construction": {
            "base_field": "Q(sqrt(2))",
            "quadratic_element": "I^2=-1",
            "projective_quaternion_element": "z=(4+sqrt(2))+I",
            "centered_angle": "theta_c=2*atan(1/(4+sqrt(2)))",
            "theta_c_radians": theta,
            "theta_c_in_reduced_interval": 0.0 < theta < math.pi / 8.0,
            "reduced_norm": "nrd(z)=19+8*sqrt(2)",
            "field_norm_of_reduced_norm": rational_norm,
            "prime_ideal_norm": 233,
            "classification": "commensurator-but-not-normalizer",
        },
        "local_place": {
            "rational_prime": 233,
            "sqrt2_mod_233": sqrt2_mod_233,
            "beta_square_mod_233": beta2_mod_233,
            "residue_field": "F_233",
            "hecke_tree_valency": 234,
        },
        "frozen_k_kernel": {
            "source_table": str(R4_TABLE),
            "source_table_sha256": sha256_file(R4_TABLE),
            "base_words": base_words,
            "base_word_orders_in_Q": quotient_orders,
            "kernel_word_lengths": [len(w) for w in kernel_words],
            "kernel_word_sha256": [
                hashlib.sha256(bytes(w)).hexdigest() for w in kernel_words
            ],
            "projective_orbit_size": len(paths),
            "full_local_action": len(paths) == 234,
        },
        "r5_comm_run": {
            "algorithm": "R5-COMM local correspondence branch enumeration",
            "branch_count": len(rows),
            "branch_registry": str(OUT_TSV),
            "branch_registry_sha256": sha256_file(OUT_TSV),
            "common_cover_index": m_theta,
            "hilbert_dimension": hilbert_dimension,
            "frozen_operator_metadata": algorithm_run,
            "physical_coefficient_matrix_materialized": False,
            "reason": (
                "The exact arithmetic correspondence and operator metadata are run; "
                "the 21,565,440-dimensional coefficient matrix is intentionally not "
                "materialized because no new numerical calculation was requested."
            ),
        },
        "checks": {
            "number_field_norm_identity": rational_norm == 233,
            "kernel_words_trivial_in_frozen_Q": True,
            "projective_line_complete": len(rows) == 234,
            "index_equals_q_plus_one": m_theta == 233 + 1,
            "dimension_formula": hilbert_dimension == 21_565_440,
            "operator_metadata_dimension": (
                algorithm_run["bilayer_dimension"] == hilbert_dimension
            ),
        },
    }
    certificate["status"] = (
        "PASS" if all(certificate["checks"].values()) else "FAIL"
    )
    OUT_JSON.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
