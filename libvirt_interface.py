import libvirt
import time
from datetime import datetime
from constants import *


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
    
def start_vm_if_not_running():
    conn, domain = getconn()
    if domain.info()[0] != libvirt.VIR_DOMAIN_RUNNING:
        domain.create()
        time.sleep(60) # hack
                
    
def type_text(cmd, delayTime=5):
    # Open connection to libvirt
    conn, domain = getconn()

    print(f"typing {cmd}")
    send_string_to_vm(domain, cmd)
    time.sleep(delayTime)
    conn.close()
    # return grab_screenshot(conn, domain)
    
    
def key(keys):
    conn, domain = getconn()
    keys = keys.replace('+', ' ')
    cmd_list = keys.strip().lower().split()
    cmd_keycodes = []
    for cmd in cmd_list:
        if char_to_keycode.get(cmd):
            cmd_keycodes.append(char_to_keycode.get(cmd))
        elif special_keys_mapping.get(cmd):
            cmd_keycodes.append(special_keys_mapping.get(cmd))
    print(cmd_keycodes)
    domain.sendKey(0, 0, cmd_keycodes, len(cmd_keycodes))
    

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

