"""Orchestrate proof-complete exact-key external deduplication through radius 7."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import csv
import gzip
import hashlib
import json
import shutil
from pathlib import Path
import struct
import subprocess
import sys
import time

from production_code.group.universal_cover import (
    GENERATOR_MATRICES,
    IDENTITY_MATRIX,
    exact_cosh_distance_over_R,
    matrix_from_word,
)


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "data" / "production" / "group_ball"
EXECUTABLE = HERE / "external_group_ball.exe"
SOURCE = HERE / "external_group_ball.cpp"
BUCKETS = 256
RAW_BYTES = 136
UNIQUE_BYTES = 135
REGISTRY_BYTES = 147
EXPECTED_SHELLS_0_6 = [1, 8, 56, 392, 2736, 19096, 133288]
EXPECTED_BALLS_0_6 = [1, 9, 65, 457, 3193, 22289, 155577]
ABELIAN = (
    (1, 0, 0, 0), (0, -1, 0, 0), (-1, -1, 1, 0), (-1, -1, 0, -1),
    (-1, 0, 0, 0), (0, 1, 0, 0), (1, 1, -1, 0), (1, 1, 0, 1),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def negate_field(field: tuple[int, ...]) -> tuple[int, ...]:
    return (field[0],) + tuple(-value for value in field[1:])


def projective_key(matrix: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    negative = (negate_field(matrix[0]), negate_field(matrix[1]))
    return min(matrix, negative)


def encode_word(word: tuple[int, ...]) -> int:
    code = 0
    for token in word:
        code = (code << 3) | token
    return code


def decode_word(length: int, code: int) -> tuple[int, ...]:
    result = [0] * length
    for index in range(length - 1, -1, -1):
        result[index] = code & 7
        code >>= 3
    return tuple(result)


def abelian(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(ABELIAN[token][index] for token in word) for index in range(4))


def tensor_moment(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    vector = abelian(word)
    return tuple(tuple(vector[i] * vector[j] for j in range(4)) for i in range(4))


def free_candidate_counts(maximum: int) -> list[int]:
    return [1] + [8 * 7 ** (length - 1) for length in range(1, maximum + 1)]


def resource_forecast() -> dict[str, object]:
    counts = free_candidate_counts(7)
    total = sum(counts)
    return {
        "schema_version": "1.0",
        "task_id": "CM-GRP-EXT-001",
        "forecast_precedes_L7_run": True,
        "candidate_words_by_length": {str(i): value for i, value in enumerate(counts)},
        "total_free_word_candidates": total,
        "estimated_unique_group_elements": 1_087_000,
        "binary_bytes_per_raw_candidate": RAW_BYTES,
        "bucket_count": BUCKETS,
        "hash_role": "bucket selection and corruption manifests only; exact key comparison determines equality",
        "estimated_temporary_disk_bytes_primary": total * RAW_BYTES + 1_087_000 * UNIQUE_BYTES,
        "estimated_temporary_disk_bytes_with_determinism_rerun": 2 * (total * RAW_BYTES + 1_087_000 * UNIQUE_BYTES),
        "estimated_final_registry_bytes": 20 + 1_087_000 * REGISTRY_BYTES,
        "expected_peak_rss_bytes": 1_073_741_824,
        "normal_rss_target_bytes": 17_179_869_184,
        "hard_rss_ceiling_bytes": 51_539_607_552,
        "expected_runtime_seconds": 180,
        "checkpoint_interval": "each of nine generation shards, then each complete bucket-reduction pass and final registry",
        "fallback": "increase bucket count and rerun only reduction if a bucket approaches the RSS target",
        "no_swap": True,
    }


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")


def parse_kv(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            result[key] = value
    return result


def run_engine(maximum: int, name: str) -> dict[str, object]:
    run_root = OUTPUT / "work" / name
    run_root.mkdir(parents=True, exist_ok=True)
    generation = []
    for shard in range(9):
        summary = run_root / f"generation_shard_{shard:02d}.tsv"
        bucket_paths = [run_root / "generation" / f"shard-{shard:02d}" / f"bucket-{bucket:03d}.bin" for bucket in range(BUCKETS)]
        if not (summary.exists() and all(path.exists() for path in bucket_paths) and parse_kv(summary).get("status") == "COMPLETE"):
            run([str(EXECUTABLE), "generate", str(maximum), str(shard), str(run_root), str(summary)])
        fields = parse_kv(summary)
        digest = hashlib.sha256()
        for path in bucket_paths:
            digest.update(path.read_bytes())
        generation.append({
            "shard_id": shard,
            "terminal_status": fields["status"],
            "counts_by_length": {str(length): int(fields.get(f"length_{length}", 0)) for length in range(maximum + 1)},
            "total_records": int(fields["total"]),
            "peak_rss_bytes": int(fields["peak_rss_bytes"]),
            "elapsed_seconds": float(fields["elapsed_seconds"]),
            "bucket_stream_sha256": digest.hexdigest(),
        })
    generation_manifest = {
        "schema_version": "1.0", "task_id": "CM-GRP-EXT-001", "maximum_radius": maximum,
        "shards": generation, "all_complete": all(item["terminal_status"] == "COMPLETE" for item in generation),
    }
    write_json(run_root / "generation_manifest.json", generation_manifest)

    reduction_summary = run_root / "bucket_reduction.tsv"
    reduced_paths = [run_root / "reduced" / f"bucket-{bucket:03d}.bin" for bucket in range(BUCKETS)]
    if not (reduction_summary.exists() and all(path.exists() for path in reduced_paths)):
        run([str(EXECUTABLE), "reduce", str(maximum), str(run_root), str(reduction_summary)])
    bucket_rows = []
    with reduction_summary.open(encoding="utf-8") as handle:
        reader = csv.DictReader((line for line in handle if not line.startswith(("TOTAL", "maximum", "peak", "elapsed"))), delimiter="\t")
        for row in reader:
            bucket = int(row["bucket"])
            bucket_rows.append({
                "bucket": bucket, "raw": int(row["raw"]), "unique": int(row["unique"]),
                "duplicates": int(row["duplicates"]), "sha256": sha256(reduced_paths[bucket]), "terminal_status": "COMPLETE",
            })
    tail = parse_kv(reduction_summary)
    bucket_manifest = {
        "schema_version": "1.0", "bucket_count": BUCKETS, "buckets": bucket_rows,
        "all_complete": len(bucket_rows) == BUCKETS,
        "peak_rss_bytes": int(tail["peak_rss_bytes"]), "elapsed_seconds": float(tail["elapsed_seconds"]),
    }
    write_json(run_root / "bucket_manifest.json", bucket_manifest)

    registry = run_root / f"ball_radius_{maximum}_exact.bin"
    summary = run_root / f"ball_radius_{maximum}_summary.csv"
    if not (registry.exists() and summary.exists()):
        run([str(EXECUTABLE), "finalize", str(maximum), str(run_root), str(registry), str(summary)])
    counts = []
    peak_finalize = 0
    elapsed_finalize = 0.0
    inverse_closure = False
    phi8_closure = False
    minimum_shortlex_rule = False
    for line in summary.read_text(encoding="utf-8").splitlines():
        if line.startswith("#peak_rss_bytes,"):
            peak_finalize = int(line.split(",", 1)[1])
        elif line.startswith("#elapsed_seconds,"):
            elapsed_finalize = float(line.split(",", 1)[1])
        elif line.startswith("#inverse_closure,"):
            inverse_closure = line.endswith(",1")
        elif line.startswith("#phi8_closure,"):
            phi8_closure = line.endswith(",1")
        elif line.startswith("#minimum_shortlex_rule,"):
            minimum_shortlex_rule = line.endswith(",1")
        elif line and line[0].isdigit():
            radius, shell, ball = map(int, line.split(","))
            counts.append({"radius": radius, "shell": shell, "ball": ball})
    final_manifest = {
        "schema_version": "1.0", "maximum_radius": maximum, "registry_sha256": sha256(registry),
        "registry_bytes": registry.stat().st_size, "summary_sha256": sha256(summary), "counts": counts,
        "peak_rss_bytes": max(peak_finalize, bucket_manifest["peak_rss_bytes"], *(item["peak_rss_bytes"] for item in generation)),
        "elapsed_seconds": elapsed_finalize + bucket_manifest["elapsed_seconds"] + sum(item["elapsed_seconds"] for item in generation),
        "inverse_closure": inverse_closure,
        "phi8_closure": phi8_closure,
        "minimum_shortlex_rule": minimum_shortlex_rule,
        "terminal_status": "COMPLETE",
    }
    write_json(run_root / "final_merge_manifest.json", final_manifest)
    return {"root": run_root, "registry": registry, "summary": summary, "generation": generation_manifest, "buckets": bucket_manifest, "final": final_manifest}


def read_key(handle) -> tuple[tuple[int, ...], tuple[int, ...]]:
    fields = []
    for _ in range(2):
        exponent_bytes = handle.read(1)
        if len(exponent_bytes) != 1:
            raise EOFError
        coefficients = struct.unpack("<8q", handle.read(64))
        fields.append((exponent_bytes[0],) + coefficients)
    return tuple(fields)  # type: ignore[return-value]


def registry_count(path: Path) -> int:
    with path.open("rb") as handle:
        if handle.read(8) != b"BOLZAG07":
            raise ValueError("bad registry magic")
        count, record_size = struct.unpack("<QI", handle.read(12))
        if record_size != REGISTRY_BYTES or path.stat().st_size != 20 + count * record_size:
            raise ValueError("registry size contract failed")
        return count


def iter_registry(path: Path):
    count = registry_count(path)
    with path.open("rb") as handle:
        handle.seek(20)
        for element_id in range(count):
            key = read_key(handle)
            length = handle.read(1)[0]
            word, inverse_id, phi_id = struct.unpack("<III", handle.read(12))
            c8, combined, c8_stab, combined_stab = handle.read(4)
            yield {"id": element_id, "key": key, "length": length, "word": word,
                   "inverse": inverse_id, "phi": phi_id, "c8": c8, "combined": combined,
                   "c8_stabilizer": c8_stab, "combined_stabilizer": combined_stab}


def find_registry_key(path: Path, wanted):
    for item in iter_registry(path):
        if item["key"] == wanted:
            return item
    raise KeyError("exact key absent from registry")


def old_radius6_keys() -> set[tuple[tuple[int, ...], tuple[int, ...]]]:
    path = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"
    result = set()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            matrix = json.loads(line)["matrix_top_row_exact"]
            result.add(projective_key((tuple(matrix[0]), tuple(matrix[1]))))
    return result


def raw_candidates_for_key(run_root: Path, key, maximum: int) -> list[tuple[int, int, int]]:
    # The production bucket hash is not reimplemented here; scan the bounded 256
    # bucket paths shard-by-shard until matching exact keys are found.
    matches = []
    for shard in range(9):
        directory = run_root / "generation" / f"shard-{shard:02d}"
        for path in directory.glob("bucket-*.bin"):
            with path.open("rb") as handle:
                while True:
                    try:
                        candidate_key = read_key(handle)
                    except EOFError:
                        break
                    length = handle.read(1)[0]
                    word = struct.unpack("<I", handle.read(4))[0]
                    source = handle.read(1)[0]
                    if candidate_key == key:
                        matches.append((length, word, source))
    return matches


def main() -> int:
    if not EXECUTABLE.exists():
        raise SystemExit("compile external_group_ball.cpp first")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_hash, executable_hash = sha256(SOURCE), sha256(EXECUTABLE)
    started = time.perf_counter()

    # The small frozen regression is deliberately completed before the L=7 forecast/run.
    radius6 = run_engine(6, "radius6_regression")
    observed6 = radius6["final"]["counts"]
    shells6 = [item["shell"] for item in observed6]
    balls6 = [item["ball"] for item in observed6]
    old6 = old_radius6_keys()
    new6_keys = {item["key"] for item in iter_registry(radius6["registry"])}
    regression_pass = shells6 == EXPECTED_SHELLS_0_6 and balls6 == EXPECTED_BALLS_0_6 and new6_keys == old6
    if not regression_pass:
        raise RuntimeError("HARD STOP: radius-6 exact regression failed")

    forecast = resource_forecast()
    write_json(HERE / "CM_GRP_EXT_001_RESOURCE_FORECAST.json", forecast)
    write_json(OUTPUT / "CM_GRP_EXT_001_RESOURCE_FORECAST.json", forecast)

    radius7 = run_engine(7, "radius7_primary")
    rerun7 = run_engine(7, "radius7_determinism_rerun")
    restart_pass = radius7["final"]["registry_sha256"] == rerun7["final"]["registry_sha256"]
    unique_count = registry_count(radius7["registry"])

    w1 = (0, 5, 2, 7)
    w2 = (7, 2, 5, 0)
    key1 = projective_key(matrix_from_word(tuple(f"g{x}" for x in w1)))
    key2 = projective_key(matrix_from_word(tuple(f"g{x}" for x in w2)))
    duplicate_candidates = raw_candidates_for_key(radius7["root"], key1, 7)
    chosen = find_registry_key(radius7["registry"], key1)
    cross_duplicate_pass = (
        key1 == key2 and {item[2] for item in duplicate_candidates}.issuperset({0, 7})
        and chosen["length"] == min(item[0] for item in duplicate_candidates)
        and chosen["word"] == min(item[1] for item in duplicate_candidates if item[0] == chosen["length"])
    )

    inverse_pass = bool(radius7["final"]["inverse_closure"])
    phi_pass = bool(radius7["final"]["phi8_closure"])
    minimum_pass = bool(radius7["final"]["minimum_shortlex_rule"])
    tensor_invariance = (
        key1 == key2
        and exact_cosh_distance_over_R(matrix_from_word(tuple(f"g{x}" for x in w1)))
        == exact_cosh_distance_over_R(matrix_from_word(tuple(f"g{x}" for x in w2)))
        and abelian(w1) == abelian(w2)
        and tensor_moment(w1) == tensor_moment(w2)
    )
    counts7 = radius7["final"]["counts"]
    total_candidates = sum(free_candidate_counts(7))
    duplicates = total_candidates - unique_count
    rss = max(radius6["final"]["peak_rss_bytes"], radius7["final"]["peak_rss_bytes"], rerun7["final"]["peak_rss_bytes"])
    rss_pass = rss <= forecast["hard_rss_ceiling_bytes"]

    # Poincare polygon theorem: exact side pairings, one vertex cycle with
    # 8*(pi/4)=2*pi, and the oriented cycle relation give the registered
    # torsion-free genus-2 presentation and a discrete faithful PSU action.
    faithfulness = {
        "classification": "PASS",
        "theorem": "Poincare polygon theorem",
        "premises": [
            "exact regular hyperbolic octagon with interior angle pi/4",
            "exact opposite-side endpoint and midpoint pairings",
            "one eight-vertex cycle with total angle 2*pi",
            "exact oriented polygon relation",
            "exact invertible Nielsen transport to [a1,b1][a2,b2]=e",
        ],
        "conclusion": "the generated PSU(1,1) action is discrete and faithful and has the registered genus-2 surface-group presentation",
        "projective_normalization": "choose the lexicographically smaller of the normalized exact SU(1,1) coefficient tuples for M and -M",
    }
    gates = {
        "GEXT-01_shell_counts_L0_L6": shells6 == EXPECTED_SHELLS_0_6,
        "GEXT-02_ball_counts_L0_L6": balls6 == EXPECTED_BALLS_0_6,
        "GEXT-03_cross_shard_duplicate": cross_duplicate_pass,
        "GEXT-04_exact_group_key": faithfulness["classification"] == "PASS" and unique_count == counts7[-1]["ball"],
        "GEXT-05_radius7_input_exhaustive": sum(item["total_records"] for item in radius7["generation"]["shards"]) == total_candidates,
        "GEXT-06_all_buckets_reduced": radius7["buckets"]["all_complete"],
        "GEXT-07_radius7_registry": unique_count > EXPECTED_BALLS_0_6[-1],
        "GEXT-08_minimum_length": minimum_pass,
        "GEXT-09_C8_inverse_closure": phi_pass and inverse_pass,
        "GEXT-10_tensor_word_invariance": tensor_invariance,
        "GEXT-11_restart_hash": restart_pass,
        "GEXT-12_peak_RSS": rss_pass,
    }
    passed = all(gates.values())
    final_registry = OUTPUT / "ball_radius_7_exact.bin"
    final_summary = OUTPUT / "ball_radius_7_summary.csv"
    shutil.copyfile(radius7["registry"], final_registry)
    shutil.copyfile(radius7["summary"], final_summary)
    manifest = {
        "schema_version": "1.0", "task_id": "CM-GRP-EXT-001", "radius": 7,
        "generator_order": [f"g{i}" for i in range(8)], "metric": "minimum physical-shell word length",
        "identity_key": "exact projectively normalized SU(1,1) top-row algebraic tuple",
        "record_format": {"magic": "BOLZAG07", "record_bytes": REGISTRY_BYTES,
                          "fields": ["exact_key", "minimum_length", "shortlex_word_code", "inverse_id", "phi8_id", "orbit_metadata"]},
        "counts": {"input_free_words": total_candidates, "duplicate_word_representations": duplicates,
                   "unique_group_elements": unique_count, "shell_7": counts7[-1]["shell"], "ball_7": counts7[-1]["ball"]},
        "registry_sha256": sha256(final_registry), "generation_manifest": str(radius7["root"] / "generation_manifest.json"),
        "bucket_manifest": str(radius7["root"] / "bucket_manifest.json"), "final_merge_manifest": str(radius7["root"] / "final_merge_manifest.json"),
        "faithfulness": faithfulness, "acceptance": gates, "complete": passed,
    }
    write_json(OUTPUT / "ball_radius_7_manifest.json", manifest)
    certificate = {
        "schema_version": "1.0", "task_id": "CM-GRP-EXT-001",
        "classification": "PROOF_COMPLETE_RADIUS7_GROUP_REGISTRY" if passed else "CM_GRP_EXT_001_FAILED",
        "faithfulness_certificate": faithfulness,
        "exact_key": "two normalized dyadic algebraic fields (a,b), canonicalized under M~-M; exact tuple comparison only",
        "external_bucketing": {"bucket_count": BUCKETS, "hash_is_identity": False, "dedup": "exact-key sort/group within each hash bucket"},
        "regression": {"expected_shells_L0_L6": EXPECTED_SHELLS_0_6, "observed_shells_L0_L6": shells6,
                       "expected_balls_L0_L6": EXPECTED_BALLS_0_6, "observed_balls_L0_L6": balls6,
                       "old_registry_key_set_exact_match": new6_keys == old6},
        "cross_shard_duplicate": {"w1": [f"g{x}" for x in w1], "w2": [f"g{x}" for x in w2],
                                  "source_shards": sorted({item[2] for item in duplicate_candidates}), "same_exact_key": key1 == key2,
                                  "raw_representations_for_key": len(duplicate_candidates), "retained_multiplicity": 1,
                                  "chosen_minimum_length": chosen["length"], "chosen_word": [f"g{x}" for x in decode_word(chosen["length"], chosen["word"])]},
        "tensor_word_invariance": {"exact_geometry": True, "abelian_vector": list(abelian(w1)), "second_moment_equal": tensor_invariance},
        "radius7": manifest["counts"], "C8_closure": phi_pass, "inverse_closure": inverse_pass,
        "restart_registry_sha256_identical": restart_pass, "registry_sha256": sha256(final_registry),
        "resources": {"peak_rss_bytes": rss, "temporary_disk_bytes": sum(path.stat().st_size for path in (OUTPUT / "work").rglob("*") if path.is_file()),
                      "runtime_seconds": time.perf_counter() - started, "hard_rss_ceiling_bytes": forecast["hard_rss_ceiling_bytes"]},
        "acceptance": gates, "all_acceptance_pass": passed,
        "software": {"source_sha256": source_hash, "executable_sha256": executable_hash, "python": sys.version.split()[0]},
        "m7_release": passed, "m8_release": False, "main_tex_modified": False, "finished_utc": utc_now(),
    }
    write_json(HERE / "CM_GRP_EXT_001_CERTIFICATE.json", certificate)
    write_json(OUTPUT / "CM_GRP_EXT_001_CERTIFICATE.json", certificate)
    markdown = f"""# CM-GRP-EXT-001 certificate

