from mock_future import MockFuture

class MockClient:
    def __init__(self):
        self.count = 0
        self.passed_args = []
        self.result_list_to_be_sent_in_future = []

    def submit(self,*args):
        self.passed_args.append(args)
        future = MockFuture(self.result_list_to_be_sent_in_future[self.count])
        self.count = self.count + 1
        return future
        
        