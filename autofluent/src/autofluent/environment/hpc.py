from .base import BaseEnvironment

import os
from pathlib import Path
import ansys.fluent.core as pyfluent


class HpcEnvironment(BaseEnvironment):

    def __init__(self, config):
        super().__init__(config)
        self.session = None
        self.resources_config = config.get("environment", {}).get(
            "resources", {}
        )

        self.scheduler_config = config.get("environment", {}).get(
            "scheduler", {}
        )

    def check_environment(self):
        if os.getenv("SLURM_JOB_ID") is None:
            raise RuntimeError(
                "M3Environment must be run inside a SLURM job."
            )
    
    def prepare(self):
        save_path = self.config["save_dir"]["path"]
        self.workdir = Path(save_path).resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)
        os.chdir(self.workdir)

    def launch_session(self,mode):
        self.check_slurm()
        self.session = pyfluent.launch_fluent(
            mode=mode,
            dimension=3,
            precision="double",
            processor_count=self.get_cpus(),
        )

        return self.session

    def close(self):

        if self.session is not None:
            self.session.exit()
            self.session = None
    
    #class utilities

    def get_cpus(self):
        return self.resources_config.get("cpus", 1)

    def get_memory(self):
        return self.resources_config.get("memory", "4G")

    def get_partition(self):
        return self.scheduler_config.get(
            "partition",
            "normal")

    def get_walltime(self):
        return self.scheduler_config.get(
            "walltime",
            "01:00:00"
        )
    
    