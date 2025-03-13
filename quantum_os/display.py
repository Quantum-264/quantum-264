from picovision import PicoVision, PEN_P5
from quantum_os.constants import *

WIDTH, HEIGHT = 640, 480
display = PicoVision(PEN_P5, WIDTH, HEIGHT)

# Define colors as pens
PURE_BLACK = display.create_pen(0, 0, 0)
DEEP_GRAY = display.create_pen(27, 27, 27)
MID_GRAY = display.create_pen(115, 115, 115)
PURE_WHITE = display.create_pen(255, 255, 255)

FIRE_RED = display.create_pen(192, 40, 40)
RUST_RED = display.create_pen(190, 74, 47)
WARM_RED = display.create_pen(255, 107, 74)

BEIGE = display.create_pen(228, 166, 114)
PALE_PEACH = display.create_pen(255, 218, 185)
EARTH_BROWN = display.create_pen(138, 80, 0)
WARM_GOLD = display.create_pen(232, 181, 96)
GOLD_YELLOW = display.create_pen(224, 160, 44)
SOFT_YELLOW = display.create_pen(255, 235, 153)
FINAL_HIGHLIGHT = display.create_pen(255, 250, 181)

RADIOACTIVE_YELLOW = display.create_pen(214, 230, 100)
LIME_GREEN = display.create_pen(175, 254, 120)
DEEP_GREEN = display.create_pen(12, 72, 12)
GRASS_GREEN = display.create_pen(74, 166, 78)
AQUA_GREEN = display.create_pen(96, 214, 182)
CYAN_NEON = display.create_pen(0, 168, 168)

SKY_BLUE = display.create_pen(90, 161, 255)
BOLD_BLUE = display.create_pen(32, 80, 192)
DEEP_NAVY = display.create_pen(20, 36, 75)

MUTED_BLUE_GRAY = display.create_pen(62, 58, 109)
DEEP_SHADOW = display.create_pen(34, 32, 52)
MUTED_VIOLET = display.create_pen(103, 95, 153)
DEEP_PURPLE = display.create_pen(44, 18, 76)
LAVENDER = display.create_pen(225, 134, 255)
ROYAL_PURPLE = display.create_pen(134, 43, 160)

BRIGHT_PINK = display.create_pen(255, 204, 255)
PINK_NEON = display.create_pen(255, 119, 168)
DEEP_CRIMSON = display.create_pen(91, 0, 28)

# Store colors in an indexed array
COLORS = [
    PURE_BLACK,DEEP_GRAY,MID_GRAY,PURE_WHITE,
    FIRE_RED,RUST_RED,WARM_RED,BEIGE,PALE_PEACH,
    EARTH_BROWN,WARM_GOLD,GOLD_YELLOW,SOFT_YELLOW,
    FINAL_HIGHLIGHT,RADIOACTIVE_YELLOW,LIME_GREEN,
    DEEP_GREEN,GRASS_GREEN,AQUA_GREEN,CYAN_NEON,
    SKY_BLUE,BOLD_BLUE,DEEP_NAVY,MUTED_BLUE_GRAY,
    DEEP_SHADOW,MUTED_VIOLET,DEEP_PURPLE,LAVENDER,
    ROYAL_PURPLE,BRIGHT_PINK,PINK_NEON,DEEP_CRIMSON
]


BORDER_COLOR = COLORS[23]
BG_COLOR = COLORS[24]
CURSOR_COLOR = COLORS[25]
TEXT_COLOR = COLORS[3]




def draw_border():
    """Draw a border around the screen."""
    
    for _ in range(2):
        display.set_pen(BORDER_COLOR)
        display.rectangle(0, 0, WIDTH, HEIGHT)
        display.update()
    for _ in range(2):
        display.set_pen(BG_COLOR)
        display.rectangle(BORDER_WIDTH, BORDER_HEIGHT, WIDTH - (BORDER_WIDTH * 2), HEIGHT - (BORDER_HEIGHT * 2))    
        display.update()