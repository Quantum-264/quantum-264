'''
app["name"]="Flashlight"
app["id"]="flashlight_app"
app["icon"]="0000000000000000000100000000100000101000000101000010010000100100010001111110001001001100001100100101111111111010011111100111111001111111111111101111011111101111101101111110110111011110011110111011011001101101111110011001111101111111111111100001111111111000"
'''
import time
import quantum_os
from quantum_os.display import *

class App:
    def setup(self, _):
        self.uart = quantum_os.get_expansion_uart()
        
    def run(self):
        draw_border()
        while True:
            display.set_pen(TEXT_COLOR)
            display.text("Hello World", 60, 60, 1, 1)
            display.update()
            time.sleep(0.01)
            
        
    def cleanup(self):
        pass

if __name__ == '__main__':
    quantum_os.boot(App)