class MockSubplots():

    passed_args = []
    def subplots(self,*args):
        passed_args.append(args)