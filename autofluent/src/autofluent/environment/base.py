from abc import ABC, abstractmethod

class BaseEnvironment(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def check_environment(self):
        """
        Mock
        └── no Fluent required

        Local
        ├── Python
        ├── PyFluent
        └── Fluent installation

        M3
        ├── SLURM
        ├── Python
        ├── PyFluent
        └── Fluent available on M3
        """
        raise NotImplementedError

    @abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abstractmethod
    def launch_session(self, mode):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
