"""CM-112 deterministic run-manager tests."""
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
import yaml

from production_code.model_contract import ContractViolation
from production_code.pipeline.run_manager import ComputeStage, initialize_run, mark_stage_complete

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT/"production_code/config/production_reference.yaml"


def ready_workspace(directory: Path) -> Path:
    config_dir=directory/"config"; config_dir.mkdir(parents=True)
    payload=yaml.safe_load(REFERENCE.read_text(encoding="utf-8"))
    for name in payload["config_files"]:
        shutil.copy2(ROOT/"production_code/config"/name, config_dir/name)
    payload["freeze_status"]="frozen"; payload["ready_for_production"]=True
    for freeze_id, record in payload["parameter_freeze"].items():
        record["status"]="Fixed"; record["value_ref"] = record["value_ref"] or f"user://{freeze_id}"; record["units"] = record["units"] or "declared"
    path=config_dir/"production_reference.yaml"; path.write_text(yaml.safe_dump(payload,sort_keys=False),encoding="utf-8")
    return path


class RunManagerTests(unittest.TestCase):
    def test_current_incomplete_reference_cannot_start(self):
        with self.assertRaisesRegex(ContractViolation,"not frozen"):
            initialize_run(REFERENCE,ROOT,"blocked-real-run",(ComputeStage("compute","production_code.core:compute"),))

    def test_same_run_and_config_resume_deterministically(self):
        with TemporaryDirectory(dir=ROOT) as name:
            workspace=Path(name); reference=ready_workspace(workspace)
            stages=(ComputeStage("geometry","production_code.geometry.bolza:constants"),ComputeStage("spectrum","production_code.spectral:compute",("geometry",)))
            first=initialize_run(reference,workspace,"RUN-test",stages)
            resumed=initialize_run(reference,workspace,"RUN-test",stages)
            self.assertEqual(first.config_sha256,resumed.config_sha256)
            self.assertEqual(first.state_path,resumed.state_path)
            completed=mark_stage_complete(first.state_path,"geometry",{"geometry.json":"a"*64})
            self.assertEqual(completed.statuses["geometry"],"done")

    def test_run_id_cannot_change_config(self):
        with TemporaryDirectory(dir=ROOT) as name:
            workspace=Path(name); reference=ready_workspace(workspace)
            stages=(ComputeStage("compute","production_code.core:compute"),)
            initialize_run(reference,workspace,"RUN-fixed",stages)
            payload=yaml.safe_load(reference.read_text(encoding="utf-8")); payload["authority"]="changed"; reference.write_text(yaml.safe_dump(payload,sort_keys=False),encoding="utf-8")
            with self.assertRaisesRegex(ContractViolation,"different configuration"):
                initialize_run(reference,workspace,"RUN-fixed",stages)

    def test_plot_entrypoint_is_rejected(self):
        with self.assertRaisesRegex(ContractViolation,"plot/figure/render"):
            ComputeStage("bad","production_code.plotting:plot_bands")


if __name__ == "__main__": unittest.main()

