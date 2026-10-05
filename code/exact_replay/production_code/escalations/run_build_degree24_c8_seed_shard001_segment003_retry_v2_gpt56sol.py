from pathlib import Path

source = Path(__file__).with_name("build_degree24_c8_seed_shard001_segment003_retry_gpt56sol.py")
text = source.read_text(encoding="utf-8")
old = 'assert "CANDIDATE_NUMERIC\\t" not in tail'
new = 'assert not any(line.startswith("CANDIDATE_NUMERIC\\t") for line in tail.splitlines())'
assert text.count(old) == 1
text = text.replace(old, new)
namespace = {"__file__": str(source), "__name__": "__main__"}
exec(compile(text, str(source) + "#V2_EXACT_LINE_MATCH", "exec"), namespace)
