class MockFuture:

    def __init__(self, mocked_return_data):
        self.mocked_return_data = mocked_return_data

    def result(self):
        return self.mocked_return_data
        