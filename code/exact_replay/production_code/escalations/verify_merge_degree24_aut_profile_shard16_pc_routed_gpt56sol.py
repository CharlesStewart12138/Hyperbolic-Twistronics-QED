from __future__ import annotations

import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
lo, hi = 12888, 13097
output_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12888_13097_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt"
stdout_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD16_RUN_STDOUT_GPT56SOL.txt"
stderr_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD16_RUN_STDERR_GPT56SOL.txt"
wrapper = "gap_run_degree24_aut_profile_shard16_12888_13097_pc_domain_gpt56sol.g"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def read(name: str) -> list[str]:
    return (base / name).read_text(encoding="utf-8").splitlines()


def pairs(line: str, start: int = 2) -> dict[str, str]:
    parts = line.split("\t")
    require((len(parts) - start) % 2 == 0, f"malformed pairs: {line}")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field {parts[index]}")
        result[parts[index]] = parts[index + 1]
    return result


def load_map(name: str, has_solvable: bool) -> dict[int, dict[str, int]]:
    result: dict[int, dict[str, int]] = {}
    for line in read(name):
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key = int(match.group(1))
        data = pairs(line)
        result[key] = {
            "order": int(data["ORDER"]), "parity": int(data["PARITY_MAPS"]),
            "solvable": int(data["SOLVABLE"]) if has_solvable else -1,
        }
    return result


sol = load_map("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt", True)
win = load_map("GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt", False)
parity_keys = sorted(k for k in sol if lo <= k <= hi)
window_keys = sorted(k for k in win if lo <= k <= hi)
require(len(window_keys) == 210 and len(parity_keys) == 206, "sealed window/parity")
require(all(sol[k]["solvable"] == 1 for k in parity_keys), "all parity keys solvable")
require([k for k in window_keys if k not in set(parity_keys)] == [12983, 12984, 12985, 13009], "parity exclusions")

lines = read(output_name)
header = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT",
    "GAP_VERSION\t4.12.1", "DATABASE\t25000", "RANGE\t12888\t13097", "GUARD_MS\t1320000",
    "EXPECTED_ORDER_WINDOW\t210", "EXPECTED_PARITY\t206",
    "SCOPE\tExact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.",
    "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.",
]
require(lines[:9] == header, "exact header")
require(sum(line.startswith("TOTAL\t") for line in lines) == 1, "unique TOTAL")
require(lines.count("DONE") == 1 and lines[-1] == "DONE", "terminal DONE")
require(not any(line.startswith(("TOTAL_PARTIAL\t", "STOPPED_GUARD")) for line in lines), "no guard")

entries: list[dict[str, int | str]] = []
indices: list[int] = []
for index, line in enumerate(lines):
    match = re.match(r"^ENTRY\t24T(\d+)\t", line)
    if not match:
        continue
    key = int(match.group(1))
    data = pairs(line)
    required = {"ORDER", "SOLVABLE_G", "PARITY_MAPS_G", "PC_ORDER", "PARITY_MAPS_P", "AUT_ORDER", "ISO_MS", "AUT_MS", "METHOD", "CLASS_MS", "ORDER8_CLASSES", "RAW_PAIRS"}
    require(required <= data.keys(), f"24T{key} schema")
    entries.append({
        "key": key, "order": int(data["ORDER"]), "solvable": data["SOLVABLE_G"], "parity": int(data["PARITY_MAPS_G"]),
        "pc_order": int(data["PC_ORDER"]), "parity_p": int(data["PARITY_MAPS_P"]), "aut_order": int(data["AUT_ORDER"]),
        "iso": int(data["ISO_MS"]), "aut": int(data["AUT_MS"]), "method": data["METHOD"], "class_ms": int(data["CLASS_MS"]),
        "classes": int(data["ORDER8_CLASSES"]), "raw": int(data["RAW_PAIRS"]),
    })
    indices.append(index)
require([int(entry["key"]) for entry in entries] == parity_keys, "exact ordered entry keyset")

