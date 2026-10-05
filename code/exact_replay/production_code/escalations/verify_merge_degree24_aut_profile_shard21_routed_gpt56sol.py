from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


BASE = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def require(value: bool, label: str) -> None:
    if not value:
        raise AssertionError(label)


def lines(name: str) -> list[str]:
    return (BASE / name).read_text(encoding="utf-8").splitlines()


def pairs(line: str, start: int = 2) -> dict[str, str]:
    parts = line.split("\t")
    require((len(parts) - start) % 2 == 0, f"malformed pairs: {line}")
    result = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field: {parts[index]}")
        result[parts[index]] = parts[index + 1]
    return result


def load_map(name: str, with_solvable: bool) -> dict[int, dict[str, int]]:
    result = {}
    for line in lines(name):
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key, data = int(match.group(1)), pairs(line)
        require(key not in result, f"duplicate sealed key {key}")
        result[key] = {
            "order": int(data["ORDER"]), "parity": int(data["PARITY_MAPS"]),
            "solvable": int(data["SOLVABLE"]) if with_solvable else -1,
        }
    return result


SOL = load_map("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt", True)
WIN = load_map("GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt", False)


@dataclass(frozen=True)
class Segment:
    label: str
    lo: int
    hi: int
    representation: str
    window: int
    parity: int
    scans: tuple[int, ...]
    wrapper: str
    output: str
    stdout: str
    stderr: str
    expected: tuple[int, int, int, int, int, int]
    wall: str
    rss: int


SEGMENTS = (
    Segment("S1", 13929, 13984, "pc_transport", 56, 56, (13950, 13975),
        "gap_run_degree24_aut_profile_shard21_s1_13929_13984_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_13929_13984_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S1_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S1_RUN_STDERR_GPT56SOL.txt",
        (23752, 584036352, 52, 18895, 68883, 89244), "1:30.39", 259776),
    Segment("S2", 13985, 14002, "native", 18, 18, (14000,),
        "gap_run_degree24_aut_profile_shard21_s2_13985_14002_native_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_13985_14002_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S2_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S2_RUN_STDERR_GPT56SOL.txt",
        (93, 2824320, 0, 7884, 34306, 42688), "0:43.80", 194112),
    Segment("S3", 14003, 14218, "pc_transport", 216, 213,
        (14025, 14050, 14075, 14100, 14125, 14150, 14175, 14200),
        "gap_run_degree24_aut_profile_shard21_s3_14003_14218_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14003_14218_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S3_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_S3_RUN_STDERR_GPT56SOL.txt",
        (4148, 149008320, 248, 111680, 64177, 184132), "3:05.61", 184512),
)


def keys(mapping: dict[int, object], lo: int, hi: int) -> list[int]:
    return sorted(k for k in mapping if lo <= k <= hi)


def parse_entry(line: str, representation: str) -> dict[str, int | str]:
    match = re.match(r"^ENTRY\t24T(\d+)\t", line)
    require(match is not None, f"malformed ENTRY: {line}")
    key, data = int(match.group(1)), pairs(line)
    common = {"ORDER", "SOLVABLE_G", "AUT_ORDER", "AUT_MS", "METHOD", "CLASS_MS", "ORDER8_CLASSES", "RAW_PAIRS"}
    require(common <= data.keys(), f"24T{key} common schema")
    if representation == "pc_transport":
        require({"PARITY_MAPS_G", "PC_ORDER", "PARITY_MAPS_P", "ISO_MS"} <= data.keys(), f"24T{key} pc schema")
        parity, pc_order, parity_p, iso = int(data["PARITY_MAPS_G"]), int(data["PC_ORDER"]), int(data["PARITY_MAPS_P"]), int(data["ISO_MS"])
    else:
        require("PARITY_MAPS" in data, f"24T{key} native schema")
        parity, pc_order, parity_p, iso = int(data["PARITY_MAPS"]), int(data["ORDER"]), int(data["PARITY_MAPS"]), 0
    return {
        "key": key, "order": int(data["ORDER"]), "solvable": data["SOLVABLE_G"], "parity": parity,
        "pc_order": pc_order, "parity_p": parity_p, "aut_order": int(data["AUT_ORDER"]), "iso": iso,
        "aut": int(data["AUT_MS"]), "method": data["METHOD"], "class_ms": int(data["CLASS_MS"]),
        "classes": int(data["ORDER8_CLASSES"]), "raw": int(data["RAW_PAIRS"]), "representation": representation,
    }


