#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


# Unittest
class TestButton(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        self.button = GLXCurses.Button()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.button)

    def test_text(self):
        self.button.text = None
        self.assertIsNone(self.button.text)
        self.button.text = "Hello.42"
        self.assertEqual("Hello.42", self.button.text)

        self.assertRaises(TypeError, setattr, self.button, "text", 42)

    def test_preferred_width(self):
        self.button.text = "Hello.42"
        self.assertEqual(12, self.button.preferred_width)

    def test_preferred_height(self):
        self.button.text = "Hello.42"
        self.assertEqual(0, self.button.preferred_height)

    def test_interface_normal(self):
        self.button.text = "Test Interface Normal"
        self.button.interface_normal = "|  |"
        self.assertEqual("|  |", self.button.interface_normal)
        self.button.interface_normal = None
        self.assertEqual("[  ]", self.button.interface_normal)

        self.assertRaises(TypeError, setattr, self.button, 'interface_normal', 42)

    def test_interface_selected(self):
        self.button.text = "Test Interface Selected"
        self.button.interface_selected = "|< >|"
        self.assertEqual("|< >|", self.button.interface_selected)
        self.button.interface_selected = None
        self.assertEqual("[<>]", self.button.interface_selected)

        self.assertRaises(TypeError, setattr, self.button, 'interface_selected', 42)

    def test_interface(self):
        self.button.text = "Test Interface"
        self.button.has_focus = None
        self.button.has_default = None

        self.assertEqual("[  ]", self.button.interface)

        self.button.has_focus = True
        self.button.has_default = True
        GLXCurses.Application().has_default = self.button
        self.assertEqual("[<>]", self.button.interface)

        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_default = None
        self.assertEqual("[  ]", self.button.interface)
        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_default = self.button
        self.assertEqual("[<>]", self.button.interface)
        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_default = None
        self.button.has_focus = None
        self.button.has_default = None

    def test_color(self):
        self.button.text = "Test color"
        self.assertEqual(50944, self.button.color)
        self.button.sensitive = False
        self.assertEqual(1099520, self.button.color)
        self.button.sensitive = True
        self.assertEqual(50944, self.button.color)
        self.button.sensitive = True
        self.button.has_prelight = True
        GLXCurses.Application().has_prelight = self.button
        self.assertEqual(296448, self.button.color)

    def test_draw_widget_in_area(self):
        self.button.text = "Test Draw Widget In Area"
        GLXCurses.Application().has_default = self.button
        GLXCurses.Application().has_focus = self.button
        GLXCurses.Application().has_prelight = self.button
        self.button.draw_widget_in_area()
        GLXCurses.Application().has_default = None
        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_prelight = None
        self.button.draw_widget_in_area()


if __name__ == "__main__":
    unittest.main()
