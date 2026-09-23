from pathlib import Path

from .base import BaseEnvironment
from .mock_session import MockSession


class MockEnvironment(BaseEnvironment):

    def __init__(self, config):
        super().__init__(config)
        self.session = None
        self.workdir = None

    def check_environment(self):
        print("MOCK ENVIRONMENT: check")
        return True

    def prepare(self):
        save_dir = self.config.get("save_dir", {}).get("path")

        if save_dir:
            self.workdir = Path(save_dir).resolve()
        else:
            self.workdir = Path.cwd() / "mock_run"

        self.workdir.mkdir(parents=True, exist_ok=True)
        print(f"MOCK ENVIRONMENT: prepare -> {self.workdir}")
        return True

    def launch_session(self, mode):
        print(f"MOCK ENVIRONMENT: launch session ({mode})")

        self.session = MockSession(mode=mode)

        return self.session

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
