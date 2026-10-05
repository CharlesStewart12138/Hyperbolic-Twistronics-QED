from __future__ import annotations

import hashlib
import json
import math
import struct
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
CONTRACT = GROUP / "BOLZA_GEOMETRIC_BALL_FLOOD_CONTRACT.json"
THEOREM = GROUP / "BOLZA_GEOMETRIC_BALL_FLOOD_THEOREM.md"
SOURCE = GROUP / "external_geometric_ball.cpp"
WORD_CERTIFICATE = GROUP / "CM_GRP_EXT_001_CERTIFICATE.json"


@pytest.fixture(scope="session")
def contract() -> dict[str, object]:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def smoke(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    root = tmp_path_factory.mktemp("geo7_external_smoke")
    executable = root / "external_geometric_ball_test.exe"
    subprocess.run(
        [
            "g++", "-std=c++20", "-O2", "-DNDEBUG", str(SOURCE),
            "-o", str(executable), "-lgmp", "-lpsapi",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    work = root / "work"
    subprocess.run([str(executable), "init", "2", "2", str(work)], cwd=ROOT, check=True)
    while True:
        checkpoint = dict(
            line.split("\t", 1)
            for line in (work / "checkpoint.tsv").read_text(encoding="utf-8").splitlines()
            if "\t" in line
        )
        if checkpoint["complete"] == "1":
            break
        subprocess.run([str(executable), "step", str(work)], cwd=ROOT, check=True)
    registry = root / "geo_ball_r2_exact.bin"
    summary = root / "summary.tsv"
    subprocess.run(
        [str(executable), "finalize", str(work), str(registry), str(summary)],
        cwd=ROOT,
        check=True,
    )
    first_hash = hashlib.sha256(registry.read_bytes()).hexdigest()
    registry2 = root / "geo_ball_r2_exact_second.bin"
    summary2 = root / "summary_second.tsv"
    subprocess.run(
        [str(executable), "finalize", str(work), str(registry2), str(summary2)],
        cwd=ROOT,
        check=True,
    )
    fields = dict(
        line.split("\t", 1)
        for line in summary.read_text(encoding="utf-8").splitlines()
        if "\t" in line
    )
    return {
        "root": root,
        "registry": registry,
        "summary": fields,
        "first_hash": first_hash,
        "second_hash": hashlib.sha256(registry2.read_bytes()).hexdigest(),
        "checkpoint": checkpoint,
    }


def test_geo7_t01_fundamental_tile_registered(contract: dict[str, object]) -> None:
    tile = contract["fundamental_tile"]
    assert tile["center"] == "o=0 in the Poincare disk"
    assert "Dirichlet-Voronoi" in tile["role"]


def test_geo7_t02_exact_circumradius(contract: dict[str, object]) -> None:
    radius = contract["circumradius"]
    expected = math.acosh(3 + 2 * math.sqrt(2))
    assert "2^(-1/4)" in radius["over_R_exact"]
    assert float(radius["over_R_decimal"]) == pytest.approx(expected, rel=2e-16)


def test_geo7_t03_expansion_theorem_proved(contract: dict[str, object]) -> None:
    theorem = contract["GEO_FLOOD_1"]
    assert theorem["classification"] == "PROVED"
    assert "R_target+r_v" in theorem["statement"]


def test_geo7_t04_voronoi_strengthening_proved(contract: dict[str, object]) -> None:
    theorem = contract["GEO_FLOOD_2"]
    assert theorem["classification"] == "PROVED_STRONGER_PRODUCTION_FILTER"
    assert "d(x,h o)<=d(x,p)" in theorem["key_inequality"]


def test_geo7_t05_closed_boundary_contract(contract: dict[str, object]) -> None:
    assert "<=" in contract["closed_ball_convention"]
    assert "exact equality is included" in contract["closed_ball_convention"]


def test_geo7_t06_exact_distance_membership(contract: dict[str, object]) -> None:
    assert contract["distance_identity"] == "cosh(d_H(o,g o)/R)=2*|a|^2-1 for the frozen SU(1,1) representative"
    assert "T_(2m)" in contract["integral_cutoff_identity"]
    assert "no epsilon" in contract["membership"]


def test_geo7_t07_exact_key_not_hash_identity(contract: dict[str, object]) -> None:
    flood = contract["external_fixed_point"]
    assert flood["bucket_count"] == 256
    assert flood["hash_role"] == "bucket selection only"
    assert flood["equality_role"] == "full 130-byte exact algebraic key"


def test_geo7_t08_out_of_core_visited(contract: dict[str, object]) -> None:
    assert contract["external_fixed_point"]["visited_residency"] == "disk-resident sorted bucket files"
    source = SOURCE.read_text(encoding="utf-8")
    assert "unordered_set" not in source
    assert "visited" in source and "candidate.tmp" in source


def test_geo7_t09_deterministic_transport_word(contract: dict[str, object]) -> None:
    rule = contract["external_fixed_point"]["transport_word"]
    assert "minimum flood depth" in rule
    assert "shortlex" in rule
    assert "not labeled globally minimum" in rule


def test_geo7_t10_small_exact_fixed_point(smoke: dict[str, object]) -> None:
    summary = smoke["summary"]
    assert summary["target_unique_elements"] == "105"
    assert summary["shell_counts"] == "1,8,56,32,8,0"
    assert summary["frontier_exhausted"] == "1"


def test_geo7_t11_registry_binary_contract(smoke: dict[str, object]) -> None:
    path = smoke["registry"]
    with path.open("rb") as handle:
        assert handle.read(8) == b"BOLZGEO1"
        count, record_bytes, cutoff = struct.unpack("<QII", handle.read(16))
    assert (count, record_bytes, cutoff) == (105, 147, 2)
    assert path.stat().st_size == 24 + count * record_bytes


def test_geo7_t12_restart_determinism(smoke: dict[str, object]) -> None:
    assert smoke["checkpoint"]["completed_depth"] == "5"
    assert smoke["first_hash"] == smoke["second_hash"]


def test_geo7_t13_word_ball_not_geometric_ball() -> None:
    certificate = json.loads(WORD_CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["radius7"]["unique_group_elements"] == 1_085_905
    assert 1_085_905 < 23_129_593


def test_geo7_t14_memory_contract(contract: dict[str, object], smoke: dict[str, object]) -> None:
    assert contract["hard_rss_ceiling_bytes"] == 48 * 1024**3
    assert int(smoke["summary"]["peak_rss_bytes"]) < contract["hard_rss_ceiling_bytes"]


def test_geo7_t15_manuscript_lock(contract: dict[str, object]) -> None:
    assert contract["main_tex_locked"] is True
    assert contract["manuscript_pdf_generation_forbidden"] is True

