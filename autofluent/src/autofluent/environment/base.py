from abc import ABC, abstractmethod

class BaseEnvironment(ABC):
    def __init__(self,config):
        self.config = config
    
    @abstractmethod
    def check_environment(self):
        raise NotImplementedError

    @abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abstractmethod
    def launch_session(self,mode):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError