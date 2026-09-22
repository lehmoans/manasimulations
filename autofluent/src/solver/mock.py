from .base import Solver


class Mock_Solver(Solver):

    def __init__(self, config):
        super().__init__(config)

    def setup(self):
        print(" MOCK SETUP: passed ")

    def solve(self):
        print(" MOCK SOLVE: passed ")

    def post_process(self):
        print(" MOCK POST-PROCESS: passed ")

    def save(self):
        print(" MOCK SAVE: passed ")