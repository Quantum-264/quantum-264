import quantum_os
from quantum_os.constants import *
from quantum_os.display import *
from quantum_os.memory import get_free_memory
from quantum_os.cursor import Cursor


class App:
    print("[QOS].terminal")
    def setup(self, display):
        from quantum_os.terminal.command_handler import CommandHandler
        self.display = display

        self.uart = quantum_os.get_expansion_uart()

        self.line_buffer = []
        self.selected_app = 0
        self.command_handler = CommandHandler(self)
        
        self.cursor = Cursor(app=self)


    def add_to_buffer(self, line):
        self.line_buffer.append(line)
        if len(self.line_buffer) > 18:
            self.line_buffer = self.line_buffer[1:]


    def draw_colors(self, o=85):
        for i, color in enumerate(COLORS):
            self.display.set_pen(color)
            self.display.rectangle(self.cursor.x + o + (i *  CHAR_WIDTH), self.cursor.y, CHAR_WIDTH, LINE_HEIGHT-10)


    def create_header(self):
        """Add the header text to the text buffer."""
        self.add_to_buffer({"text": "Quantum-264 Terminal!", "o": 165, "c": COLORS[19]})
        self.add_to_buffer({"text": f"Free Memory: {get_free_memory()["free"]} KB", "o": 165, "c": COLORS[25]})
        self.add_to_buffer({"cmd": self.draw_colors})


    def draw_prompt(self):
        """Draws the command prompt '>' at the start of the line."""
        self.display.set_pen(TEXT_COLOR)
        self.display.text(">"+self.command_handler.buffer, self.cursor.x - 10, self.cursor.y, WIDTH, 2)
        self.cursor.x = DEFAULT_CURSOR_X + 10 + (len(self.command_handler.buffer) - 1) * CHAR_WIDTH 


    def draw_text_buffer(self):
        for text in self.line_buffer:
            if "text" in text:
                self.display.set_pen(text["c"])
                offset = text["o"] if "o" in text else 0
                self.display.text(text["text"], self.cursor.x + offset, self.cursor.y, WIDTH, 2)
            elif "cmd" in text:
                text["cmd"]()
            self.cursor.move_down()


    def backspace(self):
        """Handle the backspace key."""
        if len(self.command_handler.buffer) > 0:
            self.command_handler.buffer = self.command_handler.buffer[:-1]
            self.cursor.erase()
            erase_char(self.cursor)

        yield quantum_os.INTENT_NO_OP

    
    def handle_debounced_char(self, char):
        yield from draw_char(char, self.cursor)
        self.command_handler.buffer += char       
        yield quantum_os.INTENT_NO_OP


    def process_keys(self):
        while True:
            
            pressed_keys = quantum_os.kbd.get_keys()
            active_modifiers = quantum_os.kbd.get_modifier()
            self.display.set_clip(self.cursor.x, self.cursor.y, CHAR_WIDTH, LINE_HEIGHT - 5)
            if active_modifiers:
                pass
            
            if(len(pressed_keys) > 1):
                buffer = quantum_os.kbd.get_buffer()
                while buffer:
                    data = buffer.pop(0)
                    if len(data) == 1:
                        quantum_os.kbd.debounce(data,lambda: self.handle_debounced_char(data))

            elif any(pressed_keys):
                if "Enter" in pressed_keys:
                    yield from quantum_os.kbd.debounce("Enter", self.command_handler.handle_command, 2)
                    print("Hit Enter")
                    return
                elif "Backspace" in pressed_keys:
                    yield from quantum_os.kbd.debounce("Backspace", self.backspace)
                elif "Space" in pressed_keys:
                    yield from quantum_os.kbd.debounce(" ", lambda: self.handle_debounced_char(" "))
                elif "Tab" in pressed_keys:
                    yield from quantum_os.kbd.debounce("\t", lambda: self.handle_debounced_char("  "))
                
                else:
                    key = pressed_keys[0]
                    if len(key) == 1:  
                        yield from quantum_os.kbd.debounce(key, lambda: self.handle_debounced_char(key))
            else:
                self.last_key = None 

            self.cursor.draw()
            self.display.remove_clip()
            yield quantum_os.INTENT_NO_OP


    def run(self):
        set_border_color(BORDER_COLOR)
        self.display.set_pen(BG_COLOR)
        self.display.clear()
        self.display.update()
        print("Creating header")
        self.create_header()
        while True:
            print("Running terminal")

            quantum_os.environment["edit_file"] = False
            quantum_os.environment["load_app"] = False
        
            for i in range(2):
                """
                We draw double buffer to ensure the screen is updated in both buffers.
                This is because process_keys will only update a portion of the screen.
                Without the double buffer, one of the buffers will be stale.
                """
                yield from clear_screen()
                self.draw_text_buffer()
                self.draw_prompt()
                if i == 0:
                    self.cursor.reset()
                print("Drawing text buffer")
                yield quantum_os.INTENT_FLIP_BUFFER
            
            yield quantum_os.INTENT_FLIP_BUFFER
            yield from self.process_keys()
            if quantum_os.environment["load_app"]:
                
                yield quantum_os.INTENT_REPLACE_APP(
                    quantum_os.environment["selected_app"]
                )
                break
            elif quantum_os.environment["edit_file"]:
                yield quantum_os.INTENT_REPLACE_APP(
                    quantum_os.environment["edit_app"]
                )
            self.cursor.reset()

    def cleanup(self):
        pass


if __name__ == '__main__':
    quantum_os.boot(App)