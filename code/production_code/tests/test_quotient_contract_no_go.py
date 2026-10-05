from production_code.group.automorphism import phi8, standard_s8_images
from production_code.group.quotient_contract_no_go import certificate


def test_exact_short_witness_is_outside_standard_s8() -> None:
    assert phi8(("b1",)) == ("a2_inv", "b1", "a1")
    assert standard_s8_images()["b1"] is None


def test_q09_q11_q12_contract_is_inconsistent() -> None:
    value = certificate()
    assert value.witness_word_length == 3
    assert value.minimum_ball_size == 457
    assert value.contradiction is True
    assert value.failure_class.startswith("F1")

