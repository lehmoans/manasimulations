from .base import BaseSolver
from .fluent_modules.solver import Solver


class Fluent_Solver(BaseSolver):

    def __init__(self, session, config):
        super().__init__(config=config)
        self.fluent_solver = Solver(session, config)
        self.result = None
        self.workflow = []

    def setup(self):
        self.fluent_solver.setup()
        self.workflow.append("setup")
        return True

    def setup_solution(self):
        self.fluent_solver.setup_solution()
        self.workflow.append("solution")
        return True

    def solve(self):
        self.result = self.fluent_solver.solve()
        self.workflow.append("solve")
        return self.result

    def post_process(self):
        self.fluent_solver.post_process()
        self.workflow.append("post_process")
        return True

    def save(self):
        output = self.fluent_solver.save()
        self.workflow.append("save")
        return output

    def run(self):
        self.setup()
        self.setup_solution()
        self.solve()
        self.post_process()
        return self.save()
