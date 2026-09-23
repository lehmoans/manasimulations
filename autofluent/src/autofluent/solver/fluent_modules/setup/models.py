class Models:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        for name, value in config.items():
            if value in ("", None, 0):
                continue
            method = getattr(self, f"set_{name}", None)
            if method:
                method(value)
        return True

    def set_viscous_model(self, sub_config):
        model_type = sub_config.get("model")
        if model_type == "k-epilson":
            model_type = "k-epsilon"
        if model_type != "k-epsilon":
            raise ValueError(f"Unsupported viscous model: {model_type}")

        self.session.settings.setup.models.viscous.model = model_type

        formulation = sub_config.get("formulation")
        if formulation is not None:
            self.session.settings.setup.models.viscous.k_epsilon_model = formulation

        if "curvature_correction" in sub_config:
            self.session.settings.setup.models.viscous.options.curvature_correction = (
                sub_config["curvature_correction"]
            )

        return True
