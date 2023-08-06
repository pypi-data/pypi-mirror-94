class MockSnsHeatmap:
    passed_args = []
    passed_kwargs = []

    @staticmethod
    def heatmap(*args,**kwargs):
        passed_args.append(args)
        passed_kwargs.append(kwargs)
        print("calling method")
