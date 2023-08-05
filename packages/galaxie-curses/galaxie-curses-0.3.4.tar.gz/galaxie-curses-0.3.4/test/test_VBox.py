#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from GLXCurses.libs.Utils import glxc_type
import GLXCurses


# Unittest
class TestBox(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        GLXCurses.Application().add_window(self.win)
        self.vbox = GLXCurses.VBox()
        self.win.add(self.vbox)

    # Test
    def test_glxc_type(self):
        """Test StatusBar type"""
        box = GLXCurses.VBox()
        self.assertTrue(glxc_type(box))

    def test_new(self):
        """Test Box.new()"""
        # check default value
        vbox1 = GLXCurses.VBox().new()
        self.assertEqual(True, vbox1.homogeneous)
        self.assertEqual(0, vbox1.spacing)

        # check with value
        vbox1 = GLXCurses.VBox().new(False, spacing=4)
        self.assertEqual(False, vbox1.homogeneous)
        self.assertEqual(4, vbox1.spacing)

        # check error Type
        self.assertRaises(TypeError, vbox1.new, homogeneous=float(42), spacing=4)
        self.assertRaises(TypeError, vbox1.new, homogeneous=True, spacing="Galaxie")

    def test_draw_widget_in_area(self):
        # Create a Window
        win_main1 = GLXCurses.Window()
        win_main1.decorated = True
        win_main1.title = "Hello Container 1"
        win_main1.debug = False

        win_main2 = GLXCurses.Window()
        win_main2.decorated = True
        win_main2.title = "Hello Container 2"

        win_main3 = GLXCurses.Window()
        win_main3.decorated = True
        win_main3.title = "Hello Container 3"

        win_main4 = GLXCurses.Window()
        win_main4.decorated = True
        win_main4.title = "Hello Container 4"

        win_main5 = GLXCurses.Window()
        win_main5.decorated = True
        win_main5.title = "Hello Container 5"

        self.vbox.pack_end(win_main1)
        self.vbox.pack_end(win_main2)
        self.vbox.pack_end(win_main3)
        self.vbox.pack_end(win_main4)
        self.vbox.pack_end(win_main5)

        GLXCurses.Application().refresh()

        self.vbox.set_decorated(True)
        GLXCurses.Application().refresh()
