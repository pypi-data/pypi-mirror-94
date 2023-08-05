#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class ToolBar(GLXCurses.Widget):
    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.ToolBar"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.foreground_color_normal = (0, 0, 0)
        self.background_color_normal = (255, 255, 255)

        self.__labels = None
        self.labels = None

        # States
        self.can_default = True
        self.can_focus = True
        self.can_prelight = True
        self.sensitive = True
        self.states_list = None

        # Subscription
        # Mouse
        self.connect("MOUSE_EVENT", ToolBar._handle_mouse_event)
        # Keyboard
        self.connect("CURSES", ToolBar._handle_key_event)

    def draw(self):
        """
        Draw the ToolBar widget
        """
        self.init_button_positions()
        for item_number in range(0, len(self.labels)):
            if item_number <= 0:
                start = 0
                stop = self.get_button_width(0)
            else:
                start = self.labels[item_number - 1]["end_coord"]
                stop = start + self.get_button_width(item_number)

            if "text" in self.labels[item_number] and self.labels[item_number]["text"]:
                # Background
                self.add_string(
                    y=0,
                    x=start,
                    text=" " * int((stop + 1) - start),
                    color=self.color_prelight,
                )
                # Num Label
                self.add_string(
                    y=0,
                    x=start,
                    text=self.labels[item_number]["id"],
                    color=self.color_normal | GLXCurses.GLXC.A_REVERSE,
                )
                # text
                self.add_string(
                    y=0,
                    x=start + 2,
                    text=GLXCurses.resize_text(
                        text=self.labels[item_number]["text"],
                        max_width=self.get_button_width(item_number) - 2,
                    ),
                    color=self.style.color(
                        fg=self.style.attribute_to_rgb(attribute='dark', state='STATE_NORMAL'),
                        bg=self.style.attribute_to_rgb(attribute='base', state='STATE_PRELIGHT'),
                        attributes=True
                    ),
                )

    @property
    def labels(self):
        """
        Get the labels list, it contain items with dictionary with key 'id', 'text', 'end_coord'

        :return: The labels list
        :rtype: list
        """
        return self.__labels

    @labels.setter
    def labels(self, value=None):
        """
        Set the labels list

        Each list item must contain the text of a single button.

        By example:
            ['Hello','', '', '', '42'] will create 2 buttons separate by the space require for 4 buttons

        Take look on the examples directory

        :param value: the button list
        :type value: list
        :raise TypeError: if ``value`` is not a list
        """
        if value is None:
            value = []
        # Exit as soon of possible
        if type(value) != list:
            raise TypeError("'labels' must be a list type")
        self.__labels = []
        for _ in value:
            self.__labels.append({})
        for i in range(0, len(value)):
            self.set_label_text(idx=i, text=value[i])

    def init_button_positions(self):
        """
        Calculate positions of buttons; width is never less than 7

        Else distribute the extra width in a way that the middle vertical line
        (between F5 and F6) aligns with the center of the screen.

        The extra width is distributed in this order: F10, F5, F9, F4, ..., F6, F1.
        """
        pos = 0

        # calculate positions of buttons; width is never less than 7
        if self.width < len(self.labels) * 7:
            for i in range(0, len(self.labels)):
                if pos + 7 <= self.width:
                    pos += 7
                if "end_coord" not in self.labels[i] or self.labels[i][
                    "end_coord"
                ] != int(pos):
                    self.labels[i]["end_coord"] = int(pos)
        else:
            # Distribute the extra width in a way that the middle vertical line
            # (between F5 and F6) aligns with the center of the screen. The extra width
            # is distributed in this order: F10, F5, F9, F4, ..., F6, F1.

            for i in range(0, int(len(self.labels) / 2)):
                pos += int(self.width / len(self.labels))
                if int(len(self.labels) / 2) - 1 - i < int(
                        int(self.width % len(self.labels)) / 2
                ):
                    pos += 1

                if "end_coord" not in self.labels[i] or self.labels[i][
                    "end_coord"
                ] != int(pos):
                    self.labels[i]["end_coord"] = int(pos)

            for i in range(int(len(self.labels) / 2), len(self.labels)):
                pos += int(self.width / len(self.labels))

                if len(self.labels) - 1 - i < int(
                        (int(self.width % len(self.labels)) + 1) / 2
                ):
                    pos += 1

                if "end_coord" not in self.labels[i] or self.labels[i][
                    "end_coord"
                ] != int(pos):
                    self.labels[i]["end_coord"] = int(pos)

    def get_button_width(self, i=None):
        """
        return width of one button

        :param i: button number it start to 0
        :type i: int
        :return: width of one button
        :rtype: int
        :raise TypeError: When ``i`` is not a int type
        """
        if type(i) != int:
            raise TypeError("'i' must be a int value")
        if i == 0:
            return self.labels[0]["end_coord"]
        return self.labels[i]["end_coord"] - self.labels[i - 1]["end_coord"]

    def get_button_by_x_coord(self, x=None):
        """
        Return the button number by it X coordinate

        :param x: X coordinate value
        :type x: int
        :return: the button number
        :rtype: int
        :raise TypeError: When ``x`` is not a int type
        """
        if type(x) != int:
            raise TypeError("'x' must be a int value")
        for i in range(0, len(self.labels)):
            if self.labels[i]["end_coord"] > x:
                return i
        return -1

    def set_label_text(self, idx=None, text=None):
        """
        Set the text to a button

        :param idx: The button id it start by 0
        :type idx: int
        :param text: The text to set to it button
        :type text: str
        """
        if type(idx) != int:
            raise TypeError("'idx' must be a int value")
        if type(text) != str:
            raise TypeError("'text' must be a str value")

        if "text" not in self.labels[idx] or self.labels[idx]["text"] != text:
            self.labels[idx]["text"] = text
        if "id" not in self.labels[idx] or self.labels[idx]["id"] != "{0: >2}".format(
                idx + 1
        ):
            self.labels[idx]["id"] = "{0: >2}".format(idx + 1)

    def _handle_mouse_event(self, event_signal, event_args):  # pragma: no cover
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # convert mouse point of view to Area point of view
            y -= self.y
            x -= self.x

            if 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1:
                # We are sure about the ToolBar have been clicked
                if self.can_focus:
                    self.emit("CLAIM_FOCUS", {"id": self.id})
                if self.can_default:
                    self.emit("CLAIM_DEFAULT", {"id": self.id})
                if self.can_prelight:
                    self.emit("RELEASE_PRSELIGHT", {"id": self.id})

                if (
                        event == GLXCurses.GLXC.BUTTON1_CLICKED
                        or event == GLXCurses.GLXC.BUTTON1_RELEASED
                ):
                    self.emit(
                        "F{0}_CLICKED".format(self.get_button_by_x_coord(x) + 1),
                        {
                            "class": self.__class__.__name__,
                            "id": self.id,
                            "event_signal": "F{0}_CLICKED".format(
                                self.get_button_by_x_coord(x) + 1
                            ),
                        },
                    )

    def _handle_key_event(self, event_signal, *event_args):  # pragma: no cover
        # Check if we have to care about keyboard event
        if (
                isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement)
                and GLXCurses.Application().has_focus.id == self.id
        ):
            # Touch Escape
            if event_args[0] == GLXCurses.GLXC.KEY_ESC:
                self.emit("RELEASE_FOCUS", {"id": self.id})
                self.emit("RELEASE_DEFAULT", {"id": self.id})
                self.emit("RELEASE_PRELIGHT", {"id": self.id})

            if event_args[0] == GLXCurses.GLXC.KEY_F1:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F1_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)
            elif event_args[0] == GLXCurses.GLXC.KEY_F2:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F2_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)
            elif event_args[0] == GLXCurses.GLXC.KEY_F3:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F3_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F4:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F4_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F5:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F5_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F6:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F6_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F7:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F7_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F8:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F8_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F9:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F9_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)

            elif event_args[0] == GLXCurses.GLXC.KEY_F10:
                instance = {
                    "class": self.__class__.__name__,
                    "id": self.id,
                    "event_signal": "F10_PRESSED",
                }
                self.emit(str(instance["event_signal"]), instance)
