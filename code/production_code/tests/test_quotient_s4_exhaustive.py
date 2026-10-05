from production_code.group.quotient_s4_exhaustive import interface_counts


def test_s4_core_interface_is_exhausted_up_to_inner_automorphism() -> None:
    counts = interface_counts()
    assert counts["canonical_relation_solutions"] == 1851
    assert counts["epimorphism_orbits"] == 900
    assert counts["Q04_pass"] == 780
    assert counts["Q11_pass"] == 0

