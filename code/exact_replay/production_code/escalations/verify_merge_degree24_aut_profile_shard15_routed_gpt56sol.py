from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


BASE = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def read_lines(name: str) -> list[str]:
    return (BASE / name).read_text(encoding="utf-8").splitlines()


def paired(line: str, start: int = 2) -> dict[str, str]:
    parts = line.split("\t")
    require((len(parts) - start) % 2 == 0, f"malformed pairs: {line}")
    result: dict[str, str] = {}
    for index in range(start, len(parts), 2):
        require(parts[index] not in result, f"duplicate field {parts[index]}")
        result[parts[index]] = parts[index + 1]
    return result


def load_map(name: str, has_solvable: bool) -> dict[int, dict[str, int]]:
    result: dict[int, dict[str, int]] = {}
    for line in read_lines(name):
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key = int(match.group(1))
        data = paired(line)
        require(key not in result, f"duplicate sealed 24T{key}")
        result[key] = {
            "order": int(data["ORDER"]),
            "parity": int(data["PARITY_MAPS"]),
            "solvable": int(data["SOLVABLE"]) if has_solvable else -1,
        }
    return result


SOL = load_map("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt", True)
WIN = load_map("GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt", False)


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
    Segment(
        "S1", 12596, 12612, "pc_transport", 17, 15, (12600,),
        "gap_run_degree24_aut_profile_shard15_s1_12596_12612_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12596_12612_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S1_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S1_RUN_STDERR_GPT56SOL.txt",
        (148, 3068928, 23, 3190, 2002, 5584), "0:06.26", 142080,
    ),
    Segment(
        "S2", 12613, 12621, "native", 9, 9, (),
        "gap_run_degree24_aut_profile_shard15_s2_12613_12621_native_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12613_12621_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S2_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S2_RUN_STDERR_GPT56SOL.txt",
        (66, 1520640, 0, 1881, 3679, 5640), "0:06.31", 151296,
    ),
    Segment(
        "S3", 12622, 12887, "pc_transport", 266, 261,
        (12625, 12650, 12675, 12700, 12725, 12750, 12775, 12800, 12825, 12850, 12875),
        "gap_run_degree24_aut_profile_shard15_s3_12622_12887_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12622_12887_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S3_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_S3_RUN_STDERR_GPT56SOL.txt",
        (21986, 536702496, 293, 103909, 137541, 253320), "4:14.49", 187776,
    ),
)


def keys(mapping: dict[int, object], lo: int, hi: int) -> list[int]:
    return sorted(k for k in mapping if lo <= k <= hi)


def parse_entry(line: str, representation: str) -> dict[str, int | str]:
    match = re.match(r"^ENTRY\t24T(\d+)\t", line)
    require(match is not None, f"malformed ENTRY: {line}")
    key = int(match.group(1))
    data = paired(line)
    common = {"ORDER", "SOLVABLE_G", "AUT_ORDER", "AUT_MS", "METHOD", "CLASS_MS", "ORDER8_CLASSES", "RAW_PAIRS"}
    require(common <= data.keys(), f"24T{key} common schema")
    if representation == "pc_transport":
        require({"PARITY_MAPS_G", "PC_ORDER", "PARITY_MAPS_P", "ISO_MS"} <= data.keys(), f"24T{key} pc schema")
        parity, pc_order, parity_p, iso = int(data["PARITY_MAPS_G"]), int(data["PC_ORDER"]), int(data["PARITY_MAPS_P"]), int(data["ISO_MS"])
    else:
        require("PARITY_MAPS" in data, f"24T{key} native parity")
        parity, pc_order, parity_p, iso = int(data["PARITY_MAPS"]), int(data["ORDER"]), int(data["PARITY_MAPS"]), 0
    return {
        "key": key, "order": int(data["ORDER"]), "solvable": data["SOLVABLE_G"], "parity": parity,
        "pc_order": pc_order, "parity_p": parity_p, "aut_order": int(data["AUT_ORDER"]), "iso": iso,
        "aut": int(data["AUT_MS"]), "method": data["METHOD"], "class_ms": int(data["CLASS_MS"]),
        "classes": int(data["ORDER8_CLASSES"]), "raw": int(data["RAW_PAIRS"]), "representation": representation,
    }


