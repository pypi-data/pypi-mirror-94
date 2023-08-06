#! /usr/bin/env python3
"""This module tests the apply_color functionality
"""


__all__ = [
    'TestApplyColorSuite',
]
__version__ = '1.0.0.1'
__author__ = 'Midhun C Nair <midhunch@gmail.com>'
__maintainers__ = [
    'Midhun C Nair <midhunch@gmail.com>',
]


import unittest
from pytcolor import apply_color


class TestApplyColorSuite(unittest.TestCase):
    """
    """
    # text color
    def test_str_input_with_right_color(self):
        out = apply_color('PyTColor', color='red')
        self.assertEqual(out, '\033[31mPyTColor\033[0m')

    def test_list_input_with_right_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='red')
        self.assertEqual(
            out,
            '\033[31mPython Terminal Color\033[0m'
        )

    def test_str_input_with_wrong_color(self):
        out = apply_color('PyTColor', color='123test123')
        self.assertEqual(out, 'PyTColor\033[0m')

    def test_list_input_with_wrong_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='123test123')
        self.assertEqual(
            out,
            'Python Terminal Color\033[0m'
        )

    # bg_color
    def test_str_input_with_right_bg_color(self):
        out = apply_color('PyTColor', bg_color='red')
        self.assertEqual(out, '\033[41mPyTColor\033[0m')

    def test_list_input_with_right_bg_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], bg_color='red')
        self.assertEqual(
            out,
            '\033[41mPython Terminal Color\033[0m'
        )

    def test_str_input_with_wrong_bg_color(self):
        out = apply_color('PyTColor', bg_color='123test123')
        self.assertEqual(out, 'PyTColor\033[0m')

    def test_list_input_with_wrong_bg_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], bg_color='123test123')
        self.assertEqual(
            out,
            'Python Terminal Color\033[0m'
        )

    # style
    def test_str_input_with_right_style(self):
        out = apply_color('PyTColor', style='underline')
        self.assertEqual(out, '\033[4mPyTColor\033[0m')

    def test_list_input_with_right_style(self):
        out = apply_color(['Python', 'Terminal', 'Color'], style='underline')
        self.assertEqual(
            out,
            '\033[4mPython Terminal Color\033[0m'
        )

    def test_str_input_with_wrong_style(self):
        out = apply_color('PyTColor', style='123test123')
        self.assertEqual(out, 'PyTColor\033[0m')

    def test_list_input_with_wrong_style(self):
        out = apply_color(['Python', 'Terminal', 'Color'], style='123test123')
        self.assertEqual(
            out,
            'Python Terminal Color\033[0m'
        )

    # color bg_color and style
    def test_str_input_with_right_all(self):
        out = apply_color('PyTColor', color='red', bg_color='green', style='underline')
        self.assertEqual(out, '\033[4m\033[42m\033[31mPyTColor\033[0m')

    def test_list_input_with_right_all(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='red', bg_color='green', style='underline')
        self.assertEqual(
            out,
            '\033[4m\033[42m\033[31mPython Terminal Color\033[0m'
        )

    def test_str_input_with_wrong_all(self):
        out = apply_color('PyTColor', color='123', bg_color='test', style='123')
        self.assertEqual(out, 'PyTColor\033[0m')

    def test_list_input_with_wrong_all(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='123', bg_color='test', style='123')
        self.assertEqual(
            out,
            'Python Terminal Color\033[0m'
        )

    def test_str_input_with_all_wrong_style(self):
        out = apply_color('PyTColor', color='red', bg_color='green', style='123')
        self.assertEqual(out, '\033[42m\033[31mPyTColor\033[0m')

    def test_list_input_with_all_wrong_style(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='red', bg_color='green', style='123')
        self.assertEqual(
            out,
            '\033[42m\033[31mPython Terminal Color\033[0m'
        )

    def test_str_input_with_all_wrong_bg_color(self):
        out = apply_color('PyTColor', color='red', bg_color='123', style='underline')
        self.assertEqual(out, '\033[4m\033[31mPyTColor\033[0m')

    def test_list_input_with_all_wrong_bg_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='red', bg_color='123', style='underline')
        self.assertEqual(
            out,
            '\033[4m\033[31mPython Terminal Color\033[0m'
        )

    def test_str_input_with_all_wrong_color(self):
        out = apply_color('PyTColor', color='123', bg_color='green', style='underline')
        self.assertEqual(out, '\033[4m\033[42mPyTColor\033[0m')

    def test_list_input_with_all_wrong_color(self):
        out = apply_color(['Python', 'Terminal', 'Color'], color='123', bg_color='green', style='underline')
        self.assertEqual(
            out,
            '\033[4m\033[42mPython Terminal Color\033[0m'
        )
