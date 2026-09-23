import json
import tempfile
import unittest
from pathlib import Path

from autofluent import AutoFluent


class TestMockPipeline(unittest.TestCase):

    def test_mock_pipeline_produces_result(self):
        with tempfile.TemporaryDirectory(prefix="autofluent_test_") as run_dir:
            config = {
                "environment": {"type": "mock"},
                "save_dir": {"path": run_dir},
                "meshing": {
                    "enabled": True,
                    "file": "mock_mesh.msh",
                },
                "solver": {
                    "enabled": True,
                    "run_calc_settings": {"iter_count": 5},
                    "post_process": {
                        "iso_surface": [{"name": "x0"}],
                        "contour": [{"name": "velocity-mag"}],
                    },
                    "save": {"name": "mock_result.json"},
                },
            }

            result = AutoFluent(config).run()

            output_path = Path(result["output"])
            mesh_path = Path(run_dir) / "mock_mesh.msh"

            self.assertEqual(result["result"]["status"], "success")
            self.assertEqual(result["result"]["environment"], "mock")
            self.assertEqual(result["result"]["solution"]["iterations"], 5)

            self.assertEqual(
                result["result"]["workflow"],
                [
                    "setup.models",
                    "setup.materials",
                    "setup.zones",
                    "setup.reference_values",
                    "setup.boundary_conditions",
                    "setup.initialization",
                    "solution.controls",
                    "solution.methods",
                    "solution.monitors",
                    "solution.report_definitions",
                    "solve",
                    "post_process",
                    "post_process.iso_surface",
                    "post_process.contour",
                ],
            )

            self.assertTrue(output_path.exists())
            self.assertTrue(mesh_path.exists())

            saved_result = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(saved_result, result["result"])


if __name__ == "__main__":
    unittest.main()
