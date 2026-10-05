#!/usr/bin/env python3
"""Resume-capable wrapper for the compute-first Degree-24 controller."""

from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "run_degree24_c8_seed_compute_first_controller_gpt5.py"
source = base.read_text(encoding="ascii")

old = '''        build_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDOUT_GPT5.txt"
        build_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDERR_GPT5.txt"
        rc = run_to_files([sys.executable, str(BUILDER), "--shard", str(shard)], build_out, build_err)
        if rc != 0:
            raise RuntimeError(f"builder exit {rc} shard{tag}")

        parse_script = B / f"gap_parse_smoke_degree24_c8_seed_shard{tag}_v7_gpt56sol.g"
        parse_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDOUT_GPT5.txt"
        parse_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDERR_GPT5.txt"
        wsl_parse = "/mnt/d/work/revise/production_code/escalations/" + parse_script.name
        rc = run_to_files(["wsl.exe", "bash", "-lc", f"gap -q {wsl_parse}"], parse_out, parse_err)
        if rc != 0 or f"SHARD{tag}_V7_WRAPPER_ENGINE_PARSE_PASS" not in parse_out.read_text(encoding="ascii"):
            raise RuntimeError(f"parse smoke failed shard{tag}, exit {rc}")
'''
new = '''        build_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDOUT_GPT5.txt"
        build_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDERR_GPT5.txt"
        runner = B / f"run_degree24_c8_seed_shard{tag}_segment001_postverify_v7.sh"
        wrapper = B / f"gap_run_degree24_c8_seed_shard{tag}_segment001_unit1_{totals[shard][0]}_postverify_v7_gpt56sol.g"
        parse_script = B / f"gap_parse_smoke_degree24_c8_seed_shard{tag}_v7_gpt56sol.g"
        bundle = [build_out, build_err, runner, wrapper, parse_script]
        if any(path.exists() for path in bundle):
            if not all(path.exists() for path in bundle):
                raise RuntimeError(f"incomplete prebuilt bundle shard{tag}")
            if build_err.stat().st_size != 0 or f"PASS SHARD={tag}" not in build_out.read_text(encoding="ascii"):
                raise RuntimeError(f"invalid prebuilt bundle shard{tag}")
            note(f"REUSE_PREBUILT_BUNDLE\\tSHARD\\t{tag}")
        else:
            rc = run_to_files([sys.executable, str(BUILDER), "--shard", str(shard)], build_out, build_err)
            if rc != 0:
                raise RuntimeError(f"builder exit {rc} shard{tag}")

        parse_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDOUT_GPT5.txt"
        parse_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDERR_GPT5.txt"
        wsl_parse = "/mnt/d/work/revise/production_code/escalations/" + parse_script.name
        if parse_out.exists() or parse_err.exists():
            if not parse_out.exists() or not parse_err.exists():
                raise RuntimeError(f"incomplete parse logs shard{tag}")
            rc = 0
            note(f"REUSE_PARSE_LOGS\\tSHARD\\t{tag}")
        else:
            rc = run_to_files(["wsl.exe", "bash", "-lc", f"gap -q {wsl_parse}"], parse_out, parse_err)
        parse_text = parse_out.read_text(encoding="ascii").replace("\\\\\\r\\n", "").replace("\\\\\\n", "")
        if rc != 0 or f"SHARD{tag}_V7_WRAPPER_ENGINE_PARSE_PASS" not in parse_text:
            raise RuntimeError(f"parse smoke failed shard{tag}, exit {rc}")
'''
assert source.count(old) == 1
source = source.replace(old, new)

old = '''        runner = B / f"run_degree24_c8_seed_shard{tag}_segment001_postverify_v7.sh"
        run_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT001_RUN_STDOUT_V7_GPT5.txt"
'''
new = '''        run_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT001_RUN_STDOUT_V7_GPT5.txt"
'''
assert source.count(old) == 1
source = source.replace(old, new)

namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#V2", "exec"), namespace)
