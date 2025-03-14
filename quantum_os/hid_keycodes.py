"""
USB HID Keyboard scan codes based on USB HID Specification 1.11.
Includes standard keys, media keys, function keys, and keypad keys.

Adapted for MicroPython.
"""  

# Modifier Key Masks
MODIFIER_KEYS = {
    0x01: "Left Ctrl",
    0x02: "Left Shift",
    0x04: "Left Alt",
    0x08: "Left GUI",
    0x10: "Right Ctrl",
    0x20: "Right Shift",
    0x40: "Right Alt",
    0x80: "Right GUI",
}

# HID Keycodes (USB Standard 1.11)
KEYCODES = {
    # Letters
    0x04: "A", 0x05: "B", 0x06: "C", 0x07: "D", 0x08: "E", 0x09: "F", 0x0A: "G", 0x0B: "H",
    0x0C: "I", 0x0D: "J", 0x0E: "K", 0x0F: "L", 0x10: "M", 0x11: "N", 0x12: "O", 0x13: "P",
    0x14: "Q", 0x15: "R", 0x16: "S", 0x17: "T", 0x18: "U", 0x19: "V", 0x1A: "W", 0x1B: "X",
    0x1C: "Y", 0x1D: "Z",

    # Numbers
    0x1E: "1", 0x1F: "2", 0x20: "3", 0x21: "4", 0x22: "5", 0x23: "6", 0x24: "7", 0x25: "8",
    0x26: "9", 0x27: "0",

    # Special Keys
    0x28: "Enter", 0x29: "Esc", 0x2A: "Backspace", 0x2B: "Tab", 0x2C: "Space",
    0x2D: "-", 0x2E: "=", 0x2F: "[", 0x30: "]", 0x31: "\\", 0x32: "#", 0x33: ";", 0x34: "'",
    0x35: "`", 0x36: ",", 0x37: ".", 0x38: "/",

    # Function Keys
    0x39: "Caps Lock", 0x3A: "F1", 0x3B: "F2", 0x3C: "F3", 0x3D: "F4", 0x3E: "F5",
    0x3F: "F6", 0x40: "F7", 0x41: "F8", 0x42: "F9", 0x43: "F10", 0x44: "F11", 0x45: "F12",
    0x46: "Print Screen", 0x47: "Scroll Lock", 0x48: "Pause",

    # Navigation Keys
    0x49: "Insert", 0x4A: "Home", 0x4B: "Page Up", 0x4C: "Delete", 0x4D: "End",
    0x4E: "Page Down", 0x4F: "Right Arrow", 0x50: "Left Arrow", 0x51: "Down Arrow",
    0x52: "Up Arrow",

    # Keypad
    0x53: "Num Lock", 0x54: "Keypad /", 0x55: "Keypad *", 0x56: "Keypad -", 0x57: "Keypad +",
    0x58: "Keypad Enter", 0x59: "Keypad 1", 0x5A: "Keypad 2", 0x5B: "Keypad 3",
    0x5C: "Keypad 4", 0x5D: "Keypad 5", 0x5E: "Keypad 6", 0x5F: "Keypad 7",
    0x60: "Keypad 8", 0x61: "Keypad 9", 0x62: "Keypad 0", 0x63: "Keypad .",
    0x85: "Keypad Comma", 0xB6: "Keypad (", 0xB7: "Keypad )",

    # Extended Function Keys
    0x68: "F13", 0x69: "F14", 0x6A: "F15", 0x6B: "F16", 0x6C: "F17", 0x6D: "F18",
    0x6E: "F19", 0x6F: "F20", 0x70: "F21", 0x71: "F22", 0x72: "F23", 0x73: "F24",

    # Extra Function Keys
    0x74: "Execute", 0x75: "Help", 0x76: "Menu", 0x77: "Select", 0x78: "Stop",
    0x79: "Again", 0x7A: "Undo", 0x7B: "Cut", 0x7C: "Copy", 0x7D: "Paste",
    0x7E: "Find", 0x7F: "Mute", 0x80: "Volume Up", 0x81: "Volume Down",

    # International Keys
    0x87: "International 1 (RO)", 0x88: "International 2 (Katakana/Hiragana)",
    0x89: "International 3 (Yen)", 0x8A: "International 4 (Henkan)",
    0x8B: "International 5 (Muhenkan)", 0x8C: "International 6 (KPJPComma)",

    # Language Keys
    0x90: "LANG1 (Hangeul)", 0x91: "LANG2 (Hanja)", 0x92: "LANG3 (Katakana)",
    0x93: "LANG4 (Hiragana)", 0x94: "LANG5 (Zenkaku/Hankaku)",

    # Media Keys
    0xE8: "Media Play/Pause", 0xE9: "Media Stop", 0xEA: "Media Previous",
    0xEB: "Media Next", 0xEC: "Media Eject", 0xED: "Volume Up", 0xEE: "Volume Down",
    0xEF: "Media Mute", 0xF0: "Media WWW", 0xF1: "Media Back",
    0xF2: "Media Forward", 0xF3: "Media Stop", 0xF4: "Media Find",
    0xF5: "Media Scroll Up", 0xF6: "Media Scroll Down",
    0xF7: "Media Edit", 0xF8: "Media Sleep", 0xF9: "Media Coffee",
    0xFA: "Media Refresh", 0xFB: "Media Calculator",
}

def get_key_name(hid_code):
    """Returns the key name for a given HID keycode."""
    return KEYCODES.get(hid_code, f"Unknown(0x{hid_code:02X})")

def get_modifier_name(modifier_byte):
    """Returns a list of modifier key names from a modifier byte."""
    return [name for bit, name in MODIFIER_KEYS.items() if modifier_byte & bit]
