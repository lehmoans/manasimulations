class Boundary_Conditions():
    """
    . Boundary Conditions
│      ├── Inlets
│      ├── Outlets
│      ├── Walls
│      └── Interfaces
    """
    
    def __init__(self) -> None:
        pass

    def setup(self, session,config):

        self.session = session
        #cleaning the config of unset variables
        for name, value in config.items(): 

            if value in ("", None, 0):
                continue

            method = getattr(self,f"set_{name}_BC",None)

            if method:
                method(self.session, value[name])

    def set_inlet_BC(self,sub_config):
        if sub_config["type"] == "velocity":
            self.inlet = self.session.settings.setup.boundary_conditions.velocity_inlet["inlet"]
            self.inlet.momentum.velocity.value = self.inlet_velocity #might be wrong

        if sub_config["turbulence_intensity"]:
            self.inlet.turbulence.turb_intensity = sub_config["turbulence_intensity"]

            if sub_config["turbulence_viscosity_ratio"]:
                self.inlet.turbulence.turb_viscosity_ratio = sub_config["turbulence_viscosity_ratio"]
    
    def set_outlet_BC(self,sub_config):
        if sub_config["type"] =="pressure":
            self.outlet = self.session.settings.setup.boundary_conditions.pressure_outlet["outlet"]
        if sub_config["turbulence_intensity"]:
            self.outlet.turbulence.turb_intensity = sub_config["turbulence_intensity"]
            
"""
still hardcoded. needs to be implemented as a class incorporating all its properties
"""
    