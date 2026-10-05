"""No-go certificate for the frozen standard-S8 quotient contract.

Q-09 and Q-11 require the descended exact phi8 to preserve the standard-S8
regular adjacency multiset.  Q-12 requires injectivity on the exact group ball
B_S(e,3).  These requirements are mutually inconsistent because phi8(b1) is
a length-three element that is not any standard S8 element.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from production_code.group.automorphism import phi8, standard_s8_images
from production_code.group.quotient_candidate import S8_PRESENTATION


@dataclass(frozen=True)
class QuotientContractNoGo:
    witness_generator: str
    phi8_witness_word: tuple[str, ...]
    witness_word_length: int
    standard_shell: tuple[str, ...]
    exact_distinct_from_every_standard_shell_element: bool
    q09_q11_implication: str
    q12_implication: str
    contradiction: bool
    minimum_ball_size: int
    failure_class: str


def certificate() -> QuotientContractNoGo:
    witness = "b1"
    image = phi8((witness,))
    exact_matches = standard_s8_images()
    distinct = exact_matches[witness] is None
    return QuotientContractNoGo(
        witness_generator=witness,
        phi8_witness_word=image,
        witness_word_length=len(image),
        standard_shell=S8_PRESENTATION,
        exact_distinct_from_every_standard_shell_element=distinct,
        q09_q11_implication=(
            "If phi8 descends and conjugates the standard-S8 adjacency to itself, "
            "q(phi8(b1)) equals q(s) for at least one s in standard S8."
        ),
        q12_implication=(
            "Injectivity on B_S(e,3) makes q(phi8(b1)) distinct from q(s) for every "
            "s in standard S8 because both elements lie in B_S(e,3)."
        ),
        contradiction=distinct and len(image) <= 3,
        minimum_ball_size=457,
        failure_class="F1 source-interface / frozen-contract contradiction",
    )


def as_record() -> dict[str, object]:
    value = asdict(certificate())
    value["theorem"] = (
        "No quotient of Gamma_B can simultaneously satisfy Q-09 exact phi8 descent, "
        "Q-11 covariance of the standard S8 adjacency, and Q-12 injectivity on B_S(e,3)."
    )
    value["repair_options_not_applied"] = [
        "replace the standard S8 hopping shell by the exact geometric shell {g0,...,g7}, which phi8 cyclically permutes",
        "or remove/alter Q-11 while retaining the standard S8 shell",
    ]
    value["main_tex_modified"] = False
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(as_record(), indent=2))

