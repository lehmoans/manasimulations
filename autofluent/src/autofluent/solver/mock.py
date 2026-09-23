import json

from .base import BaseSolver


class Mock_Solver(BaseSolver):

    def __init__(self, session, config):
        super().__init__(config)
        self.session = session
        self.result = None

    def setup(self):
        print("MOCK SETUP: passed")
        return True

    def solve(self):
        print("MOCK SOLVE: passed")

        self.result = {
            "status": "success",
            "environment": "mock",
            "session_mode": self.session.mode,
            "solution": {
                "iterations": self.config.get("run_calc_settings", {}).get(
                    "iter_count", 0
                ),
                "converged": True,
            },
        }

        return self.result

    def post_process(self):
        print("MOCK POST-PROCESS: passed")
        return True

    def save(self):
        output_path = self.session.output_path

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(self.result, file, indent=2)

        print(f"MOCK SAVE: {output_path}")
        return output_path

    def run(self):
        self.setup()
        self.solve()
        self.post_process()
        output_path = self.save()

        return {
            "result": self.result,
            "output": str(output_path),
        }
