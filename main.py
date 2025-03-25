import quantum_os
import quantum_os.terminal as terminal_app
from quantum_os.display import *
from quantum_os.utils import *
import sys
import io

try:
    quantum_os.boot(terminal_app.App)

except Exception as e:
    # Capture full traceback to string
    buf = io.StringIO()
    sys.print_exception(e, buf)
    traceback_text = buf.getvalue()

    # log to file
    with open("sd/error.log", "w") as f:
        f.write(traceback_text)

    # Clear screen
    for _ in range(2):
        display.clear()
        display.set_pen(BG_COLOR)
        display.rectangle(0, 0, WIDTH, HEIGHT)
        display.update()

    # Display error header
    write_text_double_buffer("ERROR", COLORS[4], y=DEFAULT_CURSOR_Y)

    # Display traceback
    lines = traceback_text.splitlines()
    y = DEFAULT_CURSOR_Y + LINE_HEIGHT

    for line in lines:
        write_text_double_buffer(line, TEXT_COLOR, y=y)
        y += LINE_HEIGHT
        if y + LINE_HEIGHT >= HEIGHT:
            # If we run out of space, stop writing
            # Optional: clear + page forward or scroll
            break

    display.update()
