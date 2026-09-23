class FixedSimulationProfile:
    """
    Fixed first-generation AutoFluent workflow.

    The sequence is intentionally explicit so the current simulation
    profile is predictable. Additional profiles can be introduced later
    without changing AutoFluent's core lifecycle.
    """

    name = "fixed"

    def run_meshing(self, mesher):
        return mesher.run()

    def run_solver(self, solver):
        return solver.run()
