"""Exact PSL(2,p) x C2 orbit-seed scan for PGL-induced C8 automorphisms.

This companion is intentionally independent of the earlier PGL target scan.
Projective matrices are normalized by making the first nonzero row-major
entry one.  PSL(2,p) is the determinant-square subgroup of PGL(2,p).
For every PGL conjugacy class of exact-order-eight elements a and every
x in PSL, the physical images are (a^j x a^-j,1), j=0,...,7.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from production_code.group.compact_pgl2_prime_search import PGL2


RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


def reduced_ball_three() -> tuple[tuple[int, ...], ...]:
    words: list[tuple[int, ...]] = [()]
    shell: list[tuple[int, ...]] = [()]
    for _depth in range(3):
        nxt: list[tuple[int, ...]] = []
        for word in shell:
            for digit in range(8):
                if word and digit == (word[-1] + 4) % 8:
                    continue
                nxt.append(word + (digit,))
        words.extend(nxt)
        shell = nxt
    assert len(words) == 457
    return tuple(words)


def word_image(pgl: PGL2, images, word):
    value = pgl.identity
    for digit in word:
        value = pgl.multiply(value, images[digit])
    return value


def scan(prime: int) -> dict[str, object]:
    if prime not in (17, 23, 31):
        raise ValueError("supported primes are 17,23,31")
    pgl = PGL2(prime)
    ambient = pgl.elements()
    psl = tuple(x for x in ambient if not pgl.odd(x))
    assert len(ambient) == prime * (prime * prime - 1)
    assert len(psl) * 2 == len(ambient)

    order8 = {
        a for a in ambient
        if pgl.power(a, 8) == pgl.identity and pgl.power(a, 4) != pgl.identity
    }
    remaining = set(order8)
    classes = []
    while remaining:
        representative = min(remaining)
        orbit = {pgl.conjugate(z, representative) for z in ambient}
        orbit &= order8
        classes.append((representative, tuple(sorted(orbit))))
        remaining -= orbit
    assert sum(len(orbit) for _, orbit in classes) == len(order8)

    b3_words = reduced_ball_three()
    class_rows = []
    for class_index, (alpha, orbit) in enumerate(classes):
        powers = tuple(pgl.power(alpha, j) for j in range(8))
        counts: Counter[str] = Counter()
        b3_hist: Counter[int] = Counter()
        survivors = []
        for seed in psl:
            counts["seeds"] += 1
            images = tuple(pgl.conjugate(powers[j], seed) for j in range(8))
            if images[4] != pgl.inverse(images[0]):
                counts["inverse_fail"] += 1
                continue
            counts["inverse"] += 1
            if len(set(images)) != 8:
                counts["orbit_fail"] += 1
                continue
            counts["orbit8"] += 1
            if word_image(pgl, images, RELATOR) != pgl.identity:
                counts["relator_fail"] += 1
                continue
            counts["relator"] += 1
            image_keys = {
                (word_image(pgl, images, word), len(word) & 1)
                for word in b3_words
            }
            b3_hist[len(image_keys)] += 1
            if len(image_keys) != 457:
                counts["B3_fail"] += 1
                continue
            counts["B3"] += 1
            generated = pgl.generated_order(images)
            if generated != len(psl):
                counts["generation_fail"] += 1
                continue
            counts["generation"] += 1
            survivors.append(seed)
        class_rows.append({
            "class_index": class_index,
            "representative": list(alpha),
            "class_size": len(orbit),
            "centralizer_size": len(ambient) // len(orbit),
            "counts": dict(counts),
            "B3_histogram": {str(k): v for k, v in sorted(b3_hist.items())},
            "survivors": [list(x) for x in survivors],
        })

    return {
        "schema_version": "1.0",
        "family": f"PSL(2,{prime}) x C2 with all PGL-induced exact-order-eight automorphism classes",
        "field_encoding": f"F_{prime} integers 0,...,{prime-1}",
        "projective_canonicalization": "scale first nonzero row-major entry to one",
        "orders": {"PSL": len(psl), "PGL": len(ambient), "target": 2 * len(psl)},
        "physical_images": "g_j -> (alpha^j(x),1)",
        "parity": "external direct C2; all physical generators odd",
        "order8_elements_in_PGL": len(order8),
        "order8_classes_in_PGL": len(classes),
        "classes": class_rows,
        "totals": dict(sum((Counter(row["counts"]) for row in class_rows), Counter())),
        "B3_word_count": len(b3_words),
        "exhaustiveness": "all PGL conjugacy classes of exact-order-eight elements and all PSL seeds",
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: PRIME")
    result = scan(int(sys.argv[1]))
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    print(encoded.decode(), end="")
    print("payload_sha256=" + hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
