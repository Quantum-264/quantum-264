from quantum_os.display import display, COLORS
from quantum_os.constants import CHAR_WIDTH, LINE_HEIGHT

command_list = [
    {"command": "CLEAR", "description": "Clear the screen"},
    {"command": "HELP", "description": "Show this help message"},
    {"command": "APPS", "description": "List available applications"},
    {"command": "COLORS", "description": "Display all colors"},
    {"command": "MEM", "description": "Display memory usage"},
]


def show_colors(x, y):
    for i, color in enumerate(COLORS):
        for _ in range(2):
            display.set_pen(color)

            display.rectangle(x + (i *  CHAR_WIDTH), y, CHAR_WIDTH, LINE_HEIGHT)
            display.update()