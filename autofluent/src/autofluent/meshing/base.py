from abc import ABC, abstractmethod


class Mesher(ABC):

    def __init__(self, session, config):
        self.config = config
        self.session = session

    @abstractmethod
    def initialise_workflow(self):
        raise NotImplementedError

    @abstractmethod
    def load_geometry(self):
        raise NotImplementedError

    @abstractmethod
    def setup(self):
        raise NotImplementedError

    @abstractmethod
    def generate_mesh(self):
        raise NotImplementedError

    @abstractmethod
    def check_mesh(self):
        raise NotImplementedError

    @abstractmethod
    def save_mesh(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
