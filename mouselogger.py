from pynput import mouse
import time
import sys

def on_move(x, y):
    print(f'Mouse moved to %d %d'%(x,y))

def on_click(x, y, button, pressed):
    # left/right pressed/released at x, y 
    print('%s %s at %d %d'%('Left' if button is mouse.Button.left else 'Right','pressed' if pressed else 'released',x, y))

def on_scroll(x, y, dx, dy):
    # Scrolled up/down at x, y
    print('Scrolled %s at %d %d'%('up' if dy > 0 else 'down',x, y))

try:
    listener = mouse.Listener(on_move, on_click, on_scroll)
    listener.daemon = True
    listener.start()
    # trick for enabling keyboard interrupt in the code, so the code can be terminated with CTRL + C
    # use signal.pause() in linux, because signal.pause can't be used in windows
    if sys.platform.startswith("win"):
        while True:
            time.sleep(100)
    else:
        import signal
        signal.pause()
    
except (KeyboardInterrupt, SystemExit):
    exit()