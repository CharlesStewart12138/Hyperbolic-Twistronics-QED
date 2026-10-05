from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 24, "lo": 14766, "hi": 14900, "window": 135, "parity": 135,
    "exclusions": [], "scans": [14775, 14800, 14825, 14850, 14875, 14900],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard24_14766_14900_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14766_14900_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_RUN_STDERR_GPT56SOL.txt",
    "outcome": [26622, 1308524544, 207, 72760, 185293, 265406], "wall": "4:26.51", "rss": 170112,
    "forecast_ms": 366660, "forecast_classes": 43200, "forecast_raw": 2123366400,
    "map_note": "The sealed `13275..25000` parity and solvability slice covers this range exactly.",
})
print(
    "PASS shard24 range=14766-14900 window=135 parity=135 pc=135 native=0 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
