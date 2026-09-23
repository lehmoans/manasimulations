from pathlib import Path


class MockSession:

    def __init__(self, mode=None):
        self.mode = mode
        self.closed = False
        self.output_path = None

    def set_output_path(self, path):
        self.output_path = Path(path)

    def close(self):
        print("MOCK SESSION: close")
        self.closed = True
