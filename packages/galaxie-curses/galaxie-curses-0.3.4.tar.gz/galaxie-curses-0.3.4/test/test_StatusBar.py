#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import random
import string
import GLXCurses


# Unittest
class TestStatusBar(unittest.TestCase):
    def setUp(self):
        self.win = GLXCurses.Window()
        self.win.title = "StatusBar Tests"
        self.statusbar = GLXCurses.StatusBar()
        GLXCurses.Application().add_window(self.win)
        GLXCurses.Application().statusbar = self.statusbar

    def test_draw(self):
        GLXCurses.Application().refresh()

    # Test
    def test_glxc_type(self):
        self.assertTrue(GLXCurses.glxc_type(self.statusbar))

    def test_new(self):
        # create a window instance
        statusbar = GLXCurses.StatusBar()
        # get the window id
        statusbar_id_take1 = statusbar.id
        # check if returned value is a valid id
        self.assertTrue(GLXCurses.is_valid_id(statusbar_id_take1))
        # use new() method
        statusbar.new()
        # re get the window id
        statusbar_id_take2 = statusbar.id
        # check if returned value is a valid id
        self.assertTrue(GLXCurses.is_valid_id(statusbar_id_take2))
        # id's must be different
        self.assertNotEqual(statusbar_id_take1, statusbar_id_take2)

    def test_get_context_id(self):
        # generate a random string
        context_text = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        # get the window id
        statusbar_context_id_take1 = self.statusbar.get_context_id(
            context_description=context_text
        )
        # check if returned value is a valid id
        self.assertTrue(GLXCurses.is_valid_id(statusbar_context_id_take1))
        # test raises
        self.assertRaises(
            TypeError, self.statusbar.get_context_id, context_description=int()
        )

        GLXCurses.Application().refresh()

    def test_push(self):
        # generate a random string
        text_take1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        text_take2 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        # get the window id
        context_id = self.statusbar.get_context_id(context_description=text_take1)
        # check if returned value is a valid id
        self.assertTrue(GLXCurses.is_valid_id(context_id))
        # get stack size
        stack_len = len(self.statusbar.statusbar_stack)
        # call StatusBar.push() suppose to return a message id
        message_id = self.statusbar.push(context_id=context_id, text=text_take2)
        # check if returned value is a valid id
        self.assertTrue(GLXCurses.is_valid_id(message_id))
        # compare stack size suppose to grow
        self.assertGreater(len(self.statusbar.statusbar_stack), stack_len)
        # compare last element
        self.assertEqual(self.statusbar.statusbar_stack[-1]["context_id"], context_id)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["message_id"], message_id)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["text"], text_take2)

        # test raises
        self.assertRaises(
            TypeError, self.statusbar.push, context_id=str(), text=text_take2
        )
        self.assertRaises(
            TypeError, self.statusbar.push, context_id=context_id, text=float()
        )
        GLXCurses.Application().refresh()

    def test_pop(self):
        # Preparation push completely a thing and save every value's
        context_description_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        text_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        context_id_1 = self.statusbar.get_context_id(
            context_description=context_description_1
        )
        message_id_1 = self.statusbar.push(context_id=context_id_1, text=text_1)

        # compare last element
        self.assertEqual(self.statusbar.statusbar_stack[-1]["context_id"], context_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["message_id"], message_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["text"], text_1)

        # Preparation push completely a thing and save every value's
        context_description_2 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        text_2 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        context_id_2 = self.statusbar.get_context_id(
            context_description=context_description_2
        )
        message_id_2 = self.statusbar.push(context_id=context_id_2, text=text_2)

        # compare last element
        self.assertEqual(self.statusbar.statusbar_stack[-1]["context_id"], context_id_2)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["message_id"], message_id_2)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["text"], text_2)

        # POP
        self.statusbar.pop(context_id=context_id_2)

        # check if are back to previous element
        self.assertEqual(self.statusbar.statusbar_stack[-1]["context_id"], context_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["message_id"], message_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["text"], text_1)

        # test raise
        self.assertRaises(TypeError, self.statusbar.pop, context_id=int())
        self.assertRaises(
            TypeError,
            self.statusbar.pop,
        )

        GLXCurses.Application().refresh()

    def test_remove(self):
        # get stack size
        stack_len = len(self.statusbar.statusbar_stack)

        # Preparation push completely a thing and save every value's
        context_description_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        text_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        context_id_1 = self.statusbar.get_context_id(
            context_description=context_description_1
        )
        message_id_1 = self.statusbar.push(context_id=context_id_1, text=text_1)

        # compare last element
        self.assertEqual(self.statusbar.statusbar_stack[-1]["context_id"], context_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["message_id"], message_id_1)
        self.assertEqual(self.statusbar.statusbar_stack[-1]["text"], text_1)

        # compare stack size suppose to grow
        self.assertGreater(len(self.statusbar.statusbar_stack), stack_len)

        # remove
        self.statusbar.remove(context_id=context_id_1, message_id=message_id_1)

        # compare stack size suppose to grow
        self.assertEqual(len(self.statusbar.statusbar_stack), stack_len)

        # test raises
        self.assertRaises(
            TypeError, self.statusbar.remove, context_id=int(), message_id=message_id_1
        )
        self.assertRaises(
            TypeError,
            self.statusbar.remove,
            context_id=context_id_1,
            message_id=float(),
        )
        self.assertRaises(TypeError, self.statusbar.remove, message_id=message_id_1)

        GLXCurses.Application().refresh()

    def test_remove_all(self):
        # get stack size
        stack_len_1 = len(self.statusbar.statusbar_stack)

        # prepare a context_id
        context_description_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        context_id_1 = self.statusbar.get_context_id(
            context_description=context_description_1
        )

        # Preparation push completely a thing and save every value's
        text_1 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        self.statusbar.push(context_id=context_id_1, text=text_1)

        # compare stack size suppose to grow
        self.assertGreater(len(self.statusbar.statusbar_stack), stack_len_1)

        # get stack size
        stack_len_2 = len(self.statusbar.statusbar_stack)

        # Preparation push completely a thing and save every value's
        text_2 = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        self.statusbar.push(context_id=context_id_1, text=text_2)

        # compare stack size suppose to grow
        self.assertGreater(len(self.statusbar.statusbar_stack), stack_len_2)

        # remove_all
        self.statusbar.remove_all(context_id=context_id_1)

        # compare stack size suppose to grow
        self.assertGreater(len(self.statusbar.statusbar_stack), stack_len_1)

        # test raises
        self.assertRaises(TypeError, self.statusbar.remove_all, context_id=int())
        GLXCurses.Application().refresh()
