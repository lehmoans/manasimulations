from ..config.config import load_config


class AutoFluent:

    def __init__(self, config, case_path=None, environment=None):
        if case_path is not None or environment is not None:
            config = {
                "case_path": case_path,
                "environment_type": environment or "local",
            }

        self.config = load_config(config)
        self.environment_type = self.config["environment"]["type"]
        self.environment = None
        self.session = None
        self.meshing = None
        self.solver = None
        self.mesh_result = None
        self.result = None

    def configure_environment(self):
        if self.environment_type == "mock":
            from ..environment.mock import MockEnvironment
            return MockEnvironment(self.config)

        if self.environment_type == "local":
            from ..environment.local import LocalEnvironment
            return LocalEnvironment(self.config)

        if self.environment_type == "m3":
            from ..environment.hpc import HpcEnvironment
            return HpcEnvironment(self.config)

        raise ValueError(f"Unknown environment: {self.environment_type}")

    def _configure_mesher(self):
        if self.environment_type == "mock":
            from ..meshing.mock import Mock_Mesher
            return Mock_Mesher
        from ..meshing.fluent import Fluent_Mesher
        return Fluent_Mesher

    def _configure_solver(self):
        if self.environment_type == "mock":
            from ..solver.mock import Mock_Solver
            return Mock_Solver
        from ..solver.fluent import Fluent_Solver
        return Fluent_Solver

    def run(self):
        self.environment = self.configure_environment()

        try:
            self.environment.check_environment()
            self.environment.prepare()

            meshing_enabled = self.config.get("meshing", {}).get("enabled", False)
            solver_enabled = self.config.get("solver", {}).get("enabled", True)

            if meshing_enabled:
                self.session = self.environment.launch_session(mode="meshing")
                self.meshing = self._configure_mesher()(
                    self.session,
                    self.config,
                )
                self.mesh_result = self.meshing.run()

            if solver_enabled:
                if self.session is None:
                    self.session = self.environment.launch_session(mode="solve")

                self.solver = self._configure_solver()(
                    self.session,
                    self.config.get("solver", {}),
                )
                self.result = self.solver.run()

            return self.result

        finally:
            self.environment.close()
            self.session = None
