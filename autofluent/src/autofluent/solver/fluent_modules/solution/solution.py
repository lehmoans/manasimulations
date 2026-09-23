from .controls import Controls
from .methods import Methods
from .monitors import Monitors
from .report_definitions import Report_Definitions


class Solution:
    def __init__(self):
        self.controls = Controls()
        self.methods = Methods()
        self.monitors = Monitors()
        self.report_definitions = Report_Definitions()

    def setup(self, session, config):
        self.controls.setup(session, config.get("control", {}) or {})
        self.methods.setup(session, config.get("methods", {}) or {})
        self.monitors.setup(session, config.get("monitors", {}) or {})
        self.report_definitions.setup(
            session,
            config.get("report_definitions", {}) or {},
        )
        return True
