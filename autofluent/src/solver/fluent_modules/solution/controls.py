class Controls():
    """
        Solution Controls
│      ├── Monitors
│      ├── Convergence
│      └── Reporting
    """
    def __init__(self) -> None:
        pass
    
    def setup(self, session,config):

        self.session = session
        #cleaning the config of unset variables
        for name, value in config.items(): 

            method = getattr(self,f"set_{name}",None)

            if method:
                method(self.session, value[name])

        def set_model(self,sub_config):
            if sub_config["model"] == "p-v":
                self.session.tui.solve.set.p_v_coupling(24) #activation of coupling same as: self.fluent.solution.methods.p_v_coupling.flow_scheme.set_state("Coupled")
            
            