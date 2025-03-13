import time

config = {
    "cursor": {
        "default_x": 40,
        "default_y": 60,
        "margin": 30,
        "x": 40,
        "y": 60,
        "visible": True,
        "blink_timer": time.ticks_ms(),
        "blink_interval": 500
    },
    "border": {
        "width": 20,
        "height": 40
    },
    "char_width": 12,
    "line_height": 20,
    "command_buffer": "",
}
# default_cursor_x, default_cursor_y = 40, 60  # Cursor starts after the '>'
# cursor_x, cursor_y = default_cursor_x, default_cursor_y  # Current cursor position
# margin_cursor = default_cursor_x - 10  # Cursor position before the prompt
# border_width, border_height = 20, 40  # Border padding
# char_width = 12  # Approximate width of each character
# line_height = 20  # Line spacing
# command_buffer = ""  # Stores user input
# cursor_visible = True  # Controls blinking cursor
# blink_timer = time.ticks_ms()  # Track time for cursor blinking
# blink_interval = 500  # Blinking speed (ms)