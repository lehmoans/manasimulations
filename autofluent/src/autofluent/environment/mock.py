from .base import BaseEnvironment
from .mock_session import MockSession

class MockEnvironment(BaseEnvironment):

    def __init__(self, config):
        super().__init__(config)
        self.session = None

    def check_environment(self):
        print("MOCK ENVIRONMENT: check")

    def prepare(self):
        print("MOCK ENVIRONMENT: prepare")

    def launch_session(self, mode):
        print(f"MOCK ENVIRONMENT: launch session ({mode})")

        self.session = MockSession()

        return self.session

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None