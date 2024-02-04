LIBVIRT_ADDR = "qemu:///session"
LIBVIRT_VM_NAME = "archlinux"

INSTANCE_URL = 'https://wetdry.world'

TIME_ANNOUNCEMENT_STRING = "15 minutes"
# TIME_DELAY_AFTER_RUNNING_COMMAND = 15 * 60
TIME_DELAY_AFTER_RUNNING_COMMAND = 30
# TIME_DELAY_AFTER_POSTING_SCREENSHOT = (2 * 3600) - TIME_DELAY_AFTER_RUNNING_COMMAND
TIME_DELAY_AFTER_POSTING_SCREENSHOT = 1
POST_VISIBILITY = "unlisted"



# probably the wrong way to do this. whatever
# https://libvirt.org/manpages/virkeycode-linux.html
char_to_keycode = {
    '1': 2,
    '2': 3,
    '3': 4,
    '4': 5,
    '5': 6,
    '6': 7,
    '7': 8,
    '8': 9,
    '9': 10,
    '0': 11,
    '-': 12,
    '=': 13,
    'q': 16,
    'w': 17,
    'e': 18,
    'r': 19,
    't': 20,
    'y': 21,
    'u': 22,
    'i': 23,
    'o': 24,
    'p': 25,
    '[': 26,
    ']': 27,
    'a': 30,
    's': 31,
    'd': 32,
    'f': 33,
    'g': 34,
    'h': 35,
    'j': 36,
    'k': 37,
    'l': 38,
    ';': 39,
    "'": 40,
    '`': 41,
    '\\': 43,
    'z': 44,
    'x': 45,
    'c': 46,
    'v': 47,
    'b': 48,
    'n': 49,
    'm': 50,
    ',': 51,
    '.': 52,
    '/': 53,
    ' ': 57
}

# Add uppercase characters to the mapping
uppercase_mapping = {
    'A': (42, char_to_keycode['a']), # Shift + a
    'B': (42, char_to_keycode['b']), # Shift + b
    'C': (42, char_to_keycode['c']), # Shift + c
    'D': (42, char_to_keycode['d']), # Shift + d
    'E': (42, char_to_keycode['e']), # Shift + e
    'F': (42, char_to_keycode['f']), # Shift + f
    'G': (42, char_to_keycode['g']), # Shift + g
    'H': (42, char_to_keycode['h']), # Shift + h
    'I': (42, char_to_keycode['i']), # Shift + i
    'J': (42, char_to_keycode['j']), # Shift + j
    'K': (42, char_to_keycode['k']), # Shift + k
    'L': (42, char_to_keycode['l']), # Shift + l
    'M': (42, char_to_keycode['m']), # Shift + m
    'N': (42, char_to_keycode['n']), # Shift + n
    'O': (42, char_to_keycode['o']), # Shift + o
    'P': (42, char_to_keycode['p']), # Shift + p
    'Q': (42, char_to_keycode['q']), # Shift + q
    'R': (42, char_to_keycode['r']), # Shift + r
    'S': (42, char_to_keycode['s']), # Shift + s
    'T': (42, char_to_keycode['t']), # Shift + t
    'U': (42, char_to_keycode['u']), # Shift + u
    'V': (42, char_to_keycode['v']), # Shift + v
    'W': (42, char_to_keycode['w']), # Shift + w
    'X': (42, char_to_keycode['x']), # Shift + x
    'Y': (42, char_to_keycode['y']), # Shift + y
    'Z': (42, char_to_keycode['z'])   # Shift + z
}


# Add non-letter characters that need Shift to the mapping
non_letter_with_shift = {
    '!': (42, char_to_keycode['1']),
    '@': (42, char_to_keycode['2']),
    '#': (42, char_to_keycode['3']),
    '$': (42, char_to_keycode['4']),
    '%': (42, char_to_keycode['5']),
    '^': (42, char_to_keycode['6']),
    '&': (42, char_to_keycode['7']),
    '*': (42, char_to_keycode['8']),
    '(': (42, char_to_keycode['9']),
    ')': (42, char_to_keycode['0']),
    '_': (42, char_to_keycode['-']),
    '+': (42, char_to_keycode['=']),
    '{': (42, char_to_keycode['[']),
    '}': (42, char_to_keycode[']']),
    '|': (42, char_to_keycode['\\']),
    ':': (42, char_to_keycode[';']),
    '"': (42, char_to_keycode["'"]),
    '?': (42, char_to_keycode['/']),
    '>': (42, char_to_keycode['.']),
    '<': (42, char_to_keycode[','])
}

special_keys_mapping = {
    'shift': 42,
    'esc': 1,
    'ctrl': 29,
    'leftctrl': 29,
    'rightctrl': 97,
    'leftshift': 42,
    'rightshift': 54,
    'alt': 56,
    'leftalt': 56,
    'rightalt': 100,
    'up': 103,
    'down': 108,
    'left': 105,
    'right': 106,
    'end': 107,
    'insert': 110,
    'delete': 111,
    'enter': 28,
    'backspace': 14,
    'tab': 15,
    'f1': 59,
    'f2': 60,
    'f3': 61,
    'f4': 62,
    'f5': 63,
    'f6': 64,
    'f7': 65,
    'f8': 66,
    'f9': 67,
    'f10': 68,
    'f11': 87,
    'f12': 88,
    'f13': 183,
    'f14': 184,
    'f15': 185,
    'f16': 186,
    'f17': 187,
    'f18': 188,
    'f19': 189,
    'f20': 190,
    'f21': 191,
    'f22': 192,
    'f23': 193,
    'f24': 194,
    'sysrq': 99,
    'linefeed': 101,
    'home': 102,
    'pageup': 104,
    'pagedown': 109,
    'power': 116,
    'meta': 125,
    'leftmeta': 125,
    'rightmeta': 126,
    'compose': 127,
    'stop': 128
}



# Combine all mappings
char_to_keycode.update(uppercase_mapping)
char_to_keycode.update(non_letter_with_shift)