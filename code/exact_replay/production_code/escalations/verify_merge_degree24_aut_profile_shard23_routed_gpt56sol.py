from __future__ import annotations

import sys
import types
from pathlib import Path


BASE = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
template_path = BASE / "verify_merge_degree24_aut_profile_shard21_routed_gpt56sol.py"
template = template_path.read_text(encoding="utf-8")
marker = "\nchecked = [check_segment(segment) for segment in SEGMENTS]"
assert template.count(marker) == 1
module = types.ModuleType("_sealed_shard21_verifier_preamble")
module.__file__ = str(template_path)
sys.modules[module.__name__] = module
namespace: dict[str, object] = module.__dict__
exec(compile(template.split(marker, 1)[0], str(template_path), "exec"), namespace)
Segment = namespace["Segment"]
require = namespace["require"]
check_segment = namespace["check_segment"]
keys = namespace["keys"]
SOL = namespace["SOL"]
WIN = namespace["WIN"]

segments = (
    Segment("S1", 14516, 14606, "pc_transport", 91, 89, (14525, 14550, 14575, 14600),
        "gap_run_degree24_aut_profile_shard23_s1_14516_14606_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14516_14606_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S1_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S1_RUN_STDERR_GPT56SOL.txt",
        (1513, 62387712, 103, 38871, 41425, 83801), "1:24.72", 145152),
    Segment("S2", 14607, 14634, "native", 28, 28, (14625,),
        "gap_run_degree24_aut_profile_shard23_s2_14607_14634_native_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14607_14634_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S2_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S2_RUN_STDERR_GPT56SOL.txt",
        (476, 21934080, 0, 9723, 52869, 63124), "1:04.01", 169920),
    Segment("S3", 14635, 14765, "pc_transport", 131, 131, (14650, 14675, 14700, 14725, 14750),
        "gap_run_degree24_aut_profile_shard23_s3_14635_14765_pc_domain_gpt56sol.g",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14635_14765_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S3_RUN_STDOUT_GPT56SOL.txt",
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_S3_RUN_STDERR_GPT56SOL.txt",
        (6530, 315566208, 136, 64511, 66705, 136631), "2:17.71", 183552),
)
checked = [check_segment(segment) for segment in segments]
require(all(segments[i].hi + 1 == segments[i + 1].lo for i in range(2)), "segment adjacency")
full_parity, full_window = keys(SOL, 14516, 14765), keys(WIN, 14516, 14765)
require(len(full_window) == 250 and len(full_parity) == 248, "full sealed counts")
all_entries = sorted((entry for entries, _ in checked for entry in entries), key=lambda entry: int(entry["key"]))
require([int(entry["key"]) for entry in all_entries] == full_parity, "full disjoint entry union")
pc_entries = [entry for entry in all_entries if entry["representation"] == "pc_transport"]
native_entries = [entry for entry in all_entries if entry["representation"] == "native"]
require(len(pc_entries) == 220 and all(entry["solvable"] == "true" for entry in pc_entries), "full pc route")
require(len(native_entries) == 28 and all(entry["solvable"] == "false" for entry in native_entries), "full native route")
totals = tuple(sum(outcome[i] for _, outcome in checked) for i in range(6))
classes, raw, iso_ms, aut_ms, class_ms, gap_ms = totals
require(totals == (8519, 399888000, 239, 113105, 160999, 283556), "full outcome totals")
wall, max_rss = "4:46.44", 183552

merged = ["CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD23-MERGED-ROUTED", "GAP_VERSION\t4.12.1",
    "DATABASE\t25000", "RANGE\t14516\t14765", "ORDER_WINDOW\t250", "PARITY_KEYS\t248",
    "SEGMENTS\t14516..14606:pc\t14607..14634:native\t14635..14765:pc", "SCOPE\tExact Aut/order-8 profile invariants only; no seed predicates."]
for entry in all_entries:
    merged.append("\t".join(["ENTRY", f"24T{entry['key']}", "ORDER", str(entry["order"]), "SOLVABLE_G", str(entry["solvable"]),
        "PARITY_MAPS", str(entry["parity"]), "REPRESENTATION", str(entry["representation"]), "PC_ORDER", str(entry["pc_order"]),
        "AUT_ORDER", str(entry["aut_order"]), "ISO_MS", str(entry["iso"]), "AUT_MS", str(entry["aut"]), "METHOD", str(entry["method"]),
        "CLASS_MS", str(entry["class_ms"]), "ORDER8_CLASSES", str(entry["classes"]), "RAW_PAIRS", str(entry["raw"])]))
merged.extend([f"TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t14516\t14765\tORDER_WINDOW\t250\tPROCESSED\t248\tPC_TRANSPORT\t220\tNATIVE_NONSOLVABLE\t28\tORDER8_CLASSES\t{classes}\tRAW_PAIRS\t{raw}\tISO_MS\t{iso_ms}\tAUT_MS\t{aut_ms}\tCLASS_MS\t{class_ms}\tSEGMENT_GAP_MS\t{gap_ms}", "DONE"])
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14516_14765_MERGED_ROUTED_GPT56SOL.txt").write_text("\n".join(merged) + "\n", encoding="utf-8", newline="\n")

