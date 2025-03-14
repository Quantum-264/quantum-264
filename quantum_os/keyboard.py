import quantum_os
from quantum_os.hid_keycodes import get_key_name, get_modifier_name

class Keyboard:
    def __init__(self):
        self.uart = quantum_os.get_expansion_uart()
        self.keys = bytearray(7)  # Stores last 7-byte HID report
        self.prev_keys = bytearray(7)

    def update(self):
        """Reads and stores the latest HID report if available."""
        if self.uart.any() >= 7:  # Ensure full HID report is available
            data = self.uart.read(7)  # Read exactly 7 bytes
            if data and len(data) == 7:
                self.keys[:] = bytearray(data)  # Convert bytes to bytearray
        self.prev_keys[:] = self.keys  # Store previous keys

    def get_keys(self):
        """Returns human-readable key names from keycodes."""
        return [get_key_name(k) for k in self.keys[1:] if k != 0]


    def get_modifier(self):
        """Returns a list of active modifier keys."""
        return get_modifier_name(self.keys[0])
    

    
    



