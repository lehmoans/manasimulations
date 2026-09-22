class Monitors():
    def __init__ ( self):
        pass

    def setup(self,session, config):
        self.session = session
        self.config = config

        for name, value in config.items():

            if value in ("", None, 0):
                continue

            method = getattr(self, f"set_{name}", None)

            if method:
                method( value)

    def set_residals_criteria(self, sub_config):

        self.session.settings.solution.monitor.residual.equations["continuity"].absolute_criteria = (
            sub_config["continuity"]
        )
        self.session.settings.solution.monitor.residual.equations["x-velocity"].absolute_criteria = (
            sub_config["x-velocity"]
        )
        self.session.settings.solution.monitor.residual.equations["y-velocity"].absolute_criteria = (
            sub_config["y-velocity"]
        )
        self.session.settings.solution.monitor.residual.equations["z-velocity"].absolute_criteria = (
            sub_config["z-velocity"]
        )

        if "k-epislon" in self.config["viscous_model"]["type"]:
            self.session.settings.solution.monitor.residual.equations["k"].absolute_criteria = sub_config["k-velocity"]
            self.session.settings.solution.monitor.residual.equations["epsilon"].absolute_criteria = (
                sub_config["epislon"])

    def set_report_monitors(self, sub_config):
        self.session.settings.solution.monitor.report_plots.create(name= sub_config["name"])
        self.session.settings.solution.monitor.report_plots[sub_config["name"]] = {"report_defs": [sub_config["parameter"]]}

    
    """
    setup for other models
    - possible relate to the viscous model where parameters defined there will determine parameters here
    """
    
