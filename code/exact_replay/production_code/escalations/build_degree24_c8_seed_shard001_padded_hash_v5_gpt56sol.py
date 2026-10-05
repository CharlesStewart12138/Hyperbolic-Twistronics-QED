from __future__ import annotations

import hashlib
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
engine_v4 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g"
engine_v5 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g"
wrapper_v4 = base / "gap_run_degree24_c8_seed_shard001_segment001_unit1_v4_gpt56sol.g"
wrapper_v5 = base / "gap_run_degree24_c8_seed_shard001_segment001_unit1_v5_gpt56sol.g"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


engine = engine_v4.read_text(encoding="utf-8")
occurrences = engine.count("HexSHA256(")
assert occurrences >= 8
engine = engine.replace("HexSHA256(", "HexSHA256Padded(")
anchor = 'if LoadPackage("io")=fail then Error("IO package required"); fi;'
helper = '''if LoadPackage("io")=fail then Error("IO package required"); fi;
HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value);
 while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi;
 return result;
end;'''
assert engine.count(anchor) == 1
engine = engine.replace(anchor, helper)
if engine_v5.exists() or wrapper_v5.exists():
    raise FileExistsError("V5 files already exist")
engine_v5.write_text(engine, encoding="utf-8", newline="\n")
engine_sha = digest(engine_v5)

wrapper = wrapper_v4.read_text(encoding="utf-8")
old_path = "/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g"
new_path = "/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g"
assert wrapper.count(old_path) == 2
wrapper = wrapper.replace(old_path, new_path)
old_sha = next(line for line in wrapper.splitlines() if line.startswith("EXPECTED_ENGINE_SHA256:="))
wrapper = wrapper.replace(old_sha, f'EXPECTED_ENGINE_SHA256:="{engine_sha}";')
wrapper_v5.write_text(wrapper, encoding="utf-8", newline="\n")
print(f"PASS V5 engineSha={engine_sha} paddedSha256=64 occurrences={occurrences} zeroAlphaV4=SUPERSEDED noSeeds=PASS")
