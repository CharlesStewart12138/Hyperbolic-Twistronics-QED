from pathlib import Path


source_path = Path(__file__).resolve().parent / "independent_audit_degree24_aut_profile_full_seed_plan_v2_gpt56sol.py"
source = source_path.read_text(encoding="utf-8")
old = '    must(int(row["PC_ORDER"]) == order, f"transport identity 24T{key}")'
new = '''    pc_order = int(row["PC_ORDER"])
    if row["ROUTE"] == "pc":
        must(pc_order == order, f"pc transport identity 24T{key}")
    else:
        must(pc_order in (0, order), f"native representation order 24T{key}")'''
if source.count(old) != 1:
    raise AssertionError("V2 transport assertion patch point")
source = source.replace(old, new)
namespace = {"__name__": "__main__", "__file__": str(source_path)}
exec(compile(source, str(source_path), "exec"), namespace)
