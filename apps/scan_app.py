'''
app["name"]="i2c Scanner"
app["id"]="i2c_scan_app"
app["icon"]="0000000000000000000100000000100000101000000101000010010000100100010001111110001001001100001100100101111111111010011111100111111001111111111111101111011111101111101101111110110111011110011110111011011001101101111110011001111101111111111111100001111111111000"
'''

#
# This app is modified from the i2c_scan_app.py from Abeisgoat 
# https://github.com/pimoroni/picovision
#

import time
import quantum_os
from quantum_os.display import *

class App:
    def setup(self, display):
        self.uart = quantum_os.get_expansion_uart()
        self.known_addresses = {
            "0D": "PicoVision GPU",
            "20": "Keyboard GPIO Expander"
        }
        self.cols = "0123456789ABCDEF"
        self.rows = "01234567"
    
        self.display = display
        self.cursor = {"x": 0, "y": 0}
        
        draw_background()
        
        self.devices = {}

        
        for device in quantum_os.get_internal_i2c().scan():
            addr = f'{device:02X}'
            
            if addr in self.known_addresses:
                name = self.known_addresses[addr]
            else:
                name = "Unknown Device"
                
            device = {
              "addr": addr,
              "name": name,
              "x": self.cols.find(addr[1]),
              "y": self.rows.find(addr[0])
            }
            
            
            self.devices[f'{device["x"]}x{device["y"]}'] = device
        
    def run(self):    
        print("[QOS].i2c_scan_app")
        print(self.devices)
        while True:            
            if self.cursor["x"] < 0:
                self.cursor["x"] = 15
            if self.cursor["x"] > 15:
                self.cursor["x"] = 0
                
            if self.cursor["y"] < 0:
                self.cursor["y"] = 7
            if self.cursor["y"] > 7:
                self.cursor["y"] = 0
 
            self.display.set_pen(BG_COLOR)
            
            self.display.rectangle(0, 0, WIDTH, HEIGHT)
            self.display.set_pen(TEXT_COLOR)
            
            y_offset = 38
            x_offset = 33

            for col_index, col in enumerate(self.cols):
                self.display.text(col, DEFAULT_CURSOR_X + (col_index*x_offset) + 24, DEFAULT_CURSOR_Y, -1, 2, 0)


            selected_device = "No Device selected."
            for row_index, row in enumerate(self.rows):

                y = DEFAULT_CURSOR_Y + (row_index*y_offset) + y_offset
                self.display.set_pen(TEXT_COLOR)
                self.display.text(row, DEFAULT_CURSOR_X+5, y-10, -1, 2, 0)
                for col_index in range(1, 17):
                    table_x = col_index-1
                    table_y = row_index
                    pos = f'{table_x}x{table_y}'
                    text = "--"
                    
                    x = DEFAULT_CURSOR_X + (table_x*x_offset) + x_offset
                    
                    is_cursor = self.cursor["x"] == table_x and self.cursor["y"] == table_y
                    
                    if is_cursor:
                        self.display.set_pen(CURSOR_COLOR)
                        self.display.rectangle(x-12, y-14, 16, 20)
                    
                    if pos in self.devices:
                        text = self.devices[pos]["addr"]
                        self.display.set_pen(TEXT_COLOR)
                        if is_cursor:
                            selected_device = f'Device: {self.devices[pos]["name"]}'
                        if not is_cursor:
                            self.display.rectangle(x-12, y-14, 16, 20)
                            self.display.set_pen(CURSOR_COLOR)
                    else:
                        self.display.set_pen(TEXT_COLOR)
                        
                    self.display.text(text, x, y, -1, 1, 180)
                    
            self.display.line(DEFAULT_CURSOR_X, HEIGHT-BORDER_HEIGHT-y_offset-10, WIDTH-BORDER_WIDTH-x_offset, HEIGHT-BORDER_HEIGHT-y_offset-10)
            self.display.text(selected_device, DEFAULT_CURSOR_X, HEIGHT-BORDER_HEIGHT-y_offset, -1, 2, 0)
            
            yield quantum_os.INTENT_FLIP_BUFFER
            while True:
                yield quantum_os.INTENT_NO_OP

                pressed_keys = quantum_os.kbd.get_keys()
                active_modifiers = quantum_os.kbd.get_modifier()

                if active_modifiers or any(pressed_keys):
                    print(f"Modifiers: {active_modifiers}, Keys: {pressed_keys}")

                if "Up Arrow" in pressed_keys:
                    self.cursor["y"] -= 1
                    break
                if "Down Arrow" in pressed_keys:
                    self.cursor["y"] += 1
                    break
                if "Left Arrow" in pressed_keys:
                    self.cursor["x"] -= 1
                    break
                if "Right Arrow" in pressed_keys:
                    self.cursor["x"] += 1
                    break
                if "Enter" in pressed_keys:
                    print("Enter")
                    break
                if "Q" in pressed_keys:
                    print("Q")
                    yield quantum_os.INTENT_KILL_APP
                    break


    def cleanup(self):
        pass

if __name__ == '__main__':
    quantum_os.boot(App)