def check_segment(segment: Segment) -> tuple[list[dict[str, int | str]], tuple[int, int, int, int, int, int]]:
    data_lines = lines(segment.output)
    pc = segment.representation == "pc_transport"
    cert = "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT" if pc else "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT"
    scope = "Exact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds." if pc else "Exact Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for parity-capable order-window targets only; no seeds."
    header = [f"CERTIFICATE_PROFILE\t{cert}", "GAP_VERSION\t4.12.1", "DATABASE\t25000",
        f"RANGE\t{segment.lo}\t{segment.hi}", "GUARD_MS\t1320000", f"EXPECTED_ORDER_WINDOW\t{segment.window}",
        f"EXPECTED_PARITY\t{segment.parity}", f"SCOPE\t{scope}",
        "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key."]
    require(data_lines[:9] == header, f"{segment.label} header")
    require(sum(x.startswith("TOTAL\t") for x in data_lines) == 1, f"{segment.label} TOTAL")
    require(data_lines.count("DONE") == 1 and data_lines[-1] == "DONE", f"{segment.label} DONE")
    require(not any(x.startswith(("TOTAL_PARTIAL\t", "STOPPED_GUARD")) for x in data_lines), f"{segment.label} guard")
    indexed = [(i, parse_entry(x, segment.representation)) for i, x in enumerate(data_lines) if x.startswith("ENTRY\t")]
    entries = [entry for _, entry in indexed]
    expected_keys = keys(SOL, segment.lo, segment.hi)
    require([int(e["key"]) for e in entries] == expected_keys and len(entries) == segment.parity, f"{segment.label} keyset")
    running = [0, 0, 0, 0, 0]
    for position, (line_index, entry) in enumerate(indexed, start=1):
        key, sealed = int(entry["key"]), SOL[int(entry["key"])]
        require(entry["order"] == sealed["order"] and entry["parity"] == sealed["parity"], f"{segment.label} 24T{key} sealed")
        required_solvable = "true" if pc else "false"
        require(entry["solvable"] == required_solvable, f"{segment.label} 24T{key} route")
        if pc:
            require(entry["pc_order"] == entry["order"] and entry["parity_p"] == entry["parity"], f"{segment.label} 24T{key} transport")
        require(entry["raw"] == int(entry["order"]) * int(entry["classes"]), f"{segment.label} 24T{key} raw")
        require(int(entry["aut_order"]) > 0 and entry["method"] in {"pc", "native"}, f"{segment.label} 24T{key} Aut")
        values = [int(entry[name]) for name in ("classes", "raw", "iso", "aut", "class_ms")]
        require(min(values) >= 0, f"{segment.label} 24T{key} nonnegative")
        running = [a + b for a, b in zip(running, values)]
        require(line_index + 1 < len(data_lines) and data_lines[line_index + 1].startswith("CHECKPOINT\t"), f"{segment.label} 24T{key} adjacent CP")
        checkpoint = pairs(data_lines[line_index + 1], 1)
        require(int(checkpoint["LAST_COMPLETE_K"]) == key and int(checkpoint["PROCESSED"]) == position, f"{segment.label} 24T{key} CP key")
        if pc:
            require(int(checkpoint["ISO_MS"]) == running[2], f"{segment.label} 24T{key} CP iso")
        require(int(checkpoint["ORDER8_CLASSES"]) == running[0] and int(checkpoint["RAW_PAIRS"]) == running[1], f"{segment.label} 24T{key} CP sums")
    scan_lines = [x for x in data_lines if x.startswith("SCAN_CHECKPOINT\t")]
    require(len(scan_lines) == len(segment.scans), f"{segment.label} scan count")
    for line, key in zip(scan_lines, segment.scans):
        scan, prefix = pairs(line, 1), [e for e in entries if int(e["key"]) <= key]
        require(int(scan["LAST_COMPLETE_K"]) == key, f"{segment.label} scan key")
        require(int(scan["ORDER_WINDOW"]) == len(keys(WIN, segment.lo, key)), f"{segment.label} scan window")
        require(int(scan["PROCESSED"]) == len(prefix), f"{segment.label} scan processed")
        require(int(scan["ORDER8_CLASSES"]) == sum(int(e["classes"]) for e in prefix), f"{segment.label} scan classes")
        require(int(scan["RAW_PAIRS"]) == sum(int(e["raw"]) for e in prefix), f"{segment.label} scan raw")
        if pc:
            require(int(scan["ISO_MS"]) == sum(int(e["iso"]) for e in prefix), f"{segment.label} scan iso")
    total = next(x for x in data_lines if x.startswith("TOTAL\t"))
    middle = r"\tISO_MS\t(\d+)" if pc else ""
    pattern = re.compile(rf"^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t{segment.lo}\t{segment.hi}\tLAST_COMPLETE_K\t{segment.hi}"
        rf"\tORDER_WINDOW\t{segment.window}\tPROCESSED\t{segment.parity}\tORDER8_CLASSES\t(\d+)\tRAW_PAIRS\t(\d+)" + middle + r"\tAUT_MS\t(\d+)\tCLASS_MS\t(\d+)\tMS\t(\d+)$")
    match = pattern.match(total)
    require(match is not None, f"{segment.label} TOTAL schema")
    groups = list(map(int, match.groups()))
    outcome = tuple(groups) if pc else (groups[0], groups[1], 0, groups[2], groups[3], groups[4])
    require(outcome == segment.expected and tuple(running) == outcome[:5], f"{segment.label} outcome")
    stdout, stderr = (BASE / segment.stdout).read_text(encoding="utf-8").strip(), (BASE / segment.stderr).read_text(encoding="utf-8")
    require(stdout == f"WROTE /mnt/d/work/revise/production_code/escalations/{segment.output}", f"{segment.label} stdout")
    require(segment.wrapper in stderr and "Exit status: 0" in stderr, f"{segment.label} telemetry")
    wall = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)", stderr)
    rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", stderr)
    require(wall is not None and wall.group(1).strip() == segment.wall, f"{segment.label} wall")
    require(rss is not None and int(rss.group(1)) == segment.rss and segment.rss < 50331648, f"{segment.label} RSS")
    return entries, outcome


