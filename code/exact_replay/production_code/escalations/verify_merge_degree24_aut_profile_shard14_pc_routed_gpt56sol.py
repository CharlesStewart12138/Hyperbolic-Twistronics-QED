from __future__ import annotations

import re
import sys
from pathlib import Path


BASE = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
LO, HI = 12333, 12595
OUTPUT = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12333_12595_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt"
STDOUT = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_RUN_STDOUT_GPT56SOL.txt"
STDERR = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_RUN_STDERR_GPT56SOL.txt"
WRAPPER = "gap_run_degree24_aut_profile_shard14_12333_12595_pc_domain_gpt56sol.g"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def read_lines(name: str) -> list[str]:
    return (BASE / name).read_text(encoding="utf-8").splitlines()


def fields(line: str, start: int = 2) -> dict[str, str]:
    parts = line.split("\t")
    require((len(parts) - start) % 2 == 0, f"malformed paired record: {line}")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field {parts[index]}: {line}")
        result[parts[index]] = parts[index + 1]
    return result


def load_map(name: str, has_solvable: bool) -> dict[int, dict[str, int]]:
    result: dict[int, dict[str, int]] = {}
    for line in read_lines(name):
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key = int(match.group(1))
        data = fields(line)
        require(key not in result, f"duplicate sealed key 24T{key}")
        result[key] = {
            "order": int(data["ORDER"]),
            "parity": int(data["PARITY_MAPS"]),
            "solvable": int(data["SOLVABLE"]) if has_solvable else -1,
        }
    return result


solvability = load_map("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt", True)
window = load_map("GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt", False)
parity_keys = sorted(k for k in solvability if LO <= k <= HI)
window_keys = sorted(k for k in window if LO <= k <= HI)
require(len(window_keys) == 263, "sealed window count")
require(len(parity_keys) == 256, "sealed parity count")
require(all(solvability[k]["solvable"] == 1 for k in parity_keys), "all parity keys solvable")
excluded = [k for k in window_keys if k not in set(parity_keys)]
require(excluded == [12333, 12453, 12454, 12455, 12456, 12459, 12575], "sealed parity exclusions")

lines = read_lines(OUTPUT)
header = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT",
    "GAP_VERSION\t4.12.1",
    "DATABASE\t25000",
    "RANGE\t12333\t12595",
    "GUARD_MS\t1320000",
    "EXPECTED_ORDER_WINDOW\t263",
    "EXPECTED_PARITY\t256",
    "SCOPE\tExact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.",
    "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.",
]
require(lines[: len(header)] == header, "complete exact header")
require(sum(line.startswith("TOTAL\t") for line in lines) == 1, "unique TOTAL")
require(lines.count("DONE") == 1 and lines[-1] == "DONE", "unique terminal DONE")
require(not any(line.startswith(("TOTAL_PARTIAL\t", "STOPPED_GUARD")) for line in lines), "no guard marker")

entries: list[dict[str, int | str]] = []
entry_indices: list[int] = []
for index, line in enumerate(lines):
    match = re.match(r"^ENTRY\t24T(\d+)\t", line)
    if not match:
        continue
    key = int(match.group(1))
    data = fields(line)
    required = {
        "ORDER", "SOLVABLE_G", "PARITY_MAPS_G", "PC_ORDER", "PARITY_MAPS_P",
        "AUT_ORDER", "ISO_MS", "AUT_MS", "METHOD", "CLASS_MS",
        "ORDER8_CLASSES", "RAW_PAIRS",
    }
    require(required <= data.keys(), f"24T{key} entry schema")
    entry: dict[str, int | str] = {
        "key": key,
        "order": int(data["ORDER"]),
        "solvable": data["SOLVABLE_G"],
        "parity": int(data["PARITY_MAPS_G"]),
        "pc_order": int(data["PC_ORDER"]),
        "parity_p": int(data["PARITY_MAPS_P"]),
        "aut_order": int(data["AUT_ORDER"]),
        "iso": int(data["ISO_MS"]),
        "aut": int(data["AUT_MS"]),
        "method": data["METHOD"],
        "class_ms": int(data["CLASS_MS"]),
        "classes": int(data["ORDER8_CLASSES"]),
        "raw": int(data["RAW_PAIRS"]),
    }
    entries.append(entry)
    entry_indices.append(index)

