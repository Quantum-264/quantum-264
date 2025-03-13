from picovision import PicoVision, PEN_P5

WIDTH, HEIGHT = 640, 480
display = PicoVision(PEN_P5, WIDTH, HEIGHT)

# Define colors as pens
PURE_BLACK = display.create_pen(0, 0, 0)
DEEP_GRAY = display.create_pen(27, 27, 27)
MID_GRAY = display.create_pen(115, 115, 115)
PURE_WHITE = display.create_pen(255, 255, 255)

DEEP_NAVY = display.create_pen(20, 36, 75)
BOLD_BLUE = display.create_pen(32, 80, 192)
SKY_BLUE = display.create_pen(90, 161, 255)

DEEP_GREEN = display.create_pen(12, 72, 12)
GRASS_GREEN = display.create_pen(74, 166, 78)
LIME_GREEN = display.create_pen(175, 254, 120)

DEEP_CRIMSON = display.create_pen(91, 0, 28)
FIRE_RED = display.create_pen(192, 40, 40)
WARM_RED = display.create_pen(255, 107, 74)

EARTH_BROWN = display.create_pen(138, 80, 0)
GOLD_YELLOW = display.create_pen(224, 160, 44)
SOFT_YELLOW = display.create_pen(255, 235, 153)

DEEP_PURPLE = display.create_pen(44, 18, 76)
ROYAL_PURPLE = display.create_pen(134, 43, 160)
LAVENDER = display.create_pen(225, 134, 255)

DEEP_SHADOW = display.create_pen(34, 32, 52)
MUTED_BLUE_GRAY = display.create_pen(62, 58, 109)
MUTED_VIOLET = display.create_pen(103, 95, 153)

RUST_RED = display.create_pen(190, 74, 47)
BEIGE = display.create_pen(228, 166, 114)
PALE_PEACH = display.create_pen(255, 218, 185)

CYAN_NEON = display.create_pen(0, 168, 168)
PINK_NEON = display.create_pen(255, 119, 168)
BRIGHT_PINK = display.create_pen(255, 204, 255)
AQUA_GREEN = display.create_pen(96, 214, 182)
WARM_GOLD = display.create_pen(232, 181, 96)
RADIOACTIVE_YELLOW = display.create_pen(214, 230, 100)
FINAL_HIGHLIGHT = display.create_pen(255, 250, 181)

# Store colors in an indexed array
COLORS = [
    PURE_BLACK, DEEP_GRAY, MID_GRAY, PURE_WHITE,
    DEEP_NAVY, BOLD_BLUE, SKY_BLUE,
    DEEP_GREEN, GRASS_GREEN, LIME_GREEN,
    DEEP_CRIMSON, FIRE_RED, WARM_RED,
    EARTH_BROWN, GOLD_YELLOW, SOFT_YELLOW,
    DEEP_PURPLE, ROYAL_PURPLE, LAVENDER,
    DEEP_SHADOW, MUTED_BLUE_GRAY, MUTED_VIOLET,
    RUST_RED, BEIGE, PALE_PEACH,
    CYAN_NEON, PINK_NEON, BRIGHT_PINK, AQUA_GREEN,
    WARM_GOLD, RADIOACTIVE_YELLOW, FINAL_HIGHLIGHT
]


BORDER_COLOR = COLORS[20]
BG_COLOR = COLORS[19]
CURSOR_COLOR = COLORS[21]
TEXT_COLOR = COLORS[3]


