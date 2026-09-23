class Reference_Values:

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

    def set_area(self, value):
        self.session.settings.setup.reference_values.area = value

    def set_density(self, value):
        self.session.settings.setup.reference_values.density = value

    def set_velocity(self, value):
        self.session.settings.setup.reference_values.velocity = value
