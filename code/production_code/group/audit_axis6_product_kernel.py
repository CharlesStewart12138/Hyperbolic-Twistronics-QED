from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GROUP = Path(__file__).resolve().parent
DATA = ROOT / "data" / "production" / "global_direct_v2"
CERT_PATH = GROUP / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json"
CANDIDATES_PATH = DATA / "product_kernel_candidates.tsv"
CHECKPOINT_PATH = DATA / "product_kernel_scan_checkpoint.tsv"
SOURCE_PATH = GROUP / "scan_axis6_product_kernel.cpp"
OUT_JSON = GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_INDEPENDENT_AUDIT.json"
OUT_MD = GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_INDEPENDENT_AUDIT.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_tsv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            result[key] = value
    return result


def q2_mul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def q2_add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def q2_sign(x: tuple[int, int]) -> int:
    p, q = x
    if q == 0:
        return (p > 0) - (p < 0)
    if p == 0:
        return (q > 0) - (q < 0)
    if (p > 0) == (q > 0):
        return 1 if p > 0 else -1
    delta = p * p - 2 * q * q
    if delta == 0:
        raise AssertionError("unexpected rational sqrt(2) equality")
    return ((delta > 0) - (delta < 0)) if p > 0 else -((delta > 0) - (delta < 0))


def k_sign(a: tuple[int, int], b: tuple[int, int]) -> int:
    sa, sb = q2_sign(a), q2_sign(b)
    if sb == 0 or sa == 0 or sa == sb:
        return sa if sb == 0 else (sb if sa == 0 else sa)
    a2 = q2_mul(a, a)
    b2_beta2 = q2_mul(q2_mul(b, b), (2, 2))
    dominance = q2_sign((a2[0] - b2_beta2[0], a2[1] - b2_beta2[1]))
    if dominance == 0:
        raise AssertionError("unexpected beta-extension equality")
    return sa if dominance > 0 else sb


def trace_margin_sign(row: dict[str, str]) -> int:
    p, q, r, s = (int(row[f"re_c{i}"]) for i in range(4))
    exponent = int(row["exponent"])
    a = q2_add(q2_mul((p, q), (p, q)), q2_mul(q2_mul((r, s), (r, s)), (2, 2)))
    b0 = q2_mul((p, q), (r, s))
    b = (2 * b0[0], 2 * b0[1])
    threshold = q2_mul((2405, 1700), (2405, 1700))
    scale = 1 << (2 * exponent)
    a = (a[0] - scale * threshold[0], a[1] - scale * threshold[1])
    return k_sign(a, b)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(4))


def decode_word(high: int, low: int, depth: int) -> list[int]:
    packed = (high << 64) | low
    return [(packed >> (3 * (depth - 1 - index))) & 7 for index in range(depth)]


def main() -> None:
    cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    physical = cert["generator_images"]["physical_geometric"]
    generators = [
        [index for factor in physical[f"g{i}"] for index in factor["S4_phi_inverse_orbit_indices"]]
        for i in range(8)
    ]
    assert all(factor["parity"] == 1 for values in physical.values() for factor in values)
    source = SOURCE_PATH.read_text(encoding="utf-8")
    block = source.split("kGeneratorImages{{", 1)[1].split("}};", 1)[0]
    hardcoded = [int(value) for value in re.findall(r"\d+", block)]
    assert hardcoded == [value for row in generators for value in row]

    elements = list(itertools.permutations(range(4)))
    index = {value: position for position, value in enumerate(elements)}
    table = [[index[compose(left, right)] for right in elements] for left in elements]
    assert elements[0] == (0, 1, 2, 3)

    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checkpoint = parse_tsv(CHECKPOINT_PATH)
    assert checkpoint["complete"] == "1"
    assert int(checkpoint["scanned_records"]) == int(checkpoint["total_records"]) == 785_639_753
    assert len(rows) == int(checkpoint["kernel_elements"]) == 736
    assert len({int(row["record_index"]) for row in rows}) == len(rows)

    positive_margins = 0
    minimum_length = math.inf
    minimum_rows: list[int] = []
    for row in rows:
        depth = int(row["depth"])
        assert depth > 0 and depth % 2 == 0
        word = decode_word(int(row["word_high_hex"], 16), int(row["word_low_hex"], 16), depth)
        for component in range(16):
            image = 0
            for generator in word:
                image = table[image][generators[generator][component]]
            assert image == 0
        sign = trace_margin_sign(row)
        assert sign > 0
        assert row["dangerous_le_6a_B"] == "0"
        positive_margins += 1
        length = float(row["translation_length_over_a_B"])
        if length < minimum_length - 1e-14:
            minimum_length = length
            minimum_rows = [int(row["record_index"])]
        elif abs(length - minimum_length) <= 1e-14:
            minimum_rows.append(int(row["record_index"]))

    assert positive_margins == 736
    assert int(checkpoint["dangerous_elements"]) == 0
    assert minimum_length > 6.0
    result = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT-V2",
        "quotient_id": cert["quotient_id"],
        "quotient_actual_order": cert["construction"]["actual_generated_image_order"],
        "audited_registry_records": int(checkpoint["total_records"]),
        "kernel_candidate_rows": len(rows),
        "all_candidate_words_recompute_to_identity": True,
        "all_candidate_trace_margins_strictly_positive_by_integer_radical_sign": True,
        "dangerous_translation_length_le_6a_B": 0,
        "minimum_observed_kernel_translation_length_over_a_B": format(minimum_length, ".16g"),
        "minimum_observed_margin_over_6a_B": format(minimum_length - 6.0, ".16g"),
        "minimum_record_indices": minimum_rows,
        "generator_image_source_matches_scanner": True,
        "input_sha256": {
            "quotient_certificate": sha256(CERT_PATH),
            "scan_checkpoint": sha256(CHECKPOINT_PATH),
            "kernel_candidates": sha256(CANDIDATES_PATH),
            "scanner_source": sha256(SOURCE_PATH),
        },
        "classification": "GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED",
        "audited_utc": utc_now(),
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_MD.write_text(
        "# Independent audit: global systole cutoff\n\n"
        f"All {len(rows)} nonidentity product-kernel candidates emitted by the complete "
        f"{checkpoint['total_records']}-record exact-ball scan were independently re-evaluated from the "
        "frozen certificate's S4 permutations. Every image is the identity in all 16 S4 components and "
        "has even shared parity.\n\n"
        "For every candidate, a second pure-integer nested-radical sign implementation proves "
        "`|tr(g)|/2 > cosh(3a_B/R)`, hence `ell(g)>6a_B`. The dangerous count is exactly zero. "
        f"The smallest observed kernel length is `{minimum_length:.15f} a_B`, leaving margin "
        f"`{minimum_length - 6.0:.15f} a_B`.\n\n"
        "Together with the exact axis-to-basepoint theorem and the empty-frontier GEO-FLOOD-2 "
        "certificate, this proves that every nonidentity element of the frozen product kernel has "
        "translation length strictly greater than `6a_B`.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
