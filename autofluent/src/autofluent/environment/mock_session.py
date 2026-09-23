# mock_session.py

class MockSession():

    def __init__(self):
        self.closed = False

    def close(self):
        print("MOCK SESSION: close")
        self.closed = True