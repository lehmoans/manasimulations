from .base import Environment

import os
from pathlib import Path
import ansys.fluent.core as pyfluent

class Local_Environment(Environment):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.session = None
        self.workdir = None

    def prepare(self):
        pass
    
    def chdir_to_save_dir(self):
        """Prepare the local working directory and environment."""

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


    def run(self):
        """Prepare environment and launch Fluent."""

        self.prepare()
        return self.launch()

    def close(self):
        """Close the Fluent session."""

        if self.session is not None:
            self.session.exit()
            self.session = None
  