"""Cached execution wrapper for the immutable candidate-0003 verifier."""

from functools import lru_cache
import importlib


candidate = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0003")
candidate.selected_rows = lru_cache(maxsize=1)(candidate.selected_rows)
candidate.q_rotation = lru_cache(maxsize=1)(candidate.q_rotation)
verifier = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.verify_candidate_0003")


if __name__ == "__main__":
    verifier.main()
