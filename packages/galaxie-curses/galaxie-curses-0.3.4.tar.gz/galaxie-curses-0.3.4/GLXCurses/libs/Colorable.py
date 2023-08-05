#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
from GLXCurses import GLXC
import GLXCurses


class Colorable(object):
    def __init__(self):
        self.__color_normal = None
        self.__color_prelight = None
        self.__background_color_normal = None
        self.__foreground_color_normal = None
        self.__background_color_prelight = None
        self.__foreground_color_prelight = None

    @property
    def background_color_normal(self):
        """
        Get the background color

        If set to None, return a default value

        :return: the background color
        :rtype: str or None
        """

        if self.__background_color_normal:
            return self.__background_color_normal

        return GLXCurses.Application().style.attribute_to_rgb("bg", "STATE_NORMAL")

    @background_color_normal.setter
    def background_color_normal(self, value=None):
        """
        Set the ``background_color_normal`` property value

        Allowed colors: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN,WHITE, ORANGE, PINK, GRAY

        If set to None, the internal GLXCurses.Style will take precedence

        :param value: the background color
        :type value: tuple or None
        """
        if value is not None and type(value) != tuple:
            raise TypeError('"background_color_normal" value must be a tuple or None')

        if value is None:
            if self.background_color_normal is not None:
                self.__background_color_normal = None
                return
        if value is not None and self.background_color_normal != value:
            self.__background_color_normal = value

    @property
    def background_color_prelight(self):
        """
        Get the background color or GLXCurses.Style if not set

        :return: the background color
        :rtype: str or None
        """

        if self.__background_color_prelight:
            return self.__background_color_prelight

        return GLXCurses.Application().style.attribute_to_rgb("bg", "STATE_PRELIGHT")

    @background_color_prelight.setter
    def background_color_prelight(self, value=None):
        """
        Set the ``background_color_prelight`` property value

        If set to None, return a default value

        :param value: the background color for prelight state
        :type value: tuple or None
        """
        if value is not None and type(value) != tuple:
            raise TypeError('"background_color_prelight" value must be a str or None')

        if value is None:
            if self.background_color_prelight is not None:
                self.__background_color_prelight = None
                return
        if value is not None and self.background_color_prelight != value:
            self.__background_color_prelight = value

    @property
    def foreground_color_normal(self):
        if self.__foreground_color_normal:
            return self.__foreground_color_normal

        # if isinstance(self.__class__, GLXCurses.Button):
        #     return GLXCurses.application.style.get_color_text('text', 'STATE_NORMAL')

        return GLXCurses.Application().style.attribute_to_rgb("text", "STATE_NORMAL")

    @foreground_color_normal.setter
    def foreground_color_normal(self, value=None):
        """
        Set the ``foreground_color_normal`` property value

        Allowed colors:  BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN,WHITE, ORANGE, PINK, GRAY

        If set to None, the internal GLXCurses.Style will take precedence

        :param value: the foreground color
        :type value: tuple or None
        """
        if value is not None and type(value) != tuple:
            raise TypeError('"foreground_color_normal" value must be a str or None')

        if value is None:
            if self.foreground_color_normal is not None:
                self.__foreground_color_normal = None
                return
        if value is not None and self.foreground_color_normal != value:
            self.__foreground_color_normal = value

    @property
    def foreground_color_prelight(self):
        if self.__foreground_color_prelight:
            return self.__foreground_color_prelight

        # if isinstance(self.__class__, GLXCurses.Button):
        #     return 'BLACK'

        return GLXCurses.Application().style.attribute_to_rgb("text", "STATE_PRELIGHT")

    @foreground_color_prelight.setter
    def foreground_color_prelight(self, value=None):
        """
        Set the ``foreground_color_prelight`` property value

        If set to None, the internal GLXCurses.Style will take precedence

        :param value: the foreground color
        :type value: tuple or None
        """
        if value is not None and type(value) != tuple:
            raise TypeError('"foreground_color_prelight" value must be a tuple or None')

        if value is None:
            if self.foreground_color_prelight is not None:
                self.__foreground_color_prelight = None

        if value is not None and self.foreground_color_prelight != value:
            self.__foreground_color_prelight = value

    @property
    def color_normal(self):
        if self.__color_normal is not None:
            return self.__color_normal

        return GLXCurses.Application().style.color(
            fg=self.foreground_color_normal, bg=self.background_color_normal
        )

    @color_normal.setter
    def color_normal(self, value=None):
        if value is not None and type(value) != int:
            raise TypeError('"color_normal" value must be a int type or None')

        if value is None:
            if self.__color_normal is not None:
                self.__color_normal = None
                return
        if value is not None and self.__color_normal != value:
            self.__color_normal = value

    @property
    def color_prelight(self):
        if self.__color_prelight is not None:
            return self.__color_prelight
        return GLXCurses.Application().style.color(
            fg=self.foreground_color_prelight, bg=self.background_color_prelight
        )

    @color_prelight.setter
    def color_prelight(self, value=None):
        if value is not None and type(value) != int:
            raise TypeError('"color_prelight" value must be a int type or None')

        if value is None:
            if self.__color_prelight is not None:
                self.__color_prelight = None
                return
        if value is not None and self.__color_prelight != value:
            self.__color_prelight = value

    @property
    def color_insensitive(self):
        return self.color_normal | GLXC.A_DIM
