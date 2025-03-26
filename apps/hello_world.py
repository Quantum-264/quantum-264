import quantum_os
from quantum_os.display import *

class App:
    def setup(self, display):
        self.uart = quantum_os.get_expansion_uart()
        self.display = display
        self.cursor = {"x": 0, "y": 0}
        
        self.display.set_pen(BG_COLOR)
        self.display.rectangle(0, 0, WIDTH, HEIGHT)
        
    def run(self):    
        print("[QOS].hello_world_app")
        for _ in range(2):
            self.display.clear()
            self.display.set_pen(BG_COLOR)
            self.display.rectangle(0, 0, WIDTH, HEIGHT)
            self.display.update()
        while True:
            self.display.set_pen(TEXT_COLOR)
            self.display.text("Hello World!", int(WIDTH/2)-60, int(HEIGHT/2)-LINE_HEIGHT, -1, 2, 0)
            self.display.set_pen(COLORS[6])
            self.display.text("Press 'q' to exit", int(WIDTH/2)-80, int(HEIGHT/2), -1, 2, 0)
            yield quantum_os.INTENT_FLIP_BUFFER
            while True:
                yield quantum_os.INTENT_NO_OP

                pressed_keys = quantum_os.kbd.get_keys()
                if "q" in pressed_keys:
                    print("q")
                    
                    yield quantum_os.INTENT_KILL_APP
                    break

    def cleanup(self):
        pass

if __name__ == '__main__':
    quantum_os.boot(App)