from ..config.config import load_config
from .profile import FixedSimulationProfile


class AutoFluent:

    def __init__(self, config):
        self.config = load_config(config)
        self.environment_type = self.config["environment"]["type"]
        self.profile = self._configure_profile()
        self.environment = None
        self.session = None
        self.meshing = None
        self.solver = None
        self.mesh_result = None
        self.result = None

    def _configure_profile(self):
        profile_name = self.config.get("profile", "fixed")

        if profile_name == "fixed":
            return FixedSimulationProfile()

        raise ValueError(f"Unknown simulation profile: {profile_name}")

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

        raise ValueError(
            f"Unknown environment: {self.environment_type}"
        )

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

            meshing_enabled = self.config.get("meshing", {}).get(
                "enabled", False
            )
            solver_enabled = self.config.get("solver", {}).get(
                "enabled", True
            )

            if meshing_enabled:
                self.session = self.environment.launch_session(mode="meshing")
                self.meshing = self._configure_mesher()(
                    self.session,
                    self.config.get("meshing", {}),
                )
                self.mesh_result = self.profile.run_meshing(self.meshing)

            if solver_enabled:
                if self.session is None:
                    self.session = self.environment.launch_session(mode="solve")

                self.solver = self._configure_solver()(
                    self.session,
                    self.config.get("solver", {}),
                )

                context = {
                    "profile": self.profile.name,
                    "environment": self.environment_type,
                }

                if self.mesh_result is not None:
                    context["meshing"] = {
                        "mesh": str(self.mesh_result),
                        "workflow": self.meshing.workflow,
                    }

                self.result = self.profile.run_solver(
                    self.solver,
                    context=context,
                )

            return self.result

        finally:
            self.environment.close()
            self.session = None
