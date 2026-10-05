"""Exhaust all inner-C8, odd-seed maps into PSU(3,3):2 (order 12,096)."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from production_code.group.psu3_3_c8_family import (
    IDENTITY as BASE_ID,
    elements as base_elements,
    frobenius,
    matinv,
    matmul,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).with_suffix(".json")
RELATOR = (0, 5, 2, 7, 4, 1, 6, 3)
IDENTITY = (BASE_ID, 0)


def field(matrix):
    return tuple(frobenius(entry) for entry in matrix)


def multiply(left, right):
    a, e = left
    b, f = right
    return (matmul(a, field(b) if e else b), e ^ f)


def inverse(value):
    a, e = value
    return (field(matinv(a)) if e else matinv(a), e)


def power(value, exponent):
    result = IDENTITY
    while exponent:
        if exponent & 1:
            result = multiply(result, value)
        value = multiply(value, value)
        exponent >>= 1
    return result


def conjugate(by, value):
    return multiply(by, multiply(value, inverse(by)))


def order(value):
    result = IDENTITY
    for exponent in range(1, 65):
        result = multiply(result, value)
        if result == IDENTITY:
            return exponent
    raise AssertionError("element order exceeds bound")


def b3_size(images):
    values = {IDENTITY}
    for a in range(8):
        values.add(images[a])
        for b in range(8):
            if b == (a + 4) % 8:
                continue
            ab = multiply(images[a], images[b])
            values.add(ab)
            for c in range(8):
                if c != (b + 4) % 8:
                    values.add(multiply(ab, images[c]))
    return len(values)


def generated_order(images):
    seen = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        current = frontier.pop()
        for generator in images:
            value = multiply(current, generator)
            if value not in seen:
                seen.add(value)
                frontier.append(value)
    return len(seen)


def main():
    group = base_elements()
    assert len(group) == 6048
    assert all(field(field(a)) == a and matmul(a, matinv(a)) == BASE_ID for a in group)
    extension = tuple((a, e) for a in group for e in (0, 1))
    order8 = {x for x in extension if order(x) == 8}
    remaining = set(order8)
    classes = []
    while remaining:
        representative = min(remaining)
        orbit = {conjugate(g, representative) for g in extension}
        centralizer = sum(
            multiply(g, representative) == multiply(representative, g)
            for g in extension
        )
        assert len(orbit) * centralizer == len(extension)
        classes.append((representative, len(orbit), centralizer))
        remaining -= orbit
    assert sum(size for _, size, _ in classes) == len(order8)

    records = []
    for class_index, (alpha, class_size, centralizer) in enumerate(classes):
        counters = Counter(seeds=len(group))
        histogram = Counter()
        for base in group:
            images = [(base, 1)]
            for _ in range(7):
                images.append(conjugate(alpha, images[-1]))
            if not all(images[i + 4] == inverse(images[i]) for i in range(4)):
                continue
            counters["inverse"] += 1
            relator = IDENTITY
            for digit in RELATOR:
                relator = multiply(relator, images[digit])
            if relator != IDENTITY:
                continue
            counters["relator"] += 1
            if len(set(images)) != 8:
                continue
            counters["distinct"] += 1
            image_size = b3_size(images)
            histogram[image_size] += 1
            b3_pass = image_size == 457
            generation_pass = generated_order(images) == len(extension)
            counters["B3"] += b3_pass
            counters["generation"] += generation_pass
            counters["all"] += b3_pass and generation_pass
        records.append({
            "class_index": class_index,
            "representative": {"matrix_F9_row_major": list(alpha[0]), "extension_bit": alpha[1]},
            "class_size": class_size,
            "centralizer_size": centralizer,
            "counters": dict(counters),
            "B3_image_size_histogram": dict(sorted(histogram.items())),
        })
    result = {
        "scope": "exhaustive inner-C8 odd-coset maps into PSU(3,3):2",
        "encoding": "F9 entry a+3b, u^2=2; row-major matrices; semidirect field bit; all seeds have bit 1",
        "orders": {"PSU3_3": len(group), "target": len(extension)},
        "order8_elements": len(order8),
        "order8_classes": len(classes),
        "classes": records,
        "B3_contract": "all 457 freely reduced words of length <=3, inverse digit i+4, internal coset parity",
        "based_tree_scanned": False,
        "based_tree_reason": "no B3-injective candidate",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
