from abc import ABC, abstractmethod

class Environment(ABC):

    @abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abstractmethod
    def launch(self,mode):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError