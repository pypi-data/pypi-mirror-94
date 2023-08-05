#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


# Unittest
class TestFrame(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.window1 = GLXCurses.Window()
        self.frame = GLXCurses.Frame()
        GLXCurses.Application().add_window(self.window1)
        self.window1.add(self.frame)

    def test_label(self):
        self.frame.label = "Hello.42"
        self.assertEqual("Hello.42", self.frame.label)
        self.assertTrue(isinstance(self.frame.label_widget, GLXCurses.Label))

        self.assertEqual(self.frame.label, self.frame.label_widget.label)
        self.assertEqual(self.frame.label_xalign, self.frame.label_widget.xalign)
        self.assertEqual(self.frame.label_yalign, self.frame.label_widget.yalign)

        self.frame.label = None
        self.assertIsNone(self.frame.label)
        self.assertIsNone(self.frame.label_widget)

        self.assertRaises(TypeError, setattr, self.frame, "label", 42)

    def test_label_widget(self):
        self.frame.label_widget = GLXCurses.Label()
        self.frame.label_widget.text = "Hello.42"
        self.assertTrue(isinstance(self.frame.label_widget, GLXCurses.Label))

        self.frame.label_widget = None
        self.assertIsNone(self.frame.label_widget)

        self.assertRaises(TypeError, setattr, self.frame, "label_widget", 42)

    def test_label_xalign(self):
        self.frame.label = "Test Label X align"
        self.frame.label_xalign = 0.5
        self.assertEqual(self.frame.label_widget.xalign, self.frame.label_xalign)
        self.frame.label_xalign = None
        self.assertEqual(0.0, self.frame.label_xalign)
        self.assertEqual(self.frame.label_widget.xalign, self.frame.label_xalign)

        self.assertRaises(TypeError, setattr, self.frame, "label_xalign", "Hello.42")

    def test_label_yalign(self):
        self.frame.label = "Test Label Y align"
        self.frame.label_yalign = 0.6
        self.assertEqual(self.frame.label_widget.yalign, self.frame.label_yalign)
        self.frame.label_yalign = None
        self.assertEqual(0.5, self.frame.label_yalign)
        self.assertEqual(self.frame.label_widget.yalign, self.frame.label_yalign)

        self.assertRaises(TypeError, setattr, self.frame, "label_yalign", "Hello.42")

    def test_shadow_type(self):
        self.frame.label = "Test shadow type"
        self.frame.shadow_type = None
        self.assertEqual(GLXCurses.GLXC.SHADOW_NONE, self.frame.shadow_type)
        for shadow_type in GLXCurses.GLXC.ShadowType:
            self.frame.shadow_type = shadow_type
            self.assertEqual(shadow_type, self.frame.shadow_type)

        self.assertRaises(TypeError, setattr, self.frame, "shadow_type", 42)

    def test_new(self):
        self.frame = self.frame.new(label="Test New Frame")
        self.assertTrue(isinstance(self.frame, GLXCurses.Frame))
        self.assertEqual("Test New Frame", self.frame.label)
        self.assertEqual("Test New Frame", self.frame.label_widget.label)

    def test_set_get_label(self):
        self.frame.set_label("Hello.42")
        self.assertEqual(self.frame.label, self.frame.get_label())

    def test_set_get_label_widget(self):
        self.frame.set_label_widget(GLXCurses.Label())
        self.assertEqual(self.frame.label_widget, self.frame.get_label_widget())

    def test_set_get_label_align(self):
        self.frame.label = "Test label align"
        self.frame.set_label_align(xalign=0.0, yalign=0.0)
        self.assertEqual(0.0, self.frame.label_xalign)
        self.assertEqual(0.0, self.frame.label_yalign)
        self.assertEqual(0.0, self.frame.label_widget.xalign)
        self.assertEqual(0.0, self.frame.label_widget.yalign)

        self.frame.set_label_align(xalign=0.3, yalign=0.3)
        xalign, yalign = self.frame.get_label_align()
        self.assertEqual(xalign, self.frame.label_xalign)
        self.assertEqual(yalign, self.frame.label_yalign)
        self.assertEqual(0.3, self.frame.label_widget.xalign)
        self.assertEqual(0.3, self.frame.label_widget.yalign)

    def test_set_get_shadow_type(self):
        for shadow_type in GLXCurses.GLXC.ShadowType:
            self.frame.set_shadow_type(shadow_type)
            self.assertEqual(self.frame.get_shadow_type(), self.frame.shadow_type)

    def test_draw_in_area(self):
        self.frame.new("Test Frame Child")
        frame2 = GLXCurses.Frame().new("Child")
        self.frame.add(frame2)
        GLXCurses.Application().refresh()
        self.frame.set_decorated(False)
        GLXCurses.Application().refresh()
        self.frame.set_decorated(True)
        GLXCurses.Application().refresh()


if __name__ == "__main__":
    unittest.main()
