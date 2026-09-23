from .base import BaseSolver


class Mock_Solver(BaseSolver):

    def __init__(self, session, config):
        super().__init__(config)
        self.session = session

    def setup(self):
        print("MOCK SETUP: passed")
        return True

    def solve(self):
        print("MOCK SOLVE: passed")
        return True

    def post_process(self):
        print("MOCK POST-PROCESS: passed")
        return True

    def save(self):
        print("MOCK SAVE: passed")
        return True

    def run(self):
        self.setup()
        self.solve()
        self.post_process()
        self.save()
        return True
