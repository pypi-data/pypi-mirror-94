import os
import sys
import msvcrt

KEYBOARD_KEYS = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0'
]

KEYBOARD_KEYS_VALUE = [
    b'a',
    b'b',
    b'c',
    b'd',
    b'e',
    b'f',
    b'g',
    b'h',
    b'i',
    b'j',
    b'k',
    b'l',
    b'm',
    b'n',
    b'o',
    b'p',
    b'q',
    b'r',
    b's',
    b't',
    b'u',
    b'v',
    b'w',
    b'x',
    b'y',
    b'z',
    b'1',
    b'2',
    b'3',
    b'4',
    b'5',
    b'6',
    b'7',
    b'8',
    b'9',
    b'0'
]

class keyboard():
    def getCurrentKey():
        code = msvcrt.getch()

        if code in KEYBOARD_KEYS_VALUE:
            index = KEYBOARD_KEYS_VALUE.index(code)
            code = KEYBOARD_KEYS[index]

        return code

    def isKey(key):
        key = str(key)
        key = key.lower

        code = msvcrt.getch()
        status = False

        if code in KEYBOARD_KEYS_VALUE:
            index = KEYBOARD_KEYS_VALUE.index(code)
            code = KEYBOARD_KEYS[index]

        if key == code:
            status = True
        else:
            status = False

        return status