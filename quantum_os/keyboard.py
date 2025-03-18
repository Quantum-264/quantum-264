import quantum_os
from quantum_os.hid_keycodes import get_key_name, get_modifier_name
from collections import deque

class Keyboard:
    def __init__(self):
        self.uart = quantum_os.get_expansion_uart()
        self.keys = bytearray(7)  # Stores last 7-byte HID report
        self.prev_keys = bytearray(7)
        self.pressed_keys = set()
        self.modifier = 0x00
        self.buffer = bytearray(5)

    def update(self):
        """Reads and stores the latest HID report if available."""

        data = self.uart.read(2)

        if not data or len(data) != 2:
            return None  # Invalid packet size
        
        #print as 16-bit binary
        packet = (data[0] << 8) | data[1]  # Combine two bytes into one 16-bit value

        start_bits = (packet >> 13) & 0b111
        action = (packet >> 12) & 0b1
        keycode = (packet >> 4) & 0xFF
        stop_bits = (packet >> 1) & 0b111
        stop_action = packet & 0b1  # Redundant press/release verification

        # Validate packet
        if action != stop_action:
            return None  # Corrupted data

        if start_bits == 0b101 and stop_bits == 0b011:
            # Process key events
            if action:
                self.pressed_keys.add(keycode)
                if self.buffer[-1] != keycode:
                    self.buffer.append(keycode)
                # print("Pressed key: ",get_key_name(keycode))
            else:
                self.pressed_keys.discard(keycode)
                # print("Released key: ", get_key_name(keycode))

            action = "Pressed" if action else "Released"

        elif start_bits == 0b110 and stop_bits == 0b010:
            # Process modifier events
            self.modifier = keycode  # Store new modifier state
            print("Modifier key: ", get_modifier_name(self.modifier))

    def get_keys(self):
        """Returns human-readable key names from currently pressed keycodes."""
        shift = self.modifier & 0x02 or self.modifier & 0x20
        k = [get_key_name(k, shift) for k in self.pressed_keys]
        self.buffer = bytearray(5)
        return k


    def get_modifier(self):
        """Returns a list of active modifier keys."""
        return get_modifier_name(self.modifier)
    
    def get_buffer(self):
        q = [get_key_name(k) for k in self.buffer if k != 0]
        self.buffer = bytearray(5)
        return q


    
    



