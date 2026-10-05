from pathlib import Path
import sys

from verify_single_pc_degree24_aut_profile_gpt56sol import verify_single_pc_profile


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
result = verify_single_pc_profile(base, {
    "shard": 29, "lo": 15441, "hi": 15576, "window": 136, "parity": 135,
    "exclusions": [15574], "scans": [15450, 15475, 15500, 15525, 15550, 15575],
    "solvability_maps": ["GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt"],
    "parity_maps": ["GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt"],
    "wrapper": "gap_run_degree24_aut_profile_shard29_15441_15576_pc_domain_gpt56sol.g",
    "output": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_15441_15576_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "stdout": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD29_RUN_STDOUT_GPT56SOL.txt",
    "stderr": "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD29_RUN_STDERR_GPT56SOL.txt",
    "outcome": [40840, 2007367680, 160, 75921, 189965, 273643], "wall": "4:35.36", "rss": 181824,
    "forecast_ms": 366660, "forecast_classes": 43200, "forecast_raw": 2123366400,
    "map_note": "The sealed `13275..25000` parity and solvability slice covers this range exactly.",
})
print(
    "PASS shard29 range=15441-15576 window=136 parity=135 pc=135 native=0 excluded=15574 "
    f"classes={result['classes']} raw={result['raw']} isoMs={result['iso_ms']} autMs={result['aut_ms']} "
    f"classMs={result['class_ms']} gapMs={result['gap_ms']} wall={result['wall']} maxRssKb={result['rss']}"
)
