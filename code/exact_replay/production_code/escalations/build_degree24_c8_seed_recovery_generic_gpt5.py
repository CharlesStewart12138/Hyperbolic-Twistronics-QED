#!/usr/bin/env python3
"""Build a no-replay recovery segment from the latest durable checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path


B = Path(__file__).resolve().parent
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    if temp.exists():
        raise RuntimeError(f"stale temp: {temp}")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


def pairs(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    return dict(zip(parts[start::2], parts[start + 1::2], strict=True))


parser = argparse.ArgumentParser()
parser.add_argument("--shard", type=int, required=True)
args = parser.parse_args()
shard = args.shard
assert 6 <= shard <= 905
tag = f"{shard:03d}"

summary = None
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[:2] == ["SHARD", str(shard)]:
        summary = pairs(parts, 2)
        break
assert summary is not None
total_units = int(summary["CLASS_UNITS"])

checkpoint = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CHECKPOINT_GPT56SOL.txt"
checkpoint_tmp = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CHECKPOINT_TMP_GPT56SOL.txt"
assert checkpoint.exists() and not checkpoint_tmp.exists()
cp_data = checkpoint.read_bytes()
cp_sha = digest(cp_data)
cp_lines = cp_data.decode("ascii").splitlines()
assert len(cp_lines) == 3
assert cp_lines[0] == f"CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD{tag}"
assert cp_lines[2] == "DONE"
payload, payload_sha = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert digest(payload.encode("ascii")) == payload_sha
parts = payload.split("\t")
assert parts[:2] == ["SHARD", tag]
cp = pairs(parts, 2)
current_unit = int(cp["UNIT"])
next_unit = int(cp["NEXT_UNIT"])
assert next_unit == current_unit + 1 and 1 <= current_unit < total_units
prefix_bytes = int(cp["OUTPUT_PREFIX_BYTES"])
prefix_sha = cp["OUTPUT_PREFIX_SHA256"]
counter_names = (
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
)
counters = [int(cp[name]) for name in counter_names]
assert counters[0] == current_unit and counters[2] == current_unit

wrappers: list[tuple[int, Path]] = []
for path in B.glob(f"gap_run_degree24_c8_seed_shard{tag}_segment*_unit*_postverify_v7_gpt56sol.g"):
    match = re.search(r"_segment([0-9]+)_", path.name)
    assert match
    wrappers.append((int(match.group(1)), path))
assert wrappers
wrappers.sort()
assert len({segment for segment, _ in wrappers}) == len(wrappers)
source_segment, source_wrapper = wrappers[-1]
new_segment = source_segment + 1
source_text = source_wrapper.read_text(encoding="ascii")
out_match = re.search(r'^OUT:="([^"]+)";$', source_text, flags=re.MULTILINE)
assert out_match
source_output = Path(out_match.group(1).replace("/mnt/d/", "D:/"))
assert source_output.parent.resolve() == B.resolve() and source_output.exists()
physical = source_output.read_bytes()
assert physical.startswith(f"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD{tag}".encode("ascii"))
assert len(physical) >= prefix_bytes
prefix = physical[:prefix_bytes]
suffix = physical[prefix_bytes:]
assert digest(prefix) == prefix_sha
prefix_lines = prefix.decode("ascii").splitlines()
assert prefix_lines[-1].startswith(
    f"ALPHA_DONE\tUNIT\t{current_unit}\tKEY\t{cp['KEY']}\tALPHA\t{cp['ALPHA']}\t"
)
suffix_text = suffix.decode("ascii")
assert f"CHECKPOINT_COMMITTED\tUNIT\t{next_unit}\t" not in suffix_text
assert f"ALPHA_DONE\tUNIT\t{next_unit + 1}\t" not in suffix_text
assert "\nTOTAL\t" not in suffix_text and "\nTOTAL_PARTIAL\t" not in suffix_text

segment_label = f"{new_segment:03d}"
output_name = (
    f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT{segment_label}_"
    f"UNIT{next_unit}_{total_units}_POSTVERIFY_V7_GPT56SOL.txt"
)
wrapper = B / (
    f"gap_run_degree24_c8_seed_shard{tag}_segment{segment_label}_"
    f"unit{next_unit}_{total_units}_postverify_v7_gpt56sol.g"
)
runner = B / f"run_degree24_c8_seed_shard{tag}_segment{segment_label}_postverify_v7.sh"
parse = B / f"gap_parse_smoke_degree24_c8_seed_shard{tag}_segment{segment_label}_v7_gpt56sol.g"
evidence = B / (
    f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT{source_segment:03d}_"
    f"RECOVERY_FROM_UNIT{current_unit}_EVIDENCE_GPT5.txt"
)
suffix_path = B / (
    f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT{source_segment:03d}_"
    f"POSTPREFIX_SUFFIX_AFTER_UNIT{current_unit}_GPT5.txt"
)
for path in (B / output_name, wrapper, runner, parse, evidence):
    assert not path.exists(), f"no-clobber {path}"
if suffix:
    assert not suffix_path.exists()
    atomic_write(suffix_path, suffix)

evidence_lines = [
    f"CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD{tag}-SEGMENT{source_segment:03d}-RECOVERY",
    "STATUS\tRECOVERABLE_DURABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT",
    "ORIGINAL_FILES_MODIFIED\t0", "SYNTHETIC_SCIENTIFIC_RECORDS_ADDED\t0",
    f"SOURCE_OUTPUT\t{source_output.name}\tBYTES\t{len(physical)}\tSHA256\t{digest(physical).upper()}",
    f"LAST_DURABLE_UNIT\t{current_unit}", f"NEXT_UNIT\t{next_unit}",
    f"LAST_DURABLE_KEY_ALPHA\t{cp['KEY']}\t{cp['ALPHA']}",
    f"CHECKPOINT_SHA256\t{cp_sha.upper()}", f"OUTPUT_PREFIX_BYTES\t{prefix_bytes}",
    f"OUTPUT_PREFIX_SHA256\t{prefix_sha.upper()}", f"POSTPREFIX_SUFFIX_BYTES\t{len(suffix)}",
]
if suffix:
    evidence_lines.append(f"POSTPREFIX_SUFFIX\t{suffix_path.name}\tSHA256\t{digest(suffix).upper()}")
evidence_lines += [
    f"RECOVERY\tSTART_UNIT{next_unit}; committed units1..{current_unit} are not replayed",
    "FAILED_PROCESS_ABSENT_REQUIRED\t1", "DONE", "",
]
evidence_data = "\n".join(evidence_lines).encode("ascii")
atomic_write(evidence, evidence_data)

new_text, count = re.subn(r'^OUT:="[^"]+";$',
    f'OUT:="/mnt/d/work/revise/production_code/escalations/{output_name}";',
    source_text, count=1, flags=re.MULTILINE)
assert count == 1
new_text, count = re.subn(r'INTERNAL_GUARD_MS:=[0-9]+; START_UNIT:=[0-9]+;',
    f'INTERNAL_GUARD_MS:=1320000; START_UNIT:={next_unit};', new_text, count=1)
assert count == 1
new_text, count = re.subn(r'INITIAL_COUNTERS:=\[[0-9,]+\];',
    'INITIAL_COUNTERS:=[' + ','.join(map(str, counters)) + '];', new_text, count=1)
assert count == 1
new_text, count = re.subn(r'PREVIOUS_CHECKPOINT_SHA256:="[^"]+";',
    f'PREVIOUS_CHECKPOINT_SHA256:="{cp_sha}";', new_text, count=1)
assert count == 1
new_text, count = re.subn(
    r'PREVIOUS_OUTPUT_FILE:="[^"]+"; PREVIOUS_OUTPUT_PREFIX_BYTES:=[0-9]+;',
    f'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/{source_output.name}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={prefix_bytes};',
    new_text, count=1)
assert count == 1
new_text, count = re.subn(r'PREVIOUS_OUTPUT_PREFIX_SHA256:="[^"]+";',
    f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{prefix_sha}";', new_text, count=1)
assert count == 1
wrapper_data = new_text.encode("ascii")
runner_data = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{wrapper.name}\n"
).encode("ascii")
engine_match = re.search(r'^ENGINE_FILE:="([^"]+)";$', new_text, flags=re.MULTILINE)
assert engine_match
parse_data = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{wrapper.name}");\n'
    f'if f=fail then Error("S{tag} segment{segment_label} wrapper parse failed"); fi;\n'
    f'g:=ReadAsFunction("{engine_match.group(1)}");\n'
    f'if g=fail then Error("S{tag} segment{segment_label} engine parse failed"); fi;\n'
    f'Print("SHARD{tag}_SEGMENT{segment_label}_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
atomic_write(wrapper, wrapper_data)
atomic_write(runner, runner_data)
atomic_write(parse, parse_data)

print(f"PASS SHARD={tag} START_UNIT={next_unit} PREVIOUS_UNIT={current_unit} NO_REPLAY=1")
print(f"CHECKPOINT={checkpoint.name} SHA256={cp_sha.upper()}")
print(f"SOURCE_OUTPUT={source_output.name} PHYSICAL_BYTES={len(physical)} PHYSICAL_SHA256={digest(physical).upper()}")
print(f"PREFIX_BYTES={prefix_bytes} PREFIX_SHA256={prefix_sha.upper()} SUFFIX_BYTES={len(suffix)}")
print(f"EVIDENCE={evidence.name} SHA256={digest(evidence_data).upper()}")
print(f"WRAPPER={wrapper.name} SHA256={digest(wrapper_data).upper()}")
print(f"RUNNER={runner.name} SHA256={digest(runner_data).upper()}")
print(f"PARSE={parse.name} SHA256={digest(parse_data).upper()}")
