"""PF-GOV-001 source-version freeze regression."""
import hashlib
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "production_code" / "config" / "model.yaml"


class ProductionSourceFreezeTests(unittest.TestCase):
    def test_frozen_sources_match_bytes_and_hashes(self):
        record = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["source_version"]
        for kind in ("tex", "pdf"):
            path = ROOT / record[f"{kind}_path"]
            payload = path.read_bytes()
            self.assertEqual(len(payload), record[f"{kind}_bytes"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), record[f"{kind}_sha256"])

    def test_pdf_is_declared_current_256_page_artifact(self):
        record = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["source_version"]
        self.assertEqual(record["pdf_pages"], 256)
        self.assertEqual(record["manuscript_role"], "authoritative_current_model")

    def test_non_git_state_is_explicit(self):
        record = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["source_version"]
        self.assertIsNone(record["repository_commit"])
        self.assertEqual(record["repository_state"], "not_a_git_repository")


if __name__ == "__main__":
    unittest.main()

