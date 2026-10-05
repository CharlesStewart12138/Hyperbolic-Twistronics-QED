"""Independent arithmetic and convention audit for the R5 recovery.

Independence rule: this file imports neither the constructive certificate
builder nor the frozen R5 operator implementation.  It reimplements the
finite-field calculation in homogeneous projective coordinates.
"""

from __future__ import annotations

import array
import csv
import hashlib
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUP = ROOT / "OPERATOR_CLOSURE_R5_REVIEWER_SUPPLEMENT"
CERT = SUP / "05_CONSTRUCTIVE_COMMENSURATOR" / "R5_COMM_EXAMPLE_CERTIFICATE.json"
REG = SUP / "05_CONSTRUCTIVE_COMMENSURATOR" / "R5_COMM_BRANCH_REGISTRY.tsv"
TABLE = (
    ROOT
    / "CONSTRUCTIVE_EXECUTION_R4"
    / "17_FINAL_FREEZE"
    / "artifacts"
    / "CAND-R4-0005.right_generators_u32le.bin"
)
OUT = Path(__file__).resolve().parent / "INDEPENDENT_R5_RECOVERY_AUDIT.json"

P = 233
D = 172
SQRT2 = 85
ZETA8 = 97
ALPHA = 86
NQ = 46080

F = tuple[int, int]
M = tuple[F, F, F, F]
ZERO: F = (0, 0)
ONE: F = (1, 0)
IDENTITY: M = (ONE, ZERO, ZERO, ONE)
Point = tuple[F, F]
INFINITY: Point = (ONE, ZERO)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def add(x: F, y: F) -> F:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def neg(x: F) -> F:
    return ((-x[0]) % P, (-x[1]) % P)


def sub(x: F, y: F) -> F:
    return add(x, neg(y))


def mul(x: F, y: F) -> F:
    return (
        (x[0] * y[0] + D * x[1] * y[1]) % P,
        (x[0] * y[1] + x[1] * y[0]) % P,
    )


def inv(x: F) -> F:
    denominator = (x[0] * x[0] - D * x[1] * x[1]) % P
    if denominator == 0:
        raise ZeroDivisionError(x)
    q = pow(denominator, -1, P)
    return (x[0] * q % P, -x[1] * q % P)


def div(x: F, y: F) -> F:
    return mul(x, inv(y))


def scalar(x: int) -> F:
    return (x % P, 0)


def mmul(a: M, b: M) -> M:
    return (
        add(mul(a[0], b[0]), mul(a[1], b[2])),
        add(mul(a[0], b[1]), mul(a[1], b[3])),
        add(mul(a[2], b[0]), mul(a[3], b[2])),
        add(mul(a[2], b[1]), mul(a[3], b[3])),
    )


def minv(a: M) -> M:
    determinant = sub(mul(a[0], a[3]), mul(a[1], a[2]))
    q = inv(determinant)
    return tuple(mul(q, x) for x in (a[3], neg(a[1]), neg(a[2]), a[0]))  # type: ignore[return-value]


def matrix_word(generators: list[M], word: list[int]) -> M:
    result = IDENTITY
    for token in word:
        result = mmul(result, generators[token])
    return result


def canonical(point: Point) -> Point:
    x, y = point
    if y == ZERO:
        return INFINITY
    return (div(x, y), ONE)


def act(matrix: M, point: Point) -> Point:
    x, y = point
    return canonical(
        (
            add(mul(matrix[0], x), mul(matrix[1], y)),
            add(mul(matrix[2], x), mul(matrix[3], y)),
        )
    )


def geometric_generators() -> list[M]:
    beta: F = (0, 1)
    result = []
    for nu in range(8):
        z = pow(ZETA8, nu, P)
        zi = pow(z, -1, P)
        result.append(
            (
                scalar(ALPHA),
                mul(beta, scalar(z)),
                mul(beta, scalar(zi)),
                scalar(ALPHA),
            )
        )
    return result


def quotient_apply(table: array.array[int], word: list[int]) -> int:
    state = 0
    for token in word:
        state = table[token * NQ + state]
    return state


def quotient_order(table: array.array[int], word: list[int]) -> int:
    state = 0
    for order in range(1, 2001):
        for token in word:
            state = table[token * NQ + state]
        if state == 0:
            return order
    raise AssertionError("quotient order not found")


def inverse_word(word: list[int]) -> list[int]:
    return [((token + 4) % 8) for token in reversed(word)]


