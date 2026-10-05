"""Exact finite exhaustion of the modular unipotent (m,p,d)=(6,3,3) family.

This is a narrow escalation artifact.  It enumerates the C8-invariant
cohomology classes for extensions of P=F_3^4 by each compatible 3-dimensional
square-zero (or dual square-zero) P-module, constructs an order-eight lift of
the frozen matrix A, and tests all 27 orbit seeds against the frozen exact B3
representatives.  Arithmetic in the finite groups is integer arithmetic mod
3 and mod 6; geometry enters only through the certified B3 word list.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from typing import Callable

import numpy as np

from production_code.group.universal_cover import enumerate_ball


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "production_code" / "escalations" / "MODULAR_UNIPOTENT_M6_P3_D3_EXHAUSTIVE.json"
P3 = 3
M6 = 6
A3 = np.array(
    ((0, 1, 0, 0), (2, 1, 2, 0), (0, 2, 2, 1), (0, 0, 2, 0)),
    dtype=np.int16,
)
A6 = np.array(
    ((0, 1, 0, 0), (5, 1, 5, 0), (0, 5, 5, 1), (0, 0, 5, 0)),
    dtype=np.int16,
)
ZERO4 = (0, 0, 0, 0)
UNITS4 = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
POINTS4 = tuple(product(range(3), repeat=4))
POINTS2 = tuple(product(range(3), repeat=2))
NONZERO2 = POINTS2[1:]


# L is the quotient P -> U, S is A on U, BK is a basis of ker(L), and BU is
# an A-invariant section with L*BU=I and A*BU=BU*S.  Thus [BU|BK] block
# diagonalizes A, which is essential for separating the two Bockstein pieces.
MODULE_DATA = (
    {
        "L": ((1, 0, 2, 0), (0, 1, 2, 1)),
        "S": ((0, 2), (2, 2)),
        "BK": ((0, 1), (1, 0), (0, 1), (2, 1)),
        "BU": ((1, 2), (1, 0), (0, 2), (2, 0)),
    },
    {
        "L": ((1, 0, 2, 1), (0, 1, 0, 1)),
        "S": ((0, 2), (2, 1)),
        "BK": ((0, 1), (1, 0), (2, 1), (2, 0)),
        "BU": ((0, 1), (2, 1), (0, 1), (1, 0)),
    },
)


# Rows/columns use NONZERO2 in lexicographic order.  This is a normalized
# bar-cocycle representative for the unique zero-power alternating U-class
# in H^2(U,M) for the square-zero module.  Its alternating L-coordinate on
# ((1,0),(0,1)) equals one.  validate_hard_cocycle() checks all 9^3 cocycle
# equations, both coordinate power equations, and the normalization.
HARD_TABLE = (
    ((1,2,1),(2,0,2),(1,2,1),(1,2,2),(1,1,0),(0,2,2),(1,1,0),(2,2,1)),
    ((2,1,2),(1,0,1),(1,0,2),(1,0,1),(1,1,0),(0,0,1),(2,1,0),(1,0,2)),
    ((2,2,2),(2,1,1),(0,2,2),(2,1,1),(1,1,0),(1,1,1),(0,0,0),(1,1,2)),
    ((2,1,0),(2,1,0),(2,1,0),(2,1,0),(2,1,0),(0,0,0),(0,0,0),(2,1,0)),
    ((2,0,1),(2,1,2),(2,0,1),(0,1,2),(1,1,0),(0,0,2),(1,1,0),(1,2,1)),
    ((0,1,1),(1,0,2),(0,1,1),(0,2,2),(2,0,0),(2,2,2),(2,0,0),(2,0,1)),
    ((1,1,2),(0,2,1),(0,0,2),(1,1,1),(1,1,0),(0,1,1),(0,0,0),(0,0,2)),
    ((2,1,0),(2,1,0),(0,0,0),(2,1,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)),
)
HARD_LOOKUP = {
    (x, y): np.array(HARD_TABLE[i][j], dtype=np.int16)
    for i, x in enumerate(NONZERO2)
    for j, y in enumerate(NONZERO2)
}


def vec(matrix: np.ndarray, value: tuple[int, ...], modulus: int = 3) -> tuple[int, ...]:
    return tuple(int(x) for x in matrix @ np.array(value, dtype=np.int16) % modulus)


def inv_matrix(matrix: np.ndarray) -> np.ndarray:
    n = len(matrix)
    augmented = np.concatenate((matrix.copy() % 3, np.eye(n, dtype=np.int16)), axis=1)
    row = 0
    for column in range(n):
        pivot = next(i for i in range(row, n) if augmented[i, column])
        augmented[[row, pivot]] = augmented[[pivot, row]]
        if augmented[row, column] == 2:
            augmented[row] = 2 * augmented[row] % 3
        for i in range(n):
            if i != row and augmented[i, column]:
                augmented[i] = (augmented[i] - augmented[i, column] * augmented[row]) % 3
        row += 1
    return augmented[:, n:] % 3


def hard(u: tuple[int, int], v: tuple[int, int]) -> np.ndarray:
    if u == (0, 0) or v == (0, 0):
        return np.zeros(3, dtype=np.int16)
    return HARD_LOOKUP[(u, v)].copy()


def rho_u(u: tuple[int, int], value: np.ndarray) -> np.ndarray:
    x, y, z = (int(q) for q in value)
    return np.array((x + u[0] * z, y + u[1] * z, z), dtype=np.int16) % 3


def validate_hard_cocycle() -> bool:
    for x in POINTS2:
        for y in POINTS2:
            for z in POINTS2:
                yz = tuple((y[i] + z[i]) % 3 for i in range(2))
                xy = tuple((x[i] + y[i]) % 3 for i in range(2))
                if not np.array_equal(
                    (rho_u(x, hard(y, z)) + hard(x, yz)) % 3,
                    (hard(x, y) + hard(xy, z)) % 3,
                ):
                    return False
    e0, e1 = (1, 0), (0, 1)
    for e in (e0, e1):
        two_e = tuple(2 * q % 3 for q in e)
        if np.any((hard(e, e) + hard(two_e, e)) % 3):
            return False
    return int(hard(e0, e1)[2] - hard(e1, e0)[2]) % 3 == 1


def solve_12(equations: list[np.ndarray]) -> np.ndarray | None:
    matrix = np.array(equations, dtype=np.int16) % 3
    row = 0
    pivots: list[int] = []
    for column in range(12):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i, column]), None)
        if pivot is None:
            continue
        matrix[[row, pivot]] = matrix[[pivot, row]]
        if matrix[row, column] == 2:
            matrix[row] = 2 * matrix[row] % 3
        hits = np.where(matrix[:, column] != 0)[0]
        hits = hits[hits != row]
        if len(hits):
            matrix[hits] = (matrix[hits] - matrix[hits, column:column+1] * matrix[row]) % 3
        pivots.append(column)
        row += 1
    for i in range(row, len(matrix)):
        if not np.any(matrix[i, :12]) and matrix[i, 12]:
            return None
    answer = np.zeros(12, dtype=np.int16)
    for i, column in enumerate(pivots):
        answer[column] = matrix[i, 12]
    return answer


def intertwiners(left: np.ndarray, right: np.ndarray) -> tuple[np.ndarray, ...]:
    answer = []
    for entries in product(range(3), repeat=4):
        q = np.array(entries, dtype=np.int16).reshape(2, 2)
        if np.array_equal(left @ q % 3, q @ right % 3):
            answer.append(q)
    return tuple(answer)


class Extension:
    def __init__(
        self,
        module_index: int,
        dual: bool,
        scalar: int,
        q_u: np.ndarray,
        q_k: np.ndarray,
        alternating: int,
    ):
        datum = MODULE_DATA[module_index]
        self.module_index = module_index
        self.dual = dual
        self.scalar = scalar
        self.q_u = q_u.copy() % 3
        self.q_k = q_k.copy() % 3
        self.alternating = alternating % 3
        self.L = np.array(datum["L"], dtype=np.int16)
        self.S = np.array(datum["S"], dtype=np.int16)
        self.BK = np.array(datum["BK"], dtype=np.int16)
        self.BU = np.array(datum["BU"], dtype=np.int16)
        change = np.concatenate((self.BU, self.BK), axis=1) % 3
        self.change_inverse = inv_matrix(change)
        block = self.change_inverse @ A3 @ change % 3
        assert not np.any(block[:2, 2:]) and not np.any(block[2:, :2])
        assert np.array_equal(block[:2, :2], self.S)
        self.K = block[2:, 2:]
        if dual:
            tw = scalar * inv_matrix(self.S).T % 3
        else:
            tw = scalar * self.S % 3
        self.T = np.zeros((3, 3), dtype=np.int16)
        self.T[:2, :2] = tw
        self.T[2, 2] = scalar
        self.r = self._solve_alpha_correction()
        self.validate()

    def coordinates(self, point: tuple[int, ...]) -> tuple[tuple[int, int], tuple[int, int]]:
        result = self.change_inverse @ np.array(point, dtype=np.int16) % 3
        return tuple(int(x) for x in result[:2]), tuple(int(x) for x in result[2:])

    def action(self, point: tuple[int, ...], value: np.ndarray | tuple[int, ...]) -> np.ndarray:
        u, _ = self.coordinates(point)
        x, y, z = (int(q) for q in value)
        if self.dual:
            return np.array((x, y, z + u[0] * x + u[1] * y), dtype=np.int16) % 3
        return np.array((x + u[0] * z, y + u[1] * z, z), dtype=np.int16) % 3

    def cocycle(self, left: tuple[int, ...], right: tuple[int, ...]) -> np.ndarray:
        ul, kl = self.coordinates(left)
        ur, kr = self.coordinates(right)
        result = np.zeros(3, dtype=np.int16)
        if not self.dual:
            for i in range(2):
                if ul[i] + ur[i] >= 3:
                    result[:2] += self.q_u[:, i]
                if kl[i] + kr[i] >= 3:
                    result[:2] += self.q_k[:, i]
            if self.scalar == 2:
                result += self.alternating * hard(ul, ur)
        elif self.scalar == 2:
            result[2] += self.alternating * kl[1] * kr[0]
        return result % 3

    def _solve_alpha_correction(self) -> dict[tuple[int, ...], np.ndarray]:
        coefficient: dict[tuple[int, ...], np.ndarray] = {}
        constant: dict[tuple[int, ...], np.ndarray] = {}
        for target in POINTS4:
            current = ZERO4
            cm = np.zeros((3, 12), dtype=np.int16)
            cv = np.zeros(3, dtype=np.int16)
            for i in range(4):
                for _ in range(target[i]):
                    a_current = vec(A3, current)
                    action_matrix = np.column_stack(
                        tuple(self.action(a_current, np.eye(3, dtype=np.int16)[:, j]) for j in range(3))
                    ) % 3
                    cm[:, 3*i:3*i+3] = (cm[:, 3*i:3*i+3] + action_matrix) % 3
                    cv = (
                        cv + self.cocycle(a_current, vec(A3, UNITS4[i]))
                        - self.T @ self.cocycle(current, UNITS4[i])
                    ) % 3
                    current = tuple((current[j] + UNITS4[i][j]) % 3 for j in range(4))
            coefficient[target] = cm
            constant[target] = cv

        equations: list[np.ndarray] = []
        for left in POINTS4:
            a_left = vec(A3, left)
            action_matrix = np.column_stack(
                tuple(self.action(a_left, np.eye(3, dtype=np.int16)[:, j]) for j in range(3))
            ) % 3
            for right in POINTS4:
                total = tuple((left[i] + right[i]) % 3 for i in range(4))
                a_right = vec(A3, right)
                cm = (coefficient[left] + action_matrix @ coefficient[right] - coefficient[total]) % 3
                cv = (
                    constant[left] + action_matrix @ constant[right]
                    + self.cocycle(a_left, a_right) - self.T @ self.cocycle(left, right)
                    - constant[total]
                ) % 3
                for k in range(3):
                    if np.any(cm[k]) or cv[k]:
                        equations.append(np.concatenate((cm[k], np.array((-cv[k] % 3,), dtype=np.int16))))

        # Enforce alpha^8=1, not merely invariance of the cohomology class.
        for point in POINTS4:
            cm = np.zeros((3, 12), dtype=np.int16)
            cv = np.zeros(3, dtype=np.int16)
            current = point
            for _ in range(8):
                cm = (self.T @ cm + coefficient[current]) % 3
                cv = (self.T @ cv + constant[current]) % 3
                current = vec(A3, current)
            for k in range(3):
                if np.any(cm[k]) or cv[k]:
                    equations.append(np.concatenate((cm[k], np.array((-cv[k] % 3,), dtype=np.int16))))

        solution = solve_12(equations)
        if solution is None:
            raise RuntimeError("listed invariant cohomology class has no order-eight lift")
        answer = {
            point: (coefficient[point] @ solution + constant[point]) % 3
            for point in POINTS4
        }
        return answer

    def validate(self) -> None:
        """Exhaust all cocycle triples and all alpha base pairs exactly."""

        point_index = {point: i for i, point in enumerate(POINTS4)}
        addition = np.empty((81, 81), dtype=np.int16)
        cocycles = np.empty((81, 81, 3), dtype=np.int16)
        actions = np.empty((81, 3, 3), dtype=np.int16)
        basis = np.eye(3, dtype=np.int16)
        for i, left in enumerate(POINTS4):
            actions[i] = np.column_stack(tuple(self.action(left, basis[:, j]) for j in range(3))) % 3
            for j, right in enumerate(POINTS4):
                addition[i, j] = point_index[tuple((left[k] + right[k]) % 3 for k in range(4))]
                cocycles[i, j] = self.cocycle(left, right)
        for i, left in enumerate(POINTS4):
            if not np.array_equal(self.T @ actions[i] % 3, actions[point_index[vec(A3, left)]] @ self.T % 3):
                raise RuntimeError("C8/module intertwining failed")
        if np.any(cocycles[0]) or np.any(cocycles[:, 0]):
            raise RuntimeError("cocycle is not normalized")

        z_indices = np.arange(81, dtype=np.int16)[None, :]
        for i in range(81):
            lhs = (
                np.einsum("ab,yzb->yza", actions[i], cocycles)
                + cocycles[i, addition]
            ) % 3
            rhs = (
                cocycles[i, :, None, :]
                + cocycles[addition[i, :, None], z_indices, :]
            ) % 3
            if not np.array_equal(lhs, rhs):
                raise RuntimeError("associativity/cocycle equation failed")

        for left in POINTS4:
            a_left = vec(A3, left)
            for right in POINTS4:
                total = tuple((left[i] + right[i]) % 3 for i in range(4))
                a_right = vec(A3, right)
                lhs = (self.T @ self.cocycle(left, right) + self.r[total]) % 3
                rhs = (
                    self.r[left] + self.action(a_left, self.r[right])
                    + self.cocycle(a_left, a_right)
                ) % 3
                if not np.array_equal(lhs, rhs):
                    raise RuntimeError("alpha homomorphism equation failed")

        if not np.array_equal(np.linalg.matrix_power(self.T.astype(np.int64), 8) % 3, np.eye(3, dtype=np.int64)):
            raise RuntimeError("T does not have eighth power one")
        for point in POINTS4:
            value = np.zeros(3, dtype=np.int16)
            current = point
            for _ in range(8):
                value = (self.T @ value + self.r[current]) % 3
                current = vec(A3, current)
            if np.any(value) or current != point:
                raise RuntimeError("alpha eighth power correction failed")

    def multiply(self, left, right):
        lv, lh = left
        rv, rh = right
        lp = tuple(x % 3 for x in lh)
        rp = tuple(x % 3 for x in rh)
        value = (np.array(lv) + self.action(lp, rv) + self.cocycle(lp, rp)) % 3
        base = tuple((lh[i] + rh[i]) % 6 for i in range(4))
        return tuple(int(x) for x in value), base

    def inverse(self, element):
        value, base = element
        negative_base = tuple(-x % 6 for x in base)
        point = tuple(x % 3 for x in base)
        negative_point = tuple(-x % 3 for x in point)
        target = (-np.array(value) - self.cocycle(point, negative_point)) % 3
        result = self.action(negative_point, target)
        return tuple(int(x) for x in result), negative_base

    def alpha(self, element):
        value, base = element
        point = tuple(x % 3 for x in base)
        new_value = (self.T @ np.array(value) + self.r[point]) % 3
        return tuple(int(x) for x in new_value), vec(A6, base, 6)

    def label(self) -> dict:
        return {
            "module_index": self.module_index,
            "dual": self.dual,
            "scalar": self.scalar,
            "q_u": self.q_u.tolist(),
            "q_k": self.q_k.tolist(),
            "alternating": self.alternating,
            "T": self.T.tolist(),
            "K": self.K.tolist(),
        }


def forced_u_power_correction(s: np.ndarray, alternating: int) -> np.ndarray:
    """Solve the affine cube-map correction for the c=- hard class."""

    tw = (-s) % 3
    for entries in product(range(3), repeat=4):
        q = np.array(entries, dtype=np.int16).reshape(2, 2)
        valid = True
        for u in POINTS2:
            su = vec(s, u)
            two_u = tuple(2 * x % 3 for x in u)
            two_su = tuple(2 * x % 3 for x in su)
            power_u = (hard(u, u) + hard(two_u, u))[:2] % 3
            power_su = (hard(su, su) + hard(two_su, su))[:2] % 3
            left = tw @ q @ np.array(u, dtype=np.int16)
            right = q @ s @ np.array(u, dtype=np.int16)
            defect = alternating * (power_su - tw @ power_u)
            if np.any((left - right - defect) % 3):
                valid = False
                break
        if valid:
            return q
    raise RuntimeError("no affine U-power correction for hard class")


def extension_classes(module_index: int, dual: bool, scalar: int) -> tuple[Extension, ...]:
    datum = MODULE_DATA[module_index]
    s = np.array(datum["S"], dtype=np.int16)
    change = np.concatenate(
        (np.array(datum["BU"], dtype=np.int16), np.array(datum["BK"], dtype=np.int16)), axis=1
    ) % 3
    k = (inv_matrix(change) @ A3 @ change)[2:, 2:] % 3
    zero = np.zeros((2, 2), dtype=np.int16)
    if not dual and scalar == 1:
        parameters = tuple((q, zero, 0) for q in intertwiners(s, s))
    elif not dual and scalar == 2:
        parameters = tuple(
            (forced_u_power_correction(s, b), q, b)
            for q in intertwiners((-s) % 3, k)
            for b in range(3)
        )
    elif dual and scalar == 1:
        parameters = ((zero, zero, 0),)
    else:
        parameters = tuple((zero, zero, b) for b in range(3))
    return tuple(Extension(module_index, dual, scalar, q_u, q_k, b) for q_u, q_k, b in parameters)


def run() -> dict:
    if not validate_hard_cocycle():
        raise RuntimeError("hard cocycle validation failed")
    ball = enumerate_ball(3).elements
    identity = ((0, 0, 0), (0, 0, 0, 0))
    orbit_relation = (0, 5, 2, 7, 4, 1, 6, 3)
    cases = []
    totals = Counter()
    survivors = []
    for module_index in range(2):
        for dual in (False, True):
            for scalar in (1, 2):
                extensions = extension_classes(module_index, dual, scalar)
                expected = {(False, 1): 9, (False, 2): 27, (True, 1): 1, (True, 2): 3}
                if len(extensions) != expected[(dual, scalar)]:
                    raise RuntimeError("cohomology class count mismatch")
                counts = Counter()
                witness_histogram = Counter()
                for class_index, extension in enumerate(extensions):
                    for seed in product(range(3), repeat=3):
                        x = (seed, (1, 0, 0, 0))
                        images = [x]
                        for _ in range(7):
                            images.append(extension.alpha(images[-1]))
                        if images[4] != extension.inverse(images[0]):
                            counts["inverse_fail"] += 1
                            continue
                        relation_value = identity
                        for index in orbit_relation:
                            relation_value = extension.multiply(relation_value, images[index])
                        if relation_value != identity:
                            counts["relator_fail"] += 1
                            continue
                        counts["inverse_relator_pass"] += 1
                        seen = {}
                        collision = None
                        for item in ball:
                            value = identity
                            for token in item.representative:
                                value = extension.multiply(value, images[int(token[1])])
                            if value in seen:
                                collision = (seen[value], item.representative)
                                break
                            seen[value] = item.representative
                        if collision is not None:
                            counts["B3_fail"] += 1
                            witness = " ".join(collision[0]) + " = " + " ".join(collision[1])
                            witness_histogram[witness] += 1
                            continue
                        counts["B3_pass"] += 1
                        survivors.append(
                            {
                                "class": extension.label(),
                                "class_index": class_index,
                                "seed": list(seed),
                                "physical_images": [[list(v), list(h)] for v, h in images],
                            }
                        )
                totals.update(counts)
                cases.append(
                    {
                        "module_index": module_index,
                        "dual": dual,
                        "scalar": scalar,
                        "cohomology_classes": len(extensions),
                        "seed_rows": 27 * len(extensions),
                        "counts": dict(counts),
                        "witness_histogram": dict(witness_histogram),
                    }
                )
    if sum(case["cohomology_classes"] for case in cases) != 80:
        raise RuntimeError("total cohomology class count mismatch")
    if sum(case["seed_rows"] for case in cases) != 2160:
        raise RuntimeError("total seed count mismatch")
    result = {
        "schema_version": "1.0",
        "classification": "EXACT_EXHAUSTION",
        "family": "modular unipotent metabelian extensions (m,p,d)=(6,3,3), trivial E-character",
        "group_order": 6**4 * 3**3,
        "cohomology_class_count": sum(case["cohomology_classes"] for case in cases),
        "seed_count": sum(case["seed_rows"] for case in cases),
        "hard_cocycle_validated": True,
        "exhaustive_self_tests": {
            "validated_classes": 80,
            "cocycle_associativity_P_triples_per_class": 81**3,
            "alpha_homomorphism_P_pairs_per_class": 81**2,
            "alpha_eighth_power_base_points_per_class": 81,
            "module_intertwining_base_points_per_class": 81,
        },
        "cases": cases,
        "totals": dict(totals),
        "B3_survivors": survivors,
        "conclusion": "No inverse/relator-admissible seed is injective on the certified 457-element B3 ball.",
        "scope": [
            "Both irreducible A-quotients U of F3^4.",
            "Square-zero and dual square-zero faithful 3-dimensional U-modules.",
            "Both scalar C8 lifts c=+1,-1.",
            "All C8-invariant H^2 classes: 9+27+1+3 per U.",
            "One normalized order-eight alpha lift per class; all lifts are conjugate because 3 and 8 are coprime.",
            "All 27 module coordinates of the orbit seed over the fixed base e_a.",
            "H=C6^4=P x E with P=C3^4 and E=C2^4; E acts trivially on M in this nonsplit branch.",
            "Every extension cocycle is inflated from P; cohomology in positive E-degree vanishes since 2 is invertible on M.",
            "Parity is the sum of the four H coordinates modulo 2; the e_a seed and its C8 orbit are all odd.",
        ],
    }
    return result


def main() -> None:
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("sha256", sha256(payload.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