classes = raw = iso_ms = aut_ms = class_ms = 0
for position, (entry, index) in enumerate(zip(entries, indices), start=1):
    key = int(entry["key"])
    sealed = sol[key]
    require(entry["order"] == sealed["order"] and entry["parity"] == sealed["parity"], f"24T{key} sealed fields")
    require(entry["solvable"] == "true", f"24T{key} pc route")
    require(entry["pc_order"] == entry["order"] and entry["parity_p"] == entry["parity"], f"24T{key} transport")
    require(entry["raw"] == int(entry["order"]) * int(entry["classes"]), f"24T{key} raw")
    require(int(entry["aut_order"]) > 0 and entry["method"] in {"pc", "native"}, f"24T{key} Aut fields")
    require(min(int(entry[name]) for name in ("iso", "aut", "class_ms", "classes", "raw")) >= 0, f"24T{key} nonnegative")
    classes += int(entry["classes"]); raw += int(entry["raw"]); iso_ms += int(entry["iso"]); aut_ms += int(entry["aut"]); class_ms += int(entry["class_ms"])
    require(lines[index + 1].startswith("CHECKPOINT\t"), f"24T{key} adjacent checkpoint")
    checkpoint = pairs(lines[index + 1], 1)
    require(int(checkpoint["LAST_COMPLETE_K"]) == key and int(checkpoint["PROCESSED"]) == position, f"24T{key} checkpoint key/count")
    require(int(checkpoint["ISO_MS"]) == iso_ms and int(checkpoint["ORDER8_CLASSES"]) == classes and int(checkpoint["RAW_PAIRS"]) == raw, f"24T{key} checkpoint sums")

scan_keys = [12900, 12925, 12950, 12975, 13000, 13025, 13050, 13075]
scan_lines = [line for line in lines if line.startswith("SCAN_CHECKPOINT\t")]
require(len(scan_lines) == len(scan_keys) == 8, "scan count")
for line, key in zip(scan_lines, scan_keys):
    scan = pairs(line, 1)
    prefix = [entry for entry in entries if int(entry["key"]) <= key]
    require(int(scan["LAST_COMPLETE_K"]) == key, f"scan {key} key")
    require(int(scan["ORDER_WINDOW"]) == sum(lo <= item <= key for item in window_keys), f"scan {key} window")
    require(int(scan["PROCESSED"]) == len(prefix), f"scan {key} processed")
    require(int(scan["ISO_MS"]) == sum(int(entry["iso"]) for entry in prefix), f"scan {key} ISO")
    require(int(scan["ORDER8_CLASSES"]) == sum(int(entry["classes"]) for entry in prefix), f"scan {key} classes")
    require(int(scan["RAW_PAIRS"]) == sum(int(entry["raw"]) for entry in prefix), f"scan {key} raw")

total_line = next(line for line in lines if line.startswith("TOTAL\t"))
match = re.fullmatch(
    r"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t12888\t13097\tLAST_COMPLETE_K\t13097\tORDER_WINDOW\t210\tPROCESSED\t206"
    r"\tORDER8_CLASSES\t(\d+)\tRAW_PAIRS\t(\d+)\tISO_MS\t(\d+)\tAUT_MS\t(\d+)\tCLASS_MS\t(\d+)\tMS\t(\d+)", total_line,
)
require(match is not None, "TOTAL schema")
outcome = tuple(map(int, match.groups()))
require(outcome == (classes, raw, iso_ms, aut_ms, class_ms, outcome[5]), "TOTAL sums")
classes, raw, iso_ms, aut_ms, class_ms, gap_ms = outcome
require(outcome == (43401, 1066622976, 255, 105223, 184790, 298126), "exact outcome")

stdout = (base / stdout_name).read_text(encoding="utf-8").strip()
stderr = (base / stderr_name).read_text(encoding="utf-8")
require(stdout == f"WROTE /mnt/d/work/revise/production_code/escalations/{output_name}", "WROTE stdout")
require(wrapper in stderr and "Exit status: 0" in stderr, "wrapper/exit telemetry")
wall_match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)", stderr)
rss_match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", stderr)
require(wall_match is not None and rss_match is not None, "resource telemetry")
wall, rss = wall_match.group(1).strip(), int(rss_match.group(1))
require(wall == "4:59.37" and rss == 257472 and rss < 50331648, "exact resources")

merged = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD16-MERGED-ROUTED", "GAP_VERSION\t4.12.1",
    "DATABASE\t25000", "RANGE\t12888\t13097", "ORDER_WINDOW\t210", "PARITY_KEYS\t206",
    "ROUTING\t12888..13097:pc;native-empty", "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates.",
]
for entry in entries:
    merged.append("\t".join([
        "ENTRY", f"24T{entry['key']}", "ORDER", str(entry["order"]), "SOLVABLE_G", str(entry["solvable"]), "PARITY_MAPS", str(entry["parity"]),
        "REPRESENTATION", "pc_transport", "PC_ORDER", str(entry["pc_order"]), "AUT_ORDER", str(entry["aut_order"]), "ISO_MS", str(entry["iso"]),
        "AUT_MS", str(entry["aut"]), "METHOD", str(entry["method"]), "CLASS_MS", str(entry["class_ms"]), "ORDER8_CLASSES", str(entry["classes"]), "RAW_PAIRS", str(entry["raw"]),
    ]))