require([int(e["key"]) for e in entries] == parity_keys, "exact ordered entry keyset")
classes = raw = iso_ms = aut_ms = class_ms = 0
for position, (entry, line_index) in enumerate(zip(entries, entry_indices), start=1):
    key = int(entry["key"])
    sealed = solvability[key]
    require(entry["order"] == sealed["order"], f"24T{key} order")
    require(entry["solvable"] == "true", f"24T{key} pc-solvable route")
    require(entry["parity"] == sealed["parity"], f"24T{key} parity")
    require(entry["pc_order"] == entry["order"], f"24T{key} pc order transport")
    require(entry["parity_p"] == entry["parity"], f"24T{key} parity transport")
    require(entry["raw"] == int(entry["order"]) * int(entry["classes"]), f"24T{key} raw identity")
    require(int(entry["aut_order"]) > 0, f"24T{key} Aut order")
    require(entry["method"] in {"pc", "native"}, f"24T{key} class method")
    require(min(int(entry[n]) for n in ("iso", "aut", "class_ms", "classes", "raw")) >= 0, f"24T{key} nonnegative")
    classes += int(entry["classes"])
    raw += int(entry["raw"])
    iso_ms += int(entry["iso"])
    aut_ms += int(entry["aut"])
    class_ms += int(entry["class_ms"])
    require(line_index + 1 < len(lines) and lines[line_index + 1].startswith("CHECKPOINT\t"), f"24T{key} adjacent checkpoint")
    checkpoint = fields(lines[line_index + 1], 1)
    require(int(checkpoint["LAST_COMPLETE_K"]) == key, f"24T{key} checkpoint key")
    require(int(checkpoint["PROCESSED"]) == position, f"24T{key} checkpoint count")
    require(int(checkpoint["ISO_MS"]) == iso_ms, f"24T{key} checkpoint ISO")
    require(int(checkpoint["ORDER8_CLASSES"]) == classes, f"24T{key} checkpoint classes")
    require(int(checkpoint["RAW_PAIRS"]) == raw, f"24T{key} checkpoint raw")

scan_lines = [line for line in lines if line.startswith("SCAN_CHECKPOINT\t")]
scan_keys = list(range(12350, 12576, 25))
require(len(scan_lines) == len(scan_keys) == 10, "scan checkpoint count")
for line, key in zip(scan_lines, scan_keys):
    scan = fields(line, 1)
    prefix = [e for e in entries if int(e["key"]) <= key]
    require(int(scan["LAST_COMPLETE_K"]) == key, f"scan {key} key")
    require(int(scan["ORDER_WINDOW"]) == sum(LO <= k <= key for k in window_keys), f"scan {key} window")
    require(int(scan["PROCESSED"]) == len(prefix), f"scan {key} processed")
    require(int(scan["ISO_MS"]) == sum(int(e["iso"]) for e in prefix), f"scan {key} ISO")
    require(int(scan["ORDER8_CLASSES"]) == sum(int(e["classes"]) for e in prefix), f"scan {key} classes")
    require(int(scan["RAW_PAIRS"]) == sum(int(e["raw"]) for e in prefix), f"scan {key} raw")

