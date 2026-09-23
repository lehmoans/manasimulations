
"""
method_caller: used in each defined class to match the yaml 
variables to its assigned setter functions defined within the class
"""
def method_caller(session,config):

        #cleaning the c
        for name, value in config.items(): 

            method = getattr(self,f"set_{name}",None)

            if method:
                method(session, value[name])