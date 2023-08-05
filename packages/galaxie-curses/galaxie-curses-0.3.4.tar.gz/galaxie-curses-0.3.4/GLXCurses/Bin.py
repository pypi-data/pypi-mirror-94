#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Bin(GLXCurses.Container):
    def __init__(self):
        """
        A container with just one child

        **Description**

        The :class:`Bin <GLXCurses.Bin.Bin>` widget is a container with just one child. It is not very useful itself,
        but it is useful for deriving subclasses, since it provides common code needed for handling a single child widget.

        Many GLXCurses widgets are subclasses of :class:`Bin <GLXCurses.Bin.Bin>`, including
         * :class:`Window <GLXCurses.Window.Window>`
         * :class:`Button <GLXCurses.Button.Button>`
         * :class:`Frame <GLXCurses.Frame.Frame>`
         * :class:`HandleBox <GLXCurses.HandleBox.HandleBox>`
         * :class:`ScrolledWindow <GLXCurses.ScrolledWindow.ScrolledWindow>`
        """
        GLXCurses.Container.__init__(self)
        self.glxc_type = "GLXCurses.Bin"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

    def get_child(self):
        """
        Gets the child of the GLXCurses.Bin, or None if the bin contains no child widget.

        The returned widget does not have a reference added, so you do not need to unref it.

        :return: the child of GLXCurses.Bin , or None if it does not have a child.
        :rtype: GLXCurses.Bin or None
        """
        return self.child
