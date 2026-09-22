class Materials():
    """
     2. Materials
│      ├── Fluid materials
│      └── Solid materials
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

    def set_material(self,session,sub_config):
        if "fluid" in sub_config:
            session.tui.define.materials.change_create(sub_config["name"], sub_config["name"], "yes", "constant", sub_config["fluid"]["density"])
        elif "solid" in sub_config:
            pass

"""
further work:
* material properties (eg constant vs dynamic density) need to dynamically added
    - currently hardcoded according to needs. 
    - may require turning this into a class that can accomodate all those properties
"""

