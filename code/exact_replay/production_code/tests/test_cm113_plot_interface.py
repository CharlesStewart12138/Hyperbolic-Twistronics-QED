"""CM-113 read-only plot-interface tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from production_code.model_contract import ContractViolation
from production_code.pipeline.data_contract import DatasetMetadata, write_json_dataset
from production_code.pipeline.plot_interface import load_plot_dataset, validate_plot_style

ROOT=Path(__file__).resolve().parents[2]


def metadata():
    return DatasetMetadata(run_id="CM113-test",run_type="production",model_version={"tex":"a"*64},parameters={"x":1},quotient={"id":"none"},sector={"id":"all"},errors={"abs":1e-12},units={"x":"dimensionless"},config_sha256="b"*64)


class PlotInterfaceTests(unittest.TestCase):
    def test_verified_json_is_loaded_without_compute(self):
        with TemporaryDirectory(dir=ROOT/"data/production") as directory:
            _, manifest=write_json_dataset({"x":[1,2,3]},metadata(),Path(directory),ROOT)
            loaded=load_plot_dataset(manifest)
            self.assertEqual(loaded.data,{"x":[1,2,3]})
            self.assertEqual(loaded.manifest["run_id"],"CM113-test")

    def test_tampered_data_is_rejected(self):
        with TemporaryDirectory(dir=ROOT/"data/production") as directory:
            data, manifest=write_json_dataset({"x":[1]},metadata(),Path(directory),ROOT)
            data.write_text('{"x":[2]}\n',encoding="utf-8")
            with self.assertRaisesRegex(ContractViolation,"hash mismatch"):
                load_plot_dataset(manifest)

    def test_physics_changing_style_is_rejected(self):
        with self.assertRaisesRegex(ContractViolation,"non-aesthetic"):
            validate_plot_style({"eta":0.1,"color":"black"})

    def test_aesthetic_style_is_immutable(self):
        style=validate_plot_style({"color":"black","linewidth":1.5,"panel_label":"a"})
        with self.assertRaises(TypeError): style["color"]="red"


if __name__ == "__main__": unittest.main()

