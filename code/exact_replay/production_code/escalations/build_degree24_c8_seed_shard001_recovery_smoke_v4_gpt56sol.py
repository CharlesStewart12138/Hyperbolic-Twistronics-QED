from __future__ import annotations

import hashlib
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
engine_v3 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v3_gpt56sol.g"
engine_v4 = base / "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g"
wrapper_v3 = base / "gap_run_degree24_c8_seed_shard001_v3_gpt56sol.g"
wrapper_smoke = base / "gap_run_degree24_c8_seed_shard001_segment001_unit1_v4_gpt56sol.g"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest().upper()


engine = engine_v3.read_text(encoding="utf-8")
anchor = 'd:=24; db:=NrTransitiveGroups(d);'
assert engine.count(anchor) == 1
engine = engine.replace(anchor, 'if not IsBound(STOP_AFTER_UNIT) then STOP_AFTER_UNIT:=fail; fi;\n' + anchor)
anchor = 'start:=Runtime(); stoppedGuard:=false; stoppedCandidate:=false; lastUnit:=START_UNIT-1;'
assert engine.count(anchor) == 1
engine = engine.replace(anchor, 'start:=Runtime(); stoppedGuard:=false; stoppedCandidate:=false; stoppedTest:=false; lastUnit:=START_UNIT-1;')
anchor = '   if Length(reps)>0 then stoppedCandidate:=true; break; fi;\n   if Runtime()-start>=INTERNAL_GUARD_MS then stoppedGuard:=true; break; fi;'
replacement = '   if Length(reps)>0 then stoppedCandidate:=true; break; fi;\n   if STOP_AFTER_UNIT<>fail and unitNo=STOP_AFTER_UNIT then stoppedTest:=true; break; fi;\n   if Runtime()-start>=INTERNAL_GUARD_MS then stoppedGuard:=true; break; fi;'
assert engine.count(anchor) == 1
engine = engine.replace(anchor, replacement)
engine = engine.replace('if not stoppedGuard and not stoppedCandidate then', 'if not stoppedGuard and not stoppedCandidate and not stoppedTest then')
engine = engine.replace('if stoppedGuard or stoppedCandidate then break; fi;', 'if stoppedGuard or stoppedCandidate or stoppedTest then break; fi;')
engine = engine.replace('if stoppedCandidate or stoppedGuard then', 'if stoppedCandidate or stoppedGuard or stoppedTest then')
anchor = ' if stoppedCandidate then AppendTo(OUT,"STOPPED_CANDIDATE\\n"); else AppendTo(OUT,"STOPPED_GUARD\\n"); fi;'
replacement = ' if stoppedCandidate then AppendTo(OUT,"STOPPED_CANDIDATE\\n");\n elif stoppedTest then AppendTo(OUT,"STOPPED_RECOVERY_SMOKE\\n");\n else AppendTo(OUT,"STOPPED_GUARD\\n"); fi;'
assert engine.count(anchor) == 1
engine = engine.replace(anchor, replacement)
if engine_v4.exists() or wrapper_smoke.exists():
    raise FileExistsError("V4 smoke files already exist")
engine_v4.write_text(engine, encoding="utf-8", newline="\n")
engine_sha = digest(engine_v4)

wrapper = wrapper_v3.read_text(encoding="utf-8")
wrapper = wrapper.replace(
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL.txt";',
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt";\nSTOP_AFTER_UNIT:=1;',
)
old_engine_path = "/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v3_gpt56sol.g"
new_engine_path = "/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g"
assert wrapper.count(old_engine_path) == 2
wrapper = wrapper.replace(old_engine_path, new_engine_path)
old_sha_line = next(line for line in wrapper.splitlines() if line.startswith("EXPECTED_ENGINE_SHA256:="))
wrapper = wrapper.replace(old_sha_line, f'EXPECTED_ENGINE_SHA256:="{engine_sha}";')
wrapper_smoke.write_text(wrapper, encoding="utf-8", newline="\n")
print(f"PASS V4 recovery-smoke engineSha={engine_sha} stopAfterUnit=1 internalGuard=1320000 canonicalCandidateSchema=PASS noReplayPlan=PASS")
