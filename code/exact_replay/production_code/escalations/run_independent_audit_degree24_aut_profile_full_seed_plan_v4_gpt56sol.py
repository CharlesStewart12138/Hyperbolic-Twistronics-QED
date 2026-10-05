from pathlib import Path


source_path = Path(__file__).resolve().parent / "independent_audit_degree24_aut_profile_full_seed_plan_v2_gpt56sol.py"
source = source_path.read_text(encoding="utf-8")
transport_old = '    must(int(row["PC_ORDER"]) == order, f"transport identity 24T{key}")'
transport_new = '''    pc_order = int(row["PC_ORDER"])
    if row["ROUTE"] == "pc":
        must(pc_order == order, f"pc transport identity 24T{key}")
    else:
        must(pc_order in (0, order), f"native representation order 24T{key}")'''
label_old = "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-SECOND-AUDIT-V2"
label_new = "PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FULL-SECOND-AUDIT-V4"
if source.count(transport_old) != 1 or source.count(label_old) != 1:
    raise AssertionError("V4 correction patch points")
source = source.replace(transport_old, transport_new).replace(label_old, label_new)
namespace = {"__name__": "__main__", "__file__": str(source_path)}
exec(compile(source, str(source_path), "exec"), namespace)
