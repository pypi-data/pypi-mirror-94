class MockAnimate:    
    passed_filenames = []
    passed_kwargs = []
   
    def save(self,filename,**kwargs):
        self.passed_filenames.append(filename)
        self.passed_kwargs.append(kwargs)


    
    
