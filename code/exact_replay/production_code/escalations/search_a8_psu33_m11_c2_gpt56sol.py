#!/usr/bin/env python3
"""Proof-complete direct orbit-seed scans in A8, PSU(3,3), and M11, times C2.

Permutation convention: p*q means composition p after q.  Each physical
generator maps to (x_j,1), where x_j=alpha^j(x_0).  The parity coordinate is
therefore the word length modulo two.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import struct
import time
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BALL = ROOT / "data/production/universal_cover/ball_radius_6_exact.jsonl.gz"
TREE = ROOT / "data/production/quotient_separator/based_tree_meta.bin"
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)


def mul(p: bytes, q: bytes) -> bytes:
    return bytes(p[i] for i in q)


def inv(p: bytes) -> bytes:
    z = bytearray(len(p))
    for i, j in enumerate(p):
        z[j] = i
    return bytes(z)


def power(p: bytes, n: int) -> bytes:
    r = bytes(range(len(p)))
    while n:
        if n & 1:
            r = mul(r, p)
        p = mul(p, p)
        n >>= 1
    return r


def order(p: bytes) -> int:
    seen = bytearray(len(p))
    out = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j, n = i, 0
        while not seen[j]:
            seen[j] = 1
            n += 1
            j = p[j]
        out = math.lcm(out, n)
    return out


def cycles(p: bytes) -> str:
    seen = bytearray(len(p))
    out = []
    for i in range(len(p)):
        if seen[i] or p[i] == i:
            seen[i] = 1
            continue
        c, j = [], i
        while not seen[j]:
            seen[j] = 1
            c.append(j + 1)
            j = p[j]
        out.append("(" + " ".join(map(str, c)) + ")")
    return "".join(out) or "()"


def closure(generators: list[bytes], expected: int | None = None) -> list[bytes]:
    identity = bytes(range(len(generators[0])))
    elements = [identity]
    known = {identity}
    q = deque([identity])
    while q:
        x = q.popleft()
        for g in generators:
            y = mul(x, g)
            if y not in known:
                known.add(y)
                elements.append(y)
                q.append(y)
                if expected is not None and len(elements) > expected:
                    raise RuntimeError(f"group exceeded expected order {expected}")
    if expected is not None and len(elements) != expected:
        raise RuntimeError(f"group order {len(elements)} != {expected}")
    return elements


def perm_from_cycles(n: int, cs: list[tuple[int, ...]]) -> bytes:
    p = list(range(n))
    for c in cs:
        for a, b in zip(c, c[1:] + c[:1]):
            p[a - 1] = b - 1
    return bytes(p)


def a8_data():
    n = 8
    a = perm_from_cycles(n, [(1, 2, 3)])
    b = perm_from_cycles(n, [(2, 3, 4, 5, 6, 7, 8)])
    base_gens = [a, b]
    base = closure(base_gens, 20160)
    transposition = perm_from_cycles(n, [(1, 2)])
    aut_gens = base_gens + [transposition]
    aut = closure(aut_gens, 40320)
    return "A8", base, base_gens, aut, aut_gens, {
        "representation": "natural degree-8 permutation action",
        "base_generators": [cycles(x) for x in base_gens],
        "automorphism_extension_generator": cycles(transposition),
    }


def m11_data():
    n = 11
    a = perm_from_cycles(n, [tuple(range(1, 12))])
    b = perm_from_cycles(n, [(3, 7, 11, 8), (4, 10, 5, 6)])
    base_gens = [a, b]
    base = closure(base_gens, 7920)
    # Aut(M11)=M11, so the same faithful degree-11 action is the full
    # automorphism group (conjugation is faithful because M11 is centerless).
    return "M11", base, base_gens, base, base_gens, {
        "representation": "natural sharply 4-transitive degree-11 permutation action",
        "base_generators": [cycles(x) for x in base_gens],
        "automorphism_group_identification": "Aut(M11)=M11",
    }


# F9 = F3[u]/(u^2+1), encoded a+bu as a+3b.
def fadd(x: int, y: int) -> int:
    return ((x % 3 + y % 3) % 3) + 3 * ((x // 3 + y // 3) % 3)


def fneg(x: int) -> int:
    return ((-x) % 3) + 3 * ((-(x // 3)) % 3)


def fmul(x: int, y: int) -> int:
    a, b, c, d = x % 3, x // 3, y % 3, y // 3
    return ((a * c + 2 * b * d) % 3) + 3 * ((a * d + b * c) % 3)


def fconj(x: int) -> int:
    return (x % 3) + 3 * ((-(x // 3)) % 3)


FINV = [0] * 9
for _x in range(1, 9):
    for _y in range(1, 9):
        if fmul(_x, _y) == 1:
            FINV[_x] = _y


def vscale(v: tuple[int, int, int], a: int):
    return tuple(fmul(a, x) for x in v)


def vnorm(v: tuple[int, int, int]):
    for x in v:
        if x:
            return vscale(v, FINV[x])
    raise ValueError("zero projective vector")


def hermitian(v: tuple[int, int, int], w: tuple[int, int, int]):
    z = 0
    for x, y in zip(v, w):
        z = fadd(z, fmul(fconj(x), y))
    return z


def psu33_data():
    points = sorted({vnorm((a, b, c)) for a in range(9) for b in range(9)
                     for c in range(9) if (a or b or c) and hermitian((a, b, c), (a, b, c)) == 0})
    if len(points) != 28:
        raise RuntimeError(f"unitary isotropic point count {len(points)} != 28")
    pindex = {v: i for i, v in enumerate(points)}

    # Unitary transvection T_v(w)=w+u*v*h(v,w), with u^bar=-u.
    u = 3
    transvections = []
    for v in points:
        image = []
        for w in points:
            coefficient = fmul(u, hermitian(v, w))
            z = tuple(fadd(w[i], fmul(coefficient, v[i])) for i in range(3))
            image.append(pindex[vnorm(z)])
        transvections.append(bytes(image))

    # Two generators are selected deterministically only after verifying that
    # their closure is all 6048 elements; fall back to the full proven set.
    base_gens = transvections
    base = closure(base_gens, 6048)
    sigma = bytes(pindex[vnorm(tuple(fconj(x) for x in v))] for v in points)
    aut_gens = base_gens + [sigma]
    aut = closure(aut_gens, 12096)
    return "PSU(3,3)", base, base_gens, aut, aut_gens, {
        "representation": "faithful degree-28 action on isotropic points of PG(2,9)",
        "field_encoding": "F9=F3[u]/(u^2+1), a+bu encoded a+3b",
        "hermitian_form": "h(v,w)=sum(conjugate(v_i)*w_i)",
        "base_generators": "28 unitary transvections T_v(w)=w+u*v*h(v,w)",
        "automorphism_extension_generator": "coordinate Frobenius a+bu -> a-bu",
        "isotropic_points_encoded": [list(v) for v in points],
    }


def conjugacy_classes_order8(aut: list[bytes], aut_gens: list[bytes]):
    order8 = {x for x in aut if order(x) == 8}
    total = len(order8)
    reps = []
    gens = aut_gens + [inv(g) for g in aut_gens]
    while order8:
        rep = min(order8)
        orbit = {rep}
        q = deque([rep])
        while q:
            x = q.popleft()
            for g in gens:
                y = mul(mul(g, x), inv(g))
                if y not in orbit:
                    orbit.add(y)
                    q.append(y)
        if not orbit <= order8:
            raise RuntimeError("order-8 conjugacy orbit escaped order-8 inventory")
        order8.difference_update(orbit)
        reps.append((rep, len(orbit)))
    if sum(z for _, z in reps) != total:
        raise RuntimeError("order-8 class partition mismatch")
    return total, reps


def load_b3():
    words = []
    h = hashlib.sha256()
    with gzip.open(BALL, "rt", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec["minimum_geometric_word_length"] <= 3:
                word = tuple(int(x[1:]) for x in rec["representative"])
                words.append((rec["element_id"], word))
    if len(words) != 457:
        raise RuntimeError(f"B3 size {len(words)} != 457")
    with BALL.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return words, h.hexdigest()


def eval_word(images: list[bytes], word: tuple[int, ...], identity: bytes):
    x = identity
    for g in word:
        x = mul(x, images[g])
    return x


def subgroup_size(images: list[bytes], cap: int):
    identity = bytes(range(len(images[0])))
    seen = {identity}
    q = deque([identity])
    while q:
        x = q.popleft()
        for g in images:
            y = mul(x, g)
            if y not in seen:
                seen.add(y)
                q.append(y)
                if len(seen) > cap:
                    raise RuntimeError("subgroup exceeded base group")
    return len(seen)


def scan_based(images: list[bytes], group: list[bytes]):
    index = {x: i for i, x in enumerate(group)}
    identity_index = index[bytes(range(len(images[0])))]
    transitions = [[0] * len(group) for _ in range(8)]
    for g in range(8):
        for i, x in enumerate(group):
            transitions[g][i] = index[mul(x, images[g])]
    with TREE.open("rb") as f:
        header = f.read(20)
        magic, count, record_size = struct.unpack("<8sQI", header)
        if magic != b"BOLZAT01" or count != 23_129_593 or record_size != 8:
            raise RuntimeError("based-tree header drift")
        states = [0] * count
        for node in range(count):
            raw = f.read(8)
            if len(raw) != 8:
                raise RuntimeError("short based tree")
            parent, generator, depth, reserved = struct.unpack("<IBBH", raw)
            if node == 0:
                if parent != 0 or depth != 0:
                    raise RuntimeError("bad based-tree root")
                states[0] = identity_index
                continue
            if parent >= node or generator >= 8:
                raise RuntimeError("bad based-tree edge")
            states[node] = transitions[generator][states[parent]]
            # Product identity requires base identity and even parity.
            if depth % 2 == 0 and states[node] == identity_index:
                word = []
                current = node
                # A second sequential pass would be needed to reconstruct all
                # ancestors without retaining metadata; retain the exact node.
                return {"pass": False, "witness_node": node, "witness_depth": depth}
    return {"pass": True, "nodes_scanned": count}


def scan_group(data, b3_words, do_based: bool):
    name, base, base_gens, aut, aut_gens, encoding = data
    started = time.perf_counter()
    identity = bytes(range(len(base[0])))
    base_set = set(base)
    total_order8, classes = conjugacy_classes_order8(aut, aut_gens)
    result = {
        "group": name,
        "base_order": len(base),
        "product_order": 2 * len(base),
        "permutation_degree": len(base[0]),
        "encoding": encoding,
        "automorphism_order": len(aut),
        "exact_order8_automorphisms": total_order8,
        "exact_order8_conjugacy_classes": len(classes),
        "classes": [],
    }
    for class_index, (alpha, class_size) in enumerate(classes):
        if power(alpha, 8) != identity or power(alpha, 4) == identity:
            raise RuntimeError("automorphism representative does not have exact order 8")
        alpha_inv = inv(alpha)
        alpha_map = {}
        for x in base:
            y = mul(mul(alpha, x), alpha_inv)
            if y not in base_set:
                raise RuntimeError("automorphism does not normalize base group")
            alpha_map[x] = y
        counts = {
            "all_seeds": len(base),
            "alpha4_inverse": 0,
            "eight_distinct_images": 0,
            "surface_relator": 0,
            "b3_injective": 0,
            "base_generation": 0,
            "product_generation": 0,
            "based_tree_pass": 0,
        }
        first_failures = {}
        b3_rejections = []
        survivors = []
        for seed_index, seed in enumerate(base):
            images = [seed]
            for _ in range(7):
                images.append(alpha_map[images[-1]])
            if images[4] != inv(seed):
                continue
            counts["alpha4_inverse"] += 1
            if len(set(images)) != 8:
                first_failures.setdefault("distinct", {"seed_index": seed_index})
                continue
            counts["eight_distinct_images"] += 1
            rel = identity
            for j in RELATOR:
                rel = mul(rel, images[j])
            if rel != identity:
                first_failures.setdefault("relator", {"seed_index": seed_index, "relator_image": list(rel)})
                continue
            counts["surface_relator"] += 1
            seen = {}
            collision = None
            for element_id, word in b3_words:
                key = (eval_word(images, word, identity), len(word) & 1)
                if key in seen:
                    collision = {
                        "seed_index": seed_index,
                        "first_element_id": seen[key][0],
                        "first_word": list(seen[key][1]),
                        "second_element_id": element_id,
                        "second_word": list(word),
                        "image_base_one_line": list(key[0]),
                        "image_parity": key[1],
                    }
                    break
                seen[key] = (element_id, word)
            if collision is not None:
                first_failures.setdefault("b3_collision", collision)
                b3_rejections.append({"seed_index": seed_index, "seed_one_line": list(seed), "collision": collision})
                continue
            counts["b3_injective"] += 1
            generated = subgroup_size(images, len(base))
            if generated != len(base):
                first_failures.setdefault("generation", {"seed_index": seed_index, "generated_base_order": generated})
                continue
            counts["base_generation"] += 1
            # Each base group is perfect.  A subgroup of GxC2 projecting onto
            # G and containing odd lifts cannot be a graph G->C2, hence is full.
            counts["product_generation"] += 1
            witness = {
                "seed_index": seed_index,
                "seed_one_line": list(seed),
                "seed_cycles": cycles(seed),
                "images_one_line": [list(x) for x in images],
                "images_cycles": [cycles(x) for x in images],
            }
            if do_based:
                based = scan_based(images, base)
                witness["based_tree"] = based
                if based["pass"]:
                    counts["based_tree_pass"] += 1
            survivors.append(witness)
        result["classes"].append({
            "class_index": class_index,
            "class_size": class_size,
            "representative_one_line": list(alpha),
            "representative_cycles": cycles(alpha),
            "centralizer_order": len(aut) // class_size,
            "counts": counts,
            "first_failures": first_failures,
            "b3_rejections": b3_rejections,
            "survivors": survivors,
        })
    result["elapsed_seconds"] = time.perf_counter() - started
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--groups", nargs="+", choices=("A8", "PSU33", "M11"), default=("A8", "PSU33", "M11"))
    parser.add_argument("--based", action="store_true", help="scan immutable 23,129,593-node based tree for positive B3/generation survivors")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    b3_words, ball_sha256 = load_b3()
    builders = {"A8": a8_data, "PSU33": psu33_data, "M11": m11_data}
    report = {
        "schema_version": "1.0",
        "algorithm": "proof_complete_direct_orbit_seed_G_times_C2",
        "permutation_convention": "p*q is p after q; words multiply left-to-right from identity",
        "one_line_encoding": "zero-based list: entry i is the image of point i; cycle strings are one-based",
        "physical_images": "g_j -> (alpha^j(seed),1)",
        "frozen_relator_indices": list(RELATOR),
        "b3_records": len(b3_words),
        "b3_source": str(BALL.relative_to(ROOT)).replace("\\", "/"),
        "b3_source_sha256": ball_sha256,
        "based_requested": args.based,
        "groups": [],
    }
    for key in args.groups:
        print(f"building/scanning {key}", flush=True)
        report["groups"].append(scan_group(builders[key](), b3_words, args.based))
        print(json.dumps(report["groups"][-1], separators=(",", ":")), flush=True)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()



