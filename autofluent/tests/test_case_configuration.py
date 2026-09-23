import tempfile
import unittest
from pathlib import Path

from autofluent.config.configuration import CaseConfigurationManager


class TestCaseConfigurationManager(unittest.TestCase):

    def test_save_and_load_saved_case_without_touching_current_case(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current = root / "case.yaml"
            saved = root / "saved_case_configurations"

            current.write_text(
                "solver:\n  enabled: true\n",
                encoding="utf-8",
            )

            manager = CaseConfigurationManager(
                case_path=current,
                saved_dir=saved,
            )

            data = {
                "geometry": {"file": "pump.scdC"},
                "solver": {"enabled": True, "iterations": 500},
            }

            path = manager.save_as(data, "pump_fsi")

            self.assertTrue(path.exists())
            self.assertEqual(manager.list_saved(), ["pump_fsi"])
            self.assertEqual(manager.load_saved("pump_fsi"), data)
            self.assertEqual(
                current.read_text(encoding="utf-8"),
                "solver:\n  enabled: true\n",
            )

    def test_saved_name_resolves_to_yaml(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manager = CaseConfigurationManager(
                case_path=root / "case.yaml",
                saved_dir=root / "saved_case_configurations",
            )
            manager.save_as({"solver": {"enabled": True}}, "test_case")

            self.assertEqual(
                manager.resolve_case("test_case"),
                root / "saved_case_configurations" / "test_case.yaml",
            )


if __name__ == "__main__":
    unittest.main()
