import machine
import time

from core.terminal_app.terminal import Terminal

# Set up UART (Serial Port)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))  # Adjust pins if needed

terminal = Terminal(uart)
terminal.run()