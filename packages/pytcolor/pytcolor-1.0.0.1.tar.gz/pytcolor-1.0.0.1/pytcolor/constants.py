#! /usr/bin/env python3
"""This will define the constants for PyTColor package.
"""


# from __future__ import


__all__ = [
    'COLORS_RANGE',
    'COLORS_NAME',
    'BG_COLORS_RANGE',
    'STYLES_RANGE',
    'STYLES_NAME',
    'COLORS_MAPPING',
    'BG_COLORS_MAPPING',
    'STYLES_MAPPING',
    'DEFAULT',
]
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


COLORS_RANGE = range(30, 38)
COLORS_NAME = [
    'grey',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
]

BG_COLORS_RANGE = range(40, 48)
STYLES_RANGE = [1, 2, 4, 5, 7, 8]
STYLES_NAME = [
    'bold',
    'dark',
    #  no style for number 3,
    'underline',
    'blink',
    #  no style for number 6,
    'reverse',
    'concealed'
]

COLORS_MAPPING = dict(
    list(
        zip(
            COLORS_NAME,
            list(COLORS_RANGE)
        )
    )
)

BG_COLORS_MAPPING = dict(
    list(
        zip(
            COLORS_NAME,
            list(BG_COLORS_RANGE)
        )
    )
)

STYLES_MAPPING = dict(
    list(
        zip(
            STYLES_NAME,
            list(STYLES_RANGE)
        )
    )
)

DEFAULT = '\033[0m'

