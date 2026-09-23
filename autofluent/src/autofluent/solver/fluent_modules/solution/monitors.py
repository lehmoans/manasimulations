class Monitors:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session
        residuals = config.get("residuals", {}) or {}
        if residuals:
            self.set_residuals(residuals)

        reports = config.get("reports", {}) or {}
        for name, report in reports.items():
            if report:
                self.set_report_monitor(name, report)
        return True

    def set_residuals(self, sub_config):
        for equation, criteria in sub_config.items():
            if criteria in ("", None, 0):
                continue
            self.session.settings.solution.monitor.residual.equations[
                equation
            ].absolute_criteria = criteria

    def set_report_monitor(self, name, sub_config):
        parameter = sub_config.get("parameter")
        if not parameter:
            return
        self.session.settings.solution.monitor.report_plots.create(name=name)
        self.session.settings.solution.monitor.report_plots[name] = {
            "report_defs": [parameter]
        }
