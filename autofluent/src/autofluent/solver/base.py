from abc import ABC, abstractmethod


class BaseSolver(ABC):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def setup_solution(self):
        raise NotImplementedError

    @abstractmethod
    def solve(self):
        raise NotImplementedError

    @abstractmethod
    def post_process(self):
        raise NotImplementedError

    @abstractmethod
    def save(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
