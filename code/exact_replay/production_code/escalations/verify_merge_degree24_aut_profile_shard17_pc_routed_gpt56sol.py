from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 17, "lo": 13098, "hi": 13302, "window": 205, "parity": 205,
    "exclusions": [], "scans": [13100, 13125, 13150, 13175, 13200, 13225, 13250, 13275, 13300],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt", "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt", "GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard17_13098_13302_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_13098_13302_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD17_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD17_RUN_STDERR_GPT56SOL.txt",
    "outcome": [41083, 1009655808, 315, 111403, 228291, 353662], "wall": "5:55.20", "rss": 179904,
    "forecast_ms": 365925, "forecast_classes": 13120, "forecast_raw": 322437120,
    "map_note": "Two sealed map slices splice disjointly at catalogue keys 13274/13275 and jointly cover this range exactly.",
})
print(
    "PASS shard17 range=13098-13302 window=205 parity=205 pc=205 native=0 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