verify = ["CERTIFICATE_VERIFY\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD23", "RANGE\t14516\t14765",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "ORDER_WINDOW\t250", "PARITY_KEYS\t248", "ENTRY_KEYS_EXACT\tPASS",
    "SOLVABLE_PC_ROUTE\t220\tPASS", "NONSOLVABLE_NATIVE_ROUTE\t28\tPASS", "PC_ORDER_PARITY_TRANSPORT\t220\tPASS",
    "RAW_IDENTITIES\t248\tPASS", "ENTRY_CHECKPOINT_PAIRS\t248\tPASS", "SCAN_CHECKPOINTS\t10\tPASS",
    "UNIQUE_TOTAL_DONE_NO_GUARD\t3\tPASS", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}",
    f"AUT_MS\t{aut_ms}", f"CLASS_MS\t{class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", f"WALL\t{wall}", f"MAX_RSS_KB\t{max_rss}",
    "SEALED_KEYSETS_AND_STREAMS\tPASS", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "VERIFY\tPASS", "DONE"]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_VERIFY_GPT56SOL.txt").write_text("\n".join(verify) + "\n", encoding="utf-8", newline="\n")

ratio, raw_ratio = (aut_ms + class_ms) / 367997, raw / 677173056
aggregate = ["CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD23", "STATUS\tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED",
    "DEGREE\t24", "DATABASE\t25000", "RANGE\t14516\t14765", "LAST_COMPLETE_K\t14765", "ORDER_WINDOW\t250", "PARITY_KEYS\t248",
    "PARITY_EXCLUDED\t2", "SEGMENTS\t14516..14606-pc;14607..14634-native;14635..14765-pc", "PC_TRANSPORT_KEYS\t220",
    "NATIVE_NONSOLVABLE_KEYS\t28", f"ORDER8_CLASSES\t{classes}", f"RAW_PAIRS\t{raw}", f"ISO_MS\t{iso_ms}", f"AUT_MS\t{aut_ms}",
    f"CLASS_MS\t{class_ms}", f"AUT_PLUS_CLASS_MS\t{aut_ms + class_ms}", f"SEGMENT_GAP_MS\t{gap_ms}", "POINT_FORECAST_MS\t367997",
    f"ACTUAL_TO_POINT_RATIO\t{ratio:.6f}", "POINT_FORECAST_CLASSES\t14725", "POINT_FORECAST_RAW_PAIRS\t677173056",
    f"ACTUAL_TO_RAW_POINT_RATIO\t{raw_ratio:.6f}", "ENTRY_CHECKPOINT_PAIRS\t248", "SCAN_CHECKPOINTS\t10", "RAW_IDENTITIES_PASS\t248",
    "PC_TRANSPORT_IDENTITIES_PASS\t220", "CANDIDATE_OR_SEED_PREDICATES\tNOT_RUN", "INTERNAL_GUARD_MS\t1320000",
    "EXTERNAL_WALL_GUARD_SECONDS\t1400", f"WALL\t{wall}", "S1_WALL\t1:24.72", "S2_WALL\t1:04.01", "S3_WALL\t2:17.71",
    f"MAX_RSS_KB\t{max_rss}", "EXTERNAL_GUARD_EVENTS\t0", "GUARD_TRIGGERED_FINAL_SEGMENT\t0", "VERIFY\tPASS",
    "SCOPE\tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 14516..14765 only. This is not full degree-24 closure and contains no seed test.", "DONE"]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_AGGREGATE_GPT56SOL.txt").write_text("\n".join(aggregate) + "\n", encoding="utf-8", newline="\n")

certificate = ["# Degree-24 exact Aut/order-8 profile - shard 23", "",
    "Status: **complete and independently verified for catalogue range `14516..14765` only**. This is not full degree-24 closure.", "",
    "Sealed evidence gives 250 order-window and 248 parity-capable keys: 220 solvable and 28 nonsolvable. The nonsolvable keys are exactly `14607..14634`; parity exclusions are exactly `14519` and `14537`. The exact contiguous routing is PC `14516..14606`, native `14607..14634`, and PC `14635..14765`.", "",
    "For every solvable key, an exact isomorphism from G to a pc group P induces an automorphism-group isomorphism by conjugation, preserving automorphism order and conjugacy. GAP checks group order and exact C2-epimorphism counts on both sides. The nonsolvable block is computed directly on the permutation group.", "",
    f"Exact totals: {classes:,} exact-order-8 classes; {raw:,} raw pairs; ISO/AUT/class times {iso_ms:,}/{aut_ms:,}/{class_ms:,} ms; GAP time {gap_ms:,} ms; wall {wall}; peak RSS {max_rss:,} KiB. All 248 entry/checkpoint pairs, 10 scan checkpoints, key sets, raw identities, 220 PC transports, headers, totals, terminals, streams, guards, and resources pass.", "",
    "No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run. Shard 23 is sealed; shard 24 remains unrun."]
(BASE / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_GPT56SOL_CERTIFICATE.md").write_text("\n".join(certificate) + "\n", encoding="utf-8", newline="\n")
print(f"PASS shard23 range=14516-14765 window=250 parity=248 pc=220 native=28 classes={classes} raw={raw} isoMs={iso_ms} autMs={aut_ms} classMs={class_ms} gapMs={gap_ms} wall={wall} maxRssKb={max_rss}")
