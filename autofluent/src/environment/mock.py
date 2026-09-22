from base import Environment

class Mock_Environment(Environment):
    def __init__(self) -> None:
        super().__init__()
    
    def prepare(self):
        print("MOCK ENVIRONMENT: prepare")
    
    def launch(self, mode):
        print("MOCK ENVIRONMENT: session launch")
    
    def close(self):
        print("MOCK ENVIRONMENT: session close")