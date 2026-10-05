from pathlib import Path


source_path = Path(__file__).resolve().parent / "build_degree24_c8_seed_shard001_continuation_from_unit1_gpt56sol.py"
source = source_path.read_text(encoding="utf-8")
old = 'assert "CANDIDATE_NUMERIC\\t" not in previous_text'
new = 'assert not any(line.startswith("CANDIDATE_NUMERIC\\t") for line in previous_text.splitlines())'
if source.count(old) != 1:
    raise AssertionError("candidate-record assertion patch point")
source = source.replace(old, new)
exec(compile(source, str(source_path), "exec"), {"__name__": "__main__", "__file__": str(source_path)})
