from abc import ABC, abstractmethod

#creating super class for meshing, will be updated according to mock or not
class Mesher(ABC):

    def __init__(self, session,config):
        self.config = config
        self.session = session

    @abstractmethod
    def initialise_workflow(self):
        raise NotImplemented

    @abstractmethod
    def load_geometry(self):
        raise NotImplemented

    @abstractmethod
    def setup(self):
        raise NotImplemented

    @abstractmethod
    def generate_mesh(self):
        raise NotImplemented

    @abstractmethod
    def check_mesh(self):
        raise NotImplemented

    @abstractmethod
    def save_mesh(self):
        raise NotImplemented
    
    @abstractmethod
    def run(self):
        raise NotImplemented

#setup config type hints
