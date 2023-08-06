# -*- coding: utf-8 -*-

__version__ = '0.1.6'
__title__ = 'koinput'
__author__ = 'k0per'
__copyright__ = 'Copyright 2021-present k0per'

import koinput.Menu
from inputs import int_input, float_input
# int_input = __import__('inputs').int_input
# float_input = __import__('inputs').float_input

__all__ = [
    'int_input',
    'float_input',
    'Menu'
]
