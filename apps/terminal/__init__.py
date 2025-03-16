import time
import quantum_os
from quantum_os.constants import *
from quantum_os.display import *
from quantum_os.memory import get_free_memory
from quantum_os.fs import get_applications

class App:
    def setup(self, display):
        self.display = display

        self.do_get_apps()

        self.uart = quantum_os.get_expansion_uart()

        self.cursor = {"x": DEFAULT_CURSOR_X, "y": DEFAULT_CURSOR_Y}
        self.command_buffer = ""
        self.command = ""
        self.command_history = []
        self.cursor_visible = True
        self.blink_interval = 500
        self.blinking_cursor = True
        self.blink_timer = time.ticks_ms()
        self.cursor_color = CURSOR_COLOR
        self.line_buffer = []
        self.selected_app = 0

        self.commands = {
            "CLEAR": {"description": "Clear the screen", "handler": self.command_clear},
            "HELP": {"description": "Show this help message", "handler": self.command_help},
            "APPS": {"description": "List available applications", "handler": self.command_apps},
            "COLORS": {"description": "Display all colors", "handler": self.command_colors},
            "MEM": {"description": "Display memory usage", "handler": self.command_mem},
        }


    def do_get_apps(self):
        self.apps = get_applications()
        self.str_apps = str(self.apps)

    def reset_cursor_position(self):
        self.cursor["x"] = DEFAULT_CURSOR_X
        self.cursor["y"] = DEFAULT_CURSOR_Y

    def clear_screen(self, prompt=True):
        """Clear the screen and reset cursor."""
        # display.draw_background()
        display.set_pen(BG_COLOR)
        display.rectangle(0, 0, WIDTH, HEIGHT)
        # for _ in range(2):
        # display.set_pen(BG_COLOR)
        # display.clear()
            # display.update()
        # self.reset_cursor_position()
        # self.command_buffer = ""
        # self.draw_header()

        # if prompt:
        #     self.draw_prompt()

        
        # yield from self.draw_cursor(force=True)  # Ensure cursor is visible on reset
        yield quantum_os.INTENT_NO_OP

    def add_to_buffer(self, line):
        self.line_buffer.append(line)
        if len(self.line_buffer) > 18:
            self.line_buffer = self.line_buffer[1:]

    def move_cursor_down(self, lines=1):
        """Move the cursor down one line."""
        self.cursor["y"] += LINE_HEIGHT * lines


    def draw_colors(self, o=70):
        for i, color in enumerate(COLORS):
            display.set_pen(color)
            display.rectangle(self.cursor["x"] + o + (i *  CHAR_WIDTH), self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT)


    def create_header(self):
        """Add the header text to the text buffer."""
        self.add_to_buffer({"text": "Quantum-264 Terminal", "o": 150, "c": COLORS[19]})
        self.add_to_buffer({"text": f"Free Memory: {get_free_memory()["free"]} KB", "o": 150, "c": COLORS[25]})
        self.add_to_buffer({"cmd": self.draw_colors})


    def draw_prompt(self):
        """Draws the command prompt '>' at the start of the line."""
        display.set_pen(TEXT_COLOR)
        display.text(">"+self.command_buffer, self.cursor["x"] - 10, self.cursor["y"], WIDTH, 2)
        self.cursor["x"] = DEFAULT_CURSOR_X + 10 + (len(self.command_buffer) - 1) * CHAR_WIDTH 


    def erase_cursor(self):
        """Erase the cursor by redrawing the background in its place."""
        self.cursor_color = CURSOR_COLOR if self.cursor_visible else BG_COLOR

    def draw_cursor(self, force=False):
        """Draws a blinking rectangle cursor at the current position."""
        # Blink every blink_interval ms
        if time.ticks_ms() - self.blink_timer > self.blink_interval:
            self.cursor_visible = not self.cursor_visible  # Toggle visibility
            # self.cursor_color = CURSOR_COLOR if self.cursor_visible else BG_COLOR
            self.erase_cursor()  
            self.blink_timer = time.ticks_ms()  # Reset timer

        display.set_pen(self.cursor_color)
        display.rectangle(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)


    def command_unknown(self):
        """Display an unknown command message."""
        self.add_to_buffer({"text": f"Unknown command: {self.command}", "c": COLORS[2]})

    def command_apps(self):
        """Display a list of available applications."""
        self.add_to_buffer({"text": "Available applications:", "c": COLORS[6]})
        for app_index, app in enumerate(self.apps):
            self.add_to_buffer({"text": f"{app_index + 1}. {app["title"]}", "c": COLORS[4]})

    def command_clear(self):
        """Clear the text buffer."""
        self.line_buffer = []

    def command_help(self):
        """Display a list of available commands."""
        self.add_to_buffer({"text": "Available commands:", "c": COLORS[6]})
        for key, value in self.commands.items():
            self.add_to_buffer({"text": f"{key} - {value["description"]}", "c": COLORS[4]})

    def command_colors(self):
        """Display all colors."""
        self.add_to_buffer({"cmd": self.draw_colors})

    def command_mem(self):
        """Display memory usage."""
        self.add_to_buffer({"text": f"Free Memory: {get_free_memory()["free"]} KB", "c": COLORS[25]})

    def command_load_app(self):
        """Load an application."""
        yield quantum_os.INTENT_REPLACE_APP(
            self.apps[self.selected_app]
        )
    

    ## TODO: Add CommandHandler class
    def handle_command(self):
        """Handle user input and execute commands."""
        # Remove leading/trailing spaces
        self.command = self.command_buffer.strip()

        # Clear command buffer
        self.command_buffer = ""  

        # Add command to text buffer
        self.add_to_buffer({"text": f">{self.command}", "c": COLORS[3], "o": -10})

        try:
            # Execute command
            self.commands[self.command]["handler"]()
        except KeyError:
            # Handle unknown command
            self.command_unknown()
    
        # ensure there is a yield 
        yield quantum_os.INTENT_NO_OP

    def draw_text_buffer(self):
        for text in self.line_buffer:
            if "text" in text:
                display.set_pen(text["c"])
                offset = text["o"] if "o" in text else 0
                display.text(text["text"], self.cursor["x"] + offset, self.cursor["y"], WIDTH, 2)
            elif "cmd" in text:
                text["cmd"]()
            self.move_cursor_down()

    def process_keys(self):
        pressed_keys = quantum_os.kbd.get_keys()
        active_modifiers = quantum_os.kbd.get_modifier()

        if active_modifiers:
            pass
        if any(pressed_keys):
            if "Enter" in pressed_keys:
                yield from self.handle_command()
            elif "Backspace" in pressed_keys:
                self.command_buffer = self.command_buffer[:-1]
            elif "Space" in pressed_keys:
                self.command_buffer += " "
            elif "Tab" in pressed_keys:
                self.command_buffer += "\t"
            elif len(pressed_keys[0]) == 1:  
                self.command_buffer += pressed_keys[0]
            
            
            yield quantum_os.INTENT_FLIP_BUFFER
        
        yield quantum_os.INTENT_NO_OP


    def run(self):
        self.create_header()
        while True:
            yield from self.clear_screen()
            yield from self.process_keys()

            self.draw_text_buffer()
            self.draw_prompt()
            self.draw_cursor()
            yield quantum_os.INTENT_FLIP_BUFFER
            self.reset_cursor_position()
            time.sleep(0.1)
            

    def cleanup(self):
        pass


if __name__ == '__main__':
    quantum_os.boot(App)