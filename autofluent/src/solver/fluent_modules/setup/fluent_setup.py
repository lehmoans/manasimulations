from .boundary_conditions import Boundary_Conditions
from .initialization import Initialisation
from .materials import Materials
from .models import Models
from .reference_values import Reference_Values
from .zones import Zones

class Fluent_Setup():
    def __init__(self) -> None:
        
        self.boundary_conditions = Boundary_Conditions()
        self.initialization = Initialisation()
        self.materials = Materials()
        self.viscous_models = Models()
        self.reference_values = Reference_Values()
        self.zones = Zones()
    
    def setup(self, session, config):
        self.viscous_models.setup(session, config["viscous_model"])

        self.materials.setup(session, config["materials"])
        self.zones.setup(session, config[""]) # UPDATE THIS WITH FUNCTIONS 

        self.reference_values = Reference_Values()

        self.boundary_conditions = Boundary_Conditions()
        self.initialization = Initialisation()
        
        
        
        

