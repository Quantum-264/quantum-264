import time
import quantum_os
from quantum_os.constants import *
from quantum_os.display import *
from quantum_os.memory import get_free_memory
from quantum_os.fs import get_applications
from quantum_os.utils import write_text_double_buffer


class App:
    print("[QOS].terminal")
    def setup(self, display):
        from quantum_os.terminal.command_handler import CommandHandler
        self.display = display

        # self.do_get_apps()

        self.uart = quantum_os.get_expansion_uart()

        self.cursor = {"x": DEFAULT_CURSOR_X, "y": DEFAULT_CURSOR_Y}
        self.cursor_visible = True
        self.blink_interval = 500
        self.blinking_cursor = True
        self.blink_timer = time.ticks_ms()
        self.cursor_color = CURSOR_COLOR
        self.line_buffer = []
        self.selected_app = 0
        self.last_key = None
        self.last_key_timer = time.ticks_ms()
        self.debounce_delay = 100
        self.command_handler = CommandHandler(self)
        # self.load_app = False
        


    def do_get_apps(self):
        self.apps = get_applications()
        self.str_apps = str(self.apps)

    def reset_cursor_position(self):
        self.cursor["x"] = DEFAULT_CURSOR_X
        self.cursor["y"] = DEFAULT_CURSOR_Y

    def clear_screen(self, prompt=True):
        """Clear the screen and reset cursor."""
        display.set_pen(BG_COLOR)
        display.rectangle(0, 0, WIDTH, HEIGHT)
        yield quantum_os.INTENT_NO_OP

    def add_to_buffer(self, line):
        self.line_buffer.append(line)
        if len(self.line_buffer) > 18:
            self.line_buffer = self.line_buffer[1:]

    def move_cursor_down(self, lines=1):
        """Move the cursor down one line."""
        self.cursor["y"] += LINE_HEIGHT * lines


    def draw_colors(self, o=85):
        for i, color in enumerate(COLORS):
            display.set_pen(color)
            display.rectangle(self.cursor["x"] + o + (i *  CHAR_WIDTH), self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT-10)


    def create_header(self):
        """Add the header text to the text buffer."""
        self.add_to_buffer({"text": "Quantum-264 Terminal!", "o": 165, "c": COLORS[19]})
        self.add_to_buffer({"text": f"Free Memory: {get_free_memory()["free"]} KB", "o": 165, "c": COLORS[25]})
        self.add_to_buffer({"cmd": self.draw_colors})


    def draw_prompt(self):
        """Draws the command prompt '>' at the start of the line."""
        display.set_pen(TEXT_COLOR)
        display.text(">"+self.command_handler.buffer, self.cursor["x"] - 10, self.cursor["y"], WIDTH, 2)
        self.cursor["x"] = DEFAULT_CURSOR_X + 10 + (len(self.command_handler.buffer) - 1) * CHAR_WIDTH 


    def draw_cursor(self, force=False):
        """Draws a blinking rectangle cursor at the current position."""
        # Blink every blink_interval ms
        if time.ticks_ms() - self.blink_timer > self.blink_interval:
            self.cursor_visible = not self.cursor_visible  # Toggle visibility
            self.cursor_color = CURSOR_COLOR if self.cursor_visible else BG_COLOR
            self.blink_timer = time.ticks_ms()  # Reset timer

        display.set_clip(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
        display.set_pen(self.cursor_color)
        display.rectangle(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
        display.update()

    def draw_text_buffer(self):
        for text in self.line_buffer:
            if "text" in text:
                display.set_pen(text["c"])
                offset = text["o"] if "o" in text else 0
                display.text(text["text"], self.cursor["x"] + offset, self.cursor["y"], WIDTH, 2)
            elif "cmd" in text:
                text["cmd"]()
            self.move_cursor_down()

    def erase_cursor(self):
        """Erase the cursor by redrawing the background in its place."""
        display.set_clip(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
        for _ in range(2):
            display.set_pen(BG_COLOR)
            display.rectangle(0, 0, WIDTH, HEIGHT)
            display.update()

    def draw_char(self, char):
        """Draw a single character to the screen."""
        display.set_clip(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
        self.erase_cursor()
        write_text_double_buffer(char, TEXT_COLOR, self.cursor["x"], self.cursor["y"])
        self.cursor["x"] += CHAR_WIDTH
        display.update()

        self.command_handler.buffer += char
        yield quantum_os.INTENT_NO_OP
        
    def erase_char(self):
        """Erase the last character from the screen."""
        self.cursor["x"] -= CHAR_WIDTH
        write_text_double_buffer("\b", BG_COLOR, self.cursor["x"], self.cursor["y"])
        display.update()

    def backspace(self):
        """Handle the backspace key."""
        if len(self.command_handler.buffer) > 0:
            self.command_handler.buffer = self.command_handler.buffer[:-1]
            self.erase_cursor()
            self.erase_char()

        yield quantum_os.INTENT_NO_OP


    def debounce(self, key, callback, debounce_delay=100):
        """Debounce a callback function."""
        if key != self.last_key or (time.ticks_ms() - self.last_key_timer) > debounce_delay:
            yield from callback()
            self.last_key_timer = time.ticks_ms()
            self.last_key = key

        yield quantum_os.INTENT_NO_OP


    def process_keys(self):
        while True:
            
            pressed_keys = quantum_os.kbd.get_keys()
            active_modifiers = quantum_os.kbd.get_modifier()
            display.set_clip(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
            if active_modifiers:
                pass
            
            if(len(pressed_keys) > 1):
                buffer = quantum_os.kbd.get_buffer()
                while buffer:
                    data = buffer.pop(0)
                    if len(data) == 1:
                        self.debounce(data, lambda: self.draw_char(data), self.debounce_delay)


            elif any(pressed_keys):
                if "Enter" in pressed_keys:
                    yield from self.debounce("Enter", self.command_handler.handle_command, self.debounce_delay*2)
                    print("Hit Enter")
                    return
                elif "Backspace" in pressed_keys:
                    yield from self.debounce("Backspace", self.backspace, self.debounce_delay/2)
                elif "Space" in pressed_keys:
                    yield from self.debounce(" ", lambda: self.draw_char(" "), self.debounce_delay)
                elif "Tab" in pressed_keys:
                    yield from self.debounce("\t", lambda: self.draw_char("\t"), self.debounce_delay)
                
                else:
                    key = pressed_keys[0]
                    if len(key) == 1:  
                        yield from self.debounce(key, lambda: self.draw_char(key), self.debounce_delay)
            else:
                self.last_key = None 
            
            self.draw_cursor()
            display.remove_clip()
            yield quantum_os.INTENT_NO_OP


    def run(self):
        set_border_color(BORDER_COLOR)
        display.set_pen(BG_COLOR)
        display.clear()
        display.update()
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
                yield from self.clear_screen()
                self.draw_text_buffer()
                self.draw_prompt()
                if i == 0:
                    self.reset_cursor_position()
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
            self.reset_cursor_position()
            

    def cleanup(self):
        pass


if __name__ == '__main__':
    quantum_os.boot(App)