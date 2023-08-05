#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import os
import curses
import GLXCurses

term = os.environ.get("TERM")


# Unittest
class TestWindow(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.window1 = GLXCurses.Window()
        self.window2 = GLXCurses.Window()
        GLXCurses.Application().add_window(self.window1)
        self.window1.add(self.window2)

    # Test Property
    def test_accept_focus(self):
        self.assertTrue(self.window1.accept_focus)
        self.window1.accept_focus = False
        self.assertFalse(self.window1.accept_focus)
        self.assertRaises(TypeError, setattr, self.window1, "accept_focus", None)

    def test_application(self):
        window = GLXCurses.Window()
        self.assertIsNone(window.application)
        window.application = GLXCurses.Application()
        self.assertEqual(GLXCurses.Application(), window.application)

        self.assertRaises(TypeError, setattr, window, "application", 42)

    def test_attached_to(self):

        self.window1.attached_to = self.window2
        self.assertEqual(self.window2, self.window1.attached_to)

        self.window1.attached_to = None
        self.assertEqual(None, self.window1.attached_to)

        self.assertRaises(TypeError, setattr, self.window1, "attached_to", 42)

    def test_decorated(self):
        self.assertFalse(self.window1.decorated)

        self.window1.decorated = True
        self.assertTrue(self.window1.decorated)

        self.assertRaises(TypeError, setattr, self.window1, "decorated", None)

    def test_default_height(self):
        self.assertEqual(0, self.window1.default_height)
        self.window1.default_height = None
        self.assertEqual(0, self.window1.default_height)
        self.window1.default_height = 42
        self.assertEqual(42, self.window1.default_height)
        self.window1.default_height = -1
        self.assertEqual(-1, self.window1.default_height)

        self.assertRaises(TypeError, setattr, self.window1, "default_height", "Hello")
        self.assertRaises(ValueError, setattr, self.window1, "default_height", -42)

    def test_default_width(self):
        self.assertEqual(0, self.window1.default_width)
        self.window1.default_width = None
        self.assertEqual(0, self.window1.default_width)
        self.window1.default_width = 42
        self.assertEqual(42, self.window1.default_width)
        self.window1.default_width = -1
        self.assertEqual(-1, self.window1.default_width)

        self.assertRaises(TypeError, setattr, self.window1, "default_width", "Hello")
        self.assertRaises(ValueError, setattr, self.window1, "default_width", -42)

    def test_deletable(self):
        self.assertFalse(self.window1.deletable)

        self.window1.deletable = True
        self.assertTrue(self.window1.deletable)

        self.window1.deletable = None
        self.assertFalse(self.window1.deletable)

        self.assertRaises(TypeError, setattr, self.window1, "deletable", "Hello")

    def test_destroy_with_parent(self):

        self.assertFalse(self.window1.destroy_with_parent)
        self.window1.destroy_with_parent = None
        self.assertFalse(self.window1.destroy_with_parent)
        self.window1.destroy_with_parent = True
        self.assertTrue(self.window1.destroy_with_parent)

        self.assertRaises(
            TypeError, setattr, self.window1, "destroy_with_parent", "Hello"
        )

    def test_focus_on_map(self):
        self.assertTrue(self.window1.focus_on_map)
        self.window1.focus_on_map = False
        self.assertFalse(self.window1.focus_on_map)
        self.window1.focus_on_map = None
        self.assertTrue(self.window1.focus_on_map)

        self.assertRaises(TypeError, setattr, self.window1, "focus_on_map", "Hello")

    def test_focus_visible(self):
        self.assertTrue(self.window1.focus_visible)
        self.window1.focus_visible = False
        self.assertFalse(self.window1.focus_visible)
        self.window1.focus_visible = None
        self.assertTrue(self.window1.focus_visible)

        self.assertRaises(TypeError, setattr, self.window1, "focus_visible", "Hello")

    def test_gravity(self):
        self.assertEqual(GLXCurses.GLXC.GRAVITY_NORTH_WEST, self.window1.gravity)
        self.window1.gravity = GLXCurses.GLXC.GRAVITY_CENTER
        self.assertEqual(GLXCurses.GLXC.GRAVITY_CENTER, self.window1.gravity)
        self.window1.gravity = None
        self.assertEqual(GLXCurses.GLXC.GRAVITY_NORTH_WEST, self.window1.gravity)

        self.assertRaises(TypeError, setattr, self.window1, "gravity", 42)
        self.assertRaises(ValueError, setattr, self.window1, "gravity", "Hello")

    def test_has_resize_grip(self):
        self.assertFalse(self.window1.has_resize_grip)
        self.window1.has_resize_grip = False
        self.assertFalse(self.window1.has_resize_grip)
        self.window1.has_resize_grip = None
        self.assertFalse(self.window1.has_resize_grip)

        self.assertRaises(TypeError, setattr, self.window1, "has_resize_grip", "Hello")

    def test_has_toplevel_focus(self):
        self.assertFalse(self.window1.has_toplevel_focus)
        self.window1.has_toplevel_focus = False
        self.assertFalse(self.window1.has_toplevel_focus)
        self.window1.has_toplevel_focus = None
        self.assertFalse(self.window1.has_toplevel_focus)

        self.assertRaises(
            TypeError, setattr, self.window1, "has_toplevel_focus", "Hello"
        )

    def test_hide_titlebar_when_maximized(self):
        self.assertFalse(self.window1.hide_titlebar_when_maximized)
        self.window1.hide_titlebar_when_maximized = False
        self.assertFalse(self.window1.hide_titlebar_when_maximized)
        self.window1.hide_titlebar_when_maximized = None
        self.assertFalse(self.window1.hide_titlebar_when_maximized)

        self.assertRaises(
            TypeError, setattr, self.window1, "hide_titlebar_when_maximized", "Hello"
        )

    def test_icon(self):
        self.assertEqual(curses.ACS_DIAMOND, self.window1.icon)
        self.window1.icon = curses.ACS_CKBOARD
        self.assertEqual(curses.ACS_CKBOARD, self.window1.icon)

        self.window1.icon = None
        self.assertEqual(curses.ACS_DIAMOND, self.window1.icon)

        self.assertRaises(TypeError, setattr, self.window1, "icon", "Hello")

    def test_icon_name(self):
        self.assertEqual(None, self.window1.icon_name)
        self.window1.icon_name = "Hello.42"
        self.assertEqual("Hello.42", self.window1.icon_name)

        self.window1.icon_name = None
        self.assertEqual(None, self.window1.icon_name)

        self.assertRaises(TypeError, setattr, self.window1, "icon_name", 42)

    def test_is_active(self):

        self.assertFalse(self.window1.is_active)
        self.window1.is_active = True
        self.assertTrue(self.window1.is_active)
        self.window1.is_active = None
        self.assertFalse(self.window1.is_active)

        self.assertRaises(TypeError, setattr, self.window1, "is_active", "Hello")

    def test_is_maximized(self):
        self.assertFalse(self.window1.is_maximized)
        self.window1.is_maximized = True
        self.assertTrue(self.window1.is_maximized)
        self.window1.is_maximized = None
        self.assertFalse(self.window1.is_maximized)

        self.assertRaises(TypeError, setattr, self.window1, "is_maximized", "Hello")

    def test_mnemonics_visible(self):
        self.assertTrue(self.window1.mnemonics_visible)
        self.window1.mnemonics_visible = False
        self.assertFalse(self.window1.mnemonics_visible)
        self.window1.mnemonics_visible = None
        self.assertTrue(self.window1.mnemonics_visible)

        self.assertRaises(
            TypeError, setattr, self.window1, "mnemonics_visible", "Hello"
        )

    def test_modal(self):
        self.assertFalse(self.window1.modal)
        self.window1.modal = True
        self.assertTrue(self.window1.modal)
        self.window1.modal = None
        self.assertFalse(self.window1.modal)

        self.assertRaises(TypeError, setattr, self.window1, "modal", "Hello")

    def test_resizable(self):
        self.assertTrue(self.window1.resizable)

        self.window1.resizable = False
        self.assertFalse(self.window1.resizable)

        self.window1.resizable = None
        self.assertTrue(self.window1.resizable)

        self.assertRaises(TypeError, setattr, self.window1, "resizable", 42)

    def test_role(self):
        self.assertIsNone(self.window1.role)
        self.window1.role = "Hello.42"
        self.assertEqual("Hello.42", self.window1.role)
        self.window1.role = None
        self.assertIsNone(self.window1.role)

        self.assertRaises(TypeError, setattr, self.window1, "role", 42)

    def test_screen(self):
        window = GLXCurses.Window()
        screen = GLXCurses.Screen()
        self.assertIsNone(window.screen)
        window.screen = screen
        self.assertEqual(screen, window.screen)
        window.screen = None
        self.assertIsNone(window.screen)

        self.assertRaises(TypeError, setattr, window, "screen", 42)

    def test_skip_pager_hint(self):
        self.assertFalse(self.window1.skip_pager_hint)
        self.window1.skip_pager_hint = True
        self.assertTrue(self.window1.skip_pager_hint)
        self.window1.skip_pager_hint = None
        self.assertFalse(self.window1.skip_pager_hint)

        self.assertRaises(TypeError, setattr, self.window1, "skip_pager_hint", 42)

    def test_skip_taskbar_hint(self):
        self.assertFalse(self.window1.skip_taskbar_hint)
        self.window1.skip_taskbar_hint = True
        self.assertTrue(self.window1.skip_taskbar_hint)
        self.window1.skip_taskbar_hint = None
        self.assertFalse(self.window1.skip_taskbar_hint)

        self.assertRaises(TypeError, setattr, self.window1, "skip_taskbar_hint", 42)

    def test_startup_id(self):
        self.assertIsNone(self.window1.startup_id)
        self.window1.startup_id = "Hello.42"
        self.assertEqual("Hello.42", self.window1.startup_id)
        self.window1.startup_id = None
        self.assertIsNone(self.window1.startup_id)

        self.assertRaises(TypeError, setattr, self.window1, "startup_id", 42)

    def test_title(self):
        self.assertIsNone(self.window1.title)
        self.window1.title = "Hello.42"
        self.assertEqual("Hello.42", self.window1.title)
        self.window1.title = None
        self.assertIsNone(self.window1.title)
        self.assertRaises(TypeError, setattr, self.window1, "title", 42)

    def test_transient_for(self):
        self.window1.transient_for = self.window2

        self.assertEqual(self.window2, self.window1.transient_for)

        self.window1.transient_for = None
        self.assertIsNone(self.window1.transient_for)

        self.assertRaises(TypeError, setattr, self.window1, "transient_for", 42)

    def test_type(self):
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, self.window1.type)
        self.window1.type = GLXCurses.GLXC.WINDOW_POPUP
        self.assertEqual(GLXCurses.GLXC.WINDOW_POPUP, self.window1.type)
        self.window1.type = None
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, self.window1.type)

        self.assertRaises(TypeError, setattr, self.window1, "type", 42)
        self.assertRaises(ValueError, setattr, self.window1, "type", "Hello.42")

    def test_type_hint(self):
        self.assertEqual(GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL, self.window1.type_hint)
        for hint in [
            GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DIALOG,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_MENU,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_TOOLBAR,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_SPLASHSCREEN,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_UTILITY,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DOCK,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DESKTOP,
        ]:
            self.window1.type_hint = hint
            self.assertEqual(hint, self.window1.type_hint)
        self.window1.type_hint = None
        self.assertEqual(GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL, self.window1.type_hint)
        self.assertRaises(TypeError, setattr, self.window1, "type_hint", 42)
        self.assertRaises(ValueError, setattr, self.window1, "type_hint", "Hello.42")

    def test_urgency_hint(self):
        self.assertFalse(self.window1.urgency_hint)
        self.window1.urgency_hint = True
        self.assertTrue(self.window1.urgency_hint)
        self.window1.urgency_hint = None
        self.assertFalse(self.window1.urgency_hint)

        self.assertRaises(TypeError, setattr, self.window1, "urgency_hint", "Hello")

    def test_window_position(self):
        self.assertEqual(GLXCurses.GLXC.WIN_POS_NONE, self.window1.position)
        for position in [
            GLXCurses.GLXC.WIN_POS_NONE,
            GLXCurses.GLXC.WIN_POS_CENTER,
            GLXCurses.GLXC.WIN_POS_MOUSE,
            GLXCurses.GLXC.WIN_POS_CENTER_ALWAYS,
            GLXCurses.GLXC.WIN_POS_CENTER_ON_PARENT,
        ]:
            self.window1.position = position
            self.assertEqual(position, self.window1.position)

        self.window1.position = None
        self.assertEqual(GLXCurses.GLXC.WIN_POS_NONE, self.window1.position)
        self.assertRaises(TypeError, setattr, self.window1, "position", 42)
        self.assertRaises(ValueError, setattr, self.window1, "position", "Hello.42")

    def test_decoration_button_layout(self):
        self.assertEqual("menu:close", self.window1.decoration_button_layout)
        self.window1.decoration_button_layout = "close"
        self.assertEqual("close", self.window1.decoration_button_layout)
        self.window1.decoration_button_layout = None
        self.assertEqual("menu:close", self.window1.decoration_button_layout)

        self.assertRaises(
            TypeError, setattr, self.window1, "decoration_button_layout", 42
        )

    def test_decoration_resize_handle(self):
        self.assertEqual(0, self.window1.decoration_resize_handle)
        self.window1.decoration_resize_handle = 42
        self.assertEqual(42, self.window1.decoration_resize_handle)
        self.window1.decoration_resize_handle = None
        self.assertEqual(0, self.window1.decoration_resize_handle)

        self.assertRaises(
            TypeError, setattr, self.window1, "decoration_resize_handle", "Hello.42"
        )
        self.assertRaises(
            ValueError, setattr, self.window1, "decoration_resize_handle", -42
        )

    # Test
    def test_window_glxc_type(self):
        """Test if Window is GLXCurses Type"""
        self.assertTrue(GLXCurses.glxc_type(self.window1))

    def test_window_draw_widget_in_area(self):
        """Test Window.draw_widget_in_area()"""
        self.window1.decorated = True
        self.window1.title = "GLXCurses Window tests"
        GLXCurses.Application().add_window(self.window1)
        GLXCurses.Application().refresh()
        self.window1.decorated = False
        GLXCurses.Application().refresh()
        self.window1.decorated = True
        GLXCurses.Application().refresh()
        self.window1.sensitive = False
        GLXCurses.Application().refresh()
        self.window1.sensitive = True
        GLXCurses.Application().refresh()

    def test_window_add_accel_group(self):
        """Test Window.add_accel_group()"""
        self.assertRaises(NotImplementedError, self.window1.add_accel_group)

    def test_window_remove_accel_group(self):
        """Test Window.remove_accel_group()"""
        self.assertRaises(NotImplementedError, self.window1.remove_accel_group)

    def test_activate_focus(self):
        self.window2.has_focus = True
        self.assertTrue(self.window1.activate_focus())
        self.window2.has_focus = False
        self.assertFalse(self.window1.activate_focus())

    def test_activate_default(self):
        self.window2.has_default = True
        self.assertTrue(self.window1.activate_default())
        self.window2.has_default = False
        self.assertFalse(self.window1.activate_default())

    def test_get_focus(self):
        self.window2.has_focus = True
        self.assertIsNone(self.window1.get_focus())
        self.window1.is_focus = True
        self.assertEqual(self.window1.get_focus(), self.window2)

    def test_set_get_default(self):
        self.window1.set_default(self.window2)
        self.assertEqual(self.window1.get_default_widget(), self.window2)
        self.window1.set_default(None)
        self.assertIsNone(self.window1.get_default_widget())
        self.assertRaises(TypeError, self.window1.set_default, 42)

    def test_window_get_window_type(self):
        """Test Window.get_window_type()"""
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, self.window1.get_window_type())


if __name__ == "__main__":
    unittest.main()
