from .base import BaseEnvironment

import os
from pathlib import Path
from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
import ansys.fluent.core as pyfluent

class LocalEnvironment(BaseEnvironment):
    def __init__(self, config):
        super().__init__(config)
        self.session = None
        self.workdir = None

    def check_environment(self):

        try:
            fluent_exe = get_fluent_exe_path()

        except Exception as exc:
            raise RuntimeError(
                "Unable to discover a Fluent installation."
            ) from exc

        if not fluent_exe.exists():
            raise RuntimeError(
                f"Fluent executable was not found: {fluent_exe}"
            )

        return True

    def prepare(self):
        save_path = self.config["save_dir"]["path"]

        self.workdir = Path(save_path).resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)

        os.chdir(self.workdir)

    def launch_session(self,mode):
        """Launch a local Fluent session."""

        fluent_config = self.config.get("fluent", {})
        resources = self.config.get("resources", {})

        dimension = fluent_config.get("dimension", 3)
        precision = fluent_config.get("precision", "double")
        processors = resources.get("cpus", 1)

        self.session = pyfluent.launch_fluent(
            mode=mode,
            dimension=dimension,
            precision=precision,
            processor_count=processors,
        )

        return self.session

    def close(self):
        """Close the Fluent session."""

        if self.session is not None:
            self.session.exit()
            self.session = None
  