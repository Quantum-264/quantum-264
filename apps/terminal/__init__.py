import time
import quantum_os
from quantum_os.constants import *
from quantum_os.display import *
from quantum_os.memory import get_free_memory
from quantum_os.utils import write_text_double_buffer
from apps.terminal.commands import command_list, show_colors
from quantum_os.fs import get_applications

class App:
    def setup(self, display):
        self.display = display

        self.do_get_apps()

        self.uart = quantum_os.get_expansion_uart()

        self.cursor = {"x": DEFAULT_CURSOR_X, "y": DEFAULT_CURSOR_Y}
        self.command_buffer = ""
        self.command = ""
        self.cursor_visible = True
        self.blink_interval = 500
        self.blinking_cursor = True
        self.blink_timer = time.ticks_ms()

    def do_get_apps(self):
        self.apps = get_applications()
        self.str_apps = str(self.apps)

    def reset_cursor(self):
        self.cursor["x"] = DEFAULT_CURSOR_X
        self.cursor["y"] = DEFAULT_CURSOR_Y

    def clear_screen(self, prompt=True):
        """Clear the screen and reset cursor."""
        for _ in range(2):
            display.set_pen(BG_COLOR)
            display.clear()
            display.update()
        self.reset_cursor()
        self.command_buffer = ""
        draw_border()
        self.draw_header()
        if prompt:
            self.draw_prompt()
        
        self.draw_cursor(force=True)  # Ensure cursor is visible on reset

    def move_cursor_down(self, lines=1):
        """Move the cursor down one line."""
        self.cursor["y"] += LINE_HEIGHT * lines

    

    def draw_header(self):
        """Draw a header at the top of the screen."""
        write_text_double_buffer(f"Quantum-264 Terminal", COLORS[19], x=self.cursor["x"] + 150, y=self.cursor["y"])
        self.move_cursor_down()
        write_text_double_buffer(f"Free Memory: {get_free_memory()["total"]} KB", COLORS[25], x=self.cursor["x"] + 150, y=self.cursor["y"])
        self.move_cursor_down()
        show_colors(x=self.cursor["x"] + 70, y=self.cursor["y"])
        self.move_cursor_down()

    def draw_prompt(self):
        """Draws the command prompt '>' at the start of the line."""
        for _ in range(2):
            display.set_pen(TEXT_COLOR)
            display.text(">", self.cursor["x"] - 10, self.cursor["y"], WIDTH, 2)
            display.update()


    def erase_cursor(self):
        """Erase the cursor by redrawing the background in its place."""
        display.set_pen(BG_COLOR)
        display.rectangle(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
        display.update()

    def draw_cursor(self, force=False):
        """Draws a blinking rectangle cursor at the current position."""
        # Blink every blink_interval ms
        if time.ticks_ms() - self.blink_timer > self.blink_interval:
            self.cursor_visible = not self.cursor_visible  # Toggle visibility
            self.blink_timer = time.ticks_ms()  # Reset timer

        if self.cursor_visible or force:  # Always draw if force=True
            display.set_pen(CURSOR_COLOR)
            display.rectangle(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT - 5)
            display.update()
        else:
            self.erase_cursor()
    

    def delete_character(self):
        """Erase the last character properly."""
        if self.command_buffer:  # Only delete if there's something to remove
            self.erase_cursor()  # Remove cursor before clearing character
            self.command_buffer = self.command_buffer[:-1]  # Remove last character
            self.cursor["x"] -= CHAR_WIDTH  # Move cursor back

            # Prevent moving left beyond the prompt
            if self.cursor["x"] < DEFAULT_CURSOR_X:
                self.cursor["x"] = DEFAULT_CURSOR_X

            # Erase character by drawing a BG_COLOR box
            display.set_pen(BG_COLOR)
            display.rectangle(self.cursor["x"], self.cursor["y"], CHAR_WIDTH, LINE_HEIGHT)
            display.update()
        self.draw_cursor(force=True)  # Redraw cursor after deletion


    def scroll_text(self):
        """Scroll text upwards when reaching the bottom."""
        if self.cursor["y"] + LINE_HEIGHT >= HEIGHT:
            self.clear_screen()
            

    def draw_text(self, char):
        """Draw a single character and update cursor position."""
        for _ in range(2):
            self.erase_cursor()  # Remove the cursor before drawing new text

        # Handle backspace
        if char in ("\b", "\x7f"):  # Support both Backspace (0x08) and Delete (0x7F)
            self.delete_character()
            return

        # Handle Enter (New Line)
        if char == "\n":
            self.cursor["x"] = DEFAULT_CURSOR_X  # Reset cursor to start of new line
            self.move_cursor_down()  # Move down a line
            self.scroll_text()
            yield from self.handle_command()  # Execute command
            self.command_buffer = ""  # Reset command buffer
            self.draw_cursor(force=True)  # Ensure cursor is visible
            return

        # Handle word wrapping
        if self.cursor["x"] + CHAR_WIDTH >= WIDTH:
            self.cursor["x"] = DEFAULT_CURSOR_X
            self.move_cursor_down()
            self.scroll_text()
            self.draw_prompt()

        # Draw character
        for _ in range(2):
            display.set_pen(TEXT_COLOR)
            display.text(char, self.cursor["x"], self.cursor["y"], WIDTH, 2)
            display.update()

        # Store character and move cursor
        self.command_buffer += char
        self.cursor["x"] += CHAR_WIDTH

        self.draw_cursor(force=True)  # Redraw cursor at new position
        yield quantum_os.INTENT_NO_OP


    ## TODO: Add CommandHandler class
    def handle_command(self):
        """Handle user input and execute commands."""
        print("Command:", self.command_buffer.strip(), "length", len(self.command_buffer.strip()))
        if self.command_buffer.strip():  # Check if there's a command to execute
            self.command = self.command_buffer.strip()  # Remove leading/trailing spaces
            # for _ in range(2):
            #     erase_cursor()
            #     clear_screen()  # Clear screen before executing command

            # Execute command
            if self.command == "CLEAR":
                self.clear_screen(False)  # Don't draw prompt after clearing
            elif self.command == "HELP":
                for _ in range(2):
                    display.set_pen(COLORS[6])
                    display.text("Available commands:", MARGIN_CURSOR, self.cursor["y"], WIDTH, 2)
                    display.update()
                
                self.move_cursor_down()
                for i, cmd in enumerate(command_list):
                    for _ in range(2):
                        display.set_pen(COLORS[4])
                        display.text(f"{cmd["command"]} - {cmd["description"]}", MARGIN_CURSOR, self.cursor["y"] + (i * LINE_HEIGHT), WIDTH, 2)
                        display.update()
                self.move_cursor_down(len(command_list))
            elif self.command == "APPS":
                display.set_pen(COLORS[6])

                display.text("Available applications:", MARGIN_CURSOR, self.cursor["y"], WIDTH, 2)
                self.move_cursor_down()
                for app_index, app in enumerate(self.apps):
                    display.text(f"{app_index + 1}. {app["title"]}", MARGIN_CURSOR, self.cursor["y"] + app_index * LINE_HEIGHT, WIDTH, 2)
                    display.update()

            elif self.command == "APP0":
                self.move_cursor_down()
                yield quantum_os.INTENT_REPLACE_APP(
                        self.apps[1]
                    )
                # print(self.apps)

                # quantum_os.prepare_for_launch()
                # imp = __import__(self.apps[1]["file"])  # Import the top-level 'apps' module
                # app = getattr(imp, self.apps[1]["file"], None)  # Retrieve 'scan_app' submodule
                # print("app", app, self.apps[1]["file"], imp)
                # if app:
                #     app_instance = app.App()
                #     app_instance.setup(display)
                #     app_instance.run()
                
                

                # apps = get_applications()
                # for i, app in enumerate(apps):
                #     display.text(f"{i + 1}. {app["title"]}", MARGIN_CURSOR, self.cursor["y"] + i * LINE_HEIGHT, WIDTH, 2)
                # display.update()
            elif self.command == "COLORS":
                self.clear_screen(False)
                show_colors(x=self.cursor["x"], y=self.cursor["y"])
                self.move_cursor_down()
            elif self.command == "MEM":
                write_text_double_buffer(f"Free Memory: {get_free_memory()["total"]} KB", COLORS[25], x=self.cursor["x"], y=self.cursor["y"])
                self.move_cursor_down()

            else:
                self.cursor["x"] = MARGIN_CURSOR  # Reset cursor to start of new line
                write_text_double_buffer(f"Unknown command: {self.command}", COLORS[2], x=self.cursor["x"], y=self.cursor["y"])
                self.cursor["x"] = DEFAULT_CURSOR_X  # Reset cursor to start of new line
                self.move_cursor_down()

        self.draw_prompt()  # Redraw prompt after command execution
        self.draw_cursor(force=True)  # Ensure cursor is visible after command
        yield quantum_os.INTENT_NO_OP  # Flip buffer after executing command

    def run(self):
        self.clear_screen()
        yield quantum_os.INTENT_FLIP_BUFFER
        while True:
            self.draw_cursor()
            yield quantum_os.INTENT_NO_OP

            pressed_keys = quantum_os.kbd.get_keys()
            active_modifiers = quantum_os.kbd.get_modifier()

            if active_modifiers or any(pressed_keys):
                print(f"Modifiers: {active_modifiers}, Keys: {pressed_keys}")
                
                if "Enter" in pressed_keys:
                    yield from self.draw_text("\n")
                elif "Backspace" in pressed_keys:
                    yield from self.draw_text("\b")
                elif "Space" in pressed_keys:
                    yield from self.draw_text(" ")
                elif "Tab" in pressed_keys:
                    yield from self.draw_text("\t")
                else:                    
                    yield from self.draw_text(pressed_keys[0])
                
                time.sleep(0.1)
            
            


        # while True:
        #     self.command = ""
        #     # Draw blinking cursor asynchronously (independent of input)
        #     self.draw_cursor()
        #     if self.uart.any():
        #         char = self.uart.read(1)  # Read 1 byte
        #         if char:
        #             yield from self.draw_text(char.decode("utf-8"))
                    
        #             # print(self.command)
        #             # if self.command == "app0":
        #             #     yield quantum_os.INTENT_REPLACE_APP(
        #             #         self.apps[1]
        #             #     )
        #             #     break
        #             time.sleep(0.01)  # Small delay for smooth input
    
    def cleanup(self):
        pass


if __name__ == '__main__':
    quantum_os.boot(App)