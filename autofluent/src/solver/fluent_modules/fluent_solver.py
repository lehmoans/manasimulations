# module import
from pathlib import Path
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization import set_config
import ansys.fluent.visualization.pyvista as pv

#utilities
from src.config.config import load_config,cleanup_config

# importing fluent classes
from .setup.fluent_setup import Fluent_Setup
from .solution.solution import Solution
from .post_process.post_process import Post_Process

class fluent_solver:
    def __init__(self,session, config):
        self.fluent_setup = Fluent_Setup
        self.solution = Solution()
        self.run_post_process= Post_Process()
        
        self.config = load_config(config)["solver"]
        self.session = session

    def setup(self):
        
        #setup
        self.fluent_setup.setup(self.session, self.config)
        self.solution.setup(self.session, self.config["solution"])
        return True

    def solve(self):
        self.session.settings.solution.run_calculation.iterate(iter_count= self.config["solver"]["run_calc_settings"]["iter_count"])
    
    def post_process(self):
        if self.config["save"]["enabled"]:
            self.run_post_process.setup(self.session, self.config)

    def save(self):
        self.session.settings.file.write_case_data(
        file_name=self.config["save"]["name"])

    def run(self):
        self.setup()
        self.solve()
        self.post_process()
        self.save()


        
    
        