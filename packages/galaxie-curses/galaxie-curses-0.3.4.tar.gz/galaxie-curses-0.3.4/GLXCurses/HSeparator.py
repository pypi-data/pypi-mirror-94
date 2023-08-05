#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses


class HSeparator(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        """
        The GLXCurses.HSeparator widget is a horizontal separator, used to visibly separate the widgets within a \
        window.

        It displays a horizontal line.
        """
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

    def draw_widget_in_area(self):
        self.preferred_height = 1
        self.preferred_width = self.width
        self.check_position()

        self.add_horizontal_line(
            y=self.y_offset,
            x=self.x_offset,
            character=curses.ACS_HLINE,
            length=self.preferred_width - self.x_offset,
            color=self.color_normal,
        )
