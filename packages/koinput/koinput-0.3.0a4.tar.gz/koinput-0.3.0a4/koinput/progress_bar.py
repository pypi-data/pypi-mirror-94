import sys


def move(x, y):
    print("\033[%d;%dH" % (y, x))


class ProgressBar:
    def __init__(self):
        pass
