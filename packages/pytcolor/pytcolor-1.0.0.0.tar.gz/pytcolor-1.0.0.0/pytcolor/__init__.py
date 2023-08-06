#! /usr/bin/env python3
"""This will define the init for PyTColor package.
"""


# from __future__ import


__all__ = [
    'apply_color',
    'color_print',
    'ColoredStreamHandler',
    'COLORS_NAME',
    'STYLES_NAME',
    'DEFAULT',
]
__version__ = '1.0.0.0'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


from .colors import (
    apply_color,
    color_print,
    ColoredStreamHandler,
)

from .constants import (
    COLORS_NAME,
    STYLES_NAME,
    DEFAULT,
)
