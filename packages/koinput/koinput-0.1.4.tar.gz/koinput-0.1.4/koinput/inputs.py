import sys
from colorama import Fore


def int_input(input_suggestion='', greater=float('-inf'), less=float('inf'), console_colour=Fore.RESET,
              error_message='Неверный формат числа.\n', error_message_colour=Fore.RED,
              input_is_greater_than_less_error="Число больше допустимого.\n",
              input_is_less_than_greater_error="Число меньше допустимого.\n",
              input_is_less_error_colour=None, input_is_greater_error_colour=None,
              strictly_greater=True, strictly_less=True):
    if input_is_less_error_colour is None:
        input_is_less_error_colour = error_message_colour
    if input_is_greater_error_colour is None:
        input_is_greater_error_colour = error_message_colour
    while True:
        try:
            sys.stdout.write(input_suggestion)
            introduced = int(input().split()[0])
            if introduced <= greater and strictly_greater:
                sys.stdout.write(input_is_greater_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_less_than_greater_error + console_colour)
            elif introduced < greater and not strictly_greater:
                sys.stdout.write(input_is_greater_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_less_than_greater_error + console_colour)
            elif introduced >= less and strictly_less:
                sys.stdout.write(input_is_less_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_greater_than_less_error + console_colour)
            elif introduced > less and not strictly_less:
                sys.stdout.write(input_is_less_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_greater_than_less_error + console_colour)
            else:
                return introduced
        except:
            sys.stdout.write(error_message_colour)
            sys.stdout.write('     \r')
            sys.stdout.write(error_message + console_colour)


def float_input(input_suggestion='', greater=float('-inf'), less=float('inf'), console_colour=Fore.RESET,
                error_message='Неверный формат числа.\n', error_message_colour=Fore.RED,
                input_is_greater_than_less_error="Число больше допустимого.\n",
                input_is_less_than_greater_error="Число меньше допустимого.\n",
                input_is_less_error_colour=None, input_is_greater_error_colour=None,
                strictly_greater=True, strictly_less=True):
    if input_is_less_error_colour is None:
        input_is_less_error_colour = error_message_colour
    if input_is_greater_error_colour is None:
        input_is_greater_error_colour = error_message_colour
    while True:
        try:
            sys.stdout.write(input_suggestion)
            introduced = float(input().split()[0])
            if introduced <= greater and strictly_greater:
                sys.stdout.write(input_is_greater_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_less_than_greater_error + console_colour)
            elif introduced < greater and not strictly_greater:
                sys.stdout.write(input_is_greater_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_less_than_greater_error + console_colour)
            elif introduced >= less and strictly_less:
                sys.stdout.write(input_is_less_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_greater_than_less_error + console_colour)
            elif introduced > less and not strictly_less:
                sys.stdout.write(input_is_less_error_colour)
                sys.stdout.write('     \r')
                sys.stdout.write(input_is_greater_than_less_error + console_colour)
            else:
                return introduced
        except:
            sys.stdout.write(error_message_colour)
            sys.stdout.write('     \r')
            sys.stdout.write(error_message + console_colour)


