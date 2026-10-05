"""Exact SL(2,p) x C2 scan for every PGL-induced C8 class (p=17,23).

Raw determinant-one matrices retain the central sign.  Automorphisms are
conjugation by canonical PGL matrices, and all SL seeds are enumerated.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import sys

from production_code.group.compact_pgl2_prime_search import PGL2


RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)
Mat = tuple[int, int, int, int]


def raw_mul(a: Mat, b: Mat, p: int) -> Mat:
    return ((a[0]*b[0]+a[1]*b[2])%p, (a[0]*b[1]+a[1]*b[3])%p,
            (a[2]*b[0]+a[3]*b[2])%p, (a[2]*b[1]+a[3]*b[3])%p)


def raw_inv(a: Mat, p: int) -> Mat:
    determinant = (a[0]*a[3]-a[1]*a[2]) % p
    scale = pow(determinant, -1, p)
    return (a[3]*scale%p, -a[1]*scale%p, -a[2]*scale%p, a[0]*scale%p)


def raw_pow(a: Mat, n: int, p: int) -> Mat:
    result: Mat = (1, 0, 0, 1)
    while n:
        if n & 1:
            result = raw_mul(result, a, p)
        a = raw_mul(a, a, p)
        n >>= 1
    return result


def conjugate(a: Mat, x: Mat, p: int) -> Mat:
    return raw_mul(raw_mul(a, x, p), raw_inv(a, p), p)


def reduced_ball_three() -> tuple[tuple[int, ...], ...]:
    words: list[tuple[int, ...]] = [()]
    shell: list[tuple[int, ...]] = [()]
    for _ in range(3):
        nxt = [w+(d,) for w in shell for d in range(8)
               if not w or d != (w[-1]+4)%8]
        words.extend(nxt)
        shell = nxt
    assert len(words) == 457
    return tuple(words)


def word_image(images: tuple[Mat, ...], word: tuple[int, ...], p: int) -> Mat:
    value: Mat = (1, 0, 0, 1)
    for digit in word:
        value = raw_mul(value, images[digit], p)
    return value


def generated_order(images: tuple[Mat, ...], p: int) -> int:
    identity: Mat = (1, 0, 0, 1)
    moves = images[:4] + tuple(raw_inv(x, p) for x in images[:4])
    seen = {identity}
    todo = [identity]
    while todo:
        value = todo.pop()
        for move in moves:
            target = raw_mul(value, move, p)
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return len(seen)


def scan(p: int) -> dict[str, object]:
    if p not in (17, 23):
        raise ValueError("only compact p=17,23 targets are supported")
    pgl = PGL2(p)
    ambient = pgl.elements()
    sl = tuple((a,b,c,d) for a in range(p) for b in range(p)
               for c in range(p) for d in range(p)
               if (a*d-b*c) % p == 1)
    assert len(sl) == p*(p*p-1)
    order8 = {a for a in ambient if pgl.power(a,8)==pgl.identity
              and pgl.power(a,4)!=pgl.identity}
    remaining = set(order8)
    classes = []
    while remaining:
        rep = min(remaining)
        orbit = {pgl.conjugate(z,rep) for z in ambient} & order8
        classes.append((rep,tuple(sorted(orbit))))
        remaining -= orbit
    assert sum(len(o) for _,o in classes) == len(order8)

    ball = reduced_ball_three()
    class_rows = []
    for class_index,(alpha,orbit) in enumerate(classes):
        powers = tuple(raw_pow(alpha,j,p) for j in range(8))
        counts: Counter[str] = Counter()
        hist: Counter[int] = Counter()
        survivors = []
        for seed in sl:
            counts["seeds"] += 1
            images = tuple(conjugate(powers[j],seed,p) for j in range(8))
            if images[4] != raw_inv(images[0],p):
                counts["inverse_fail"] += 1
                continue
            counts["inverse"] += 1
            if len(set(images)) != 8:
                counts["orbit_fail"] += 1
                continue
            counts["orbit8"] += 1
            if word_image(images,RELATOR,p) != (1,0,0,1):
                counts["relator_fail"] += 1
                continue
            counts["relator"] += 1
            keys={(word_image(images,w,p),len(w)&1) for w in ball}
            hist[len(keys)] += 1
            if len(keys) != 457:
                counts["B3_fail"] += 1
                continue
            counts["B3"] += 1
            if generated_order(images,p) != len(sl):
                counts["generation_fail"] += 1
                continue
            counts["generation"] += 1
            survivors.append(seed)
        class_rows.append({"class_index":class_index,"representative":list(alpha),
                           "class_size":len(orbit),"centralizer_size":len(ambient)//len(orbit),
                           "counts":dict(counts),"B3_histogram":{str(k):v for k,v in sorted(hist.items())},
                           "survivors":[list(x) for x in survivors]})
    return {"schema_version":"1.0","family":f"SL(2,{p}) x C2, all PGL-induced exact-order-eight classes",
            "orders":{"SL":len(sl),"PGL":len(ambient),"target":2*len(sl)},
            "physical_images":"g_j -> (alpha^j(x),1)","B3_word_count":457,
            "order8_elements_in_PGL":len(order8),"order8_classes_in_PGL":len(classes),
            "classes":class_rows,"totals":dict(sum((Counter(r["counts"]) for r in class_rows),Counter())),
            "exhaustiveness":"all exact-order-eight PGL classes and all determinant-one raw matrix seeds"}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: PRIME")
    result=scan(int(sys.argv[1]))
    payload=(json.dumps(result,indent=2,sort_keys=True)+"\n").encode()
    print(payload.decode(),end="")
    print("payload_sha256="+hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
