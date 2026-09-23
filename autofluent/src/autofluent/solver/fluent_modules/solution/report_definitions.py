class Report_Definitions:
    def __init__(self):
        self.session = None

    def setup(self, session, config):
        self.session = session

        quantities = config.get("quantities", {}) or {}
        for name, param in quantities.items():
            if not param:
                continue
            self.session.settings.solution.report_definitions.drag[name] = {
                "zones": param.get("zones", []),
                "force_vector": param.get("force_vector", [0, 0, 1]),
            }

        reports = config.get("reports", {}) or {}
        for name, report in reports.items():
            if not report:
                continue
            report_name = report.get("name", name)
            parameter = report.get("parameter")
            if not parameter:
                continue
            self.session.parameters.output_parameters.report_definitions.create(
                name=report_name
            )
            self.session.parameters.output_parameters.report_definitions[
                report_name
            ] = {"report_definition": parameter}
        return True
