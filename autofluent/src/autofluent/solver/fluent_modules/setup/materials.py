class Materials:

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

    def set_fluid(self, sub_config):
        name = sub_config.get("name")
        density = sub_config.get("density")

        if not name or density is None:
            return False

        self.session.tui.define.materials.change_create(
            name,
            name,
            "yes",
            "constant",
            density,
        )
        return True

    def set_solid(self, sub_config):
        return True