def check_segment(segment: Segment) -> tuple[list[dict[str, int | str]], tuple[int, int, int, int, int, int]]:
    lines = read_lines(segment.output)
    cert = "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT" if segment.representation == "pc_transport" else "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT"
    scope = "Exact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds." if segment.representation == "pc_transport" else "Exact Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for parity-capable order-window targets only; no seeds."
    header = [
        f"CERTIFICATE_PROFILE\t{cert}", "GAP_VERSION\t4.12.1", "DATABASE\t25000",
        f"RANGE\t{segment.lo}\t{segment.hi}", "GUARD_MS\t1320000",
        f"EXPECTED_ORDER_WINDOW\t{segment.window}", f"EXPECTED_PARITY\t{segment.parity}", f"SCOPE\t{scope}",
        "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.",
    ]
    require(lines[:9] == header, f"{segment.label} exact header")
    require(sum(line.startswith("TOTAL\t") for line in lines) == 1, f"{segment.label} unique TOTAL")
    require(lines.count("DONE") == 1 and lines[-1] == "DONE", f"{segment.label} DONE")
    require(not any(line.startswith(("TOTAL_PARTIAL\t", "STOPPED_GUARD")) for line in lines), f"{segment.label} guard")
    entry_lines = [(index, line) for index, line in enumerate(lines) if line.startswith("ENTRY\t")]
    entries = [parse_entry(line, segment.representation) for _, line in entry_lines]
    expected_keys = keys(SOL, segment.lo, segment.hi)
    require([int(entry["key"]) for entry in entries] == expected_keys, f"{segment.label} exact keyset")
    require(len(entries) == segment.parity, f"{segment.label} parity count")
    running = [0, 0, 0, 0, 0]
    for position, ((line_index, _), entry) in enumerate(zip(entry_lines, entries), start=1):
        key = int(entry["key"])
        sealed = SOL[key]
        require(entry["order"] == sealed["order"] and entry["parity"] == sealed["parity"], f"{segment.label} 24T{key} sealed fields")
        expected_solvable = "true" if sealed["solvable"] == 1 else "false"
        require(entry["solvable"] == expected_solvable, f"{segment.label} 24T{key} solvability")
        if segment.representation == "pc_transport":
            require(expected_solvable == "true", f"{segment.label} pc route")
            require(entry["pc_order"] == entry["order"] and entry["parity_p"] == entry["parity"], f"{segment.label} 24T{key} transport")
        else:
            require(expected_solvable == "false", f"{segment.label} native route")
        require(entry["raw"] == int(entry["order"]) * int(entry["classes"]), f"{segment.label} 24T{key} raw")
        require(int(entry["aut_order"]) > 0 and entry["method"] in {"pc", "native"}, f"{segment.label} 24T{key} Aut fields")
        values = [int(entry[name]) for name in ("classes", "raw", "iso", "aut", "class_ms")]
        require(min(values) >= 0, f"{segment.label} 24T{key} nonnegative")
        running = [a + b for a, b in zip(running, values)]
        require(line_index + 1 < len(lines) and lines[line_index + 1].startswith("CHECKPOINT\t"), f"{segment.label} 24T{key} adjacent checkpoint")
        checkpoint = paired(lines[line_index + 1], 1)
        require(int(checkpoint["LAST_COMPLETE_K"]) == key and int(checkpoint["PROCESSED"]) == position, f"{segment.label} 24T{key} checkpoint key/count")
        if segment.representation == "pc_transport":
            require(int(checkpoint["ISO_MS"]) == running[2], f"{segment.label} 24T{key} checkpoint ISO")
        require(int(checkpoint["ORDER8_CLASSES"]) == running[0] and int(checkpoint["RAW_PAIRS"]) == running[1], f"{segment.label} 24T{key} checkpoint sums")
    scan_lines = [line for line in lines if line.startswith("SCAN_CHECKPOINT\t")]
    require(len(scan_lines) == len(segment.scans), f"{segment.label} scan count")
    for line, key in zip(scan_lines, segment.scans):
        scan = paired(line, 1)
        prefix = [entry for entry in entries if int(entry["key"]) <= key]
        require(int(scan["LAST_COMPLETE_K"]) == key, f"{segment.label} scan key")
        require(int(scan["ORDER_WINDOW"]) == len(keys(WIN, segment.lo, key)), f"{segment.label} scan window")
        require(int(scan["PROCESSED"]) == len(prefix), f"{segment.label} scan processed")
        require(int(scan["ORDER8_CLASSES"]) == sum(int(entry["classes"]) for entry in prefix), f"{segment.label} scan classes")
        require(int(scan["RAW_PAIRS"]) == sum(int(entry["raw"]) for entry in prefix), f"{segment.label} scan raw")
        if segment.representation == "pc_transport":
            require(int(scan["ISO_MS"]) == sum(int(entry["iso"]) for entry in prefix), f"{segment.label} scan ISO")
    total_line = next(line for line in lines if line.startswith("TOTAL\t"))
    middle = r"\tISO_MS\t(\d+)" if segment.representation == "pc_transport" else ""
    pattern = re.compile(
        rf"^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t{segment.lo}\t{segment.hi}\tLAST_COMPLETE_K\t{segment.hi}"
        rf"\tORDER_WINDOW\t{segment.window}\tPROCESSED\t{segment.parity}\tORDER8_CLASSES\t(\d+)\tRAW_PAIRS\t(\d+)"
        + middle + r"\tAUT_MS\t(\d+)\tCLASS_MS\t(\d+)\tMS\t(\d+)$"
    )
    match = pattern.match(total_line)
    require(match is not None, f"{segment.label} TOTAL schema")
    groups = list(map(int, match.groups()))
    outcome = (groups[0], groups[1], groups[2], groups[3], groups[4], groups[5]) if segment.representation == "pc_transport" else (groups[0], groups[1], 0, groups[2], groups[3], groups[4])
    require(outcome == segment.expected, f"{segment.label} exact outcome")
    require(tuple(running) == outcome[:5], f"{segment.label} recomputed outcome")
    stdout_text = (BASE / segment.stdout).read_text(encoding="utf-8").strip()
    stderr_text = (BASE / segment.stderr).read_text(encoding="utf-8")
    require(stdout_text == f"WROTE /mnt/d/work/revise/production_code/escalations/{segment.output}", f"{segment.label} WROTE")
    require(segment.wrapper in stderr_text and "Exit status: 0" in stderr_text, f"{segment.label} telemetry binding/exit")
    wall_match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)", stderr_text)
    rss_match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", stderr_text)
    require(wall_match is not None and wall_match.group(1).strip() == segment.wall, f"{segment.label} wall")
    require(rss_match is not None and int(rss_match.group(1)) == segment.rss and segment.rss < 50331648, f"{segment.label} RSS")
    return entries, outcome


