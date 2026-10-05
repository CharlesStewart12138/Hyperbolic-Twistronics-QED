from pathlib import Path

source = Path(__file__).with_name("rebuild_degree24_c8_seed_shard001_manifest_v2_gpt56sol.py")
text = source.read_text(encoding="utf-8")
old = "} - set(core))"
new = "} - set(core) - {EXCLUSIONS.name})"
assert text.count(old) == 1
text = text.replace(old, new)
namespace = {"__file__": str(source), "__name__": "__main__"}
exec(compile(text, str(source) + "#V2_EXCLUSIONS_FIX", "exec"), namespace)
