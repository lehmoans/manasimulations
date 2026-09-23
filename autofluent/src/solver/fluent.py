from .base import BaseSolver

from .fluent_modules.solver import Solver

class Fluent_Solver(BaseSolver):

    def __init__(self, session, config):
        super().__init__(config=config)

        self.fluent_solver = Solver(session, config)
        
    def setup(self):
        self.setup = self.fluent_solver.setup()

    def solve(self):
        self.solve = self.fluent_solver.solve()

    def post_process(self):
        self.post_process = self.fluent_solver.post_process()
    
    def save(self):
        self.fluent_solver.save()
    
    def run(self):
        self.setup()
        self.solve()
        self.post_process()
        self.save()
    
        

   