checked = [check_segment(segment) for segment in SEGMENTS]
require(all(SEGMENTS[i].hi + 1 == SEGMENTS[i + 1].lo for i in range(2)), "segment adjacency")
full_parity, full_window = keys(SOL, 13929, 14218), keys(WIN, 13929, 14218)
require(len(full_window) == 290 and len(full_parity) == 287, "full sealed counts")
all_entries = sorted((e for entries, _ in checked for e in entries), key=lambda e: int(e["key"]))
require([int(e["key"]) for e in all_entries] == full_parity, "full disjoint entry union")
pc_entries = [e for e in all_entries if e["representation"] == "pc_transport"]
native_entries = [e for e in all_entries if e["representation"] == "native"]
require(len(pc_entries) == 269 and all(e["solvable"] == "true" for e in pc_entries), "full pc route")
require(len(native_entries) == 18 and all(e["solvable"] == "false" for e in native_entries), "full native route")
totals = tuple(sum(outcome[i] for _, outcome in checked) for i in range(6))
classes, raw, iso_ms, aut_ms, class_ms, gap_ms = totals
require(totals == (27993, 735868992, 300, 138459, 167366, 316064), "full outcome totals")
wall, max_rss = "5:19.80", 259776

merged = ["CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD21-MERGED-ROUTED", "GAP_VERSION\t4.12.1",
    "DATABASE\t25000", "RANGE\t13929\t14218", "ORDER_WINDOW\t290", "PARITY_KEYS\t287",
    "SEGMENTS\t13929..13984:pc\t13985..14002:native\t14003..14218:pc", "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates."]
for e in all_entries:
    merged.append("\t".join(["ENTRY", f"24T{e['key']}", "ORDER", str(e["order"]), "SOLVABLE_G", str(e["solvable"]),
        "PARITY_MAPS", str(e["parity"]), "REPRESENTATION", str(e["representation"]), "PC_ORDER", str(e["pc_order"]),
        "AUT_ORDER", str(e["aut_order"]), "ISO_MS", str(e["iso"]), "AUT_MS", str(e["aut"]), "METHOD", str(e["method"]),
        "CLASS_MS", str(e["class_ms"]), "ORDER8_CLASSES", str(e["classes"]), "RAW_PAIRS", str(e["raw"])]))
