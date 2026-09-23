class FixedSimulationProfile:
    """
    First-generation fixed AutoFluent workflow.

    The order here is the contract for the initial simulation profile.
    Future profiles can extend or replace this sequence without changing
    AutoFluent's environment lifecycle.
    """

    name = "fixed"

    def run_meshing(self, mesher):
        mesher.initialise_workflow()
        mesher.load_geometry()
        mesher.setup()
        mesher.generate_mesh()
        mesher.check_mesh()
        return mesher.save_mesh()

    def run_solver(self, solver):
        solver.setup()
        solver.setup_solution()
        solver.solve()
        solver.post_process()
        output_path = solver.save()

        return {
            "result": {
                **solver.result,
                "workflow": solver.workflow,
            },
            "output": str(output_path),
        }
