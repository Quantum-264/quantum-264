import time
from core.constants import DEFAULT_CURSOR_X, DEFAULT_CURSOR_Y, CHAR_WIDTH, LINE_HEIGHT, BORDER_WIDTH, BORDER_HEIGHT, MARGIN_CURSOR
from core.display import display, COLORS, BG_COLOR, TEXT_COLOR, BORDER_COLOR, CURSOR_COLOR, WIDTH, HEIGHT
from core.memory import get_free_memory
from core.utils import write_text_double_buffer
from core.terminal_app.commands import command_list, show_colors
from core.fs import get_applications

class Terminal:
    def __init__(self, uart, cursor_visible=True, blinking_cursor=True, blink_interval=500):
        self.uart = uart

        self.cursor_x = DEFAULT_CURSOR_X
        self.cursor_y = DEFAULT_CURSOR_Y
        self.command_buffer = ""
        self.cursor_visible = cursor_visible
        self.blink_interval = blink_interval
        self.blinking_cursor = blinking_cursor
        self.blink_timer = time.ticks_ms()

    def reset_cursor(self):
        self.cursor_x = DEFAULT_CURSOR_X
        self.cursor_y = DEFAULT_CURSOR_Y

    def clear_screen(self, prompt=True):
        """Clear the screen and reset cursor."""
        for _ in range(2):
            display.set_pen(BG_COLOR)
            display.clear()
            display.update()
        self.reset_cursor()
        self.command_buffer = ""
        self.draw_border()
        self.draw_header()
        if prompt:
            self.draw_prompt()
        
        self.draw_cursor(force=True)  # Ensure cursor is visible on reset

    def move_cursor_down(self, lines=1):
        """Move the cursor down one line."""
        self.cursor_y += LINE_HEIGHT * lines

    def draw_border(self):
        """Draw a border around the screen."""
        
        for _ in range(2):
            display.set_pen(BORDER_COLOR)
            display.rectangle(0, 0, WIDTH, HEIGHT)
            display.update()
        for _ in range(2):
            display.set_pen(BG_COLOR)
            display.rectangle(BORDER_WIDTH, BORDER_HEIGHT, WIDTH - (BORDER_WIDTH * 2), HEIGHT - (BORDER_HEIGHT * 2))    
            display.update()

    def draw_header(self):
        """Draw a header at the top of the screen."""
        write_text_double_buffer(f"Quantum-264 Terminal", COLORS[19], x=self.cursor_x + 150, y=self.cursor_y)
        self.move_cursor_down()
        write_text_double_buffer(f"Free Memory: {get_free_memory()["total"]} KB", COLORS[25], x=self.cursor_x + 150, y=self.cursor_y)
        self.move_cursor_down()
        show_colors(x=self.cursor_x + 70, y=self.cursor_y)
        self.move_cursor_down()

    def draw_prompt(self):
        """Draws the command prompt '>' at the start of the line."""
        for _ in range(2):
            display.set_pen(TEXT_COLOR)
            display.text(">", self.cursor_x - 10, self.cursor_y, WIDTH, 2)
            display.update()


    def erase_cursor(self):
        """Erase the cursor by redrawing the background in its place."""
        display.set_pen(BG_COLOR)
        display.rectangle(self.cursor_x, self.cursor_y, CHAR_WIDTH, LINE_HEIGHT - 5)
        display.update()


    def draw_cursor(self, force=False):
        """Draws a blinking rectangle cursor at the current position."""
        # Blink every blink_interval ms
        if time.ticks_ms() - self.blink_timer > self.blink_interval:
            self.cursor_visible = not self.cursor_visible  # Toggle visibility
            self.blink_timer = time.ticks_ms()  # Reset timer

        if self.cursor_visible or force:  # Always draw if force=True
            display.set_pen(CURSOR_COLOR)
            display.rectangle(self.cursor_x, self.cursor_y, CHAR_WIDTH, LINE_HEIGHT - 5)
            display.update()
        else:
            self.erase_cursor()
    

    def delete_character(self):
        """Erase the last character properly."""
        if self.command_buffer:  # Only delete if there's something to remove
            self.erase_cursor()  # Remove cursor before clearing character
            self.command_buffer = self.command_buffer[:-1]  # Remove last character
            self.cursor_x -= CHAR_WIDTH  # Move cursor back

            # Prevent moving left beyond the prompt
            if self.cursor_x < DEFAULT_CURSOR_X:
                self.cursor_x = DEFAULT_CURSOR_X

            # Erase character by drawing a BG_COLOR box
            display.set_pen(BG_COLOR)
            display.rectangle(self.cursor_x, self.cursor_y, CHAR_WIDTH, LINE_HEIGHT)
            display.update()
        self.draw_cursor(force=True)  # Redraw cursor after deletion


    def scroll_text(self):
        """Scroll text upwards when reaching the bottom."""
        if self.cursor_y + LINE_HEIGHT >= HEIGHT:
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
            self.cursor_x = DEFAULT_CURSOR_X  # Reset cursor to start of new line
            self.move_cursor_down()  # Move down a line
            self.scroll_text()
            self.handle_command()  # Execute command
            self.command_buffer = ""  # Reset command buffer
            self.draw_cursor(force=True)  # Ensure cursor is visible
            return

        # Handle word wrapping
        if self.cursor_x + CHAR_WIDTH >= WIDTH:
            self.cursor_x = DEFAULT_CURSOR_X
            self.move_cursor_down()
            self.scroll_text()
            self.draw_prompt()

        # Draw character
        for _ in range(2):
            display.set_pen(TEXT_COLOR)
            display.text(char, self.cursor_x, self.cursor_y, WIDTH, 2)
            display.update()

        # Store character and move cursor
        self.command_buffer += char
        self.cursor_x += CHAR_WIDTH

        self.draw_cursor(force=True)  # Redraw cursor at new position


    ## TODO: Add CommandHandler class
    def handle_command(self):
        """Handle user input and execute commands."""

        if self.command_buffer.strip():  # Check if there's a command to execute
            command = self.command_buffer.strip()  # Remove leading/trailing spaces
            # for _ in range(2):
            #     erase_cursor()
            #     clear_screen()  # Clear screen before executing command

            # Execute command
            if command == "clear":
                self.clear_screen(False)  # Don't draw prompt after clearing
            elif command == "help":
                for _ in range(2):
                    display.set_pen(COLORS[6])
                    display.text("Available commands:", MARGIN_CURSOR, self.cursor_y, WIDTH, 2)
                    display.update()
                
                self.move_cursor_down()
                for i, cmd in enumerate(command_list):
                    for _ in range(2):
                        display.set_pen(COLORS[4])
                        display.text(f"{cmd["command"]} - {cmd["description"]}", MARGIN_CURSOR, self.cursor_y + (i * LINE_HEIGHT), WIDTH, 2)
                        display.update()
                self.move_cursor_down(len(command_list))
            elif command == "apps":
                display.set_pen(COLORS[6])
                display.text("Available applications:", MARGIN_CURSOR, self.cursor_y, WIDTH, 2)
                apps = get_applications()
                for i, app in enumerate(apps):
                    display.text(f"{i + 1}. {app["title"]}", MARGIN_CURSOR, self.cursor_y + i * LINE_HEIGHT, WIDTH, 2)
                display.update()
            elif command == "colors":
                self.clear_screen(False)
                show_colors(x=self.cursor_x, y=self.cursor_y)
                self.move_cursor_down()
            elif command == "mem":
                self.move_cursor_down()
                write_text_double_buffer(f"Free Memory: {get_free_memory()["total"]} KB", COLORS[25], x=self.cursor_x, y=self.cursor_y)
                self.move_cursor_down()

            else:
                self.cursor_x = MARGIN_CURSOR  # Reset cursor to start of new line
                write_text_double_buffer(f"Unknown command: {command}", COLORS[2], x=self.cursor_x, y=self.cursor_y)
                self.cursor_x = DEFAULT_CURSOR_X  # Reset cursor to start of new line
                self.move_cursor_down()

        self.draw_prompt()  # Redraw prompt after command execution
        self.draw_cursor(force=True)  # Ensure cursor is visible after command



    def run(self):
        self.clear_screen()
        while True:
            # Draw blinking cursor asynchronously (independent of input)
            self.draw_cursor()
            if self.uart.any():
                char = self.uart.read(1)  # Read 1 byte
                if char:
                    self.draw_text(char.decode("utf-8"))
                    time.sleep(0.01)  # Small delay for smooth input
        