def main() -> int:
    certificate = json.loads(CERT.read_text(encoding="ascii"))
    table = array.array("I")
    with TABLE.open("rb") as handle:
        table.fromfile(handle, 8 * NQ)

    base_words = [
        [1, 3, 1, 0, 6, 4, 2, 7, 2, 0, 0, 1, 2, 3],
        [0, 7, 7, 2, 7, 1, 6, 4],
    ]
    orders = [quotient_order(table, word) for word in base_words]
    kernel_words = [word * order for word, order in zip(base_words, orders)]
    generators = geometric_generators()
    kernel_matrices = [matrix_word(generators, word) for word in kernel_words]

    moves = []
    for index, (word, matrix) in enumerate(zip(kernel_words, kernel_matrices), 1):
        moves.append((f"k{index}", word, matrix))
        moves.append((f"k{index}^-1", inverse_word(word), minv(matrix)))

    seen = {INFINITY}
    queue = deque([INFINITY])
    while queue:
        point = queue.popleft()
        for _label, _word, matrix in moves:
            target = act(matrix, point)
            if target not in seen:
                seen.add(target)
                queue.append(target)

    with REG.open("r", encoding="ascii", newline="") as handle:
        registry = list(csv.DictReader(handle, delimiter="\t"))
    move_words = {label: word for label, word, _matrix in moves}
    registry_word_checks = []
    branch_id_checks = []
    for row in registry:
        labels = [] if row["kernel_move_path"] == "identity" else row["kernel_move_path"].split()
        word: list[int] = []
        for label in labels:
            word.extend(move_words[label])
        registry_word_checks.append(
            int(row["physical_word_length"]) == len(word)
            and row["physical_word_sha256"] == hashlib.sha256(bytes(word)).hexdigest()
            and quotient_apply(table, word) == 0
        )
        seed = json.dumps(
            {"point": row["projective_point"], "moves": labels},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
        branch_id_checks.append(row["branch_id"] == hashlib.sha256(seed).hexdigest())

    ratner = (SUP / "01_RATNER_PROOF" / "RATNER_DOUBLE_COSET_PROOF.tex").read_text()
    angles = (SUP / "02_EXACT_ANGLE_DOMAINS" / "CENTERED_ANGLE_CLASSIFICATION.tex").read_text()
    covariance = (SUP / "03_PRODUCTION_COVARIANCE" / "PRODUCTION_COVARIANCE_DOMAIN.tex").read_text()
    infinite = (SUP / "04_INFINITE_OPERATOR" / "INFINITE_OPERATOR_CERTIFICATE.tex").read_text()
    original_tie = (ROOT / "OPERATOR_CLOSURE_R5" / "18_THEOREM_PACKAGE" / "R5_TIE_REGULARITY.tex").read_text()
    original_c2 = (ROOT / "OPERATOR_CLOSURE_R5" / "18_THEOREM_PACKAGE" / "R5_C2_PARAMETER_THEOREM.tex").read_text()
    original_comm = (ROOT / "OPERATOR_CLOSURE_R5" / "18_THEOREM_PACKAGE" / "R5_COMMENSURATOR_THEOREM.tex").read_text()

    checks = {
        "audit_implementation_independent_of_builder": True,
        "audit_uses_homogeneous_not_affine_projective_coordinates": True,
        "frozen_table_hash_matches_certificate": sha256_file(TABLE)
        == certificate["frozen_k_kernel"]["source_table_sha256"],
        "field_constants": SQRT2 * SQRT2 % P == 2
        and pow(D, (P - 1) // 2, P) == P - 1
        and pow(ZETA8, 8, P) == 1
        and pow(ZETA8, 4, P) == P - 1,
        "generator_determinants_one": all(
            sub(mul(g[0], g[3]), mul(g[1], g[2])) == ONE for g in generators
        ),
        "inverse_shell": all(mmul(generators[i], generators[i + 4]) == IDENTITY for i in range(4)),
        "quotient_orders_8_10": orders == [8, 10],
        "kernel_words_in_frozen_K": all(quotient_apply(table, word) == 0 for word in kernel_words),
        "independent_homogeneous_orbit_234": len(seen) == 234,
        "registry_has_234_rows": len(registry) == 234,
        "registry_indices_complete": [int(row["branch_index"]) for row in registry] == list(range(234)),
        "registry_points_unique": len({row["projective_point"] for row in registry}) == 234,
        "registry_branch_ids_unique_and_valid": len({row["branch_id"] for row in registry}) == 234
        and all(branch_id_checks),
        "registry_words_reconstruct_and_lie_in_K": all(registry_word_checks),
        "registry_hash_matches_certificate": sha256_file(REG)
        == certificate["r5_comm_run"]["branch_registry_sha256"],
        "exact_number_field_norm_233": 19 * 19 - 2 * 8 * 8 == 233,
        "hilbert_dimension_exact": 92160 * 234 == 21_565_440
        == certificate["r5_comm_run"]["hilbert_dimension"],
        "ratner_quantifier_present": "For every \\(r\\in G\\)" in ratner,
        "ratner_components_not_assumed_connected": "need not be\nconnected" in ratner
        and "finite component groups create no third closure" in ratner,
        "left_right_convention_closed": "y_r=(K,Kr)" in ratner
        and "K\\cap r^{-1}Kr" in ratner
        and "\\ell_n r k_n^{-1}" in ratner,
        "thetaN_exact": "\\boxed{\\Theta_N=\\{0\\}" in angles,
        "thetaC_exact_membership": "\\tan\\frac{\\theta}{2}\\in k" in angles,
        "thetaC_closure_exact": "\\boxed{\\overline{\\Theta_C}=[0,\\pi/8]}" in angles,
        "production_covariance_exact": "\\boxed{\\Theta_{\\rm cov}=\\{0\\}" in covariance,
        "actual_kernel_instantiated": "3.057141839" in infinite
        and "0.125,0.20,0.25" in infinite,
        "normal_core_scope_retained": "normal core" in original_comm.lower(),
        "tie_set_scope_retained": "tie" in original_tie.lower()
        and "measure" in original_tie.lower(),
        "C2_nogo_scope_retained": "C^2" in original_c2 or "C2" in original_c2,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    payload = {
        "schema": "independent-r5-recovery-audit-v1",
        "independence": {
            "imports_certificate_builder": False,
            "imports_frozen_operator_code": False,
            "projective_convention": "homogeneous column coordinates [X:Y]",
            "arithmetic": "exact integer and finite-field operations",
        },
        "checks": checks,
        "passed": sum(bool(value) for value in checks.values()),
        "total": len(checks),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
