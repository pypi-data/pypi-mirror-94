# encoding: utf-8

# cody by github@wangjia.net

import ctypes
import sys


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short), ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD), ("wAttributes", ctypes.c_ushort),
                ("srWindow", SMALL_RECT), ("dwMaximumWindowSize", COORD)]


class WinConsole:
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    INVALID_HANDLE_VALUE = -1

    h_console_output = None
    is_run_with_console = False

    def __init__(self):

        if sys.platform != "win32":
            raise EnvironmentError("just for windows")

        self.is_run_with_console = sys.stdout.isatty()
        # another way to detect envrioment:
        # import os
        # self.is_run_with_console = os.isatty(sys.stdin.fileno())

        if not self.is_run_with_console:
            print("-----warn: not run with console-----")

        self.h_console_output = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        if (self.h_console_output == self.INVALID_HANDLE_VALUE) or (self.h_console_output is None):
            raise RuntimeError("GetStdHandle: invalid handle value")

    def get_console_cursor_pos(self):
        if self.is_run_with_console:
            lp_console_screen_buffer_info = CONSOLE_SCREEN_BUFFER_INFO()
            ret = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(self.h_console_output,
                                                                    ctypes.byref(lp_console_screen_buffer_info))
            if ret == 0:
                raise RuntimeError("get_console_cursor_pos")

            return lp_console_screen_buffer_info.dwCursorPosition.X, lp_console_screen_buffer_info.dwCursorPosition.Y
        else:
            return -1, -1

    def set_console_cursor_pos(self, x, y):
        if self.is_run_with_console:
            dw_cursor_position = COORD()
            dw_cursor_position.X = x
            dw_cursor_position.Y = y
            ret = ctypes.windll.kernel32.SetConsoleCursorPosition(self.h_console_output, dw_cursor_position)
            if ret == 0:
                raise RuntimeError("set_console_cursor_pos")

        return
