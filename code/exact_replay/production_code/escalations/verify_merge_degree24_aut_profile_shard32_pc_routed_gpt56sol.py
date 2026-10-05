from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 32, "lo": 15847, "hi": 25000, "window": 135, "parity": 135,
    "exclusions": [], "scans": [k for k in range(15847, 25001) if k % 25 == 0],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard32_15847_25000_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_15847_25000_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD32_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD32_RUN_STDERR_GPT56SOL.txt",
    "outcome": [116569, 5729599488, 146, 88927, 574197, 674452], "wall": "11:18.97", "rss": 4549440,
    "forecast_ms": 366660, "forecast_classes": 43200, "forecast_raw": 2123366400,
    "map_note": "The complete sealed `13275..25000` parity and solvability slices cover the full range; exact active keys are `15847..15981`, and `15982..25000` is an exactly scanned zero-window tail.",
})
print(
    "PASS shard32 range=15847-25000 window=135 parity=135 pc=135 native=0 tail=15982-25000 scans=367 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
