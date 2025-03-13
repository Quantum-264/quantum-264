import time

default_cursor_x, default_cursor_y = 40, 60  # Cursor starts after the '>'
cursor_x, cursor_y = default_cursor_x, default_cursor_y  # Current cursor position
margin_cursor = default_cursor_x - 10  # Cursor position before the prompt
border_width, border_height = 20, 40  # Border padding
char_width = 12  # Approximate width of each character
line_height = 20  # Line spacing
command_buffer = ""  # Stores user input
cursor_visible = True  # Controls blinking cursor
blink_timer = time.ticks_ms()  # Track time for cursor blinking
blink_interval = 500  # Blinking speed (ms)