checked = [check_segment(segment) for segment in SEGMENTS]
require(all(SEGMENTS[index].hi + 1 == SEGMENTS[index + 1].lo for index in range(2)), "segment adjacency")
full_parity = keys(SOL, 12596, 12887)
full_window = keys(WIN, 12596, 12887)
require(len(full_window) == 292 and len(full_parity) == 285, "full sealed counts")
all_entries = sorted((entry for entries, _ in checked for entry in entries), key=lambda entry: int(entry["key"]))
require([int(entry["key"]) for entry in all_entries] == full_parity, "full disjoint entry union")
pc_entries = [entry for entry in all_entries if entry["representation"] == "pc_transport"]
native_entries = [entry for entry in all_entries if entry["representation"] == "native"]
require(len(pc_entries) == 276 and all(entry["solvable"] == "true" for entry in pc_entries), "full pc route")
require(len(native_entries) == 9 and all(entry["solvable"] == "false" for entry in native_entries), "full native route")
totals = tuple(sum(outcome[index] for _, outcome in checked) for index in range(6))
classes, raw, iso_ms, aut_ms, class_ms, gap_ms = totals
require(totals == (22200, 541292064, 316, 108980, 143222, 264544), "full outcome totals")
wall, max_rss = "4:27.06", 187776

merged = [
    "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD15-MERGED-ROUTED", "GAP_VERSION\t4.12.1",
    "DATABASE\t25000", "RANGE\t12596\t12887", "ORDER_WINDOW\t292", "PARITY_KEYS\t285",
    "SEGMENTS\t12596..12612:pc\t12613..12621:native\t12622..12887:pc", "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates.",
]
for entry in all_entries:
    merged.append("\t".join([
        "ENTRY", f"24T{entry['key']}", "ORDER", str(entry["order"]), "SOLVABLE_G", str(entry["solvable"]),
        "PARITY_MAPS", str(entry["parity"]), "REPRESENTATION", str(entry["representation"]), "PC_ORDER", str(entry["pc_order"]),
        "AUT_ORDER", str(entry["aut_order"]), "ISO_MS", str(entry["iso"]), "AUT_MS", str(entry["aut"]), "METHOD", str(entry["method"]),
        "CLASS_MS", str(entry["class_ms"]), "ORDER8_CLASSES", str(entry["classes"]), "RAW_PAIRS", str(entry["raw"]),
    ]))
merged.extend([
    f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t12596\t12887\tORDER_WINDOW\t292\tPROCESSED\t285\tPC_TRANSPORT\t276\tNATIVE_NONSOLVABLE\t9\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}", "DONE",
])
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12596_12887_MERGED_ROUTED_GPT56SOL.txt").write_text("\n".join(merged) + "\n", encoding="utf-8", newline="\n")

