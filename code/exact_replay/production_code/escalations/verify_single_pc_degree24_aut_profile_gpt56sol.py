from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def verify_single_pc_profile(base: Path, config: dict[str, Any]) -> dict[str, int | str]:
    base = base.resolve()

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

    def load_map(names: list[str], has_solvable: bool) -> dict[int, dict[str, int]]:
        result: dict[int, dict[str, int]] = {}
        for name in names:
            for line in read(name):
                match = re.match(r"^ENTRY\t24T(\d+)\t", line)
                if not match:
                    continue
                key = int(match.group(1))
                data = pairs(line)
                require(key not in result, f"duplicate sealed 24T{key}")
                result[key] = {
                    "order": int(data["ORDER"]), "parity": int(data["PARITY_MAPS"]),
                    "solvable": int(data["SOLVABLE"]) if has_solvable else -1,
                }
        return result

    lo, hi, shard = config["lo"], config["hi"], config["shard"]
    sol = load_map(config["solvability_maps"], True)
    win = load_map(config["parity_maps"], False)
    parity_keys = sorted(k for k in sol if lo <= k <= hi)
    window_keys = sorted(k for k in win if lo <= k <= hi)
    require(len(window_keys) == config["window"], "sealed window count")
    require(len(parity_keys) == config["parity"], "sealed parity count")
    require(all(sol[k]["solvable"] == 1 for k in parity_keys), "all parity keys solvable")
    exclusions = [k for k in window_keys if k not in set(parity_keys)]
    require(exclusions == config["exclusions"], "sealed parity exclusions")

    lines = read(config["output"])
    header = [
        "CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT",
        "GAP_VERSION\t4.12.1", "DATABASE\t25000", f"RANGE\t{lo}\t{hi}", "GUARD_MS\t1320000",
        f"EXPECTED_ORDER_WINDOW\t{config['window']}", f"EXPECTED_PARITY\t{config['parity']}",
        "SCOPE\tExact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.",
        "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.",
    ]
    require(lines[:9] == header, "complete exact header")
    require(sum(line.startswith("TOTAL\t") for line in lines) == 1, "unique TOTAL")
    require(lines.count("DONE") == 1 and lines[-1] == "DONE", "unique terminal DONE")
    require(not any(line.startswith(("TOTAL_PARTIAL\t", "STOPPED_GUARD")) for line in lines), "no guard marker")

    entries: list[dict[str, int | str]] = []
    indices: list[int] = []
    for index, line in enumerate(lines):
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        key = int(match.group(1))
        data = pairs(line)
        required = {"ORDER", "SOLVABLE_G", "PARITY_MAPS_G", "PC_ORDER", "PARITY_MAPS_P", "AUT_ORDER", "ISO_MS", "AUT_MS", "METHOD", "CLASS_MS", "ORDER8_CLASSES", "RAW_PAIRS"}
        require(required <= data.keys(), f"24T{key} entry schema")
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
        require(entry["raw"] == int(entry["order"]) * int(entry["classes"]), f"24T{key} raw identity")
        require(int(entry["aut_order"]) > 0 and entry["method"] in {"pc", "native"}, f"24T{key} Aut fields")
        require(min(int(entry[name]) for name in ("iso", "aut", "class_ms", "classes", "raw")) >= 0, f"24T{key} nonnegative")
        classes += int(entry["classes"]); raw += int(entry["raw"]); iso_ms += int(entry["iso"]); aut_ms += int(entry["aut"]); class_ms += int(entry["class_ms"])
        require(index + 1 < len(lines) and lines[index + 1].startswith("CHECKPOINT\t"), f"24T{key} adjacent checkpoint")
        checkpoint = pairs(lines[index + 1], 1)
        require(int(checkpoint["LAST_COMPLETE_K"]) == key and int(checkpoint["PROCESSED"]) == position, f"24T{key} checkpoint key/count")
        require(int(checkpoint["ISO_MS"]) == iso_ms and int(checkpoint["ORDER8_CLASSES"]) == classes and int(checkpoint["RAW_PAIRS"]) == raw, f"24T{key} checkpoint sums")

    scan_lines = [line for line in lines if line.startswith("SCAN_CHECKPOINT\t")]
    require(len(scan_lines) == len(config["scans"]), "scan checkpoint count")
    for line, key in zip(scan_lines, config["scans"]):
        scan = pairs(line, 1)
        prefix = [entry for entry in entries if int(entry["key"]) <= key]
        require(int(scan["LAST_COMPLETE_K"]) == key, f"scan {key} key")
        require(int(scan["ORDER_WINDOW"]) == sum(lo <= item <= key for item in window_keys), f"scan {key} window")
        require(int(scan["PROCESSED"]) == len(prefix), f"scan {key} processed")
        require(int(scan["ISO_MS"]) == sum(int(entry["iso"]) for entry in prefix), f"scan {key} ISO")
        require(int(scan["ORDER8_CLASSES"]) == sum(int(entry["classes"]) for entry in prefix), f"scan {key} classes")
        require(int(scan["RAW_PAIRS"]) == sum(int(entry["raw"]) for entry in prefix), f"scan {key} raw")

    total_line = next(line for line in lines if line.startswith("TOTAL\t"))
    total_pattern = re.compile(
        rf"^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t{lo}\t{hi}\tLAST_COMPLETE_K\t{hi}"
        rf"\tORDER_WINDOW\t{config['window']}\tPROCESSED\t{config['parity']}\tORDER8_CLASSES\t(\d+)\tRAW_PAIRS\t(\d+)"
        r"\tISO_MS\t(\d+)\tAUT_MS\t(\d+)\tCLASS_MS\t(\d+)\tMS\t(\d+)$"
    )
    match = total_pattern.match(total_line)
    require(match is not None, "exact TOTAL schema")
    outcome = tuple(map(int, match.groups()))
    require(outcome[:5] == (classes, raw, iso_ms, aut_ms, class_ms), "TOTAL recomputation")
    require(outcome == tuple(config["outcome"]), "exact sealed outcome")
    gap_ms = outcome[5]

    stdout = (base / config["stdout"]).read_text(encoding="utf-8").strip()
    stderr = (base / config["stderr"]).read_text(encoding="utf-8")
    require(stdout == f"WROTE /mnt/d/work/revise/production_code/escalations/{config['output']}", "exact WROTE stdout")
    require(config["wrapper"] in stderr and "Exit status: 0" in stderr, "wrapper and exit telemetry")
    wall_match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)", stderr)
    rss_match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", stderr)
    require(wall_match is not None and rss_match is not None, "resource telemetry")
    wall, rss = wall_match.group(1).strip(), int(rss_match.group(1))
    require(wall == config["wall"] and rss == config["rss"] and rss < 50331648, "exact resources")

    prefix = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{shard}"
    merged_name = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_{lo}_{hi}_MERGED_ROUTED_GPT56SOL.txt"
    merged = [
        f"CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD{shard}-MERGED-ROUTED", "GAP_VERSION\t4.12.1",
        "DATABASE\t25000", f"RANGE\t{lo}\t{hi}", f"ORDER_WINDOW\t{config['window']}", f"PARITY_KEYS\t{config['parity']}",
        f"ROUTING\t{lo}..{hi}:pc;native-empty", "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates.",
    ]
    for entry in entries:
        merged.append("\t".join([
            "ENTRY", f"24T{entry['key']}", "ORDER", str(entry["order"]), "SOLVABLE_G", str(entry["solvable"]), "PARITY_MAPS", str(entry["parity"]),
            "REPRESENTATION", "pc_transport", "PC_ORDER", str(entry["pc_order"]), "AUT_ORDER", str(entry["aut_order"]), "ISO_MS", str(entry["iso"]),
            "AUT_MS", str(entry["aut"]), "METHOD", str(entry["method"]), "CLASS_MS", str(entry["class_ms"]), "ORDER8_CLASSES", str(entry["classes"]), "RAW_PAIRS", str(entry["raw"]),
        ]))
    merged.extend([f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t{lo}\t{hi}\tORDER_WINDOW\t{config['window']}\tPROCESSED\t{config['parity']}\tPC_TRANSPORT\t{config['parity']}\tNATIVE_NONSOLVABLE\t0\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}", "DONE"])
    (base / merged_name).write_text("\n".join(merged) + "\n", encoding="utf-8", newline="\n")

    verify_name = f"{prefix}_VERIFY_GPT56SOL.txt"
    verify = [
        f"CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD{shard}", f"RANGE\t{lo}\t{hi}",
        f"ORDER_WINDOW\t{config['window']}", f"PARITY_KEYS\t{config['parity']}", "ENTRY_KEYS_EXACT\tPASS",
        f"SOLVABLE_PC_ROUTE\t{config['parity']}\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t0\tPASS",
        f"PC_ORDER_PARITY_TRANSPORT\t{config['parity']}\tPASS", f"RAW_IDENTITIES\t{config['parity']}\tPASS",
        f"ENTRY_CHECKPOINT_PAIRS\t{config['parity']}\tPASS", f"SCAN_CHECKPOINTS\t{len(config['scans'])}\tPASS",
        "UNIQUE_TOTAL_DONE_NO_GUARD\tPASS", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}",
        f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}", f"MAX_RSS_KB\t{rss}",
        "SEALED_KEYSETS_AND_STREAMS\tPASS", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE",
    ]
    (base / verify_name).write_text("\n".join(verify) + "\n", encoding="utf-8", newline="\n")

    ratio = (aut_ms + class_ms) / config["forecast_ms"]
    raw_ratio = raw / config["forecast_raw"]
    aggregate_name = f"{prefix}_AGGREGATE_GPT56SOL.txt"
    aggregate = [
        f"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD{shard}", "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED",
        "DEGREE\t24", "DATABASE\t25000", f"RANGE\t{lo}\t{hi}", f"LAST_COMPLETE_K\t{hi}", f"ORDER_WINDOW\t{config['window']}",
        f"PARITY_KEYS\t{config['parity']}", f"PARITY_EXCLUDED\t{len(exclusions)}", f"SEGMENTS\t{lo}..{hi}-pc;native-empty",
        f"PC_TRANSPORT_KEYS\t{config['parity']}", "NATIVE_NONSOLVABLE_KEYS\t0", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}",
        f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}",
        f"SEGMENT_GAP_MS\t{gap_ms}", f"POINT_FORECAST_MS\t{config['forecast_ms']}", f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}",
        f"POINT_FORECAST_CLASSES\t{config['forecast_classes']}", f"POINT_FORECAST_RAW_PAIRS\t{config['forecast_raw']}",
        f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}", f"ENTRY_CHECKPOINT_PAIRS\t{config['parity']}",
        f"SCAN_CHECKPOINTS\t{len(config['scans'])}", f"RAW_IDENTITIES_PASS\t{config['parity']}",
        f"PC_TRANSPORT_IDENTITIES_PASS\t{config['parity']}", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN",
        "INTERNAL_GUARD_MS\t1320000", "EXTERNAL_WALL_GUARD_SECONDS\t1400", f"WALL\t{wall}", f"MAX_RSS_KB\t{rss}",
        "EXTERNAL_GUARD_EVENTS\t0", "GUARD_TRIGGERED_FINAL_SEGMENT\t0", "VERIFY\tPASS",
        f"SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range {lo}..{hi} only. This is not full degree-24 closure and contains no seed test.", "DONE",
    ]
    (base / aggregate_name).write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")

    certificate_name = f"{prefix}_GPT56SOL_CERTIFICATE.md"
    map_note = config.get("map_note", "The sealed parity and solvability evidence covers the range exactly.")
    certificate = [
        f"# Degree-24 exact Aut/order-8 profile - shard {shard}", "",
        f"Status: **complete and independently verified for catalogue range `{lo}..{hi}` only**. This is not full degree-24 closure.", "",
        f"{map_note} It gives {config['window']} order-window and {config['parity']} parity-capable keys, all solvable. The exact routing is one pc-domain segment and an empty native segment.", "",
        "For every included key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation, preserving automorphism order and conjugacy. GAP checks group order and exact C2-epimorphism counts on both sides.", "",
        f"Exact totals: {classes:,} exact-order-8 classes; {raw:,} raw pairs; ISO/AUT/class times {iso_ms:,}/{aut_ms:,}/{class_ms:,} ms; GAP time {gap_ms:,} ms; wall {wall}; peak RSS {rss:,} KiB. All {config['parity']} entry/checkpoint pairs, {len(config['scans'])} scan checkpoints, key sets, raw identities, transports, header, totals, terminals, streams, guards, and resources pass.", "",
        f"No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard {shard} is sealed; shard {shard + 1} remains unrun.",
    ]
    (base / certificate_name).write_text("\n".join(certificate) + "\n", encoding="utf-8", newline="\n")
    return {"classes": classes, "raw": raw, "iso_ms": iso_ms, "aut_ms": aut_ms, "class_ms": class_ms, "gap_ms": gap_ms, "wall": wall, "rss": rss, "merged": merged_name, "verify": verify_name, "aggregate": aggregate_name, "certificate": certificate_name}
