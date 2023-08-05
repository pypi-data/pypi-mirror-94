#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import logging
import curses


class Menu(GLXCurses.Window, GLXCurses.Movable, GLXCurses.Box):
    def __init__(self):
        # Load heritage
        GLXCurses.Window.__init__(self)
        GLXCurses.Box.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.glxc_type = "GLXCurses.{0}".format(self.__class__.__name__)
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # self.selected_menu_item = 0

        # Default Setting
        self.decorated = True

        # Subscription
        self.connect("BUTTON1_CLICKED", Menu._handle_mouse_event)  # Mouse Button
        self.connect("BUTTON1_RELEASED", Menu._handle_mouse_event)
        # Keyboard
        self.connect("CURSES", Menu._handle_key_event)

        self.debug = True

    def _handle_mouse_event(self, event_signal, event_args=None):
        if event_args is None:
            event_args = {}

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.can_focus and self.has_focus:
            # setting
            key = event_args[0]
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.emit("RELEASE_FOCUS", {"id": self.id})
                self.emit("RELEASE_DEFAULT", {"id": self.id})
                self.emit("RELEASE_FOCUS", {"id": self.id})

    def _update_preferred_sizes(self):
        self.preferred_width = GLXCurses.clamp(
            self._get_estimated_preferred_width(), 0, self.width
        )
        self.preferred_height = GLXCurses.clamp(
            self._get_estimated_preferred_height(), 0, self.height
        )

    def _get_estimated_preferred_width(self):
        """
        Estimate a preferred width, by consider X Location, allowed width

        :return: a estimated preferred width
        :rtype: int
        """
        estimated_preferred_width = 0
        if self.decorated:
            estimated_preferred_width += 3

        content_area_width = 0
        if self.children:
            for child in self.children:
                if child.widget.preferred_width > content_area_width:
                    content_area_width = child.widget.preferred_width

        if self.title:
            estimated_preferred_width += max(content_area_width, len(self.title))
        else:
            estimated_preferred_width += max(content_area_width, 0)

        return estimated_preferred_width

    def _get_estimated_preferred_height(self):
        """
        Estimate a preferred height, by consider Y Location

        :return: a estimated preferred height
        :rtype: int
        """
        estimated_preferred_height = 0
        if self.decorated:
            estimated_preferred_height += 2
        if self.children:
            for _ in self.children:
                estimated_preferred_height += 1

        return estimated_preferred_height

    @property
    def color(self):
        return self.style.color(fg=(255, 255, 255), bg=self.background_color_prelight, attributes=False)

    def draw_widget_in_area(self):
        # Create the subwin
        self._update_preferred_sizes()

        # Draw the child.
        if self.children is not None:
            self.draw_background()

            box_spacing = 0
            if self.decorated:
                self._draw_box()
                box_spacing += 2

            count = 0
            for child in self.children:
                if count < self.preferred_height - box_spacing:
                    child.widget.parent = self
                    child.widget.stdscr = self.stdscr

                    if self.decorated:
                        child.widget.x = self.x_offset + 1
                        if self.parent and isinstance(self.parent, GLXCurses.MenuBar):
                            child.widget.y = (
                                    self.y_offset + 1 + child.properties.position + 1
                            )
                        else:
                            child.widget.y = (
                                    self.y_offset + 1 + child.properties.position
                            )
                        child.widget.width = self.preferred_width - 2
                        child.widget.height = self.preferred_height - 2

                    else:
                        child.widget.x = self.x_offset
                        if self.parent and isinstance(self.parent, GLXCurses.MenuBar):
                            child.widget.y = (
                                    self.y_offset + child.properties.position + 1
                            )
                        else:
                            child.widget.y = self.y_offset + child.properties.position
                        child.widget.width = self.preferred_width - 1
                        child.widget.height = self.preferred_height - 1

                    if self.debug:
                        logging.debug(
                            "Set child -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                                child.widget.x,
                                child.widget.y,
                                child.widget.width,
                                child.widget.height,
                            )
                        )

                    child.widget.draw()
                count += 1

    # def draw_background(self, fg='BLACK', bg='CYAN'):
    #     for y_inc in range(self.y_offset, self.y_offset + self.preferred_height):
    #         for x_inc in range(self.x_offset, self.x_offset + self.preferred_width):
    #             self.add_character(
    #                 y=y_inc,
    #                 x=x_inc,
    #                 character=' ',
    #                 color=self.style.color(fg=fg, bg=bg)
    #             )

    def _draw_title(self):
        pass

    def _draw_box(self):
        # Create a box and add the name of the windows like a king, who trust that !!!
        if self.decorated:
            # Bottom
            for x_inc in range(
                    self.x_offset + 1, self.x_offset + self.preferred_width - 1
            ):
                self.add_character(
                    y=self.y_offset + self.preferred_height - 1,
                    x=x_inc,
                    character=curses.ACS_HLINE,
                    color=self.color,
                )

            # Top
            for x_inc in range(
                    self.x_offset + 1, self.x_offset + self.preferred_width - 1
            ):
                self.add_character(
                    y=self.y_offset,
                    x=x_inc,
                    character=curses.ACS_HLINE,
                    color=self.color,
                )

            # Right side
            for y_inc in range(0 + 1, self.preferred_height - 1):
                self.add_character(
                    y=self.y_offset + y_inc,
                    x=self.x_offset + self.preferred_width - 1,
                    character=curses.ACS_VLINE,
                    color=self.color,
                )

            # Left side
            for y_inc in range(0 + 1, self.preferred_height - 1):
                self.add_character(
                    y=self.y_offset + y_inc,
                    x=self.x_offset,
                    character=curses.ACS_VLINE,
                    color=self.color,
                )

            # Upper-right corner
            self.add_character(
                y=self.y_offset,
                x=self.preferred_width + self.x_offset - 1,
                character=curses.ACS_URCORNER,
                color=self.color,
            )

            # Upper-left corner
            self.add_character(
                y=self.y_offset,
                x=self.x_offset,
                character=curses.ACS_ULCORNER,
                color=self.color,
            )

            # Bottom-right corner
            self.add_character(
                y=self.y_offset + self.preferred_height - 1,
                x=self.x_offset + self.preferred_width - 1,
                character=curses.ACS_LRCORNER,
                color=self.color,
            )

            # Bottom-left corner
            self.add_character(
                y=self.y_offset + self.preferred_height - 1,
                x=self.x_offset,
                character=curses.ACS_LLCORNER,
                color=self.color,
            )

            # Bottom-left tee_pointing_right
            self.add_character(
                y=self.y_offset + self.preferred_height - 4,
                x=self.x_offset + 1,
                character=curses.ACS_LTEE,
                color=self.color,
            )

            # Bottom-right corner
            self.add_character(
                y=self.y_offset + self.preferred_height - 4,
                x=self.x_offset + self.preferred_width - 2,
                character=curses.ACS_RTEE,
                color=self.color,
            )

            # Bottom
            for x_inc in range(
                    self.x_offset + 2, self.x_offset + self.preferred_width - 2
            ):
                self.add_character(
                    y=self.y_offset + self.preferred_height - 4,
                    x=x_inc,
                    character=curses.ACS_HLINE,
                    color=self.color,
                )

    @staticmethod
    def remove_accel_group():
        pass

    @staticmethod
    def add_accel_group():
        pass
