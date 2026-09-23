#utilities
from ..config.config import load_config

class AutoFluent():

    def __init__(self, config):
        self.config = load_config(config)
        self.environment_type = self.config["environment"]["type"]

    def configure_environment(self):

        if self.environment_type == "mock":
            from ..environment.mock import MockEnvironment
            return MockEnvironment(self.config)

        elif self.environment_type == "local":
            from ..environment.local import LocalEnvironment
            return LocalEnvironment(self.config)

        elif self.environment_type == "m3":
            from ..environment.hpc import HpcEnvironment
            return HpcEnvironment(self.config)

        else:
            raise ValueError(
                f"Unknown environment: {self.environment_type}"
            )

    def run(self):
        session = None
        
        # assign environment
        self.environment = self.configure_environment()
        
        #environment prep
        self.environment.check_environment()
        self.environment.prepare()
            
        #meshing
        if self.config["meshing"]["enabled"]:
            session = self.environment.launch_session(mode = "meshing")

            if self.environment_type == "mock":
                from ..meshing.mock import Mock_Mesher
                self.mesher_class = Mock_Mesher
            else:
                from ..meshing.fluent import Fluent_Mesher
                self.mesher_class = Fluent_Mesher

            self.meshing = self.mesher_class(session,self.config["meshing"])

            self.meshing.run()

        if self.config["solver"]["enabled"]:
            if not session:
                session = self.environment.launch_session(mode = "solve")
            
            if self.environment_type == "mock":
                from ..solver.mock import Mock_Solver
                self.solver_class = Mock_Solver
            else:
                from ..solver.fluent import Fluent_Solver
                self.solver_class = Fluent_Solver

            self.solver = self.solver_class(
            session,self.config["solver"])

            self.solver.run()
        
        if session:
            session.close()
    