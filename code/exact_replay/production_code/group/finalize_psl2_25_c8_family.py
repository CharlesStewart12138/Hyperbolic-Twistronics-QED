"""Finalize the exact PSL(2,25) x C2 semilinear-C8 family audit."""

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
from production_code.group.psl2_25_c8_family import (
    IDENTITY,
    PHYSICAL_RELATOR,
    alpha_power,
    b3_injective,
    candidate_seeds,
    generated_subgroup,
    matinv,
    physical_images,
    psl_elements,
    word_image,
)
from production_code.group.psl2_25_c8_orbits import (
    alpha_centralizer,
    centralizer_orbits,
    pgl_elements,
)
from production_code.group.universal_cover import matrix_from_word


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
BALL = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"
OUT_JSON = GROUP / "PSL2_25_C8_FAMILY_CERTIFICATE.json"
OUT_MD = GROUP / "PSL2_25_C8_FAMILY_CERTIFICATE.md"

REPRESENTATIVES = (
    (0, 1, 19, 20),
    (0, 1, 23, 7),
    (1, 2, 6, 23),
    (1, 2, 20, 22),
    (1, 4, 10, 22),
    (1, 8, 21, 9),
)
WITNESSES = (
    (0, 0, 1, 4, 6, 1, 4, 5),
    (0, 0, 1, 6, 0, 5, 7, 2),
    (0, 1, 0, 3, 2, 7, 4, 5),
    (0, 2, 0, 5, 0, 2, 0, 5),
    (0, 2, 0, 3, 0, 5, 0, 3),
    (0, 1, 3, 0, 3, 1, 0, 3),
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
    images = physical_images(seed)
    if word_image(images, word) != IDENTITY:
        raise RuntimeError("declared word is not in the quotient kernel")
    matrix = matrix_from_word(tuple(f"g{digit}" for digit in word))
    based, translation, cosh_exact, half_trace = _geometry_from_matrix(matrix)
    # Here every half trace is the positive Q(sqrt(2)) integer p+q sqrt(2).
    if half_trace[0] != 0 or any(half_trace[index] for index in range(3, 9)):
        raise RuntimeError("unexpected witness trace field shape")
    p, q = int(half_trace[1]), int(half_trace[2])
    if p <= 0 or q < 0 or not (p < 2405 and q < 1700):
        raise RuntimeError("witness does not pass the exact strict 6a comparison")
    if not translation < 6.0:
        raise RuntimeError("numeric cross-check of exact 6a comparison failed")
    return {
        "seed_representative": list(seed),
        "geometric_word": [f"g{digit}" for digit in word],
        "geometric_word_length": len(word),
        "quotient_image": list(IDENTITY),
        "nonidentity_in_surface_group": True,
        "half_trace_exact": {
            "basis": "1,sqrt(2)",
            "coefficients": [p, q],
        },
        "strict_exact_comparison": f"{p}+{q}sqrt(2) < 2405+1700sqrt(2)=cosh(3a_B/R)",
        "based_displacement_over_a_B": based,
        "translation_length_over_a_B": translation,
        "dangerous_strictly_below_6a_B": True,
        "cosh_based_displacement_exact_field": list(cosh_exact),
    }


def main() -> None:
    words = b3_words()
    if len(words) != 457:
        raise RuntimeError("B3 fixture drift")
    psl = psl_elements()
    if len(psl) != 7800 or len(pgl_elements()) != 15600:
        raise RuntimeError("projective group order drift")
    if not all(alpha_power(element, 8) == element for element in psl):
        raise RuntimeError("alpha^8 is not the identity")
    if any(all(alpha_power(element, divisor) == element for element in psl) for divisor in (1, 2, 4)):
        raise RuntimeError("alpha does not have exact order eight")

    seeds = candidate_seeds(words)
    if len(seeds) != 48:
        raise RuntimeError("semilinear B3 candidate count drift")
    if not all(len(generated_subgroup(seed)) == 7800 for seed in seeds):
        raise RuntimeError("a candidate fails PSL surjectivity")
    if not all(b3_injective(seed, words) for seed in seeds):
        raise RuntimeError("a retained seed fails exact B3 injectivity")
    if not all(word_image(physical_images(seed), PHYSICAL_RELATOR) == IDENTITY for seed in seeds):
        raise RuntimeError("surface relation drift")
    if not all(
        all(physical_images(seed)[j + 4] == matinv(physical_images(seed)[j]) for j in range(4))
        for seed in seeds
    ):
        raise RuntimeError("inverse shell drift")

    centralizer = alpha_centralizer()
    orbits = centralizer_orbits(seeds)
    if len(centralizer) != 8 or len(orbits) != 6 or any(len(orbit) != 8 for orbit in orbits):
        raise RuntimeError("centralizer orbit reduction drift")
    if tuple(orbit[0] for orbit in orbits) != REPRESENTATIVES:
        raise RuntimeError("orbit representative drift")
    candidate_hash = hashlib.sha256(
        json.dumps(seeds, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    witnesses = [exact_short_witness(seed, word) for seed, word in zip(REPRESENTATIVES, WITNESSES, strict=True)]

    record = {
        "schema_version": "1.0",
        "family_task_id": "PF-GRP-001-C8-TRACTABLE-CONSTRUCTIVE-V3-PSL2-25-SEMILINEAR",
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "classification": "PROOF_COMPLETE_SEMILINEAR_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR",
        "construction": {
            "field": "F25=F5[u]/(u^2-3), encoded a+b*u as a+5b",
            "quotient": "PSL(2,25) x C2_parity",
            "order": 15600,
            "PSL_order": 7800,
            "projective_matrix_normalization": "first nonzero entry equals one",
            "semilinear_automorphism": "alpha(M)=A sigma(M) A^-1, A=(0,1;u,u), sigma(x)=x^5",
            "alpha_exact_order": 8,
            "physical_generator_images": "q(g_j)=(alpha^j(B),1)",
            "inverse_shell": True,
            "surface_relator": list(PHYSICAL_RELATOR),
            "bipartite": True,
            "surjectivity_argument": "The matrix images generate simple perfect PSL(2,25). A subgroup of PSL x C2 projecting onto PSL and containing odd generators cannot be the graph of the trivial (hence only) homomorphism PSL->C2, so it is the full direct product.",
        },
        "proof_complete_parameterization": {
            "all_PSL_projective_elements_enumerated": 7800,
            "relation_inverse_shell_eight_direction_and_exact_B3_seeds": len(seeds),
            "exact_B3_elements": len(words),
            "all_candidates_generate_PSL": True,
            "candidate_seed_list_sha256": candidate_hash,
            "alpha_centralizer_in_PGammaL_order": len(centralizer),
            "kernel_equivalence_orbits": len(orbits),
            "orbit_sizes": [len(orbit) for orbit in orbits],
            "kernel_equivalence_reason": "If beta commutes with alpha and B'=beta(B), then q_B'(w)=beta(q_B(w)) for every physical word w; therefore the kernels are identical word by word.",
        },
        "global_rejection": {
            "method": "one exact short-kernel witness per kernel-equivalence orbit",
            "full_axis_registry_scan_required": False,
            "reason": "An explicit nonidentity kernel element with exact translation length below 6a_B is already a decisive global rejection.",
            "all_six_orbits_rejected": True,
            "witnesses": witnesses,
        },
        "scope": "This is an exhaustive no-go for the fixed Frobenius-semilinear alpha class in PSL(2,25) x C2 after exact enumeration of all PSL seed images. It is not a no-go for other finite groups or other Aut(PSL(2,25)) order-eight classes.",
        "provenance": {
            "axis_registry_sha256_not_read": "1148bf89c1d3dddf3f26eda57f2385ce8e65cbc8ce8042546683f18bde235c5b",
            "family_code_sha256": sha256(GROUP / "psl2_25_c8_family.py"),
            "orbit_code_sha256": sha256(GROUP / "psl2_25_c8_orbits.py"),
            "universal_ball_fixture_sha256": sha256(BALL),
        },
    }
    OUT_JSON.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    minimum = min(item["translation_length_over_a_B"] for item in witnesses)
    maximum = max(item["translation_length_over_a_B"] for item in witnesses)
    OUT_MD.write_text(
        """# Exact PSL(2,25) x C2 semilinear-C8 family audit

Classification: `PROOF_COMPLETE_SEMILINEAR_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR`.

The complete 7,800-element PSL seed enumeration leaves 48 seeds after the
surface relation, inverse-shell, eight-direction and exact 457-element B3
gates. Every seed generates PSL(2,25), hence with the frozen odd parity the
quotient is PSL(2,25) x C2 of order 15,600. The order-eight semilinear
automorphism has centralizer order eight; its action splits the 48 seeds into
six orbits of size eight, and all seeds in an orbit define exactly the same
kernel.

One explicit length-eight kernel word was checked for each orbit using the
independent exact Bolza SU(1,1) engine. Their half traces lie strictly below
`cosh(3 a_B/R)=2405+1700 sqrt(2)`, so their translation lengths lie strictly
below `6 a_B`. The six values range from %.12f to %.12f a_B. Thus every one
of the 48 candidates fails the global systole gate. A 785,639,753-record scan
is unnecessary for this negative conclusion because each kernel already has
an exact disqualifying witness.

Scope is limited to this fixed Frobenius-semilinear automorphism class.
""" % (minimum, maximum),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

