from pathlib import Path

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
import ansys.fluent.core as pyfluent

from .base import BaseEnvironment


class LocalEnvironment(BaseEnvironment):

    def __init__(self, config):
        super().__init__(config)
        self.session = None
        self.workdir = None

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
                "Unable to detect a Fluent installation. "
                "Specify environment.local.fluent.root in environment.yaml."
            ) from exc

    def check_environment(self):
        return self.fluent_root().exists()

    def prepare(self):
        save_path = self.config.get("save_dir", {}).get("path")
        self.workdir = Path(save_path or Path.cwd() / "autofluent_run").resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)

    def launch_session(self, mode):
        fluent_config = self.environment_config.get("fluent", {})
        resources = self.environment_config.get("resources", {})

        self.session = pyfluent.launch_fluent(
            mode=mode,
            dimension=fluent_config.get("dimension", 3),
            precision=fluent_config.get("precision", "double"),
            processor_count=resources.get("cpus", 1),
            fluent_path=str(self.fluent_root()),
        )
        return self.session

    def close(self):
        if self.session is not None:
            self.session.exit()
            self.session = None
