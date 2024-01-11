# PUP that saves screenshots to disk every 15 seconds
from PIL import ImageGrab
from threading import Thread
from sys import exit
import time


def take_screenshot():
    while True:
        print('taking screenshot')
        image = ImageGrab.grab()
        now = time.strftime("%d-%m-%Y" + ' ' + "%H-%M-%S")
        image.save(now + '.png')
        time.sleep(15)


def main():
    try:
        thread1 = Thread(target=take_screenshot, args=(), daemon=True)
        thread1.start()
        thread1.join()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
