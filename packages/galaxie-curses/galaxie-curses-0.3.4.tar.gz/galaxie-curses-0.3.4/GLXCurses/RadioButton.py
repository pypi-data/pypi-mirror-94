#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import logging


class RadioButton(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # Internal Widget Setting
        self.__text = None

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.sensitive = True
        self.states_list = None

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

        self.connect("MOUSE_EVENT", RadioButton._handle_mouse_event)
        self.connect("CURSES", RadioButton._handle_key_event)

    @property
    def active(self):
        return self.state["ACTIVE"]

    @active.setter
    def active(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"active" value must be a bool type or None')
        if self.active != value:
            self.state["ACTIVE"] = value

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
    def interface(self, active="(*) ", unactivated="( ) "):
        if self.active:
            return active
        return unactivated

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
        self.preferred_width = len(self.interface)
        if self.text:
            self.preferred_width += len(self.text)
        self.preferred_height = 1
        self.check_justification()
        self.check_position()

        # self.create_or_resize()
        if (
            self.text
            and len(
                GLXCurses.resize_text(self.text, self.width - len(self.interface), "~")
            )
            > 0
        ):
            self.add_string(
                y=self.y_offset, x=self.x_offset, text=self.interface, color=self.color
            )

            message_to_display = GLXCurses.resize_text(
                self.text, self.width - len(self.interface), "~"
            )
            self.add_string(
                y=self.y_offset,
                x=self.x_offset + len(self.interface),
                text=message_to_display,
                color=self.color,
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
                if event == curses.BUTTON1_PRESSED:
                    self.emit("button-pressed-event", {"id": self.id})
                elif event == curses.BUTTON1_RELEASED:
                    self.emit("button-release-event", {"id": self.id})
                    self.emit("activate", {"id": self.id})
                if event == curses.BUTTON1_CLICKED:
                    self.emit("button-pressed-event", {"id": self.id})
                    self.emit("button-release-event", {"id": self.id})
                    self.emit("activate", {"id": self.id})

                if (
                    event == 134217728
                    or event == 2097152
                    or event == 524288
                    or event == 65536
                ):
                    # GLXCurses.Application().has_default = self.id
                    # GLXCurses.Application().has_prelight = self.id
                    self.active = not self.active
                    self.emit("CLAIM_PRELIGHT", {"id": self.id})
                    self.emit("CLAIM_DEFAULT", {"id": self.id})

                if event == curses.BUTTON1_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON1_TRIPLE_CLICKED:
                    pass

                if event == 524288 or event == 134217728:
                    self.emit("activate", {"id": self.id})
                    self.emit("CLAIM_DEFAULT", {"id": self.id})

                self.emit(
                    self.curses_mouse_states[event],
                    {
                        "class": self.__class__.__name__,
                        "label": self.text,
                        "id": self.id,
                    },
                )

        else:
            if self.debug:
                logging.debug(
                    "{0} -> id:{1}, object:{2}, is not sensitive".format(
                        self.__class__.__name__, self.id, self
                    )
                )

    def _handle_key_event(self, event_signal, *event_args):  # pragma: no cover
        # Check if we have to care about keyboard event
        if (
            self.sensitive
            and isinstance(GLXCurses.Application().has_default, GLXCurses.ChildElement)
            and GLXCurses.Application().has_default.id == self.id
        ):
            # setting
            key = event_args[0]

            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.emit("RELEASE_FOCUS", {"id": self.id})
                self.emit("RELEASE_DEFAULT", {"id": self.id})
                self.emit("RELEASE_PRELIGHT", {"id": self.id})

            if key == ord(" "):
                self.emit("activate", {"id": self.id})
                self.emit("CLAIM_DEFAULT", {"id": self.id})
