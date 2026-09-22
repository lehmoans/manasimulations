class Reference_Values():
    """
        Reference Values
│      └── Density, velocity, area, length, etc.
    """

    def __init__(self) -> None:
        pass

    def setup(self, session,config):

        self.session = session
        #cleaning the config of unset variables
        for name, value in config.items(): 

            if value in ("", None, 0):
                continue

            method = getattr(self,f"set_{name}",None)

            if method:
                method(self.session, value[name])
    
    def set_area(self,sub_config):
        self.session.settings.setup.reference_values.area = sub_config["area"]
   
    def set_density(self,sub_config):
        self.session.settings.setup.reference_values.density = sub_config["density"]

    def set_velocity(self, sub_config):
        self.session.settings.setup.reference_values.velocity = sub_config["velocity"]

