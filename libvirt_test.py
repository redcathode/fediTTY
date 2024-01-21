import libvirt
import time
from datetime import datetime

# TODO: DRY!!!


# this is probably the wrong way to do this.
# an LLM wrote these, if you're concerned
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


# Combine all mappings
char_to_keycode.update(uppercase_mapping)
char_to_keycode.update(non_letter_with_shift)

def send_string_to_vm(domain, text):
    for char in text:
        keycode_info = char_to_keycode.get(char)
        print(f"sending keycodes {keycode_info}")
        if keycode_info:
            if isinstance(keycode_info, tuple):
                # Press and hold the Shift key
                domain.sendKey(0, 0, [keycode_info[0], keycode_info[1]], 2)
                time.sleep(0.05)
                # pass
            else:
                # Press the key
                domain.sendKey(0, 0, [keycode_info], 1)
                time.sleep(0.05)
                
def control_key(text):
    conn = libvirt.open('qemu:///system')
    text = text.lower()
    # Find the domain by name
    domain = conn.lookupByName('archlinux')
    keycode_info = char_to_keycode.get(text[0])
    KEY_CTRL = 29
    if keycode_info:
        if isinstance(keycode_info, tuple):
                # Press and hold the Shift key
                domain.sendKey(0, 0, [KEY_CTRL, keycode_info[0], keycode_info[1]], 3)
                time.sleep(0.1)
                # pass
        else:
            # Press the key
            domain.sendKey(0, 0, [KEY_CTRL, keycode_info], 2)
            time.sleep(0.1)
    time.sleep(5)
    conn.close()
                
def run_command(cmd, delayTime=5):
    # Open connection to libvirt
    conn = libvirt.open('qemu:///system')

    # Find the domain by name
    domain = conn.lookupByName('archlinux')

    KEY_ENTER = 28
    print(f"executing cmd {cmd}")
    send_string_to_vm(domain, cmd)
    domain.sendKey(0, 0, [KEY_ENTER], 1)
    time.sleep(delayTime)
    conn.close()
    # return grab_screenshot(conn, domain)
    
def type_text(cmd, delayTime=5):
    # Open connection to libvirt
    conn = libvirt.open('qemu:///system')

    # Find the domain by name
    domain = conn.lookupByName('archlinux')

    print(f"typing {cmd}")
    send_string_to_vm(domain, cmd)
    time.sleep(delayTime)
    conn.close()
    # return grab_screenshot(conn, domain)
    
def hit_enter():
    conn = libvirt.open('qemu:///system')
    domain = conn.lookupByName('archlinux')
    KEY_ENTER = 28
    domain.sendKey(0, 0, [KEY_ENTER], 1)
    time.sleep(5)
    conn.close()
    

def grab_screenshot(conn=None, domain=None):
    if conn is None or domain is None:
        conn = libvirt.open('qemu:///system')
        domain = conn.lookupByName('archlinux')
    
    stream = conn.newStream()

    domain.screenshot(stream, 0)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"feditty-{current_datetime}.png"
    fileHandler = open(filename, 'wb')
    streamBytes = stream.recv(262120)
    while streamBytes != b'':
        fileHandler.write(streamBytes)
        streamBytes = stream.recv(262120)
    fileHandler.close()
    stream.finish()
    conn.close()
    
    return filename
    
    

if __name__ == "__main__":
    pass
    # print(run_command_and_grab_screenshot("echo 'hello world'"))

# Close the connection