merged.extend([f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t12888\t13097\tORDER_WINDOW\t210\tPROCESSED\t206\tPC_TRANSPORT\t206\tNATIVE_NONSOLVABLE\t0\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}", "DONE"])
(base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12888_13097_MERGED_ROUTED_GPT56SOL.txt").write_text("\n".join(merged) + "\n", encoding="utf-8", newline="\n")

verify = [
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD16", "RANGE\t12888\t13097", "ORDER_WINDOW\t210", "PARITY_KEYS\t206",
    "ENTRY_KEYS_EXACT\tPASS", "SOLVABLE_PC_ROUTE\t206\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t0\tPASS", "PC_ORDER_PARITY_TRANSPORT\t206\tPASS",
    "RAW_IDENTITIES\t206\tPASS", "ENTRY_CHECKPOINT_PAIRS\t206\tPASS", "SCAN_CHECKPOINTS\t8\tPASS", "UNIQUE_TOTAL_DONE_NO_GUARD\tPASS",
    f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}",
    f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}", f"MAX_RSS_KB\t{rss}", "SEALED_KEYSETS_AND_STREAMS\tPASS",
    "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE",
]
(base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD16_VERIFY_GPT56SOL.txt").write_text("\n".join(verify) + "\n", encoding="utf-8", newline="\n")

ratio = (aut_ms + class_ms) / 367710
raw_ratio = raw / 324009984
aggregate = [
    "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD16", "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED",
    "DEGREE\t24", "DATABASE\t25000", "RANGE\t12888\t13097", "LAST_COMPLETE_K\t13097", "ORDER_WINDOW\t210", "PARITY_KEYS\t206",
    "PARITY_EXCLUDED\t4", "SEGMENTS\t12888..13097-pc;native-empty", "PC_TRANSPORT_KEYS\t206", "NATIVE_NONSOLVABLE_KEYS\t0",
    f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}",
    f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", "POINT_FORECAST_MS\t367710", f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}",
    "POINT_FORECAST_CLASSES\t13184", "POINT_FORECAST_RAW_PAIRS\t324009984", f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}",
    "ENTRY_CHECKPOINT_PAIRS\t206", "SCAN_CHECKPOINTS\t8", "RAW_IDENTITIES_PASS\t206", "PC_TRANSPORT_IDENTITIES_PASS\t206",
    "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "INTERNAL_GUARD_MS\t1320000", "EXTERNAL_WALL_GUARD_SECONDS\t1400",
    f"WALL\t{wall}", f"MAX_RSS_KB\t{rss}", "EXTERNAL_GUARD_EVENTS\t0", "GUARD_TRIGGERED_FINAL_SEGMENT\t0", "VERIFY\tPASS",
    "SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 12888..13097 only. This is not full degree-24 closure and contains no seed test.", "DONE",
]
(base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD16_AGGREGATE_GPT56SOL.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")

certificate = [
    "# Degree-24 exact Aut/order-8 profile - shard 16", "",
    "Status: **complete and independently verified for catalogue range `12888..13097` only**. This is not full degree-24 closure.", "",
    "Sealed evidence gives 210 order-window and 206 parity-capable keys, all solvable. Therefore the exact collapsed routing is one pc-domain segment over the full range and an empty native segment. The four parity-excluded keys are `12983..12985` and `13009`; they receive no automorphism calculation.", "",
    "For each included key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation, preserving automorphism order and conjugacy. GAP checks group order and exact C2-epimorphism counts on both sides.", "",
    f"Exact totals: {classes:,} exact-order-8 classes; {raw:,} raw pairs; ISO/AUT/class times {iso_ms:,}/{aut_ms:,}/{class_ms:,} ms; GAP time {gap_ms:,} ms; wall {wall}; peak RSS {rss:,} KiB. All 206 entry/checkpoint pairs, eight scan checkpoints, key sets, raw identities, transports, header, terminal markers, streams, guards, and resources pass.", "",
    "No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard 16 is sealed; shard 17 remains unrun.",
]
(base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD16_GPT56SOL_CERTIFICATE.md").write_text("\n".join(certificate) + "\n", encoding="utf-8", newline="\n")
print(f"PASS shard16 range=12888-13097 window=210 parity=206 pc=206 native=0 classes={classes} raw={raw} isoMs={iso_ms} autMs={aut_ms} classMs={class_ms} gapMs={gap_ms} wall={wall} maxRssKb={rss}")