verify = [
    "CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD15", "RANGE\t12596\t12887",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "ORDER_WINDOW\t292", "PARITY_KEYS\t285", "ENTRY_KEYS_EXACT\tPASS",
    "SOLVABLE_PC_ROUTE\t276\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t9\tPASS", "PC_ORDER_PARITY_TRANSPORT\t276\tPASS",
    "RAW_IDENTITIES\t285\tPASS", "ENTRY_CHECKPOINT_PAIRS\t285\tPASS", "SCAN_CHECKPOINTS\t12\tPASS",
    "UNIQUE_TOTAL_DONE_NO_GUARD\t3\tPASS", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}",
    f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}", f"MAX_RSS_KB\t{max_rss}",
    "SEALED_KEYSETS_AND_STREAMS\tPASS", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_VERIFY_GPT56SOL.txt").write_text("\n".join(verify) + "\n", encoding="utf-8", newline="\n")

ratio = (aut_ms + class_ms) / 366103
raw_ratio = raw / 262944768
aggregate = [
    "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD15", "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED",
    "DEGREE\t24", "DATABASE\t25000", "RANGE\t12596\t12887", "LAST_COMPLETE_K\t12887", "ORDER_WINDOW\t292", "PARITY_KEYS\t285",
    "PARITY_EXCLUDED\t7", "SEGMENTS\t12596..12612-pc;12613..12621-native;12622..12887-pc", "PC_TRANSPORT_KEYS\t276",
    "NATIVE_NONSOLVABLE_KEYS\t9", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}",
    f"CLASS_MS\t{class_ms}", f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", "POINT_FORECAST_MS\t366103",
    f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}", "POINT_FORECAST_CLASSES\t10800", "POINT_FORECAST_RAW_PAIRS\t262944768",
    f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}", "ENTRY_CHECKPOINT_PAIRS\t285", "SCAN_CHECKPOINTS\t12", "RAW_IDENTITIES_PASS\t285",
    "PC_TRANSPORT_IDENTITIES_PASS\t276", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "INTERNAL_GUARD_MS\t1320000",
    "EXTERNAL_WALL_GUARD_SECONDS\t1400", f"WALL\t{wall}", "S1_WALL\t0:06.26", "S2_WALL\t0:06.31", "S3_WALL\t4:14.49",
    f"MAX_RSS_KB\t{max_rss}", "EXTERNAL_GUARD_EVENTS\t0", "FAILED_READONLY_AUDIT_ATTEMPTS\t2", "GUARD_TRIGGERED_FINAL_SEGMENT\t0",
    "VERIFY\tPASS", "SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 12596..12887 only. This is not full degree-24 closure and contains no seed test.", "DONE",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_AGGREGATE_GPT56SOL.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")

certificate = [
    "# Degree-24 exact Aut/order-8 profile - shard 15", "",
    "Status: **complete and independently verified for catalogue range `12596..12887` only**. This is not full degree-24 closure.", "",
    "Sealed evidence gives 292 order-window and 285 parity-capable keys: 276 solvable and nine nonsolvable. The nonsolvable keys are exactly `12613..12621`. The exact disjoint routing uses pc-domain segments `12596..12612` and `12622..12887`, with one native segment `12613..12621`. Their catalogue ranges are contiguous, nonoverlapping, and exhaustive.", "",
    "For each solvable key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation, preserving automorphism order and conjugacy. GAP checks group order and the exact C2-epimorphism count on both sides. The nonsolvable block is computed directly on the permutation group.", "",
    f"Exact totals: {classes:,} exact-order-8 classes; {raw:,} raw pairs; ISO/AUT/class times {iso_ms:,}/{aut_ms:,}/{class_ms:,} ms; GAP time {gap_ms:,} ms; wall {wall}; peak RSS {max_rss:,} KiB. All 285 entry/checkpoint pairs, 12 scan checkpoints, key sets, raw identities, 276 pc transports, headers, totals, terminals, streams, guards, and resource records pass.", "",
    "Two non-scientific interactive read-only commands had PowerShell path-token typos. Their records are preserved and excluded; neither modified any input nor affected GAP. The canonical verifier recomputes every invariant from sealed files.", "",
    "No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard 15 is sealed; shard 16 remains unrun.",
]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_GPT56SOL_CERTIFICATE.md").write_text("\n".join(certificate) + "\n", encoding="utf-8", newline="\n")
print(
    f"PASS shard15 range=12596-12887 window=292 parity=285 pc=276 native=9 classes={classes} raw={raw} "
    f"isoMs={iso_ms} autMs={aut_ms} classMs={class_ms} gapMs={gap_ms} wall={wall} maxRssKb={max_rss}"
)
