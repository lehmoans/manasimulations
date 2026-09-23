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
        viscous_config = config.get("viscous_model")
        if viscous_config:
            self.viscous_models.setup(session, {"viscous_model": viscous_config})

        materials_config = config.get("materials")
        if materials_config:
            self.materials.setup(session, materials_config)

        zones_config = config.get("zones")
        if zones_config:
            self.zones.setup(session, zones_config)

        reference_config = config.get("reference_values")
        if reference_config:
            self.reference_values.setup(session, reference_config)

        boundary_config = config.get("BC")
        if boundary_config:
            self.boundary_conditions.setup(session, boundary_config)

        initialization_config = config.get("initialization")
        if initialization_config:
            self.initialization.setup(session, initialization_config)

        return True
