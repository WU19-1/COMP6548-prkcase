from pynput import mouse

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
    listener.start()
    listener.join()
except KeyboardInterrupt:
    exit()