total_line = next(line for line in lines if line.startswith("TOTAL\t"))
total_pattern = re.compile(
    r"^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t12333\t12595\tLAST_COMPLETE_K\t12595"
    r"\tORDER_WINDOW\t263\tPROCESSED\t256\tORDER8_CLASSES\t(\d+)\tRAW_PAIRS\t(\d+)"
    r"\tISO_MS\t(\d+)\tAUT_MS\t(\d+)\tCLASS_MS\t(\d+)\tMS\t(\d+)$"
)
match = total_pattern.match(total_line)
require(match is not None, "exact TOTAL schema")
total_classes, total_raw, total_iso, total_aut, total_class, gap_ms = map(int, match.groups())
require((total_classes, total_raw, total_iso, total_aut, total_class) == (classes, raw, iso_ms, aut_ms, class_ms), "TOTAL sums")
require((classes, raw, iso_ms, aut_ms, class_ms, gap_ms) == (6265, 123526656, 222, 73564, 77093, 158727), "sealed outcome totals")

stdout_text = (BASE / STDOUT).read_text(encoding="utf-8").strip()
stderr_text = (BASE / STDERR).read_text(encoding="utf-8")
require(stdout_text == f"WROTE /mnt/d/work/revise/production_code/escalations/{OUTPUT}", "exact WROTE stdout")
require(WRAPPER in stderr_text, "wrapper bound in telemetry")
wall_match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)", stderr_text)
rss_match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", stderr_text)
require(wall_match is not None and rss_match is not None, "resource telemetry")
wall, max_rss = wall_match.group(1).strip(), int(rss_match.group(1))
require(wall == "2:39.89" and max_rss == 182400, "exact wall/RSS")
require("Exit status: 0" in stderr_text and max_rss < 50331648, "exit and RSS guard")

merged_lines = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD14-MERGED-ROUTED",
    "GAP_VERSION\t4.12.1",
    "DATABASE\t25000",
    "RANGE\t12333\t12595",
    "ORDER_WINDOW\t263",
    "PARITY_KEYS\t256",
    "ROUTING\t12333..12595:pc;native-empty",
    "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates.",
]
for entry in entries:
    merged_lines.append(
        "\t".join(
            [
                "ENTRY", f"24T{entry['key']}", "ORDER", str(entry["order"]), "SOLVABLE_G", str(entry["solvable"]),
                "PARITY_MAPS", str(entry["parity"]), "REPRESENTATION", "pc_transport", "PC_ORDER", str(entry["pc_order"]),
                "AUT_ORDER", str(entry["aut_order"]), "ISO_MS", str(entry["iso"]), "AUT_MS", str(entry["aut"]),
                "METHOD", str(entry["method"]), "CLASS_MS", str(entry["class_ms"]), "ORDER8_CLASSES", str(entry["classes"]),
                "RAW_PAIRS", str(entry["raw"]),
            ]
        )
    )
merged_lines.extend(
    [
        f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t12333\t12595\tORDER_WINDOW\t263\tPROCESSED\t256\tPC_TRANSPORT\t256\tNATIVE_NONSOLVABLE\t0\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}",
        "DONE",
    ]
)
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12333_12595_MERGED_ROUTED_GPT56SOL.txt").write_text("\n".join(merged_lines) + "\n", encoding="utf-8", newline="\n")

verify_lines = [
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD14",
    "RANGE\t12333\t12595", "ORDER_WINDOW\t263", "PARITY_KEYS\t256", "ENTRY_KEYS_EXACT\tPASS",
    "SOLVABLE_PC_ROUTE\t256\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t0\tPASS", "PC_ORDER_PARITY_TRANSPORT\t256\tPASS",
    "RAW_IDENTITIES\t256\tPASS", "ENTRY_CHECKPOINT_PAIRS\t256\tPASS", "SCAN_CHECKPOINTS\t10\tPASS",
    "UNIQUE_TOTAL_DONE_NO_GUARD\tPASS", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}",
    f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}",
    f"MAX_RSS_KB\t{max_rss}", "SEALED_KEYSETS_AND_STREAMS\tPASS", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN",
    "VERIFY\tPASS", "DONE",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_VERIFY_GPT56SOL.txt").write_text("\n".join(verify_lines) + "\n", encoding="utf-8", newline="\n")

