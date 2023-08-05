#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# Inspired by: https://developer.gnome.org/gtk3/stable/GtkButton.html

import GLXCurses
import curses
import logging


class Button(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.__relief = None
        self.__text = None
        self.__interface_normal = None
        self.__interface_selected = None

        self.interface_normal = None
        self.interface_selected = None

        self.can_default = True
        self.can_focus = True
        self.sensitive = True

        self.connect("MOUSE_EVENT", self.__class__._handle_mouse_event)
        self.connect("CURSES", self.__class__._handle_key_event)
        self.curses_mouse_states = {
            GLXCurses.GLXC.BUTTON1_PRESSED: "BUTTON1_PRESS",
            GLXCurses.GLXC.BUTTON1_RELEASED: "BUTTON1_RELEASED",
            GLXCurses.GLXC.BUTTON1_CLICKED: "BUTTON1_CLICKED",
            GLXCurses.GLXC.BUTTON1_DOUBLE_CLICKED: "BUTTON1_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON1_TRIPLE_CLICKED: "BUTTON1_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON2_PRESSED: "BUTTON2_PRESSED",
            GLXCurses.GLXC.BUTTON2_RELEASED: "BUTTON2_RELEASED",
            GLXCurses.GLXC.BUTTON2_CLICKED: "BUTTON2_CLICKED",
            GLXCurses.GLXC.BUTTON2_DOUBLE_CLICKED: "BUTTON2_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON2_TRIPLE_CLICKED: "BUTTON2_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON3_PRESSED: "BUTTON3_PRESSED",
            GLXCurses.GLXC.BUTTON3_RELEASED: "BUTTON3_RELEASED",
            GLXCurses.GLXC.BUTTON3_CLICKED: "BUTTON3_CLICKED",
            GLXCurses.GLXC.BUTTON3_DOUBLE_CLICKED: "BUTTON3_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON3_TRIPLE_CLICKED: "BUTTON3_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON4_PRESSED: "BUTTON4_PRESSED",
            GLXCurses.GLXC.BUTTON4_RELEASED: "BUTTON4_RELEASED",
            GLXCurses.GLXC.BUTTON4_CLICKED: "BUTTON4_CLICKED",
            GLXCurses.GLXC.BUTTON4_DOUBLE_CLICKED: "BUTTON4_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON4_TRIPLE_CLICKED: "BUTTON4_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON_SHIFT: "BUTTON_SHIFT",
            GLXCurses.GLXC.BUTTON_CTRL: "BUTTON_CTRL",
            GLXCurses.GLXC.BUTTON_ALT: "BUTTON_ALT",
        }

        self.color_prelight = self.style.color(
            fg=self.style.attribute_to_rgb("base", "STATE_PRELIGHT"),
            bg=self.style.attribute_to_rgb("dark", "STATE_NORMAL"),
            attributes=False
        ) | GLXCurses.GLXC.A_REVERSE

    # @property
    # def relief(self):
    #     """
    #     The border relief style.
    #
    #     :return:
    #     """
    #     return self.__relief

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.__text != value:
            self.__text = value
            self.preferred_width = len(self.text) + len(self.interface)

    @property
    def interface_normal(self):
        """
        Get the ``interface_normal`` property value

        It property is use for display a chars around the button when the widget has default

        Default Value: "[  ]"

        :return: ``interface_normal`` property value
        :rtype: str
        """
        return self.__interface_normal

    @interface_normal.setter
    def interface_normal(self, value=None):
        """
        Get the ``interface_normal`` property value

        It property is use for display a chars around the button when the widget haven't default

        :param value: ``interface_normal`` property value
        :type value: str or None
        :raise TypeError: When ``interface_normal`` property value is not a str type or None
        """
        if value is None:
            value = "[  ]"
        if type(value) != str:
            raise TypeError("'interface_normal' property value must be a str typ eor None")
        if self.interface_normal != value:
            self.__interface_normal = value

    @property
    def interface_selected(self):
        """
        Get the ``interface_selected`` property value

        It property is use for display a chars around the button when the widget has default

        Default Value: "[<>]"

        :return: ``interface_selected`` property value
        :rtype: str
        """
        return self.__interface_selected

    @interface_selected.setter
    def interface_selected(self, value=None):
        """
        Get the ``interface_selected`` property value

        It property is use for display a chars around the button when the widget has default

        :param value: ``interface_selected`` property value
        :type value: str or None
        :raise TypeError: When ``interface_selected`` property value is not a str type or None
        """
        if value is None:
            value = "[<>]"
        if type(value) != str:
            raise TypeError("'selected' property value must be a str typ eor None")
        if self.interface_selected != value:
            self.__interface_selected = value

    @property
    def interface(self, normal="[  ]", selected="[<>]"):
        if (
                self.has_default
                and GLXCurses.Application().has_default
                and GLXCurses.Application().has_default.id == self.id
        ):
            return self.interface_selected
        return self.interface_normal

    @property
    def color(self):
        if not self.sensitive:
            return self.color_insensitive

        if (
                self.has_prelight
                and GLXCurses.Application().has_prelight
                and GLXCurses.Application().has_prelight.id == self.id
        ):
            return self.color_prelight

        return self.color_normal

    def draw_widget_in_area(self):

        self.preferred_width = len(self.text) + len(self.interface)
        self.preferred_height = 1
        self.check_justification()
        self.check_position()

        if (
                self.text
                and len(
            GLXCurses.resize_text(self.text, self.width - len(self.interface), "~")
        )
                > 0
        ):
            self.add_string(
                self.y_offset,
                self.x_offset,
                self.interface[: int(len(self.interface) / 2)],
                self.color,
            )

            message_to_display = GLXCurses.resize_text(
                self.text, self.width - len(self.interface), "~"
            )
            self.add_string(
                self.y_offset,
                self.x_offset + int(len(self.interface) / 2),
                message_to_display,
                self.color,
            )

            self.add_string(
                self.y_offset,
                self.x_offset + int(len(self.interface) / 2) + len(message_to_display),
                self.interface[-int(len(self.interface) / 2):],
                self.color,
            )

    def _handle_mouse_event(self, event_signal, event_args):  # pragma: no cover
        if self.sensitive:
            # Read the mouse event information's
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x

            x_pos_start = self.x_offset + len(self.interface) + len(self.text) - 1
            x_pos_stop = self.x_offset
            y_pos_start = self.y_offset
            y_pos_stop = self.y_offset - self.preferred_height + 1

            that_for_me = (
                    y_pos_start >= y >= y_pos_stop and x_pos_start >= x >= x_pos_stop
            )

            if that_for_me:
                if not self.has_focus or not self.has_default or not self.has_prelight:
                    self.emit("grab-focus", {"id": self.id})
                # BUTTON1
                if event == curses.BUTTON1_PRESSED:
                    self.emit("button-pressed-event", {"id": self.id})
                elif event == curses.BUTTON1_RELEASED:
                    self.emit("button-release-event", {"id": self.id})
                if event == curses.BUTTON1_CLICKED:
                    self.emit("button-pressed-event", {"id": self.id})
                    self.emit("button-release-event", {"id": self.id})

                if event == curses.BUTTON1_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON1_TRIPLE_CLICKED:
                    pass

                self.emit(
                    self.curses_mouse_states[event],
                    {
                        "class": self.__class__.__name__,
                        "label": self.text,
                        "id": self.id,
                    },
                )

            # else:
            #     self.emit('RELEASE_FOCUS', {'id': self.id})
            #     self.emit('RELEASE_DEFAULT', {'id': self.id})
            #     self.emit('RELEASE_PRELIGHT', {'id': self.id})
        else:
            if self.debug:
                logging.debug(
                    "{0} -> id:{1}, object:{2}, is not sensitive".format(
                        self.__class__.__name__, self.id, self
                    )
                )

    def _handle_key_event(self, event_signal, *event_args):  # pragma: no cover
        # Check if we have to care about keyboard event
        if self.sensitive and self.has_default:
            # setting
            key = event_args[0]

            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.emit("RELEASE_FOCUS", {"id": self.id})
                self.emit("RELEASE_DEFAULT", {"id": self.id})
                self.emit("RELEASE_PRELIGHT", {"id": self.id})

            if (
                    len(
                        GLXCurses.resize_text(
                            self.text, self.width - len(self.interface), "~"
                        )
                    )
                    > 0
            ):
                if key == ord(self.text[0].upper()) or key == ord(self.text[0].lower()):
                    instance = {
                        "class": self.__class__.__name__,
                        "label": self.text,
                        "id": self.id,
                    }
                    self.emit(event_signal, instance)

            if key == curses.KEY_ENTER or key == ord("\n"):
                self.emit("CLAIM_PRELIGHT", {"id": self.id})
                # Create a Dict with everything
                instance = {
                    "class": self.__class__.__name__,
                    "label": self.text,
                    "id": self.id,
                }
                self.emit(event_signal, instance)
                self.emit("RELEASE_PRELIGHT", {"id": self.id})