merged.extend([f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t13929\t14218\tORDER_WINDOW\t290\tPROCESSED\t287\tPC_TRANSPORT\t269\tNATIVE_NONSOLVABLE\t18\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}", "DONE"])
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_13929_14218_MERGED_ROUTED_GPT56SOL.txt").write_text("\n".join(merged) + "\n", encoding="utf-8", newline="\n")

verify = ["CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD21", "RANGE\t13929\t14218",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "ORDER_WINDOW\t290", "PARITY_KEYS\t287", "ENTRY_KEYS_EXACT\tPASS",
    "SOLVABLE_PC_ROUTE\t269\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t18\tPASS", "PC_ORDER_PARITY_TRANSPORT\t269\tPASS",
    "RAW_IDENTITIES\t287\tPASS", "ENTRY_CHECKPOINT_PAIRS\t287\tPASS", "SCAN_CHECKPOINTS\t11\tPASS",
    "UNIQUE_TOTAL_DONE_NO_GUARD\t3\tPASS", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}",
    f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}", f"MAX_RSS_KB\t{max_rss}",
    "SEALED_KEYSETS_AND_STREAMS\tPASS", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE"]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_VERIFY_GPT56SOL.txt").write_text("\n".join(verify) + "\n", encoding="utf-8", newline="\n")

ratio, raw_ratio = (aut_ms + class_ms) / 366213, raw / 432407712
aggregate = ["CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD21", "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED",
    "DEGREE\t24", "DATABASE\t25000", "RANGE\t13929\t14218", "LAST_COMPLETE_K\t14218", "ORDER_WINDOW\t290", "PARITY_KEYS\t287",
    "PARITY_EXCLUDED\t3", "SEGMENTS\t13929..13984-pc;13985..14002-native;14003..14218-pc", "PC_TRANSPORT_KEYS\t269",
    "NATIVE_NONSOLVABLE_KEYS\t18", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}",
    f"CLASS_MS\t{class_ms}", f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", "POINT_FORECAST_MS\t366213",
    f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}", "POINT_FORECAST_CLASSES\t12449", "POINT_FORECAST_RAW_PAIRS\t432407712",
    f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}", "ENTRY_CHECKPOINT_PAIRS\t287", "SCAN_CHECKPOINTS\t11", "RAW_IDENTITIES_PASS\t287",
    "PC_TRANSPORT_IDENTITIES_PASS\t269", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "INTERNAL_GUARD_MS\t1320000",
    "EXTERNAL_WALL_GUARD_SECONDS\t1400", f"WALL\t{wall}", "S1_WALL\t1:30.39", "S2_WALL\t0:43.80", "S3_WALL\t3:05.61",
    f"MAX_RSS_KB\t{max_rss}", "EXTERNAL_GUARD_EVENTS\t0", "GUARD_TRIGGERED_FINAL_SEGMENT\t0", "VERIFY\tPASS",
    "SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 13929..14218 only. This is not full degree-24 closure and contains no seed test.", "DONE"]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_AGGREGATE_GPT56SOL.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")

certificate = ["# Degree-24 exact Aut/order-8 profile - shard 21", "",
    "Status: **complete and independently verified for catalogue range `13929..14218` only**. This is not full degree-24 closure.", "",
    "Sealed evidence gives 290 order-window and 287 parity-capable keys: 269 solvable and 18 nonsolvable. The nonsolvable keys are exactly `13985..14002`; parity exclusions are exactly `14050..14052`. The exact contiguous routing is PC `13929..13984`, native `13985..14002`, and PC `14003..14218`.", "",
    "For every solvable key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation, preserving automorphism order and conjugacy. GAP checks group order and exact C2-epimorphism counts on both sides. The nonsolvable block is computed directly on the permutation group.", "",
    f"Exact totals: {classes:,} exact-order-8 classes; {raw:,} raw pairs; ISO/AUT/class times {iso_ms:,}/{aut_ms:,}/{class_ms:,} ms; GAP time {gap_ms:,} ms; wall {wall}; peak RSS {max_rss:,} KiB. All 287 entry/checkpoint pairs, 11 scan checkpoints, key sets, raw identities, 269 PC transports, headers, totals, terminals, streams, guards, and resources pass.", "",
    "No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard 21 is sealed; shard 22 remains unrun."]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_GPT56SOL_CERTIFICATE.md").write_text("\n".join(certificate) + "\n", encoding="utf-8", newline="\n")
print(f"PASS shard21 range=13929-14218 window=290 parity=287 pc=269 native=18 classes={classes} raw={raw} isoMs={iso_ms} autMs={aut_ms} classMs={class_ms} gapMs={gap_ms} wall={wall} maxRssKb={max_rss}")
