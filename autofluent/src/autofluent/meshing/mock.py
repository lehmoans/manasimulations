from .base import Mesher


class Mock_Mesher(Mesher):

    def __init__(self, session, config):
        super().__init__(session, config)
        self.mesh_path = None

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
        mesh_name = self.config.get("file") or "mock_mesh.msh"
        self.mesh_path = self.session.output_path.parent / mesh_name
        self.mesh_path.write_text(
            "MOCK MESH\nstatus: generated\n",
            encoding="utf-8",
        )
        print(f"MOCK: mesh saved -> {self.mesh_path}")
        return self.mesh_path

    def run(self):
        self.initialise_workflow()
        self.load_geometry()
        self.setup()
        self.generate_mesh()
        self.check_mesh()
        return self.save_mesh()
