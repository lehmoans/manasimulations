from .base import Mesher


class Mock_Mesher(Mesher):

    def __init__(self, session, config):
        super().__init__(session, config)

    def initialise_workflow(self):
        print("MOCK: workflow initialized")
        return True

    def load_geometry(self):
        print("MOCK: geometry loaded")
        return True

    def setup(self):
        print("MOCK: setup complete")
        return True

    def generate_mesh(self):
        print("MOCK: mesh generated")
        return True

    def check_mesh(self):
        print("MOCK: mesh checked")
        return True

    def save_mesh(self):
        print("MOCK: mesh saved")
        return True

    def run(self):
        self.initialise_workflow()
        self.load_geometry()
        self.setup()
        self.generate_mesh()
        self.check_mesh()
        self.save_mesh()
        return True
