class Methods:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        discretization = config.get("discretization", {}) or {}
        if discretization:
            self.set_discretization(discretization)
        return True

    def set_discretization(self, sub_config):
        spatial = (
            self.session.settings.solution.methods
            .spatial_discretization.discretization_scheme
        )
        for field, value in sub_config.items():
            if value not in ("", None, 0):
                spatial[field] = value
        return True
