#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class VBox(GLXCurses.Box, GLXCurses.Dividable):
    def __init__(self):
        # Load heritage
        GLXCurses.Box.__init__(self)
        GLXCurses.Dividable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.VBox"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.preferred_height = 2
        self.preferred_width = 2

        # Default Value
        self.spacing = 0
        self.homogeneous = True

    def new(self, homogeneous=True, spacing=None):
        """
        Creates a new GLXCurses :class:`VBox <GLXCurses.VBox.VBox>`

        :param homogeneous: True if all children are to be given equal space allotments.
        :type homogeneous: bool
        :param spacing: The number of characters to place by default between children.
        :type spacing: int
        :return: a new :class:`VBox <GLXCurses.VBox.VBox>`.
        :raise TypeError: if ``homogeneous`` is not bool type
        :raise TypeError: if ``spacing`` is not int type or None
        """
        if type(homogeneous) != bool:
            raise TypeError('"homogeneous" argument must be a bool type')
        if spacing is not None:
            if type(spacing) != int:
                raise TypeError('"spacing" must be int type or None')

        self.__init__()
        self.spacing = GLXCurses.clamp_to_zero(spacing)
        self.homogeneous = homogeneous
        return self

    def draw_widget_in_area(self):
        # in case it have children attach to the widget.
        if self.children:

            self.start = self.y
            self.stop = self.height
            self.num = len(self.children)
            self.round_type = GLXCurses.GLXC.ROUND_DOWN

            # for each children
            for child in self.children:
                child.widget.stdscr = self.stdscr
                # Get position dictionary like: {'0': (0, 32), '1': (33, 65), '2': (66, 99)}
                start, stop = self.split_positions[
                    "{0}".format(child.properties.position)
                ]
                child.widget.y = start
                child.widget.x = self.x
                child.widget.width = self.width

                # # If that the last element it finish to end
                if child.properties.position == len(self.children) - 1:
                    if self.get_decorated():
                        child.widget.height = self.height - child.widget.y + 1
                    else:
                        child.widget.height = self.height - child.widget.y
                else:
                    child.widget.height = stop - start + 1

                child.widget.draw_widget_in_area()
