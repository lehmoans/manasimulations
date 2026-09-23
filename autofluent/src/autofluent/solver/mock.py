import json

from .base import BaseSolver


class Mock_Solver(BaseSolver):

    def __init__(self, session, config):
        super().__init__(config)
        self.session = session
        self.result = None
        self.workflow = []

    def _record(self, stage):
        self.workflow.append(stage)
        print(f"MOCK SOLVER: {stage}")

    def setup_models(self):
        self._record("setup.models")

    def setup_materials(self):
        self._record("setup.materials")

    def setup_zones(self):
        self._record("setup.zones")

    def setup_reference_values(self):
        self._record("setup.reference_values")

    def setup_boundary_conditions(self):
        self._record("setup.boundary_conditions")

    def initialize(self):
        self._record("setup.initialization")

    def setup(self):
        self.setup_models()
        self.setup_materials()
        self.setup_zones()
        self.setup_reference_values()
        self.setup_boundary_conditions()
        self.initialize()
        return True

    def setup_solution_controls(self):
        self._record("solution.controls")

    def setup_solution_methods(self):
        self._record("solution.methods")

    def setup_monitors(self):
        self._record("solution.monitors")

    def setup_report_definitions(self):
        self._record("solution.report_definitions")

    def setup_solution(self):
        self.setup_solution_controls()
        self.setup_solution_methods()
        self.setup_monitors()
        self.setup_report_definitions()
        return True

    def solve(self):
        self._record("solve")

        iterations = (
            self.config.get("run_calc_settings", {})
            .get("iter_count", 0)
        )

        self.result = {
            "status": "success",
            "environment": "mock",
            "session_mode": self.session.mode,
            "solution": {
                "iterations": iterations,
                "converged": True,
            },
        }

        return self.result

    def post_process_iso_surfaces(self):
        self._record("post_process.iso_surface")

    def post_process_contours(self):
        self._record("post_process.contour")

    def post_process(self):
        self._record("post_process")

        post_process = self.config.get("post_process", {})

        if post_process.get("iso_surfaces"):
            self.post_process_iso_surfaces()

        if post_process.get("contours"):
            self.post_process_contours()

        return True

    def save(self):
        output_path = self.session.output_path

        payload = {
            **self.result,
            "workflow": self.workflow,
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

        print(f"MOCK SAVE: {output_path}")
        return output_path

    def run(self):
        self.setup()
        self.setup_solution()
        self.solve()
        self.post_process()
        output_path = self.save()

        return {
            "result": {
                **self.result,
                "workflow": self.workflow,
            },
            "output": str(output_path),
        }
