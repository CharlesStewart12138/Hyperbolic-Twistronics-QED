"""Named generator-shell registry for physical and presentation contracts."""

from __future__ import annotations

from production_code.group.geometric_shell_contract import (
    GEOMETRIC_INVERSE_INDEX,
    GEOMETRIC_TO_STANDARD_WORD,
)
from production_code.group.nielsen import standard_to_geometric
from production_code.group.surface_group import TOKENS as PRESENTATION_TOKENS


S8_GEOMETRIC = tuple(f"g{index}" for index in range(8))
S8_PRESENTATION = tuple(PRESENTATION_TOKENS)


def geometric_entry(index: int) -> dict[str, object]:
    index = int(index)
    if not 0 <= index < 8:
        raise ValueError("geometric shell index must lie in 0,...,7")
    standard_word = GEOMETRIC_TO_STANDARD_WORD[index]
    return {
        "id": f"g{index}",
        "nu": index,
        "exact_matrix": (
            ("1+sqrt(2)", f"sqrt(2+2*sqrt(2))*zeta8^{index}"),
            (f"sqrt(2+2*sqrt(2))*zeta8^(-{index})", "1+sqrt(2)"),
        ),
        "inverse": f"g{GEOMETRIC_INVERSE_INDEX[index]}",
        "standard_word": standard_word,
        "phi8_image": f"g{(index + 1) % 8}",
        "parity": len(standard_word) % 2,
        "use_in_physical_nearest_neighbour_hamiltonian": True,
        "presentation_letter_is_physical_nearest_neighbour": False,
        "presentation_word_length": len(standard_word),
        "geometric_word_length": 1,
    }


def presentation_entry(token: str) -> dict[str, object]:
    if token not in S8_PRESENTATION:
        raise ValueError(f"unknown presentation token: {token}")
    geometric_word = standard_to_geometric((token,))
    return {
        "id": token,
        "geometric_word": geometric_word,
        "parity": 1,
        "use_in_physical_nearest_neighbour_hamiltonian": False,
        "presentation_letter_is_physical_nearest_neighbour": token in {"a1", "a1_inv", "b1", "b1_inv"},
        "presentation_word_length": 1,
        "geometric_word_length": len(geometric_word),
    }


def registry() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "registry_id": "PF-GRP-001-SHELL-REGISTRY",
        "physical_shell_name": "S8_GEOMETRIC",
        "algebraic_shell_name": "S8_PRESENTATION",
        "S8_GEOMETRIC": tuple(geometric_entry(index) for index in range(8)),
        "S8_PRESENTATION": tuple(presentation_entry(token) for token in S8_PRESENTATION),
    }


def validate_registry() -> bool:
    payload = registry()
    geometric = payload["S8_GEOMETRIC"]
    presentation = payload["S8_PRESENTATION"]
    return all((
        S8_GEOMETRIC != S8_PRESENTATION,
        len(geometric) == len(presentation) == 8,
        all(entry["geometric_word_length"] == 1 for entry in geometric),
        all(entry["parity"] == 1 for entry in geometric),
        all(entry["use_in_physical_nearest_neighbour_hamiltonian"] for entry in geometric),
        not any(entry["use_in_physical_nearest_neighbour_hamiltonian"] for entry in presentation),
        all(geometric[GEOMETRIC_INVERSE_INDEX[index]]["inverse"] == f"g{index}"
            for index in range(8)),
    ))
