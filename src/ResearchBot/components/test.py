class Testing:
    def __init__(self) :
        self.test = "Testing for variables"
        
    def change_vars(self):
        self.testvar = "Did I get added ?"
    
    def rand_method(self):
        print(self.testvar)
        
        
testing1 = Testing()
testing1.change_vars()
testing1.rand_method()