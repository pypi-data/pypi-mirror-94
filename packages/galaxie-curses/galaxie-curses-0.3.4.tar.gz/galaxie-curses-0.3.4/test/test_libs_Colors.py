import unittest

from GLXCurses.libs.Colors import Colors


class TestLibsColors(unittest.TestCase):
    def setUp(self):
        self.colors = Colors()

    def test_itu_recommendation(self):
        self.colors.itu_recommendation = None
        self.assertEqual('BT.601', self.colors.itu_recommendation)

        for value in ['BT.601', 'BT.709', 'BT.2100', 'CUSTOM']:
            self.colors.itu_recommendation = value
            self.assertEqual(value, self.colors.itu_recommendation)

        self.assertRaises(TypeError, setattr, self.colors, 'itu_recommendation', 42)
        self.assertRaises(ValueError, setattr, self.colors, 'itu_recommendation', 'Hello.42')

    def test_get_luma_component_rgb(self):
        # for value in ['BT.601', 'BT.709', 'BT.2100', 'CUSTOM']:
        self.colors.itu_recommendation = 'BT.601'
        self.assertEqual(0.33763886032268264, self.colors.get_luma_component_rgb(0, 0, 255))

        self.colors.itu_recommendation = 'BT.709'
        self.assertEqual(0.26870057685088805, self.colors.get_luma_component_rgb(0, 0, 255))

        self.colors.itu_recommendation = 'BT.2100'
        self.assertEqual(0.2435159132377184, self.colors.get_luma_component_rgb(0, 0, 255))

        self.colors.itu_recommendation = 'CUSTOM'
        self.assertEqual(0.49598387070548977, self.colors.get_luma_component_rgb(0, 0, 255))

    def test_colornum(self):
        self.assertEqual(128, self.colors.curses_color_pair_number(fg=0, bg=0))
        self.assertEqual(129, self.colors.curses_color_pair_number(fg=1, bg=0))
        self.assertEqual(130, self.colors.curses_color_pair_number(fg=2, bg=0))
        self.assertEqual(131, self.colors.curses_color_pair_number(fg=3, bg=0))
        self.assertEqual(132, self.colors.curses_color_pair_number(fg=4, bg=0))
        self.assertEqual(133, self.colors.curses_color_pair_number(fg=5, bg=0))
        self.assertEqual(134, self.colors.curses_color_pair_number(fg=6, bg=0))
        self.assertEqual(135, self.colors.curses_color_pair_number(fg=7, bg=0))

        self.assertEqual(144, self.colors.curses_color_pair_number(fg=0, bg=1))
        self.assertEqual(145, self.colors.curses_color_pair_number(fg=1, bg=1))
        self.assertEqual(146, self.colors.curses_color_pair_number(fg=2, bg=1))
        self.assertEqual(147, self.colors.curses_color_pair_number(fg=3, bg=1))
        self.assertEqual(148, self.colors.curses_color_pair_number(fg=4, bg=1))
        self.assertEqual(149, self.colors.curses_color_pair_number(fg=5, bg=1))
        self.assertEqual(150, self.colors.curses_color_pair_number(fg=6, bg=1))
        self.assertEqual(151, self.colors.curses_color_pair_number(fg=7, bg=1))

        self.assertEqual(160, self.colors.curses_color_pair_number(fg=0, bg=2))
        self.assertEqual(161, self.colors.curses_color_pair_number(fg=1, bg=2))
        self.assertEqual(162, self.colors.curses_color_pair_number(fg=2, bg=2))
        self.assertEqual(163, self.colors.curses_color_pair_number(fg=3, bg=2))
        self.assertEqual(164, self.colors.curses_color_pair_number(fg=4, bg=2))
        self.assertEqual(165, self.colors.curses_color_pair_number(fg=5, bg=2))
        self.assertEqual(166, self.colors.curses_color_pair_number(fg=6, bg=2))
        self.assertEqual(167, self.colors.curses_color_pair_number(fg=7, bg=2))

        self.assertEqual(176, self.colors.curses_color_pair_number(fg=0, bg=3))
        self.assertEqual(177, self.colors.curses_color_pair_number(fg=1, bg=3))
        self.assertEqual(178, self.colors.curses_color_pair_number(fg=2, bg=3))
        self.assertEqual(179, self.colors.curses_color_pair_number(fg=3, bg=3))
        self.assertEqual(180, self.colors.curses_color_pair_number(fg=4, bg=3))
        self.assertEqual(181, self.colors.curses_color_pair_number(fg=5, bg=3))
        self.assertEqual(182, self.colors.curses_color_pair_number(fg=6, bg=3))
        self.assertEqual(183, self.colors.curses_color_pair_number(fg=7, bg=3))

        self.assertEqual(192, self.colors.curses_color_pair_number(fg=0, bg=4))
        self.assertEqual(193, self.colors.curses_color_pair_number(fg=1, bg=4))
        self.assertEqual(194, self.colors.curses_color_pair_number(fg=2, bg=4))
        self.assertEqual(195, self.colors.curses_color_pair_number(fg=3, bg=4))
        self.assertEqual(196, self.colors.curses_color_pair_number(fg=4, bg=4))
        self.assertEqual(197, self.colors.curses_color_pair_number(fg=5, bg=4))
        self.assertEqual(198, self.colors.curses_color_pair_number(fg=6, bg=4))
        self.assertEqual(199, self.colors.curses_color_pair_number(fg=7, bg=4))

        self.assertEqual(208, self.colors.curses_color_pair_number(fg=0, bg=5))
        self.assertEqual(209, self.colors.curses_color_pair_number(fg=1, bg=5))
        self.assertEqual(210, self.colors.curses_color_pair_number(fg=2, bg=5))
        self.assertEqual(211, self.colors.curses_color_pair_number(fg=3, bg=5))
        self.assertEqual(212, self.colors.curses_color_pair_number(fg=4, bg=5))
        self.assertEqual(213, self.colors.curses_color_pair_number(fg=5, bg=5))
        self.assertEqual(214, self.colors.curses_color_pair_number(fg=6, bg=5))
        self.assertEqual(215, self.colors.curses_color_pair_number(fg=7, bg=5))

        self.assertEqual(224, self.colors.curses_color_pair_number(fg=0, bg=6))
        self.assertEqual(225, self.colors.curses_color_pair_number(fg=1, bg=6))
        self.assertEqual(226, self.colors.curses_color_pair_number(fg=2, bg=6))
        self.assertEqual(227, self.colors.curses_color_pair_number(fg=3, bg=6))
        self.assertEqual(228, self.colors.curses_color_pair_number(fg=4, bg=6))
        self.assertEqual(229, self.colors.curses_color_pair_number(fg=5, bg=6))
        self.assertEqual(230, self.colors.curses_color_pair_number(fg=6, bg=6))
        self.assertEqual(231, self.colors.curses_color_pair_number(fg=7, bg=6))

        self.assertEqual(240, self.colors.curses_color_pair_number(fg=0, bg=7))
        self.assertEqual(241, self.colors.curses_color_pair_number(fg=1, bg=7))
        self.assertEqual(242, self.colors.curses_color_pair_number(fg=2, bg=7))
        self.assertEqual(243, self.colors.curses_color_pair_number(fg=3, bg=7))
        self.assertEqual(244, self.colors.curses_color_pair_number(fg=4, bg=7))
        self.assertEqual(245, self.colors.curses_color_pair_number(fg=5, bg=7))
        self.assertEqual(246, self.colors.curses_color_pair_number(fg=6, bg=7))
        self.assertEqual(247, self.colors.curses_color_pair_number(fg=7, bg=7))

    def test__strip_hash(self):
        self.assertEqual("ffffff", self.colors.strip_hash("#ffffff"))
        self.assertEqual("ffffff", self.colors.strip_hash("ffffff"))

    def test_rgb_hex_to_list_int(self):
        self.assertEqual([255, 255, 255], self.colors.rgb_hex_to_list_int("#FFFFFF"))
        self.assertEqual([238, 238, 238], self.colors.rgb_hex_to_list_int("#EEEEEE"))
        self.assertEqual([0, 0, 255], self.colors.rgb_hex_to_list_int("#0000FF"))
        self.assertEqual([0, 255, 0], self.colors.rgb_hex_to_list_int("#00FF00"))
        self.assertEqual([255, 0, 0], self.colors.rgb_hex_to_list_int("#FF0000"))
        self.assertEqual([0, 0, 0], self.colors.rgb_hex_to_list_int("#000000"))

    def test_rgb_to_ansi16(self):
        self.colors.itu_recommendation = 'CUSTOM'
        # Black
        self.assertEqual(0, self.colors.rgb_to_ansi16(r=0, g=0, b=0))
        # Red
        self.assertEqual(1, self.colors.rgb_to_ansi16(r=170, g=0, b=0))
        # Green
        self.assertEqual(2, self.colors.rgb_to_ansi16(r=0, g=170, b=0))
        # YELLOW
        self.assertEqual(3, self.colors.rgb_to_ansi16(r=170, g=128, b=0))
        # BLUE
        self.assertEqual(4, self.colors.rgb_to_ansi16(r=0, g=0, b=170))
        # MAGENTA
        self.assertEqual(5, self.colors.rgb_to_ansi16(r=170, g=0, b=170))
        # CYAN
        self.assertEqual(6, self.colors.rgb_to_ansi16(r=0, g=170, b=170))
        # WHITE
        self.assertEqual(7, self.colors.rgb_to_ansi16(r=170, g=170, b=170))

        # BRIGHT
        self.assertEqual(0, self.colors.rgb_to_ansi16(r=0, g=0, b=0))
        # RED BRIGHT
        self.assertEqual(1, self.colors.rgb_to_ansi16(r=255, g=85, b=85))
        # GREEN BRIGHT
        self.assertEqual(2, self.colors.rgb_to_ansi16(r=85, g=255, b=85))
        # YELLOW BRIGHT
        self.assertEqual(3, self.colors.rgb_to_ansi16(r=255, g=255, b=85))
        # BLUE BRIGHT
        self.assertEqual(4, self.colors.rgb_to_ansi16(r=85, g=85, b=255))
        # MAGENTA BRIGHT
        self.assertEqual(5, self.colors.rgb_to_ansi16(r=255, g=85, b=255))
        # CYAN BRIGHT
        self.assertEqual(6, self.colors.rgb_to_ansi16(r=85, g=255, b=255))
        # WHITE BRIGHT
        self.assertEqual(7, self.colors.rgb_to_ansi16(r=255, g=255, b=255))

    def test_rgb_to_hsp(self):
        self.assertEqual(1048576, self.colors.rgb_to_curses_attributes(r=0, g=0, b=0))
        self.assertEqual(2097152, self.colors.rgb_to_curses_attributes(r=127, g=127, b=127))
        self.assertEqual(2097152, self.colors.rgb_to_curses_attributes(r=255, g=255, b=255))

    def test_hex_rgb_to_curses(self):
        self.assertEqual(
            2131712,
            self.colors.hex_rgb_to_curses(fg='#FFFFFFF', bg='000000')
        )
        self.assertEqual(
            33792,
            self.colors.hex_rgb_to_curses(fg='#0000FF', bg='000000')
        )
        self.assertEqual(
            1110016,
            self.colors.hex_rgb_to_curses(fg='#000000', bg='FFFFFFF')
        )

        self.assertEqual(
            2160384,
            self.colors.hex_rgb_to_curses(fg=None, bg='FFFFFFF')
        )

        self.assertEqual(
            1081344,
            self.colors.hex_rgb_to_curses(fg='#000000', bg=None)
        )

        self.assertRaises(TypeError, self.colors.hex_rgb_to_curses, fg=42, bg='424242')
        self.assertRaises(TypeError, self.colors.hex_rgb_to_curses, fg='424242', bg=42)

    def test_color(self):
        self.assertEqual(
            2131712,
            self.colors.color()
        )
        self.assertEqual(
            2131712,
            self.colors.color(fg=(255, 255, 255), bg=(0, 0, 0))
        )

        self.assertRaises(TypeError, self.colors.color, 42, (0, 0, 0), True)
        self.assertRaises(TypeError, self.colors.color, (0, 0, 0), 42, True)
        self.assertRaises(TypeError, self.colors.color, (0, 0, 0), (0, 0, 0), 42)


if __name__ == '__main__':
    unittest.main()
