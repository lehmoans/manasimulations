class Report_Definitions():
    def __init__(self) -> None:
        pass

    def setup(self,session,config):
        self.session = session
        #cleaning the config of unset variables
        for name, value in config.items(): 
            method = getattr(self,f"set_{name}",None)

            if method:
                method(self.session, value[name])
    
    def set_report_definitions(self,sub_config):
        #creates a quantity that is measured during calc from the defined zones/axis
        for param in sub_config["quantities"]:
            param_name = param["name"]

            self.session.settings.solution.report_definitions.drag[param_name] = {}
            self.session.settings.solution.report_definitions.drag[param_name] = {
            "zones": [param["zones"]],
            "force_vector": param["force_vector"],
        }

        for param in sub_config["parameter_report_definition"]["reports"].values():
            self.session.parameters.output_parameters.report_definitions.create(name=param["name"])
            self.session.parameters.output_parameters.report_definitions["parameter-1"] = {
            "report_definition": "cd-mon1"
        }

        
    