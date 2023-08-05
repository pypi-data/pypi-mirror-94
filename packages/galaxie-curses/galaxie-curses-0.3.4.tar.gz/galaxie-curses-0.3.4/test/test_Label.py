#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


class TestLabel(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.window1 = GLXCurses.Window()
        self.label = GLXCurses.Label()
        GLXCurses.Application().add_window(self.window1)
        self.window1.add(self.label)

    def test_angle(self):

        self.label.angle = 0
        self.assertEqual(0, self.label.angle)
        self.label.angle = 42
        self.assertEqual(42, self.label.angle)
        self.label.angle = None
        self.assertEqual(0, self.label.angle)
        self.assertRaises(TypeError, setattr, self.label, "angle", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "angle", -1)
        self.assertRaises(ValueError, setattr, self.label, "angle", 361)

    def test_attributes(self):
        self.label.attributes = ["Hello.42"]
        self.assertEqual("Hello.42", self.label.attributes[0])
        self.label.attributes = ["Hello.42", "Hello.42"]
        self.assertEqual("Hello.42", self.label.attributes[1])
        self.label.attributes = None
        self.assertEqual([], self.label.attributes)
        self.assertRaises(TypeError, setattr, self.label, "attributes", "Hello.42")

    def test_cursor_position(self):

        self.label.cursor_position = 0
        self.assertEqual(0, self.label.cursor_position)
        self.label.cursor_position = 42
        self.assertEqual(42, self.label.cursor_position)
        self.label.cursor_position = None
        self.assertEqual(0, self.label.cursor_position)
        self.assertRaises(TypeError, setattr, self.label, "cursor_position", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "cursor_position", -1)

    def test_justify(self):
        self.label.justify = None
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_CENTER, self.label.justify)
        for justify in GLXCurses.GLXC.Justification:
            self.label.justify = justify
            self.assertEqual(justify, self.label.justify)
        self.assertRaises(TypeError, setattr, self.label, "justify", 42)

    def test_label(self):
        self.label.label = None
        self.assertEqual("", self.label.label)
        self.label.label = "Hello.42"
        self.assertEqual("Hello.42", self.label.label)
        self.assertRaises(TypeError, setattr, self.label, "label", 42)

    def test_lines(self):
        self.label.lines = None
        self.assertEqual(-1, self.label.lines)
        self.label.lines = 42
        self.assertEqual(42, self.label.lines)
        self.label.lines = None
        self.assertEqual(-1, self.label.lines)
        self.assertRaises(TypeError, setattr, self.label, "lines", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "lines", -2)

    def test_max_width_chars(self):
        self.label.max_width_chars = None
        self.assertEqual(-1, self.label.max_width_chars)
        self.label.max_width_chars = 42
        self.assertEqual(42, self.label.max_width_chars)
        self.label.max_width_chars = None
        self.assertEqual(-1, self.label.max_width_chars)
        self.assertRaises(TypeError, setattr, self.label, "max_width_chars", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "max_width_chars", -2)

    def test_mnemonic_keyval(self):
        self.label.mnemonic_keyval = None
        self.assertEqual(16777215, self.label.mnemonic_keyval)
        self.label.mnemonic_keyval = 42
        self.assertEqual(42, self.label.mnemonic_keyval)
        self.label.mnemonic_keyval = None
        self.assertEqual(16777215, self.label.mnemonic_keyval)
        self.assertRaises(TypeError, setattr, self.label, "mnemonic_keyval", "Hello.42")

    def test_mnemonic_widget(self):
        self.label.mnemonic_widget = None
        self.assertIsNone(self.label.mnemonic_widget)
        self.label.mnemonic_widget = GLXCurses.Widget()
        self.assertTrue(isinstance(self.label.mnemonic_widget, GLXCurses.Widget))
        self.label.mnemonic_widget = None
        self.assertIsNone(self.label.mnemonic_widget)
        self.assertRaises(TypeError, setattr, self.label, "mnemonic_widget", "Hello.42")

    def test_pattern(self):
        self.label.pattern = None
        self.assertIsNone(self.label.pattern)
        self.label.pattern = "#"
        self.assertEqual("#", self.label.pattern)
        self.label.pattern = None
        self.assertIsNone(self.label.pattern)
        self.assertRaises(TypeError, setattr, self.label, "pattern", 42)

    def test_selectable(self):
        self.label.selectable = None
        self.assertFalse(self.label.selectable)
        self.label.selectable = True
        self.assertTrue(self.label.selectable)
        self.label.selectable = False
        self.assertFalse(self.label.selectable)
        self.assertRaises(TypeError, setattr, self.label, "selectable", 42)

    def test_selection_bound(self):
        self.label.selection_bound = None
        self.assertEqual(0, self.label.selection_bound)
        self.label.selection_bound = 42
        self.assertEqual(42, self.label.selection_bound)
        self.label.selection_bound = None
        self.assertEqual(0, self.label.selection_bound)
        self.assertRaises(TypeError, setattr, self.label, "selection_bound", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "selection_bound", -42)

    def test_single_line_mode(self):
        self.label.single_line_mode = None
        self.assertFalse(self.label.single_line_mode)
        self.label.single_line_mode = True
        self.assertTrue(self.label.single_line_mode)
        self.label.single_line_mode = False
        self.assertFalse(self.label.single_line_mode)
        self.assertRaises(
            TypeError, setattr, self.label, "single_line_mode", "Hello.42"
        )

    def test_track_visited_links(self):
        self.label.track_visited_links = None
        self.assertTrue(self.label.track_visited_links)
        self.label.track_visited_links = False
        self.assertFalse(self.label.track_visited_links)
        self.label.track_visited_links = True
        self.assertTrue(self.label.track_visited_links)
        self.assertRaises(
            TypeError, setattr, self.label, "track_visited_links", "Hello.42"
        )

    def test_use_markdown(self):
        self.label.use_markdown = None
        self.assertFalse(self.label.use_markdown)
        self.label.use_markdown = False
        self.assertFalse(self.label.use_markdown)
        self.label.use_markdown = True
        self.assertTrue(self.label.use_markdown)
        self.assertRaises(TypeError, setattr, self.label, "use_markdown", "Hello.42")

    def test_use_underline(self):
        self.label.use_underline = None
        self.assertFalse(self.label.use_underline)
        self.label.use_underline = False
        self.assertFalse(self.label.use_underline)
        self.label.use_underline = True
        self.assertTrue(self.label.use_underline)
        self.assertRaises(TypeError, setattr, self.label, "use_underline", "Hello.42")

    def test_width_chars(self):
        self.label.width_chars = None
        self.assertEqual(-1, self.label.width_chars)
        self.label.width_chars = 42
        self.assertEqual(42, self.label.width_chars)
        self.label.width_chars = -1
        self.assertEqual(-1, self.label.width_chars)
        self.assertRaises(TypeError, setattr, self.label, "width_chars", "Hello.42")
        self.assertRaises(ValueError, setattr, self.label, "width_chars", -42)

    def test_wrap(self):
        self.label.wrap = None
        self.assertFalse(self.label.wrap)
        self.label.wrap = False
        self.assertFalse(self.label.wrap)
        self.label.wrap = True
        self.assertTrue(self.label.wrap)
        self.assertRaises(TypeError, setattr, self.label, "wrap", "Hello.42")

    def test_wrap_mode(self):
        self.label.wrap_mode = None
        self.assertEqual(GLXCurses.GLXC.WRAP_WORD, self.label.wrap_mode)
        for mode in GLXCurses.GLXC.WrapMode:
            self.label.wrap_mode = mode
            self.assertEqual(mode, self.label.wrap_mode)
        self.label.wrap_mode = GLXCurses.GLXC.WRAP_WORD
        self.assertEqual(GLXCurses.GLXC.WRAP_WORD, self.label.wrap_mode)
        self.assertRaises(TypeError, setattr, self.label, "wrap_mode", 42)
        self.assertRaises(ValueError, setattr, self.label, "wrap_mode", "Hello.42")

    def test_new(self):
        label = self.label.new()
        self.assertEqual("", label.label)
        label = self.label.new("Test GLXCurses.Label.new()")
        self.assertEqual("Test GLXCurses.Label.new()", label.label)
        label = self.label.new(None)
        self.assertEqual("", label.label)

    def test_set_text(self):
        self.label.set_text(None)
        self.label.set_text("Test GLXCurses.Label.set_text()")
        self.label.use_markdown = True
        self.label.use_underline = True
        self.label.mnemonic_keyval = 42
        self.label.mnemonic_widget = GLXCurses.Widget()
        self.assertEqual("Test GLXCurses.Label.set_text()", self.label.label)
        self.assertTrue(self.label.use_markdown)
        self.assertTrue(self.label.use_underline)
        self.assertEqual(42, self.label.mnemonic_keyval)
        self.assertTrue(isinstance(self.label.mnemonic_widget, GLXCurses.Widget))
        self.label.set_text("Test GLXCurses.Label.set_text()")
        self.assertEqual("Test GLXCurses.Label.set_text()", self.label.label)
        self.assertFalse(self.label.use_markdown)
        self.assertFalse(self.label.use_underline)
        self.assertEqual(16777215, self.label.mnemonic_keyval)
        self.assertIsNone(self.label.mnemonic_widget)

    def test_set_attributes(self):
        attributes = ["Hello.42"]
        self.label.set_attributes(attributes=attributes)
        self.assertEqual("Hello.42", self.label.attributes[0])

    def test_set_markdown(self):
        self.label.label = None
        self.label.use_markdown = False
        self.label.set_markdown("**P** _k_ ++t++ ++***W***++")
        self.assertEqual("P k t W", self.label.get_text())
        self.assertTrue(self.label.attributes[0]["HIDDEN"])
        self.assertTrue(self.label.attributes[1]["HIDDEN"])
        self.assertFalse(self.label.attributes[2]["HIDDEN"])
        self.assertTrue(self.label.attributes[2]["A_BOLD"])
        self.assertTrue(self.label.attributes[3]["HIDDEN"])
        self.assertTrue(self.label.attributes[4]["HIDDEN"])
        self.assertFalse(self.label.attributes[5]["HIDDEN"])
        self.assertTrue(self.label.attributes[6]["HIDDEN"])
        self.assertFalse(self.label.attributes[7]["HIDDEN"])
        self.assertTrue(self.label.attributes[7]["A_ITALIC"])
        self.assertFalse(self.label.attributes[7]["A_BOLD"])
        self.assertTrue(self.label.attributes[8]["HIDDEN"])
        self.assertFalse(self.label.attributes[9]["HIDDEN"])
        self.assertTrue(self.label.attributes[10]["HIDDEN"])

    def test_set_markdown_with_mnemonic(self):
        self.label.label = None
        self.label.use_markdown = False
        self.label.use_underline = True
        self.label.set_markdown_with_mnemonic("**_P** *k* ++t++ ++***W***++")
        self.assertEqual("**_P** *k* ++t++ ++***W***++", self.label.label)
        self.assertEqual("P", chr(self.label.mnemonic_keyval))
        self.assertEqual("P k t W", self.label.get_text())
        self.assertTrue(self.label.attributes[0]["HIDDEN"])
        self.assertTrue(self.label.attributes[1]["HIDDEN"])
        self.assertTrue(self.label.attributes[2]["HIDDEN"])
        self.assertTrue(self.label.attributes[3]["A_BOLD"])
        self.assertFalse(self.label.attributes[3]["HIDDEN"])
        self.assertTrue(self.label.attributes[4]["HIDDEN"])
        self.assertTrue(self.label.attributes[5]["HIDDEN"])
        self.assertFalse(self.label.attributes[6]["HIDDEN"])
        self.assertTrue(self.label.attributes[7]["HIDDEN"])
        self.assertFalse(self.label.attributes[8]["HIDDEN"])
        self.assertFalse(self.label.attributes[8]["A_BOLD"])
        self.assertTrue(self.label.attributes[8]["A_ITALIC"])
        self.assertTrue(self.label.attributes[9]["HIDDEN"])
        self.assertFalse(self.label.attributes[10]["HIDDEN"])

    def test_set_pattern(self):
        self.label.label = "Test set_pattern()"
        self.label.set_pattern(pattern="___ ___")
        self.assertEqual("___ ___", self.label.pattern)

    def test_set_justify(self):
        self.label.label = "Test set_justify()"
        self.label.set_justify(GLXCurses.GLXC.JUSTIFY_LEFT)
        self.assertEqual(self.label.justify, GLXCurses.GLXC.JUSTIFY_LEFT)

        self.label.set_justify(GLXCurses.GLXC.JUSTIFY_RIGHT)
        self.assertEqual(self.label.justify, GLXCurses.GLXC.JUSTIFY_RIGHT)

        self.label.set_justify(GLXCurses.GLXC.JUSTIFY_CENTER)
        self.assertEqual(self.label.justify, GLXCurses.GLXC.JUSTIFY_CENTER)

    def test_set_xalign(self):
        self.label.label = "Test set_xalign()"
        self.label.set_xalign(0.1)
        self.assertEqual(self.label.xalign, 0.1)
        self.label.set_xalign(0.5)
        self.assertEqual(self.label.xalign, 0.5)
        self.label.set_xalign(0.1)
        self.assertEqual(self.label.xalign, 0.1)
        self.label.set_xalign(None)
        self.assertEqual(self.label.xalign, 0.5)

    def test_set_yalign(self):
        self.label.label = "Test set_yalign()"
        self.label.set_yalign(0.1)
        self.assertEqual(self.label.yalign, 0.1)
        self.label.set_yalign(0.5)
        self.assertEqual(self.label.yalign, 0.5)
        self.label.set_yalign(0.1)
        self.assertEqual(self.label.yalign, 0.1)
        self.label.set_yalign(None)
        self.assertEqual(self.label.yalign, 0.5)

    def test_set_width_chars(self):
        self.label.label = "Test set_width_chars()"
        self.label.set_width_chars(5)
        self.assertEqual(self.label.width_chars, 5)

        self.label.set_width_chars(None)
        self.assertEqual(self.label.width_chars, -1)

    def test_set_max_width_chars(self):
        self.label.label = "Test set_max_width_chars()"
        self.label.set_max_width_chars(5)
        self.assertEqual(self.label.max_width_chars, 5)

        self.label.set_max_width_chars(None)
        self.assertEqual(self.label.max_width_chars, -1)

    def test_set_line_wrap(self):
        self.label.label = "Test set_line_wrap()"
        self.label.set_line_wrap(False)
        self.assertFalse(self.label.wrap)
        self.label.set_line_wrap(True)
        self.assertTrue(self.label.wrap)
        self.label.set_line_wrap(None)
        self.assertFalse(self.label.wrap)

    def test_set_line_wrap_mode(self):
        self.label.label = "Test set_line_wrap_mode()"
        for wrap_mode in GLXCurses.GLXC.WrapMode:
            self.label.set_line_wrap_mode(wrap_mode)
            self.assertEqual(wrap_mode, self.label.wrap_mode)

    def test_set_lines(self):
        self.label.label = "Test set_lines()"
        self.label.set_lines(None)
        self.assertEqual(-1, self.label.lines)
        self.label.set_lines(42)
        self.assertEqual(42, self.label.lines)
        self.label.set_lines(None)
        self.assertEqual(-1, self.label.lines)

    def test_get_set_mnemonic_keyval(self):
        self.label.set_text_with_mnemonic("_Hello.42")
        self.assertEqual(72, self.label.get_mnemonic_keyval())
        self.label.set_text_with_mnemonic("Hello._42")
        self.assertEqual(52, self.label.get_mnemonic_keyval())

    def test_get_set_selectable(self):
        self.label.label = "Test get_selectable()"
        self.label.set_selectable(None)
        self.assertFalse(self.label.get_selectable())
        self.label.set_selectable(True)
        self.assertTrue(self.label.get_selectable())
        self.label.set_selectable()
        self.assertFalse(self.label.get_selectable())

    def test_get_text(self):
        self.label.set_markdown_with_mnemonic("**_42**")
        self.assertEqual("42", self.label.get_text())

    def test_Label_get_justify(self):
        label = GLXCurses.Label()
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_LEFT, label.get_justify())

        label.justify = GLXCurses.GLXC.JUSTIFY_RIGHT
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_RIGHT, label.get_justify())

    def test_Label_set_justify(self):
        label = GLXCurses.Label()

        self.assertEqual(GLXCurses.GLXC.JUSTIFY_LEFT, label.justify)

        for justify in GLXCurses.GLXC.Justification:
            label.set_justify(justify)
            self.assertEqual(justify, label.justify)

        self.assertRaises(ValueError, label.set_justify, "Hello")

    def test_Label_get_line_wrap(self):
        """Test Label.get_line_wrap()"""
        label = GLXCurses.Label()
        self.assertEqual(False, label.get_line_wrap())

        label.wrap = True
        self.assertEqual(True, label.get_line_wrap())

    def test_Label_set_line_wrap(self):
        """Test Label.set_line_wrap()"""
        label = GLXCurses.Label()
        self.assertEqual(False, label.wrap)

        label.set_line_wrap(True)
        self.assertEqual(True, label.wrap)

        self.assertRaises(TypeError, label.set_line_wrap, "Hello")

    def test_Label_get_width_chars(self):
        """Test Label.get_width_chars()"""
        label = GLXCurses.Label()
        self.assertEqual(-1, label.get_width_chars())

        label.width_chars = 42
        self.assertEqual(42, label.get_width_chars())

    def test_Label_set_width_chars(self):
        """Test Label.set_width_chars()"""
        label = GLXCurses.Label()
        self.assertEqual(-1, label.width_chars)

        label.set_width_chars(42)
        self.assertEqual(42, label.width_chars)

        self.assertRaises(TypeError, label.set_width_chars, "Hello")


if __name__ == "__main__":
    unittest.main()
