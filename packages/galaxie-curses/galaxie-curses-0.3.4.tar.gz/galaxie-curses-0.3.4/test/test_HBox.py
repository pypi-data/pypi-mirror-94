#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import GLXCurses

# Unittest
class TestBox(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        GLXCurses.Application().add_window(self.win)
        self.hbox = GLXCurses.HBox()
        self.win.add(self.hbox)

    # Test
    def test_glxc_type(self):
        """Test StatusBar type"""
        box = GLXCurses.HBox()
        self.assertTrue(GLXCurses.glxc_type(box))

    def test_new(self):
        """Test Box.new()"""
        # check default value
        hbox1 = GLXCurses.HBox().new()
        self.assertEqual(True, hbox1.homogeneous)
        self.assertEqual(0, hbox1.spacing)

        # check with value
        hbox1 = GLXCurses.HBox().new(False, spacing=4)
        self.assertEqual(False, hbox1.homogeneous)
        self.assertEqual(4, hbox1.spacing)

        # check error Type
        self.assertRaises(TypeError, hbox1.new, homogeneous=float(42), spacing=4)
        self.assertRaises(TypeError, hbox1.new, homogeneous=True, spacing="Galaxie")

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

        self.hbox.pack_end(win_main1)
        self.hbox.pack_end(win_main2)
        self.hbox.pack_end(win_main3)
        self.hbox.pack_end(win_main4)
        self.hbox.pack_end(win_main5)

        GLXCurses.Application().refresh()

        self.hbox.set_decorated(True)
        GLXCurses.Application().refresh()
