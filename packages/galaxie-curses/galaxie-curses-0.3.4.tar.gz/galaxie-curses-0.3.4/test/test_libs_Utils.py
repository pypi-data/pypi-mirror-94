#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from GLXCurses.libs.Utils import check_mnemonic_in_text
from GLXCurses.libs.Utils import clamp_to_zero
from GLXCurses.libs.Utils import clamp
from GLXCurses.libs.Utils import resize_text_wrap_char
from GLXCurses.libs.Utils import resize_text
from GLXCurses.libs.Utils import glxc_type
from GLXCurses.libs.Utils import new_id
from GLXCurses.libs.Utils import is_valid_id
from GLXCurses.libs.Utils import merge_dicts
from GLXCurses.libs.Utils import sizeof
from GLXCurses.libs.Utils import disk_usage
from GLXCurses.libs.Utils import round_up
from GLXCurses.libs.Utils import round_down
from GLXCurses.libs.Utils import round_half_up
from GLXCurses.libs.Utils import round_half_down

# from GLXCurses.Utils import get_split_area_positions
from GLXCurses import Window


# Unittest
class TestLibsUtils(unittest.TestCase):
    def test_check_mnemonic_in_text(self):
        excepted = {"text": "Hello", "position": 0}
        self.assertEqual(excepted, check_mnemonic_in_text(text="_Hello"))
        excepted = {"text": "Hell_o", "position": 1}
        self.assertEqual(excepted, check_mnemonic_in_text(text="H_ell_o"))
        excepted = {"text": "Hello", "position": None}
        self.assertEqual(excepted, check_mnemonic_in_text(text="Hello"))
        excepted = {"text": "", "position": None}
        self.assertEqual(excepted, check_mnemonic_in_text())
        self.assertRaises(TypeError, check_mnemonic_in_text, text=42, mnemonic_char="_")
        self.assertRaises(
            TypeError, check_mnemonic_in_text, text="Hello", mnemonic_char=42
        )
        self.assertRaises(
            ValueError, check_mnemonic_in_text, text="Hello", mnemonic_char="__"
        )

    def test_glxc_type(self):
        self.assertTrue(glxc_type(Window()))
        self.assertFalse(glxc_type(int()))
        self.assertFalse(glxc_type())

    def test_clamp_to_zero(self):
        """Test Utils.clamp_to_zero()"""
        self.assertEqual(0, clamp_to_zero(-42))
        self.assertEqual(0, clamp_to_zero(0))
        self.assertEqual(42, clamp_to_zero(42))
        self.assertRaises(TypeError, clamp_to_zero, float(42.42))

    def test_clamp(self):
        """Test Utils.clamp()"""
        self.assertEqual(42, clamp(value=1, smallest=42, largest=100))
        self.assertEqual(42.0, clamp(value=1.0, smallest=42, largest=100))

        self.assertEqual(42, clamp(value=100, smallest=0, largest=42))
        self.assertEqual(42.0, clamp(value=100.0, smallest=0, largest=42))

        self.assertRaises(TypeError, clamp, value=str(""), smallest=0, largest=42)
        self.assertRaises(TypeError, clamp, value=100, smallest=str(""), largest=42)
        self.assertRaises(TypeError, clamp, value=100, smallest=0, largest=str(""))

    def test_resize_text_wrap_char(self):
        """Test Utils.clamp_to_zero()"""
        text = "123456789"
        width = 3
        self.assertEqual("123", resize_text_wrap_char(text, width))
        self.assertEqual("123456789", resize_text_wrap_char(text, 10))
        # Test Error
        self.assertRaises(
            TypeError, resize_text_wrap_char, text=text, max_width=str("Hello")
        )
        self.assertRaises(TypeError, resize_text_wrap_char, text=int(2), max_width=3)

    def test_resize_text(self):
        text = "123456789ABCDEFGHIJKLMOPQRSTUVWXYZ"
        width = 16
        self.assertEqual("1234567~TUVWXYZ", resize_text(text, width, "~"))
        width = 15
        self.assertEqual("1234567~TUVWXYZ", resize_text(text, width, "~"))
        width = 14
        self.assertEqual("1234567~UVWXYZ", resize_text(text, width, "~"))
        width = 13
        self.assertEqual("123456~UVWXYZ", resize_text(text, width, "~"))
        width = 12
        self.assertEqual("123456~VWXYZ", resize_text(text, width, "~"))
        width = 11
        self.assertEqual("12345~VWXYZ", resize_text(text, width, "~"))
        width = 10
        self.assertEqual("12345~WXYZ", resize_text(text, width, "~"))
        width = 9
        self.assertEqual("1234~WXYZ", resize_text(text, width, "~"))
        width = 8
        self.assertEqual("1234~XYZ", resize_text(text, width, "~"))
        width = 7
        self.assertEqual("123~XYZ", resize_text(text, width, "~"))
        width = 6
        self.assertEqual("123~YZ", resize_text(text, width, "~"))
        width = 5
        self.assertEqual("12~YZ", resize_text(text, width, "~"))
        width = 4
        self.assertEqual("12~Z", resize_text(text, width, "~"))
        width = 3
        self.assertEqual("1~Z", resize_text(text, width, "~"))
        width = 2
        self.assertEqual("1Z", resize_text(text, width, "~"))
        width = 1
        self.assertEqual("1", resize_text(text, width, "~"))
        width = 0
        self.assertEqual("", resize_text(text, width, "~"))
        width = -1
        self.assertEqual("", resize_text(text, width, "~"))

        # Test Error
        self.assertRaises(
            TypeError, resize_text, text=text, max_width=width, separator=int(42)
        )
        self.assertRaises(
            TypeError, resize_text, text=text, max_width="coucou", separator="~"
        )
        self.assertRaises(
            TypeError, resize_text, text=int(42), max_width=width, separator="~"
        )

    def test_id_generator(self):
        """Test Utils.id_generator()"""
        id_1 = new_id()
        self.assertTrue(is_valid_id(id_1))
        self.assertEqual(len(id_1), 8)
        # max_iteration = 10000000 - Take 99.114s  on Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz
        # max_iteration = 1000000  - Take 9.920s   on Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz
        # max_iteration = 100000   - Take 0.998s   on Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz
        # max_iteration = 10000    - Take 0.108s   on Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz

        max_iteration = 10000
        for _ in range(1, max_iteration):
            id_2 = new_id()
            self.assertEqual(len(id_2), 8)
            self.assertNotEqual(id_1, id_2)

    def test_is_valid_id(self):
        """Test Utils.is_valid_id()"""
        id_1 = new_id()
        self.assertTrue(is_valid_id(id_1))
        self.assertFalse(is_valid_id(42))

    def test_Utils_merge_dicts(self):
        """Test Utils merge_dicts()"""
        result_wanted1 = {"a": 4, "b": 2}
        value1 = {"a": 4}
        value2 = {"b": 2}
        self.assertEqual(result_wanted1, merge_dicts(value1, value2))
        value1 = {"a": 0, "b": 0}
        value2 = {"a": 4, "b": 2}
        self.assertEqual(value2, merge_dicts(value1, value2))

    # def test_get_os_temporary_dir(self):
    #     """Test Utils.get_os_temporary_dir()"""
    #     from GLXCurses.libs.Utils import get_os_temporary_dir
    #
    #     accepted_value = ["/tmp", "/var/tmp", "/usr/tmp"]
    #     self.assertTrue(get_os_temporary_dir() in accepted_value)
    #
    #     # use TMP env variable
    #     os.environ["TMPDIR"] = "/tmp"
    #     self.assertTrue(get_os_temporary_dir() in accepted_value)
    #
    #     os.environ["TMPDIR"] = "/tmp/lulu"
    #     self.assertRaises(FileNotFoundError, get_os_temporary_dir)

    def test_utils_sizeof(self):
        """Test Utils sizeof"""
        # Ref: https://en.wikipedia.org/wiki/Metric_prefix
        self.assertEqual("1Y", sizeof(1000000000000000000000000))
        self.assertEqual("1Z", sizeof(1000000000000000000000))
        self.assertEqual("1E", sizeof(1000000000000000000))
        self.assertEqual("1P", sizeof(1000000000000000))
        self.assertEqual("1T", sizeof(1000000000000))
        self.assertEqual("1G", sizeof(1000000000))
        self.assertEqual("1M", sizeof(1000000))
        self.assertEqual("1k", sizeof(1000))
        self.assertEqual("10", sizeof(10))

        self.assertRaises(TypeError, sizeof, "42")

    def test_round_up(self):
        self.assertEqual(43, round_up(42.42))
        self.assertEqual(42.5, round_up(42.42, 1))
        self.assertEqual(42.42, round_up(42.42, 2))

    def test_round_down(self):
        self.assertEqual(42, round_down(42.42))
        self.assertEqual(42.4, round_down(42.42, 1))
        self.assertEqual(42.42, round_down(42.42, 2))

    def test_round_half_up(self):
        self.assertEqual(42, round_half_up(42.42))
        self.assertEqual(42.5, round_half_up(42.53, 1))
        self.assertEqual(42.42, round_half_up(42.42, 2))

    def test_round_half_down(self):
        self.assertEqual(42, round_half_down(42.42))
        self.assertEqual(42.8, round_half_down(42.77, 1))
        self.assertEqual(42.42, round_half_down(42.42, 2))

    def test_utils_disk_usage(self):
        """Test Utils disk_usage"""
        self.assertEqual(str, type(disk_usage(".")))
        self.assertGreater(len(disk_usage(".")), 7)

    # def test_utils_get_split_area_positions(self):
    #     """test Utils get_split_area_positions()"""
    #     self.assertEqual(
    #         {'0': (0, 32), '1': (33, 65), '2': (66, 99)},
    #         get_split_area_positions(start=0, stop=99, num=3)
    #     )

    # def test_utils_get_split_area_positions(self):
    #     """test Utils get_split_area_positions()"""
    #     self.assertEqual(
    #         {'0': (0, 32), '1': (33, 65), '2': (66, 99)},
    #         get_split_area_positions(start=0, stop=99, num=3)
    #     )
    #     self.assertEqual(
    #         {'0': (0, 19), '1': (20, 39), '2': (40, 59), '3': (60, 79), '4': (80, 99)},
    #         get_split_area_positions(start=0, stop=99, num=5)
    #     )
    #
    #     self.assertRaises(TypeError, get_split_area_positions, start=None, stop=99, num=3)
    #     self.assertRaises(TypeError, get_split_area_positions, start=0, stop=None, num=3)
    #     self.assertRaises(TypeError, get_split_area_positions, start=0, stop=99, num=None)
