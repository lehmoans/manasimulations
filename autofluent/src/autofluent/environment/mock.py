from base import BaseEnvironment

class MockEnvironment(BaseEnvironment):
    def __init__(self,config) -> None:
        super().__init__(config)
    
    def check_environment(self):
        pass
    
    def prepare(self):
        print("MOCK ENVIRONMENT: prepare")
    
    def launch_session(self, mode):
        print("MOCK ENVIRONMENT: session launch")
    
    def close(self):
        print("MOCK ENVIRONMENT: session close")