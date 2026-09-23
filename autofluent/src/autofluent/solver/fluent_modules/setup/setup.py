from .boundary_conditions import Boundary_Conditions
from .initialization import Initialisation
from .materials import Materials
from .models import Models
from .reference_values import Reference_Values
from .zones import Zones


class Setup:
    def __init__(self):
        self.boundary_conditions = Boundary_Conditions()
        self.initialization = Initialisation()
        self.materials = Materials()
        self.viscous_models = Models()
        self.reference_values = Reference_Values()
        self.zones = Zones()

    def setup(self, session, config):
        viscous_config = (config.get("models", {}) or {}).get("viscous")
        if viscous_config:
            self.viscous_models.setup(session, {"viscous_model": viscous_config})

        for key, component in (
            ("materials", self.materials),
            ("zones", self.zones),
            ("reference_values", self.reference_values),
            ("BC", self.boundary_conditions),
            ("initialization", self.initialization),
        ):
            value = config.get(key)
            if value:
                component.setup(session, value)
        return True
