class Initialisation():
    """
        Initialization
│      ├── Hybrid initialization
│      └── Patch
    """

    def __init__(self) -> None:
        pass

    def setup(self,session, config):
        self.session =session
        self.config = config

        #cleaning the config of unset variables
        for name, value in config.items(): 

            if value in ("", None, 0):
                continue

            method = getattr(self,f"set_{name}",None)

            if method:
                method(session, value[name])
    
    
    def set_initialize(self,sub_config):
        init_type = sub_config["type"]
        self.session.settings.solution.initialization.initialization_type = init_type

        if  init_type == "standard":
            self.session.settings.solution.initialization.standard_initialize()

        elif init_type == "hybrid":
            self.session.settings.solution.initialization.hybrid_initialize()

    

    """
    further work:
    - setup for other initialization parameters

    """
            