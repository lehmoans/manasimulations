from .utilities import method_caller
class Models():
    """
      Case / Model
│      ├── General settings
│      ├── Models
│      └── Operating conditions
    """
    def __init__(self) -> None:
        pass

    def setup(self, session,config):

        #cleaning the config of unset variables
        for name, value in config.items(): 

            if value in ("", None, 0):
                continue

            method = getattr(self,f"set_{name}",None)

            if method:
                method(session, value[name])
        
    def set_viscous_model(self,sub_config):
        if sub_config["type"] == "k-epilson":
            self.session.settings.setup.models.viscous.model = sub_config["type"]
            self.session.settings.setup.models.viscous.k_epsilon_model = sub_config["k_epilson"]
            self.session.settings.setup.models.viscous.options.curvature_correction = sub_config["curvature_correction"]
        
        print(f'VISCOUS MODEL: {sub_config["type"]}')

"""
further work:
*need to add other models too: k-w etc
    - will need to convert this to classes to accomodate properties
"""
        
        
        

    