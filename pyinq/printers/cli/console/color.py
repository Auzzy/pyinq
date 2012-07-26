"""
Colors text in console mode application (win32).
Uses ctypes and Win32 methods SetConsoleTextAttribute and
GetConsoleScreenBufferInfo.

$Id: color_console.py 534 2009-05-10 04:00:59Z andre $

Refactored and modified by Austin Noto-Moniz.
"""

from ctypes import windll, Structure, c_short, c_ushort, byref

_stdout_handle = windll.kernel32.GetStdHandle(-11)

BLACK = 0x0
BLUE = 0x1
GREEN = 0x2
CYAN = 0x3
RED = 0x4
MAGENTA = 0x5
YELLOW = 0x6
GREY = 0x7

def set_fore(color=GREY, intense=False):
    fore = color | (0x8 if intense else 0x0)
    back = get_back()
    _set_color(fore,back)

def set_back(color=BLACK, intense=False):
    fore = get_fore()
    back = (color*0x10) | (0x80 if intense else 0x0)
    _set_color(fore,back)

def get_back():
    color = _get_color()
    return color-color%0x10

def get_fore():
    color = _get_color()
    return color%0x10


class _Coord(Structure):
    """struct in wincon.h."""
    _fields_ = [("X", c_short),
            ("Y", c_short)]

class _SmallRect(Structure):
    """struct in wincon.h."""
    _fields_ = [("Left", c_short),
            ("Top", c_short),
            ("Right", c_short),
            ("Bottom", c_short)]

class _ConsoleScreenBufferInfo(Structure):
    """struct in wincon.h."""
    _fields_ = [("dwSize", _Coord),
            ("dwCursorPosition", _Coord),
            ("wAttributes", c_ushort),
            ("srWindow", _SmallRect),
            ("dwMaximumWindowSize", _Coord)]

def _get_color():
    """Returns the color of the console screen buffer."""
    csbi = _ConsoleScreenBufferInfo()
    windll.kernel32.GetConsoleScreenBufferInfo(_stdout_handle, byref(csbi))
    return csbi.wAttributes

def _set_color(fore, back):
    """Sets the color of the console screen buffer."""
    windll.kernel32.SetConsoleTextAttribute(_stdout_handle, fore | back)
