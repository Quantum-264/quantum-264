import quantum_os
from quantum_os.display import *

class App:
    """
    This app intentionally throws an error to 
    ensure errors are caught and displayed on screen
    """
    def setup(self, display):       
        #Intentional Error
        a = self.sdfoijhasddkj
        
    def run(self):    
        print("[QOS].error_test")
        yield quantum_os.INTENT_NO_OP
        
    
    def cleanup(self):
        pass

if __name__ == '__main__':
    quantum_os.boot(App)