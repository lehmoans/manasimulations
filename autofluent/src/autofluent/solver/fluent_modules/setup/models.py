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
        model_type = sub_config.get("type")
        if model_type != "k-epsilon":
            if model_type == "k-epilson":
                model_type = "k-epsilon"
            else:
                raise ValueError(f"Unsupported viscous model: {model_type}")

        self.session.settings.setup.models.viscous.model = model_type

        model_variant = sub_config.get("k_epsilon")
        if model_variant is None:
            model_variant = sub_config.get("k_epilson")

        if model_variant is not None:
            self.session.settings.setup.models.viscous.k_epsilon_model = model_variant

        if "curvature_correction" in sub_config:
            self.session.settings.setup.models.viscous.options.curvature_correction = (
                sub_config["curvature_correction"]
            )

        print(f"VISCOUS MODEL: {model_type}")
        return True
