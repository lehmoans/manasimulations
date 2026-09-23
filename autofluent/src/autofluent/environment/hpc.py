from .base import BaseEnvironment

import os
from pathlib import Path
import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path


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

    def check_slurm(self):
        if os.getenv("SLURM_JOB_ID") is None:
            raise RuntimeError(
                "HpcEnvironment must be run inside a SLURM job."
            )
    def check_fluent_access(self):
        
        try:
            fluent_exe = get_fluent_exe_path()
        except Exception as exc:
            raise RuntimeError(
                "Fluent could not be discovered on the HPC system."
            ) from exc
        
        if not fluent_exe.exists():
            raise RuntimeError(
                f"Fluent executable is not accessible: {fluent_exe}"
            )

        if not os.access(fluent_exe, os.X_OK):
            raise RuntimeError(
                f"Fluent executable is not executable: {fluent_exe}"
            )
    
    def check_environment(self):
        self.check_slurm()
        self.check_fluent_access()
    
    def prepare(self):
        save_path = self.config["save_dir"]["path"]
        self.workdir = Path(save_path).resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)
        os.chdir(self.workdir)

    def launch_session(self,mode):

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
    
    