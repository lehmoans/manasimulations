from .base import Mesher


class Mock_Mesher(Mesher):

    def __init__(self, session, config):
        super().__init__(session, config)
        self.mesh_path = None
        self.workflow = []

    def _record(self, stage):
        self.workflow.append(stage)
        print(f"MOCK MESH: {stage}")

    def initialise_workflow(self):
        self._record("initialise_workflow")
        return True

    def load_geometry(self):
        self._record("load_geometry")
        return True

    def setup(self):
        self._record("setup")
        return True

    def generate_mesh(self):
        self._record("generate_mesh")
        return True

    def check_mesh(self):
        self._record("check_mesh")
        return True

    def save_mesh(self):
        mesh_name = self.config.get("file") or "mock_mesh.msh"
        self.mesh_path = self.session.output_path.parent / mesh_name
        self.mesh_path.write_text(
            "MOCK MESH\nstatus: generated\n",
            encoding="utf-8",
        )
        self._record("save_mesh")
        print(f"MOCK MESH: artifact -> {self.mesh_path}")
        return self.mesh_path

    def run(self):
        self.initialise_workflow()
        self.load_geometry()
        self.setup()
        self.generate_mesh()
        self.check_mesh()
        return self.save_mesh()