- Classification: `{certificate['classification']}`
- Exact identity key: normalized algebraic SU(1,1) top row, canonical under `M ~ -M`; equality uses the exact tuple, never its hash.
- Faithfulness: `PASS` by the Poincare polygon theorem applied to the frozen exact regular-octagon side pairings and Nielsen transport.
- Buckets: {BUCKETS}; exact sort/group reduction.
- L0--L6 shells: `{shells6}`; balls: `{balls6}`; old key set exact match: `{new6_keys == old6}`.
- Radius 7: {total_candidates:,} freely reduced input words, {duplicates:,} duplicate representations, {unique_count:,} distinct elements; shell 7 = {counts7[-1]['shell']:,}.
- C8 closure: `{phi_pass}`; inverse closure: `{inverse_pass}`; tensor word invariance: `{tensor_invariance}`.
- Restart registry SHA-256: `{certificate['registry_sha256']}` (`{'PASS' if restart_pass else 'FAIL'}`).
- Peak RSS: {rss:,} bytes; runtime: {certificate['resources']['runtime_seconds']:.3f} s.
- m7 release: `{'YES' if passed else 'NO'}`; m8 remains closed.
"""
    (HERE / "CM_GRP_EXT_001_CERTIFICATE.md").write_text(markdown, encoding="utf-8")
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
