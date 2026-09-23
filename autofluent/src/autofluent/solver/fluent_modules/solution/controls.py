class Controls:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        model = config.get("model")
        if model:
            self.set_model(model)
        return True

    def set_model(self, model):
        if model != "p-v":
            raise ValueError(f"Unsupported pressure-velocity coupling: {model}")
        self.session.settings.solution.methods.p_v_coupling.flow_scheme = "coupled"
        return True
