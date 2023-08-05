#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

from GLXCurses import Actionable

import unittest


# Unittest
class TestActionable(unittest.TestCase):

    # Test
    def test_Actionable_action_name(self):
        actionable = Actionable()
        self.assertIsNone(actionable.action_name)
        self.assertIsNone(actionable.get_action_name())

        actionable.action_name = "Hello.42"
        self.assertEqual(actionable.action_name, "Hello.42")
        self.assertEqual(actionable.get_action_name(), "Hello.42")

        actionable.action_name = None
        self.assertIsNone(actionable.action_name)
        self.assertIsNone(actionable.get_action_name())

        actionable.set_action_name("Hello.42.42")
        self.assertEqual(actionable.action_name, "Hello.42.42")
        self.assertEqual(actionable.get_action_name(), "Hello.42.42")

        actionable.set_action_name()
        self.assertIsNone(actionable.action_name)
        self.assertIsNone(actionable.get_action_name())

        self.assertRaises(TypeError, setattr, actionable, "action_name", 42)
        self.assertRaises(TypeError, actionable.set_action_name, 42)

    def test_Actionable_target_value(self):
        actionable = Actionable()
        self.assertIsNone(actionable.action_target)
        self.assertIsNone(actionable.get_action_target_value())

        actionable.action_target = "Hello.42"
        self.assertEqual(actionable.action_target, "Hello.42")
        self.assertEqual(actionable.get_action_target_value(), "Hello.42")

        actionable.action_target = None
        self.assertIsNone(actionable.action_target)
        self.assertIsNone(actionable.get_action_target_value())

        actionable.set_action_target_value("Hello.42.42")
        self.assertEqual(actionable.action_target, "Hello.42.42")
        self.assertEqual(actionable.get_action_target_value(), "Hello.42.42")

        actionable.set_action_target_value()
        self.assertIsNone(actionable.action_target)
        self.assertIsNone(actionable.get_action_target_value())


if __name__ == "__main__":
    unittest.main()
