import machine
import time
from picovision import PicoVision, PEN_RGB555

# Set up the display
WIDTH, HEIGHT = 640, 480
display = PicoVision(PEN_RGB555, WIDTH, HEIGHT)

# Define colors
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# Set up UART (Serial Port)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))  # Adjust pins if needed

# Text settings
char_width = 12  # Approximate width of each character
cursor_x, cursor_y = char_width, char_width # Starting position
line_height = 20  # Spacing between lines
text_buffer = []  # Store typed characters for handling backspace

def clear_screen():
    """Clear the screen and reset cursor."""
    global cursor_x, cursor_y, text_buffer
    display.set_pen(BLACK)
    display.clear()
    display.update()
    display.clear()
    display.update()  # Ensure both buffers are cleared
    cursor_x, cursor_y = char_width, char_width
    text_buffer = []

def scroll_text():
    """Scroll text upwards when reaching the bottom."""
    global cursor_y
    if cursor_y + line_height >= HEIGHT:
        clear_screen()

def delete_character():
    """Erase the last character properly."""
    global cursor_x, cursor_y

    if text_buffer:  # Only delete if there's something to remove
        text_buffer.pop()  # Remove last character from buffer
        cursor_x -= char_width  # Move cursor back

        # Prevent moving left beyond margin
        if cursor_x < char_width:
            cursor_x = WIDTH - char_width
            cursor_y -= line_height  # Move up a line if needed

        # Draw a black box over the deleted character to erase it
        for _ in range(2):  # Draw twice for double-buffer sync
            display.set_pen(BLACK)
            display.rectangle(cursor_x, cursor_y, char_width, line_height)
            display.update()

def draw_text(char):
    """Draw a single character to both buffers."""
    global cursor_x, cursor_y, text_buffer

    # Handle backspace (delete previous character)
    if char in ("\b", "\x7f"):  # Support both Backspace (0x08) and Delete (0x7F)
        delete_character()
        return

    # Handle newline
    if char == "\n":
        cursor_x = char_width
        cursor_y += line_height
        scroll_text()
        text_buffer.append(char)
        return

    # Handle word wrapping
    if cursor_x + char_width >= WIDTH:
        cursor_x = char_width
        cursor_y += line_height
        scroll_text()

    # Draw character onto both buffers
    for _ in range(2):
        display.set_pen(WHITE)
        display.text(char, cursor_x, cursor_y, WIDTH, 2)
        display.update()

    # Store character in buffer for deletion handling
    text_buffer.append(char)

    # Move cursor right
    cursor_x += char_width

# Clear the screen at start
clear_screen()

while True:
    if uart.any():
        char = uart.read(1)  # Read 1 byte
        if char:
            draw_text(char.decode("utf-8"))
            time.sleep(0.01)  # Small delay for readability
