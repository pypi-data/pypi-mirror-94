#!/usr/bin/env python

# https://www.linuxjournal.com/content/about-ncurses-colors-0
# https://gist.github.com/ifonefox/6046257
# https://invisible-island.net/ncurses/ncurses-slang.html
# xterms (8-color with 64-color pairs and 16-color with 256-color pairs) and non-color vt100/vt220.

import curses
import re
import math


class Colors(object):
    def __init__(self):
        self.__itu_recommendation = None
        self.itu_recommendation = 'BT.601'

        self.curses_color_pairs_init()

    @property
    def itu_recommendation(self):
        """
        Get ``itu_recommendation`` property value

        Where:

        https://en.wikipedia.org/wiki/ITU-R

        https://en.wikipedia.org/wiki/Rec._601

        https://en.wikipedia.org/wiki/Rec._709

        https://en.wikipedia.org/wiki/Rec._2100

        Allowed Value: 'BT.601', 'BT.709', 'BT.2100'
        Default Value: 'BT.601'

        :return: itu_recommendation property value
        :rtype: str
        """
        return self.__itu_recommendation

    @itu_recommendation.setter
    def itu_recommendation(self, value=None):
        if value is None:
            value = 'BT.601'
        if type(value) != str:
            raise TypeError("'itu_recommendation' property value must be a str or None")
        if value not in ['BT.601', 'BT.709', 'BT.2100', 'CUSTOM']:
            raise ValueError("'itu_recommendation' property value must be 'BT.601', 'BT.709' or 'BT.2100'")

        if self.itu_recommendation != value:
            self.__itu_recommendation = value

    @property
    def color_detection_value(self):
        return {
            curses.COLOR_BLACK: {"itu": "BT.601", "dim": 0.06, 'normal': 0.33},
            curses.COLOR_BLUE: {"itu": "CUSTOM", "dim": 0.45, 'normal': 0.6},
            curses.COLOR_GREEN: {"itu": "BT.601", "dim": 0.45, 'normal': 0.75},
            curses.COLOR_CYAN: {"itu": "BT.709", "dim": 0.777, 'normal': 0.894},
            curses.COLOR_RED: {"itu": "CUSTOM", "dim": 0.45, 'normal': 0.6},
            curses.COLOR_MAGENTA: {"itu": "CUSTOM", "dim": 0.45, 'normal': 0.69},
            curses.COLOR_YELLOW: {"itu": "BT.709", "dim": 0.715, 'normal': 0.921},
            curses.COLOR_WHITE: {"itu": "BT.601", "dim": 0.561, 'normal': 0.891},
        }

    @staticmethod
    def curses_color(color):
        """
        A "translation" function that converts standard-intensity CGA color numbers (0 to 7) to curses color numbers,
        using the curses constant names like COLOR_BLUE or COLOR_RED

        :param color:
        :return: curses.COLOR
        """
        return 7 & color

    @staticmethod
    def curses_color_pair_number(fg, bg):
        """
        A function to set an integer bit pattern based on the classic color byte

        :param fg: Forground color
        :type fg: int
        :param bg: Background color
        :type bg: int
        """
        return 1 << 7 | (7 & bg) << 4 | 7 & fg

    def curses_color_pairs_init(self):
        """
        It function create all possible color pairs

        :return:
        """
        if curses.has_colors():
            curses.start_color()
        try:
            curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
            for bg in [0, 1, 2, 3, 4, 5, 6, 7]:
                for fg in [0, 1, 2, 3, 4, 5, 6, 7]:
                    curses.init_pair(self.curses_color_pair_number(fg, bg),
                                     self.curses_color(fg),
                                     self.curses_color(bg)
                                     )
        except curses.error:
            curses.use_default_colors()

    @staticmethod
    def strip_hash(str_rgb):
        """
        Strip leading `#` if exists.

        :param str_rgb: the str it contain a # or not
        :type str_rgb: str
        :return: a str without #
        :rtype: str
        """
        if str_rgb.startswith('#'):
            return str_rgb.lstrip('#')
        return str_rgb

    def get_luma_component_rgb(self, r, g, b):
        # HSP  where the P stands for Perceived brightness
        # http://alienryderflex.com/hsp.html
        # Back to double
        r /= 255.0
        g /= 255.0
        b /= 255.0
        if self.itu_recommendation == 'BT.2100':
            # BT.2100
            return math.sqrt(r * r * 0.2627 + g * g * 0.6780 + b * b * 0.0593)
        if self.itu_recommendation == 'BT.709':
            # BT.709
            return math.sqrt(r * r * 0.2126 + g * g * 0.7152 + b * b * 0.0722)
        if self.itu_recommendation == 'BT.601':
            # BT.601
            return math.sqrt(r * r * 0.299 + g * g * 0.587 + b * b * 0.114)
        if self.itu_recommendation == 'CUSTOM':
            # More Blue
            return math.sqrt(r * r * 0.2627 + g * g * 0.7152 + b * b * 0.246)

    @staticmethod
    def rgb_to_ansi16(r, g, b):
        return (round(b / 255) << 2) | (round(g / 255) << 1) | round(r / 255)

    def rgb_to_curses_attributes(self, r, g, b):

        ansi_color = self.rgb_to_ansi16(r, g, b)
        self.itu_recommendation = self.color_detection_value[ansi_color]['itu']
        luma_component = self.get_luma_component_rgb(r, g, b)

        if luma_component <= self.color_detection_value[ansi_color]['dim']:
            return 1048576
        elif luma_component <= self.color_detection_value[ansi_color]['normal']:
            return 0
        else:
            return 2097152

    def rgb_hex_to_list_int(self, str_rgb):
        return [int(h, 16) for h in re.split(r'(..)(..)(..)', self.strip_hash(str_rgb))[1:4]]

    # Entry point           
    def color(self, fg=None, bg=None, attributes=None):
        """
        Convert a RGB value to a directly usable curses color

        draw(y, x, "Hello", color) where the return of it function is directly usable

        :return: color.pair | curses.Attribut
        :rtype: int
        """
        if fg is None:
            fg = (255, 255, 255)

        if bg is None:
            bg = (0, 0, 0)
        if attributes is None:
            attributes = True

        if type(fg) != tuple:
            raise TypeError("'fg' argument value must be a tuple type or None")

        if type(bg) != tuple:
            raise TypeError("'bg' argument value must be a tuple type or None")

        if type(attributes) != bool:
            raise TypeError("'attributes' argument value must be a bool type or None")

        if attributes:
            return curses.color_pair(
                self.curses_color_pair_number(
                    fg=self.rgb_to_ansi16(fg[0], fg[1], fg[2]),
                    bg=self.rgb_to_ansi16(bg[0], bg[1], bg[2])
                )
            ) | self.rgb_to_curses_attributes(fg[0], fg[1], fg[2])
        else:
            return curses.color_pair(
                self.curses_color_pair_number(
                    fg=self.rgb_to_ansi16(fg[0], fg[1], fg[2]),
                    bg=self.rgb_to_ansi16(bg[0], bg[1], bg[2])
                )
            )

    def hex_rgb_to_curses(self, fg=None, bg=None):
        """
        Convert a RGB value to a directly usable curses color

        draw(y, x, "Hello", color) where the return of it function is directly usable

        bg='#000000', FG='#FFFFFF'

        :return: color.pair | curses.Attribut
        :rtype: int
        """
        if fg is None:
            fg = 'FFFFFF'
        if bg is None:
            bg = '000000'

        if type(fg) != str:
            raise TypeError("'fg' argument value must be a str or None")
        if type(bg) != str:
            raise TypeError("'bg' argument value must be a str or None")

        fg = self.rgb_hex_to_list_int(self.strip_hash(fg))
        bg = self.rgb_hex_to_list_int(self.strip_hash(bg))

        return curses.color_pair(
            self.curses_color_pair_number(
                fg=self.rgb_to_ansi16(fg[0], fg[1], fg[2]),
                bg=self.rgb_to_ansi16(bg[0], bg[1], bg[2])
            )
        ) | self.rgb_to_curses_attributes(fg[0], fg[1], fg[2])
