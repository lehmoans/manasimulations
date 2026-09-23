class Boundary_Conditions:

    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session

        for name, value in config.items():
            if value in ("", None, 0):
                continue

            method = getattr(self, f"set_{name}_BC", None)
            if method:
                method(value)

        return True

    def set_inlet_BC(self, sub_config):
        inlet_name = sub_config.get("name", "inlet")

        if sub_config.get("type") == "velocity":
            inlet = self.session.settings.setup.boundary_conditions.velocity_inlet[
                inlet_name
            ]
            inlet.momentum.velocity.value = sub_config.get("value", 0)

            if "turbulence_intensity" in sub_config:
                inlet.turbulence.turb_intensity = sub_config["turbulence_intensity"]

            if "turbulence_viscosity_ratio" in sub_config:
                inlet.turbulence.turb_viscosity_ratio = sub_config[
                    "turbulence_viscosity_ratio"
                ]

    def set_outlet_BC(self, sub_config):
        outlet_name = sub_config.get("name", "outlet")

        if sub_config.get("type") == "pressure":
            outlet = self.session.settings.setup.boundary_conditions.pressure_outlet[
                outlet_name
            ]

            if "value" in sub_config:
                outlet.momentum.gauge_pressure.value = sub_config["value"]

            if "turbulence_intensity" in sub_config:
                outlet.turbulence.turb_intensity = sub_config["turbulence_intensity"]
