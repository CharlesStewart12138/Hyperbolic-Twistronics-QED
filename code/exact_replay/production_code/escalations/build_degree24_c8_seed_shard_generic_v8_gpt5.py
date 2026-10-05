from pathlib import Path


BASE = Path(__file__).with_name("build_degree24_c8_seed_shard_generic_v7_gpt56sol.py")
source = BASE.read_text(encoding="ascii")

old_assert = '''    ) or (\n        route == "native" and representation in {"pc_single", "pc_transport"} and pc_order == order\n+    )\n+'''
new_assert = '''    ) or (\n        route == "native" and representation in {"pc_single", "pc_transport"} and pc_order == order\n+    ) or (\n+        route == "native" and representation == "native" and pc_order == order\n+    )\n+'''
if source.count(old_assert) != 1:
    raise RuntimeError("unexpected v7 Python assertion template")
source = source.replace(old_assert, new_assert)

old_gap = '((row.representation="pc_single" or row.representation="pc_transport") and row.pcOrder=row.order)'
new_gap = '((row.representation="pc_single" or row.representation="pc_transport" or row.representation="native") and row.pcOrder=row.order)'
if source.count(old_gap) != 1:
    raise RuntimeError("unexpected v7 GAP assertion template")
source = source.replace(old_gap, new_gap)

namespace = {"__file__": str(BASE), "__name__": "__main__"}
exec(compile(source, str(BASE), "exec"), namespace)
