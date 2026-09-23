from .base import BaseEnvironment

import os
from pathlib import Path
import ansys.fluent.core as pyfluent

class LocalEnvironment(BaseEnvironment):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.session = None
        self.workdir = None

    def check_environment(self):
        pass

    def prepare(self):
        pass

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
  