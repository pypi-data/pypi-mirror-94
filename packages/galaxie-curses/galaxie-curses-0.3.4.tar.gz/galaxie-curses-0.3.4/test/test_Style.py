#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from random import randint
import sys
import os

# Require when you haven't GLXCurses as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

import GLXCurses


# Unittest
class TestStyle(unittest.TestCase):
    def setUp(self):
        # Before the test start
        # Require for init the stdscr
        self.application = GLXCurses.Application()
        # The component to test
        self.style = GLXCurses.Style()

    # Tests
    def test_default_attribute_states(self):
        """Test Style.get_default_attribute_states()"""
        # Check first level dictionary
        self.assertEqual(type(self.style.default_attributes_states), type(dict()))
        # For each key's
        for attribute in [
            "text_fg",
            "bg",
            "light",
            "dark",
            "mid",
            "text",
            "base",
            "black",
            "white",
        ]:
            # Check if the key value is a dictionary
            self.assertEqual(type(self.style.default_attributes_states[attribute]), type(dict()))
            # For each key value, in that case a sub dictionary
            for state in [
                "STATE_NORMAL",
                "STATE_ACTIVE",
                "STATE_PRELIGHT",
                "STATE_SELECTED",
                "STATE_INSENSITIVE",
            ]:
                # Check if the key value is a string
                self.assertEqual(
                    type(self.style.default_attributes_states[attribute][state]), type(tuple())
                )

    def test_get_color_pair(self):
        """Test Style.get_curses_color_pair()"""
        # Check if fg='WHITE', bg='BLACK' first in the list
        self.assertEqual(self.style.color(fg=(255, 255, 255), bg=(0, 0, 0), attributes=True), 2131712)

        # Check if fg='WHITE', bg='BLUE' return a int type
        self.assertEqual(type(self.style.color(fg=(255, 255, 255), bg=(0, 0, 255))), type(int()))

        # Check if fg='WHITE', bg='BLUE' return a value > 0
        self.assertGreater(self.style.color(fg=(255, 255, 255), bg=(0, 0, 255)), 0)

        # Check if fg='RED', bg='BLUE' return a value > 0
        self.assertGreater(self.style.color(fg=(255, 0, 0), bg=(0, 0, 255)), 0)

    def test_attribute_states(self):
        """Test Style.get_attribute_states()"""
        # Load a valid Style
        self.style.attributes_states = self.style.default_attributes_states

        # Load the Valid Style
        attribute_states = self.style.attributes_states
        # Check first level dictionary
        self.assertEqual(type(attribute_states), type(dict()))
        # For each key's
        for attribute in [
            "text_fg",
            "bg",
            "light",
            "dark",
            "mid",
            "text",
            "base",
            "black",
            "white",
        ]:
            # Check if the key value is a dictionary
            self.assertEqual(type(attribute_states[attribute]), type(dict()))
            # For each key value, in that case a sub dictionary
            for state in [
                "STATE_NORMAL",
                "STATE_ACTIVE",
                "STATE_PRELIGHT",
                "STATE_SELECTED",
                "STATE_INSENSITIVE",
            ]:
                # Check if the key value is a string
                self.assertEqual(type(attribute_states[attribute][state]), type(tuple()))

        # Try to change style
        attribute_states = self.style.default_attributes_states
        attribute_states["text_fg"]["STATE_NORMAL"] = (255, 255, 0)
        self.style.attributes_states = attribute_states

        # Check if not a dictionary
        self.assertRaises(
            TypeError, setattr, self.style, "attributes_states", float(randint(1, 42))
        )

        # Check raise with wrong Style
        attribute_states = dict()

        # Check with a empty dictionary
        self.assertRaises(
            KeyError, setattr, self.style, "attributes_states", attribute_states
        )

        # Check with first level dictionary it look ok
        attribute_states["text_fg"] = dict()
        attribute_states["bg"] = dict()
        attribute_states["light"] = dict()
        attribute_states["dark"] = dict()
        attribute_states["mid"] = dict()
        attribute_states["__text"] = dict()
        attribute_states["base"] = dict()
        attribute_states["black"] = dict()
        attribute_states["white"] = dict()
        self.assertRaises(
            KeyError, setattr, self.style, "attributes_states", attribute_states
        )

        attribute_states = self.style.attributes_states
        attribute_states["text_fg"] = list()
        self.assertRaises(
            TypeError, setattr, self.style, "attributes_states", attribute_states
        )

        attribute_states = self.style.default_attributes_states
        attribute_states["text_fg"]["STATE_NORMAL"] = int(42)
        self.assertRaises(
            TypeError, setattr, self.style, "attributes_states", attribute_states
        )


if __name__ == "__main__":
    unittest.main()
