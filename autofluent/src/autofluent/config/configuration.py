from copy import deepcopy
from pathlib import Path

import yaml


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = PACKAGE_ROOT.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SAVED_CASE_CONFIGURATIONS_DIR = PROJECT_ROOT / "saved_case_configurations"


class CaseConfigurationManager:
    """Create, load, save, and discover reusable case configurations."""

    def __init__(
        self,
        case_path=None,
        saved_dir=None,
        config_dir=None,
    ):
        self.config_dir = Path(config_dir or CONFIG_DIR)
        self.case_path = Path(case_path or self.config_dir / "case.yaml")
        self.saved_dir = Path(
            saved_dir or PROJECT_ROOT / "saved_case_configurations"
        )

    def ensure_saved_directory(self):
        self.saved_dir.mkdir(parents=True, exist_ok=True)
        return self.saved_dir

    @staticmethod
    def _read(path):
        path = Path(path)
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @staticmethod
    def _write(path, data):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                sort_keys=False,
                default_flow_style=False,
                allow_unicode=True,
            )

    def load_current(self):
        return self._read(self.case_path)

    def load_saved(self, name):
        path = self.saved_path(name)
        if not path.exists():
            raise FileNotFoundError(
                f"Saved case configuration not found: {name}"
            )
        return self._read(path)

    def save_current(self, data):
        self._write(self.case_path, deepcopy(data))
        return self.case_path

    def save_as(self, data, name, overwrite=False):
        path = self.saved_path(name)
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"Saved case configuration already exists: {path.name}"
            )
        self._write(path, deepcopy(data))
        return path

    def saved_path(self, name):
        safe_name = Path(str(name)).name
        if safe_name.endswith(".yaml"):
            filename = safe_name
        else:
            filename = f"{safe_name}.yaml"

        if filename in {".yaml", ""}:
            raise ValueError("A non-empty case configuration name is required.")

        return self.saved_dir / filename

    def list_saved(self):
        self.ensure_saved_directory()
        return sorted(
            path.stem
            for path in self.saved_dir.glob("*.yaml")
            if path.is_file()
        )

    def resolve_case(self, case):
        """Resolve a case argument to a YAML path.

        Supported values:
        - None: current config/case.yaml
        - an existing YAML path
        - a saved configuration name
        """
        if case is None:
            return self.case_path

        path = Path(case)
        if path.exists():
            return path

        saved = self.saved_path(str(case))
        if saved.exists():
            return saved

        raise FileNotFoundError(
            f"Case configuration could not be resolved: {case}"
        )
