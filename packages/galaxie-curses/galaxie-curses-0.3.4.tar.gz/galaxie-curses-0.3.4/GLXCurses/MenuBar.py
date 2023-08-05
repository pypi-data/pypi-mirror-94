#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
from curses import A_BOLD, KEY_DOWN, KEY_UP
from curses import A_REVERSE
from curses import KEY_LEFT
from curses import KEY_RIGHT
from curses import BUTTON1_RELEASED
import curses


class MenuBar(GLXCurses.Box, GLXCurses.Dividable):
    def __init__(self):
        # Load heritage
        GLXCurses.Box.__init__(self)
        GLXCurses.Dividable.__init__(self)

        self.glxc_type = "GLXCurses.{0}".format(self.__class__.__name__)
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.__info_label = None
        self.__selected_menu = None
        self.__selected_menu_item = None

        # Internal Widget Setting
        self.can_focus = True
        self.can_default = True
        self.can_prelight = True
        self.spacing = 4

        self.info_label = None
        self.selected_menu = 0
        self.selected_menu_item = 0
        self.list_machin = []

        # Cab be remove
        self.debug = True

        self.color_prelight = self.style.color(
            bg=self.style.attribute_to_rgb("dark", "STATE_NORMAL"),
            fg=self.style.attribute_to_rgb("white", "STATE_NORMAL"),
            attributes=False
        )
        self.color_normal = self.style.color(
            fg=self.style.attribute_to_rgb("base", "STATE_PRELIGHT"),
            bg=self.style.attribute_to_rgb("dark", "STATE_NORMAL"),
            attributes=False
        ) | GLXCurses.GLXC.A_REVERSE
        # Subscription
        # Mouse
        self.connect("MOUSE_EVENT", MenuBar._handle_mouse_event)
        # Keyboard
        self.connect("CURSES", MenuBar._handle_key_event)

    @property
    def color(self):
        if not self.sensitive:
            return self.color_insensitive

        if self.has_prelight:
            return self.color_prelight

        return self.color_normal

    @property
    def info_label(self):
        return self.__info_label

    @info_label.setter
    def info_label(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.info_label != text:
            self.__info_label = text

    @property
    def selected_menu(self):
        return self.__selected_menu

    @selected_menu.setter
    def selected_menu(self, selected_menu=None):
        if selected_menu is not None and type(selected_menu) != int:
            raise TypeError('"selected_menu" must be a int type or None')
        if self.selected_menu != selected_menu:
            self.__selected_menu = selected_menu

    @property
    def selected_menu_item(self):
        return self.__selected_menu_item

    @selected_menu_item.setter
    def selected_menu_item(self, selected_menu_item=None):
        if selected_menu_item is None:
            selected_menu_item = 0
        if selected_menu_item is not None and type(selected_menu_item) != int:
            raise TypeError('"selected_menu_item" must be a int type or None')
        if self.selected_menu_item != selected_menu_item:
            self.__selected_menu_item = selected_menu_item

    def draw_widget_in_area(self):
        """
        White the menubar to the stdscr, the location is imposed to top left corner
        """
        self._update_sizes()
        self._update_preferred_sizes()

        self.draw_background(
            color=self.style.color(
                fg=self.style.attribute_to_rgb("base", "STATE_PRELIGHT"),
                bg=self.style.attribute_to_rgb("dark", "STATE_NORMAL"),
                attributes=False
            ) | GLXCurses.GLXC.A_REVERSE
        )
        self._draw_menu_bar()
        self._draw_info_label()

    def _update_preferred_sizes(self):
        self.preferred_height = self.height
        self.preferred_width = self.width

    def _update_sizes(self):
        self.start = self.x
        self.stop = self.width - 1
        self.num = len(self.children)
        self.round_type = GLXCurses.GLXC.ROUND_DOWN

        self._upgrade_position()

    def _upgrade_position(self):
        pos = 0
        for child in self.children:
            if child.widget.title is not None:
                self.list_machin.append(
                    {
                        "start": pos + 1,
                        "stop": pos + len(child.widget.title) + self.spacing,
                    }
                )
                pos += len(child.widget.title) + self.spacing

    def _draw_info_label(self):
        if self.info_label:
            text = GLXCurses.resize_text(self.info_label, self.width, "~")
            for x_inc in range(0, len(text)):
                try:
                    self.subwin.delch(0, self.width - len(text) + x_inc)
                    self.subwin.insstr(
                        0,
                        self.width - len(text) + x_inc,
                        text[x_inc],
                        self.color_normal,
                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_menu_bar(self):
        if self.children:
            self.start = self.x
            self.stop = self.width
            self.num = len(self.children)
            self.round_type = GLXCurses.GLXC.ROUND_DOWN

            count = 0

            for child in self.children:
                box_spacing = 0
                if child.widget.decorated:
                    box_spacing = 2
                if self.can_focus and self.has_focus:
                    if self.selected_menu is not None and self.selected_menu == count:
                        self.has_prelight = True
                        if len(child.widget.children) > 0:
                            child.widget.parent = self
                            child.widget.x = GLXCurses.Application().x
                            child.widget.y = GLXCurses.Application().y
                            child.widget.x_offset = self.list_machin[count]["start"] - 1
                            child.widget.width = self.width
                            child.widget.height = GLXCurses.clamp(
                                len(child.widget.children) + box_spacing,
                                0,
                                GLXCurses.Application().height,
                            )
                            child.widget.x_offset = GLXCurses.clamp(
                                child.widget.x_offset,
                                0,
                                self.width - child.widget.preferred_width,
                            )
                            for sub_child in child.widget.children:
                                sub_child.widget.x = child.widget.x_offset

                            child.widget.stdscr = self.stdscr
                            child.widget.draw()
                    else:
                        self.has_prelight = False
                else:
                    self.has_prelight = False

                if child.widget.title is not None:
                    title = GLXCurses.check_mnemonic_in_text(text=child.widget.title)
                    # Draw one dark before

                    self.add_character(
                        y=0,
                        x=self.list_machin[count]["start"],
                        character=" ",
                        color=self.color,
                    )
                    # Draw entire text

                    self.add_string(
                        y=0,
                        x=self.list_machin[count]["start"] + 1,
                        text=title["text"],
                        color=self.color,
                    )
                    # Draw the shortcut character
                    if self.has_prelight:
                        color_shortcut = self.style.color(fg=(255, 255, 0), bg=(0, 0, 0), attributes=True)
                    else:
                        color_shortcut = self.color_normal

                    if title["position"] is not None:
                        self.add_character(
                            y=0,
                            x=self.list_machin[count]["start"] + 1 + title["position"],
                            character=title["text"][title["position"]],
                            color=color_shortcut,
                        )
                    # Draw one dark after
                    self.add_character(
                        y=0,
                        x=self.list_machin[count]["start"] + 1 + len(title["text"]),
                        character=" ",
                        color=self.color,
                    )
                count += 1

    def _coordinates_in_area(self, x, y):
        y -= self.y
        x -= self.x
        if (0 <= y <= self.height - 1) and (0 <= x <= self.width - 1):
            return True

        return False

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            if self._coordinates_in_area(x, y):
                # We are sure about the ToolBar have been clicked
                self.emit("grab-focus", {"id": self.id})
                if self.children is not None:
                    count = 0
                    y -= self.y
                    x -= self.x
                    for child in self.children:
                        if (
                                self.list_machin[count]["start"]
                                <= x
                                <= self.list_machin[count]["start"]
                                + len(child.widget.title)
                        ):
                            self.selected_menu = count
                            # GLXCurses.Application().has_prelight = child.widget.children[0].widget
                            try:
                                self.emit(
                                    "CLAIM_PRELIGHT",
                                    {"id": child.widget.children[0].widget.id},
                                )
                            except IndexError:
                                pass

                            if (
                                    event == GLXCurses.GLXC.BUTTON1_CLICKED
                                    or event == BUTTON1_RELEASED
                            ):
                                self.emit(
                                    "BUTTON1_CLICKED",
                                    {
                                        "class": self.__class__.__name__,
                                        "id": self.id,
                                        "event_signal": "BUTTON1_CLICKED",
                                    },
                                )
                        count += 1

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.can_focus and self.has_focus:
            # setting
            key = event_args[0]
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.selected_menu = 0
                self.selected_menu_item = 0

                self.emit("RELEASE_FOCUS", {"id": self.id})
                self.emit("RELEASE_PRELIGHT", {"id": self.id})
                self.emit("RELEASE_DEFAULT", {"id": self.id})

            if key == KEY_RIGHT:
                if self.selected_menu + 1 > len(self.children) - 1:
                    self.selected_menu = 0
                    self.selected_menu_item = 0
                else:
                    self.selected_menu += 1
                    self.selected_menu_item = 0
                try:
                    self.emit(
                        "CLAIM_PRELIGHT",
                        {
                            "id": self.children[self.selected_menu]
                                .widget.children[0]
                                .widget.id
                        },
                    )
                    self.emit(
                        "CLAIM_DEFAULT",
                        {
                            "id": self.children[self.selected_menu]
                                .widget.children[0]
                                .widget.id
                        },
                    )
                except IndexError:
                    pass

            if key == KEY_LEFT:
                if self.selected_menu - 1 < 0:
                    self.selected_menu = len(self.children) - 1
                    self.selected_menu_item = 0
                else:
                    self.selected_menu -= 1
                    self.selected_menu_item = 0
                try:
                    self.emit(
                        "CLAIM_PRELIGHT",
                        {
                            "id": self.children[self.selected_menu]
                                .widget.children[0]
                                .widget.id
                        },
                    )
                    self.emit(
                        "CLAIM_DEFAULT",
                        {
                            "id": self.children[self.selected_menu]
                                .widget.children[0]
                                .widget.id
                        },
                    )
                except IndexError:
                    pass

            if self.children and (key == KEY_UP or key == KEY_DOWN):
                for child in self.children:
                    if child.properties.position == self.selected_menu:
                        if child.widget.children:
                            if key == KEY_UP:
                                if self.selected_menu_item - 1 < 0:
                                    self.selected_menu_item = (
                                            len(child.widget.children) - 1
                                    )
                                else:
                                    self.selected_menu_item -= 1

                            if key == KEY_DOWN:
                                if (
                                        self.selected_menu_item + 1
                                        > len(child.widget.children) - 1
                                ):
                                    self.selected_menu_item = 0
                                else:
                                    self.selected_menu_item += 1
                            try:
                                self.emit(
                                    "CLAIM_PRELIGHT",
                                    {
                                        "id": child.widget.children[
                                            self.selected_menu_item
                                        ].widget.id
                                    },
                                )
                                self.emit(
                                    "CLAIM_DEFAULT",
                                    {
                                        "id": child.widget.children[
                                            self.selected_menu_item
                                        ].widget.id
                                    },
                                )
                            except IndexError:
                                pass
