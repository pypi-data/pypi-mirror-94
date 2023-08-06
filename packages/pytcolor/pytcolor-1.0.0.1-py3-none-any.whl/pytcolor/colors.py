#! /usr/bin/env python3
"""This will define the functionality code for the PyTColor.
"""


# from __future__ import


__all__ = [
    'apply_color',
    'color_print',
    'ColoredStreamHandler',
]
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import os
import logging

from logging import StreamHandler

from .constants import (
    COLORS_NAME,
    STYLES_NAME,
    DEFAULT,
    STYLES_MAPPING,
    BG_COLORS_MAPPING,
    COLORS_MAPPING,
)


def apply_color(inp: str or list, color=None, bg_color=None, style=None, as_string=True) -> str or list:
    """
    """

    if color not in COLORS_NAME:
        # logging.info("not a valid color so ignoring")
        color = None
    if bg_color not in COLORS_NAME:
        # logging.info("not a valid bg_color so ignoring")
        bg_color = None
    if style not in STYLES_NAME:
        # logging.info("not a valid style so ignoring")
        style = None

    if isinstance(inp, str):
        inp = [inp]

    formats = []
    end = []
    if os.environ.get('ANSI_COLORS_DISABLED', None) is None:
        format_template = '\033[%sm'
        end = [DEFAULT]
        if style is not None:
            formats.append(
                format_template % STYLES_MAPPING[style]
            )
        if bg_color is not None:
            formats.append(
                format_template % BG_COLORS_MAPPING[bg_color]
            )
        if color is not None:
            formats.append(
                format_template % COLORS_MAPPING[color]
            )

        # print("the ret_val = ", ret_val)

    if not as_string:
        ret_val = formats + inp + end
    else:
        ret_val = ''.join(formats) + ' '.join(inp) + ''.join(end)

    return ret_val


def color_print(*args, color=None, bg_color=None, style=None, **kwargs):
    """
    """
    # print_val = apply_color(args, color=color, bg_color=bg_color, style=style)

    print(apply_color(args, color=color, bg_color=bg_color, style=style, as_string=True), **kwargs)


class ColoredStreamHandler(StreamHandler):
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

        self._level_color_mapping = {
            "50:*": ("red", None, "underline"),
            "40:50": ("red", None, None),
            "30:40": ("yellow", None, None),
            "20:30": ("cyan", None, None),
            "10:20": ("cyan", None, "underline")
        }
        self._coloring = (None, None, None)

    def setLevel(self, level):
        ret = super().setLevel(level)
        level = self.level
        coloring = (None, None, None)
        for k in self._level_color_mapping:
            start, end = k.split(':')
            if start == '*':
                start = 0
            if end == '*':
                end = float('inf')

            start = int(start) if isinstance(start, str) else start
            end = int(end) if isinstance(end, str) else end

            if level >= start and level < end:
                coloring = self._level_color_mapping[k]
                break

        self._coloring = coloring
        return ret

    def get_coloring(self, level):
        coloring = (None, None, None)
        for k in self._level_color_mapping:
            start, end = k.split(':')
            if start == '*':
                start = 0
            if end == '*':
                end = float('inf')

            start = int(start) if isinstance(start, str) else start
            end = int(end) if isinstance(end, str) else end

            if level >= start and level < end:
                coloring = self._level_color_mapping[k]
                break

        return coloring

    def emit(self, record):
        """
        """
        # msg = record.getMessage()
        coloring = self.get_coloring(record.levelno)
        # print("The record level = ", record.levelno, coloring)
        msg = record.msg

        msg = apply_color(
            msg,
            color=coloring[0],
            bg_color=coloring[1],
            style=coloring[2]
        )
        record.msg = msg
        record.message = record.getMessage()
        super().emit(record)
