from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 18, "lo": 13303, "hi": 13516, "window": 214, "parity": 206,
    "exclusions": [13491, 13492, 13494, 13495, 13496, 13497, 13498, 13499],
    "scans": [13325, 13350, 13375, 13400, 13425, 13450, 13475, 13500],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard18_13303_13516_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_13303_13516_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD18_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD18_RUN_STDERR_GPT56SOL.txt",
    "outcome": [60187, 1479155712, 227, 104390, 305763, 421949], "wall": "7:04.17", "rss": 1780032,
    "forecast_ms": 367710, "forecast_classes": 13184, "forecast_raw": 324009984,
    "map_note": "The sealed `13275..25000` parity and solvability slice covers this range exactly.",
})
print(
    "PASS shard18 range=13303-13516 window=214 parity=206 pc=206 native=0 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
