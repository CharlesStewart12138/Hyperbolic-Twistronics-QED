from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 30, "lo": 15577, "hi": 15711, "window": 135, "parity": 135,
    "exclusions": [], "scans": [15600, 15625, 15650, 15675, 15700],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard30_15577_15711_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_15577_15711_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD30_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD30_RUN_STDERR_GPT56SOL.txt",
    "outcome": [57857, 2843787264, 197, 81868, 181877, 271314], "wall": "4:32.90", "rss": 173952,
    "forecast_ms": 366660, "forecast_classes": 43200, "forecast_raw": 2123366400,
    "map_note": "The sealed `13275..25000` parity and solvability slice covers this range exactly.",
})
print(
    "PASS shard30 range=15577-15711 window=135 parity=135 pc=135 native=0 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
