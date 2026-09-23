from abc import ABC, abstractmethod

#creating super class for meshing, will be updated according to mock or not
class BaseSolver(ABC):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def setup(self):
        raise NotImplemented

    @abstractmethod
    def solve(self):
        raise NotImplemented

    @abstractmethod
    def post_process(self):
        raise NotImplemented

    @abstractmethod
    def save(self):
        raise NotImplemented

   