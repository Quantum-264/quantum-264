import time
from quantum_os.display import *
class Cursor:
    def __init__(self, app, x=DEFAULT_CURSOR_X, y=DEFAULT_CURSOR_Y, cusor_visible=True, blink_interval=500, blinking_cursor=True, default_cursor_color=CURSOR_COLOR, bg_color=BG_COLOR):
        self.app = app
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.cursor_visible = cusor_visible
        self.blink_interval = blink_interval
        self.blinking_cursor = blinking_cursor
        self.blink_timer = time.ticks_ms()
        self.default_cursor_color = default_cursor_color
        self.cursor_color = default_cursor_color
        self.bg_color = bg_color

    def reset(self):
        self.x = self.default_x
        self.y = self.default_y

    
    def move_down(self, lines=1):
        """Move the cursor down n line."""
        self.y += LINE_HEIGHT * lines

    
    def draw(self):
        """Draws a blinking rectangle cursor at the current position."""
        if self.app == None: 
            return
        
        # Blink every blink_interval ms
        if time.ticks_ms() - self.blink_timer > self.blink_interval:
            self.cursor_visible = not self.cursor_visible  # Toggle visibility
            self.cursor_color = self.default_cursor_color if self.cursor_visible else self.bg_color
            self.blink_timer = time.ticks_ms()  # Reset timer

        display.set_clip(self.x, self.y, CHAR_WIDTH, LINE_HEIGHT - 5)
        display.set_pen(self.cursor_color)
        display.rectangle(self.x, self.y, CHAR_WIDTH, LINE_HEIGHT - 5)
        display.update()

    
    def erase(self):
        """Erase the cursor by redrawing the background in its place."""
        display.set_clip(self.x, self.y, CHAR_WIDTH, LINE_HEIGHT - 5)
        for _ in range(2):
            display.set_pen(BG_COLOR)
            display.rectangle(0, 0, WIDTH, HEIGHT)
            display.update()