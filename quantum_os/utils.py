from quantum_os.display import display, WIDTH
from quantum_os.constants import DEFAULT_CURSOR_X, DEFAULT_CURSOR_Y

def write_text_double_buffer(text, color, x=DEFAULT_CURSOR_X, y=DEFAULT_CURSOR_Y):
    """Write text to the screen using double buffering."""
    for _ in range(2):
        display.set_pen(color)
        display.text(text, x, y, WIDTH, 2)
        display.update()