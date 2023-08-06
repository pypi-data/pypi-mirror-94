PyTColor: Python Terminal Color
===============================


1.0.0.1
-------

* Added support to python >= 3.0.0


1.0.0.0
-------

PyTColor: A simple python package to get color terminal outputs.

* ``color_print`` can be used to substitute the python ``print`` with keywords ``color``, ``bg_color``, ``style``.
* ``color_print`` is api compatible with python ``print``.
* ``ColoredStreamHandler`` can be used instead of python ``StreamHandler`` in logging to get colored logs.


Dependancies
============

* `python`_>=3.0.0


QuickStart
==========

Installation and Basic Configuration
------------------------------------

1. Install PyTColor: Python Terminal Color by running ``pip install PyTColor``.
2. There is no specific configuration needed to use PyTColor.

.. code:: python

    # color_print
    from pytcolor import color_print
    color_print("PyTColor", color='green', bg_color='red', style='underline', end=' ')
    color_print("Python", "Terminal", color='magenta', bg_color='None', style='underline')
    color_print("Python Terminal Color", color='cyan', bg_color='grey', style='bold')

    # ColoredStreamHandler
    import logging
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)

    ch = ColoredStreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')


Basic Usage
===========

Below are some basic ussage for PyTColor package.

example::

    >>>from pytcolor import color_print
    >>>color_print("PyTColor", color='green', bg_color='red', style='underline', end=' ')
    PyTColor  # \033[4m\033[41m\033[32mPyTColor\033[0m
    >>>from pytcolor.constants import COLORS_NAME, STYLES_NAME
    >>>COLORS_NAME
    ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    >>>STYLES_NAME
    ['bold', 'dark', 'underline', 'blink', 'reverse', 'concealed']
    >>>from pytcolor import ColoredStreamHandler
    >>>class CustomColoredStreamHandler(ColoredStreamHandler):
    ...    def __init__(self, *args, **kwargs):
    ...        super().__init__(*args, **kwargs)  # important to call first
    ...        self._level_color_mapping = {
    ...            "50:*": ("red", None, "underline"),   # critical and above
    ...            "40:50": ("red", None, None),         # error and above till critical but not critical
    ...            "30:40": ("yellow", None, None),      # warning and above till error but not error
    ...            "20:30": ("cyan", None, None),        # info and above till warning but not warning
    ...            "10:20": ("cyan", None, "underline")  # debug and above till info but not info
    ...        }


.. _python: http://python.org
