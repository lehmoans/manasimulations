class MockSession:

    def __init__(self, mode=None):
        self.mode = mode
        self.closed = False

    def close(self):
        print("MOCK SESSION: close")
        self.closed = True