ratio = (aut_ms + class_ms) / 366714
raw_ratio = raw / 197240832
aggregate_lines = [
    "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD14",
    "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED", "DEGREE\t24", "DATABASE\t25000", "RANGE\t12333\t12595",
    "LAST_COMPLETE_K\t12595", "ORDER_WINDOW\t263", "PARITY_KEYS\t256", "PARITY_EXCLUDED\t7",
    "SEGMENTS\t12333..12595-pc;native-empty", "PC_TRANSPORT_KEYS\t256", "NATIVE_NONSOLVABLE_KEYS\t0",
    f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}",
    f"CLASS_MS\t{class_ms}", f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}",
    "POINT_FORECAST_MS\t366714", f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}", "POINT_FORECAST_CLASSES\t10096",
    "POINT_FORECAST_RAW_PAIRS\t197240832", f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}",
    "ENTRY_CHECKPOINT_PAIRS\t256", "SCAN_CHECKPOINTS\t10", "RAW_IDENTITIES_PASS\t256", "PC_TRANSPORT_IDENTITIES_PASS\t256",
    "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "INTERNAL_GUARD_MS\t1320000", "EXTERNAL_WALL_GUARD_SECONDS\t1400",
    f"WALL\t{wall}", f"MAX_RSS_KB\t{max_rss}", "EXTERNAL_GUARD_EVENTS\t0", "FAILED_VERIFIER_ATTEMPTS\t1",
    "FAILED_READONLY_AUDIT_ATTEMPTS\t1", "GUARD_TRIGGERED_FINAL_SEGMENT\t0", "VERIFY\tPASS",
    "SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 12333..12595 only. This is not full degree-24 closure and contains no seed test.",
    "DONE",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_AGGREGATE_GPT56SOL.txt").write_text("\n".join(aggregate_lines) + "\n", encoding="utf-8", newline="\n")

certificate_lines = [
    "# Degree-24 exact Aut/order-8 profile - shard 14", "",
    "Status: **complete and independently verified for catalogue range `12333..12595` only**. This is not full degree-24 closure.", "",
    "The sealed evidence contains 263 order-window keys and 256 parity-capable keys. All 256 parity keys are solvable, so the exact maximal routing is one pc-domain segment over the whole catalogue range and an empty native segment. The seven parity-excluded keys are `12333`, `12453..12456`, `12459`, and `12575`; the scanner visits them but constructs no automorphism group for them.", "",
    "For each included key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation. It preserves automorphism order and conjugacy. GAP checks group order and the exact number of epimorphisms to C2 on both sides, so every class count and raw contribution is transported exactly.", "",
    f"Exact totals: 6,265 exact-order-8 classes; 123,526,656 raw pairs; ISO/AUT/class times {iso_ms}/{aut_ms}/{class_ms} ms; GAP time {gap_ms} ms; wall {wall}; peak RSS {max_rss} KiB. All 256 entry/checkpoint pairs, 10 scan checkpoints, key sets, raw identities, transport identities, complete header, unique TOTAL, terminal DONE, stdout, stderr, guard status, and resource records pass.", "",
    "A PowerShell audit typo and a separate compact PowerShell verifier draft both failed parsing before file reads or scientific output. Their records and sources are preserved as FAILED_V1 evidence and excluded. The canonical Python verifier reruns all checks from the sealed inputs.", "",
    "No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard 14 is sealed; shard 15 remains unrun.",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_GPT56SOL_CERTIFICATE.md").write_text("\n".join(certificate_lines) + "\n", encoding="utf-8", newline="\n")

print(
    "PASS shard14 range=12333-12595 window=263 parity=256 pc=256 native=0 "
    f"classes={classes} raw={raw} isoMs={iso_ms} autMs={aut_ms} classMs={class_ms} "
    f"gapMs={gap_ms} wall={wall} maxRssKb={max_rss}"
)
