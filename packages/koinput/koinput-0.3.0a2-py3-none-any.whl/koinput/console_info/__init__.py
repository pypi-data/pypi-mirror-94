import koinput.console_info.win_console
import koinput.console_info.unix_console


def move(x, y):
    print("\033[%d;%dH" % (y, x))