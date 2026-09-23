from .controls import Controls
from .methods import Methods
from .monitors import Monitors
from .report_definitions import Report_Definitions

class Solution():
    def __init__(self):
        self.controls = Controls()
        self.methods = Methods()
        self.monitors = Monitors()
        self.report_definitions = Report_Definitions()
    
    def setup(self, session, config):
        self.controls.setup(session,config)
        self.methods.setup(session,config)
        self.monitors.setup(session,config)
        self.report_definitions.setup(session,config)

    

    

    
        
        
