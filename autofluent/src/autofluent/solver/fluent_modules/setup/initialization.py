class Initialisation:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        init_type = config.get("type")
        if init_type:
            self.set_initialize({"type": init_type})
        return True

    def set_initialize(self, sub_config):
        init_type = sub_config["type"]
        self.session.settings.solution.initialization.initialization_type = init_type
        if init_type == "standard":
            self.session.settings.solution.initialization.standard_initialize()
        elif init_type == "hybrid":
            self.session.settings.solution.initialization.hybrid_initialize()
        else:
            raise ValueError(f"Unsupported initialization type: {init_type}")
        return True
