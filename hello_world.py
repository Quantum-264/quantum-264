from modes import VGA
import machine

display = VGA()
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))  # Adjust pins if needed

padding = 25
cursor_x, cursor_y = padding, padding  # Starting position

WHITE = display.create_pen(255, 255, 255)

while True:
    #display.text("Hello World!", 0, 0, 640, 4)
    if uart.any():  # Check if data is available
        char = uart.read(1)  # Read 1 byte
        
        if char:
            display.text(char, cursor_x, cursor_y, 640, 4)
            cursor_x = cursor_x + padding
            if cursor_x > 600:
                cursor_x = padding
                cursor_y = cursor_y + padding
    display.set_pen(WHITE)
    display.update()
