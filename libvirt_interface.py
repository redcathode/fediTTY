import libvirt
import time
from datetime import datetime
from constants import *

# TODO: DRY!!!

def getconn():
    conn = libvirt.open(LIBVIRT_ADDR)

    # Find the domain by name
    domain = conn.lookupByName(LIBVIRT_VM_NAME)
    return conn, domain

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
    conn, domain = getconn()
    text = text.lower()
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
    conn, domain = getconn()

    KEY_ENTER = 28
    print(f"executing cmd {cmd}")
    send_string_to_vm(domain, cmd)
    domain.sendKey(0, 0, [KEY_ENTER], 1)
    time.sleep(delayTime)
    conn.close()
    # return grab_screenshot(conn, domain)
    
def type_text(cmd, delayTime=5):
    # Open connection to libvirt
    conn, domain = getconn()

    print(f"typing {cmd}")
    send_string_to_vm(domain, cmd)
    time.sleep(delayTime)
    conn.close()
    # return grab_screenshot(conn, domain)
    
def hit_enter():
    conn, domain = getconn()
    KEY_ENTER = 28
    domain.sendKey(0, 0, [KEY_ENTER], 1)
    time.sleep(5)
    conn.close()
    
def key():
    """writes """
    conn, domain = getconn()
    

def grab_screenshot():
    conn, domain = getconn()
    
    stream = conn.newStream()

    domain.screenshot(stream, 0)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"screenshots/feditty-{current_datetime}.png"
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

