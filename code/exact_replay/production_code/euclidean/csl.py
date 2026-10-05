"""Exact square coincidence-site-lattice arithmetic.

MANUSCRIPT SOURCE:
Equation: Eqs. (204)–(414), including Sigma, C_M, B_M and representatives.
Section: Euclidean square-bilayer commensurability.
Model scope: exact integer geometry; no floating-angle inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import atan, gcd, pi


Matrix2 = tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]


@dataclass(frozen=True)
class SquareCSL:
    m: int
    n: int
    parity_divisor: int
    sigma: int
    n_sc: int
    cos_theta: Fraction
    sin_theta: Fraction
    theta: float
    p: int
    q: int
    direct_basis_over_a: Matrix2
    reciprocal_basis_over_2pi_over_a: Matrix2
    representatives: tuple[tuple[int, int], ...]


def _primitive_pair(m: int, n: int) -> tuple[int, int]:
    if isinstance(m, bool) or isinstance(n, bool) or not isinstance(m, int) or not isinstance(n, int):
        raise TypeError("m and n must be integers")
    if not (m > n > 0) or gcd(m, n) != 1:
        raise ValueError("require a primitive pair m>n>0 with gcd(m,n)=1")
    return m, n


def parity_divisor(m: int, n: int) -> int:
    """Return d=1 for opposite parity and d=2 for both-odd data."""

    m, n = _primitive_pair(m, n)
    return 2 if (m & 1) and (n & 1) else 1


def reduced_gaussian_pair(m: int, n: int) -> tuple[int, int]:
    """Return (p,q) from the unified primitive CSL basis formula."""

    d = parity_divisor(m, n)
    if d == 1:
        return m, n
    return (m + n) // 2, (n - m) // 2


def complementary_pair(m: int, n: int) -> tuple[int, int]:
    """Return (m^sharp,n^sharp)=((m+n)/d,(m-n)/d)."""

    d = parity_divisor(m, n)
    return (m + n) // d, (m - n) // d


def csl(m: int, n: int) -> SquareCSL:
    """Construct the exact rotation, primitive direct/reciprocal bases and quotient.

    MANUSCRIPT SOURCE:
    Equation: rational rotation, parity divisor, Eqs. for Sigma, C_M and B_M.
    Section: exact square CSL arithmetic.
    Model scope: one primitive rational half-angle pair.
    """

    m, n = _primitive_pair(m, n)
    d = parity_divisor(m, n)
    norm = m*m + n*n
    sigma = norm // d
    p, q = reduced_gaussian_pair(m, n)
    direct: Matrix2 = ((Fraction(p), Fraction(-q)), (Fraction(q), Fraction(p)))
    reciprocal: Matrix2 = tuple(tuple(entry / sigma for entry in row) for row in direct)  # type: ignore[assignment]
    return SquareCSL(
        m=m,
        n=n,
        parity_divisor=d,
        sigma=sigma,
        n_sc=2*sigma,
        cos_theta=Fraction(m*m - n*n, norm),
        sin_theta=Fraction(2*m*n, norm),
        theta=2.0*atan(Fraction(n, m)),
        p=p,
        q=q,
        direct_basis_over_a=direct,
        reciprocal_basis_over_2pi_over_a=reciprocal,
        representatives=tuple((j, 0) for j in range(sigma)),
    )


def reduced_representative(m: int, n: int) -> SquareCSL:
    """Return the unique crystallographic representative in (0,pi/4)."""

    cell = csl(m, n)
    if cell.theta <= pi/4.0:
        return cell
    return csl(*complementary_pair(m, n))


def all_subhundred_cells() -> tuple[SquareCSL, ...]:
    """Derive every nontrivial crystallographic class with 2*Sigma<100."""

    unique: dict[tuple[int, Fraction, Fraction], SquareCSL] = {}
    for m in range(2, 10):
        for n in range(1, m):
            if gcd(m, n) != 1:
                continue
            cell = csl(m, n)
            if cell.n_sc >= 100:
                continue
            reduced = reduced_representative(m, n)
            unique[(reduced.sigma, reduced.cos_theta, reduced.sin_theta)] = reduced
    return tuple(sorted(unique.values(), key=lambda cell: cell.theta))

