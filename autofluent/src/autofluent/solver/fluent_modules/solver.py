from .post_process.post_process import Post_Process
from .setup.setup import Setup
from .solution.solution import Solution


class Solver:

    def __init__(self, session, config):
        self.fluent_setup = Setup()
        self.solution = Solution()
        self.run_post_process = Post_Process()

        self.config = config
        self.session = session

    def setup(self):
        setup_config = self.config.get("setup", self.config)

        self.fluent_setup.setup(self.session, setup_config)
        return True

    def setup_solution(self):
        solution_config = self.config.get("solution", {})
        self.solution.setup(self.session, solution_config)
        return True

    def solve(self):
        iter_count = (
            self.config.get("run_calc_settings", {})
            .get("iter_count", 0)
        )

        self.session.settings.solution.run_calculation.iterate(
            iter_count=iter_count
        )
        return {
            "status": "success",
            "iterations": iter_count,
        }

    def post_process(self):
        save_config = self.config.get("save", {})

        if save_config.get("enabled", False):
            self.run_post_process.setup(self.session, self.config)

        return True

    def save(self):
        save_config = self.config.get("save", {})
        file_name = save_config.get("name") or "autofluent_result.cas.h5"

        return self.session.settings.file.write_case_data(
            file_name=file_name
        )

    def run(self):
        self.setup()
        self.setup_solution()
        self.solve()
        self.post_process()
        return self.save()
