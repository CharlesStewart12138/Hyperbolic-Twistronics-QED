from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_exact_radius_three_ball_and_lower_bound_certificate():
    ball = json.loads((ROOT / "data" / "production" / "quotient_separator" / "ball_3a_exact" / "based_enumeration_summary.json").read_text(encoding="utf-8"))
    cert = json.loads((ROOT / "production_code" / "group" / "BASED_QUOTIENT_SIZE_LOWER_BOUND.json").read_text(encoding="utf-8"))
    assert ball["complete"] is True
    assert ball["cutoff_displacement_over_a_B"] == 3
    assert ball["dangerous_nonidentity_elements"] == 2336
    assert ball["shell_counts_including_identity_at_depth_zero"] == [1, 8, 56, 392, 712, 704, 368, 80, 16, 0]
    assert ball["terminal_empty_shell_depth"] == 9
    assert cert["exact_radius_3_ball"]["elements_including_identity"] == 2337
    assert cert["theorem"]["raw_image_order_lower_bound"] == 2337
    assert cert["theorem"]["parity_adjusted_image_order_lower_bound"] == 2338
    assert cert["comparison"]["minimum_order_determined"] is False
    assert cert["comparison"]["finite_device_scalability_obstruction_proved"] is False
    assert cert["word_radius_127_156_used"] is False
    assert cert["global_scope_evaluated"] is False
