class Methods():
    """
    Solver Settings
│      ├── Pressure-velocity coupling
│      ├── Spatial discretisation
│      ├── Gradient
│      └── Transient settings
    """
    def __init__(self) -> None:
        pass

    def setup(self,session, config):
        self.session = session
        self.config = config

        for name, value in config.items():

            if value in ("", None, 0):
                continue

            method = getattr(self, f"set_{name}", None)

            if method:
                method(session, value)

    def set_discretization(self, sub_config):
        if "pressure" in sub_config:
            self.session.tui.solve.set.discretization_scheme("pressure", 12)

        """
        below dependent on viscous model rather than what defined
        - below doesnt matter, all will have to be second order
        - will have to find specific commands to each viscous model such that 2nd discretization
            is conserved
        """
        if "k-epislon" in self.config["viscous_model"]["model"]: 
            self.session.tui.solve.set.discretization_scheme("k", sub_config["k"])
            self.session.tui.solve.set.discretization_scheme("epsilon", sub_config["epilson"])
        

        """
        # pythonic equivalent of 2nd order discretizations of above
        self.session.solution.methods.spatial_discretization.discretization_scheme["pressure"] = "second-order"
        self.session.solution.methods.spatial_discretization.discretization_scheme["k"] = "second-order-upwind"
        self.session.solution.methods.spatial_discretization.discretization_scheme["epsilon"] = "second-order-upwind"
        """

        """
        Further work:
        - implement as a class for each viscous model as well as different characteristic (velocity etc)
        """
        

