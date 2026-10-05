"""CM-111 structured-output contract tests."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import numpy as np

from production_code.model_contract import ContractViolation
from production_code.pipeline.data_contract import DatasetMetadata, write_csv_dataset, write_json_dataset, write_npz_dataset

ROOT = Path(__file__).resolve().parents[2]


def metadata():
    return DatasetMetadata(run_id="CM111-test",run_type="production",model_version={"tex_sha256":"a"*64},parameters={"PF-X":1.0},quotient={"id":"not_applicable"},sector={"id":"all"},errors={"absolute":1e-12},units={"energy":"rad/s"},config_sha256="b"*64)


class StructuredDataContractTests(unittest.TestCase):
    def test_json_manifest_has_every_provenance_field(self):
        with TemporaryDirectory(dir=ROOT/"data/production") as directory:
            data_path, manifest_path = write_json_dataset({"x":[1,2]}, metadata(), Path(directory), ROOT)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertTrue(data_path.is_file())
            for key in ["model_version","parameters","quotient","sector","errors","units","config_sha256","data"]:
                self.assertIn(key, manifest)
            self.assertEqual(len(manifest["data"]["sha256"]), 64)

    def test_csv_and_npz_writers_emit_sidecars(self):
        with TemporaryDirectory(dir=ROOT/"data/production") as directory:
            csv_path, csv_meta = write_csv_dataset([{"x":1,"y":2},{"x":3,"y":4}], metadata(), Path(directory), ROOT)
            npz_path, npz_meta = write_npz_dataset({"x":np.arange(3)}, metadata(), Path(directory), ROOT)
            self.assertTrue(all(path.is_file() for path in [csv_path,csv_meta,npz_path,npz_meta]))

    def test_missing_error_metadata_is_fatal(self):
        with self.assertRaisesRegex(ContractViolation, "errors metadata"):
            DatasetMetadata(run_id="bad",run_type="production",model_version={"x":1},parameters={"x":1},quotient={"x":1},sector={"x":1},errors={},units={"x":1},config_sha256="a"*64)

    def test_cross_namespace_write_is_fatal(self):
        with self.assertRaisesRegex(ContractViolation, "data/production"):
            write_json_dataset({}, metadata(), ROOT/"data/validation", ROOT)


if __name__ == "__main__": unittest.main()

