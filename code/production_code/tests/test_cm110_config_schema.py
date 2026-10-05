"""CM-110 typed production-reference schema tests."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import yaml

from production_code.model_contract import ContractViolation
from production_code.pipeline.config_schema import load_production_reference

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "production_code/config/production_reference.yaml"


class ProductionConfigSchemaTests(unittest.TestCase):
    def test_schema_lists_every_pf_row_and_fragment(self):
        reference = load_production_reference(REFERENCE, require_ready=False)
        self.assertEqual(len(reference.records), 89)
        self.assertEqual(len(reference.config_files), 15)
        self.assertFalse(reference.ready_for_production)

    def test_incomplete_reference_fails_closed_for_execution(self):
        with self.assertRaisesRegex(ContractViolation, "not frozen"):
            load_production_reference(REFERENCE, require_ready=True)

    def test_missing_parameter_record_fails(self):
        payload = yaml.safe_load(REFERENCE.read_text(encoding="utf-8"))
        del payload["parameter_freeze"][payload["required_freeze_ids"][0]]
        with TemporaryDirectory(dir=ROOT) as directory:
            tmp = Path(directory)
            for name in payload["config_files"]:
                (tmp/name).write_text("schema_version: 1\n", encoding="utf-8")
            path = tmp/"production_reference.yaml"; path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ContractViolation, "must match"):
                load_production_reference(path, require_ready=False)


if __name__ == "__main__": unittest.main()

