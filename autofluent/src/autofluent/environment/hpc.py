import os
from pathlib import Path

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path

from .base import BaseEnvironment


class HpcEnvironment(BaseEnvironment):

    def __init__(self, config):
        super().__init__(config)
        self.session = None
        environment = config.get("environment", {})
        self.resources_config = environment.get("resources", {})
        self.scheduler_config = environment.get("scheduler", {})

    @property
    def environment_config(self):
        return self.config.get("environment", {})

    def fluent_root(self):
        root = self.environment_config.get("fluent", {}).get("root")
        if root:
            root = Path(root).expanduser().resolve()
            if not root.exists():
                raise RuntimeError(f"Configured Fluent root does not exist: {root}")
            return root

        try:
            exe = Path(get_fluent_exe_path()).resolve()
            return exe.parent.parent.parent
        except Exception as exc:
            raise RuntimeError(
                "Fluent could not be detected on the HPC system. "
                "Specify environment.m3.fluent.root in environment.yaml."
            ) from exc

    def check_slurm(self):
        if os.getenv("SLURM_JOB_ID") is None:
            raise RuntimeError("HpcEnvironment must be run inside a SLURM job.")

    def check_environment(self):
        self.check_slurm()
        self.fluent_root()
        return True

    def prepare(self):
        save_path = self.config.get("save_dir", {}).get("path")
        self.workdir = Path(save_path or Path.cwd() / "autofluent_run").resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)

    def launch_session(self, mode):
        fluent_config = self.environment_config.get("fluent", {})
        self.session = pyfluent.launch_fluent(
            mode=mode,
            dimension=fluent_config.get("dimension", 3),
            precision=fluent_config.get("precision", "double"),
            processor_count=self.get_cpus(),
            fluent_path=str(self.fluent_root()),
        )
        return self.session

    def close(self):
        if self.session is not None:
            self.session.exit()
            self.session = None

    def get_cpus(self):
        return self.resources_config.get("cpus", 1)

    def get_memory(self):
        return self.resources_config.get("memory", "4G")

    def get_partition(self):
        return self.scheduler_config.get("partition", "normal")

    def get_walltime(self):
        return self.scheduler_config.get("walltime", "01:00:00")
