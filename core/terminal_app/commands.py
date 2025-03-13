from core.display import display, COLORS
from core.constants import CHAR_WIDTH, LINE_HEIGHT

command_list = [
    {"command": "clear", "description": "Clear the screen"},
    {"command": "help", "description": "Show this help message"},
    {"command": "apps", "description": "List available applications"},
    {"command": "colors", "description": "Display all colors"},
    {"command": "mem", "description": "Display memory usage"},
]


def show_colors(x, y):
    for i, color in enumerate(COLORS):
        for _ in range(2):
            display.set_pen(color)

            display.rectangle(x + (i *  CHAR_WIDTH), y, CHAR_WIDTH, LINE_HEIGHT)
            display.update()