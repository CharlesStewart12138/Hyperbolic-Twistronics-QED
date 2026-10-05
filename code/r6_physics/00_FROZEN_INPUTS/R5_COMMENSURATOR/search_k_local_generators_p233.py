from __future__ import annotations

import array
import json
import random
from collections import deque
from pathlib import Path


P = 233
D = 172  # u^2 = 2 + 2 sqrt(2) after sqrt(2) -> 85 mod 233
SQRT2 = 85
ZETA8 = 97
ALPHA = 86
NQ = 46080
ROOT = Path(__file__).resolve().parents[2]
TABLE_PATH = ROOT / "CONSTRUCTIVE_EXECUTION_R4" / "17_FINAL_FREEZE" / "artifacts" / "CAND-R4-0005.right_generators_u32le.bin"


def fadd(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def fneg(x: tuple[int, int]) -> tuple[int, int]:
    return ((-x[0]) % P, (-x[1]) % P)


def fsub(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return fadd(x, fneg(y))


def fmul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return ((x[0] * y[0] + D * x[1] * y[1]) % P, (x[0] * y[1] + x[1] * y[0]) % P)


def finv(x: tuple[int, int]) -> tuple[int, int]:
    den = (x[0] * x[0] - D * x[1] * x[1]) % P
    if den == 0:
        raise ZeroDivisionError(x)
    inv = pow(den, -1, P)
    return (x[0] * inv % P, -x[1] * inv % P)


def fdiv(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return fmul(x, finv(y))


ZERO = (0, 0)
ONE = (1, 0)


Matrix = tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]
IDENTITY: Matrix = (ONE, ZERO, ZERO, ONE)


def mmul(a: Matrix, b: Matrix) -> Matrix:
    return (
        fadd(fmul(a[0], b[0]), fmul(a[1], b[2])),
        fadd(fmul(a[0], b[1]), fmul(a[1], b[3])),
        fadd(fmul(a[2], b[0]), fmul(a[3], b[2])),
        fadd(fmul(a[2], b[1]), fmul(a[3], b[3])),
    )


def minv(a: Matrix) -> Matrix:
    det = fsub(fmul(a[0], a[3]), fmul(a[1], a[2]))
    di = finv(det)
    return tuple(fmul(di, x) for x in (a[3], fneg(a[1]), fneg(a[2]), a[0]))  # type: ignore[return-value]


def mpow(a: Matrix, n: int) -> Matrix:
    out = IDENTITY
    while n:
        if n & 1:
            out = mmul(out, a)
        a = mmul(a, a)
        n >>= 1
    return out


def scalar(n: int) -> tuple[int, int]:
    return (n % P, 0)


def geometric_generators() -> list[Matrix]:
    beta = (0, 1)
    result = []
    for nu in range(8):
        z = pow(ZETA8, nu, P)
        zi = pow(z, -1, P)
        result.append((scalar(ALPHA), fmul(beta, scalar(z)), fmul(beta, scalar(zi)), scalar(ALPHA)))
    return result


def projective_action(a: Matrix, x: tuple[int, int] | None) -> tuple[int, int] | None:
    if x is None:
        if a[2] == ZERO:
            return None
        return fdiv(a[0], a[2])
    num = fadd(fmul(a[0], x), a[1])
    den = fadd(fmul(a[2], x), a[3])
    if den == ZERO:
        return None
    return fdiv(num, den)


def quotient_apply(table: array.array[int], state: int, word: list[int]) -> int:
    for token in word:
        state = table[token * NQ + state]
    return state


def quotient_order(table: array.array[int], word: list[int]) -> int:
    state = 0
    for order in range(1, 2001):
        state = quotient_apply(table, state, word)
        if state == 0:
            return order
    raise RuntimeError("quotient order not found")


def matrix_word(gens: list[Matrix], word: list[int]) -> Matrix:
    out = IDENTITY
    for token in word:
        out = mmul(out, gens[token])
    return out


def orbit(gens: list[Matrix], start: tuple[int, int] | None = None, cap: int = 100000) -> set[tuple[int, int] | None]:
    moves = gens + [minv(g) for g in gens]
    seen = {start}
    queue = deque([start])
    while queue:
        point = queue.popleft()
        for move in moves:
            target = projective_action(move, point)
            if target not in seen:
                seen.add(target)
                queue.append(target)
                if len(seen) > cap:
                    return seen
    return seen


def main() -> None:
    raw = array.array("I")
    with TABLE_PATH.open("rb") as stream:
        raw.fromfile(stream, 8 * NQ)
    gens = geometric_generators()
    checks = {
        "sqrt2_square": SQRT2 * SQRT2 % P == 2,
        "zeta8_order": pow(ZETA8, 8, P) == 1 and pow(ZETA8, 4, P) == P - 1,
        "generator_determinants": all(fsub(fmul(g[0], g[3]), fmul(g[1], g[2])) == ONE for g in gens),
        "inverse_shell": all(mmul(gens[i], gens[i + 4]) == IDENTITY for i in range(4)),
    }

    rng = random.Random(20260915)
    kernel_records = []
    kernel_matrices: list[Matrix] = []
    best_orbit: set[tuple[int, int] | None] = {None}
    for attempt in range(1, 501):
        length = rng.randint(4, 14)
        word = [rng.randrange(8)]
        while len(word) < length:
            token = rng.randrange(8)
            if token != (word[-1] + 4) % 8:
                word.append(token)
        order = quotient_order(raw, word)
        base_matrix = matrix_word(gens, word)
        kernel_matrix = mpow(base_matrix, order)
        if kernel_matrix == IDENTITY:
            continue
        trial = kernel_matrices + [kernel_matrix]
        trial_orbit = orbit(trial, cap=1000)
        if len(trial_orbit) > len(best_orbit):
            expanded_word = word * order
            kernel_matrices.append(kernel_matrix)
            kernel_records.append({
                "attempt": attempt,
                "base_word_g_indices": word,
                "quotient_order": order,
                "kernel_word_length": len(expanded_word),
                "kernel_word_g_indices": expanded_word,
                "orbit_after_adjoining": len(trial_orbit),
            })
            best_orbit = trial_orbit
            if len(best_orbit) == P + 1:
                break

    payload = {
        "prime": P,
        "sqrt2_residue": SQRT2,
        "quadratic_extension": f"u^2={D} over F_{P}",
        "zeta8_residue": ZETA8,
        "checks": checks,
        "kernel_generators": kernel_records,
        "projective_orbit_size": len(best_orbit),
        "expected_local_hecke_degree": P + 1,
        "status": "PASS" if all(checks.values()) and len(best_orbit) == P + 1 else "FAIL",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
