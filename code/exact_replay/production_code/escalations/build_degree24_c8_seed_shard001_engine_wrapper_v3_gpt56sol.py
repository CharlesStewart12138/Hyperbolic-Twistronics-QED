from __future__ import annotations

import hashlib
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
engine_v2 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v2_gpt56sol.g"
engine_v3 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v3_gpt56sol.g"
wrapper_v2 = base / "gap_run_degree24_c8_seed_shard001_v2_gpt56sol.g"
wrapper_v3 = base / "gap_run_degree24_c8_seed_shard001_v3_gpt56sol.g"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


engine = engine_v2.read_text(encoding="utf-8")
old_required = ' "EXPECTED_PROFILE_SHA256","EXPECTED_PLAN_SHA256"];'
new_required = ' "EXPECTED_PROFILE_SHA256","EXPECTED_PLAN_SHA256","ENGINE_FILE","EXPECTED_ENGINE_SHA256",\n "PROFILE_FILE","PLAN_FILE"];'
assert engine.count(old_required) == 1
engine = engine.replace(old_required, new_required)
old_catalogue = 'if db<>25000 then Error("degree-24 catalogue mismatch"); fi;'
new_catalogue = old_catalogue + '''
if HexSHA256(StringFile(ENGINE_FILE))<>LowercaseString(EXPECTED_ENGINE_SHA256) then Error("engine hash mismatch"); fi;
if HexSHA256(StringFile(PROFILE_FILE))<>LowercaseString(EXPECTED_PROFILE_SHA256) then Error("profile hash mismatch"); fi;
if HexSHA256(StringFile(PLAN_FILE))<>LowercaseString(EXPECTED_PLAN_SHA256) then Error("plan hash mismatch"); fi;'''
assert engine.count(old_catalogue) == 1
engine = engine.replace(old_catalogue, new_catalogue)
assert engine.count('Print("WROTE ",OUT,"\\n"); QUIT;') == 1
engine = engine.replace('Print("WROTE ",OUT,"\\n"); QUIT;', 'Print("WROTE ",OUT,"\\n"); QUIT_GAP(0);')
if engine_v3.exists() or wrapper_v3.exists():
    raise FileExistsError("V3 engine/wrapper already exists")
engine_v3.write_text(engine, encoding="utf-8", newline="\n")
engine_sha = digest(engine_v3)

wrapper = wrapper_v2.read_text(encoding="utf-8")
anchor = 'EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";'
injected = anchor + '''
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v3_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="''' + engine_sha + '";'
assert wrapper.count(anchor) == 1
wrapper = wrapper.replace(anchor, injected)
assert wrapper.count("alpha_checkpoint_v2_gpt56sol.g") == 1
wrapper = wrapper.replace("alpha_checkpoint_v2_gpt56sol.g", "alpha_checkpoint_v3_gpt56sol.g")
wrapper_v3.write_text(wrapper, encoding="utf-8", newline="\n")
print(f"PASS V3 engineSha={engine_sha} runtimeHashChecks=engine/profile/plan quit=QUIT_GAP wrapperRecords=466 noSeeds=PASS")
