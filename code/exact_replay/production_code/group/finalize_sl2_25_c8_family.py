"""Finalize the exact SL(2,25) x C2 lifted semilinear-C8 family audit."""

from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from production_code.group.injectivity_bridge import _geometry_from_matrix
from production_code.group.psl2_25_c8_orbits import alpha_centralizer
from production_code.group.sl2_25_c8_family import (
    IDENTITY,
    PHYSICAL_RELATOR,
    alpha_power,
    b3_injective,
    candidate_seeds,
    centralizer_orbits,
    generated_subgroup,
    matinv,
    physical_images,
    sl_elements,
    word_image,
)
from production_code.group.universal_cover import matrix_from_word


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
BALL = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"
OUT_JSON = GROUP / "SL2_25_C8_FAMILY_CERTIFICATE.json"
OUT_MD = GROUP / "SL2_25_C8_FAMILY_CERTIFICATE.md"

REPRESENTATIVES = (
    (0, 6, 13, 22), (0, 7, 8, 22), (0, 23, 22, 8), (0, 24, 17, 8),
    (1, 7, 9, 7), (1, 10, 14, 18), (1, 16, 13, 7), (1, 17, 1, 18),
    (1, 18, 12, 10), (1, 22, 19, 10), (2, 6, 6, 5), (2, 9, 9, 20),
    (6, 6, 1, 18), (6, 10, 8, 18), (8, 10, 11, 18), (8, 12, 1, 18),
)
WITNESSES = (
    (0,0,1,4,6,1,4,5), (0,0,3,4,7,2,4,7),
    (0,0,3,4,7,2,4,7), (0,0,1,4,6,1,4,5),
    (0,2,0,3,0,5,0,3), (0,1,0,3,2,7,4,5),
    (0,2,4,6,1,6,4,2), (0,1,3,0,3,1,0,3),
    (0,1,0,3,2,7,4,5), (0,1,3,0,3,1,0,3),
    (0,2,4,6,1,6,4,2), (0,2,0,3,0,5,0,3),
    (0,2,0,3,4,6,4,7), (0,2,3,6,4,6,7,2),
    (0,2,0,3,4,6,4,7), (0,2,3,6,4,6,7,2),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def b3_words() -> tuple[tuple[int, ...], ...]:
    result = []
    with gzip.open(BALL, "rt", encoding="utf-8") as stream:
        for record in map(json.loads, stream):
            if int(record["minimum_geometric_word_length"]) <= 3:
                result.append(tuple(int(token[1:]) for token in record["representative"]))
    return tuple(result)


def exact_short_witness(seed: tuple[int, ...], word: tuple[int, ...]) -> dict[str, object]:
    if word_image(physical_images(seed), word) != IDENTITY:
        raise RuntimeError("declared word is not in the lifted quotient kernel")
    matrix = matrix_from_word(tuple(f"g{digit}" for digit in word))
    based, translation, cosh_exact, half_trace = _geometry_from_matrix(matrix)
    if half_trace[0] != 0 or any(half_trace[index] for index in range(3, 9)):
        raise RuntimeError("unexpected witness trace field shape")
    p, q = int(half_trace[1]), int(half_trace[2])
    if p == 0 or p * q < 0:
        raise RuntimeError("unexpected mixed-sign half trace")
    abs_p, abs_q = abs(p), abs(q)
    if not (abs_p < 2405 and abs_q < 1700 and translation < 6.0):
        raise RuntimeError("witness does not pass the exact strict 6a comparison")
    return {
        "seed_representative": list(seed),
        "geometric_word": [f"g{digit}" for digit in word],
        "geometric_word_length": len(word),
        "quotient_image": list(IDENTITY),
        "nonidentity_in_surface_group": True,
        "half_trace_exact": {"basis": "1,sqrt(2)", "coefficients": [p, q]},
        "absolute_half_trace_coefficients": [abs_p, abs_q],
        "strict_exact_comparison": f"{abs_p}+{abs_q}sqrt(2) < 2405+1700sqrt(2)=cosh(3a_B/R)",
        "based_displacement_over_a_B": based,
        "translation_length_over_a_B": translation,
        "dangerous_strictly_below_6a_B": True,
        "cosh_based_displacement_exact_field": list(cosh_exact),
    }


def main() -> None:
    words = b3_words()
    sl = sl_elements()
    if len(words) != 457 or len(sl) != 15600:
        raise RuntimeError("fixture/group order drift")
    if not all(alpha_power(element, 8) == element for element in sl):
        raise RuntimeError("lifted alpha^8 is not identity")
    if any(all(alpha_power(element, divisor) == element for element in sl) for divisor in (1, 2, 4)):
        raise RuntimeError("lifted alpha lacks exact order eight")
    seeds = candidate_seeds(words)
    if len(seeds) != 128:
        raise RuntimeError("lifted B3 candidate count drift")
    if not all(len(generated_subgroup(seed)) == 15600 for seed in seeds):
        raise RuntimeError("a retained seed fails SL surjectivity")
    if not all(b3_injective(seed, words) for seed in seeds):
        raise RuntimeError("a retained seed fails B3 injectivity")
    if not all(word_image(physical_images(seed), PHYSICAL_RELATOR) == IDENTITY for seed in seeds):
        raise RuntimeError("surface relation drift")
    if not all(
        all(physical_images(seed)[j + 4] == matinv(physical_images(seed)[j]) for j in range(4))
        for seed in seeds
    ):
        raise RuntimeError("inverse shell drift")
    orbits = centralizer_orbits(seeds)
    if len(alpha_centralizer()) != 8 or len(orbits) != 16 or any(len(orbit) != 8 for orbit in orbits):
        raise RuntimeError("lifted centralizer orbit drift")
    if tuple(orbit[0] for orbit in orbits) != REPRESENTATIVES:
        raise RuntimeError("lifted orbit representative drift")
    witnesses = [exact_short_witness(seed, word) for seed, word in zip(REPRESENTATIVES, WITNESSES, strict=True)]
    candidate_hash = hashlib.sha256(json.dumps(seeds, separators=(",", ":")).encode("ascii")).hexdigest()
    record = {
        "schema_version": "1.0",
        "family_task_id": "PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3-SL2-25-LIFTED",
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "classification": "PROOF_COMPLETE_LIFTED_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR",
        "construction": {
            "field": "F25=F5[u]/(u^2-3)",
            "quotient": "SL(2,25) x C2_parity",
            "order": 31200,
            "SL_order": 15600,
            "semilinear_automorphism": "alpha(M)=A sigma(M) A^-1, A=(0,1;u,u), sigma(x)=x^5",
            "alpha_exact_order": 8,
            "physical_generator_images": "q(g_j)=(alpha^j(B),1)",
            "inverse_shell": True,
            "bipartite": True,
            "surjectivity_argument": "The matrix images generate perfect SL(2,25). Since SL has no nontrivial homomorphism to C2 and the physical images are odd, their subgroup in SL x C2 is the full direct product.",
        },
        "proof_complete_parameterization": {
            "all_SL_elements_enumerated": 15600,
            "relation_inverse_shell_eight_direction_and_exact_B3_seeds": len(seeds),
            "exact_B3_elements": len(words),
            "all_candidates_generate_SL": True,
            "candidate_seed_list_sha256": candidate_hash,
            "alpha_centralizer_in_PGammaL_order": len(alpha_centralizer()),
            "kernel_equivalence_orbits": len(orbits),
            "orbit_sizes": [len(orbit) for orbit in orbits],
            "kernel_equivalence_reason": "Commuting semilinear automorphisms transport every physical-word image, so all eight seeds in an orbit have exactly the same kernel.",
        },
        "global_rejection": {
            "method": "one exact length-eight kernel witness per kernel-equivalence orbit",
            "full_axis_registry_scan_required": False,
            "all_sixteen_orbits_rejected": True,
            "witnesses": witnesses,
        },
        "scope": "This is an exhaustive no-go for the lifted SL(2,25) x C2 family with the fixed Frobenius-semilinear alpha. It is not a no-go for other groups or automorphism classes.",
        "provenance": {
            "family_code_sha256": sha256(GROUP / "sl2_25_c8_family.py"),
            "universal_ball_fixture_sha256": sha256(BALL),
        },
    }
    OUT_JSON.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    values = [item["translation_length_over_a_B"] for item in witnesses]
    OUT_MD.write_text(
        """# Exact SL(2,25) x C2 lifted semilinear-C8 family audit

Classification: `PROOF_COMPLETE_LIFTED_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR`.

Exhaustive enumeration of all 15,600 SL(2,25) seed matrices leaves 128 seeds
after the frozen relation, inverse-shell, direction, generation and exact B3
gates. The order-eight semilinear centralizer divides these into sixteen
kernel-equivalence orbits of size eight.

Each orbit has an explicit nonidentity length-eight kernel word. Independent
exact Bolza SU(1,1) evaluation puts all sixteen translation lengths strictly
below 6 a_B (range %.12f--%.12f a_B), decisively rejecting the family without
using based displacement as a proxy and without requiring a full registry
scan.
""" % (min(values), max(values)),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

