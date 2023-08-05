#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


# Inspired from: https://developer.gnome.org/gtk3/stable/GtkTextTag.html
# Inspired from: https://developer.gnome.org/pygtk/stable/class-gtktexttag.html


class TextTag(GLXCurses.Object):
    def __init__(self):
        """
        You may wish to begin by reading the text widget conceptual overview which gives an overview of all the
        objects and data types related to the text widget and how they work together.

        Tags should be in the TextTagTable for a given TextBuffer before using them with that buffer.

        For each property of TextTag, there is a “set” property, e.g. “font-set” corresponds to “font”.
        These “set” properties reflect whether a property has been set or not.

        They are maintained by GLXCurses and you should not set them independently.
        """
        GLXCurses.Object.__init__(self)
        self.__accumulative_margin = None
        self.__background = None
        self.__background_full_height = None
        self.__background_full_height_set = None
        self.__background_rgb = None
        self.__background_set = None
        self.__direction = None
        self.__editable = None
        self.__editable_set = None
        self.__fallback = None
        self.__fallback_set = None
        self.__family = None
        self.__family_set = None
        self.__font = None
        self.__font_desc = None
        self.__font_features = None
        self.__font_features_set = None
        self.__foreground = None
        self.__foreground_rgb = None
        self.__foreground_set = None
        self.__indent = None
        self.__indent_set = None
        self.__invisible = None
        self.__invisible_set = None
        self.__justification = None
        self.__justification_set = None
        self.__language = None
        self.__language_set = None
        self.__left_margin = None
        self.__left_margin_set = None
        self.__letter_spacing = None
        self.__letter_spacing_set = None
        self.__name = None
        self.__paragraph_background = None
        self.__paragraph_background_rgb = None
        self.__paragraph_background_set = None
        self.__chars_above_lines = None
        self.__chars_above_lines_set = None
        self.__chars_below_lines = None
        self.__chars_below_lines_set = None
        self.__chars_inside_wrap = None
        self.__chars_inside_wrap_set = None
        self.__right_margin = None
        self.__right_margin_set = None
        self.__rise = None
        self.__rise_set = None
        self.__scale = None
        self.__scale_set = None
        self.__size = None
        self.__size_points = None
        self.__size_set = None
        self.__stretch = None
        self.__stretch_set = None
        self.__strikethrough = None
        self.__strikethrough_rgb = None
        self.__strikethrough_rgb_set = None
        self.__strikethrough_set = None
        self.__style = None
        self.__style_set = None
        self.__tabs = None
        self.__tabs_set = None
        self.__underline = None
        self.__underline_rgb = None
        self.__underline_rgb_set = None
        self.__underline_set = None
        self.__variant = None
        self.__variant_set = None
        self.__weight = None
        self.__weight_set = None
        self.__wrap_mode = None
        self.__wrap_mode_set = None

        self.accumulative_margin = False
        self.background = "BLUE"
        self.background_full_height = False
        self.background_rgb = {"r": 0, "g": 0, "b": 255}
        self.background_set = False
        self.direction = GLXCurses.GLXC.TEXT_DIR_NONE
        self.editable = True
        self.editable_set = False

    @property
    def accumulative_margin(self):
        """
        Whether the margins accumulate or override each other.

        When set to ``True`` the margins of this tag are added to the margins of any other non-accumulative
        margins present.

        When set to ``False`` the margins override one another (the default).

        Default value is ``False`` and be restore when ``accumulative_margin`` is set to ``None``

        :return: If ``True`` the margins of this tag are added to the margins of any other non-accumulative
        :rtype: bool
        """
        return self.__accumulative_margin

    @accumulative_margin.setter
    def accumulative_margin(self, value=None):
        """
        Set the ``accumulative_margin`` property value

        :param value: If ``True`` the margins of this tag are added to the margins of any other non-accumulative
        :type value: boot or None
        :raise TypeError: When  ``accumulative_margin`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.accumulative_margin != value:
            self.__accumulative_margin = value

    @property
    def background(self):
        """
        Background color as a string.

        :return: color as a string
        :rtype: str
        """
        return self.__background

    @background.setter
    def background(self, value=None):
        """
        Set the ``background`` property value

        :param value: color as a string
        :type value: boot or None
        :raise TypeError: If ``background`` value is not a str type or None
        """
        if value is None:
            value = "BLUE"
        if type(value) != str:
            raise TypeError('"value" must be a str type or None')
        if self.background != value:
            self.__background = value

    @property
    def background_full_height(self):
        """
        Whether the background color fills the entire line height or only the height of the tagged characters.

        When set to ``True`` the background color fills the entire line height

        Default value is ``False`` and be restore when ``background_full_height`` is set to ``None``

        :return: If ``True`` the background color fills the entire line height
        :rtype: bool
        """
        return self.__background_full_height

    @background_full_height.setter
    def background_full_height(self, value=None):
        """
        Set the ``background_full_height`` property value

        :param value: If ``True`` the background color fills the entire line height
        :type value: boot or None
        :raise TypeError: When  ``background_full_height`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.background_full_height != value:
            self.__background_full_height = value

    @property
    def background_full_height_set(self):
        """
        Whether this tag affects background height.

        When set to ``True`` this tag affects background height

        Default value is ``False`` and be restore when ``background_full_height_set`` is set to ``None``

        :return: ``True`` If this tag affects background height
        :rtype: bool
        """
        return self.__background_full_height_set

    @background_full_height_set.setter
    def background_full_height_set(self, value=None):
        """
        Set the ``background_full_height_set`` property value

        :param value: If ``True``  this tag affects background height
        :type value: boot or None
        :raise TypeError: When  ``background_full_height_set`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError(
                '"background_full_height_set" value must be a bool type or None'
            )
        if self.background_full_height_set != value:
            self.__background_full_height_set = value

    @property
    def background_rgb(self):
        """
        Background color as a RGB.

        Default value is ``{'r': 0, 'g': 0, 'b': 255}`` and be restore when ``background_rgb`` is set to ``None``

        :return: The RGB color as dict with **r**, **g**, **b** key_name
        :rtype: dict
        """
        return self.__background_rgb

    @background_rgb.setter
    def background_rgb(self, value=None):
        """
        Set the ``background_full_height_set`` property value

        :param value: The RGB color as dict with **r**, **g**, **b** key_name
        :type value: dict or None
        :raise TypeError: When  ``background_rgb`` value is not a dict type or None
        """
        if value is None:
            value = {"r": 0, "g": 0, "b": 255}
        if type(value) != dict:
            raise TypeError('"background_rgb" value must be a dict type or None')
        if self.background_rgb != value:
            self.__background_rgb = value

    @property
    def background_set(self):
        """
        Whether this tag affects the background color.

        Default value is ``False`` and be restore when ``background_set`` is set to ``None``

        :return: If ``True``, this tag affects the background color
        :rtype: bool
        """
        return self.__background_set

    @background_set.setter
    def background_set(self, value=None):
        """
        Set the ``background_set`` property value

        :param value: If ``True``, this tag affects the background color
        :type value: boot or None
        :raise TypeError: When  ``background_set`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"background_set" value must be a bool type or None')
        if self.background_set != value:
            self.__background_set = value

    @property
    def direction(self):
        """
        Text direction, e.g. right-to-left -> 'RTL' or left-to-right -> 'LTR'.

        :return: GLXC.TextDirection direction type
        :rtype: str
        """
        return self.__direction

    @direction.setter
    def direction(self, value=None):
        """
        Set ``direction`` property value

        :param value: a GLXCurses.GLXC.TextDirection
        :type value: GLXCurses.GLXC.TextDirection or None
        """
        if value is None:
            value = GLXCurses.GLXC.TEXT_DIR_NONE
        if type(value) != str:
            raise TypeError('"direction" value must be a str type or None')
        if value.lower() == "right-to-left":
            value = GLXCurses.GLXC.TEXT_DIR_RTL
        if value.lower() == "left-to-right":
            value = GLXCurses.GLXC.TEXT_DIR_LTR
        if not value.upper() in GLXCurses.GLXC.TextDirection:
            raise TypeError('"direction" value must a valid GLXC.TextDirection or None')
        if self.direction != value.upper():
            self.__direction = value.upper()

    @property
    def editable(self):
        """
        Whether the text can be modified by the user.

        Default value is ``True`` and be restore when ``editable`` is set to ``None``

        :return: If ``True``, the text can be modified by the user.
        :rtype: bool
        """
        return self.__editable

    @editable.setter
    def editable(self, value=None):
        """
        Set the ``editable`` property value

        :param value: If ``True``, the text can be modified by the user.
        :type value: boot or None
        :raise TypeError: When ``editable`` value is not a bool type or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"editable" value must be a bool type or None')
        if self.editable != value:
            self.__editable = value

    @property
    def editable_set(self):
        """
        Whether this tag affects text editability.

        Default value is ``False`` and be restore when ``editable_set`` is set to ``None``

        :return: If ``False``, text editability is disable
        :rtype: bool
        """
        return self.__editable_set

    @editable_set.setter
    def editable_set(self, value=None):
        """
        Set the ``editable_set`` property value

        :param value: If ``False``, text editability is disable.
        :type value: boot or None
        :raise TypeError: When ``editable_set`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"editable_set" value must be a bool type or None')
        if self.editable_set != value:
            self.__editable_set = value

    @property
    def family(self):
        """
        Name of the font family, e.g. Sans, Helvetica, Times, Monospace.

        Default value is ``None`` and be restore when ``family`` is set to ``None``

        :return: The font family name
        :rtype: str or None
        """
        return self.__family

    @family.setter
    def family(self, value=None):
        """
        Set the ``editable`` property value

        :param value: The font family name
        :type value: str or None
        :raise TypeError: When ``family`` value is not a bool type or None
        """
        if value is None:
            value = True
        if type(value) != str:
            raise TypeError('"family" value must be a str type or None')
        if self.family != value:
            self.__family = value

    @property
    def family_set(self):
        """
        Whether this tag affects the font family.

        Default value is ``False`` and be restore when ``editable_set`` is set to ``None``

        :return: If ``False``, text editability is disable
        :rtype: bool
        """
        return self.__family_set

    @family_set.setter
    def family_set(self, value=None):
        """
        Set the ``family_set`` property value

        :param value: If ``False``, text editability is disable.
        :type value: boot or None
        :raise TypeError: When ``editable_set`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"family_set" value must be a bool type or None')
        if self.family_set != value:
            self.__family_set = value
