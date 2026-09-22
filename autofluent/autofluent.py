#utilities
from .src.config.config import load_config
#environments
from .src.environment.local import Local_Environment
from .src.environment.hpc import HPC_Environment
from .src.environment.mock import Mock_Environment
#modules
from .src.meshing.mock import Mock_Mesher
from .src.meshing.fluent import Fluent_Mesher
from .src.solver.mock import Mock_Solver
from .src.solver.fluent import Fluent_Solver


class AutoFluent():
    def __init__(self,config):
        self.config = load_config(config)
    

    def configure_environment(self):

        self.environment_type = self.config["environment"]["type"]

        environments = {
            "local": Local_Environment,
            "hpc": HPC_Environment,
            "mock": Mock_Environment,}
        
        try:
            environment_class = environments[self.environment_type]
            
        except KeyError:
            raise ValueError(
                f"Unknown environment: {self.environment_type}"
            )

        return environment_class(self.config)

    def run(self):
        self.environment = self.configure_environment()
            
        #meshing
        if self.config["meshing"]["enabled"]:
            session = self.environment.launch_session(mode = "meshing")

            if self.environment_type == "mock":
                self.mesher_class = Mock_Mesher
            else:
                self.mesher_class = Fluent_Mesher

            self.meshing = self.mesher_class(
            session,
            self.config["meshing"])

            self.meshing.run()
            session.close()

        if self.config["solver"]["enabled"]:
            session = self.environment.launch_session(mode = "solve")
            if self.environment_type == "mock":
                self.solver_class = Mock_Solver
            else:
                self.solver_class = Fluent_Solver

            self.solver = self.solver_class(
            session,self.config["solver"])

            self.solver.run()
            session.close()
    

        
